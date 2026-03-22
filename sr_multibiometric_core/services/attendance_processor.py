import logging

_logger = logging.getLogger(__name__)


class AttendanceProcessor:
    """Convert raw biometric logs into hr.attendance records."""

    @classmethod
    def process_logs(cls, env, limit=100):
        Log = env['biometric.log']
        Employee = env['hr.employee']
        Attendance = env['hr.attendance']

        # Process in sudo mode to avoid user-specific access issues in cron context.
        Log_sudo = Log.sudo()
        Employee_sudo = Employee.sudo()
        Attendance_sudo = Attendance.sudo()

        logs = Log_sudo.search([('processed', '=', False)], order='timestamp asc', limit=limit)
        if not logs:
            return 0

        processed_count = 0
        employee_cache = {}

        _logger.info('Processing %d biometric logs...', len(logs))

        for log in logs:
            error_message = False
            try:
                # Ensure every log is isolated so a single failure does not block the batch.
                with env.cr.savepoint():
                    log = Log_sudo.browse(log.id).exists()
                    if not log or log.processed:
                        continue

                    emp = employee_cache.get(log.device_user_id)
                    if not emp:
                        emp = Employee_sudo.search([('biometric_id', '=', log.device_user_id)], limit=1)
                        if emp:
                            employee_cache[log.device_user_id] = emp
                        else:
                            error_message = 'No employee found for biometric_id %s' % log.device_user_id

                    if not emp:
                        # Keep the log pending until the employee biometric_id mapping exists.
                        _logger.info(
                            'Biometric log %s kept pending: no employee mapped to biometric_id %s',
                            log.id,
                            log.device_user_id,
                        )
                        continue

                    if emp:
                        # Idempotency: if attendance already has this exact timestamp, just mark processed.
                        same_ts = Attendance_sudo.search([
                            ('employee_id', '=', emp.id),
                            '|',
                            ('check_in', '=', log.timestamp),
                            ('check_out', '=', log.timestamp),
                        ], limit=1)

                        if not same_ts:
                            open_att = Attendance_sudo.search([
                                ('employee_id', '=', emp.id),
                                ('check_out', '=', False),
                            ], order='check_in desc', limit=1)

                            if open_att:
                                if log.timestamp > open_att.check_in:
                                    try:
                                        open_att.write({'check_out': log.timestamp})
                                    except Exception as exc:
                                        error_message = 'overlap/close error: %s' % str(exc)
                                else:
                                    error_message = 'out-of-order timestamp for open attendance'
                            else:
                                # Avoid overlap: do not create if timestamp is already covered by another attendance.
                                overlap = Attendance_sudo.search([
                                    ('employee_id', '=', emp.id),
                                    ('check_in', '<=', log.timestamp),
                                    '|',
                                    ('check_out', '=', False),
                                    ('check_out', '>=', log.timestamp),
                                ], limit=1)

                                if overlap:
                                    error_message = 'overlap detected; attendance not created'
                                else:
                                    try:
                                        Attendance_sudo.create({
                                            'employee_id': emp.id,
                                            'check_in': log.timestamp,
                                        })
                                    except Exception as exc:
                                        error_message = 'create error: %s' % str(exc)

                    vals = {'processed': True}
                    if error_message and 'error_message' in log._fields:
                        vals['error_message'] = error_message
                    log.write(vals)

                if error_message:
                    _logger.warning('Biometric log %s processed with warning: %s', log.id, error_message)
                processed_count += 1

                if processed_count % 100 == 0:
                    env.cr.commit()

            except Exception as e:
                _logger.error('Error processing biometric log ID %s: %s', log.id, str(e))
                # Never leave a problematic log pending forever.
                try:
                    with env.cr.savepoint():
                        failed_log = Log_sudo.browse(log.id).exists()
                        if failed_log and not failed_log.processed:
                            vals = {'processed': True}
                            if 'error_message' in failed_log._fields:
                                vals['error_message'] = 'processor_exception: %s' % str(e)
                            failed_log.write(vals)
                            processed_count += 1
                except Exception:
                    _logger.exception('Failed to mark biometric log %s as processed after exception.', log.id)

        env.cr.commit()
        _logger.info('Successfully processed %d logs out of %d.', processed_count, len(logs))
        return processed_count

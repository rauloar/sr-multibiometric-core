from odoo import models, fields, api

class BiometricLog(models.Model):
    _name = 'biometric.log'
    _description = 'Biometric Raw Attendance Log'
    _order = 'timestamp desc'
    _rec_name = 'device_user_id'

    device_id = fields.Many2one(
        comodel_name='biometric.device',
        string='Device',
        required=True,
        ondelete='cascade',
        index=True,
    )
    device_user_id = fields.Char(
        string='Device User ID',
        required=True,
        index=True,
    )
    timestamp = fields.Datetime(
        string='Event Timestamp',
        required=True,
        index=True,
    )
    punch = fields.Selection(
        selection=[
            ('check_in', 'Check-In'),
            ('check_out', 'Check-Out'),
        ],
        string='Punch Type',
        required=True,
    )
    raw_data = fields.Text(string='Raw Payload')
    processed = fields.Boolean(
        string='Processed',
        default=False,
        index=True,
    )

    _unique_device_log = models.Constraint(
        'UNIQUE(device_id, device_user_id, timestamp)',
        'A log entry for this device, user, and timestamp already exists.',
    )

    @api.model
    def cron_process_logs(self):
        """Called by the ir.cron to process raw logs into hr.attendance."""
        from ..services.attendance_processor import AttendanceProcessor
        AttendanceProcessor.process_logs(self.env, limit=100)

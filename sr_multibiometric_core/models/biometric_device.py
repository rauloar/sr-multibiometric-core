import logging
from odoo import models, fields, api, _

class BiometricDevice(models.Model):
    _name = 'biometric.device'
    _description = 'Biometric Attendance Device'
    _order = 'name'

    name = fields.Char(string='Device Name', required=True)
    driver_id = fields.Many2one(
        'biometric.driver',
        string='Device Brand',
        required=True,
        ondelete='restrict',
    )
    device_type = fields.Char(
        string='Device Type',
        related='driver_id.tech_key',
        store=True,
        readonly=True,
    )
    driver_installed = fields.Boolean(
        string='Driver Installed',
        related='driver_id.is_installed',
    )
    ip = fields.Char(string='IP Address', required=True)
    port = fields.Integer(string='TCP Port', required=True, default=4370)
    username = fields.Char(string='Username')
    password = fields.Char(string='Password')
    location = fields.Char(string='Location')
    sync_interval = fields.Integer(string='Sync Interval (min)', default=5)
    auto_sync = fields.Boolean(string='Auto Sync', default=True)
    last_sync = fields.Datetime(string='Last Sync', readonly=True)
    status = fields.Selection(
        selection=[
            ('online', 'Online'),
            ('offline', 'Offline'),
            ('error', 'Error'),
        ],
        string='Status',
        default='offline',
        readonly=True,
    )
    timezone = fields.Char(string='Device Timezone', default='UTC')
    sdk_mode = fields.Selection(
        [
            ('auto', 'Auto'),
            ('sdk', 'Real SDK'),
            ('fake', 'Fake / Demo'),
        ],
        default='auto',
        string='SDK Mode',
    )
    active = fields.Boolean(default=True)
    log_count = fields.Integer(string='Log Count', compute='_compute_log_count')

    def _compute_log_count(self):
        Log = self.env['biometric.log']
        for device in self:
            device.log_count = Log.search_count([('device_id', '=', device.id)])

    def action_view_logs(self):
        """Open all biometric logs for this device."""
        self.ensure_one()
        return {
            'name': _('Biometric Logs'),
            'type': 'ir.actions.act_window',
            'res_model': 'biometric.log',
            'view_mode': 'list,form',
            'domain': [('device_id', '=', self.id)],
        }

    def action_install_driver(self):
        """Open the driver installation wizard for the selected brand."""
        self.ensure_one()
        return {
            'name': _('Install Driver'),
            'type': 'ir.actions.act_window',
            'res_model': 'biometric.driver.install.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_driver_id': self.driver_id.id},
        }

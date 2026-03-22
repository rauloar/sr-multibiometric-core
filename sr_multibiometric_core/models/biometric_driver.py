from odoo import models, fields


class BiometricDriver(models.Model):
    _name = 'biometric.driver'
    _description = 'Biometric Device Driver'
    _order = 'name'

    name = fields.Char(string='Brand Name', required=True)
    tech_key = fields.Char(
        string='Technical Key',
        required=True,
        help='Internal key used to route actions to the correct driver (e.g. zkteco).',
    )
    module_name = fields.Char(
        string='Module Name',
        required=True,
        help='Name of the Odoo module that implements this driver (e.g. sr_multibiometric_zkteco).',
    )
    is_installed = fields.Boolean(
        string='Driver Installed',
        compute='_compute_is_installed',
    )

    def _compute_is_installed(self):
        ModuleModel = self.env['ir.module.module']
        for driver in self:
            module = ModuleModel.search([('name', '=', driver.module_name)], limit=1)
            driver.is_installed = module.state == 'installed' if module else False

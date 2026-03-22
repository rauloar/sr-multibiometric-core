from odoo import models, fields, _


class BiometricDriverInstallWizard(models.TransientModel):
    _name = 'biometric.driver.install.wizard'
    _description = 'Install Biometric Driver'

    driver_id = fields.Many2one('biometric.driver', string='Driver', readonly=True, required=True)
    module_name = fields.Char(related='driver_id.module_name', readonly=True)

    def action_install_driver(self):
        self.ensure_one()
        module = self.env['ir.module.module'].search(
            [('name', '=', self.driver_id.module_name)], limit=1
        )
        if not module:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Driver module unavailable'),
                    'message': _(
                        'Se requiere un módulo driver adicional.\n\n'
                        'Este software se distribuye bajo licencia LGPL-3.\n'
                        'NO SE PROPORCIONA GARANTÍA.\n'
                        'El driver puede requerir un acuerdo comercial.'
                    ),
                    'type': 'warning',
                    'sticky': True,
                },
            }
        return module.button_immediate_install()

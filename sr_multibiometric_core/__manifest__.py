{
    'name': 'SR Multibiometric Core',
    'version': '19.0.1.0.0',
    'category': 'Human Resources/Attendance',
    'summary': 'Core module for multi-brand biometric attendance integration',
    'description': (
        'Main module providing the base architecture to connect various brands of biometric terminals to Odoo HR Attendance.\n'
        '\n'
        'This module is part of the SR Multibiometric suite.\n'
        'Distributed under the GNU LGPL-3 license. Commercial services are allowed.\n'
        'Driver modules are distributed separately.'
    ),
    'author': 'SR',
    'website': 'https://sr.local',
    'images': ['static/description/icon.png'],
    'license': 'LGPL-3',
    'application': True,
    'installable': True,
    'depends': [
        'hr',
        'hr_attendance',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/biometric_drivers.xml',
        'views/biometric_menu.xml',
        'views/biometric_device_views.xml',
        'views/biometric_log_views.xml',
        'wizards/driver_install_wizard_views.xml',
    ],
}

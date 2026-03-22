# Server Setup Guide

Place the module folder directly into your standard Odoo addons environment.

Example path layout:
`/opt/odoo/custom-addons/sr_multibiometric_core`

Ensure the Odoo system user has appropriate filesystem boundaries mapped.

```bash
sudo chown -R odoo:odoo /opt/odoo/custom-addons/sr_multibiometric_core
sudo chmod -R 755 /opt/odoo/custom-addons/sr_multibiometric_core
```

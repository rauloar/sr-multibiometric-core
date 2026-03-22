# Odoo Configuration Guide

Ensure your primary `odoo.conf` routing files recognise the directory where the SR Multibiometric modules are placed.

Example standard configuration mapping:
```ini
addons_path = /opt/odoo/odoo/addons,/opt/odoo/custom-addons
```

After modifying the configuration or dumping a new module folder, safely restart your service manager:
```bash
sudo systemctl restart odoo
```

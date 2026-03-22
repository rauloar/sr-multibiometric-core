# Driver Installation

Specific hardware drivers (e.g., `sr_multibiometric_zkteco`) are distributed separately and must be loaded via the standard Odoo module manager.

1. Unzip the desired driver folder into the same `addons_path` next to the core module.
2. Formally restart the Odoo service.
3. Activate Developer Mode via the Odoo Settings menu.
4. Open the **Apps** window and click **Update Apps List**.
5. Remove the default "Apps" filter from the search bar (as drivers are technically background modules).
6. Search for your specific hardware ingestor (e.g., `sr_multibiometric_zkteco`) and click **Install**.

*Disclaimer: Driver components may require a commercial agreement. Installation services are not included. LGPL-3. NO WARRANTY.*

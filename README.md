# Simple dashboard for my vps
Contains simple pastebin and works closely with [vps-wake-on-lan-no-ssh](https://github.com/AlexSzczygielski/vps-wake-on-lan-no-ssh). It uses the same `.wol_env` file. Configuration is available inside [dashboard-config json](dashboard_config.json).

Remember to run this on different port than vps-wake-on-lan-no-ssh app.
Remember to add `PASTEBIN_PASSWORD=` with password content to the `.wol_env` file.

```bash
cd vps-dashboard
gunicorn -b 0.0.0.0:VPS-DASHBOARD_PORT_HERE run:app
```
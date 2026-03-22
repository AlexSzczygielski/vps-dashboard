# Simple dashboard for my vps
<div align="center">

[![Python](https://img.shields.io/badge/Backend-Python-blue?logo=python&logoColor=yellow)](https://www.python.org)  [![Flask](https://img.shields.io/badge/Web_Framework-Flask-red?logo=flask)](https://flask.palletsprojects.com/)   [![Mikrus](https://img.shields.io/badge/Hardware-Mikrus-green)](https://frog.mikr.us)
</div>

Contains simple pastebin and works closely with [vps-wake-on-lan-no-ssh](https://github.com/AlexSzczygielski/vps-wake-on-lan-no-ssh). It uses the same `.wol_env` file. Configuration is available inside [dashboard-config json](dashboard_config.json).

Remember to run this on different port than vps-wake-on-lan-no-ssh app.
Remember to add `PASTEBIN_PASSWORD=` with password content to the `.wol_env` file.

```bash
cd vps-dashboard
gunicorn -b 0.0.0.0:VPS-DASHBOARD_PORT_HERE run:app
```

---

<div align="center">
<img width = 80%  src= "https://frog02-30432.wykr.es/demo_assets/vps-dashboard-night-demo.png">
</div>
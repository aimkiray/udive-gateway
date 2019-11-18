# Taste Guide

> Based on CentOS 7 x64

Install dependencies

```bash
cd iot-server
pip install -r requirements.txt
```

Build tables

```bash
python manage.py db migrate
python manage.py db upgrade
```

Start server

```bash
python gate.py
```

Enjoy it!
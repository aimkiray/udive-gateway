# Taste Guide

> Based on CentOS 7 x64

Install dependencies

```bash
cd iot-server
pip install -r requirements.txt
```

Start server

```bash
python gate.py
```

build two tables

```sql
CREATE TABLE IF NOT EXISTS `user`(
   `user_id` INT UNSIGNED AUTO_INCREMENT,
   PRIMARY KEY ( `user_id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `gate`(
   `gate_id` INT UNSIGNED AUTO_INCREMENT,
   PRIMARY KEY ( `gate_id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
```

Enjoy it!
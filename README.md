# eth-audit
python worker to extract to DB normal and erc20 txs from an ETH account/address

DB in use is mysql

# STEPS TO GRANT PRIVILEGES ON MYSQL
1. login as root: sudo su
2. access mysql: mysql
3. select user from mysql.user;
4. create user 'stephen'@'localhost' identified by 'somepassword';
5. grant all privileges on * . * to  'stephen'@'localhost';
6. flush privileges;
7. now login as stephen: sudo su -l stephen
8. mysql -u stephen -p
9. password: somepassword

# STEPS TO INSTALL PYTHON ENV - ARCH LINUX
1. sudo pacman -S python-pip
2. python -m venv my_env

# ALLOW .SH EXECUTION
1. chmod +x audit.sh

# SYSTEMD LOCATION
1. /lib/systemd/system/eth-worker.service

# SYSTEMD SCRIPT
[Unit]
Description=Python ETH Tx Extraction
Requires=network.target
After=network.target
ConditionPathExists=/home/stephen/eth-audit/audit.sh

[Service]
Type=simple
User=stephen
Group=stephen
WorkingDirectory=/home/stephen/eth-audit
ExecStart=/home/stephen/eth-audit/audit.sh
Restart=always
RestartSec=300

[Install]
WantedBy=multi-user.target
Alias=eth-worker.service

# SYSTEMD ACTIVATION
1. systemctl status eth-worker
2. systemctl start eth-worker
3. systemctl restart eth-worker
4. sudo systemctl enable eth-worker
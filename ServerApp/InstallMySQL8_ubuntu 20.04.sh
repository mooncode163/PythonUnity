# https://www.linuxidc.com/Linux/2018-11/155408.htm
# https://blog.csdn.net/WANG_yu09/article/details/82709233
# 20.04 mysql 默认是8.0
sudo apt-get install lsb-release
sudo apt update
sudo apt-get install mysql-server
mysql_secure_installation

sudo apt-get install libmysqlclient-dev
pip3 install mysql
sudo apt-get install git
 
sudo cat /etc/mysql/debian.cnf
mysql -u debian-sys-maint -p 
sCFS9l8aL5dQZLsQ
 
sudo service mysql restart
mysql -u root -p

# 设置远程登录
use mysql;
select host, user, authentication_string, plugin from user;
update user set host='%' where user='root';
flush privileges;


MySql8.0修改root密码
https://blog.csdn.net/wolf131721/article/details/93004013
use mysql;
update user set authentication_string='' where user='root';
flush privileges;

SHOW VARIABLES LIKE 'validate_password%'; 
set global validate_password.policy=0;
 
ALTER USER 'root'@'%' IDENTIFIED WITH mysql_native_password BY 'qianlizhiwai';
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'qianlizhiwai';
 
flush privileges;
exit;
sudo service mysql restart



 


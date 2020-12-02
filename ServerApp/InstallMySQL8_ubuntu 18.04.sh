# https://www.linuxidc.com/Linux/2018-11/155408.htm
# https://blog.csdn.net/WANG_yu09/article/details/82709233

sudo apt-get install lsb-release

彻底删除mydql5.7

sudo apt-get autoremove --purge mysql-server-5.7 
sudo apt-get remove mysql-server         
sudo apt-get autoremove mysql-server  
sudo apt-get remove mysql-common
sudo rm -rf /etc/mysql/  /var/lib/mysql    #重要
dpkg -l |grep ^rc|awk '{print $2}' |sudo xargs dpkg -P    #清理残留数据
sudo apt autoremove


wget -c https://dev.mysql.com/get/mysql-apt-config_0.8.10-1_all.deb
sudo dpkg -i mysql-apt-config_0.8.10-1_all.deb
sudo apt update
sudo apt-get install mysql-server

sudo apt-get install libmysqlclient-dev

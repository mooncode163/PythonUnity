# https://www.linuxidc.com/Linux/2018-11/155408.htm

sudo apt update
sudo apt-get install git

sudo apt-get remove python3.6

sudo apt-get install python3.7

3. 调整Python3的优先级，使得3.7优先级较高 
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.7 1

7.建立新的指向python3.7的软链接
#添加python3的软链接
ln -s /usr/local/python3/bin/python3.7 /usr/bin/python3
#添加 pip3 的软链接
ln -s /usr/local/python3/bin/pip3.7 /usr/bin/pip3

sudo apt-get install python3-pip

#!/bin/sh 
# 方法2：
# /etc/init.d 开机自动执行脚本 将这个脚本放到 /etc/init.d 下
# https://www.jianshu.com/p/004e57d6a168
# cd /etc/init.d/
# update-rc.d autorun.sh defaults

# 放在/etc/init.d/下的脚本不能自动执行
# 要在/etc/rc2.d/下创建软连接  cd /etc/rc2.d/　sudo ln -s /etc/init.d/autorun.sh ./S01autorun.sh ，测试后，正常启动了(S表示开始)。
# autorun.sh 需要可执行权限

# vnc


sh /var/www/html/PythonUnity/ServerApp/ServerLaunch.sh

# vnc
# vncserver :1
# vncconfig

# ubuntu安装nginx
# sudo apt-get install nginx
# service nginx start


# Terminator安装
# http://www.manongjc.com/article/40690.html
# sudo add-apt-repository ppa:gnome-terminator
# sudo apt-get update
# sudo apt-get install terminator
# 如果你要移除Terminator，卸载命令:

# sudo apt-get remove terminator
# 安装完成后按 ctrl+alt+t，就会运行Terminator窗口

# vnc
# 用VNC搭建Ubuntu VNC可视化界面
# https://help.aliyun.com/knowledge_detail/59330.html
# vnc 复制粘贴  在linux执行vncconfig
# vncserver -kill :1
# vncserver :1
# vncconfig


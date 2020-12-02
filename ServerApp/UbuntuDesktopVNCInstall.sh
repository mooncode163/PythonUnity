#!/bin/sh

# 用VNC搭建Ubuntu VNC可视化界面
#  https://help.aliyun.com/knowledge_detail/59330.html

apt-get update
apt-get install vnc4server
vncserver   (设置密码 qianli)
sudo apt-get install x-window-system-core
sudo apt-get install gdm3
sudo apt-get install ubuntu-desktop
sudo apt-get install gnome-panel gnome-settings-daemon metacity nautilus gnome-terminal
sudo apt-get install terminator


# x11vnc
# Ubuntu 20.04 VNC 安装与设置
# https://blog.csdn.net/bluewhalerobot/article/details/106770429


vncserver -kill :1
vncserver :1

# Terminator安装
# http://www.manongjc.com/article/40690.html
# sudo add-apt-repository ppa:gnome-terminator
# sudoapt-get update
# sudo apt-get install terminator
# 如果你要移除Terminator，卸载命令:
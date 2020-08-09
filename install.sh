#!/usr/bin/env bash

# Install pip3
sudo apt-get install python3-pip

# Install mysql 5.7
echo 'deb http://repo.mysql.com/apt/ubuntu/ trusty mysql-5.7-dmr' | sudo tee -a /etc/apt/sources.list
sudo apt-get update
sudo apt-get install mysql-server-5.7

# Install MySQLdb version 1.3.x
sudo apt-get install python3-dev
sudo apt-get install libmysqlclient-dev
sudo apt-get install zlib1g-dev
sudo pip3 install mysqlclient==1.3.10


# Install SQLAlchemy
sudo pip3 install SQLAlchemy==1.2.5

# Install flask, flask_cors and other require modules for python
sudo pip3 install flask
sudo pip3 install requests
sudo pip3 install flask_cors
sudo pip3 install flasgger
sudo pip3 install pathlib2

#!/bin/bash
# Debian
# From Docker python

change mirrors
apt-get install apt-transport-https ca-certificates
cp -a /etc/apt/sources.list /etc/apt/sources.list.bak
cp -a /Judger/include/sources.list /etc/apt/sources.list


# update packs
apt update
apt upgrade -y

apt install libseccomp-dev -y
apt install expect -y

# install python path
apt install python2 -y

cd /Judger

# install mysql
apt install mysql-common -y

# install java
apt install openjdk-17-jdk -y
apt install openjdk-17-jre -y

# set python pip
python3 -m pip config set global.index-url https://repo.huaweicloud.com/repository/pypi/simple
python3 -m pip config set global.trusted-host  repo.huaweicloud.com
python3 -m pip install -U pip



# set serve path
python3 -m pip install -r requirements.txt

# install pascal
cd /Judger/include
tar -xvf fpc-3.2.2.x86_64-linux.tar
cd fpc-3.2.2.x86_64-linux

expect -c "
    spawn ./install.sh;
    expect {
        *\[/usr\]*: {
            send \"\r\";
            exp_continue;
        }
        *\(Y/n\)*: {
            send \"Y\r\";
            exp_continue;
        }
        *\[/usr/share/doc/fpc-3.2.2/examples\]*: {
            send \"\r\";
            exp_continue;
        }
    }
"


# remove pascal packs
cd /Judger/include
rm -rf fpc-3.2.2.x86_64-linux
cd /Judger

# start Client
python client.py
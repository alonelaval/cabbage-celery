#/bin/bash

set -e 
sudo yum -y install epel-release
sudo yum -y install gcc gcc-c++ kernel-devel
sudo yum -y install python-devel libxslt-devel libffi-devel openssl-devel
sudo yum -y install freetype-devel fontconfig-devel 
sudo yum -y install MySQL-python
sudo yum -y install python-pip
sudo yum -y install unzip
sudo yum -y install zip 
sudo yum -y install byobu

sudo pip install -i https://pypi.douban.com/simple --upgrade pytesseract
sudo pip install -i https://pypi.douban.com/simple --upgrade Image
sudo pip install -i https://pypi.douban.com/simple --upgrade bs4




sudo pip install -i https://pypi.douban.com/simple --upgrade redis

#
sudo pip install -i https://pypi.douban.com/simple --upgrade pip
sudo pip install -i https://pypi.douban.com/simple --upgrade setuptools
sudo pip install -i https://pypi.douban.com/simple --upgrade tornado
sudo pip install -i https://pypi.douban.com/simple --upgrade torndsession
#
sudo pip install -i https://pypi.douban.com/simple --upgrade SQLAlchemy
sudo pip install -i https://pypi.douban.com/simple --upgrade html5lib
sudo pip install -i https://pypi.douban.com/simple --upgrade selenium 
sudo pip install -i https://pypi.douban.com/simple --upgrade xlwt 
sudo pip install -i https://pypi.douban.com/simple --upgrade DBUtils 
sudo pip install -i https://pypi.douban.com/simple --upgrade BeautifulSoup 
sudo pip install -i https://pypi.douban.com/simple --upgrade beautifulsoup4
sudo pip install -i https://pypi.douban.com/simple --upgrade celery==3.1.24 
sudo pip install -i https://pypi.douban.com/simple --upgrade zope.event 
sudo pip install -i https://pypi.douban.com/simple --upgrade zope.interface 
sudo pip install -i https://pypi.douban.com/simple --upgrade gevent 
sudo pip install -i https://pypi.douban.com/simple --upgrade greenlet 
sudo pip install -i https://pypi.douban.com/simple --upgrade Beaker 
sudo pip install -i https://pypi.douban.com/simple --upgrade kazoo 
sudo pip install -i https://pypi.douban.com/simple --upgrade kombu==3.0.37
sudo pip install -i https://pypi.douban.com/simple --upgrade apscheduler  
sudo pip install -i https://pypi.douban.com/simple --upgrade requests
sudo pip install -i https://pypi.douban.com/simple --upgrade websocket
sudo pip install -i https://pypi.douban.com/simple --upgrade websocket-client
sudo pip install -i https://pypi.douban.com/simple --upgrade hdfs
#sudo pip uninstall -q Django 

#sudo unzip ~/cabbage_install/jdk1.6.0_45.zip -d /usr/local


#sudo pip install -i https://pypi.douban.com/simple --upgrade tensorflow
#sudo pip install -i https://pypi.douban.com/simple Keras==0.1.2
#sudo pip install -i https://pypi.douban.com/simple  -U numpy 
#sudo pip install -i https://pypi.douban.com/simple --upgrade JPype1
#sudo pip install -i https://pypi.douban.com/simple --upgrade h5py
#sudo pip install -i https://pypi.douban.com/simple --upgrade theano
#sudo pip install -i https://pypi.douban.com/simple --upgrade scipy



#java环境
#JAVA_COMMAND='
#export JAVA_HOME=/usr/local/jdk1.6.0_45
#export JAVA_BIN=/usr/local/jdk1.6.0_45/bin
#export PATH=$PATH:$JAVA_HOME/bin
#export CLASSPATH=.:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar
#export JAVA_HOME JAVA_BIN PATH CLASSPATH'
#
#
#cat >> ~/.bash_profile <<eof
#
#$JAVA_COMMAND
#
#eof
#
#source ~/.bash_profile



#sed -i '/export JAVA_HOME=\/usr\/local\/jdk1.6.0_45/d' ~/.bash_profile
#sed -i '/export JAVA_BIN=\/usr\/local\/jdk1.6.0_45\/bin/d' ~/.bash_profile
#sed -i '/export PATH=$PATH:$JAVA_HOME\/bin/d' ~/.bash_profile
#sed -i '/export CLASSPATH=.:$JAVA_HOME\/lib\/dt.jar:$JAVA_HOME\/lib\/tools.jar/d' ~/.bash_profile
#sed -i '/export JAVA_HOME JAVA_BIN PATH CLASSPATH/d' ~/.bash_profile



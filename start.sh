#!/bin/bash

VERSION=$(virtualenv --version | awk '{print $(NF-2);exit}')

var1=$(echo ${VERSION} | cut -f1 -d.)
var2="not found"

result=$(echo $var1 | grep "{$var2}")

if [[ "result" != "" ]] 
then
  echo "包含virtualenv,无需安装"
else
  echo "不包含virtualenv,安装中: pip3 install virtualenv"
  pip3 install virtualenv 
fi

vtwo=$(virtualenv --version | awk '{print $(NF-2);exit}')
var3=$(echo ${vtwo} | cut -f1 -d.)
if [ $var3 -ge 20 ]
then
  echo "no need"
  virtualenv processxlsx
else
  echo "need"
  virtualenv --no-site-packages processxlsx
fi

source /home/maninsuit/work/projects/cve/processxlsx/bin/activate

# check if need to install requests
NONEED=$(pip freeze | grep requests)
if [ $NONEED ]
then
  echo "no need to install requirements" 
else
  pip install -r requirements.txt
fi

#python3 cvestatus.py

#python3 pyexcel.py

python3 cmp.py

deactivate

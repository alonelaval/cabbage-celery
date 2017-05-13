#/bin/bash 


cpath=`pwd`
cd ..
p=`pwd`


cfgPath=$1
export PYTHONPATH=$PYTHONPATH:$p/src
echo $PYTHONPATH

python $p/src/com/pingansec/cabbage/monitor_server_main.py $cfgPath 

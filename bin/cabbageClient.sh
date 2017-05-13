#/bin/bash 

cpath=`pwd`
cd ..
p=`pwd`

cfgPath=$1
export C_FORCE_ROOT=true
export PYTHONPATH=$PYTHONPATH:$p/src
echo $PYTHONPATH

python $p/src/com/pingansec/cabbage/client_main.py $cfgPath
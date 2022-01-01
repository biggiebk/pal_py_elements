#!/usr/bin/bash
# A very poor script to manage mongod
# Mostly for test purposes, for a better script see the main project

# Set environment
environment=$1

# Lets source our envionment
mongo_home="mongo/$environment"
mongo_data="$environment/data"
mongo_log="$environment/logs"
mongo_conf="Projects/pal_py_elements/cfg/$environment/pal_mongodb.conf"
home=~
echo -e "ENVIORNMENT VARIABLES"
echo Home: $home
echo Enviornment: $environment
echo Mongo Home: $home/$mongo_home
echo Data: $home/$mongo_data
echo Log: $home/$mongo_log
echo Conf: $home/$mongo_conf

case $2 in

  'init')
    echo -e "\n Initializing DB for $environment"
    bin/init_elements_db.py $environment
  ;;

  'start')
    cd $home/$mongo_home
    echo -e "\nSTARTING"
    mongod --config $home/$mongo_conf
  ;;

  'stop')
    cd $home/$mongo_home
    echo -e "\nSTOPPING"
    mongod --config $home/$mongo_conf --shutdown
  ;;

  'reset')
    cd $home/$mongo_home
    echo -e "\nRESETING"
    mongod --config $home/$mongo_conf --shutdown >/dev/null 2>/dev/null
    mkdir -p $home/$environment >/dev/null 2>/dev/null
    rm -Rf data/*
    mkdir data >/dev/null 2>/dev/null
    mkdir logs >/dev/null 2>/dev/null
  ;;

  'reinit')
    base=`pwd`
    cd $home/$mongo_home
    echo -e "\nREINIT"
    mongod --config $home/$mongo_conf --shutdown >/dev/null 2>/dev/null
    mkdir -p $home/$environment >/dev/null 2>/dev/null
    rm -Rf data/*
    mkdir data >/dev/null 2>/dev/null
    mkdir logs >/dev/null 2>/dev/null
    mongod --config $home/$mongo_conf
    cd $base
    bin/init_elements_db.py $environment
  ;;

  'running')
    echo -e "\nRUNNING INSTANCES"
    ps -x |grep mongod |grep -v grep
  ;;

esac

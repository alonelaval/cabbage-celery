#!/bin/bash


ps -ef|grep cabbage/start.sh|awk '{print $2}'|xargs kill -9
ps -ef|grep cabbage/start.sh
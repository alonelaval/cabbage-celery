#!/bin/bash
sudo rabbitmqctl stop_app
sudo rabbitmqctl reset
sudo rabbitmqctl start_app

sudo rabbitmqctl add_user cabbage_celery cabbage_celery
sudo rabbitmqctl set_user_tags cabbage_celery administrator
sudo rabbitmqctl add_vhost cabbage_vhost

sudo rabbitmqctl set_permissions -p cabbage_vhost cabbage_celery ".*" ".*" ".*"
sudo rabbitmqctl list_vhosts
sudo rabbitmqctl list_permissions -p cabbage_vhost
sudo rabbitmqctl list_queues -p cabbage_vhost

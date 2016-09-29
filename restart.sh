#!/bin/sh
ps aux | grep 'manage' | awk '{print "kill -9 "$2";"}' | sh
echo 'restart'
nohup /root/project/blog_old/manage.py runserver 0.0.0.0:8001 &
echo 'finish!'
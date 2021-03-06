#!/bin/sh

/home/ejabberd/bin/ejabberdctl start;
/home/ejabberd/bin/ejabberdctl status;
CODE="$?";
while [ "$CODE" -ne "0" ] ; do
    /home/ejabberd/bin/ejabberdctl status;
    CODE="$?";
    sleep 1
done;
/home/ejabberd/bin/ejabberdctl register admin localhost password;

/home/ejabberd/bin/ejabberdctl register monitor localhost passw0rd;
/home/ejabberd/bin/ejabberdctl register monitor_0 localhost passw0rd;
/home/ejabberd/bin/ejabberdctl register monitor_1 localhost passw0rd;
/home/ejabberd/bin/ejabberdctl register monitor_2 localhost passw0rd;
/home/ejabberd/bin/ejabberdctl register monitor_3 localhost passw0rd;
/home/ejabberd/bin/ejabberdctl register monitor_4 localhost passw0rd;
/home/ejabberd/bin/ejabberdctl register monitor_5 localhost passw0rd;
/home/ejabberd/bin/ejabberdctl register monitor_6 localhost passw0rd;
/home/ejabberd/bin/ejabberdctl register monitor_7 localhost passw0rd;

/home/ejabberd/bin/ejabberdctl register analyser localhost passw0rd;
/home/ejabberd/bin/ejabberdctl register analyser_0 localhost passw0rd;
/home/ejabberd/bin/ejabberdctl register analyser_1 localhost passw0rd;
/home/ejabberd/bin/ejabberdctl register analyser_2 localhost passw0rd;
/home/ejabberd/bin/ejabberdctl register analyser_3 localhost passw0rd;
/home/ejabberd/bin/ejabberdctl register analyser_4 localhost passw0rd;
/home/ejabberd/bin/ejabberdctl register analyser_5 localhost passw0rd;
/home/ejabberd/bin/ejabberdctl register analyser_6 localhost passw0rd;
/home/ejabberd/bin/ejabberdctl register analyser_7 localhost passw0rd;


/home/ejabberd/bin/ejabberdctl register planner localhost passw0rd;
/home/ejabberd/bin/ejabberdctl register executor localhost passw0rd;

tail -f /home/ejabberd/logs/ejabberd.log
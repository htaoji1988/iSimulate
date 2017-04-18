ps -ef|grep "python startV2.py"|grep -v grep|awk '{print $2}'|xargs kill -9

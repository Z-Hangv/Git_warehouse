if [ $1 = "start" ];then
	echo start robot
	cd /root/xrobot/bin
	python run_robot.py   > /dev/null 2>&1 &
	sleep 1
elif [ $1 = "stop" ];then
	cd /root/xrobot/bin
	python stop_robot.py
else
	echo wrong, usage: robot start or robot stop
fi


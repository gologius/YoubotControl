#ROSControl
This script is an example of TCP client for rosbridge.

Install rosbridge on the remote machine.
$ sudo apt-get install ros-indigo-rosbridge-suite
$ sudo apt-get install ros-indigo-youbot-driver

Run the youbot driver and the rosbridge TCP server.
$ roscore
$ roslaunch rosbridge_server rosbridge_tcp.launch
$ sudo su - 
$ roslaunch youbot_driver_ros_interface youbot_driver.launch

# YoubotControl
This script is an example of TCP client for rosbridge.
C++ is windows only.

## Preparation in youbot
Install rosbridge on the remote machine.
```bash
$ sudo apt-get install ros-indigo-rosbridge-suite
$ sudo apt-get install ros-indigo-youbot-driver
```

Run the youbot driver and the rosbridge TCP server.
```bash
$ roscore
$ roslaunch rosbridge_server rosbridge_tcp.launch
$ sudo su -
$ roslaunch youbot_driver_ros_interface youbot_driver.launch
```

## Running

### Python
Then run ` Python/YoubotController.py` this script, and you can control the youbot.

### C++
open and run ` C++/KUKAControll/KUKAControll.sln`, you can control the youbot.

# -*- coding: utf-8 -*-
"""
This script is an example of TCP client for rosbridge.

Install rosbridge on the remote machine.
$ sudo apt-get install ros-indigo-rosbridge-suite
$ sudo apt-get install ros-indigo-youbot-driver

Run the youbot driver and the rosbridge TCP server.
$ roscore
$ roslaunch rosbridge_server rosbridge_tcp.launch
$ sudo su - 
$ roslaunch youbot_driver_ros_interface youbot_driver.launch

"""

import socket
import json

def make_message(twist):
    return json.dumps(dict(op='publish',
                           topic='/cmd_vel',
                           msg=twist))

def make_twist(x_lin, y_lin, z_lin, x_ang, y_ang, z_ang):
    return dict(linear=dict(x=x_lin, y=y_lin, z=z_lin),
                angular=dict(x=x_ang, y=y_ang, z=z_ang))

if __name__ == '__main__':
    host = '192.168.100.40'
    port = 9090
    lin_vel = 0.05
    ang_vel = 0.3

    sock = socket.socket()
    sock.connect((host, port))
    
    print "Use WASD keys (& Enter) to move the youbot."
    while True:
        x_lin = y_lin = 0.0
        
        key = raw_input()
        if key == 'w':
            x_lin = lin_vel
        elif key == 'a':
            y_lin = ang_vel
        elif key == 's':
            x_lin = -lin_vel
        elif key == 'd':
            y_lin = -ang_vel
        elif key == 'q':
            break;                
        else:
            continue
        
        twist = make_twist(x_lin, y_lin, 0.0, 0.0, 0.0, 0.0)
        message = make_message(twist)
        sock.send(message)
    
    #stop youbot
    twist = make_twist(0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    message = make_message(twist)
    sock.send(message)
    
    sock.close()

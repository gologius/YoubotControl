# -*- coding: utf-8 -*-
"""
------------------------------------------------------
This script is an example of TCP client for rosbridge.

Install rosbridge on the remote machine.
$ sudo apt-get install ros-indigo-rosbridge-suite

Run the turtlesim and the rosbridge TCP server.
$ roscore
$ roslaunch rosbridge_server rosbridge_tcp.launch
$ rosrun youbot_driv

Then run this script, and you can control the turtle.
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
    lin_vel = 0.2
    ang_vel = 0.3

    sock = socket.socket()
    sock.connect((host, port))

    """
    advertise = json.dumps(dict(op='advertise', 
                                topic='/turtle1/cmd_vel',
                                type='geometry_msgs/Twist'))
    sock.send(advertise)
    """

    
    print "Use WASD keys (& Enter) to move the youbot."
    while True:
        x_lin = z_ang = 0.0
        
        key = raw_input()
        if key == 'w':
            x_lin = lin_vel
        elif key == 'a':
            z_ang = ang_vel
        elif key == 's':
            x_lin = -lin_vel
        elif key == 'd':
            z_ang = -ang_
        elif key == 'q':
            break;                
        else:
            continue
        
        twist = make_twist(x_lin, 0.0, 0.0, 0.0, 0.0, z_ang)
        message = make_message(twist)
        sock.send(message)
    
    #stop
    twist = make_twist(0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    message = make_message(twist)
    sock.send(message)
    
    sock.close()

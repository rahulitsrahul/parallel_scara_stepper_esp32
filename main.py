from machine import Timer, Pin
import machine
import time
import utime
from actuator_stpr import *
from scara_kinematics import *
from robot import *
machine.freq(240000000)


if __name__ == "__main__":
    print("STARTED")
    # Initiate the elements of the Robot (Actuators, kinematics and robot_control)
    actuator = actuator_stpr()
    print("stepper_initiated")
    scara_kin = scara_kinematics(L0=50, L1=100, L2=100)
    print("scara_kinematics_initiated")
    robo = robot(actuator, scara_kin)
    print("Robot_Initiated")

    # Move the robot to position (x, y)
    print("Move robot to 50, 130")
    robo.move_robot(50, 130)
    while robo.is_moving():
        pass


    for _ in range(10):
        # Move the robot horizontal between (-50, 130) and (+50, 130) with the resolution of 2 units
        x_val = list(range(-90, 90, 5))
        y_val = [130]*len(x_val)

        for x,y in zip(x_val, y_val):
            # while robo.is_moving():
            #     pass
            robo.move_robot(x, y)

        x_val = list(range(90, -90, -5))
        y_val = [130]*len(x_val)

        for x,y in zip(x_val, y_val):
            # while robo.is_moving():
            #     pass
            robo.move_robot(x, y)

    
    
    
    # for _ in range(20):
    #     robo.move_robot(50, 130)
    #     while robo.is_moving():
    #         pass
    #     robo.move_robot(-50, 130)
    #     while robo.is_moving():
    #         pass





    
    



  


    




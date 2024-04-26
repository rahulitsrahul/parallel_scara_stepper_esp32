class robot(object):
    def __init__(self, actuator, kinematics):
        self.actuator = actuator
        self.kinematics = kinematics
        self.is_waiting_for_prev_stpes_completion = False

        """
        when both the links are vertical (90 deg), the x, y positions are [0, 186.6] for L0=50, L1=100, L2= 100
        This may vary for actual robot limit switch positions
        """
        self.initiate_actuators(x=0, y=186.6)    
    
    def initiate_actuators(self, x, y):
        # Here, essentially the robot links hit the limit switches and move to the zero positions of the actuators 
        print("POS: ", self.actuator.current_pos)
        
        # Move the stepper motor to 90 deg and set the current step position as [0, 0]
        self.actuator.move_stepper([0, 0])
        while self.is_moving():
            pass
        
        """
        Get the angles for the position x=0, y=186.6 and set them as initial actuator theta angles.
        This corresponds to for the pos x=0, y=186.6, the stepper motor positions are 0, 0
        """
        link_angles = self.kinematics.get_link_angles(x=x, y=y)
        print("angles for the position ",[x, y], ": ", link_angles)

        self.kinematics.init_theta_a1 = link_angles[0]
        self.kinematics.init_theta_a2 = link_angles[1]

        self.actuator.current_pos = [0, 0]
        
        # Wait till the previous execution is completed
        while self.actuator.timer_status:
            pass

        # Move the robot to 0, 130 for initialization
        self.move_robot(0, 130)
    

    def move_robot(self, x, y):
        # Get the steps required to move to position x, y
        steps_to_move = self.kinematics.get_steps_for_pos(x, y)
        
        # Receive the next position to move, perform calculations and wait till previous step execution
        while(self.is_moving()):
            pass
        
        # Move the actuators to reach the steps computed
        self.actuator.move_stepper(steps_to_move)


    def is_moving(self):
        return self.actuator.timer_status


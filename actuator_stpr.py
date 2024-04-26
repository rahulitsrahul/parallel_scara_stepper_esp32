from machine import Pin, Timer
import time
import utime

class actuator_stpr(object):
    def __init__(self):
        # Define the stepper motor step pins and direction pins
        self.step_pin = [Pin(19, Pin.OUT), Pin(14, Pin.OUT)]    # Define Step pins
        self.dir_pin = [Pin(18, Pin.OUT), Pin(12, Pin.OUT)]     # Define dir pins
        self.ena_pin = [Pin(21, Pin.OUT), Pin(13, Pin.OUT)]     # Define dir pins

        # Initialize the stepper pins to High/Low
        [pin.on() for pin in self.dir_pin]  # initialize dir pins
        [pin.off() for pin in self.ena_pin] # initalize enable pins
        [pin.on() for pin in self.step_pin] # initalize step pins
        
        self.num_steppers = len(self.step_pin)

        # Initialize the parameters
        self.current_pos = [-1, -1] # Counter which remembers the stepper position counts
        self.target_pos = [-1, -1]
        self.stepsPerRevolution = 200
        self.timer_status = False
        self.timer_0 = Timer(0)
        self.to_move = None # steps to move with sign (+/-)
        self.to_move_steps = None # steps to move without sign
        self.to_move_steps_indexes = None # list contain the sorted indexes from max to till min of the to_move_steps
        self.R = None # Ratio of max step / min step
        self.R = [None]*(self.num_steppers-1)
        self.c1 = None
        self.c2 = None
        self.counter = [1]*self.num_steppers
        self.init = True


    def move_stepper(self, target_pos):
        t1 = utime.ticks_us()
        # print("move stepper")
        self.timer_status = True
        self.target_pos = target_pos

        self.to_move = [current - targ for current, targ in zip(self.current_pos, self.target_pos)]
        self.to_move_steps = [abs(elem) for elem in self.to_move]

        self.to_move_steps_indexes = sorted(range(len(self.to_move_steps)), key=lambda i: self.to_move_steps[i], reverse=True)
        
        # Calculate R values, handling division by zero
        self.R = [self.to_move_steps[self.to_move_steps_indexes[0]] / max(self.to_move_steps[self.to_move_steps_indexes[i+1]], 1) if (i < len(self.to_move_steps_indexes) - 1) else 1 for i in range(len(self.to_move_steps_indexes))]

        # # in case of divisible by zero R[i] = 1
        # self.R = [self.to_move_steps[self.to_move_steps_indexes[0]] / self.to_move_steps[self.to_move_steps_indexes[i+1]] if (i < len(self.to_move_steps_indexes) - 1) and (self.to_move_steps[self.to_move_steps_indexes[i+1]]!=0) else 1 for i in range(len(self.R))]
        

        # Update direction pin to point to rotate either CW or CCW
        [pin.off() if move_val>0 else pin.on() for pin, move_val in zip(self.dir_pin, self.to_move)]

        # print("dir_1: ", self.dir_pin[0].value(), " dir_2 : ", self.dir_pin[1].value()) 

        self.counter = [1]*self.num_steppers
        self.init = True
        self.init_1 = True
        
        t2 = utime.ticks_us()
        print("time_elapsed_Init: ", t2-t1)

        self.timer_0.init(mode=Timer.PERIODIC, period=4, callback=self.run_stepper)
        

    def run_stepper(self, Timer):
        # print("RUN STEPPER Func")
        repeat = 1 if self.init else 1 # for the first call, run the loop for only once to compensate the computation
        # t1 = utime.ticks_us()
        for _ in range(repeat):
            for i in range(len(self.to_move_steps_indexes)):
                if self.to_move_steps[self.to_move_steps_indexes[i]] != 0:
                    self.step_pin[self.to_move_steps_indexes[i]].off()

            time.sleep_us(200)

            if self.to_move_steps[self.to_move_steps_indexes[0]] != 0:
                    self.step_pin[self.to_move_steps_indexes[0]].on()
                    self.counter[0] += 1
                    # Update the current position +1 if dir is cw, -1 if CCW
                    self.current_pos[self.to_move_steps_indexes[0]] = (self.current_pos[self.to_move_steps_indexes[0]]+1) if (self.dir_pin[self.to_move_steps_indexes[0]].value()==1) else (self.current_pos[self.to_move_steps_indexes[0]]-1)


            for i in range(1, len(self.to_move_steps_indexes)):
                if self.to_move_steps[self.to_move_steps_indexes[i]] != 0:
                    if (self.counter[0] / self.counter[i]) > self.R[i-1]:
                        self.step_pin[self.to_move_steps_indexes[i]].on()
                        self.counter[i] += 1
                        # Update the current position +1 if dir is cw, -1 if CCW
                        self.current_pos[self.to_move_steps_indexes[i]] = self.current_pos[self.to_move_steps_indexes[i]]+1 if (self.dir_pin[self.to_move_steps_indexes[i]].value()==1) else self.current_pos[self.to_move_steps_indexes[i]]-1
            
            self.init = False # update the init variable as it enters the loop
            # t2 = utime.ticks_us()
            # print("time_elapsed_Init: ", t2-t1)
            if abs(self.current_pos[self.to_move_steps_indexes[0]] - self.target_pos[self.to_move_steps_indexes[0]]) == 0:
                self.timer_0.deinit()
                self.timer_status = False
                # print("completed, POS: ", self.current_pos)
                break
            
            # time.sleep_us(200)
            
            # # # Update the timer period
            if (self.init_1):
                self.init_1 = False # update the init variable as it enters the loop
                # print('change timer period')
                self.timer_0.init(mode=Timer.PERIODIC, period=4, callback=self.run_stepper)
        


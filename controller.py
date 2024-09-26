from inputs import get_gamepad
import math
import threading
import keyboard
import time

class TimeTrackedButton():
    def __init__(self) -> None:
        self.is_pressed = False
        self.press_time = 0
        self.press_duration = None

    def press(self):
        if not self.is_pressed:
            self.is_pressed = True
            self.press_time = time.time()
            self.press_duration = None
    
    def release(self):
        if self.is_pressed:
            self.is_pressed = False
            self.set_duration()

    def set_duration(self):
        self.press_duration = time.time() - self.press_time
        # how long the press duration of button is visible to Controller class
        # 0.5 seems to perform good: (1 causes duplicate presses and <0.5 causes no presses) 
        time.sleep(0.5)
        self.press_duration = None




class Controller():
    MAX_TRIG_VAL = math.pow(2, 8)
    MAX_JOY_VAL = math.pow(2, 15)

    def __init__(self):

        self.LeftJoystickY = 0
        self.LeftJoystickX = 0
        self.RightJoystickY = 0
        self.RightJoystickX = 0
        self.LeftTrigger = 0    
        self.RightTrigger = 0
        self.LeftBumper = 0
        self.RightBumper = 0
        self.LeftThumb = 0
        self.RightThumb = 0
        self.Back = 0
        self.Start = 0
        self.LeftDPad = 0
        self.RightDPad = 0
        self.UpDPad = 0
        self.DownDPad = 0

        self.A = TimeTrackedButton()
        self.X = TimeTrackedButton()
        self.Y = TimeTrackedButton()
        self.B = TimeTrackedButton()

        self.TimeStamp = 0

        self._monitor_thread = threading.Thread(target=self._monitor_controller, args=())
        self._monitor_thread.daemon = True
        self._monitor_thread.start()


    def read(self): # return the buttons/triggers that you care about in this methode

        lx = self.LeftJoystickY
        ly = self.LeftJoystickX
        rx = self.RightJoystickY
        ry = self.RightJoystickX
        lt = self.LeftTrigger
        rt = self.RightTrigger
        lb = self.LeftBumper
        rb = self.RightBumper
        a  = self.A.press_duration
        x  = self.X.press_duration
        y  = self.Y.press_duration
        b  = self.B.press_duration
        
        return [lx, ly, a, x, y, b, rt, rb, lt, lb, rx, ry]    


    def _monitor_controller(self):
        while True:
            events = get_gamepad()
            for event in events:
                if event.code == 'ABS_Y':
                    self.LeftJoystickY = event.state / Controller.MAX_JOY_VAL # normalize between -1 and 1
                elif event.code == 'ABS_X':
                    self.LeftJoystickX = event.state / Controller.MAX_JOY_VAL # normalize between -1 and 1
                elif event.code == 'ABS_RY':
                    self.RightJoystickY = event.state / Controller.MAX_JOY_VAL # normalize between -1 and 1
                elif event.code == 'ABS_RX':
                    self.RightJoystickX = event.state / Controller.MAX_JOY_VAL # normalize between -1 and 1
                elif event.code == 'ABS_Z':
                    self.LeftTrigger = event.state / Controller.MAX_TRIG_VAL # normalize between 0 and 1
                elif event.code == 'ABS_RZ':
                    self.RightTrigger = event.state / Controller.MAX_TRIG_VAL # normalize between 0 and 1
                elif event.code == 'BTN_TL':
                    self.LeftBumper = event.state
                elif event.code == 'BTN_TR':
                    self.RightBumper = event.state
                elif event.code == 'BTN_THUMBL':
                    self.LeftThumb = event.state
                elif event.code == 'BTN_THUMBR':
                    self.RightThumb = event.state
                elif event.code == 'BTN_SELECT':
                    self.Back = event.state
                elif event.code == 'BTN_START':
                    self.Start = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY1':
                    self.LeftDPad = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY2':
                    self.RightDPad = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY3':
                    self.UpDPad = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY4':
                    self.DownDPad = event.state
                elif event.code == 'BTN_SOUTH':
                    if event.state == 1: self.A.press()
                    else: self.A.release()
                elif event.code == 'BTN_NORTH':
                    if event.state == 1: self.Y.press()
                    else: self.Y.release()
                elif event.code == 'BTN_WEST':
                    if event.state == 1: self.X.press()
                    else: self.X.release()
                elif event.code == 'BTN_EAST':
                    if event.state == 1: self.B.press()
                    else: self.B.release()




if __name__ == '__main__':
    joy = Controller()
    while True:
        print(joy.read())
        if keyboard.is_pressed('esc'):
            break

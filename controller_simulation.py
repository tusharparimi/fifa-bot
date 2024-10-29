import vgamepad as vg
#from inputs import get_gamepad
#from inputs import devices
import time
import pygetwindow as gw
import screenshot_taker as st
import controller as cn
import keyboard
import math

#TODO: write code that can play take in manual and simulated(AI) controls and play the game 
# (preferably a toggle 't' button to switch between manual and AI)

class Simulator():
    KEYS = ['a', 'b', 'x', 'y', 'lb', 'rb']
    def __init__(self, controller_type='xbox') -> None:
        self.simulate = False
        self.cn_object = cn.Controller()
        self.buttons = {k:None for k in Simulator.KEYS}
        #print(self.buttons)
        if controller_type == 'xbox': 
            self.gamepad = vg.VX360Gamepad()
            self.buttons['a']  = vg.XUSB_BUTTON.XUSB_GAMEPAD_A
            self.buttons['y']  = vg.XUSB_BUTTON.XUSB_GAMEPAD_Y
            self.buttons['x']  = vg.XUSB_BUTTON.XUSB_GAMEPAD_X
            self.buttons['b']  = vg.XUSB_BUTTON.XUSB_GAMEPAD_B
            self.buttons['lb'] = vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER
            self.buttons['rb'] = vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER
        else: 
            self.gamepad = vg.VDS4Gamepad()
            self.buttons['a']  = vg.DS4_BUTTONS.DS4_BUTTON_CROSS
            self.buttons['y']  = vg.DS4_BUTTONS.DS4_BUTTON_TRIANGLE
            self.buttons['x']  = vg.DS4_BUTTONS.DS4_BUTTON_SQUARE
            self.buttons['b']  = vg.DS4_BUTTONS.DS4_BUTTON_CIRCLE
            self.buttons['lb'] = vg.DS4_BUTTONS.DS4_BUTTON_SHOULDER_LEFT
            self.buttons['rb'] = vg.DS4_BUTTONS.DS4_BUTTON_SHOULDER_RIGHT

    def toggle(self):
        self.simulate = True if self.simulate is False else False

    def play(self):
        press_duration = 0.1
        while True:
            # time.sleep(0.2)
            if keyboard.is_pressed('esc'):
                print("Simulation Stopped !!!")
                break
            if keyboard.is_pressed('t'):
                print("toggle !!!")
                self.toggle()
                time.sleep(0.1)
                continue
            if self.simulate:
                # AI sim
                # fake inference for now till I have my precious model
                print("AI")
                pass
            else:
                # Manual sim
                print('Manual')

                # time tracked buttons
                if self.cn_object.A.press_duration:
                    self.gamepad.press_button(button=self.buttons['a'])
                    press_duration = self.cn_object.A.press_duration \
                        if self.cn_object.A.press_duration else 0.1
                if self.cn_object.Y.press_duration:
                    self.gamepad.press_button(button=self.buttons['y'])
                    press_duration = self.cn_object.Y.press_duration \
                        if self.cn_object.Y.press_duration else 0.1
                if self.cn_object.X.press_duration:
                    self.gamepad.press_button(button=self.buttons['x'])
                    press_duration = self.cn_object.X.press_duration \
                        if self.cn_object.X.press_duration else 0.1
                if self.cn_object.B.press_duration:
                    self.gamepad.press_button(button=self.buttons['b'])
                    press_duration = self.cn_object.B.press_duration \
                        if self.cn_object.B.press_duration else 0.1             
                self.gamepad.update()
                time.sleep(press_duration)
                self.gamepad.reset()
                self.gamepad.update()
                time.sleep(0.1)

                # normie buttons
                self.gamepad.left_joystick_float( \
                    x_value_float=self.cn_object.LeftJoystickX, \
                        y_value_float=self.cn_object.LeftJoystickY)
                self.gamepad.right_joystick_float( \
                    x_value_float=self.cn_object.RightJoystickX, \
                        y_value_float=self.cn_object.RightJoystickY)
                self.gamepad.left_trigger_float(value_float=self.cn_object.LeftTrigger)
                self.gamepad.right_trigger_float(value_float=self.cn_object.RightTrigger)
                if self.cn_object.LeftBumper != 0.0:
                    self.gamepad.press_button(button=self.buttons['lb'])  
                if self.cn_object.RightBumper != 0.0:
                    self.gamepad.press_button(button=self.buttons['rb'])  
                self.gamepad.update()
                time.sleep(0.1)
                
                

    
if __name__ == '__main__':
    sim = Simulator('xbox')
    sim.play()




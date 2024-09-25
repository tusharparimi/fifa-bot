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
    def __init__(self) -> None:
        self.simulate = False
        self.cn_object = cn.Controller()
        self.gamepad = vg.VX360Gamepad()
    
    def toggle(self):
        self.simulate = True if self.simulate is False else False

    def play(self):
        while True:
            # time.sleep(0.2)
            if keyboard.is_pressed('esc'):
                print("Simulation Stopped !!!")
                break
            if keyboard.is_pressed('t'):
                print("toggle !!!")
                self.toggle()
                time.sleep(0.01)
                continue
                #self.fifa_window.activate()
                #elif not self.simulate: del gamepad
            if self.simulate:
                # fake inference for now till I have my precious model
                print("AI")
                pass
            else:
            # manual
                print('Manual')
                if self.cn_object.A != 0.0:
                    self.gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)  # press the A button
                    # print("A")           
                if self.cn_object.B != 0.0:
                    self.gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_B)    
                    # print("B")
                #if self.cn_object.LeftJoystickX != 0.0 or self.cn_object.LeftJoystickY != 0.0:
                self.gamepad.left_joystick_float( \
                    x_value_float=self.cn_object.LeftJoystickX, \
                        y_value_float=self.cn_object.LeftJoystickY)
                #print("Left stick")
                self.gamepad.update()
                time.sleep(0.1)
                self.gamepad.reset()
                self.gamepad.update()
                time.sleep(0.1)

    
if __name__ == '__main__':
    sim = Simulator()
    sim.play()




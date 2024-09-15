import vgamepad as vg
from inputs import get_gamepad
from inputs import devices
import time
import pygetwindow as gw

# just playing aroung for now

gamepad = vg.VX360Gamepad()

fifa_window = gw.getWindowsWithTitle('FC 24')[0]
fifa_window.activate()

i = 0
while i<5:

    print('press')
    gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)  # press the A button
    gamepad.update()
    time.sleep(0.5)

    print('release')
    gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)  # release the A button
    gamepad.update()  # send the updated state to the computer
    time.sleep(0.5)

    i = i+1

#for device in devices:
#    print(device)


# while True:
#     events = get_gamepad()
#     for event in events:
#         print(event)





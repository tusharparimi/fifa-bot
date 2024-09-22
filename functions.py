import os
from csv import DictWriter
from csv import writer
from ctypes import windll, wintypes, byref
import keyboard
from pathlib import Path
import matplotlib.pyplot as plt
import pyautogui


def log_csvfile(dict_data,csvfile_name):
    if os.path.exists(csvfile_name):
        with open(csvfile_name,'a') as f_object:
            dictwriter_object=DictWriter(f_object,fieldnames=[col for col in dict_data])
            dictwriter_object.writerow(dict_data)
            f_object.close()
    else:
        with open(csvfile_name,'w') as f_object:
            writer_object=writer(f_object)
            writer_object.writerow([col for col in dict_data])
            writer_object.writerow([dict_data[col] for col in dict_data])
            f_object.close()

def get_cursor_pos():
    cursor = wintypes.POINT()
    windll.user32.GetCursorPos(byref(cursor))
    return (cursor.x, cursor.y)

def str2tuplelist(s):
    tuple_list = []
    for each in s.split(", "):
        tuple_list.append(tuple([int(item) for item in each[1:-1].split(" ")]))
    return tuple_list

def tuplelist2str(tuple_list):
    s = ""
    for each in tuple_list:
        s = s + f"({each[0]} {each[1]}), "
    return s[:-2]

def select_roi(game_name, win_topleft=(-6, 0), win_size=(865, 515)): 
    roi = []
    try:
        with open(Path(".\\roi.txt"), 'r') as file:
            for line in file.readlines():
                if (line.split(":")[1]) == \
                    tuplelist2str([win_topleft, win_size]):
                    print(f"Used roi, detected for {line.split(":")[0]}! : " + \
                          f"{line.split(":")[2][:-1]}")
                    roi = str2tuplelist(line.split(":")[2][:-1])
                    img = pyautogui.screenshot(region=(roi[0][0], roi[0][1], \
                                                       (roi[1][0]-roi[0][0]), \
                                                        (roi[1][1]-roi[0][1])))
                    #img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
                    plt.imshow(img) 
                    plt.show(block=False)
                    plt.pause(0.1)
                    #print("To re-use roi (Press 'y'), else next (Press 'n')")
                    print("Press [y/n] [to use detected ROI/see next saved ROI]")
                    while True:
                        event = keyboard.read_event()
                        if event.event_type == keyboard.KEY_DOWN and event.name == 'y':
                            print("\nROI selected !!!")
                            plt.close()
                            return str2tuplelist(line.split(":")[2][:-1])
                        if event.event_type == keyboard.KEY_DOWN and event.name == 'n':
                            roi = []
                            break
                    plt.close()
    except FileNotFoundError:
        print("\nNo pre-computed ROIs available")

    roi_selected = False
    while not roi_selected:
        print("\nManually select new ROI...")
        #print("Place cursor on the topleft of ROI and press 'l' to lock: ")
        print("\nPlace cursor on the topleft of ROI and Press [l]: ")
        keyboard.wait("l")
        x, y = get_cursor_pos() 
        print(f"({x},{y}) locked as topleft!")
        roi.append((x, y))
        #print("Place cursor on the bottomright of ROI and press 'l' to lock: ")
        print("\nPlace cursor on the bottomright of ROI and Press [l]: ")
        keyboard.wait("l")
        x, y = get_cursor_pos() 
        print(f"({x},{y}) locked as bottomright!")
        roi.append((x, y))
        img = pyautogui.screenshot(region=(roi[0][0], roi[0][1], (roi[1][0]-roi[0][0]), \
                                            (roi[1][1]-roi[0][1])))
        #img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        plt.imshow(img) 
        plt.show(block=False)
        plt.pause(0.1)

        #print("\nTo save this roi, (Press 'y') else to select again (Press 'n')")
        print("\nPress [y/s/n] [use ROI/save and use ROI/select new ROI]")
        while True:
            event = keyboard.read_event()
            if event.event_type == keyboard.KEY_DOWN and event.name == 'y':
                roi_selected = True
                break
            if event.event_type == keyboard.KEY_DOWN and event.name == 's':
                with open(Path(".\\roi.txt"), "a") as file:
                    file.write(game_name + ":" + \
                               tuplelist2str([win_topleft, win_size]) + ":" + \
                                tuplelist2str(roi) + "\n")
                roi_selected = True
                break
            if event.event_type == keyboard.KEY_DOWN and event.name == 'n':
                roi = []
                break
        #cv2.destroyWindow("current roi")
        plt.close()
    print("\nROI selected !!!")
    return roi
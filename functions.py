import os
from csv import DictWriter
from csv import writer
from ctypes import windll, wintypes, byref

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

def str2roi(s):
    pass

def roi2str(t):
    pass
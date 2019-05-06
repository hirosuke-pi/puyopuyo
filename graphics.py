import os, sys
import time

#datalist : [ y1:[x1:[str, forecol, backcol], x2:.. ], y2:[].. ]
def clear():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

def reset_color():
    if os.name == "nt":
        set_colors_win32()
    else:
        sys.stdout.write("\033[0m")


def cprint(data_list):
    if os.name == "nt":
        for data_line in data_list:
            for data in data_line:
                set_colors_win32(data[1], data[2])
                sys.stdout.write(data[0])
                sys.stdout.flush()
                set_colors_win32()
            sys.stdout.write("\r\n")
            sys.stdout.flush()
    else:
        for data_line in data_list:
            for data in data_line: 
                set_colors_unix(data[1], data[2])
                sys.stdout.write(data[0])
                sys.stdout.flush()
                sys.stdout.write("\033[0m")
            sys.stdout.write("\r\n")
            sys.stdout.flush()


def set_colors_unix(forecol = "w", backcol = "k"):
    if forecol == "k":
        sys.stdout.write("\033[30m")
    elif forecol == "r" or forecol == "R":
        sys.stdout.write("\033[31m")
    elif forecol == "g" or forecol == "G":
        sys.stdout.write("\033[32m")
    elif forecol == "y" or forecol == "Y":
        sys.stdout.write("\033[33m")
    elif forecol == "b" or forecol == "B":
        sys.stdout.write("\033[34m")
    elif forecol == "m" or forecol == "M":
        sys.stdout.write("\033[35m")       
    elif forecol == "c" or forecol == "C":
        sys.stdout.write("\033[36m")
    elif forecol == "w" or forecol == "W" or forecol == "":
        sys.stdout.write("\033[37m")

    if backcol == "k"  or forecol == "":
        sys.stdout.write("\033[40m")
    elif backcol == "r" or backcol == "R":
        sys.stdout.write("\033[41m")
    elif backcol == "g" or backcol == "G":
        sys.stdout.write("\033[42m")
    elif backcol == "y" or backcol == "Y":
        sys.stdout.write("\033[43m")
    elif backcol == "b" or backcol == "B":
        sys.stdout.write("\033[44m")
    elif backcol == "m" or backcol == "M":
        sys.stdout.write("\033[45m")       
    elif backcol == "c" or backcol == "C":
        sys.stdout.write("\033[46m")
    elif backcol == "w" or backcol == "W":
        sys.stdout.write("\033[47m")
    sys.stdout.flush()

    


def set_colors_win32(forecol = "w", backcol = "k"):
    import ctypes
    STD_OUTPUT_HANDLE  = -11

    FOREGROUND_BLACK   = 0x00
    FOREGROUND_BLUE    = 0x01
    FOREGROUND_GREEN   = 0x02
    FOREGROUND_RED     = 0x04
    FOREGROUND_CYAN    = FOREGROUND_BLUE  | FOREGROUND_GREEN
    FOREGROUND_MAGENTA = FOREGROUND_BLUE  | FOREGROUND_RED
    FOREGROUND_YELLOW  = FOREGROUND_GREEN | FOREGROUND_RED
    FOREGROUND_WHITE   = FOREGROUND_BLUE  | FOREGROUND_GREEN | FOREGROUND_RED
    FOREGROUND_INTENSITY = 0x08

    BACKGROUND_BLACK   = 0x00
    BACKGROUND_BLUE    = 0x10
    BACKGROUND_GREEN   = 0x20
    BACKGROUND_RED     = 0x40
    BACKGROUND_CYAN    = BACKGROUND_BLUE  | BACKGROUND_GREEN
    BACKGROUND_MAGENTA = BACKGROUND_BLUE  | BACKGROUND_RED
    BACKGROUND_YELLOW  = BACKGROUND_GREEN | BACKGROUND_RED
    BACKGROUND_WHITE   = BACKGROUND_BLUE  | BACKGROUND_GREEN | BACKGROUND_RED
    BACKGROUND_INTENSITY = 0x80

    std_out_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)

    if forecol == "k":
        fore = FOREGROUND_BLACK
    elif forecol == "b":
        fore = FOREGROUND_BLUE
    elif forecol == "g":
        fore = FOREGROUND_GREEN
    elif forecol == "r":
        fore = FOREGROUND_RED
    elif forecol == "c":
        fore = FOREGROUND_CYAN
    elif forecol == "m":
        fore = FOREGROUND_MAGENTA
    elif forecol == "y":
        fore = FOREGROUND_YELLOW
    elif forecol == "w" or forecol == "":
        fore = FOREGROUND_WHITE
    elif forecol == "B":
        fore = FOREGROUND_BLUE    | FOREGROUND_INTENSITY
    elif forecol == "G":
        fore = FOREGROUND_GREEN   | FOREGROUND_INTENSITY
    elif forecol == "R":
        fore = FOREGROUND_RED     | FOREGROUND_INTENSITY
    elif forecol == "C":
        fore = FOREGROUND_CYAN    | FOREGROUND_INTENSITY
    elif forecol == "M":
        fore = FOREGROUND_MAGENTA | FOREGROUND_INTENSITY
    elif forecol == "Y":
        fore = FOREGROUND_YELLOW  | FOREGROUND_INTENSITY
    elif forecol == "W":
        fore = FOREGROUND_WHITE   | FOREGROUND_INTENSITY
    else:
        fore = FOREGROUND_WHITE

        #背景色
    if backcol == "k" or forecol == "":
        back = BACKGROUND_BLACK
    elif backcol == "b":
        back = BACKGROUND_BLUE
    elif backcol == "g":
        back = BACKGROUND_GREEN
    elif backcol == "r":
        back = BACKGROUND_RED
    elif backcol == "c":
        back = BACKGROUND_CYAN
    elif backcol == "m":
        back = BACKGROUND_MAGENTA
    elif backcol == "y":
        back = BACKGROUND_YELLOW
    elif backcol == "w":
        back = BACKGROUND_WHITE
    elif backcol == "B":
        back = BACKGROUND_BLUE    | BACKGROUND_INTENSITY
    elif backcol == "G":
        back = BACKGROUND_GREEN   | BACKGROUND_INTENSITY
    elif backcol == "R":
        back = BACKGROUND_RED     | BACKGROUND_INTENSITY
    elif backcol == "C":
        back = BACKGROUND_CYAN    | BACKGROUND_INTENSITY
    elif backcol == "M":
        back = BACKGROUND_MAGENTA | BACKGROUND_INTENSITY
    elif backcol == "Y":
        back = BACKGROUND_YELLOW  | BACKGROUND_INTENSITY
    elif backcol == "W":
        back = BACKGROUND_WHITE   | BACKGROUND_INTENSITY
    else:
        back = BACKGROUND_BLACK

    ctypes.windll.kernel32.SetConsoleTextAttribute(std_out_handle, fore | back) 
import pyautogui
import time
import keyboard
import sys
from pynput import mouse
from datetime import datetime
import datetime
import os
import sys
import ctypes
import pygetwindow as gw

delay_time = 1
pyautogui.PAUSE = 0.1
im = pyautogui.screenshot()
pos = (1883, 1030)
rgb = im.getpixel(pos)
rgb_goal = (186, 187, 186)
org = pyautogui.position()
should_exit = False
paused = False
click_paused = False
first_time = None
later_time = None


def get_active_window():
    active_window = gw.getActiveWindow()
    return active_window


def bring_window_to_foreground(hwnd):
    user32 = ctypes.windll.user32
    user32.SetForegroundWindow(hwnd)


# Disable Terminal Output
def disable_print():
    sys.stdout = open(os.devnull, "w")


# Restore Terminal Output
def enable_print():
    sys.stdout = sys.__stdout__


def toggle_pause():  # gpt
    enable_print()
    global paused
    paused = not paused
    print("Pausing" if paused else "Unpausing")


def exit_program():
    enable_print()
    global should_exit
    Timestamp("Exited: ")
    td_dif(first_time, later_time)
    td_calc()
    disable_print()
    should_exit = True


# Register the Ctrl+F8 and Ctrl+F9 hotkey
keyboard.add_hotkey("ctrl+f8", toggle_pause)  # gpt
keyboard.add_hotkey("ctrl+f9", exit_program)


def next_locate():  # unused because the image doesn't grab, also only works on one monitor
    try:
        photo = pyautogui.locateOnScreen("yes_next.png")
        if photo is not None:
            photo_center = pyautogui.center(photo)
            pyautogui.click(photo_center)
            print(photo)
            print(photo_center)
        else:
            print("Image not found.")

    except Exception as e:
        print("An error occurred:", str(e))


def get_pos_rgb():  # used for finding pixel position and and rgb
    for i in range(11):
        if i < 11:
            pos = pyautogui.position()
            i = i + 1
            rgb = im.getpixel((pos))
            print(pos)

            print(rgb)
            time.sleep(3)


def pixel_click(org_pos):  # clicks location and moves back - used in next_click
    initial_window = get_active_window()
    initial_window_hwnd = initial_window._hWnd
    print("Initial window not found.")
    pyautogui.PAUSE = 0.1  # sets pyautogui delay to .1 seconds to improve efficiency
    pyautogui.click(pos)
    pyautogui.moveTo(org_pos)
    pyautogui.PAUSE = delay_time  # returns pyautogui.pause to original value
    bring_window_to_foreground(initial_window_hwnd)
    print("Next slide.")

    time.sleep(3)


def on_click(button, pressed):
    global paused
    global click_paused
    if button == mouse.Button.left and paused == False:
        if pressed:
            click_paused = True
            print("Left click detected, Pausing...")
            disable_print()
        else:
            enable_print()
            click_paused = False
            print("Loop resumed.")


def next_click(delay_time):
    try:
        while not should_exit:
            global paused
            global click_paused
            if should_exit is True:  # ends if exit true
                break
            if not paused and not click_paused:  # checks for paused
                time.sleep(delay_time)
                print(f"Loop running... Delay ({delay_time})")
                org_pos = pyautogui.position()
                current_color = pyautogui.pixel(pos[0], pos[1])
                if current_color == rgb_goal and paused == False:
                    pixel_click(org_pos)
                    delay_time = (
                        0.5  # lowers delay in case so the code can make sure it clicked
                    )
                else:
                    time.sleep(2)
                    print("Nothing found.")
                    time.sleep(1)
                    delay_time = 3
            else:
                enable_print()
                print("Loop paused.")
                while paused or click_paused:
                    if should_exit is True:
                        paused = False
                        exit_program
                    else:
                        time.sleep(0.1)
            time.sleep(0.1)  # Add a small delay to avoid excessive CPU usage
    except KeyboardInterrupt:
        print("Loop interrupted. Exiting the code.")
        Timestamp("Exited: ")
        td_dif(first_time, later_time)
        td_calc()
        exit_program


def Timestamp(prefix):
    global first_time, later_time
    enable_print()
    now = datetime.datetime.now()
    dt_string = now.strftime("%m/%d/%Y %H:%M:%S")
    # datetime object containing current date and time
    if first_time is None:
        first_time = now
    # dd/mm/YY H:M:S
    else:
        later_time = now
    print(prefix + dt_string)
    with open("timestamps.log", "a") as a:
        a.write(f"\n{prefix} {dt_string}")


def td_dif(a, b):
    difference = a - b
    seconds_in_day = 24 * 60 * 60
    diff_in_seconds = difference.days * seconds_in_day + difference.seconds
    minutes, seconds = divmod(diff_in_seconds, 60)
    return minutes, seconds


def td_calc():
    with open("timestamps.log", "a") as a:
        if first_time is not None and later_time is not None:
            minutes, seconds = td_dif(later_time, first_time)
            if minutes < 1:
                print(f"Time elapsed: {seconds} seconds")
                a.write(f"\n\t Time elapsed: {seconds} seconds")
                return minutes, seconds
            else:
                a.write(f"\n\t Time elapsed: {minutes} minutes, {seconds} seconds")
                print(f"Time elapsed: {minutes} minutes, {seconds} seconds")
                return minutes, seconds
        else:
            print("Insufficient timestamps to calculate the difference.")
            return None, None


###### Start of code ######

# first_time defined and reason inputted
os.chdir("./Driving course/")
Timestamp("\nOpened code: ")
reason = input("Input reason: ")
if len(reason) == 0:
    cap_reason = "No reason given."
    print(cap_reason)
else:
    cap_reason = reason.title()
with open("timestamps.log", "a") as a:
    a.write(f"\nReason: {cap_reason}")

# Create a listener for mouse events
mouse_listener = mouse.Listener(on_click=on_click)
mouse_listener.start()

# Start the main loop
try:
    next_click(delay_time)
except OSError:
    exit_program()

###### End of code ######

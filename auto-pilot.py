import pyautogui
import time
import keyboard
import pystray
from pystray import MenuItem as item
from PIL import Image
import sys
from pynput import mouse
from datetime import datetime
import datetime

delay_time = 1
pyautogui.PAUSE = 0.1
im = pyautogui.screenshot()
pos = (1883, 1030)
rgb = im.getpixel(pos)
rgb_goal = (186, 187, 186)
org = pyautogui.position()
# Global flag variable to control pause/unpause
should_exit = False
paused = False
click_paused = False
first_time = None
fol = True
later_time = None


def toggle_pause():  # gpt
    global paused
    paused = not paused
    print("Pausing" if paused else "Unpausing")


def exit_program():
    global should_exit
    Timestamp("Exited: ")
    td_div(first_time, later_time)
    td_calc()
    should_exit = True


# Register the Ctrl+F8 hotkey
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
    pyautogui.PAUSE = 0.1  # sets pyautogui delay to .1 seconds to improve efficiency
    pyautogui.click(pos)
    pyautogui.moveTo(org_pos)
    pyautogui.PAUSE = delay_time  # returns pyautogui.pause to original value
    print("Next slide.")
    time.sleep(3)


def on_click(x, y, button, pressed):
    global paused
    global click_paused
    if button == mouse.Button.left and paused == False:
        if pressed:
            click_paused = True
            print("Left click detected, Pausing...")
        else:
            click_paused = False
            print("Loop resumed.")


def next_click(delay_time):
    try:
        while not should_exit:
            global paused
            global click_paused
            if should_exit is True:  # ends if exit true
                break
            elif not paused and not click_paused:  # checks for paused
                time.sleep(delay_time)
                print(f"Loop running... Delay ({delay_time})")
                org_pos = pyautogui.position()
                rgb_color = rgb
                current_color = pyautogui.pixel(pos[0], pos[1])
                if current_color == rgb_goal and paused == False:
                    pixel_click(org_pos)
                    delay_time = (
                        0.5  # lowers delay in case so the code can make sure it clicked
                    )

                elif not paused and not click_paused:
                    time.sleep(2)
                    print("Nothing found.")
                    time.sleep(1)
                    delay_time = 3
            else:
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
        # now = datetime.now()
        Timestamp("Exited: ")
        td_div(first_time, later_time)
        td_calc()
        # print(td_div(later_time, first_time))
        exit_program


# Create the system tray icon
def create_tray_icon():  # gpt bullshit
    image = Image.open("tray_icon.png")  # Replace with the path to your icon image
    menu = (
        item("Toggle Pause/Unpause", toggle_pause),
        item("Exit", exit_program),
    )
    tray_icon = pystray.Icon("TROLLED", image, "Tooltip", menu)
    tray_icon.run()


datetime.timedelta


def Timestamp(prefix):
    global first_time, later_time

    now = datetime.datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    # datetime object containing current date and time
    if first_time is None:
        first_time = now
    # dd/mm/YY H:M:S
    else:
        later_time = now
    print(prefix + dt_string)
    with open("timestamps.log", "a") as a:
        a.write(f"\n{prefix} {dt_string}")


def td_div(a, b):
    difference = a - b
    seconds_in_day = 24 * 60 * 60
    diff_in_seconds = difference.days * seconds_in_day + difference.seconds
    minutes, seconds = divmod(diff_in_seconds, 60)
    return minutes, seconds


def td_calc():
    with open("timestamps.log", "a") as a:
        if first_time is not None and later_time is not None:
            minutes, seconds = td_div(later_time, first_time)
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


# Start of code
Timestamp("Opened code: ")

# Create a listener for mouse events
mouse_listener = mouse.Listener(on_click=on_click)

# Start the mouse listener
mouse_listener.start()

next_click(delay_time)
# create_tray_icon()
# Start the main loop
# next_click(delay_time)

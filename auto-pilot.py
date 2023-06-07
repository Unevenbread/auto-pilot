import pyautogui
import time
import keyboard
import pystray
from pystray import MenuItem as item
from PIL import Image
import sys
from pynput import mouse

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


def toggle_pause():  # gpt
    global paused
    paused = not paused
    print("Pausing" if paused else "Unpausing")


def exit_program():
    global should_exit
    should_exit = True


# Register the Ctrl+F8 hotkey
keyboard.add_hotkey("ctrl+f8", toggle_pause)  # gpt
keyboard.add_hotkey("ctrl+f9", exit_program)


def next_locate():  # unused because the image doesn't grab, also only works on one monitor
    try:
        photo = pyautogui.locateOnScreen(r".\yes_next.png")
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
    for i in range(10):
        if i == 10:
            break
        else:
            pos = pyautogui.position()
            i = i + 1
            print(pos)
            rgb = im.getpixel((pos))
            print(rgb)
            time.sleep(3)
            continue


def pixel_click(org_pos):  # clicks location and moves back - used in next_click
    pyautogui.PAUSE = 0.1  # sets pyautogui delay to .1 seconds to improve efficiency
    pyautogui.click(pos)
    pyautogui.moveTo(org_pos)
    pyautogui.PAUSE = delay_time  # returns pyautogui.pause to original value
    print("next")
    time.sleep(3)

def on_click(
    x, y, button, pressed
): 
    global paused
    if button == mouse.Button.left:
        if pressed:
            paused = True
            print("left click detected")
        else:
            paused = False
            print("Loop resumed.")

def next_click(delay_time):
    try:
        while not should_exit:
            global paused
            if should_exit is True:
                break
            elif not paused:
                time.sleep(delay_time)
                print(f"Loop running... Delay ({delay_time})")
                org_pos = pyautogui.position()
                rgb_color = rgb
                current_color = pyautogui.pixel(pos[0], pos[1])
                # print (f"current_color {current_color}")
                # i = 1
                if current_color == rgb_goal:
                    pixel_click(org_pos)
                    delay_time = 0.5  # lowers delay in case so the code can make sure it clicked
                else:
                    time.sleep(2)
                    print("nothing found")
                    time.sleep(1)
                    delay_time = 5
                    continue
            else:
                print("Loop paused...")
                while paused:
                    if should_exit is True:
                        paused = False
                        exit_program
                    else:
                        time.sleep(0.1)
            time.sleep(0.1)  # Add a small delay to avoid excessive CPU usage
    except KeyboardInterrupt:
        print("Loop interrupted. Exiting the code.")
        exit


# Create the system tray icon
def create_tray_icon():  # gpt bullshit
    image = Image.open(r".\icon.png")  # Replace with the path to your icon image
    menu = (
        item("Toggle Pause/Unpause", toggle_pause),
        item("Exit", exit_program),
    )
    tray_icon = pystray.Icon("name_of_icon", image, "Tooltip", menu)
    tray_icon.run()


# Create a listener for mouse events
mouse_listener = mouse.Listener(on_click=on_click)

# Start the mouse listener
mouse_listener.start()

# Start the main loop
next_click(delay_time)

# Run the next_click loop in a separate thread
# import threading
# thread = threading.Thread(target=next_click)
# thread.start()

# Run the system tray icon in the main thread
# create_tray_icon()


# try:
#     while True:
#         # Code to be executed in the loop
#         next_locate()
#         # Delay for 5 seconds
#         time.sleep(3)
# except KeyboardInterrupt:
#     print("Loop interrupted. Exiting the code.")

# Get and print the mouse coordinates.
# x, y = pyautogui.position()
# positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)


# pyautogui.moveTo

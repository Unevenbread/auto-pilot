# Automated Clicker

This script is designed to automate the process of clicking through slides of a presentation, particularly for educational purposes. It utilizes various Python libraries to control mouse clicks, capture screen information, and manage pauses.

## Features

- Automated slide clicking: The script automatically clicks through slides of a presentation when a specific pixel color is detected.
- Pause and resume functionality: You can pause and resume the script using the hotkey "Ctrl + F8".
- Graceful exit: The script can be exited using the hotkey "Ctrl + F9", and it calculates and logs the time elapsed during its execution.

## Prerequisites

Before using this script, ensure you have the following libraries installed:

- pyautogui
- keyboard
- pystray
- pynput

## Usage

1. Make sure all the required libraries are installed.
2. Adjust the script settings as needed (e.g., `pos`, `rgb_goal`, `delay_time`).
4. While the script is running, it will continuously check for the specified pixel color. When the color matches, it will click the corresponding position and move back.

## Hotkeys

- **Ctrl + F8:** Toggle pause/unpause of the script.
- **Ctrl + F9:** Exit the script gracefully and calculate the time elapsed.

## Important Notes

- The script is designed for money making purposes and should not be used responsibly.
- The script might need adjustments depending on the specifics of your setup, such as screen resolution, pixel colors, and slide software.

## Disclaimer

This script is provided as-is, and the authors assume no responsibility for any unintended consequences or misuse. Use at your own risk.

## License

This script is provided under the [WTFPL License](LICENSE). You are free to modify and distribute it, but you are responsible for ensuring its appropriate use and compliance with any relevant laws or regulations.

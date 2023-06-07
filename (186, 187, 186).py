(186, 187, 186)
while True:
    if not paused:
        # Perform your desired operations here
        print("Loop running...")
    else:
        # Add any additional logic for the paused state, if needed
        print("Loop paused...")
    
    # Break the loop on 'Esc' key press
    if keyboard.is_pressed("esc"):
        break

C:\Users\DCutler\Desktop\testing\icon.png
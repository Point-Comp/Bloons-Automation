import pyautogui
from pynput import keyboard
import time

#This is basically a dynamic restart mechanism like it constantly reads the screen to see if there is a giveup/restart button to be pressed
# We look at the red pixel to know the end screen is visible
SENSE_X, SENSE_Y = 1666, 1088 
TARGET_COLOR = (233, 6, 28) 

# We click the specific give Up button coordinates
GIVE_UP_X, GIVE_UP_Y = 570.0, 792.5

def check_and_restart():
    print(f"\n--- FAIL-SAFE SENSOR CHECK ---")
    
    current_color = pyautogui.pixel(SENSE_X, SENSE_Y)
    print(f"Checking Trigger Pixel ({SENSE_X}, {SENSE_Y})")
    print(f"Detected RGB: {current_color}")

    if pyautogui.pixelMatchesColor(SENSE_X, SENSE_Y, TARGET_COLOR, tolerance=30):
        print("✅ TRIGGER DETECTED: End Screen is visible.")
        print(f"Action: Clicking 'Give Up' at ({GIVE_UP_X}, {GIVE_UP_Y})...")
        
        # Move and click the Give Up button
        pyautogui.click(GIVE_UP_X, GIVE_UP_Y)
        
        time.sleep(1)
        print("--- RESTART TEST COMPLETE ---")
    else:
        print("❌ RESULT: No match. The end screen trigger pixel wasn't found.")

def on_press(key):
    try:
        if hasattr(key, 'char') and key.char == 'd':
            check_and_restart()
        if key == keyboard.Key.esc:
            print("Exiting debug script...")
            return False
    except Exception as e:
        print(f"Error: {e}")

print(f"Sentry Active. Get to the End Screen and press 'd'.")
print(f"Logic: If Red is seen at ({SENSE_X}, {SENSE_Y}), Click Give Up at ({GIVE_UP_X}, {GIVE_UP_Y})")

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
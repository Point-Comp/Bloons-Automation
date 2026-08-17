import pyautogui
from pynput import keyboard
import sys

# take a picture of the specific icon or placement on screen and paste and use it here to find coords,
TARGET_IMAGE = 'home.png'

def find_coordinates():
    print(f"\n--- Scanning for {TARGET_IMAGE} ---")
    try:
        # Grayscale and confidence make Mac detection MUCH more reliable
        pos = pyautogui.locateCenterOnScreen(TARGET_IMAGE, grayscale=True, confidence=0.7)
        if pos:
            # Divide by 2 for Retina scaling
            scaled_x = pos.x / 2
            scaled_y = pos.y / 2
            print(f"✅ Found! Raw X: {pos.x}, Y: {pos.y}")
            print(f"📍 Scaled X: {scaled_x}, Y: {scaled_y}")
            print(f"Use this: human_click({scaled_x}, {scaled_y})")
        else:
            print("❌ Image not found. Check if it's visible on screen.")
    except Exception as e:
        print(f"⚠️ Error: {e}")

def on_press(key):
    try:
        if hasattr(key, 'char') and key.char == 'p':
            find_coordinates()
        if key == keyboard.Key.esc:
            print("\n🛑 Escape pressed. Quitting script...")
            return False
    except Exception as e:
        print(f"Listener error: {e}")

print("INSTRUCTIONS:")
print("1. Ensure your game/app is visible.")
print("2. Press 'p' to print the image center coordinates.")
print("3. Press 'Escape' to quit the script.")

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()

import pyautogui
import time

print("Position your mouse over the target pixel...")
time.sleep(6) # Gives you 3 seconds to move your mouse to the right spot
x, y = pyautogui.position()
color = pyautogui.pixel(x*2, y*2)

print(f"Coordinates: ({x}, {y})")
print(f"RGB Color: {color}")
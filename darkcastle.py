import pyautogui
from pynput import keyboard
import time

def human_click(x, y, wait=0.1):
    pyautogui.moveTo(x, y)
    pyautogui.mouseDown()
    time.sleep(wait)
    pyautogui.mouseUp()

def start_automation():
    print("Automation started...")
    while True:
        time.sleep(1)
        human_click(755.0, 861.5)
        time.sleep(1)
        human_click(153.0, 414.5)
        human_click(153.0, 414.5)
        time.sleep(1)
        human_click(760.0, 545.0)
        time.sleep(1)
        human_click(457.5, 462.0)
        time.sleep(1)
        human_click(1039.5, 464.0)
        time.sleep(6)
        human_click(772.0, 695.0)
        time.sleep(1)
        human_click(1144.5, 554.0)
        pyautogui.press('q')
        human_click(1144.5, 554.0)
        human_click(1144.5, 554.0)
        pyautogui.press('/')
        pyautogui.press('/')
        pyautogui.press('/')
        pyautogui.press('/')
        pyautogui.press('/')
        pyautogui.press('/')
        pyautogui.press('/')
        pyautogui.press('.')
        pyautogui.press('.')
        pyautogui.press('.')
        pyautogui.press('.')
        pyautogui.press('space')
        pyautogui.press('space')
        time.sleep(360)
        human_click(1144.5, 554.0)
        time.sleep(3)
        human_click(544.0, 782.5)
        time.sleep(4)
        
        


        print("Cycle done.")


def on_press(key):
    try:
        if hasattr(key, 'char') and key.char == 'd':
            start_automation()
        if key == keyboard.Key.esc:
            return False
    except AttributeError:
        pass

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()

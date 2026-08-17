import pyautogui
from pynput import keyboard
import time

is_running = False

class GameFail(Exception): 
    pass

SENSE_X, SENSE_Y = 1666, 1088      
TARGET_COLOR = (233, 6, 28)        
GIVE_UP_X, GIVE_UP_Y = 570.0, 792.5 

def check_for_defeat():
    if pyautogui.pixelMatchesColor(SENSE_X, SENSE_Y, TARGET_COLOR, tolerance=25):
        print("⚠️ Possible Defeat Detected! Running Consensus Check...")
        
        confidence_score = 0
        for _ in range(4):
            time.sleep(0.5)
            if pyautogui.pixelMatchesColor(SENSE_X, SENSE_Y, TARGET_COLOR, tolerance=30):
                confidence_score += 1
            else:
                break 
                
        if confidence_score == 4:
            print("!!! DEFEAT CONFIRMED (4/4 Confidence) !!!")
            human_click(GIVE_UP_X, GIVE_UP_Y) 
            time.sleep(2) 
            
            print("Pressing Escape to clear menu...")
            pyautogui.press('esc')
            time.sleep(1)
            
            raise GameFail 
        else:
            print(f"False Alarm! (Score: {confidence_score}/4). Resuming game...")

def smart_sleep(seconds):
    end_time = time.time() + seconds
    while time.time() < end_time:
        check_for_defeat()
        time.sleep(1) 

def human_click(x, y, wait=0.1):
    pyautogui.moveTo(x, y)
    pyautogui.mouseDown()
    time.sleep(wait)
    pyautogui.mouseUp()

def start_automation():
    global is_running
    if is_running:
        return
    is_running = True
    print("Automation started...")
    
    while True:
        try:
            time.sleep(3.5)
            human_click(89.5, 894)
            time.sleep(2)
            human_click(89.5, 894)
            time.sleep(2)
            human_click(89.5, 894)
            time.sleep(2)
            human_click(1075.5, 526.0)
            time.sleep(1)
            human_click(1406.0, 184.0)
            time.sleep(1)
            pyautogui.scroll(-50)
            time.sleep(1) 
            human_click(1405.0, 804.0, wait=0.2)
            time.sleep(1)
            human_click(349.0, 618.5)
            time.sleep(1)
            human_click(755.5, 824.0)
            time.sleep(4.5)

            
            check_for_defeat()
            human_click(442.0, 237.5)
            time.sleep(0.2)
            pyautogui.press('c')
            time.sleep(0.2)
            human_click(442.0, 237.5)
            time.sleep(0.1)
            pyautogui.press('.')
            pyautogui.press(',')
            pyautogui.press(',')
            time.sleep(0.2)

            
            check_for_defeat()
            human_click(449.0, 148.0)
            time.sleep(0.2)
            pyautogui.press('m')
            time.sleep(0.1)
            human_click(449.0, 148.0)
            pyautogui.press('.')
            pyautogui.press('.')
            pyautogui.press(',')
            pyautogui.press(',')
            pyautogui.press(',')
            
            pyautogui.press('.')
            pyautogui.press('.')
            pyautogui.press(',')
            pyautogui.press(',')
            pyautogui.press(',')
            time.sleep(0.2)

            
            check_for_defeat()
            human_click(544.0, 153.0)
            time.sleep(0.2)
            pyautogui.press('m')
            time.sleep(0.2)
            human_click(544.0, 153.0)
            pyautogui.press('.')
            pyautogui.press('.')
            pyautogui.press(',')
            pyautogui.press(',')
            pyautogui.press(',')
            
            pyautogui.press('.')
            pyautogui.press('.')
            pyautogui.press(',')
            pyautogui.press(',')
            pyautogui.press(',')
            time.sleep(0.2)

            
            check_for_defeat()
            human_click(451.5, 392.0)
            time.sleep(0.2)
            pyautogui.press('m')
            time.sleep(0.2)
            human_click(451.5, 392.0)
            pyautogui.press('.')
            pyautogui.press('.')
            pyautogui.press(',')
            pyautogui.press(',')
            pyautogui.press(',')
            
            pyautogui.press('.')
            pyautogui.press('.')
            pyautogui.press(',')
            pyautogui.press(',')
            pyautogui.press(',')
            time.sleep(0.2)

            
            check_for_defeat()
            human_click(293.5, 190.5)
            time.sleep(0.2)
            pyautogui.press('m')
            time.sleep(0.2)
            human_click(293.5, 190.5)
            pyautogui.press('.')
            pyautogui.press('.')
            pyautogui.press(',')
            pyautogui.press(',')
            pyautogui.press(',')
            
            pyautogui.press('.')
            pyautogui.press('.')
            pyautogui.press(',')
            pyautogui.press(',')
            pyautogui.press(',')
            time.sleep(0.2)

            pyautogui.press('space')
            pyautogui.press('space')
            pyautogui.press('space')

            
            smart_sleep(136)

            
            check_for_defeat()
            human_click(278.0, 287.5)
            time.sleep(0.2)
            pyautogui.press('m')
            time.sleep(0.2)
            human_click(278.0, 287.5)
            pyautogui.press('.')
            pyautogui.press('.')
            pyautogui.press(',')
            pyautogui.press(',')
            pyautogui.press(',')
            
            pyautogui.press('.')
            pyautogui.press('.')
            pyautogui.press(',')
            pyautogui.press(',')
            pyautogui.press(',')
            time.sleep(0.2)

            
            check_for_defeat()
            human_click(494.5, 90.5)
            time.sleep(0.2)
            pyautogui.press('m')
            time.sleep(0.2)
            human_click(494.5, 90.5)
            pyautogui.press('.')
            pyautogui.press('.')
            pyautogui.press('.')
            pyautogui.press(',')
            pyautogui.press(',')
            
            pyautogui.press('.')
            pyautogui.press('.')
            pyautogui.press('.')
            pyautogui.press(',')
            pyautogui.press(',')

            
            smart_sleep(95)
            
            check_for_defeat() 
            human_click(755.0, 827.0)

            print("Cycle done. Restarting...")

        except GameFail:
            print("Game Over detected! Resetting to Main Menu...")
            
            pyautogui.keyUp('c')
            pyautogui.keyUp('m')
            pyautogui.mouseUp() 
            
            time.sleep(2)
            continue

def on_press(key):
    try:
        if hasattr(key, 'char') and key.char == 'd':
            start_automation()
        if key == keyboard.Key.esc:
            print("Stopping automation...")
            return False
    except AttributeError:
        pass

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
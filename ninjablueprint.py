import pyautogui
from pynput import keyboard
import time
import Quartz.CoreGraphics as CG

is_running = False

class GameFail(Exception): 
    pass

SENSE_X, SENSE_Y = 1666, 1088      
TARGET_COLOR = (233, 6, 28)        
GIVE_UP_X, GIVE_UP_Y = 570.0, 792.5 #

def check_for_defeat():

    if pyautogui.pixelMatchesColor(SENSE_X, SENSE_Y, TARGET_COLOR, tolerance=25):
        print("⚠️ Possible Defeat Detected! Running Consensus Check...")
        
        confidence_score = 0
        
        for _ in range(4):
            time.sleep(0.2)
            if pyautogui.pixelMatchesColor(SENSE_X, SENSE_Y, TARGET_COLOR, tolerance=30):
                confidence_score += 1
            else:
                break 
                
        if confidence_score == 4:
            print("!!! DEFEAT CONFIRMED (4/4 Confidence) !!!")
            human_click(GIVE_UP_X, GIVE_UP_Y) 
            time.sleep(4) 
            
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

def quartz_flick(start_x, start_y, end_x, end_y):
    def send_event(ev_type, pos):
        event = CG.CGEventCreateMouseEvent(None, ev_type, pos, CG.kCGMouseButtonLeft)
        CG.CGEventPost(CG.kCGHIDEventTap, event)

    start_point = CG.CGPointMake(start_x, start_y)
    send_event(CG.kCGEventLeftMouseDown, start_point)
    time.sleep(0.2) 


    prime_pos = CG.CGPointMake(start_x - 10, start_y)
    send_event(CG.kCGEventLeftMouseDragged, prime_pos)
    time.sleep(0.05)

    steps = 40 
    for i in range(steps + 1):
        curr_x = start_x + (end_x - start_x) * (i / steps)
        curr_pos = CG.CGPointMake(curr_x, start_y) 
        send_event(CG.kCGEventLeftMouseDragged, curr_pos)
        time.sleep(0.01)

    send_event(CG.kCGEventLeftMouseUp, CG.CGPointMake(end_x, start_y))
    time.sleep(0.5)

def human_click(x, y, wait=0.1):
    pyautogui.moveTo(x, y)
    pyautogui.mouseDown()
    time.sleep(wait)
    pyautogui.mouseUp()

def start_automation():
    global is_running
    if is_running:
        print("Automation already active!")
        return
    
    is_running = True
    print("Automation started...")
    
    while True:
        try:

            time.sleep(3.5)
            human_click(89.5, 894)
            time.sleep(2)
            human_click(1075.5, 526.0)
            time.sleep(1)
            human_click(1406.0, 184.0)
            time.sleep(1)
            pyautogui.scroll(-50)
            time.sleep(1) 
            human_click(1405.0, 804.0, wait=0.2)
            time.sleep(5)
            
            quartz_flick(1170, 600, 300, 600)
            time.sleep(1)
            human_click(631.0, 375.5)
            time.sleep(1)
            human_click(755.5, 795.0)
            time.sleep(4)
            
            human_click(679.5, 636.5)
            time.sleep(0.2)
            pyautogui.press('t')
            time.sleep(0.2)
            human_click(679.5, 636.5)
            time.sleep(0.1)
            pyautogui.press(',', presses=5, interval=0.1)
            pyautogui.press('.', presses=3, interval=0.1)
            pyautogui.press('space')
            pyautogui.press('space')
            pyautogui.press('space')
            
            
            time.sleep(0.2)
            smart_sleep(46)
            pyautogui.press(',')
            smart_sleep(2)
            pyautogui.press(',')
            smart_sleep(3)
            pyautogui.press('space')
            time.sleep(0.2)
            human_click(679.5, 536.5)
            time.sleep(0.2)
            pyautogui.press('t')
            time.sleep(0.2)
            human_click(679.5, 536.5)
            time.sleep(0.1)
            pyautogui.press(',', presses=5, interval=0.1)
            pyautogui.press('.', presses=3, interval=0.1)
            time.sleep(4)
            pyautogui.press('space')
            pyautogui.press('space')
            pyautogui.press('space')
            smart_sleep(25)
            
            

            human_click(755.0, 795.0)
            print("Cycle done successfully. Restarting...")

        except GameFail:
            # If smart_sleep or any check triggers, it lands here and restarts Phase 1
            print("Resetting to Main Menu...")
            time.sleep(2)
            continue 

def on_press(key):
    try:
        if hasattr(key, 'char') and key.char == 'd':
            start_automation()
        if key == keyboard.Key.esc:
            print("Stopping...")
            return False
    except AttributeError:
        pass

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
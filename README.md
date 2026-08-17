# BTD6 Autoplay

A set of macOS automation scripts that play through fixed Bloons strategies unattended.

Written in Python with `pyautogui`, `pynput`, and raw Quartz CoreGraphics events for the input the higher-level libraries can't produce.

> **How to use.**
> Every coordinate in these scripts will be different across devices. The scripts are the working skeleton and the numbers inside them are placeholders you replace with your own using the included calibration tools.
>


---

## Requirements

- macOS for the Bloons Monkey City scripts, but works on all platforms for BTD6
- Python 3.9+
- Bloons(...)

```bash
pip install -r requirements.txt
```

### macOS permissions

Nothing will work until the terminal (or IDE) running the script is granted both of these in **System Settings → Privacy & Security**:

- **Accessibility** — lets `pyautogui` and `pynput` synthesise clicks and keystrokes
- **Screen Recording** — lets `pyautogui.pixel()` read the screen for defeat detection

Permissions are granted per-application, so running from iTerm and running from VS Code need separate approvals.

---

## Setting it up on your machine


There are three kinds of number to replace in any strategy file:

| What | Where | How to get yours |
| --- | --- | --- |
| Menu navigation clicks | The opening sequence of `start_automation()` — home, map select, difficulty, start | `CoordinateFinder.py` |
| Tower placement clicks | Every `human_click(x, y)` in the body of the run | `CoordinateFinder.py` or a manual read |
| The defeat sensor | `SENSE_X`, `SENSE_Y`, `TARGET_COLOR`, `GIVE_UP_X`, `GIVE_UP_Y` | `colourpicker.py`, verified with `restartmech.py` |

### 1. Calibrate the defeat sensor(restartmech.py)

Lose a game deliberately (or let one fail) to reach the end screen. Run `colourpicker.py`, park your cursor on a patch of the red banner that's solidly red and won't be overlapped by text, and wait for it to sample:

```bash
python colourpicker.py
```

It prints coordinates and an RGB triple. Paste those into `SENSE_X, SENSE_Y` and `TARGET_COLOR` at the top of each strategy file.

Then get the Give Up button's position with `CoordinateFinder.py` and set `GIVE_UP_X, GIVE_UP_Y`. That one is a *logical* coordinate, because it goes to `human_click` rather than to a pixel read.

Verify it

```bash
python restartmech.py   # press 'd'
```

It reports the RGB it actually saw and whether the match fired. If it misses, widen the tolerance or pick a less noisy pixel.

### 2. Capture the coordinates you need(coordinate finding)

For each button or tile the script has to hit, take a tight screenshot of it (⌘⇧4, drag a box — crop small, background pixels hurt the match), save it in the folder beside the script, and point `TARGET_IMAGE` at it:

```bash
python CoordinateFinder.py   # press 'p' with the game visible
```

It prints a ready-to-paste `human_click(x, y)` line with the Retina division already applied.

Tower placements work the same way, via landmarks. There's no icon sitting on an empty tile to match against so use a corner of the track, a rock, a bend in the path or even something like a piece of scenery like flowers. Screenshot that landmark instead, match it, and place the tower at a known offset from what `CoordinateFinder.py` returns(so like some coordinates cardinally away from it that you cna trial and error):

```python
LANDMARK = (743.0, 512.0)      # from CoordinateFinder.py
human_click(LANDMARK[0] - 40, LANDMARK[1] + 25)
```


### 3. Retime the run

The waits are tuned to how long rounds take at your fast-forward speed with your strategy. Once the clicks land in the right places, watch a full run and adjust each `smart_sleep()` until the upgrades arrive when you intended. Err long being early means the upgrade silently fails for lack of cash, and everything after it is then wrong too. Remember that by playing with autostart off and waiting a little before starting the next round can help the script catch up with any potential round popping variance(useful for consecratedground in BMC)

### 4. Add your own strategy

Copy the closest runner, keep `human_click`, `check_for_defeat`, `smart_sleep`, the `GameFail` class and the `try/except` loop exactly as they are, and rewrite only the body of `start_automation()` with your own sequence.

The pattern for a single tower is pretty much the same.

```python
human_click(x, y)              # click the map position
pyautogui.press('m')           # tower hotkey — places it
time.sleep(0.2)
human_click(x, y)              # click it again to select it
pyautogui.press('.')           # upgrade path 2
pyautogui.press(',')           # upgrade path 1
```

Then `space` to start the round.
---

## Usage

Once calibrated:

```bash
python consecratedground.py
```

Then switch to the game and press **`d`** to start the loop. Press **`esc`** to stop the listener and exit.

The keyboard listener runs globally, so the game window keeps focus while the script waits for the trigger.

---

## How it works

### Clicks the game will actually register

BTD6 sometimes ignores instantaneous synthetic clicks its a little finnicky, so every click is decomposed into a move, a press, a hold, and a release:

```python
def human_click(x, y, wait=0.1):
    pyautogui.moveTo(x, y)
    pyautogui.mouseDown()
    time.sleep(wait)
    pyautogui.mouseUp()
```

### Drags via Quartz

`pyautogui.dragTo()` doesn't move the map carousel as BMC needs a continuous stream of drag events with a small initial "prime" movement before it recognises the gesture as a drag rather than a click(because you have to drag to reach consecrated ground from the menu). `quartz_flick()` posts `kCGEventLeftMouseDragged` events directly to the HID event tap, interpolated across 40 steps:

```python
event = CG.CGEventCreateMouseEvent(None, ev_type, pos, CG.kCGMouseButtonLeft)
CG.CGEventPost(CG.kCGHIDEventTap, event)
```

### Defeat detection with a consensus check

The end-of-game screen is identified by a single red pixel at a fixed location. 

```python
if pyautogui.pixelMatchesColor(SENSE_X, SENSE_Y, TARGET_COLOR, tolerance=25):
    confidence_score = 0
    for _ in range(4):
        time.sleep(0.5)
        if pyautogui.pixelMatchesColor(SENSE_X, SENSE_Y, TARGET_COLOR, tolerance=30):
            confidence_score += 1
        else:
            break
```

A confirmed defeat clicks **Give Up**, escapes back to the menu, and raises `GameFail`. That exception unwinds out of wherever the run had reached and is caught by the loop in `start_automation()`, which restarts the strategy from the main menu meaning recovery logic lives in one place instead of being threaded through every wait. And it loops continuously even if you lose for some reason.

### Waiting without going blind

A plain `time.sleep(45)` between upgrade stages means 45 seconds of not noticing a loss. `smart_sleep()` slices the wait into one-second polls:

```python
def smart_sleep(seconds):
    end_time = time.time() + seconds
    while time.time() < end_time:
        check_for_defeat()
        time.sleep(1)
```

### Retina coordinate spaces

Two coordinate systems are in play:

| API | Space |
| --- | --- |
| `pyautogui.moveTo`, `click` | logical points (e.g. 1512 × 982) |
| `pyautogui.pixel`, `locateCenterOnScreen` | physical pixels (2× on Retina, this may differ on your device) |

Hence `colourpicker.py` doubles the cursor position before sampling, and `CoordinateFinder.py` halves what image matching returns. `SENSE_X, SENSE_Y` are physical; `GIVE_UP_X, GIVE_UP_Y` are logical.

---

## Scripts

### Strategy runners

| File | Towers used | Notes |
| --- | --- | --- |
| `consecratedground.py` | Apprentice (`h`), SuperMonkey (`g`) | Seven staged placements, full defeat detection |
| `moabyard.py` | Village (`c`), Spike Factory (`m`) | Detection checkpoints between every placement; releases held keys on failure |
| `ninjablueprint.py` | Ninjas (`t`) | Uses `quartz_flick` for map selection |
| `dartsnipe.py` | Dart Monkey (`q`), Sniper (`e`) | Longest run, ~15 placements; no defeat detection |
| `darkcastle.py` | Dart Monkey (`q`) | Single-placement, 6-minute run |

Upgrades are applied with the game's own path hotkeys — `,` `.` `/` for paths 1/2/3(or 1/2 in BMC) after re-selecting the tower, with `space` to start the round and fast-forward.


### Calibration tools

| File | Purpose |
| --- | --- |
| `colourpicker.py` | Hold the cursor over a pixel for 6s; prints its coordinates and RGB |
| `CoordinateFinder.py` | Screenshot a button or icon, point `TARGET_IMAGE` at it, then press `p` to locate it on screen and print Retina-corrected coordinates |
| `restartmech.py` | Isolates the defeat sensor — sit on the end screen, press `d`, and it reports whether the trigger pixel matched before clicking Give Up |

---

## Known limitations

- **Timing is open-loop.** Waits are tuned constants, not reads of game state, so a lag spike desynchronises the rest of the run. The only closed-loop signal is the defeat pixel.
- **`pixelMatchesColor` is deprecated** and removed in recent `pyscreeze` releases; the pinned version in `requirements.txt` still has it. Replacing it with a direct `pyautogui.pixel()` comparison would future-proof the sensor.
- **`is_running` is never reset**, so the flag only guards against a double-press of `d` within one process lifetime.
- **Only `moabyard.py` releases held keys** in its `GameFail` handler — the others can theoretically leave a modifier stuck if a failure lands mid-keypress.
- **Nothing adapts to the window.** Coordinates are absolute, so moving or resizing the game window invalidates every click and the defeat sensor with it. Resolving this properly would mean anchoring to a located reference image at startup and offsetting from it, rather than hard-coding — a worthwhile rewrite, and the reason `CoordinateFinder.py` exists in the first place.

---

## Disclaimer

Written for personal use on single player runs as a project. None of this is intended or even useful for competitive, co-op, or leaderboard play. 

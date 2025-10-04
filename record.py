import keyboard
import json
keyboard.press("alt")
keyboard.press_and_release("tab")
keyboard.release("alt")
'''
0) a
1) d
2) s
3) w
4) aw
5) dw
6) asw
7) dsw
8) null
'''
combos = [
    {
        "a": False,
        "d": False,
        "s": False,
        "w": False
    },
    {
        "a": True,
        "d": False,
        "s": False,
        "w": False
    },
    {
        "a": False,
        "d": True,
        "s": False,
        "w": False
    },
    {
        "a": False,
        "d": False,
        "s": True,
        "w": False
    },
    {
        "a": False,
        "d": False,
        "s": False,
        "w": True
    },
    {
        "a": True,
        "d": False,
        "s": False,
        "w": True
    },
    {
        "a": False,
        "d": True,
        "s": False,
        "w": True
    },
    {
        "a": True,
        "d": False,
        "s": True,
        "w": True
    },
    {
        "a": False,
        "d": True,
        "s": True,
        "w": True
    }
]
buttons = {
    "a": False,
    "d": False,
    "s": False,
    "w": False
}
pressed_keys, first_time, previous, recorded = [], 0, ['impossible','null',0,buttons], ''
events = keyboard.record(until='enter')
for event in events:
    filter = ['a','d','s','w']
    first_time = event.time if first_time == 0 else first_time
    currentKey = 'w' if event.name == 'up' else 's' if event.name == 'down' else 'a' if event.name == 'left' else 'd' if event.name == 'right' else event.name
    if event.name != previous[0] or event.event_type != previous[1]:
        if currentKey in filter:
            if event.event_type == 'down':
                buttons[f"{currentKey}"] = True
            elif event.event_type == 'up':
                buttons[f"{currentKey}"] = False
        for i in range(len(combos)):
            if buttons == combos[i]:
                move = i
        details = [event.name,event.event_type,move,event.time-first_time]
        previous = details.copy()
        pressed_keys.append(details.copy())
    else:
        pressed_keys[-1][3] = event.time-first_time
    for i in range(len(combos)):
        if buttons == combos[i]:
            move = i
    recorded = f"{recorded}{move}"
with open(f'game.json','w') as f:
    json.dump({"first_time":first_time,"moves":recorded,"pressed_keys":pressed_keys},f,indent=4)
keyboard.press("alt")
keyboard.press_and_release("tab")
keyboard.release("alt")
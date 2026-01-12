import time, threading, ctypes, tkinter as tk
from tkinter import ttk
import os, tempfile, shutil, sys, pythoncom
import pyWinhook as pyhook
user32 = ctypes.windll.user32
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
clicking = False
current_hotkey = "F6"
def mouse_click():
    user32.mouse_event(MOUSEEVENTF_LEFTDOWN,0,0,0,0)
    user32.mouse_event(MOUSEEVENTF_LEFTUP,0,0,0,0)
def autoclicker_loop():
    last_click = time.perf_counter()
    while True:
        now = time.perf_counter()
        if clicking:
            try:
                interval = max(float(interval_var.get()), 0.01)
            except:
                interval = 0.01
            if now - last_click >= interval:
                mouse_click()
                last_click = now
        time.sleep(0.001)
threading.Thread(target=autoclicker_loop, daemon=True).start()
def toggle_clicking():
    global clicking
    clicking = not clicking
    root.after(0, lambda: status_var.set("ON" if clicking else "OFF"))
    root.after(0, lambda: toggle_btn.config(text="Stop" if clicking else "Start"))
def on_keyboard_event(event):
    try:
        if event.Key.upper() == current_hotkey:
            toggle_clicking()
            return False
    except Exception:
        pass
    return True
def start_hook():
    hm = pyhook.HookManager()
    hm.KeyDown = on_keyboard_event
    hm.HookKeyboard()
    pythoncom.PumpMessages()
threading.Thread(target=start_hook, daemon=True).start()
root = tk.Tk()
root.title("DodyClicker")
root.resizable(False, False)
current_hotkey = "F6" 
key_display_var = tk.StringVar(value=current_hotkey)
src = os.path.join(getattr(sys,'_MEIPASS','.'),'icon.ico')
wicon = tempfile.NamedTemporaryFile(delete=False,suffix=".ico")
shutil.copy(src,wicon.name)
root.iconbitmap(wicon.name)
frame = ttk.Frame(root, padding=10)
frame.grid()
ttk.Label(frame, text="DodyClicker 1.2").grid(row=0, column=0, sticky="w")
ttk.Label(frame, text="Click wait (seconds):         ").grid(row=1, column=0, sticky="w")
interval_var = tk.StringVar(value="0")
ttk.Entry(frame, textvariable=interval_var, width=10).grid(row=1, column=1)
def apply_key():
    global current_hotkey
    new_key = togglekey.get().strip().upper()
    if not new_key:
        return
    current_hotkey = new_key
    key_display_var.set(current_hotkey)
ttk.Label(frame, text="Activation key:").grid(row=2, column=0, sticky="w")
togglekey = tk.StringVar(value=current_hotkey)
ttk.Entry(frame, textvariable=togglekey, width=10).grid(row=2, column=1)
ttk.Button(frame, text="Apply Key", command=lambda: apply_key()).grid(row=2, column=2, padx=5)
toggle_btn = ttk.Button(frame, text="Start", command=toggle_clicking)
toggle_btn.grid(row=4, column=1, columnspan=1, pady=5)
status_var = tk.StringVar(value="OFF")
ttk.Label(frame, text="Status:").grid(row=3, column=0, sticky="w")
status_label = tk.Label(frame, textvariable=status_var, width=10, relief="groove", borderwidth=1, anchor="center")
status_label.grid(row=3, column=1, sticky="w")
key_display = tk.Label(frame, textvariable=key_display_var, width=4, height=2, relief="groove", borderwidth=2, anchor="center", font=("Arial", 12))
key_display.grid(row=2, column=3, padx=5)
def on_close():
    root.destroy()
root.protocol("WM_DELETE_WINDOW", on_close)


root.mainloop()

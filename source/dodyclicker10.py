import time
import threading
import ctypes
import tkinter as tk
from tkinter import ttk
import keyboard
import os
import tempfile,shutil,sys
user32 = ctypes.windll.user32
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
clicking = False
def mouse_click():
    user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
def autoclicker_loop():
    while True:
        if clicking:
            mouse_click()
        time.sleep(max(float(interval_var.get()), 0.01))
def toggle_clicking():
    global clicking
    clicking = not clicking
    root.after(0, lambda: status_var.set("ON" if clicking else "OFF"))
    root.after(0, lambda: toggle_btn.config(text="Stop" if clicking else "Start"))

def hotkey_listener():
    keyboard.add_hotkey(toggle_key_var.get(), toggle_clicking, suppress=True)
    keyboard.wait()
root = tk.Tk()
root.title("DodyClicker")
src=os.path.join(getattr(sys,'_MEIPASS','.'),'icon.ico')
wicon=tempfile.NamedTemporaryFile(delete=False,suffix=".ico");shutil.copy(src,wicon.name);root.iconbitmap(wicon.name)
root.resizable(False, False)
frame = ttk.Frame(root, padding=10)
frame.grid()
ttk.Label(frame, text="Click wait (seconds):         ").grid(row=1, column=0, sticky="w")
interval_var = tk.StringVar(value="0")
ttk.Entry(frame, textvariable=interval_var, width=10).grid(row=1, column=1)
ttk.Label(frame, text="Activation key:").grid(row=2, column=0, sticky="w")
toggle_key_var = tk.StringVar(value="f6")
ttk.Entry(frame, textvariable=toggle_key_var, width=10).grid(row=2, column=1)
toggle_btn = ttk.Button(frame, text="Start", command=toggle_clicking)
toggle_btn.grid(row=4, column=1, columnspan=1, pady=5)
status_var = tk.StringVar(value="OFF")
ttk.Label(frame, text="Status:").grid(row=3, column=0, sticky="w")
status_label = tk.Label(frame,textvariable=status_var,width=10,relief="groove", borderwidth=1,anchor="center")
status_label.grid(row=3, column=1, sticky="w")
ttk.Label(frame, text="DodyClicker 1.0").grid(row=0, column=0, sticky="w")
threading.Thread(target=autoclicker_loop, daemon=True).start()
threading.Thread(target=hotkey_listener, daemon=True).start()
last_key = toggle_key_var.get()
def hotkey_updater():
    global last_key
    while True:
        key = toggle_key_var.get()
        if key != last_key:
            try: keyboard.remove_hotkey(last_key)
            except: pass
            keyboard.add_hotkey(key, toggle_clicking, suppress=True)
            last_key = key
        time.sleep(0.2)
threading.Thread(target=hotkey_updater, daemon=True).start()
root.mainloop()


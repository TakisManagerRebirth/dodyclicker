import time,threading,ctypes,ctypes.wintypes,queue,tkinter as tk,os,tempfile,shutil,sys
from tkinter import ttk
WINSIZE=1.4
WINFONT ="Segoe UI"
user32=ctypes.windll.user32
kernel32=ctypes.windll.kernel32
MOUSEEVENTF_LEFTDOWN=0x0002
MOUSEEVENTF_LEFTUP=0x0004
WM_HOTKEY=0x0312
WM_QUIT=0x0012
MOD_NONE=0x0000
HOTKEY_ID=1
clicking=False
current_hotkey_vk=0x75
hotkey_thread_id=0
hotkey_q=queue.Queue()
def mouse_click():
    user32.mouse_event(MOUSEEVENTF_LEFTDOWN,0,0,0,0)
    user32.mouse_event(MOUSEEVENTF_LEFTUP,0,0,0,0)
def autoclicker_loop():
    global last_click
    now=time.perf_counter()
    try:interval=max(float(interval_var.get()),0.01)
    except:interval=0.01
    if clicking and now-last_click>=interval:
        mouse_click()
        last_click=now
    root.after(6,autoclicker_loop)
def toggle_clicking():
    global clicking
    clicking=not clicking
    status_var.set("ON" if clicking else "OFF")
    toggle_btn.config(text="Stop" if clicking else "Start")
def apply_key():
    global current_hotkey_vk
    vk=togglekey.get().strip().upper()
    vk_dict = {
"ESC":0x1B,"F1":0x70,"F2":0x71,"F3":0x72,"F4":0x73,"F5":0x74,"F6":0x75,"F7":0x76,"F8":0x77,"F9":0x78,"F10":0x79,"F11":0x7A,"F12":0x7B,
"PRINTSCREEN":0x2C,"SCROLLLOCK":0x91,"PAUSE":0x13,"TILDE":0xC0,"1":0x31,"2":0x32,"3":0x33,"4":0x34,"5":0x35,"6":0x36,"7":0x37,"8":0x38,"9":0x39,"0":0x30,
"MINUS":0xBD,"EQUAL":0xBB,"BACKSPACE":0x08,"TAB":0x09,"Q":0x51,"W":0x57,"E":0x45,"R":0x52,"T":0x54,"Y":0x59,"U":0x55,"I":0x49,"O":0x4F,"P":0x50,
"LBRACKET":0xDB,"RBRACKET":0xDD,"BACKSLASH":0xDC,"CAPSLOCK":0x14,"A":0x41,"S":0x53,"D":0x44,"F":0x46,"G":0x47,"H":0x48,"J":0x4A,"K":0x4B,"L":0x4C,
"SEMICOLON":0xBA,"APOSTROPHE":0xDE,"ENTER":0x0D,"LSHIFT":0xA0,"Z":0x5A,"X":0x58,"C":0x43,"V":0x56,"B":0x42,"N":0x4E,"M":0x4D,"COMMA":0xBC,"PERIOD":0xBE,"SLASH":0xBF,"RSHIFT":0xA1,
"LMENU":0xA4,"SPACE":0x20,"RMENU":0xA5,"LCTRL":0xA2,"RCTRL":0xA3,"LWIN":0x5B,"RWIN":0x5C,"APPS":0x5D,"INSERT":0x2D,"HOME":0x24,"PAGEUP":0x21,"DELETE":0x2E,"END":0x23,"PAGEDOWN":0x22,
"UP":0x26,"DOWN":0x28,"LEFT":0x25,"RIGHT":0x27,
"NUMLOCK":0x90,"NUMPAD0":0x60,"NUMPAD1":0x61,"NUMPAD2":0x62,"NUMPAD3":0x63,"NUMPAD4":0x64,"NUMPAD5":0x65,"NUMPAD6":0x66,"NUMPAD7":0x67,"NUMPAD8":0x68,"NUMPAD9":0x69,
"NUMPADMULT":0x6A,"NUMPADADD":0x6B,"NUMPADSEPARATOR":0x6C,"NUMPADSUB":0x6D,"NUMPADDOT":0x6E,"NUMPADDIV":0x6F
    }
    if vk in vk_dict:
        user32.PostThreadMessageW(hotkey_thread_id,WM_QUIT,0,0)
        user32.UnregisterHotKey(None,HOTKEY_ID)
        current_hotkey_vk=vk_dict[vk]
        t=threading.Thread(target=hotkey_thread,daemon=True);t.start()
        key_display_var.set(vk)
def hotkey_thread():
    global hotkey_thread_id
    hotkey_thread_id=kernel32.GetCurrentThreadId()
    if not user32.RegisterHotKey(None,HOTKEY_ID,MOD_NONE,current_hotkey_vk):
        return
    msg=ctypes.wintypes.MSG()
    while True:
        ret=user32.GetMessageW(ctypes.byref(msg),None,0,0)
        if ret==0:
            break
        if ret==-1:
            break
        if msg.message==WM_HOTKEY and msg.wParam==HOTKEY_ID:
            try:hotkey_q.put_nowait(True)
            except:pass
        user32.TranslateMessage(ctypes.byref(msg))
        user32.DispatchMessageW(ctypes.byref(msg))
    user32.UnregisterHotKey(None,HOTKEY_ID)
def poll_hotkey_queue():
    try:
        while True:
            hotkey_q.get_nowait()
            toggle_clicking()
    except:
        pass
    root.after(20,poll_hotkey_queue)
root=tk.Tk()
root.title("DodyClicker")
root.resizable(False,False)
try:ctypes.windll.shcore.SetProcessDpiAwareness(1)
except:pass
root.tk.call("tk","scaling",WINSIZE)
key_display_var=tk.StringVar(value="F6")
src=os.path.join(getattr(sys,'_MEIPASS','.'), 'icon.ico')
wicon=tempfile.NamedTemporaryFile(delete=False,suffix=".ico")
try:shutil.copy(src,wicon.name)
except:pass
wicon.close()
try:root.iconbitmap(wicon.name)
except:pass
frame=ttk.Frame(root,padding=int(10*WINSIZE));frame.grid()
ttk.Label(frame,text="DodyClicker 1.3",font=(WINFONT,int(12*WINSIZE))).grid(row=0,column=0,sticky="w")
ttk.Label(frame,text="Click wait (seconds):",font=(WINFONT,int(10*WINSIZE))).grid(row=1,column=0,sticky="w")
interval_var=tk.StringVar(value="0")
ttk.Entry(frame,textvariable=interval_var,width=int(10*WINSIZE),font=(WINFONT,int(10*WINSIZE))).grid(row=1,column=1)
ttk.Label(frame,text="Trigger key:",font=(WINFONT,int(10*WINSIZE))).grid(row=2,column=0,sticky="w")
togglekey=tk.StringVar(value="F6")
ttk.Entry(frame,textvariable=togglekey,width=int(10*WINSIZE),font=(WINFONT,int(10*WINSIZE))).grid(row=2,column=1)
ttk.Button(frame,text="Apply Key",command=apply_key).grid(row=2,column=2,padx=int(5*WINSIZE))
toggle_btn=ttk.Button(frame,text="Start",command=toggle_clicking,width=int(15*WINSIZE));toggle_btn.grid(row=4,column=1,pady=int(8*WINSIZE))
status_var=tk.StringVar(value="OFF");ttk.Label(frame,text="Status:",width=int(10*WINSIZE),font=(WINFONT,int(10*WINSIZE))).grid(row=3,column=0,sticky="w")
status_label=tk.Label(frame,textvariable=status_var,width=int(10*WINSIZE),relief="groove",borderwidth=1,anchor="center",font=(WINFONT,int(10*WINSIZE)));status_label.grid(row=3,column=1,sticky="w")
key_display=tk.Label(frame,textvariable=key_display_var,width=int(4*WINSIZE),height=int(2*WINSIZE),relief="groove",borderwidth=2,anchor="center",font=(WINFONT,int(12*WINSIZE)));key_display.grid(row=2,column=3,padx=int(5*WINSIZE))
last_click=time.perf_counter()
t=threading.Thread(target=hotkey_thread,daemon=True);t.start()
root.after(6,autoclicker_loop)
root.after(20,poll_hotkey_queue)
def on_close():
    try:user32.PostThreadMessageW(hotkey_thread_id,WM_QUIT,0,0)
    except:pass
    try:user32.UnregisterHotKey(None,HOTKEY_ID)
    except:pass
    try:os.unlink(wicon.name)
    except:pass
    root.destroy()
root.protocol("WM_DELETE_WINDOW",on_close)


root.mainloop()
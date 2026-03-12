import time,threading,ctypes,ctypes.wintypes,queue,tkinter as tk,os,tempfile,shutil,sys
from tkinter import ttk
F="Segoe UI"
user=ctypes.windll.user32
krnl=ctypes.windll.kernel32
IM,IK,MDL,MLU,MDR,MRU,KDN,KUP,WH,WQ,MN,HK=0,1,0x0002,0x0004,0x0008,0x0010,0x0000,0x0002,0x0312,0x0012,0x0000,1
dc=user.GetDC(0)
dpi=ctypes.windll.gdi32.GetDeviceCaps(dc,88)
user.ReleaseDC(0,dc)
BASE_W=1.4
W=(dpi/96)*BASE_W
class MI(ctypes.Structure):
 _fields_=[("dx",ctypes.c_long),("dy",ctypes.c_long),("mouseData",ctypes.c_ulong),("dwFlags",ctypes.c_ulong),("time",ctypes.c_ulong),("dwExtraInfo",ctypes.POINTER(ctypes.c_ulong))]
class KI(ctypes.Structure):
 _fields_=[("wVk",ctypes.c_ushort),("wScan",ctypes.c_ushort),("dwFlags",ctypes.c_ulong),("time",ctypes.c_ulong),("dwExtraInfo",ctypes.POINTER(ctypes.c_ulong))]
class II(ctypes.Union):
 _fields_=[("mi",MI),("ki",KI)]
class I(ctypes.Structure):
 _fields_=[("type",ctypes.c_ulong),("ii",II)]
clk,hk_vk,htid,q,auto_id,hk_id=False,0x75,0,queue.Queue(),None,None
D={
 "A":0x41,"B":0x42,"C":0x43,"D":0x44,"E":0x45,"F":0x46,"G":0x47,"H":0x48,"I":0x49,"J":0x4A,"K":0x4B,"L":0x4C,"M":0x4D,"N":0x4E,"O":0x4F,"P":0x50,
 "Q":0x51,"R":0x52,"S":0x53,"T":0x54,"U":0x55,"V":0x56,"W":0x57,"X":0x58,"Y":0x59,"Z":0x5A,
 "0":0x30,"1":0x31,"2":0x32,"3":0x33,"4":0x34,"5":0x35,"6":0x36,"7":0x37,"8":0x38,"9":0x39,
 "F1":0x70,"F2":0x71,"F3":0x72,"F4":0x73,"F5":0x74,"F6":0x75,"F7":0x76,"F8":0x77,"F9":0x78,"F10":0x79,"F11":0x7A,"F12":0x7B,
 "NUM0":0x60,"NUM1":0x61,"NUM2":0x62,"NUM3":0x63,"NUM4":0x64,"NUM5":0x65,"NUM6":0x66,"NUM7":0x67,"NUM8":0x68,"NUM9":0x69,
 "NUM*":0x6A,"NUM+":0x6B,"NUM-":0x6D,"NUM.":0x6E,"NUM/":0x6F,
 "BACKSPACE":0x08,"TAB":0x09,"ENTER":0x0D,"SHIFT":0x10,"CTRL":0x11,"ALT":0x12,"CAPSLOCK":0x14,
 "ESC":0x1B,"SPACE":0x20," ":0x20,"PAGEUP":0x21,"PAGEDOWN":0x22,"END":0x23,"HOME":0x24,
 "LEFT":0x25,"UP":0x26,"RIGHT":0x27,"DOWN":0x28,
 "INS":0x2D,"DEL":0x2E,"`":0xC0,
 "OEM_1":0xBA,"OEM_PLUS":0xBB,"OEM_COMMA":0xBC,"OEM_MINUS":0xBD,"OEM_PERIOD":0xBE,"OEM_2":0xBF,"OEM_3":0xC0,
 "OEM_4":0xDB,"OEM_5":0xDC,"OEM_6":0xDD,"OEM_7":0xDE
}
def sm(f):
 i=I(IM,II(mi=MI(0,0,0,f,0,None)))
 user.SendInput(1,ctypes.byref(i),ctypes.sizeof(i))
def sk(v,f):
 i=I(IK,II(ki=KI(v,ctypes.windll.user32.MapVirtualKeyW(v,0),f,0,None)))
 user.SendInput(1,ctypes.byref(i),ctypes.sizeof(i))
def mc():
 if not clk:return
 m=mode.get()
 if m=="RIGHT":sm(MDR);sm(MRU)
 elif m=="LEFT":sm(MDL);sm(MLU)
 else:
  v=skv.get().upper()
  if v in D:
   vk=D[v]
   sk(vk,KDN);sk(vk,KUP)
def loop():
 global lc,auto_id
 n=time.perf_counter()
 if not clk:auto_id=root.after(1,loop);return
 try:
  iv_val=float(iv.get())
  if iv_val < 0.0075: iv_val = 0.0075
 except:iv_val=0.0075
 if clk and n-lc>=iv_val:mc();lc=n
 auto_id=root.after(1,loop)
def toggle():
 global clk,lc
 clk=not clk
 lc=time.perf_counter()
 st.set("ON" if clk else "OFF")
 btn.config(text="Stop" if clk else "Start")
def setkey():
 global hk_vk
 v=tkv.get().strip().upper()
 if v in D:
  hk_vk=D[v]
  if htid:user.PostThreadMessageW(htid,WQ,0,0)
def ht():
 global htid
 htid=krnl.GetCurrentThreadId()
 while True:
  user.UnregisterHotKey(None,HK)
  if not user.RegisterHotKey(None,HK,MN,hk_vk):break
  m=ctypes.wintypes.MSG()
  while user.GetMessageW(ctypes.byref(m),None,0,0)>0:
   if m.message==WH:q.put(1)
   elif m.message==WQ:break
  if m.message==WQ:continue
def poll():
 running = True
 if not running:return
 try:
  while 1:q.get_nowait();toggle()
 except:pass
 if running:root.after(20,poll)
root=tk.Tk()
root.title("DodyClicker 1.6")
root.resizable(False,False)
try:ctypes.windll.shcore.SetProcessDpiAwareness(1)
except:pass
root.tk.call("tk","scaling",W)
iv,tkv,skv,st,mode=tk.StringVar(value="0"),tk.StringVar(value="F6"),tk.StringVar(value=""),tk.StringVar(value="OFF"),tk.StringVar(value="LEFT")
wico_name=""
try:
 src=os.path.join(getattr(sys,'_MEIPASS','.'),'icon.ico')
 wico=tempfile.NamedTemporaryFile(delete=False,suffix=".ico")
 wico_name=wico.name;wico.close()
 shutil.copy(src,wico_name);root.iconbitmap(wico_name)
except:pass
f=ttk.Frame(root,padding=int(10*W));f.grid()
ttk.Label(f,text="DodyClicker 1.6",font=(F,int(12*W))).grid(row=0,column=0,sticky="w")
ttk.Label(f,text="Click wait (seconds):",font=(F,int(10*W))).grid(row=1,column=0,sticky="w")
ttk.Entry(f,textvariable=iv,width=8,font=(F,int(10*W))).grid(row=1,column=1)
ttk.Label(f,text="Trigger key:",font=(F,int(10*W))).grid(row=2,column=0,sticky="w")
e1=ttk.Entry(f,textvariable=tkv,width=8,font=(F,int(10*W)))
e1.grid(row=2,column=1);e1.bind("<FocusOut>",lambda _:setkey())
ttk.Label(f,text="Click type:",font=(F,int(10*W))).grid(row=3,column=0,sticky="w")
ttk.Label(f,text="Spamkey (optional):",font=(F,int(10*W))).grid(row=4,column=0,sticky="w")
ttk.Radiobutton(f,text="Left",variable=mode,value="LEFT").grid(row=3,column=1,sticky="w")
ttk.Radiobutton(f,text="Right",variable=mode,value="RIGHT").grid(row=3,column=2,sticky="w")
ttk.Radiobutton(f,text="Key:",variable=mode,value="KEY").grid(row=4,column=1,sticky="w")
ttk.Entry(f,textvariable=skv,width=8,font=(F,int(10*W))).grid(row=4,column=2,sticky="w")
tk.Label(f,textvariable=st,width=8,relief="groove",anchor="center",font=(F,int(10*W))).grid(row=5,column=2,sticky="w")
btn=ttk.Button(f,text="Start",command=toggle,width=12,padding=(1,5))
btn.grid(row=5,column=1,pady=int(8*W),sticky="w")
lc=time.perf_counter()
threading.Thread(target=ht,daemon=True).start()
root.after(5,loop)
root.after(20,poll)
root.bind_all("<Button-1>",lambda e:root.focus_set() if not isinstance(e.widget,tk.Entry) else None,add="+")
def close():
 try:
  if auto_id:root.after_cancel(auto_id)
  if htid:user.PostThreadMessageW(htid,WQ,0,0)
  user.UnregisterHotKey(None,HK)
  if wico_name:os.unlink(wico_name)
 except:pass
 root.destroy()
root.protocol("WM_DELETE_WINDOW",close)
root.mainloop()
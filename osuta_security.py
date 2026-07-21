import hashlib
import base64
import datetime
import requests
import os
import subprocess
import uuid
import sys

# --- CONFIGURATION ---
# All Free စနစ် ဖြစ်သည့်အတွက် Token/Trial logic များ လိုအပ်တော့ပါ။

def check_activation(device_id=None):
    """
    All Free စနစ်ဖြစ်သောကြောင့် မည်သည့် Device မျိုးတွင်မဆို 
    အမြဲတမ်း True (Unlimited) ကိုသာ Return ပြန်ပေးပါမည်။
    """
    return True, "Unlimited Free"

def get_device_id():
    """
    Script ၏ အခြားနေရာများတွင် Device ID လိုအပ်ပါက သုံးနိုင်ရန် ထိန်းသိမ်းထားပေးပါသည်။
    """
    hwid_paths = ["/sdcard/.osuta_sys_id", "/data/data/com.termux/files/home/.osuta_sys_id", ".osuta_sys_id"]
    for path in hwid_paths:
        try:
            if os.path.exists(path) and os.path.getsize(path) > 0:
                with open(path, 'r') as f:
                    sid = f.read().strip()
                    if len(sid) == 16: return sid
        except: continue

    hw_info = ""
    props = ["ro.product.model", "ro.product.brand", "ro.serialno"]
    for prop in props:
        try:
            out = subprocess.check_output(f"getprop {prop}", shell=True, stderr=subprocess.DEVNULL).decode().strip()
            if out and out != "unknown": hw_info += out
        except: pass
    try:
        aid = subprocess.check_output("settings get secure android_id", shell=True, stderr=subprocess.DEVNULL).decode().strip()
        if aid and aid != "null": hw_info += aid
    except: pass
    
    if not hw_info: hw_info = str(uuid.getnode())
    new_hwid = hashlib.sha256(f"OSUTA_PRO_{hw_info}".encode()).hexdigest()[:16].upper()

    for path in hwid_paths:
        try:
            with open(path, 'w') as f: f.write(new_hwid)
        except: continue
    return new_hwid

# --- MAIN EXECUTION EXAMPLE ---
if __name__ == "__main__":
    is_active, status = check_activation()
    if is_active:
        print(f"\033[1;32m[✓] Access Granted: {status}\033[0m")
        # ဒီအောက်မှာ သင့်ရဲ့ အဓိက Script/Bot Logic များကို ဆက်လက် Run နိုင်ပါသည်။

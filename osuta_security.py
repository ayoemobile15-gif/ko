import hashlib
import base64
import datetime
import requests
import os
import subprocess
import uuid
import sys

# --- CONFIGURATION ---
SECRET_KEY = "OSUTA_PRIVATE_SECRET_2026"

def get_token_path():
    paths = ["/sdcard/.osuta_token", "/data/data/com.termux/files/home/.osuta_token", ".osuta_token"]
    for p in paths:
        try:
            with open(p, 'a') as f: pass
            return p
        except: continue
    return ".osuta_token"

def get_trial_path():
    paths = ["/sdcard/.osuta_trial", "/data/data/com.termux/files/home/.osuta_trial", ".osuta_trial"]
    for p in paths:
        try:
            with open(p, 'a') as f: pass
            return p
        except: continue
    return ".osuta_trial"

def get_internet_time():
    time_apis = [
        'http://worldtimeapi.org/api/timezone/Asia/Yangon',
        'https://timeapi.io/api/Time/current/zone?timeZone=Asia/Yangon'
    ]
    for api in time_apis:
        try:
            response = requests.get(api, timeout=5)
            if response.status_code == 200:
                data = response.json()
                dt_str = data.get('datetime') or data.get('currentDateTime')
                if dt_str: return datetime.datetime.fromisoformat(dt_str.split('.')[0])
        except: continue
    try:
        res = requests.get('http://www.google.com', timeout=5)
        return datetime.datetime.strptime(res.headers['Date'], '%a, %d %b %Y %H:%M:%S GMT')
    except: return datetime.datetime.now()

def check_trial(device_id):
    """
    All Free စနစ်ဖြစ်သောကြောင့် Trial / Expiry လုံးဝ မစစ်တော့ဘဲ 
    အမြဲတမ်း Unlimited Free ခွင့်ပြုပေးမည်။
    """
    return True, "Unlimited Free"

def check_activation(device_id):
    """
    မည်သည့် Device တွင်မဆို Token သို့မဟုတ် Trial လိုအပ်ချက်မရှိဘဲ တန်းဝင်ရောက်နိုင်မည်။
    """
    return True, "Unlimited Free"

# --- ၁။ မူရင်းအတိုင်း အတိအကျ ထားရှိပေးထားသော GET_DEVICE_ID FUNCTION ---
def get_device_id():
    hwid_paths = ["/sdcard/.osuta_sys_id", "/data/data/com.termux/files/home/.osuta_sys_id", ".osuta_sys_id"]
    for path in hwid_paths:
        try:
            if os.path.exists(path):
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

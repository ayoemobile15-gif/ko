import hashlib
import os
import subprocess
import uuid


def get_token_path():
    paths = [
        "/sdcard/.osuta_token",
        "/data/data/com.termux/files/home/.osuta_token",
        ".osuta_token",
    ]
    for path in paths:
        try:
            with open(path, "a"):
                pass
            return path
        except Exception:
            continue
    return ".osuta_token"


def get_trial_path():
    paths = [
        "/sdcard/.osuta_trial",
        "/data/data/com.termux/files/home/.osuta_trial",
        ".osuta_trial",
    ]
    for path in paths:
        try:
            with open(path, "a"):
                pass
            return path
        except Exception:
            continue
    return ".osuta_trial"


def check_trial(device_id):
    return True, "Unlimited Free"


def check_activation(device_id):
    return True, "Unlimited Free"


def get_device_id():
    hwid_paths = [
        "/sdcard/.osuta_sys_id",
        "/data/data/com.termux/files/home/.osuta_sys_id",
        ".osuta_sys_id",
    ]

    for path in hwid_paths:
        try:
            if os.path.exists(path):
                with open(path, "r") as f:
                    sid = f.read().strip()
                if len(sid) == 16:
                    return sid
        except Exception:
            continue

    hw_info = ""
    props = ["ro.product.model", "ro.product.brand", "ro.serialno"]

    for prop in props:
        try:
            out = subprocess.check_output(
                f"getprop {prop}",
                shell=True,
                stderr=subprocess.DEVNULL,
            ).decode().strip()
            if out and out != "unknown":
                hw_info += out
        except Exception:
            pass

    try:
        aid = subprocess.check_output(
            "settings get secure android_id",
            shell=True,
            stderr=subprocess.DEVNULL,
        ).decode().strip()
        if aid and aid != "null":
            hw_info += aid
    except Exception:
        pass

    if not hw_info:
        hw_info = str(uuid.getnode())

    new_hwid = hashlib.sha256(f"OSUTA_PRO_{hw_info}".encode()).hexdigest()[:16].upper()

    for path in hwid_paths:
        try:
            with open(path, "w") as f:
                f.write(new_hwid)
            break
        except Exception:
            continue

    return new_hwid

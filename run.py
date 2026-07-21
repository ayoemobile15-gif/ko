import os
import sys
import time
import osuta_security

G = "\033[1;32m"
R = "\033[1;31m"
Y = "\033[1;33m"
C = "\033[1;36m"
W = "\033[1;37m"
RESET = "\033[0m"


def show_logo():
    os.system("clear" if os.name == "posix" else "cls")
    print(f"""{C}
 ██████ ███████ ██ ██ ████████ █████
 ██     ██      ██ ██    ██    ██
 ██     ███████ ██ ██    ██    ███████
 ██     ██      ██ ██    ██         ██
 ██████ ███████ ██████  ██    ███████
{RESET}
{G} [ OSUTA FREE TOOL ] {RESET}
{Y} ---------------------------------------------- {RESET}
{W} Author   : OSUTA {RESET}
{W} Version  : 1.1.0 Free {RESET}
{W} Telegram : @osuta247 {RESET}
{Y} ---------------------------------------------- {RESET}
""")


def load_ko_module():
    try:
        import ko
    except ImportError:
        print(f"{R}[-] Error: ko module not found!{RESET}")
        sys.exit(1)

    if hasattr(ko, "check_activation"):
        ko.check_activation = lambda: True
    if hasattr(ko, "Logo"):
        ko.Logo = show_logo

    return ko


def main():
    dev_id = osuta_security.get_device_id()
    status, result = osuta_security.check_activation(dev_id)

    if not status:
        show_logo()
        print(f"{R}[-] Activation check failed: {result}{RESET}")
        print(f"{W}Device ID: {Y}{dev_id}{RESET}")
        sys.exit(1)

    ko = load_ko_module()

    while True:
        show_logo()
        print(f"{G} [+] Status: Activated ({result}){RESET}")
        print(f"{Y} ---------------------------------------------- {RESET}")
        print(f"{W} [1] ADB Connect Tool{RESET}")
        print(f"{W} [2] Auto Bypass (Scan + Ruijie){RESET}")
        print(f"{W} [3] Exit Tool{RESET}")
        print(f"{Y} ---------------------------------------------- {RESET}")

        choice = input(f"{C} Select Option >> {RESET}").strip()

        if choice == "1":
            if hasattr(ko, "option_adb_connect"):
                ko.option_adb_connect()
            else:
                print(f"{R}[-] Function not found in ko module!{RESET}")
        elif choice == "2":
            if hasattr(ko, "option_auto_bypass"):
                ko.option_auto_bypass()
            else:
                print(f"{R}[-] Function not found in ko module!{RESET}")
        elif choice == "3":
            print(f"
{G}[+] Thank you for using OSUTA! Goodbye.{RESET}")
            break
        else:
            print(f"
{R}[-] Invalid Option!{RESET}")

        time.sleep(1)


if __name__ == "__main__":
    main()

import subprocess
import os
import re

def is_nvidia_prime_installed():
    try:
        result = subprocess.run(['rpm', '-q', 'nvidia-prime'], stdout=subprocess.PIPE, text=True)
        return 'nvidia-prime' in result.stdout
    except:
        return False

def is_bumblebee_installed():
    try:
        result = subprocess.run(['rpm', '-q', 'bumblebee'], stdout=subprocess.PIPE, text=True)
        return 'bumblebee' in result.stdout
    except:
        return False

def check_drm_devices():
    try:
        drm_devices = os.listdir('/sys/class/drm/')
        return 'card0' in drm_devices and 'card1' in drm_devices
    except:
        return False

def check_xorg_log():
    try:
        with open('/var/log/Xorg.0.log', 'r') as log_file:
            log_content = log_file.read()
            return 'NVIDIA' in log_content
    except:
        return False

def check_prime_select():
    try:
        result = subprocess.run(['prime-select', 'query'], stdout=subprocess.PIPE, text=True)
        return result.stdout.strip() in ['nvidia', 'intel']
    except:
        return False

def get_installed_gpus():
    try:
        result = subprocess.run(['lspci'], stdout=subprocess.PIPE, text=True)
        gpus = []
        for line in result.stdout.splitlines():
            if 'VGA compatible controller' in line or '3D controller' in line:
                gpus.append(line.strip())
        return gpus
    except Exception as e:
        print(f"Fehler beim Abrufen der Grafikkarten: {e}")
        return []

def is_nvidia_optimus():
    nvidia_prime = is_nvidia_prime_installed()
    bumblebee = is_bumblebee_installed()
    drm_check = check_drm_devices()
    xorg_check = check_xorg_log()
    prime_check = check_prime_select()

    return (nvidia_prime or bumblebee) and (drm_check or xorg_check or prime_check)

if __name__ == "__main__":
    gpus = get_installed_gpus()
    has_nvidia = any('NVIDIA' in gpu for gpu in gpus)
    has_other_gpus = len(gpus) > 1  # Überprüfen, ob mehr als eine GPU vorhanden ist

    if is_nvidia_optimus():
        if has_nvidia and has_other_gpus:
            print("NVIDIA Optimus-Konfiguration wahrscheinlich vorhanden.")
            print("Gefundene Grafikkarten:")
            for gpu in gpus:
                print(f" - {gpu}")
        else:
            print("NVIDIA-Grafikkarte erkannt, aber keine andere GPU gefunden.")
    else:
        print("Keine NVIDIA Optimus-Konfiguration erkannt.")

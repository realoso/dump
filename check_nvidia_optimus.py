import subprocess
import os

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

def is_nvidia_optimus():
    nvidia_prime = is_nvidia_prime_installed()
    bumblebee = is_bumblebee_installed()
    drm_check = check_drm_devices()
    xorg_check = check_xorg_log()
    prime_check = check_prime_select()

    return (nvidia_prime or bumblebee) and (drm_check or xorg_check or prime_check)

if __name__ == "__main__":
    if is_nvidia_optimus():
        print("NVIDIA Optimus-Konfiguration erkannt.")
    else:
        print("Keine NVIDIA Optimus-Konfiguration erkannt.")

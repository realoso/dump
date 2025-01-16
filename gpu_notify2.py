import subprocess
import re

def get_gpu_info():
    try:
        result = subprocess.run(['lspci'], stdout=subprocess.PIPE, text=True)
        gpu_lines = []
        
        for line in result.stdout.splitlines():
            if 'VGA compatible controller' in line or '3D controller' in line:
                gpu_lines.append(line.strip())
        
        return gpu_lines if gpu_lines else ["Keine GPU gefunden."]
    
    except Exception as e:
        return [f"Ein Fehler ist aufgetreten: {e}"]

def format_gpu_manufacturer(gpu):
    if 'NVIDIA' in gpu:
        manufacturer = "NVIDIA"
    elif 'AMD' in gpu or 'Advanced Micro Devices' in gpu or 'American Micro Devices' in gpu:
        manufacturer = "AMD"
    elif 'Intel' in gpu:
        manufacturer = "INTEL"
    else:
        manufacturer = "UNBEKANNT"

    return manufacturer

def format_gpu_model(gpu):
    end = gpu.rfind(']')
    
    if end != -1:
        start = gpu.rfind('[', 0, end)  # Suche nach der letzten öffnenden Klammer vor der schließenden Klammer
        if start != -1:
            return gpu[start + 1:end].strip()  # Gibt den Text zwischen den Klammern zurück
    return "Modell unbekannt"


def display_gpu_info():
    gpu_info = get_gpu_info()
    
    for gpu in gpu_info:
        print(gpu)
        titel = format_gpu_manufacturer(gpu)
        text = format_gpu_model(gpu)
        
        # Sende die Benachrichtigung mit notify-send
        subprocess.run(['notify-send', '-a', 'GPU Detector', titel, text, '-t', '5000'])  # 5000 ms = 5 Sekunden

if __name__ == "__main__":
    display_gpu_info()

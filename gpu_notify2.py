import subprocess

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

def format_gpu_title(gpu):
    # Bestimme den Hersteller und die Modellbezeichnung
    if 'NVIDIA' in gpu:
        manufacturer = "NVIDIA"
        full_manufacturer = "NVIDIA Corporation"
    elif 'AMD' in gpu or 'Advanced Micro Devices' in gpu or 'American Micro Devices' in gpu:
        manufacturer = "AMD"
        full_manufacturer = "Advanced Micro Devices"
    elif 'Intel' in gpu:
        manufacturer = "INTEL"
        full_manufacturer = "Intel Corporation"
    else:
        manufacturer = "UNBEKANNT"
        full_manufacturer = "Unbekannt"

    # Extrahiere die Modellbezeichnung
    model_start = gpu.split(':', 2)[2].strip() if ':' in gpu else gpu
    model_parts = model_start.split(' ')
    
    # Halte die Modellbezeichnung kurz und lesbar
    if manufacturer == "NVIDIA":
        model = ' '.join(model_parts[1:3])  # Z.B. "GeForce GTX 1060" -> "GTX 1060"
    elif manufacturer == "AMD":
        model = ' '.join(model_parts[1:])  # Z.B. "Radeon RX 580" -> "RX 580"
    elif manufacturer == "INTEL":
        model = ' '.join(model_parts[1:])  # Z.B. "UHD Graphics 620" -> "UHD 620"
    else:
        model = "Modell unbekannt"
    print(manufacturer)
    print(model)
    return manufacturer, model

def display_gpu_info():
    gpu_info = get_gpu_info()
    
    for gpu in gpu_info:
        hersteller, generation = format_gpu_title(gpu)
        
        # Sende die Benachrichtigung mit notify-send
        subprocess.run(['notify-send', '-a', 'GPU Detector', hersteller, generation, '-t', '5000'])  # 5000 ms = 5 Sekunden

if __name__ == "__main__":
    display_gpu_info()

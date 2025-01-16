import subprocess

def get_gpu_info():
    try:
        result = subprocess.run(['lspci'], stdout=subprocess.PIPE, text=True)
        gpu_lines = []
        
        for line in result.stdout.splitlines():
            if 'VGA compatible controller' in line or '3D controller' in line:
                gpu_lines.append(line.strip())
        
        if gpu_lines:
            return "\n".join(gpu_lines)
        else:
            return "Keine GPU gefunden."
    
    except Exception as e:
        return f"Ein Fehler ist aufgetreten: {e}"

def display_gpu_info():
    gpu_info = get_gpu_info()
    
    # Sende die Benachrichtigung mit notify-send und setze den Anwendungsnamen
    subprocess.run(['notify-send', '-a', 'GPU INFO', 'GPU Informationen', gpu_info])

if __name__ == "__main__":
    display_gpu_info()

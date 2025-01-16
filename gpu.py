import subprocess

def get_gpu_info():
    try:
        # Führe den Befehl lspci aus und speichere die Ausgabe
        result = subprocess.run(['lspci'], stdout=subprocess.PIPE, text=True)
        
        # Durchsuche die Ausgabe nach der GPU
        for line in result.stdout.splitlines():
            if 'VGA compatible controller' in line or '3D controller' in line:
                return line.strip()
        
        return "Keine GPU gefunden."
    
    except Exception as e:
        return f"Ein Fehler ist aufgetreten: {e}"

if __name__ == "__main__":
    gpu_info = get_gpu_info()
    print(f"Die im PC verbaute GPU ist: {gpu_info}")

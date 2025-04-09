import os
import platform
import subprocess

def play(file_path):
    sistem = platform.system()

    if not os.path.isfile(file_path):
        return  # Hata vermesin, sessizce geç

    try:
        if sistem == "Windows":
            subprocess.Popen(
                ['powershell', '-c', f'(New-Object Media.SoundPlayer "{file_path}").PlaySync()'],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )

        elif sistem == "Linux":
            subprocess.Popen(
                ['mpg123', file_path],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )

        elif sistem == "Darwin":  # macOS
            subprocess.Popen(
                ['afplay', file_path],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
    except:
        pass  # Her şey sessiz, hata da yok

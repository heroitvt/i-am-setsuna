import subprocess
import time
import os

exe = r"d:\Viet Hoa Game\I am Setsuna\SETSUNA.exe"
print(f"Launching {exe}...")
proc = subprocess.Popen([exe], cwd=os.path.dirname(exe))
time.sleep(3)
poll = proc.poll()
print(f"Process poll after 3s: {poll} (None means still running happily)")
if poll is None:
    print("Game process is running successfully!")
    proc.terminate()
    try:
        proc.wait(timeout=2)
    except:
        proc.kill()
else:
    print(f"Game exited early with code {poll}!")

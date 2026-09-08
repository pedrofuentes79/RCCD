import subprocess
import time
import sys

processes = []

def process(duration: int, plot: bool = False):
    args = [sys.executable, "ping_client.py", "--duration", str(duration)]
    if plot: 
        args.append("--plot")
        
    proc = subprocess.Popen(args)
    processes.append(proc)
    return proc

# Solo ploteamos en el primer proceso, el resto estan para saturar la red
process(30, plot=True)

time.sleep(5)

# 10 procesos de 20s cada uno
for i in range(10):
    process(20)

time.sleep(5)

for i in range(5):
    process(5)
    time.sleep(1)

# Esperamos a que terminen todos los subprocesos antes de cerrar el programa
for p in processes:
    p.wait()

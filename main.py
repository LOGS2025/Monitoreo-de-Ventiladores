import libre_windows_monitor
import time
import os
import subprocess

script_dir = os.path.dirname(os.path.abspath(__file__))
bat = os.path.join(script_dir, "balloon.bat")

def main():
    subprocess.run([bat, "Iniciando Programa"])
    print("Initializing")
    monitor = libre_windows_monitor.Monitor()

    monitor.initHardwareMonitor()
    monitor.initialize_openhardwaremonitor()
    subprocess.run([bat, "Inicialización exitosa"])

    for i in range(1):
        for _ in range(60):
            monitor.readTemps()
            time.sleep(1)
        subprocess.run([bat, f"Ronda {i} completada!!!"])
        monitor.createDF(1000)
    subprocess.run([bat, "DF Creado"])

    monitor.closeHardwareMonitor()
    subprocess.run([bat, "Programa finalizado"])
  

if __name__ == "__main__":
    main()

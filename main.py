import libre_windows_monitor
import Arduino
import time
import os
import subprocess

script_dir = os.path.dirname(os.path.abspath(__file__))
bat = os.path.join(script_dir, "balloon.bat")

def main():
    subprocess.run([bat, "Iniciando Programa"])
    print("Initializing")
    monitor = libre_windows_monitor.Monitor()
    switch = Arduino.ArduinoPort()

    monitor.initHardwareMonitor(fans)
    monitor.initialize_openhardwaremonitor()

    subprocess.run([bat, f"Inicialización exitosa con ventiladores en {fans}"])

    for i in range(10):
        fans = bool(input("Enter true or false : "))
        for _ in range(300):
            monitor.readTemps()
            time.sleep(1)
        subprocess.run([bat, f"Ronda {_} completada!!!"])
        monitor.createDF(1000)
        subprocess.run([bat, "DF Creado"])

        monitor.closeHardwareMonitor()
        switch.closePort()
        subprocess.run([bat, "Programa finalizado"])
  

if __name__ == "__main__":
    main()

import libreHardware_windows
import time

def main():
    monitor = libreHardware_windows.Monitor()

    monitor.initHardwareMonitor()

    for i in range(2):    
        for _ in range(600):
            monitor.readTemps()
            time.sleep(10)

        monitor.createCSV()
    
    monitor.closeHardwareMonitor()
   

if __name__ == "__main__":
    main()

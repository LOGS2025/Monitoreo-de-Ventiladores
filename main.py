import libre_windows_monitor
import time

def main():
    monitor = libre_windows_monitor.Monitor()

    monitor.initHardwareMonitor()
    monitor.initialize_openhardwaremonitor()

    for _ in range(300):
        monitor.readTemps()
        time.sleep(1)

    monitor.createCSV()
    
    monitor.closeHardwareMonitor()
   

if __name__ == "__main__":
    main()

import Temperatures
import time

def main():
    monitor = Temperatures.Monitor()

    monitor.initHardwareMonitor()

    for i in range(2):    
        for _ in range(600):
            monitor.readTemps()
            time.sleep(10)

        monitor.createCSV()
    
    monitor.closeHardwareMonitor()
   

if __name__ == "__main__":
    main()

import Temperatures
import time

def main():
    monitor = Temperatures.Monitor()

    monitor.initHardwareMonitor()
    
    for _ in range(60):
        monitor.readTemps()
        time.sleep(1)

    monitor.createDF()
    
    monitor.closeHardwareMonitor()
   

if __name__ == "__main__":
    main()

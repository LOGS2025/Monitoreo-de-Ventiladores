from HardwareMonitor.Hardware import SensorType
from HardwareMonitor.Hardware import IParameter
from HardwareMonitor.Hardware import ISensor
from HardwareMonitor.Hardware import IHardware
from HardwareMonitor.Hardware import IComputer
from HardwareMonitor.Hardware import IVisitor
from HardwareMonitor.Hardware import Computer
import time
import pandas as pd

class UpdateVisitor(IVisitor):
    __namespace__ = "TestHardwareMonitor"  # must be unique among implementations of the IVisitor interface
    def VisitComputer(self, computer: IComputer):
        computer.Traverse(self)

    def VisitHardware(self, hardware: IHardware):
        hardware.Update()
        for subHardware in hardware.SubHardware:
            subHardware.Update()

    def VisitParameter(self, parameter: IParameter): pass

    def VisitSensor(self, sensor: ISensor): pass

class Monitor:
    fan_state : bool
    rows = []

    def initHardwareMonitor(self):
        self.computer = Computer()  # settings can not be passed as constructor argument (following below)
        
        self.computer.IsMotherboardEnabled = True
        self.computer.IsControllerEnabled = True
        self.computer.IsCpuEnabled = True
        self.computer.IsGpuEnabled = True
        self.computer.IsBatteryEnabled = True
        self.computer.IsMemoryEnabled = True
        self.computer.IsNetworkEnabled = True
        self.computer.IsStorageEnabled = True
        self.fan_state = True

        self.computer.Open()

    # There is only one monitor so we store everything here?
        # We want to monitor :

    SENSOR_MAP = {
        "/gpu-nvidia/0/temperature/0" : "gpu_temp",
        "/gpu-nvidia/0/temperature/2" : "gpu_hotspot",
        "/gpu-amd/0/load/0" : "gpu_amd_load",
        #"/gpu-nvidia/0/load/0" : "gpu_nvidia_load",    # Defaults to 0
        "/nvme/1/temperature/0" : "ssd_temp",
        "/nvme/1/load/33" : "ssd_load",
        #"/amdcpu/0/temperature/2" : "cpu_temp",        # Defaults to 0
        "/amdcpu/0/load/1" : "cpu_max_load",
        "/amdcpu/0/load/0" : "cpu_load",
        #"/gpu-nvidia/0/load/5" : "d3d_load",           # Defaults to 0
    }

    def readTemps(self):
        self.computer.Accept(UpdateVisitor())

        row = {
        "timestamp": time.time(),
        "fan_state": self.fan_state,
        }

        for hardware in self.computer.Hardware:
            for sensor in hardware.Sensors:
                if sensor.Value is None:
                    continue

                key = self.SENSOR_MAP.get(str(sensor.Identifier))
                if key:
                    row[key] = sensor.Value

        self.rows.append(row)
        
    def createCSV(self, round):
        # Create a new data frame each time
        df = pd.DataFrame(self.rows)
        df.to_csv(f"thermal_log{round}.csv", index=False)
        # Reset data on rows
        self.rows = ''

    def closeHardwareMonitor(self):
        self.computer.Close()




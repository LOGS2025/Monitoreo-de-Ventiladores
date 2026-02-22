from HardwareMonitor.Hardware import SensorType
from HardwareMonitor.Hardware import IParameter
from HardwareMonitor.Hardware import ISensor
from HardwareMonitor.Hardware import IHardware
from HardwareMonitor.Hardware import IComputer
from HardwareMonitor.Hardware import IVisitor
from HardwareMonitor.Hardware import Computer
import time
import pandas as pd
import os
import clr
from datetime import datetime

# Source - https://github.com/snip3rnick/PyHardwareMonitor
# Retrieved 2026-02-22
# Python Harware Monitor is a thin package layer for LibreHardwareMonitorLib using pythonnet. Libre Hardware Monitor, 
# a fork of Open Hardware Monitor, is free software that can monitor the temperature sensors, fan speeds, voltages, 
# load and clock speeds of your computer. This package is mostly auto generated using the pythonstubs generator tool for .NET libraries. 

# Source - https://openhardwaremonitor.org/downloads/
# Retrieved 2026-02-22
# The free Open Hardware Monitor software runs on Microsoft Windows with the .NET Framework version 4.5 and above. 
# On Linux systems the Open Hardware Monitor requires Mono with WinForms.


dll_path = R"C:\Users\lopez\OneDrive\Desktop\Arduino\ventiladorespyino\OpenHardwareMonitorLib.dll"
clr.AddReference(dll_path)

from OpenHardwareMonitor import Hardware

openhardwaremonitor_hwtypes = {
Hardware.HardwareType.Mainboard: "Mainboard",
Hardware.HardwareType.CPU: "CPU",
Hardware.HardwareType.GpuNvidia: "Nvidia GPU",
Hardware.HardwareType.GpuAti: "ATI GPU",
}

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
    df = pd.DataFrame()
    rows = []
    OpenHardwareHandle = ''

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

        self.computer.Open()

    def initialize_openhardwaremonitor(self):
        self.OpenHardwareHandle = Hardware.Computer()
        self.OpenHardwareHandle.MainboardEnabled = True
        self.OpenHardwareHandle.SuperIOEnabled = True
        self.OpenHardwareHandle.CPUEnabled = True
        self.OpenHardwareHandle.RAMEnabled = True
        self.OpenHardwareHandle.GPUEnabled = True
        self.OpenHardwareHandle.HDDEnabled = True
        self.OpenHardwareHandle.SSDEnabled = True
        self.OpenHardwareHandle.BatteryEnabled = True
        self.OpenHardwareHandle.PsuEnabled = True
        self.OpenHardwareHandle.CoolingDeviceEnabled = True
        self.OpenHardwareHandle.UPSEnabled = True

        self.OpenHardwareHandle.Open()

    # There is only one monitor so we store everything here?
        # We want to monitor :

    SENSOR_MAP = { # Only this ones return something
        "/gpu-nvidia/0/temperature/0" : "gpu_temp",
        "/gpu-nvidia/0/temperature/2" : "gpu_hotspot",
        "/nvme/1/temperature/0" : "ssd_temp",
        "/nvme/1/load/33" : "ssd_load",
        "/amdcpu/0/load/1" : "cpu_max_load",
        "/amdcpu/0/load/0" : "cpu_load",
    }

    openHardware_SENSOR_MAP = {
    "GPU_CLOCK" : {
        "type" : "Clock",
        "hardware" : "NVIDIA NVIDIA GeForce RTX 3050 Ti Laptop GPU",
        "name" : "GPU Core"
        },
    "GPU_CLOCK_AMD" : {
        "type" : "Clock",
        "hardware" : "AMD Radeon Graphics",
        "name" : "GPU Core"
        },
    "GPU_LOAD" : {
        "type" : "Load",
        "hardware" : "NVIDIA NVIDIA GeForce RTX 3050 Ti Laptop GPU",
        "name" : "GPU Core"
        },
    "GPU_POWER" : {
        "type" : "Power",
        "hardware" : "NVIDIA NVIDIA GeForce RTX 3050 Ti Laptop GPU",
        "name" : "GPU Power"
        },
    "CPU_LOAD" : {
        "type" : "Load",
        "hardware" : "AMD Ryzen 7 5800H",
        "name" : "CPU Total"
        },
    "GPU_VOLTAGE": {
        "type" : "Voltage",
        "hardware" : "AMD Radeon Graphics",
        "name" : "GPU Core"
        }
    }
    # If it is from gpu, go to gpu dict and enter the key

    def readTemps(self):
        self.computer.Accept(UpdateVisitor())
        row = {
        "timestamp": time.time(),
        "fan_state": self.fan_state,
        }

        # Libre hardware part
        for hardware in self.computer.Hardware:
            for sensor in hardware.Sensors:
                if sensor.Value is None:
                    continue

                key = self.SENSOR_MAP.get(str(sensor.Identifier))
                if key:
                    row[key] = sensor.Value

        # Open hardware part
        for hardware in self.OpenHardwareHandle.Hardware:
            hardware.Update()
            for sensor in hardware.Sensors:
                    for key, cfg in self.openHardware_SENSOR_MAP.items():
                        if (
                            str(sensor.SensorType) == cfg["type"]
                            and cfg["hardware"] in sensor.Hardware.Name
                            and cfg["name"] in sensor.Name
                        ):
                            row[key] = sensor.Value # Save to df

        self.rows.append(row)

    def createDF(self, number):
        now = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        self.df = pd.DataFrame(self.rows)
        self.df.to_csv(f"thermal_log.{number}.{self.fan_state}.{now}.csv", index=False)

    def closeHardwareMonitor(self):
        self.computer.Close()


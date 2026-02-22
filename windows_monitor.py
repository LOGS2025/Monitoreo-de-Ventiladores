import os
import clr

dll_path = R"C:\Users\lopez\OneDrive\Desktop\Arduino\ventiladorespyino\OpenHardwareMonitorLib.dll"
clr.AddReference(dll_path)

from OpenHardwareMonitor import Hardware

openhardwaremonitor_sensortypes = [
    "Voltage",      # 0
    "Clock",        # 1
    "Temperature",  # 2
    "Load",         # 3
    "Fan",          # 4
    "Flow",         # 5
    "Control",      # 6
    "Level",        # 7
    "Factor",       # 8
    "Power",        # 9
    "Data",         # 10
    "SmallData",    # 11
]

openhardwaremonitor_hwtypes = {
    Hardware.HardwareType.Mainboard: "Mainboard",
    Hardware.HardwareType.SuperIO: "Super I/O",
    Hardware.HardwareType.CPU: "CPU",
    Hardware.HardwareType.RAM: "RAM",
    Hardware.HardwareType.GpuNvidia: "Nvidia GPU",
    Hardware.HardwareType.GpuAti: "ATI GPU",
    Hardware.HardwareType.TBalancer: "T-Balancer",
    Hardware.HardwareType.Heatmaster: "Heatmaster",
    Hardware.HardwareType.HDD: "HDD",
}

def initialize_openhardwaremonitor():
    handle = Hardware.Computer()
    handle.MainboardEnabled = True
    handle.SuperIOEnabled = True
    handle.CPUEnabled = True
    handle.RAMEnabled = True
    handle.GPUEnabled = True
    handle.HDDEnabled = True
    handle.SSDEnabled = True
    handle.BatteryEnabled = True
    handle.PsuEnabled = True
    handle.CoolingDeviceEnabled = True
    handle.UPSEnabled = True

    handle.Open()
    return handle

def fetch_stats(handle):
    for hardware in handle.Hardware:
        hardware.Update()
        print(f"Hardware: {openhardwaremonitor_hwtypes.get(hardware.HardwareType, 'Unknown')} - {hardware.Name}")
        for sensor in hardware.Sensors:
            parse_sensor(sensor)

        for subhardware in hardware.SubHardware:
            subhardware.Update()
            print(f"  SubHardware: {openhardwaremonitor_hwtypes.get(subhardware.HardwareType, 'Unknown')} - {subhardware.Name}")
            for subsensor in subhardware.Sensors:
                parse_sensor(subsensor)

def parse_sensor(sensor):
    if sensor.Value is not None:
        sensor_type = str(sensor.SensorType)
        unit = "\u00B0C" if sensor_type == "Temperature" else ""
        if sensor_type == "Temperature":
            print(
                u"%s %s %s Sensor #%i %s - %.2f%s"
                % (
                    openhardwaremonitor_hwtypes.get(sensor.Hardware.HardwareType, "Unknown"),
                    sensor.Hardware.Name,
                    sensor_type,
                    sensor.Index,
                    sensor.Name,
                    sensor.Value,
                    unit
                )
            )
        else:
            print(
                u"%s %s %s Sensor #%i %s - %.2f"
                % (
                    openhardwaremonitor_hwtypes.get(sensor.Hardware.HardwareType, "Unknown"),
                    sensor.Hardware.Name,
                    sensor_type,
                    sensor.Index,
                    sensor.Name,
                    sensor.Value
                )
            )
    else:
        print(f"Sensor without value: {sensor.Name} of type {openhardwaremonitor_sensortypes[sensor.SensorType]}")

if __name__ == "__main__":
    print("OpenHardwareMonitor:")
    HardwareHandle = initialize_openhardwaremonitor()
    fetch_stats(HardwareHandle)
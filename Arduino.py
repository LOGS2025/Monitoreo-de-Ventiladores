import serial
import time

class ArduinoPort():
    def __init__(self, port = "COM6", baud = 9600):
        self.ser = None
        try:
            self.ser = serial.Serial(port,baud,timeout=1)  # open serial port with inter of 1 second
            print(f"Connected to {self.ser.name}")
        except serial.SerialException as e:
            print("Error during comm_socket startup", e)

    
    def closePort(self):
        if self.ser and self.ser.is_open:
            self.ser.close()             # close port
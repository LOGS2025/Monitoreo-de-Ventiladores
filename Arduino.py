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

    def writeToPort(self, temperature : int) :
        if self.ser and self.ser.is_open :
            msg = f"{temperature}\n"      # convert int → string + newline
            self.ser.write(msg.encode("ascii"))     # write a string
            time.sleep(0.5)
                # Receive confirmation that data was sent correctly
            try:
                response = self.ser.readline().decode("ascii").strip()
                print("Arduino:", response)
            except Exception:
                pass
        else : 
            print("Port was not open")

    def closePort(self):
        if self.ser and self.ser.is_open:
            self.ser.close()             # close port
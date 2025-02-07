import serial
import time
import json
import os
import subprocess


class Arduino:

    def __init__(self, port=None, baudrate=9600):

        # Set the port we will use
        self._port = port

        # Set the baudrate
        self.baudrate = baudrate

        # The serial we will use
        self.ser = None

        # Init serial
        self.init_serial()

    @property
    def port(self):

        if self._port is None:
            self._port = self.find_port()

        return self._port


    def find_port(self):

        # Subprocess run and get the results
        ports = subprocess.check_output("ls /dev/tty*", shell=True).decode("utf-8")

        # Split the rows
        ports = ports.split("\n")

        # Loop through the ports
        for port in ports:

            try:
                # Open Serial Connection
                arduino = serial.Serial(port, self.baudrate, timeout=1)
                time.sleep(2)  # Allow time for connection to establish

                # Read Response
                for _ in range(100):
                    response = arduino.readline()  # .decode("utf-8") # .strip()
                    print("Arduino says:", response)

                # Close Serial Connection
                arduino.close()

                self.port = port

                return port

            except:
                pass


    def init_serial(self):

        if self.ser is None:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=1)
            time.sleep(2)

    def deinit_serial(self):

        if self.ser is not None:
            self.ser.close()

        # Set the serial to None
        self.ser = None


    def send_json(self, data: dict) -> dict:

        # Convert to string
        data_str = (json.dumps(data) + "\n").encode("utf-8")

        # Write the data
        self.ser.write(data_str)

        # Wait for the response
        for _ in range(100):
            response = self.ser.readline()
            # .decode("utf-8").strip()
            print("Arduino says:", response)

            # If the response is not empty
            if response:
                break

        # # Deserialise the response
        # if response is not None:
        #     return json.loads(response)

    def send_cmd(self, cmd, val, port=None) -> dict:

        # The data we want to send
        data = {"cmd": cmd, "val": val}

        return self.send_json(data)


if __name__ == "__main__":

    ard = Arduino("/dev/tty.usbmodem0000011")
    # ard.find_port()

    ard.send_cmd("bob", 9)
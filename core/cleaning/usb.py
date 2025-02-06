import serial
import time
import json


def find_port():
    # TODO: Find the port we need to use
    pass


def send_cmd(port, cmd, val, baudrate=9600):



    # Open Serial Connection
    arduino = serial.Serial(port, baudrate, timeout=1)
    time.sleep(2)  # Allow time for connection to establish

    data = {"cmd": cmd, "val": val}

    # Convert to string
    cmd = json.dumps(data) + "\n"

    # Convert to binary
    cmd = cmd.encode("utf-8")

    print("Sending:", cmd)

    # Send Data
    arduino.write(cmd)

    # # Wait for the command to be processed
    # time.sleep(2)

    print("Waiting for response")

    # Read Response
    for _ in range(100):
        response = arduino.readline() #.decode("utf-8") # .strip()
        print("Arduino says:", response)

    # Close Serial Connection
    arduino.close()


if __name__ == "__main__":

    port = "/dev/tty.usbmodem0000011"

    send_cmd(port, "led", 1)
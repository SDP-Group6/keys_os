import subprocess


def connect_wifi(ssid, password):

    # Whether the connection was successful
    success = False

    # TODO: Connect to wifi using iwconfig
    try:

        # Allow throw of error if the connection fails
        result = subprocess.run(['iwconfig', 'wlan0', 'essid', ssid, 'key', password], check=True)

        # Whether successful connection
        success = result.returncode == 0

        # Check if the connection was successful
        if success:
            print("Successfully connected to wifi")
        else:
            print("Failed to connect to wifi")

    except Exception as e:
        print("Error connecting to wifi:", e)

    return success


import serial
import time

class StateMachine:
    def __init__(self, initial_state: str = "IDLE"):
        # Member to track the device's status
        self.current_state = initial_state
        self.serial_interface = None


    def prepare(self):
        self.open_serial_port('COM3')


    def start(self):
        while(True):
            print("Read data")
            str = "bla bla"
            ret = self.handle_message(str) 
            print(ret)
            time.sleep(2)


    def handle_message(self, msg: str):
        match self.current_state:
            case "IDLE":
                return "Device in Idle state"
            case "PSM":
                return "Device in PSM"
            case "InDr":  
                return "Device in InDr"
            case _:  # The underscore is the 'default' case
                return "Unknown command!"
        

    def open_serial_port(self, port_name: str, baudrate: int = 38400):
        """
        Tries to open a serial port and handles common error cases.
        Returns the serial object if successful, None otherwise.
        """
        try:
            # attempt to open the port
            self.serial_interface = serial.Serial(port_name, baudrate, timeout=1)
            print(f"Successfully opened {port_name} at {baudrate} baud.")
 

        except serial.SerialException as e:
            if "PermissionError" in str(e):
                print(f"Error: Access denied to {port_name}. Try running as admin or closing other apps.")
            elif "FileNotFoundError" in str(e) or "does not exist" in str(e):
                print(f"Error: The port {port_name} was not found. Check your connection.")
            else:
                # This catches 'Port is already open' or 'Resource busy'
                print(f"Error: Could not open {port_name}. It might be in use by another program.")
                print(f"Details: {e}")
                
        except Exception as e:
            print(f"An unexpected error occurred: {e}")



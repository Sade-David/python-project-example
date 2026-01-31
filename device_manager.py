import threading
import time
import yaml
import utilities as utils
from state_machine import SystemController
from state_machine import MsgStruct


class DeviceManager:

    def __init__(self, sm_instance: SystemController, initial_state: str = "NOT_INITIALIZED"):
        # Member to track the device's status
        self.current_state = initial_state
        self.serial_interface = None
        self.sm = sm_instance
        self._thread = None
        self._is_running = False

        # read config file
        config_data = self.read_config_data('device_config.yaml')
        if config_data:
            baud = config_data['device_interface']['baudrate']
            port = config_data['device_interface']['port']
            self.serial_interface = self.open_serial_interface(port, baud)
            self.current_state = "INITIALIZED"
    

    def initialize_device(self):
        print("initialize_device")
        


    def read_config_data(self, file_path: str):
        print("read_config_data")
        try:
            with open(file_path, 'r') as file:
                # yaml.safe_load is the secure way to load YAML data
                data = yaml.safe_load(file)
                return data
        except FileNotFoundError:
            print("Error: The file was not found.")
        except yaml.YAMLError as e:
            print(f"Error parsing YAML: {e}")


    def open_serial_interface(self, port_name: str, baudrate: int = 38400):
        print(f"open_serial_interface {port_name} {baudrate}")
        # secure open serial port 


    def send_message_to_device(self, out_message: str):
        print("send_message_to_device") 
        formatted_msg = utils.hex_string_to_bytes(out_message)   
        # send message
        # later: verify it by ACK from device

    
    def enter_psm(self):
        print("enter_psm")

    def exit_psm(self):    
        print("exit_psm")

    def while_in_psm(self, msg: str):
        print("while_in_psm")
        sm_msg = MsgStruct(time=1.0, trigger="BOOT_DONE", accuracy=0.99)
        self.sm.handle_message(sm_msg)


    def _read_loop(self):
        print("receive_message_from_device")
        """The loop running in the background thread."""
        while self._is_running:
            if self.ser and self.ser.in_waiting > 0:
                try:
                    msg = "asdf"
                    match self.current_state:
                        case "IDLE":
                            return "Device in Idle state"
                        case "PSM":
                            self.while_in_psm(msg)
                            return "Device in PSM"
                        case "InDr":  
                            return "Device in InDr"
                        case _:  # The underscore is the 'default' case
                            return "Unknown command!"
                except Exception as e:
                    print(f"Error parsing serial data: {e}")
            # Prevent 100% CPU usage
                time.sleep(0.01)        
       
    def start(self):
        # 1. Check if already running to prevent double-starting
        if self._is_running:
            print("Reader is already running.")
            return

        # 2. Open the hardware connection
        try:
            # self.ser = serial.Serial(self.port, 9600)
            if self.serial_interface == None:
                print("Serial interface is not opened")
                return
            
            # 3. ALWAYS create a NEW thread object here
            self._is_running = True
            self._thread = threading.Thread(target=self._read_loop, daemon=True)
            self._thread.start()
            print("Thread started.")
        except Exception as e:
            print(f"Start failed: {e}")

    def stop(self):
        self._is_running = False
        if self._thread:
            self._thread.join() # Wait for the thread to actually die
            self._thread = None # Clear the reference
        
        if self.ser:
            self.ser.close()
        print("Thread stopped and cleaned up.")

  
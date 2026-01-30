import utilities as utils
import yaml


class PsmMod:

    def __init__(self, initial_state: str = "NOT_INITIALIZED"):
        # Member to track the device's status
        self.current_state = initial_state
        self.serial_interface = None
        
    

    def initialize_device(self):
        print("initialize_device")   
        config_data = self.read_config_data('device_config.yaml')
        self.serial_interface = self.open_serial_interface('COM3')


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
        print("open_serial_interface")
        # secure open serial port 

    def send_message(out_message: str):
        print("send_message") 
        formatted_msg = utils.hex_string_to_bytes(out_message)   
        # send message
        # later: verify it by ACK from device
    
        
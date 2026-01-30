import serial
import time
import yaml


class StateMachine:
    def __init__(self, initial_state: str = "IDLE"):
        # Member to track the device's status
        self.current_state = initial_state
        self.device_manager = None
        config_data = self.read_config_file('state_machine_config.yaml')


    def read_config_file(self, file_path: str):
        try:
            with open(file_path, 'r') as file:
                # yaml.safe_load is the secure way to load YAML data
                data = yaml.safe_load(file)
                return data
        except FileNotFoundError:
            print("Error: The file was not found.")
        except yaml.YAMLError as e:
            print(f"Error parsing YAML: {e}")
     
       
    #def prepare(self):
    #def start(self):
        

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
        

 
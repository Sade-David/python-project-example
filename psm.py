class PsmMod:

    def __init__(self, initial_state: str = "PSM"):
        # Member to track the device's status
        self.current_state = initial_state
        self.serial_interface = None
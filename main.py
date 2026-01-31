# --- Wiring them together ---
import state_machine
import device_manager
import time






'''
# Create the State Machine first
my_sm = state_machine.SystemController()
my_dm = device_manager.DeviceManager(my_sm)

my_dm.initialize_device()
my_dm.receive_message_from_device()


# Initialize
# 1. Successful Boot (Moving Init -> Normal)
msg1 = state_machine.MsgStruct(time=1.2, trigger="BOOT_DONE", accuracy=0.98)
my_sm.handle_message(msg1)

# 2. Accuracy Drop (Moving Normal -> Monitor)
msg2 = state_machine.MsgStruct(time=5.5, trigger="SENSE", accuracy=0.45)
my_sm.handle_message(msg2)

# 3. Accuracy Recovery (Moving Monitor -> Normal)
msg3 = state_machine.MsgStruct(time=10.0, trigger="SENSE", accuracy=0.92)
my_sm.handle_message(msg3)


try:
    # Main thread stays alive or runs a GUI
    while True:
        time.sleep(1)
        
    except KeyboardInterrupt:
        print("Shutting down...")
        reader.stop()
        # Optionally: brain.stop()

pos1 = (52.5200, 13.4050)
pos2 = (52.5300, 13.4150)

dist = calculate_distance(*pos1, *pos2)
print(f"Distance: {dist:.2f} meters")

'''
import threading
import queue
from dataclasses import dataclass
from statemachine import StateMachine, State

@dataclass
class MsgStruct:
    time: float
    trigger: str
    accuracy: float


class SystemController(StateMachine):
    # States
    init     = State('Init', initial=True)
    normal   = State('Normal')
    psm      = State('Power Save Mode')
    monitor  = State('Monitor')
    shutdown = State('Shutdown')

    # Transitions
    to_normal   = normal.from_(init, psm, monitor)
    to_psm      = psm.from_(normal)
    to_monitor  = monitor.from_(normal, psm)
    to_shutdown = shutdown.from_(init, normal, psm, monitor)

    def __init__(self):
        # 1. Initialize the StateMachine logic
        super().__init__()
        
        # 2. Create a Queue for incoming messages
        self._msg_queue = queue.Queue()
        
        # 3. Create a background thread to process the queue
        self._is_running = True
        self._worker_thread = threading.Thread(target=self._queue_worker, daemon=True)
        self._worker_thread.start()


    def handle_message(self, data: MsgStruct):
        """
        CONTEXT SWITCH: This method is called by the Reader thread.
        It only places the data in the queue and returns immediately.
        """
        print("SM: handle_message")
        self._msg_queue.put(data)

    def _queue_worker(self):
        """
        This runs in the SystemController's own thread.
        It pulls messages and performs the actual state logic.
        """
        while self._is_running:
            try:
                # Wait for a message (blocks for 1 second, then loops to check self._is_running)
                data = self._msg_queue.get(timeout=1.0)
                
                # The REAL handling happens here, in this thread's context
                self._process_logic(data)
                
                # Signal the queue that we are done
                self._msg_queue.task_done()
            except queue.Empty:
                continue

    def _process_logic(self, data: MsgStruct):
        """Actual state transition logic."""
        print("SM: _process_logic")
        handler_name = f"on_message_{self.current_state.id}"
        if hasattr(self, handler_name):
            getattr(self, handler_name)(data)


    def stop(self):
        self._is_running = False
        self._worker_thread.join()


    # --- Logic for INIT ---
    def on_message_init(self, data: MsgStruct):
        if data.trigger == "BOOT_DONE" and data.accuracy > 0.95:
            self.to_normal()

    # --- Logic for NORMAL ---
    def on_message_normal(self, data: MsgStruct):
        # Decision based on multiple fields
        if data.trigger == "LOW_POWER":
            self.to_psm()
        elif data.accuracy < 0.50:
            print("Accuracy too low! Moving to Monitor.")
            self.to_monitor()
        elif data.time > 3600: # 1 hour limit
            self.to_shutdown()

    # --- Logic for PSM ---
    def on_message_psm(self, data: MsgStruct):
        if data.trigger == "CHARGING":
            self.to_normal()
        elif data.time > 500: # PSM timeout
            self.to_shutdown()

    # --- Logic for MONITOR ---
    def on_message_monitor(self, data: MsgStruct):
        if data.accuracy > 0.90:
            self.to_normal()
        elif data.trigger == "USER_OFF":
            self.to_shutdown()

    # Entry/Exit Hooks
    def on_enter_normal(self):
        print("-> Entered Normal Mode")

    def on_exit_normal(self):
        print("<- Leaving Normal Mode")



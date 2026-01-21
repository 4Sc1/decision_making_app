import socket
from PyQt5.QtCore import QObject
from pylsl import StreamInfo, StreamOutlet

class MarkerStreamer(QObject):
    EVENT_FORM_SHOWING = "SHOWING"
    EVENT_FORM_CLOSED = "CLOSED"
    
    def __init__(self):
        super().__init__()
        self.info = StreamInfo('ExperimentApp', 'Markers', 1, 0, 'string', socket.gethostname())
        self.outlet = StreamOutlet(self.info)

    def send_marker(self, marker):
        self.outlet.push_sample([marker])
        
    def send_trial_marker(self, form_name, trial_nr):
        self.send_marker(f"{form_name}_TRIAL_{trial_nr}")
        
    def send_trial_timeout_marker(self, form_name, trial_nr):
        self.send_marker(f"{form_name}_TRIAL_{trial_nr}_TIMEOUT")
        
    def send_button_click_marker(self, form_name, button_name):
        self.send_marker(f"{form_name}_BUTTON_{button_name}")
        
    def send_key_pressed_marker(self, form_name, key_name):
        self.send_marker(f"{form_name}_KEY_{key_name}")
    
    def send_form_event_marker(self, form_name, state):
        self.send_marker(self.create_form_event_marker(form_name, state))
        
    def create_form_event_marker(self, form_name, state):
        return f"{form_name}_{state}"
    
    def stop(self):
        self.outlet.__del__()

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt
from utils.marker_streamer import MarkerStreamer

class FormBase(QWidget):
    
    def __init__(self, name:str, marker_streamer: MarkerStreamer):
        super().__init__()
        self.name = name
        self.marker_streamer = marker_streamer
        self.key_map = {
            Qt.Key_1: '1', Qt.Key_2: '2', Qt.Key_3: '3', Qt.Key_4: '4', Qt.Key_B: 'B', Qt.Key_G: 'G',
            Qt.Key_R: 'R', Qt.Key_Y: 'Y', Qt.Key_Backspace: 'BACKSPACE', Qt.Key_Space: 'SPACE',
            Qt.Key_Up: 'UPARROW', Qt.Key_Down: 'DOWNARROW',
        }
        
    def showEvent(self, event):
        super().showEvent(event)
        self.marker_streamer.send_form_event_marker(self.name, MarkerStreamer.EVENT_FORM_SHOWING)

    def closeEvent(self, event):
        super().closeEvent(event)
        self.marker_streamer.send_form_event_marker(self.name, MarkerStreamer.EVENT_FORM_CLOSED)
        
    def button_clicked(self, button_name):
        self.marker_streamer.send_button_click_marker(self.name, button_name)
        
    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        
        key_name = self.key_map.get(event.key())
        
        if not key_name:
            key_name = "OTHER"
        
        self.marker_streamer.send_key_pressed_marker(self.name, key_name)
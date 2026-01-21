from gui.instructions_form_base import InstructionsFormBase
from utils.marker_streamer import MarkerStreamer

class OuttroForm(InstructionsFormBase):
    def __init__(self, marker_streamer: MarkerStreamer):
        main_label_text = ""
        instructions = [
            "Thank you for participating in our study!\nYou have completed all tasks.\nPlease inform the experimenter that you are done.", 
        ]
        super().__init__(name="outtro", marker_streamer=marker_streamer, main_label_text=main_label_text, instructions=instructions)
from gui.instructions_form_base import InstructionsFormBase
from utils.marker_streamer import MarkerStreamer

class AnotherTrialInstructionsForm(InstructionsFormBase):
    def __init__(self, name:str, marker_streamer: MarkerStreamer, main_label_text:str = ""):
        main_label_text = main_label_text
        instructions = [
            "Well done!\n\nLet's do it again.\n\nAre you ready?"
        ]
        super().__init__(name=name, marker_streamer=marker_streamer, main_label_text=main_label_text, instructions=instructions)
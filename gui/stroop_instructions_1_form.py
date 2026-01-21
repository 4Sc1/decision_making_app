from gui.instructions_form_base import InstructionsFormBase
from utils.marker_streamer import MarkerStreamer

class StroopInstructions1Form(InstructionsFormBase):
    def __init__(self, marker_streamer: MarkerStreamer):
        main_label_text = ""
        instructions = [
            "In the following experiment you will be presented with the names of colors. These color names will be presented in ink.\nThis ink can be the same color as the word, or a different color.",
            "Your task is to indicate the color of the ink, not the word itself.",
            "You will have to press the 'R', 'G', 'B', or 'Y' key according to the color of the ink.",
            "For example, if the word 'GREEN' is presented in red ink, you should press the 'R' key:",
            "If the word 'BLUE' is presented in green ink, you should press the 'G' key:",
            "Here are a few examples to help you understand the task.",
        ]
        super().__init__(name="stroop_inst1", marker_streamer=marker_streamer, main_label_text=main_label_text, instructions=instructions)
from gui.instructions_form_base import InstructionsFormBase
from utils.marker_streamer import MarkerStreamer

class EaaPhase1InitialInstructions1Form(InstructionsFormBase):
    def __init__(self, marker_streamer: MarkerStreamer):
        main_label_text = ""
        instructions = [
            "For this part of the study, you will have to decide if you want to look at an unpleasant picture and hear static noise in exchange for points.", 
            "Before each trial you will see on the screen the probability of the unpleasant picture and noise appearing (0%, 50%, or 100%), and the points you can earn (1 point, 5 points, 10 points).",
        ]
        super().__init__(name="eaa_p1_inst1", marker_streamer=marker_streamer, main_label_text=main_label_text, instructions=instructions)
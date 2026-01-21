from gui.instructions_form_base import InstructionsFormBase
from utils.marker_streamer import MarkerStreamer

class EaaPhase1InitialInstructions3Form(InstructionsFormBase):
    def __init__(self, marker_streamer: MarkerStreamer):
        main_label_text = ""
        instructions = [
            "Now, you will see the unpleasant picture and hear the static noise for you to get familiar with it. ",
        ]
        super().__init__(name="eaa_p1_inst3", marker_streamer=marker_streamer, main_label_text=main_label_text, instructions=instructions)
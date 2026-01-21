from gui.instructions_form_base import InstructionsFormBase
from utils.marker_streamer import MarkerStreamer

class EaaPhase1InitialInstructions4Form(InstructionsFormBase):
    def __init__(self, marker_streamer: MarkerStreamer):
        main_label_text = ""
        instructions = [
            "We will now go through a familiarization phase. Points will not be available in this phase, and you will NOT be able to choose for yourself, you must follow the instructions on the screen.",
        ]
        super().__init__(name="eaa_p1_inst4", marker_streamer=marker_streamer, main_label_text=main_label_text, instructions=instructions)
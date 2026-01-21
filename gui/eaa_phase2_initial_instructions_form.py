from gui.instructions_form_base import InstructionsFormBase
from utils.marker_streamer import MarkerStreamer

class EaaPhase2InitialInstructionsForm(InstructionsFormBase):
    def __init__(self, marker_streamer: MarkerStreamer):
        main_label_text = ""
        instructions = [
            "From now onwards you will see points on the screen, and you can choose for yourself whether to 'accept' or 'reject' a deal in exchange for the points.",
            "You will be offered a total of 54 deals.",
            "During this experiment, please keep your hands on the keyboard at all times to ensure you can respond promptly.\n\nPlease also look at the screen all times unless you are identifying the correct key to press. Do not close your eyes except for natural blinking.",
            "Are you ready?\n\nPlease let the experimenter know.",
        ]
        super().__init__(name="eaa_p2_inst", marker_streamer=marker_streamer, main_label_text=main_label_text, instructions=instructions)
from gui.instructions_form_base import InstructionsFormBase
from utils.marker_streamer import MarkerStreamer

class StroopInstructions3Form(InstructionsFormBase):
    def __init__(self, marker_streamer: MarkerStreamer):
        main_label_text = ""
        instructions = [
            "You will have to press 'R', 'G', 'B', or 'Y' key as quickly as possible, but also as accurately as possible.",
            "During this experiment, please keep your hands on the keyboard at all times to ensure you can respond promptly.\n\nPlease also look at the screen all times unless you are identifying the correct key to press. Do not close your eyes except for natural blinking.",
            "Are you ready?\n\nPlease let the experimenter know.",
        ]
        super().__init__(name="stroop_inst3", marker_streamer=marker_streamer, main_label_text=main_label_text, instructions=instructions)
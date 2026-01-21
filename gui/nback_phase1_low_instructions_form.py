from gui.instructions_form_base import InstructionsFormBase
from utils.marker_streamer import MarkerStreamer

class NBackPhase1LowInstructionsForm(InstructionsFormBase):
    def __init__(self, marker_streamer: MarkerStreamer):
        main_label_text = ""
        instructions = [
            "LOW DIFFICULTY",
            "On the low difficulty level, a displayed letter is a target if it is the same as the letter that was shown immediately prior to it.\n\nIn the sequence 'D F R R T X A' the second 'R' is a target. The other letters are non-targets.",
            "For each letter displayed:\n\nPress the '1' key if the letter is a target.\nPress the '2' key if the letter is a non-target.",
            "We will now do a few trials to practice the low difficulty level.\n\nAre you ready?"
        ]
        super().__init__(name="nback_p1_inst2", marker_streamer=marker_streamer, main_label_text=main_label_text, instructions=instructions)
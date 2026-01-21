from gui.instructions_form_base import InstructionsFormBase
from utils.marker_streamer import MarkerStreamer

class NBackPhase1HighInstructionsForm(InstructionsFormBase):
    def __init__(self, marker_streamer: MarkerStreamer):
        main_label_text = ""
        instructions = [
            "HIGH DIFFICULTY",
            "On the high difficulty level, a displayed letter is a target if it is the same as the letter that was shown three letters prior to it.\n\nIn the sequence 'P X E H A C H' the second 'H' is a target. The other letters are non-targets.",
            "For each letter displayed:\n\nPress the '1' key if the letter is a target.\nPress the '2' key if the letter is a non-target.",
            "We will now do a few trials to practice the high difficulty level.\n\nAre you ready?"
        ]
        super().__init__(name="nback_p1_inst6", marker_streamer=marker_streamer, main_label_text=main_label_text, instructions=instructions)
from gui.instructions_form_base import InstructionsFormBase
from utils.marker_streamer import MarkerStreamer

class NBackPhase1InitialInstructionsForm(InstructionsFormBase):
    def __init__(self, marker_streamer: MarkerStreamer):
        main_label_text = ""
        instructions = [
            "For this part of the study, you will have to decide if you want to do a demanding cognitive task.", 
            "In this task, you will be viewing single letters, each presented one at a time.\n\nYour job is to determine whether the letter displayed on the screen at any given moment is a 'target' or a 'non-target'.",
            "Whether a letter can be considered a 'target' will depend on the task's level of difficulty.",
            "There are three difficulty levels: low, medium, and high.\n\nBefore starting the actual task, there will be explanations and practice sessions for each level to ensure you are familiar with the task requirements.",
        ]
        super().__init__(name="nback_p1_inst1", marker_streamer=marker_streamer, main_label_text=main_label_text, instructions=instructions)
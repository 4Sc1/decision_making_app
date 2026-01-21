from gui.instructions_form_base import InstructionsFormBase
from utils.marker_streamer import MarkerStreamer

class NBackPhase2InitialInstructionsForm(InstructionsFormBase):
    def __init__(self, marker_streamer: MarkerStreamer):
        main_label_text = ""
        instructions = [
            "Now, that you have familiarized yourself with the task, let's move on to the next phase.",
            "In this phase you will have some control over the task.\n\nYou will be able to decide if you want to do a trial of the task or not.",
            "To help you decide, you will be provided with the difficulty level of a following trial symbolized by a speedometer with its needle pointing to either low, medium, or high.",
            "Additionally, the points you can earn for completing a following trial will also be displayed on a second speedometer.\n\nYou will get either 1, 5, or 10 points for completing a trial.",
        ]
        super().__init__(name="nback_p2_inst1", marker_streamer=marker_streamer, main_label_text=main_label_text, instructions=instructions)
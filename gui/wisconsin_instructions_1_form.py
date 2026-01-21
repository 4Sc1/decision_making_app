from gui.instructions_form_base import InstructionsFormBase
from utils.marker_streamer import MarkerStreamer

class WisconsinInstructions1Form(InstructionsFormBase):
    def __init__(self, marker_streamer: MarkerStreamer):
        main_label_text = ""
        instructions = [
            "In this task you will have to match a card presented to you at the bottom of your screen to one of 4 cards presented at the top of the screen.", 
            "Cards can be matched by number of symbols, color of symbols, or the shape of symbols.\n\nUse the keys '1', '2', '3', and '4' to select the card at the top of the screen that matches the card at the bottom of the screen",
            "When you have made a selection, you will receive feedback if your selection was correct.\n\nIf your selection was wrong you will need to try a different rule of classification.",
        ]
        super().__init__(name="wis_inst1", marker_streamer=marker_streamer, main_label_text=main_label_text, instructions=instructions)
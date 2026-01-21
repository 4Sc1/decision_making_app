from gui.instructions_form_base import InstructionsFormBase
from utils.marker_streamer import MarkerStreamer

class EaaPhase1InitialInstructions2Form(InstructionsFormBase):
    def __init__(self, marker_streamer: MarkerStreamer):
        main_label_text = ""
        instructions = [
            "On your keyboard:\n\nPress the 'up arrow' key to accept a deal.\nPress the 'down arrow' key to reject a deal.", 
            "If you accept:\n\nThere will be a probability that you will see the unpleasant picture and hear the unpleasant noise.\nYou will be rewarded the points specified.",
            "If you reject:\n\nYou will NOT see the unpleasant picture and NOT hear the unpleasant noise.\nYou will NOT be rewarded the points specified.",
            "You may only press the 'up arrow' or 'down arrow' key when the following text appears on the screen:\n\n'Press the 'up arrow' key to accept this deal or\npress the 'down arrow' key to reject this deal.'",
            "If you reach a certain amount of points, you can trade them for a special prize.\n\nRegardless of how many deals you accept, you will be granted a €20 voucher upon completing this study.",
        ]
        super().__init__(name="eaa_p1_inst2", marker_streamer=marker_streamer, main_label_text=main_label_text, instructions=instructions)
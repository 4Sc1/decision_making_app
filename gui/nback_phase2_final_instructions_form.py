from gui.instructions_form_base import InstructionsFormBase
from utils.marker_streamer import MarkerStreamer

class NBackPhase2FinalInstructionsForm(InstructionsFormBase):
    def __init__(self, marker_streamer: MarkerStreamer):
        main_label_text = ""
        instructions = [
            "On your keyboard:\n\nPress the 'up arrow' key to accept a trial.\nPress the 'down arrow' key to skip a trial.",
            "If you accept a trial:\n\nYou will have to invest the effort.\nYou will be rewarded the points specified.",
            "If you do not accept a trial:\n\nYou will NOT have to invest the effort.\nYou will NOT be rewarded the points specified.",
            "You may only press the 'up arrow' or 'down arrow' key when the following text appears on the screen:\n\nPress the 'up arrow' key to accept this trial or press the 'down arrow' key to skip this trial.",
            "If you reach a certain amount of points, you can trade them for a special prize.\n\nRegardless of how many trials you accept, you will be granted a €20 voucher upon completing this study.",
            "Be aware: This program can detect the effort you invest during trials.\n\nYou will only be provided with the opportunity to acquire the special prize if you invested continuously high effort during the trials.",
            "The total duration of this experiment depends on how many trials you choose to do.\n\nThe total number of trials available is 54.",
            "During this experiment, please keep your hands on the keyboard at all times to ensure you can respond promptly.\n\nPlease also look at the screen all times unless you are identifying the correct key to press. Do not close your eyes except for natural blinking.",
            "Are you ready?\n\nPlease let the experimenter know.",
        ]
        super().__init__(name="nback_p2_inst2", marker_streamer=marker_streamer, main_label_text=main_label_text, instructions=instructions)
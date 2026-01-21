import random

class EaaPhase1TrialGenerator:
    def __init__(self):
        self.trial_types = [
            (3, True, "3069.jpg"),
            (1, False, "1019.jpg"),
            (2, True, "3000.jpg"),
            (2, False, "3000.jpg"),
            (1, True, "1019.jpg"),
            (3, False, "3069.jpg"),
        ]
        self.trials_per_type = 1

    def generate_trials(self):
        return self.trial_types


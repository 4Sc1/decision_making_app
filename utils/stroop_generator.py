import random

class StroopGenerator:
    def __init__(self, trials_per_type=2):
        self.trial_types = [
            ("RED", "green"),
            ("RED", "blue"),
            ("RED", "yellow"),
            ("GREEN", "red"),
            ("GREEN", "blue"),
            ("GREEN", "yellow"),
            ("BLUE", "red"),
            ("BLUE", "green"),
            ("BLUE", "yellow"),
            ("YELLOW", "red"),
            ("YELLOW", "green"),
            ("YELLOW", "blue"),
            ("RED", "red"),
            ("RED", "red"),
            ("RED", "red"),
            ("GREEN", "green"),
            ("GREEN", "green"),
            ("GREEN", "green"),
            ("BLUE", "blue"),
            ("BLUE", "blue"),
            ("BLUE", "blue"),
            ("YELLOW", "yellow"),
            ("YELLOW", "yellow"),
            ("YELLOW", "yellow")
        ]
        
        self.trials_per_type = trials_per_type

    def generate_trials(self):        
        trials = []
        
        for color_name, ink in self.trial_types:
            for _ in range(self.trials_per_type):
                trials.append((color_name, ink))

        random.shuffle(trials)

        return trials
    
    def generate_instruction_trials(self):
        trials = []
        trials.append(("RED", "green"))
        trials.append(("BLUE", "yellow"))
        trials.append(("YELLOW", "red"))
        trials.append(("GREEN", "blue"))
        trials.append(("RED", "red"))
        trials.append(("BLUE", "blue"))
        trials.append(("YELLOW", "yellow"))
        trials.append(("GREEN", "green"))
        
        random.shuffle(trials)

        return trials


import random

class TrialOrderGenerator:
    def __init__(self, trials_per_type=6):
        self.trial_types = [
            (1, 1),
            (1, 5),
            (1, 10),
            (2, 1),
            (2, 5),
            (2, 10),
            (3, 1),
            (3, 5),
            (3, 10),
        ]
        
        self.trials_per_type = trials_per_type

    def generate_trials(self):
        trials = []
        
        for complexity, points in self.trial_types:
            for _ in range(self.trials_per_type):
                trials.append((complexity, points))

        random.shuffle(trials)

        return trials


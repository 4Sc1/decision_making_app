import random

class WisconsinTrialOrderGenerator:
    def __init__(self):
        self.shapes = ['circle', 'plus', 'triangle', 'star']
        self.colors = ['red', 'green', 'blue', 'yellow']
        self.numbers = [1, 2, 3, 4]
        rules = ['color', 'shape', 'number']
        repeated_rules = [rule for rule in rules for _ in range(10)]
        self.rules_sequence = repeated_rules * 2

    def generate_trial(self, rule):        
        card1 = {
            'color': random.choice(self.colors),
            'shape': random.choice(self.shapes),
            'number': random.choice(self.numbers)
        }

        card2 = {
            'color': card1['color'],
            'shape': random.choice([s for s in self.shapes if s != card1['shape']]),
            'number': random.choice([n for n in self.numbers if n != card1['number']])
        }

        card3 = {
            'color': random.choice([c for c in self.colors if c != card1['color'] and c != card2['color']]),
            'shape': card1['shape'],
            'number': random.choice([n for n in self.numbers if n != card1['number'] and n != card2['number']])
        }

        card4 = {
            'color': random.choice([c for c in self.colors if c not in [card1['color'], card2['color'], card3['color']]]),
            'shape': random.choice([s for s in self.shapes if s not in [card1['shape'], card2['shape'], card3['shape']]]),
            'number': card1['number']
        }

        card5 = {
            'color': [c for c in self.colors if c not in [card1['color'], card2['color'], card3['color'], card4['color']]][0],
            'shape': [s for s in self.shapes if s not in [card1['shape'], card2['shape'], card3['shape'], card4['shape']]][0],
            'number': [n for n in self.numbers if n not in [card1['number'], card2['number'], card3['number'], card4['number']]][0]
        }
        
        references = [card2, card3, card4, card5]
        random.shuffle(references)

        return {
            'to_sort': card1,
            'references': references,
            'rule': rule
        }

    def generate_trials(self):        
        trials = []
        for rule in self.rules_sequence:
            trials.append(self.generate_trial(rule))
        
        return trials

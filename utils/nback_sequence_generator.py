import random

class NBackSequenceGenerator:
    def __init__(self, sequence_length=16, num_targets=4, pos_diff=1):
        if sequence_length < num_targets * (pos_diff + 1) or pos_diff < 1:
            raise ValueError("Invalid sequence length or position difference.")
        self.sequence_length = sequence_length
        self.num_targets = num_targets
        self.pos_diff = pos_diff
        self.letters = [c for c in "ABCDEFGHJKLMNOPQRSTUVWXYZ"]
        self.target_vowels = random.sample(self.letters, self.num_targets)
        self.non_target_consonants = [c for c in self.letters if c not in self.target_vowels]

    def generate_sequence(self):        
        target_vowels = self.target_vowels.copy()
        sequence = [''] * self.sequence_length

        valid_positions = False
        while not valid_positions:
            available_positions = range(self.pos_diff, self.sequence_length)
            target_positions = sorted(random.sample(available_positions, self.num_targets))
            valid_positions = self.validate_target_positions(target_positions)

        for target_position in target_positions:
            target_consonant = target_vowels.pop(0)
            sequence[target_position] = target_consonant
            sequence[target_position - self.pos_diff] = target_consonant

        for i in range(self.sequence_length):
            if sequence[i] == '':
                prev_letter = sequence[i - self.pos_diff] if i >= self.pos_diff else ''
                valid_choices = [c for c in self.non_target_consonants if c != prev_letter]
                sequence[i] = random.choice(valid_choices)

        return ''.join(sequence)

    def validate_target_positions(self, positions):
        for i in range(len(positions) - 1):
            if abs(positions[i] - positions[i + 1]) == self.pos_diff:
                return False
        return True
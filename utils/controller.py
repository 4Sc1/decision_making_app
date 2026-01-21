# for future use

# import json

# class Controller:
#     def __init__(self, main_window, config_path = "experiment.json"):
#         self.main_window = main_window
#         self.load_config(config_path)
#         self.state = "start"
#         self.nback_trial_counts = {
#             'nback': 0,
#             'eaa': 0
#         }

#     def load_config(self, config_path):
#         with open(config_path, 'r', 'utf-8') as file:
#             self.config = json.load(file)
#         self.transitions = self.config['transitions']

#     def set_state(self, new_state):
#         self.state = new_state
#         self.main_window.update_ui(self.state)

#     def transition_next(self):
#         current_transition = self.transitions[self.state]
#         if isinstance(current_transition, dict):
#             if current_transition.get('type') == 'conditional_task':
#                 self.handle_conditional_task(current_transition)
#             elif current_transition.get('type') == 'condition':
#                 self.handle_condition(current_transition)
#         else:
#             self.state = current_transition
#             self.main_window.update_ui(self.state)

#     def handle_conditional_task(self, current_transition):
#         current_task = self.current_task()
        
#         if self.evaluate_condition(current_transition['condition']):
#             next_state = current_transition['conditions'][1]['next']
#             self.update_trial_count(current_task)
#         else:
#             next_state = current_transition['conditions'][0]['next']
#             self.update_trial_count(current_task)
        
#         if self.trial_counts[current_task] >= current_transition['trials']:
#             next_state = current_transition['next']
#             self.reset_trial_count(current_task)
        
#         self.set_state(next_state)

#     def handle_condition(self, current_transition):
#         if self.evaluate_condition(current_transition['condition']):
#             next_state = current_transition['conditions'][1]['next']
#         else:
#             next_state = current_transition['conditions'][0]['next']
#         self.set_state(next_state)

#     def evaluate_condition(self, condition):
#         return getattr(self.main_window, condition, False)

#     def update_trial_count(self, task):
#         if task in self.trial_counts:
#             self.trial_counts[task] += 1

#     def reset_trial_count(self, task):
#         if task in self.trial_counts:
#             self.trial_counts[task] = 0

#     def current_task(self):
#         if 'nback' in self.state:
#             return 'nback'
#         elif 'eaa' in self.state:
#             return 'eaa'
#         return None
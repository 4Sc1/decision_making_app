from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import pyqtSignal, QTimer, Qt
from utils.stroop_generator import StroopGenerator
from utils.marker_streamer import MarkerStreamer
from gui.form_base import FormBase
from datetime import datetime, timezone
import csv
from enum import Enum, auto
import time
import os
import platform

class StroopTaskPresentationMode(Enum):
    EXPERIMENT = auto()
    INSTRUCTION = auto()

class StroopTaskForm(FormBase):
    finished = pyqtSignal()
    
    def __init__(self, name:str, marker_streamer: MarkerStreamer, presentation_mode: StroopTaskPresentationMode, participant_id):
        super().__init__(name=name, marker_streamer=marker_streamer)
        self.presentationMode = presentation_mode
        self.participant_id = participant_id
        self.trials = None
        self.initUI()
        self.results = []
        
    def initUI(self):
        generator = StroopGenerator()
        if self.presentationMode == StroopTaskPresentationMode.EXPERIMENT:
            self.trials = generator.generate_trials()
        else:
            self.trials = generator.generate_instruction_trials()

        self.current_index = -1
        self.response_made = True
        self.trial_start_time = 0

        mainLayout = QVBoxLayout(self)

        if self.presentationMode == StroopTaskPresentationMode.INSTRUCTION:
            self.instructionLabel = QLabel("Press the button corresponding to the color of the ink, not the word.")
            self.instructionLabel.setStyleSheet("font-size: 20pt;")
            self.instructionLabel.setAlignment(Qt.AlignCenter)
            mainLayout.addWidget(self.instructionLabel)
            
        mainLayout.addStretch(1)
        self.targetLabel = QLabel("+")
        self.targetLabel.setAlignment(Qt.AlignCenter)
        self.targetLabel.setStyleSheet("font-size: 48pt; color: black") 
        mainLayout.addWidget(self.targetLabel)
        mainLayout.addStretch(1)

        self.idleTimer = QTimer(self)
        self.idleTimer.timeout.connect(self.next_trial)
        
        self.setFocusPolicy(Qt.StrongFocus)
        self.setFocus()

    def showEvent(self, event):
        self.idleTimer.start(200)
        super().showEvent(event)
        
    def next_trial(self):
        self.idleTimer.stop()
        self.response_made = False
        self.current_index += 1
        
        self.marker_streamer.send_trial_marker(self.name, self.current_index)
        
        self.trial_start_time = time.perf_counter()

        if self.current_index < len(self.trials):
            self.results.append((self.current_index + 1, self.trials[self.current_index][0], self.trials[self.current_index][1], "", "", ""))
            self.targetLabel.setText(self.trials[self.current_index][0])
            self.targetLabel.setStyleSheet("font-size: 48pt; color: {}".format(self.trials[self.current_index][1]))
        else:
            if self.presentationMode == StroopTaskPresentationMode.EXPERIMENT:
                self.save_results()
            else:
                self.finished.emit()

    def keyPressEvent(self, event):
        reaction_time = int(round((time.perf_counter() - self.trial_start_time) * 1000))
        timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        
        super().keyPressEvent(event)
        
        if not self.response_made and not self.idleTimer.isActive():
            if event.key() == Qt.Key_R:
                outcome = 'correct' if self.trials[self.current_index][1] == 'red' else 'incorrect'
            elif event.key() == Qt.Key_G:
                outcome = 'correct' if self.trials[self.current_index][1] == 'green' else 'incorrect'
            elif event.key() == Qt.Key_B:
                outcome = 'correct' if self.trials[self.current_index][1] == 'blue' else 'incorrect'
            elif event.key() == Qt.Key_Y:
                outcome = 'correct' if self.trials[self.current_index][1] == 'yellow' else 'incorrect'
            else:
                return
            
            if self.presentationMode == StroopTaskPresentationMode.INSTRUCTION and outcome == 'incorrect':
                return
        
            self.results[self.current_index] = (self.current_index + 1, self.trials[self.current_index][0], self.trials[self.current_index][1], reaction_time, outcome, timestamp)
            self.response_made = True
            
            self.targetLabel.setText('+')
            self.targetLabel.setStyleSheet("font-size: 48pt; color: black")
            
            self.idleTimer.start(200)

    def save_results(self):
        # Determine the OS
        if platform.system() == 'Windows':
            local_app_data_path = os.environ['LOCALAPPDATA']
        elif platform.system() == 'Darwin':  # Darwin is the system name for macOS
            local_app_data_path = os.path.expanduser('~/Library/Application Support')
        else:
            raise EnvironmentError("Unsupported operating system")

        folder_path = os.path.join(local_app_data_path, "ExperimentResults", "p{}".format(self.participant_id))
        os.makedirs(folder_path, exist_ok=True)
        
        csv_file_path = os.path.join(folder_path, "stroop.csv")

        with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            writer.writerow(['pid', 'utc_ts', 'trial', 'color_word', 'ink', 'rt', 'outcome'])
            
            for (trial_nr, color_word, ink, reaction_time, outcome, timestamp) in self.results:
                writer.writerow([self.participant_id, timestamp, trial_nr, color_word, ink, reaction_time, outcome])

        self.finished.emit()


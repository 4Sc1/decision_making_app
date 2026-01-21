from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import pyqtSignal, QTimer, Qt
from utils.nback_sequence_generator import NBackSequenceGenerator
from datetime import datetime, timezone
from utils.marker_streamer import MarkerStreamer
from gui.form_base import FormBase
import csv
import time
import os
import platform

class NBackTrialForm(FormBase):
    finished = pyqtSignal(int, int)
    
    def __init__(self, name:str, marker_streamer: MarkerStreamer, participant_id, phase, points, n, trial_nr):
        super().__init__(name=name, marker_streamer=marker_streamer)
        self.participant_id = participant_id
        self.phase = phase
        self.points = points
        self.n = n
        self.trial_nr = trial_nr
        self.sequence = None
        self.initUI()
        self.results = []
        
    def initUI(self):
        self.generator = NBackSequenceGenerator(sequence_length=16, num_targets = 4, pos_diff=self.n)
        
        self.sequence = self.generator.generate_sequence()
        self.current_index = -1
        self.response_made = True
        self.letter_start_time = 0

        mainLayout = QVBoxLayout(self)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.setAlignment(Qt.AlignCenter)

        self.targetLabel = QLabel('+')
        self.targetLabel.setAlignment(Qt.AlignCenter)
        self.targetLabel.setStyleSheet("font-size: 48pt; color: black; margin: 0px")
        mainLayout.addWidget(self.targetLabel)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.next_letter)
        
        self.setFocusPolicy(Qt.StrongFocus)
        self.setFocus()

    def showEvent(self, event):
        self.timer.start(2500)
        super().showEvent(event)
        
    def next_letter(self):
        if self.response_made == False:
            reaction_time = int(round((time.perf_counter() - self.letter_start_time) * 1000))
            timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            self.results[self.current_index] = (self.sequence[self.current_index], reaction_time, "timeout", timestamp)
            self.marker_streamer.send_trial_timeout_marker(self.name, self.trial_nr)
        
        self.response_made = False
        self.current_index += 1
        self.letter_start_time = time.perf_counter()

        if self.current_index < len(self.sequence):
            self.results.append((self.sequence[self.current_index], "", ""))
            self.targetLabel.setText(self.sequence[self.current_index])
            QTimer.singleShot(500, lambda: self.targetLabel.setText('+') if self.current_index < len(self.sequence) else None)
        else:
            self.targetLabel.setText('+')
            self.timer.stop()
            self.save_results()

    def keyPressEvent(self, event):
        reaction_time = int(round((time.perf_counter() - self.letter_start_time) * 1000))
        timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        
        super().keyPressEvent(event)
        
        if not self.response_made and self.timer.isActive():
            correct = self.current_index >= self.n and self.sequence[self.current_index] == self.sequence[self.current_index - self.n]
            outcome = None
            if event.key() == Qt.Key_1:
                outcome = 'correct' if correct else 'incorrect'
            elif event.key() == Qt.Key_2:
                outcome = 'incorrect' if correct else 'correct'
            else:
                return
            
            self.results[self.current_index] = (self.sequence[self.current_index], reaction_time, outcome, timestamp)
            self.response_made = True
        
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
        
        csv_file_path = os.path.join(folder_path, "nback.csv")
        
        file_exists = os.path.isfile(csv_file_path)
        
        with open(csv_file_path, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            
            if not file_exists:
                writer.writerow(['pid', 'utc_ts', 'phase', 'trial', 'n', 'points', 'letter', 'rt', 'outcome'])
            
            for (letter, reaction_time, outcome, timestamp) in self.results:
                writer.writerow([self.participant_id, timestamp, self.phase, self.trial_nr, self.n, self.points, letter, reaction_time, outcome])

        self.finished.emit(self.points, self.n)


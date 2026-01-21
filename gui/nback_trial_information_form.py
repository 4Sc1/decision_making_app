from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtSvg import QSvgWidget
from datetime import datetime, timezone
from enum import Enum, auto
from utils.marker_streamer import MarkerStreamer
from utils.path_helper import PathHelper
from gui.form_base import FormBase
import csv
import time
import os
import platform

class NBackTrialInformationPresentationMode(Enum):
    EXPERIMENT = auto()
    INSTRUCTION = auto()

class NBackTrialInformationForm(FormBase):
    finished = pyqtSignal(str)
    
    def __init__(self, name:str, marker_streamer: MarkerStreamer, presentation_mode: NBackTrialInformationPresentationMode, participant_id, main_label_text, phase, points, n, trial_nr, instructions=None, experiment_input_delay=2000):
        super().__init__(name=name, marker_streamer=marker_streamer)
        self.presentationMode = presentation_mode
        self.participant_id = participant_id
        self.main_label_text = main_label_text
        self.phase = phase
        self.points = points
        self.n = n
        self.trial_nr = trial_nr
        self.instructions = instructions
        self.key_pressed = False
        self.experiment_input_delay = experiment_input_delay
        self.experiment_inputs_enabled = False
        self.initUI()

    def initUI(self):
        self.setFocusPolicy(Qt.StrongFocus)

        mainLayout = QVBoxLayout(self)
        mainLayout.setAlignment(Qt.AlignCenter | Qt.AlignTop)
        
        if self.presentationMode != NBackTrialInformationPresentationMode.EXPERIMENT:
            self.mainLabel = QLabel(self.main_label_text)
        else:
            self.mainLabel = QLabel("Trial {}/54".format(self.trial_nr))    

        self.mainLabel.setAlignment(Qt.AlignCenter)
        mainLayout.addWidget(self.mainLabel)
        mainLayout.addStretch(1)
        
        self.trialInformationLayout = QHBoxLayout()
        self.trialInformationLayout.setContentsMargins(0, 0, 0, 0)
        self.trialInformationLayout.addStretch(1)

        difficulty_map = {
            1: 'difficulty_low.svg',
            2: 'difficulty_medium.svg',
            3: 'difficulty_high.svg'
        }

        difficulty_svg = PathHelper.resource_path(os.path.join("assets", difficulty_map.get(self.n, 'difficulty_low.svg')))
        self.difficultyImageWidget = QSvgWidget(difficulty_svg)
        self.difficultyImageWidget.setMinimumSize(333, 333)

        points_map = {
            1: 'points_1.svg',
            5: 'points_5.svg',
            10: 'points_10.svg'
        }

        points_svg = PathHelper.resource_path(os.path.join("assets", points_map.get(self.points, 'points_1.svg')))
        self.pointsImageWidget = QSvgWidget(points_svg)
        self.pointsImageWidget.setMinimumSize(333, 333)
        
        self.trialInformationLayout.addWidget(self.difficultyImageWidget)
        self.trialInformationLayout.addWidget(self.pointsImageWidget)
        self.trialInformationLayout.addStretch(1)

        mainLayout.addLayout(self.trialInformationLayout)

        if self.instructions:
            self.instructionsLabel = QLabel(self.instructions)
            self.instructionsLabel.setWordWrap(True)
            self.instructionsLabel.setFixedWidth(720)
            self.instructionsLabel.setMinimumHeight(100) 
            self.instructionsLabel.setAlignment(Qt.AlignCenter)
            mainLayout.addWidget(self.instructionsLabel, alignment=Qt.AlignCenter)
            
            if self.presentationMode == NBackTrialInformationPresentationMode.EXPERIMENT:
                self.instructionsLabel.setStyleSheet("color: white")

        mainLayout.addStretch(1)

        if self.presentationMode == NBackTrialInformationPresentationMode.INSTRUCTION:
            self.nextScreenButton = QPushButton("Press space bar to continue")
            self.nextScreenButton.setEnabled(False)
            self.key_pressed = True
            self.nextScreenButton.clicked.connect(self.onNextScreen)
            mainLayout.addWidget(self.nextScreenButton, alignment=Qt.AlignCenter)

        self.setFocus()

    def save_results(self, outcome):
        reaction_time = int(round((time.perf_counter() - self.decision_startTime) * 1000))
        timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

        if platform.system() == 'Windows':
            local_app_data_path = os.environ['LOCALAPPDATA']
        elif platform.system() == 'Darwin':
            local_app_data_path = os.path.expanduser('~/Library/Application Support')
        else:
            raise EnvironmentError("Unsupported operating system")

        folder_path = os.path.join(local_app_data_path, "ExperimentResults", "p{}".format(self.participant_id))
        os.makedirs(folder_path, exist_ok=True)
        
        csv_file_path = os.path.join(folder_path, "nback_decisions.csv")
        
        file_exists = os.path.isfile(csv_file_path)
        
        with open(csv_file_path, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            
            if not file_exists:
                writer.writerow(['pid', 'utc_ts', 'phase', 'trial', 'n', 'points', 'rt', 'outcome'])
            
            writer.writerow([self.participant_id, timestamp, self.phase, self.trial_nr, self.n, self.points, reaction_time, outcome])

    def showEvent(self, event):
        self.decision_startTime = time.perf_counter()
        if self.presentationMode == NBackTrialInformationPresentationMode.INSTRUCTION:
            QTimer.singleShot(1000, lambda: self.enableNextScreenButton())
        else:
            QTimer.singleShot(self.experiment_input_delay, self.enableExperimentInputs)
        super().showEvent(event)   
   
    def enableExperimentInputs(self):
        self.experiment_inputs_enabled = True
        self.instructionsLabel.setStyleSheet("color: black")
   
    def enableNextScreenButton(self):
        self.nextScreenButton.setEnabled(True)
        self.key_pressed = False
        
    def showCrossLabelAndEmitResult(self, result):
        if self.presentationMode != NBackTrialInformationPresentationMode.INSTRUCTION:
            self.mainLabel.hide()
            self.remove_all_stretches(layout=self.trialInformationLayout)

            self.pointsImageWidget.hide()
            self.trialInformationLayout.removeWidget(self.pointsImageWidget)
            
            self.difficultyImageWidget.hide()
            self.trialInformationLayout.removeWidget(self.difficultyImageWidget)
            
            if self.instructionsLabel:
                self.instructionsLabel.hide()
                self.trialInformationLayout.removeWidget(self.instructionsLabel)

            self.clearLayout(self.trialInformationLayout)

            self.crossLabel = QLabel('+')
            self.crossLabel.setAlignment(Qt.AlignCenter)
            self.crossLabel.setStyleSheet("font-size: 48pt; color: black; margin: 0px")

            crossLayout = QVBoxLayout(self)
            crossLayout.setContentsMargins(0, 0, 0, 0)
            crossLayout.setAlignment(Qt.AlignCenter)
            crossLayout.addWidget(self.crossLabel)
            
            self.trialInformationLayout.addLayout(crossLayout)

            self.setLayout(crossLayout)  # Apply this layout to ensure it's identical

            # Use QTimer to emit the result after showing the cross for 1 second
            QTimer.singleShot(1000, lambda: self.finished.emit(result))

    def clearLayout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def remove_all_stretches(self, layout):
        items_to_remove = []
        for i in range(layout.count()):
            item = layout.itemAt(i)
            if item.spacerItem() is not None:
                items_to_remove.append(i)

        for i in reversed(items_to_remove):
            layout.takeAt(i)
             
    def onNextScreen(self):
        if self.presentationMode == NBackTrialInformationPresentationMode.INSTRUCTION:
            self.finished.emit('')
        
    def onAcceptTrial(self):
        if self.presentationMode == NBackTrialInformationPresentationMode.EXPERIMENT:
            self.save_results(outcome='accepted')
            self.showCrossLabelAndEmitResult(result='accepted')
        
    def onRejectTrial(self):
        if self.presentationMode == NBackTrialInformationPresentationMode.EXPERIMENT:
            self.save_results(outcome='rejected')
            self.showCrossLabelAndEmitResult(result='rejected')

    def keyPressEvent(self, event: QKeyEvent):
        if not self.key_pressed:
            if self.presentationMode == NBackTrialInformationPresentationMode.INSTRUCTION and event.key() == Qt.Key_Space:
                self.key_pressed = True
                self.nextScreenButton.setEnabled(False)
                self.onNextScreen()
            if self.presentationMode == NBackTrialInformationPresentationMode.EXPERIMENT and self.experiment_inputs_enabled and event.key() == Qt.Key_Up:
                self.key_pressed = True
                self.onAcceptTrial()
            if  self.presentationMode == NBackTrialInformationPresentationMode.EXPERIMENT and self.experiment_inputs_enabled and event.key() == Qt.Key_Down:
                self.key_pressed = True
                self.onRejectTrial()
                
        super().keyPressEvent(event)

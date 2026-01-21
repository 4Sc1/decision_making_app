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

class EaaTrialInformationPresentationMode(Enum):
    EXPERIMENT = auto()
    INSTRUCTION = auto()
    MUST_ACCEPT = auto()
    MUST_REJECT = auto()

class EaaTrialInformationForm(FormBase):
    finished = pyqtSignal(str)
    
    def __init__(self, name: str, marker_streamer: MarkerStreamer, presentation_mode: EaaTrialInformationPresentationMode, participant_id, main_label_text, phase, points, probability_class, trial_nr, instructions=None, experiment_input_delay=2000):
        super().__init__(name=name, marker_streamer=marker_streamer)
        self.presentationMode = presentation_mode
        self.participant_id = participant_id
        self.main_label_text = main_label_text
        self.phase = phase
        self.points = points
        self.probability_class = probability_class
        self.trial_nr = trial_nr
        self.instructions = instructions
        self.key_pressed = False
        self.experiment_input_delay = experiment_input_delay
        self.experiment_inputs_enabled = presentation_mode != EaaTrialInformationPresentationMode.EXPERIMENT
        self.initUI()

    def initUI(self):
        self.setFixedWidth(1150)
        self.setFocusPolicy(Qt.StrongFocus)

        mainLayout = QVBoxLayout(self)
        mainLayout.setAlignment(Qt.AlignCenter | Qt.AlignTop)
        
        if self.presentationMode != EaaTrialInformationPresentationMode.EXPERIMENT:
            self.mainLabel = QLabel(self.main_label_text)
        else:
            self.mainLabel = QLabel("Trial {}/54".format(self.trial_nr))    

        self.mainLabel.setAlignment(Qt.AlignCenter)
        mainLayout.addWidget(self.mainLabel)
        mainLayout.addStretch(1)
        
        self.trialInformationLayout = QHBoxLayout()
        self.trialInformationLayout.addStretch(1)

        probability_map = {
            1: 'probability_0.svg',
            2: 'probability_50.svg',
            3: 'probability_100.svg'
        }
        
        probability_svg = PathHelper.resource_path(os.path.join("assets", probability_map.get(self.probability_class, 'probability_0.svg')))
        self.probabilityImageWidget = QSvgWidget(probability_svg)
        self.probabilityImageWidget.setMinimumSize(333, 333)
        self.trialInformationLayout.addWidget(self.probabilityImageWidget)

        if self.presentationMode == EaaTrialInformationPresentationMode.EXPERIMENT or self.presentationMode == EaaTrialInformationPresentationMode.INSTRUCTION:
        
            points_map = {
                1: 'points_1.svg',
                5: 'points_5.svg',
                10: 'points_10.svg'
            }

            points_svg = PathHelper.resource_path(os.path.join("assets", points_map.get(self.points, 'points_1.svg')))
            self.pointsImageWidget = QSvgWidget(points_svg)
            self.pointsImageWidget.setMinimumSize(333, 333)
            self.trialInformationLayout.addWidget(self.pointsImageWidget)
            
        self.trialInformationLayout.addStretch(1)

        mainLayout.addLayout(self.trialInformationLayout)
        
        if self.presentationMode == EaaTrialInformationPresentationMode.MUST_ACCEPT:
            self.instructions = "This is the deal offered to you.\nPress the 'up arrow' key to accept this deal."
        elif self.presentationMode == EaaTrialInformationPresentationMode.MUST_REJECT:
            self.instructions = "This is the deal offered to you.\nPress the 'down arrow' key to reject this deal."
        elif self.presentationMode == EaaTrialInformationPresentationMode.EXPERIMENT:
            self.instructions = "Press the 'up arrow' key to accept this deal or\npress the 'down arrow' key to reject this deal."
        
        if self.instructions:
            self.instructionsLabel = QLabel(self.instructions)
            self.instructionsLabel.setWordWrap(True)
            self.instructionsLabel.setFixedWidth(720)
            self.instructionsLabel.setAlignment(Qt.AlignCenter)
            mainLayout.addWidget(self.instructionsLabel, alignment=Qt.AlignCenter)
            
            if self.presentationMode == EaaTrialInformationPresentationMode.EXPERIMENT:
                self.instructionsLabel.setStyleSheet("color: white")
             
        mainLayout.addStretch(1)
        
        if self.presentationMode == EaaTrialInformationPresentationMode.INSTRUCTION:
            self.nextScreenButton = QPushButton("Press space bar to continue")
            self.nextScreenButton.clicked.connect(self.onNextScreen)
            self.nextScreenButton.setEnabled(False)
            mainLayout.addWidget(self.nextScreenButton)
            self.key_pressed = True
        
        self.setFocus()
            
    def save_results(self, outcome):
        reaction_time = int(round((time.perf_counter() - self.decision_startTime) * 1000))
        timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        
        prob_map = {
            1: '0.0',
            2: '0.5',
            3: '1.0'
        }
        
        # Determine the OS
        if platform.system() == 'Windows':
            local_app_data_path = os.environ['LOCALAPPDATA']
        elif platform.system() == 'Darwin':  # Darwin is the system name for macOS
            local_app_data_path = os.path.expanduser('~/Library/Application Support')
        else:
            raise EnvironmentError("Unsupported operating system")

        folder_path = os.path.join(local_app_data_path, "ExperimentResults", "p{}".format(self.participant_id))
        os.makedirs(folder_path, exist_ok=True)
        
        csv_file_path = os.path.join(folder_path, "eaa_decisions.csv")
        
        file_exists = os.path.isfile(csv_file_path)
        
        with open(csv_file_path, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            
            if not file_exists:
                writer.writerow(['pid', 'utc_ts', 'phase', 'trial', 'prob', 'points', 'rt', 'outcome'])
            
            writer.writerow([self.participant_id, timestamp, self.phase, self.trial_nr, prob_map.get(self.probability_class), self.points, reaction_time, outcome])
    
    def showCrossLabelAndEmitResult(self, result):
        if self.presentationMode != EaaTrialInformationPresentationMode.INSTRUCTION:
            # Hide and remove all previous widgets from the layout
            self.mainLabel.hide()
            self.remove_all_stretches(layout=self.trialInformationLayout)

            if self.presentationMode == EaaTrialInformationPresentationMode.EXPERIMENT:
                self.pointsImageWidget.hide()
                self.trialInformationLayout.removeWidget(self.pointsImageWidget)

            self.probabilityImageWidget.hide()
            self.trialInformationLayout.removeWidget(self.probabilityImageWidget)
            
            if self.instructionsLabel:
                self.instructionsLabel.hide()
                self.trialInformationLayout.removeWidget(self.instructionsLabel)

            # Clear the current layout before adding the cross
            self.clearLayout(self.trialInformationLayout)

            # Add the cross label, centered, similar to how it's done in the other form
            self.crossLabel = QLabel('+')
            self.crossLabel.setAlignment(Qt.AlignCenter)
            self.crossLabel.setStyleSheet("font-size: 48pt; color: black; margin: 0px")

            crossLayout = QVBoxLayout(self)
            crossLayout.setContentsMargins(0, 0, 0, 0)  # Ensure no margins are set
            crossLayout.setAlignment(Qt.AlignCenter)
            crossLayout.addWidget(self.crossLabel)

            self.trialInformationLayout.addLayout(crossLayout)

            QTimer.singleShot(1000, lambda: self.finished.emit(result))

    def clearLayout(self, layout):
        """ Helper method to clear all widgets from a given layout. """
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
    
    def showEvent(self, event):
        self.decision_startTime = time.perf_counter()
        if self.presentationMode == EaaTrialInformationPresentationMode.INSTRUCTION:
            QTimer.singleShot(1000, lambda: self.enableNextScreenButton())
        else:
            QTimer.singleShot(self.experiment_input_delay, self.enableInputs)
        super().showEvent(event)
    
    def enableNextScreenButton(self):
        self.nextScreenButton.setEnabled(True)
        self.key_pressed = False
        
    def enableInputs(self):
        self.experiment_inputs_enabled = True
        self.instructionsLabel.setStyleSheet("color: black")
    
    def onNextScreen(self):
        if self.presentationMode == EaaTrialInformationPresentationMode.INSTRUCTION:
            self.finished.emit('')
        
    def onAcceptTrial(self):
        if self.presentationMode == EaaTrialInformationPresentationMode.MUST_ACCEPT or self.presentationMode == EaaTrialInformationPresentationMode.EXPERIMENT:
            self.save_results(outcome='accepted')
            self.showCrossLabelAndEmitResult(result='accepted')
        
    def onRejectTrial(self):
        if self.presentationMode == EaaTrialInformationPresentationMode.MUST_REJECT or self.presentationMode == EaaTrialInformationPresentationMode.EXPERIMENT:
            self.save_results(outcome='rejected')
            self.showCrossLabelAndEmitResult(result='rejected')

    def keyPressEvent(self, event: QKeyEvent):
        if not self.key_pressed:
            if self.presentationMode == EaaTrialInformationPresentationMode.INSTRUCTION and event.key() == Qt.Key_Space:
                self.key_pressed = True
                self.nextScreenButton.setEnabled(False)
                self.onNextScreen()
            elif (self.presentationMode == EaaTrialInformationPresentationMode.MUST_ACCEPT or self.presentationMode == EaaTrialInformationPresentationMode.EXPERIMENT) and self.experiment_inputs_enabled and event.key() == Qt.Key_Up:
                self.key_pressed = True
                self.onAcceptTrial()
            elif (self.presentationMode == EaaTrialInformationPresentationMode.MUST_REJECT or self.presentationMode == EaaTrialInformationPresentationMode.EXPERIMENT) and self.experiment_inputs_enabled and event.key() == Qt.Key_Down:
                self.key_pressed = True
                self.onRejectTrial()
                
        super().keyPressEvent(event)

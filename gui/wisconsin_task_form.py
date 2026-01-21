import os
import time
import csv
import platform
from PyQt5.QtWidgets import QPushButton, QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel
from PyQt5.QtCore import pyqtSignal, QTimer, Qt
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtSvg import QSvgWidget
from datetime import datetime, timezone
from enum import Enum, auto
from utils.wisconsin_trial_order_generator import WisconsinTrialOrderGenerator
from utils.marker_streamer import MarkerStreamer
from utils.path_helper import PathHelper
from gui.form_base import FormBase

class WisconsinTaskPresentationMode(Enum):
    EXPERIMENT = auto()
    INSTRUCTION = auto()

class CardWidget(QWidget):
    def __init__(self, label_text):
        super().__init__()
        self.initUI(label_text)
        
    def initUI(self, label_text):
        self.setFixedSize(220, 255)
        self.setStyleSheet("QWidget { border: 2px solid black; }")
        
        frame = QFrame()
        frameLayout = QVBoxLayout(frame)
        frameLayout.setContentsMargins(5, 5, 5, 5)
        
        self.svgWidget = QSvgWidget()
        self.svgWidget.setFixedSize(185, 185)
        self.svgWidget.setStyleSheet("border: 0px solid white;")
        frameLayout.addWidget(self.svgWidget)
        
        layout = QVBoxLayout()
        label = QLabel(label_text)
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        layout.addStretch()
        
        layout.addWidget(frame, 0, Qt.AlignCenter)
        
        self.setLayout(layout)

    def loadSvg(self, svg_path):
        self.svgWidget.load(svg_path)

class WisconsinTaskForm(FormBase):
    finished = pyqtSignal()
    
    def __init__(self, name: str, marker_streamer: MarkerStreamer, presentation_mode: WisconsinTaskPresentationMode, participant_id):
        super().__init__(name=name, marker_streamer=marker_streamer)
        self.presentationMode = presentation_mode
        self.participant_id = participant_id
        self.generator = WisconsinTrialOrderGenerator()
        self.trials = self.generator.generate_trials()
        self.results = []
        self.current_trial_index = 0
        self.allowKeyEvents = False
        self.initUI()

    def initUI(self):
        self.setWindowTitle("")
        self.setFocusPolicy(Qt.StrongFocus)

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter | Qt.AlignTop)

        if self.presentationMode == WisconsinTaskPresentationMode.INSTRUCTION:
            self.mainLabel = QLabel("")
            self.layout.addWidget(self.mainLabel)
            self.layout.addSpacing(20)
            self.instructionsLabel = QLabel()
            self.layout.addWidget(self.instructionsLabel)
            self.layout.addSpacing(20)

        self.referencesLayout = QHBoxLayout()
        self.referenceCardWidgets = []
        for card in range(4):
            cardWidget = CardWidget(label_text=str(card + 1))
            self.referencesLayout.addWidget(cardWidget)
            self.referenceCardWidgets.append(cardWidget)

        self.layout.addLayout(self.referencesLayout)
        self.layout.addStretch(1)
        self.outcomeLabel = QLabel()
        self.outcomeLabel.setAlignment(Qt.AlignCenter)
        self.outcomeLabel.setStyleSheet("font-size: 30pt; color: black") 
        self.layout.addWidget(self.outcomeLabel)                
        self.layout.addStretch(1)

        self.cardToSortWidget = CardWidget(label_text="Card to Sort")
        self.cardToSortWidget.alignment = Qt.AlignCenter
        centeringLayout = QHBoxLayout()
        centeringLayout.addStretch()
        centeringLayout.addWidget(self.cardToSortWidget)
        centeringLayout.addStretch()
        self.layout.addLayout(centeringLayout)
        
        if self.presentationMode == WisconsinTaskPresentationMode.INSTRUCTION:
            self.layout.addSpacing(20)
            self.nextScreenButton = QPushButton("Press space bar to continue")
            self.nextScreenButton.clicked.connect(self.onNextScreen)
            self.layout.addWidget(self.nextScreenButton)
        
        self.setLayout(self.layout)
        
        self.setFocusPolicy(Qt.StrongFocus)
        self.setFocus()

    def showEvent(self, event):
        self.displayCurrentTrial()
        super().showEvent(event)

    def displayCurrentTrial(self):
        for widget in self.referenceCardWidgets:
            widget.show()

        self.cardToSortWidget.show()
        self.outcomeLabel.hide()

        trial = self.trials[self.current_trial_index]
        to_sort = trial['to_sort']
        references = trial['references']

        to_sort_svg_path = PathHelper.resource_path(f'assets/{to_sort["shape"]}_{to_sort["color"]}_{to_sort["number"]}.svg')
        self.cardToSortWidget.loadSvg(to_sort_svg_path)

        for widget, card in zip(self.referenceCardWidgets, references):
            svg_path = PathHelper.resource_path(f'assets/{card["shape"]}_{card["color"]}_{card["number"]}.svg')
            widget.loadSvg(svg_path)
            
        self.trial_start_time = time.perf_counter()
        
        self.allowKeyEvents = True
            
        if self.presentationMode == WisconsinTaskPresentationMode.INSTRUCTION:
            matching_keys = {'shape': None, 'color': None, 'number': None}
            
            for index, reference in enumerate(references, start=1):
                if reference['shape'] == to_sort['shape']:
                    matching_keys['shape'] = str(index)
                if reference['color'] == to_sort['color']:
                    matching_keys['color'] = str(index)
                if reference['number'] == to_sort['number']:
                    matching_keys['number'] = str(index)

            instruction_text = (
                f"For example, if you want to sort the card by shape, press '{matching_keys['shape']}'." +
                f"\n\nIf you want to sort the card by color, press '{matching_keys['color']}'." +
                f"\n\nIf you want to sort the card by number, press '{matching_keys['number']}'.\n\n"
            )
            
            instruction_text = instruction_text.replace("'None'", "'no key'")
            
            self.instructionsLabel.setText(instruction_text)

    def show_outcome(self, outcome):
        for widget in self.referenceCardWidgets:
            widget.hide()
        self.cardToSortWidget.hide()

        self.outcomeLabel.setText(outcome)
        if outcome == 'correct':
            self.outcomeLabel.setStyleSheet("font-size: 30pt; color: green")
        else:
            self.outcomeLabel.setStyleSheet("font-size: 30pt; color: red")
        self.outcomeLabel.show()

        QTimer.singleShot(1000, self.nextTrial)

    def nextTrial(self):
        self.current_trial_index += 1
        if self.current_trial_index >= len(self.trials):
            self.save_results()
        else:
            self.displayCurrentTrial()
        self.marker_streamer.send_trial_marker(self.name, self.current_trial_index)        
        self.allowKeyEvents = True  # Ensure key events are allowed again after the trial is ready.
    
    def onNextScreen(self):
        if self.presentationMode == WisconsinTaskPresentationMode.INSTRUCTION:
            self.finished.emit()
            
    def checkOutcome(self, reference_index):
        if self.presentationMode == WisconsinTaskPresentationMode.INSTRUCTION:
            return
        
        reaction_time = int(round((time.perf_counter() - self.trial_start_time) * 1000))
        timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        
        trial = self.trials[self.current_trial_index]
        reference = trial['references'][reference_index - 1]
        to_sort = trial['to_sort']
        rule = trial['rule']
        
        if rule == 'shape':
            correct = reference['shape'] == to_sort['shape']
            outcome = 'correct' if correct else 'incorrect'
        elif rule == 'color':
            correct = reference['color'] == to_sort['color']
            outcome = 'correct' if correct else 'incorrect'
        elif rule == 'number':
            correct = reference['number'] == to_sort['number']
            outcome = 'correct' if correct else 'incorrect'
        
        self.results.append((self.current_trial_index + 1, rule, to_sort['shape'], to_sort['color'], to_sort['number'], reference['shape'], reference['color'], reference['number'], reaction_time, outcome, timestamp))    
        self.show_outcome(outcome)
   
    def keyPressEvent(self, event: QKeyEvent):
        if not self.allowKeyEvents:
            return
        
        if (event.key() in [Qt.Key_1, Qt.Key_2, Qt.Key_3, Qt.Key_4] and self.presentationMode == WisconsinTaskPresentationMode.EXPERIMENT) or (event.key() == Qt.Key_Space and self.presentationMode == WisconsinTaskPresentationMode.INSTRUCTION):
            self.allowKeyEvents = False
        
            if event.key() == Qt.Key_Space:
                self.onNextScreen()
            elif event.key() == Qt.Key_1:
                self.checkOutcome(1)
            elif event.key() == Qt.Key_2:
                self.checkOutcome(2)
            elif event.key() == Qt.Key_3:
                self.checkOutcome(3)
            elif event.key() == Qt.Key_4:
                self.checkOutcome(4)
        
        super().keyPressEvent(event)
        
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
        
        csv_file_path = os.path.join(folder_path, "wisconsin.csv")

        with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            writer.writerow(['pid', 'utc_ts', 'trial', 'rule', 'shape', 'color', 'number', 'ref_shape', 'ref_color', 'ref_number', 'rt', 'outcome'])
            
            for (trial_nr, rule, shape, color, number, ref_shape, ref_color, ref_number, reaction_time, outcome, timestamp) in self.results:
                writer.writerow([self.participant_id, timestamp, trial_nr, rule, shape, color, number, ref_shape, ref_color, ref_number, reaction_time, outcome])

        self.finished.emit()

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QGridLayout, QGroupBox, QRadioButton, QLabel, QPushButton, QButtonGroup, QScrollArea, QSpacerItem, QSizePolicy)
from PyQt5.QtCore import Qt, pyqtSignal
from datetime import datetime, timezone
from utils.string_sanitizer import StringSanitizer
from utils.marker_streamer import MarkerStreamer
from gui.form_base import FormBase
import csv
import os
import platform

class TaskLoadForm(FormBase):
    finished = pyqtSignal(dict)

    def __init__(self, name:str, marker_streamer: MarkerStreamer, participant_id, n):
        super().__init__(name=name, marker_streamer=marker_streamer)
        self.initUI()
        self.participant_id = participant_id
        self.n = n

    def initUI(self):
        self.setFixedWidth(1150)

        mainLayout = QVBoxLayout(self)
        mainLayout.setAlignment(Qt.AlignCenter| Qt.AlignTop)
        mainLabel = QLabel("")
        mainLabel.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        mainLayout.addWidget(mainLabel)

        mainLayout.addSpacing(20)
        self.setupInstructionsLabel()
        mainLayout.addWidget(self.instructionsLabel)
        
        mainLayout.addSpacing(20)
        self.setupQuestionnaireScrollArea(mainLayout)
        
        self.responses = {question: None for question in self.questions}

        self.submitButton = QPushButton("Submit")
        self.submitButton.setEnabled(False)
        self.submitButton.clicked.connect(self.onSubmit)
        mainLayout.addWidget(self.submitButton)

    def setupInstructionsLabel(self):
        self.instructionsLabel = QLabel("Please rate each of the following six dimensions based on your experience during the task:")
        self.instructionsLabel.setWordWrap(True)
        
    def setupQuestionnaireGroup(self):
        group = QGroupBox()
        group.setStyleSheet("QGroupBox { border: 0; }")
        layout = QVBoxLayout(group)
        self.questionLabelGroups = {}
        self.radioButtonGroups = {}
        
        self.questions = [
            "Mental Demand: How much mental and perceptual activity was required?\nWas the task easy or demanding, simple or complex?",
            "Physical Demand: How much physical activity was required?\nWas the task easy or demanding, slack or strenuous?", 
            "Temporal Demand: How much time pressure did you feel due to the pace\nat which the tasks or task elements occurred?\nWas the pace slow or rapid?",
            "Own Performance: How successful were you in performing the task?\nHow satisfied were you with your performance?",
            "Effort: How hard did you have to work (mentally and physically)\nto accomplish your level of performance?",
            "Frustration Level: How irritated, stressed, and annoyed versus\ncontent, relaxed, and complacent did you feel during the task?"
        ]

        self.responseOptions = list(range(0, 101, 5))

        for question in self.questions:
            questionGroup = QGroupBox()
            questionGroup.setStyleSheet("border: 0;")
            questionLayout = QGridLayout(questionGroup)
            
            questionLabel = QLabel(question)
            self.questionLabelGroups[question] = []
            self.questionLabelGroups[question].append(questionLabel)
            questionLayout.addWidget(questionLabel, 0, 0, 1, -1)

            radioButtonGroup = QButtonGroup(questionGroup)
            self.radioButtonGroups[question] = []
            
            for idx, option in enumerate(self.responseOptions):
                radioButton = QRadioButton()
                radioButtonGroup.addButton(radioButton, option)
                questionLayout.addWidget(radioButton, 1, idx)
                self.radioButtonGroups[question].append(radioButton)
                radioButton.clicked.connect(lambda checked, q=question, o=option: self.updateResponse(q, o))

            firstLabel = QLabel("    Very Low")
            lastLabel = QLabel("Very High")
            if question.startswith("Own Performance"):
                firstLabel.setText("    Perfect")
                lastLabel.setText("Failure")
                
            self.questionLabelGroups[question].append(firstLabel)
            self.questionLabelGroups[question].append(lastLabel)

            questionLayout.addWidget(firstLabel, 2, 0, 1, 3, Qt.AlignLeft)
            questionLayout.addWidget(lastLabel, 2, len(self.responseOptions) -4, 1, 3, Qt.AlignRight)

            layout.addWidget(questionGroup)
            layout.addSpacing(10)
            
        return group

    def setupQuestionnaireScrollArea(self, mainLayout):
        scrollArea = QScrollArea()
        scrollAreaWidgetContents = QWidget()
        scrollAreaLayout = QVBoxLayout(scrollAreaWidgetContents)

        questionnaireGroup = self.setupQuestionnaireGroup()
        scrollAreaLayout.addWidget(questionnaireGroup)
    
        scrollArea.setWidget(scrollAreaWidgetContents)
        scrollArea.setWidgetResizable(True)
        mainLayout.addWidget(scrollArea)

    def updateResponse(self, question, option):
        timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        self.responses[question] = (option, timestamp)
        
        for questionLabel in self.questionLabelGroups[question]:
            questionLabel.setStyleSheet("color: gray")
        
        for radioButton in self.radioButtonGroups[question]:
            radioButton.setStyleSheet("color: gray")
        
        self.checkAllAnswered()

    def checkAllAnswered(self):
        allAnswered = all(response is not None for response in self.responses.values())
        self.submitButton.setEnabled(allAnswered)

    def onSubmit(self):
        # Determine the OS
        if platform.system() == 'Windows':
            local_app_data_path = os.environ['LOCALAPPDATA']
        elif platform.system() == 'Darwin':  # Darwin is the system name for macOS
            local_app_data_path = os.path.expanduser('~/Library/Application Support')
        else:
            raise EnvironmentError("Unsupported operating system")

        folder_path = os.path.join(local_app_data_path, "ExperimentResults", "p{}".format(self.participant_id))
        os.makedirs(folder_path, exist_ok=True)
        
        csv_file_path = os.path.join(folder_path, "qnr_tkld.csv")
        
        file_exists = os.path.isfile(csv_file_path)
        
        with open(csv_file_path, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            
            if not file_exists:
                writer.writerow(['pid', 'utc_ts', 'n', 'question', 'rating'])
            for question, (response, timestamp) in self.responses.items():
                writer.writerow([self.participant_id, timestamp, self.n, StringSanitizer.sanitize(question), response])
        
        self.button_clicked(button_name="submit")
        
        self.finished.emit(self.responses)
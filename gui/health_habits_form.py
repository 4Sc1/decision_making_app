from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QRadioButton, QLabel, QPushButton, QButtonGroup, QScrollArea, QSpacerItem, QSizePolicy)
from PyQt5.QtCore import Qt, pyqtSignal
from datetime import datetime, timezone
from utils.string_sanitizer import StringSanitizer
from utils.marker_streamer import MarkerStreamer
from gui.form_base import FormBase
import csv
import os
import platform

class HealthHabitsForm(FormBase):
    finished = pyqtSignal(dict)

    def __init__(self, marker_streamer: MarkerStreamer, participant_id):
        super().__init__(name="health_hab", marker_streamer=marker_streamer)
        self.participant_id = participant_id
        self.initUI()

    def initUI(self):
        self.setFixedWidth(1150)

        mainLayout = QVBoxLayout(self)
        mainLayout.setAlignment(Qt.AlignCenter | Qt.AlignTop)

        instructionsText = (
            "Please answer the following questions regarding your activities in the <b>previous month</b>."
        )

        instructionsLabel = QLabel(instructionsText)
        instructionsLabel.setWordWrap(True)
        mainLabel = QLabel("")
        mainLabel.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        mainLayout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed))
        mainLayout.addWidget(mainLabel)
        mainLayout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed))
        mainLayout.addWidget(instructionsLabel)
        mainLayout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed))

        self.scrollArea = QScrollArea()
        self.scrollArea.setFixedWidth(1024)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaLayout = QVBoxLayout(self.scrollAreaWidgetContents)

        self.questions = [
            "How often did you smoke cigarettes or used other tobacco products?",
            "How often did you consume alcoholic beverages?",
            "Have you taken cardioactive medication\n(e.g., antidepressant, antipsychotic, antihypertensive)",
            "Have you taken oral contraceptive?",
            "How often did you exercise?"
        ]

        self.responseOptions = {
            0: ["Regularly", "Occasionally", "Never"],
            1: ["Regularly", "Occasionally", "Never"],
            2: ["Yes", "No"],
            3: ["Yes", "No"],
            4: ["Regularly", "Occasionally", "Never"]
        }

        self.responses = {question: None for question in self.questions}

        self.questionnaireGroup = self.setupQuestionnaireGroup(self.questions, self.responseOptions)
        self.scrollAreaLayout.addWidget(self.questionnaireGroup)

        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        mainLayout.addWidget(self.scrollArea)

        self.submitButton = QPushButton("Submit")
        self.submitButton.setEnabled(False)
        self.submitButton.clicked.connect(self.onSubmit)
        mainLayout.addWidget(self.submitButton)

    def setupQuestionnaireGroup(self, questions, optionsDict):
        group = QGroupBox()
        layout = QVBoxLayout()
        self.questionLabels = {}
        self.radioButtonGroups = {}

        for i, question in enumerate(questions):
            questionLayout = QVBoxLayout()
            questionLabel = QLabel(question)
            self.questionLabels[question] = questionLabel
            questionLayout.addWidget(questionLabel)

            buttonGroup = QHBoxLayout()
            radioButtonGroup = QButtonGroup(self)
            self.radioButtonGroups[question] = []
            options = optionsDict[i]
            
            for option in options:
                radioButton = QRadioButton(option)
                radioButtonGroup.addButton(radioButton)
                buttonGroup.addWidget(radioButton)
                self.radioButtonGroups[question].append(radioButton)
                radioButton.clicked.connect(lambda checked, q=question, o=option: self.updateResponse(q, o))

            questionLayout.addLayout(buttonGroup)
            layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed))
            layout.addLayout(questionLayout)
            layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed))

        group.setLayout(layout)
        return group

    def updateResponse(self, question, option):
        timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        self.responses[question] = (option, timestamp)
        self.questionLabels[question].setStyleSheet("color: gray")
        
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

        csv_file_path = os.path.join(folder_path, "qnr_health_habits.csv")

        with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            writer.writerow(['pid', 'utc_ts', 'question', 'response'])
            for question, (response, timestamp) in self.responses.items():
                writer.writerow([self.participant_id, timestamp, StringSanitizer.sanitize(question), StringSanitizer.sanitize(response)])

        self.button_clicked(button_name="submit")

        self.finished.emit(self.responses)
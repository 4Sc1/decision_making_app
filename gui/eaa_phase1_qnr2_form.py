from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QRadioButton, QLabel, QPushButton, QButtonGroup, QSpacerItem, QSizePolicy)
from PyQt5.QtCore import Qt, pyqtSignal
from datetime import datetime, timezone
from utils.string_sanitizer import StringSanitizer
from utils.marker_streamer import MarkerStreamer
from gui.form_base import FormBase
import csv
import os
import platform

class EaaPhase1Qnr2Form(FormBase):
    finished = pyqtSignal(dict)

    def __init__(self, participant_id, marker_streamer: MarkerStreamer):
        super().__init__(name="eaa_p1_qnr2", marker_streamer=marker_streamer)
        self.participant_id = participant_id
        self.initUI()

    def initUI(self):
        mainLayout = QVBoxLayout(self)
        mainLayout.setAlignment(Qt.AlignCenter | Qt.AlignTop)
        
        mainLabel = QLabel("")
        mainLabel.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        mainLayout.addWidget(mainLabel)
        mainLayout.addSpacing(20)
        
        self.setupInstructionsLabel()
        mainLayout.addWidget(self.instructionsLabel)
        mainLayout.addStretch(1)

        questionnaireGroup = self.setupQuestionnaireGroup()
        mainLayout.addWidget(questionnaireGroup)
        mainLayout.addStretch(1)
        
        self.responses = {question: None for question in self.questions}

        self.submitButton = QPushButton("Submit")
        self.submitButton.setEnabled(False)
        self.submitButton.clicked.connect(self.onSubmit)
        mainLayout.addWidget(self.submitButton)

    def setupInstructionsLabel(self):
        self.instructionsLabel = QLabel("Please rate the following question on a scale from 1 to 7, where 1 is very pleasant and 7 is very unpleasant.")

    def setupQuestionnaireGroup(self):
        group = QGroupBox()
        group.setStyleSheet("QGroupBox { border: 0; }")
        layout = QVBoxLayout(group)
        
        self.questions = [
            "How unpleasant was it for you to see the picture and hear the noise?",
        ]
        
        self.responseOptions = [str(i) for i in range(1, 8)]
        
        self.questionLabels = {}
        self.radioButtonGroups = {}
        
        for question in self.questions:
            questionLayout = QVBoxLayout()
            questionLabel = QLabel(question)
            questionLayout.addWidget(questionLabel)
            self.questionLabels[question] = questionLabel

            buttonGroup = QHBoxLayout()
            radioButtonGroup = QButtonGroup(self)
            self.radioButtonGroups[question] = []
            
            for option in self.responseOptions:
                radioButton = QRadioButton(option)
                radioButtonGroup.addButton(radioButton)
                buttonGroup.addWidget(radioButton)
                self.radioButtonGroups[question].append(radioButton)
                radioButton.clicked.connect(lambda checked, q=question, o=option: self.updateResponse(q, o))
            
            questionLayout.addLayout(buttonGroup)
            layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed))
            layout.addLayout(questionLayout)
            layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed))
            
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

        csv_file_path = os.path.join(folder_path, "qnr_eaa.csv")

        file_exists = os.path.isfile(csv_file_path)

        with open(csv_file_path, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')

            if not file_exists:
                writer.writerow(['pid', 'utc_ts', 'question', 'rating'])
            for question, (response, timestamp) in self.responses.items():
                writer.writerow([self.participant_id, timestamp, StringSanitizer.sanitize(question), StringSanitizer.sanitize(response)])

        self.button_clicked(button_name="submit")

        self.finished.emit(self.responses)
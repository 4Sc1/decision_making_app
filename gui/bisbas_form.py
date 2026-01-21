from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QRadioButton, QLabel, QPushButton, QButtonGroup, QScrollArea, QSpacerItem, QSizePolicy)
from PyQt5.QtCore import Qt, pyqtSignal
from datetime import datetime, timezone
from utils.string_sanitizer import StringSanitizer
from utils.marker_streamer import MarkerStreamer
from gui.form_base import FormBase
import csv
import os
import platform

class BISBASForm(FormBase):
    finished = pyqtSignal(dict)

    def __init__(self, marker_streamer: MarkerStreamer, participant_id):
        super().__init__(name="bisbas", marker_streamer=marker_streamer)
        self.participant_id = participant_id
        self.marker_streamer = marker_streamer
        self.initUI()

    def initUI(self):
        self.setFixedWidth(1150)

        mainLayout = QVBoxLayout(self)
        mainLayout.setAlignment(Qt.AlignCenter| Qt.AlignTop)

        instructionsText = (
            "For each item, indicate how much you agree or disagree with what the item says. Please "
            "respond to all the items; do not leave any blank. Please be as accurate and honest as you can be. " 
            "Respond to each item as if it were the only item. That is, don't worry about being \"consistent\" in your responses."
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
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaLayout = QVBoxLayout(self.scrollAreaWidgetContents)

        self.questions = [ 
            "A person's family is the most important thing in life.", 
            "Even if something bad is about to happen to me,\nI rarely experience fear or nervousness.",  
            "I go out of my way to get things I want.", 
            "When I'm doing well at something I love to keep at it.", 
            "I'm always willing to try something new if I think it will be fun.", 
            "How I dress is important to me.", 
            "When I get something I want, I feel excited and energized.", 
            "Criticism or scolding hurts me quite a bit.", 
            "When I want something I usually go all-out to get it.", 
            "I will often do things for no other reason than that they might be fun.", 
            "It's hard for me to find the time to do things such as get a haircut.", 
            "If I see a chance to get something I want I move on it right away.", 
            "I feel pretty worried or upset when I think or know somebody is angry at me.", 
            "When I see an opportunity for something I like I get excited right away.", 
            "I often act on the spur of the moment.", 
            "If I think something unpleasant is going to happen\nI usually get pretty \"worked up\".", 
            "I often wonder why people act the way they do.", 
            "When good things happen to me, it affects me strongly.", 
            "I feel worried when I think I have done poorly at something important.", 
            "I crave excitement and new sensations.", 
            "When I go after something I use a \"no holds barred\" approach.",
            "I have very few fears compared to my friends.", 
            "It would excite me to win a contest.", 
            "I worry about making mistakes."
        ]

        self.responseOptions = [
            "very true for me",
            "somewhat true for me",
            "somewhat false for me",
            "very false for me"
        ]
        
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

    def setupQuestionnaireGroup(self, questions, options):
        group = QGroupBox()
        layout = QVBoxLayout()
        self.questionLabels = {}
        self.radioButtonGroups = {}

        for question in questions:
            questionLayout = QVBoxLayout()
            questionLabel = QLabel(question)
            self.questionLabels[question] = questionLabel
            questionLayout.addWidget(questionLabel)

            buttonGroup = QHBoxLayout()
            radioButtonGroup = QButtonGroup(self)
            self.radioButtonGroups[question] = []
            
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
        
        csv_file_path = os.path.join(folder_path, "qnr_bisbas.csv")
        
        with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            writer.writerow(['pid', 'utc_ts', 'question', 'rating'])
            for question, (response, timestamp) in self.responses.items():
                writer.writerow([self.participant_id, timestamp, StringSanitizer.sanitize(question), StringSanitizer.sanitize(response)])
        
        self.button_clicked(button_name="submit")
        
        self.finished.emit(self.responses)
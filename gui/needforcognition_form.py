from PyQt5.QtWidgets import (QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout, QGroupBox, QRadioButton, QLabel, QPushButton, QButtonGroup, QScrollArea, QSpacerItem, QSizePolicy)
from PyQt5.QtCore import Qt, pyqtSignal
from datetime import datetime, timezone
from utils.string_sanitizer import StringSanitizer
from utils.marker_streamer import MarkerStreamer
from gui.form_base import FormBase
import os
import csv
import platform

class NeedForCognitionForm(FormBase):
    finished = pyqtSignal(dict)

    def __init__(self, marker_streamer: MarkerStreamer, participant_id):
        super().__init__(name="nfc", marker_streamer=marker_streamer)
        self.participant_id = participant_id
        self.initUI()  
        
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
        self.setupScaleTable()
        mainLayout.addWidget(self.scaleTable)
        
        mainLayout.addSpacing(20)
        self.setupQuestionnaireScrollArea(mainLayout)
        
        self.responses = {question: None for question in self.questions}

        self.submitButton = QPushButton("Submit")
        self.submitButton.setEnabled(False)
        self.submitButton.clicked.connect(self.onSubmit)
        mainLayout.addWidget(self.submitButton)

    def setupScaleTable(self):
        self.scaleTable = QTableWidget()
        self.scaleTable.setRowCount(5)  # Five rows to accommodate all options appropriately
        self.scaleTable.setColumnCount(4)  # Two columns for positive and negative scales
        self.scaleTable.horizontalHeader().setVisible(False)
        self.scaleTable.verticalHeader().setVisible(False)
        self.scaleTable.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scaleTable.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scaleTable.setShowGrid(False)
        self.scaleTable.setEditTriggers(QTableWidget.NoEditTriggers)
        self.scaleTable.setSelectionMode(QTableWidget.NoSelection)
        self.scaleTable.setStyleSheet("QTableWidget {background: transparent; border: none;}")

        options = [
            ("+4", "= very strong agreement", " -4", "= very strong disagreement"),
            ("+3","= strong agreement", " -3", "= strong disagreement"),
            ("+2", "= moderate agreement", " -2", "= moderate disagreement"),
            ("+1", "= slight agreement", " -1", "= slight disagreement"),
            ("0", "= neither agreement nor disagreement", None, None)
        ]
        for i, (col0, col1, col2, col3) in enumerate(options):
            self.scaleTable.setItem(i, 0, QTableWidgetItem(col0))
            self.scaleTable.setItem(i, 1, QTableWidgetItem(col1))
            self.scaleTable.setItem(i, 2, QTableWidgetItem(col2))
            self.scaleTable.setItem(i, 3, QTableWidgetItem(col3))
            self.scaleTable.item(i, 0).setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.scaleTable.item(i, 1).setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            self.scaleTable.item(i, 2).setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.scaleTable.item(i, 3).setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self.scaleTable.resizeColumnsToContents()
        self.scaleTable.resizeRowsToContents()

        totalHeight = sum([self.scaleTable.rowHeight(row) for row in range(self.scaleTable.rowCount())])
        totalWidth = sum([self.scaleTable.columnWidth(col) for col in range(self.scaleTable.columnCount())])
        self.scaleTable.setFixedSize(totalWidth + self.scaleTable.verticalHeader().width(), totalHeight + self.scaleTable.horizontalHeader().height())

    def setupInstructionsLabel(self):
        self.instructionsLabel = QLabel("Rate the extent to which you agree with each of the following statements using a 9-point scale with the following values:")
        self.instructionsLabel.setWordWrap(True)
        
    def setupQuestionnaireGroup(self):
        group = QGroupBox()
        layout = QVBoxLayout()
        
        self.questions = [
            "I would prefer complex to simple problems.",
            "I like to have the responsibility of handling a situation\nthat requires a lot of thinking.", 
            "Thinking is not my idea of fun.",
            "I would rather do something that requires little thought than\nsomething that is sure to challenge my thinking abilities.",
            "I try to anticipate and avoid situations where there is likely\na chance I will have to think in depth about something.",
            "I find satisfaction in deliberating hard and for long hours.",
            "I only think as hard as I have to.",
            "I prefer to think about small, daily projects to long-term ones.",
            "I like tasks that require little thought once I've learned them.",
            "The idea of relying on thought to make my way to the top appeals to me.",
            "I really enjoy a task that involves coming up with new solutions to problems.",
            "Learning new ways to think doesn't excite me very much.",
            "I prefer my life to be filled with puzzles that I must solve.",
            "The notion of thinking abstractly is appealing to me.",
            "I would prefer a task that is intellectual, difficult, and important\nto one that is somewhat important but does not require much thought.", 
            "I feel relief rather than satisfaction after completing a task\nthat required a lot of mental effort.",
            "It's enough for me that something gets the job done; I don't care\nhow or why it works.",
            "I usually end up deliberating about issues even when they do not\naffect me personally."
        ]

        self.responseOptions = [
            "+4 ",
            "+3 ",
            "+2 ",
            "+1 ", 
            " 0 ",
            "-1 ",
            "-2 ",
            "-3 ",
            "-4 " 
        ]

        self.questionLabels = {}
        self.radioButtonGroups = {}

        for question in self.questions:
            questionLayout = QVBoxLayout()
            questionLabel = QLabel(question)
            self.questionLabels[question] = questionLabel
            questionLayout.addWidget(questionLabel)

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

        group.setLayout(layout)
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
        
        csv_file_path = os.path.join(folder_path, "qnr_nfc.csv")
        
        with open(csv_file_path, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            writer.writerow(['pid', 'utc_ts', 'question', 'rating'])
            for question, (response, timestamp) in self.responses.items():
                writer.writerow([self.participant_id, timestamp, StringSanitizer.sanitize(question), StringSanitizer.sanitize(response)])
        
        self.button_clicked(button_name="submit")
        
        self.finished.emit(self.responses)
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QSpacerItem, QSizePolicy, QLineEdit, QComboBox, QCheckBox, QPushButton, QFormLayout, QMessageBox)
from PyQt5.QtCore import pyqtSignal
from datetime import datetime, timezone
from utils.marker_streamer import MarkerStreamer
from gui.form_base import FormBase
import csv
import os
import platform

class DemographicsForm(FormBase):
    finished = pyqtSignal(str)

    def __init__(self, marker_streamer: MarkerStreamer):
        super().__init__(name="demo", marker_streamer=marker_streamer)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("")
        self.setFixedWidth(1150)
        
        layout = QVBoxLayout(self)
        
        formLayout = QFormLayout()
        self.idEdit = QLineEdit(self)
        self.idEdit.setPlaceholderText("Enter a positive integer")

        self.ageCombo = QComboBox(self)
        self.ageCombo.addItems([str(age) for age in range(18, 126)])
        self.ageCombo.setCurrentIndex(7)
        
        self.weightCombo = QComboBox(self)
        self.weightCombo.addItems([str(weight) for weight in range(35, 301)])
        self.weightCombo.setCurrentIndex(25)
        
        self.heightCombo = QComboBox(self)
        self.heightCombo.addItems([str(height) for height in range(80, 241)])
        self.heightCombo.setCurrentIndex(80)
        
        self.genderCombo = QComboBox(self)
        self.genderCombo.addItems(["Female", "Male", "Non-Binary"])
        
        self.eyesightCombo = QComboBox(self)
        self.eyesightCombo.addItems(["No", "Yes, not wearing", "Yes, contacts", "Yes, glasses"])
        
        self.handednessCombo = QComboBox(self)
        self.handednessCombo.addItems(["Right", "Left", "Ambidextrous"])
        
        self.languageCheckEnglish = QCheckBox("English", self)
        self.languageCheckGerman = QCheckBox("German", self)
        self.languageCheckFrench = QCheckBox("French", self)
        self.languageCheckLuxembourgish = QCheckBox("Luxembourgish", self)
        self.languageCheckPortuguese = QCheckBox("Portuguese", self)
        self.languageCheckOther = QCheckBox("Other", self)

        formLayout.addRow(QLabel(""))
        formLayout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed))
        formLayout.addRow("Participant ID:", self.idEdit)
        formLayout.addRow("Age:", self.ageCombo)
        formLayout.addRow("Weight (kg):", self.weightCombo)
        formLayout.addRow("Height (cm):", self.heightCombo)
        formLayout.addRow("Eyesight Correction:", self.eyesightCombo)
        formLayout.addRow("Handedness:", self.handednessCombo)
        formLayout.addRow("Gender Identity:", self.genderCombo)
        formLayout.addRow("Languages Spoken:", self.languageCheckEnglish)
        formLayout.addRow("", self.languageCheckGerman)
        formLayout.addRow("", self.languageCheckFrench)
        formLayout.addRow("", self.languageCheckLuxembourgish)
        formLayout.addRow("", self.languageCheckPortuguese)
        formLayout.addRow("", self.languageCheckOther)

        layout.addLayout(formLayout)

        self.submitButton = QPushButton("Submit", self)
        self.submitButton.clicked.connect(self.onSubmit)
        layout.addWidget(self.submitButton)

    def onSubmit(self):
        if not self.idEdit.text().isdigit() or int(self.idEdit.text()) <= 0:
            QMessageBox.warning(self, "Input Error", "Participant ID must be a positive integer.", QMessageBox.Ok, QMessageBox.Ok)
            return
        
        if not self.languageCheckEnglish.isChecked():
            QMessageBox.warning(self, "Input Error", "You need to have sufficient knowledge of the English language to continue.", QMessageBox.Ok, QMessageBox.Ok)
            return
        
        participant_id = self.idEdit.text()
        languages_spoken = [
            lang for lang, chk in [
                ("English", self.languageCheckEnglish.isChecked()),
                ("German", self.languageCheckGerman.isChecked()),
                ("French", self.languageCheckFrench.isChecked()),
                ("Luxembourgish", self.languageCheckLuxembourgish.isChecked()),
                ("Portuguese", self.languageCheckPortuguese.isChecked()),
                ("Other", self.languageCheckOther.isChecked())
            ] if chk
        ]
        
        languages_spoken_str = "/".join(languages_spoken)

        timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

        csv_data = [
            participant_id,
            timestamp,
            self.ageCombo.currentText(),
            self.weightCombo.currentText(),
            self.heightCombo.currentText(),
            self.eyesightCombo.currentText(),
            self.handednessCombo.currentText(),
            self.genderCombo.currentText(),
            languages_spoken_str
        ]

        # Determine the OS
        if platform.system() == 'Windows':
            local_app_data_path = os.environ['LOCALAPPDATA']
        elif platform.system() == 'Darwin':  # Darwin is the system name for macOS
            local_app_data_path = os.path.expanduser('~/Library/Application Support')
        else:
            raise EnvironmentError("Unsupported operating system")

        folder_path = os.path.join(local_app_data_path, "ExperimentResults", "p{}".format(participant_id))
        os.makedirs(folder_path, exist_ok=True)

        csv_file_path = os.path.join(folder_path, "demog.csv")

        with open(csv_file_path, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=';')
  
            writer.writerow(["pid", "utc_ts", "age", "weight", "height", "eyesight_correction", "handedness", "gender_identity", "languages_spoken"])
            writer.writerow(csv_data)
            
        self.button_clicked(button_name="submit")

        self.finished.emit(self.idEdit.text())

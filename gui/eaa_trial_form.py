from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import pyqtSignal, QTimer, Qt, QUrl
from PyQt5.QtGui import QPixmap
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from datetime import datetime, timezone
from utils.marker_streamer import MarkerStreamer
from utils.path_helper import PathHelper
from gui.form_base import FormBase
import csv
import os
import random
import platform

class EaaTrialForm(FormBase):
    finished = pyqtSignal(int, int)
    
    def __init__(self, name:str, marker_streamer: MarkerStreamer, participant_id, phase, points, probability_class, trial_nr, image_file):
        super().__init__(name=name, marker_streamer=marker_streamer)
        self.participant_id = participant_id
        self.phase = phase
        self.points = points
        self.probability_class = probability_class
        self.trial_nr = trial_nr
        self.image_file = image_file
        self.player = QMediaPlayer()
        self.initSound()
        self.initUI()
        
    def initUI(self):
        self.setFixedWidth(1150)
        self.pathToImage = PathHelper.resource_path(os.path.join("iaps", self.image_file))
        if self.probability_class == 1:
            self.unpleasant_experience = False
        elif self.probability_class == 2:
            self.unpleasant_experience = random.choice([True, False])
        else:
            self.unpleasant_experience = True  

        mainLayout = QVBoxLayout(self)
        
        if self.unpleasant_experience:
            self.targetLabel = QLabel()
            self.targetLabel.setAlignment(Qt.AlignCenter)
            mainLayout.addWidget(self.targetLabel)
            self.targetLabel.setPixmap(QPixmap(self.pathToImage))
            self.targetLabel.setScaledContents(True)
        else:
            mainLayout.setContentsMargins(0, 0, 0, 0)
            mainLayout.setAlignment(Qt.AlignCenter) 
            self.targetLabel = QLabel('+')  # Same label as in the first form
            self.targetLabel.setAlignment(Qt.AlignCenter)
            self.targetLabel.setStyleSheet("font-size: 48pt; color: black; margin: 0px") 
            mainLayout.addWidget(self.targetLabel)
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.save_results)
        
        self.setFocusPolicy(Qt.StrongFocus)
        self.setFocus()

    def initSound(self):
        soundFilePath = PathHelper.resource_path(os.path.join("iaps", "tv.wav"))
        url = QUrl.fromLocalFile(soundFilePath)
        content = QMediaContent(url)
        self.player.setMedia(content)
        self.player.setVolume(100)

    def showEvent(self, event):
        if self.unpleasant_experience:
            self.player.play()
        self.timer.start(1000)
        super().showEvent(event)
        
    def save_results(self):
        self.timer.stop()
        self.player.stop()
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
        
        csv_file_path = os.path.join(folder_path, "eaa.csv")
        file_exists = os.path.isfile(csv_file_path)
        
        with open(csv_file_path, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            if not file_exists:
                writer.writerow(['pid', 'utc_ts', 'phase', 'trial', 'prob', 'points', 'img'])
            writer.writerow([self.participant_id, timestamp, self.phase, self.trial_nr, prob_map.get(self.probability_class), self.points, self.image_file])
        self.finished.emit(self.points, self.probability_class)

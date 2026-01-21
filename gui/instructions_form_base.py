from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtGui import QKeyEvent
from gui.form_base import FormBase
from utils.marker_streamer import MarkerStreamer

class InstructionsFormBase(FormBase):
    finished = pyqtSignal(dict)
    
    def __init__(self, name: str, marker_streamer: MarkerStreamer, main_label_text, instructions):
        super().__init__(name=name, marker_streamer=marker_streamer)
        self._instructions = instructions
        self.current_index = 0
        self.initUI(main_label_text)
        
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.enableNavigation)

    def initUI(self, mainLabelText):
        self.setFixedWidth(1150)

        mainLayout = QVBoxLayout(self)
        mainLayout.setAlignment(Qt.AlignCenter | Qt.AlignTop)
        mainLabel = QLabel(mainLabelText)
        mainLabel.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        mainLayout.addWidget(mainLabel)
        mainLayout.addStretch(1)

        instructionsLayout = QHBoxLayout()
        instructionsLayout.addStretch()

        self.instructionsLabel = QLabel(self._instructions[self.current_index])
        self.instructionsLabel.setWordWrap(True)
        self.instructionsLabel.setFixedWidth(720)
        self.instructionsLabel.setAlignment(Qt.AlignCenter)
        self.instructionsLabel.setStyleSheet("font-size: 20pt;")
        
        instructionsLayout.addWidget(self.instructionsLabel)
        instructionsLayout.addStretch()

        mainLayout.addLayout(instructionsLayout)
        mainLayout.addStretch(1)

        buttonsLayout = QHBoxLayout()
        self.previousInstructionButton = QPushButton("Press backspace to go back")
        self.previousInstructionButton.setEnabled(False)
        self.previousInstructionButton.clicked.connect(self.onPreviousInstruction)
        self.nextInstructionButton = QPushButton("Press space bar to continue")
        self.nextInstructionButton.setEnabled(False)
        self.nextInstructionButton.clicked.connect(self.onNextInstruction)
        buttonsLayout.addStretch()
        buttonsLayout.addWidget(self.previousInstructionButton)
        buttonsLayout.addSpacing(140)
        buttonsLayout.addWidget(self.nextInstructionButton)
        buttonsLayout.addStretch()

        mainLayout.addLayout(buttonsLayout)

        self.setFocusPolicy(Qt.StrongFocus)
        self.setFocus()

    def showEvent(self, event):
        super().showEvent(event)
        self.setFocus()
        self.timer.start(2000)

    def enableNavigation(self):
        self.previousInstructionButton.setEnabled(self.current_index > 0)
        self.nextInstructionButton.setEnabled(True)

    def onNextInstruction(self):
        self.timer.stop()
        self.nextInstructionButton.setEnabled(False)
        self.previousInstructionButton.setEnabled(False)
        
        if self.current_index < len(self._instructions) - 1:
            self.current_index += 1
            self.instructionsLabel.setText(self._instructions[self.current_index])
            self.timer.start(2000)
        else:
            self.finished.emit({})

    def onPreviousInstruction(self):
        self.timer.stop()

        if self.current_index > 0:
            self.current_index -= 1
            self.instructionsLabel.setText(self._instructions[self.current_index])
            self.nextInstructionButton.setEnabled(False)
            self.previousInstructionButton.setEnabled(False)
            self.timer.start(2000)
            
    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Space and self.nextInstructionButton.isEnabled():
            self.onNextInstruction()
        elif event.key() == Qt.Key_Backspace and self.previousInstructionButton.isEnabled():
            self.onPreviousInstruction()
        
        super().keyPressEvent(event)

    @property
    def instructions(self):
        return self._instructions

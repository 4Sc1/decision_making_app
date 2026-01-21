import random
import json
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QStackedWidget, QHBoxLayout, QSpacerItem, QSizePolicy, QApplication
from PyQt5.QtCore import QThread, QEvent, Qt, pyqtSlot
from PyQt5.QtGui import QKeyEvent
from gui.another_trial_instructions_form import AnotherTrialInstructionsForm
from gui.demographics_form import DemographicsForm
from gui.health_habits_form import HealthHabitsForm
from gui.recent_activity_form import RecentActivityForm
from gui.bisbas_form import BISBASForm
from gui.needforcognition_form import NeedForCognitionForm
from gui.nback_phase1_initial_instructions_form import NBackPhase1InitialInstructionsForm
from gui.nback_phase1_low_instructions_form import NBackPhase1LowInstructionsForm
from gui.nback_phase1_medium_instructions_form import NBackPhase1MediumInstructionsForm
from gui.nback_phase1_high_instructions_form import NBackPhase1HighInstructionsForm
from gui.nback_trial_form import NBackTrialForm
from gui.task_load_form import TaskLoadForm
from gui.nback_phase2_initial_instructions_form import NBackPhase2InitialInstructionsForm
from gui.nback_trial_information_form import NBackTrialInformationForm, NBackTrialInformationPresentationMode
from gui.nback_phase2_final_instructions_form import NBackPhase2FinalInstructionsForm
from gui.eaa_phase1_initial_instructions_1_form import EaaPhase1InitialInstructions1Form
from gui.eaa_phase1_initial_instructions_2_form import EaaPhase1InitialInstructions2Form
from gui.eaa_phase1_initial_instructions_3_form import EaaPhase1InitialInstructions3Form
from gui.eaa_phase1_initial_instructions_4_form import EaaPhase1InitialInstructions4Form
from gui.eaa_phase1_qnr1_form import EaaPhase1Qnr1Form
from gui.eaa_phase1_qnr2_form import EaaPhase1Qnr2Form
from gui.eaa_trial_information_form import EaaTrialInformationForm, EaaTrialInformationPresentationMode
from gui.eaa_trial_form import EaaTrialForm
from gui.eaa_phase2_initial_instructions_form import EaaPhase2InitialInstructionsForm
from gui.stroop_instructions_1_form import StroopInstructions1Form
from gui.stroop_instructions_3_form import StroopInstructions3Form
from gui.stroop_task_form import StroopTaskForm, StroopTaskPresentationMode
from gui.wisconsin_instructions_1_form import WisconsinInstructions1Form
from gui.wisconsin_instructions_3_form import WisconsinInstructions3Form
from gui.wisconsin_task_form import WisconsinTaskForm, WisconsinTaskPresentationMode
from gui.outtro_form import OuttroForm
from utils.trial_order_generator import TrialOrderGenerator
from utils.eaa_phase1_trial_generator import EaaPhase1TrialGenerator
from utils.eaa_image_provider import EaaImageProvider
from utils.marker_streamer import MarkerStreamer

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.load_config("settings.json")
        self.nbackPhase2TrialInformationForms = []
        self.nbackPhase2TrialForms = []
        self.nbackPhase2_accepted_trials = []
        self.eaaPhase1TrialInformationForms = []
        self.eaaPhase1TrialForms = []
        self.eaaPhase2TrialInformationForms = []
        self.eaaPhase2TrialForms = []
        self.participant_id = None
        self.init_lsl()
        self.initUI()

    def load_config(self, config_path):
        with open(file=config_path, mode='r', encoding='utf-8') as file:
            self.config = json.load(file)
            self.mode = self.config['mode']
            self.shortcut = self.config['shortcut']
            self.nbackb4eaa = self.config['nbackb4eaa']
            
    def init_lsl(self):
        self.marker_streamer = MarkerStreamer()
        self.marker_thread = QThread()
        self.marker_streamer.moveToThread(self.marker_thread)
        self.marker_thread.start()
    
    def initUI(self):
        self.setWindowTitle("ExperimentApp")

        self.setWindowState(Qt.WindowFullScreen)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        self.layout = QVBoxLayout(self.centralWidget)

        hLayout = QHBoxLayout()
        leftSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        rightSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        hLayout.addItem(leftSpacer)
        self.stack = QStackedWidget(self)
        hLayout.addWidget(self.stack)
        hLayout.addItem(rightSpacer)

        self.layout.addLayout(hLayout)
        self.demographicsForm = DemographicsForm(marker_streamer=self.marker_streamer)
        self.stack.addWidget(self.demographicsForm)
        self.demographicsForm.finished.connect(self.onDemographicsFinished)
    
    def initChildForms(self):
        self.healthHabitsForm = HealthHabitsForm(participant_id=self.participant_id, marker_streamer=self.marker_streamer)
        self.recentActivityForm = RecentActivityForm(participant_id=self.participant_id, marker_streamer=self.marker_streamer)
        self.bisbasForm = BISBASForm(participant_id=self.participant_id, marker_streamer=self.marker_streamer)
        self.needforcognitionForm = NeedForCognitionForm(participant_id=self.participant_id, marker_streamer=self.marker_streamer)
        self.stroopInstructions1Form = StroopInstructions1Form(marker_streamer=self.marker_streamer)
        self.stroopInstructions2Form = StroopTaskForm(name="stroop_inst2", presentation_mode=StroopTaskPresentationMode.INSTRUCTION, participant_id=self.participant_id, marker_streamer=self.marker_streamer)
        self.stroopInstructions3Form = StroopInstructions3Form(marker_streamer=self.marker_streamer)
        self.stroopTaskForm = StroopTaskForm(name="stroop_task", presentation_mode=StroopTaskPresentationMode.EXPERIMENT, participant_id=self.participant_id, marker_streamer=self.marker_streamer)
        self.wisconsinInstructions1Form = WisconsinInstructions1Form(marker_streamer=self.marker_streamer)
        self.wisconsinInstructions2Form = WisconsinTaskForm("wis_inst2", presentation_mode=WisconsinTaskPresentationMode.INSTRUCTION, participant_id=self.participant_id, marker_streamer=self.marker_streamer)
        self.wisconsinInstructions3Form = WisconsinInstructions3Form(marker_streamer=self.marker_streamer)
        self.wisconsinTaskForm = WisconsinTaskForm(name="wis_task", presentation_mode=WisconsinTaskPresentationMode.EXPERIMENT, participant_id=self.participant_id, marker_streamer=self.marker_streamer)
        self.nbackPhase1InitialInstructionsForm = NBackPhase1InitialInstructionsForm(marker_streamer=self.marker_streamer)
        self.nbackPhase1LowInstructionsForm = NBackPhase1LowInstructionsForm(marker_streamer=self.marker_streamer)
        self.nbackPhase1LowTestForm1 = NBackTrialForm(name="nback_p1_test1", participant_id=self.participant_id, marker_streamer=self.marker_streamer, phase=1, points=0, n=1, trial_nr=1)
        self.nbackPhase1LowTest2InstructionsForm = AnotherTrialInstructionsForm(name="nback_p1_inst3", marker_streamer=self.marker_streamer)
        self.nbackPhase1LowTestForm2 = NBackTrialForm(name="nback_p1_test2", participant_id=self.participant_id, marker_streamer=self.marker_streamer, phase=1, points=0, n=1, trial_nr=2)
        self.nbackPhase1LowTaskLoadForm = TaskLoadForm(name="nback_p1_tl1",participant_id=self.participant_id, marker_streamer=self.marker_streamer, n=1)
        self.nbackPhase1MediumInstructionsForm = NBackPhase1MediumInstructionsForm(marker_streamer=self.marker_streamer)
        self.nbackPhase1MediumTestForm1 = NBackTrialForm(name="nback_p1_test3",participant_id=self.participant_id, marker_streamer=self.marker_streamer, phase=1, points=0, n=2, trial_nr=3)
        self.nbackPhase1MediumTest2InstructionsForm = AnotherTrialInstructionsForm(name="nback_p1_inst5", marker_streamer=self.marker_streamer)
        self.nbackPhase1MediumTestForm2 = NBackTrialForm(name="nback_p1_test4", participant_id=self.participant_id, marker_streamer=self.marker_streamer, phase=1, points=0, n=2, trial_nr=4)
        self.nbackPhase1MediumTaskLoadForm = TaskLoadForm(name="nback_p1_tl2", participant_id=self.participant_id, marker_streamer=self.marker_streamer, n=2)
        self.nbackPhase1HighInstructionsForm = NBackPhase1HighInstructionsForm(marker_streamer=self.marker_streamer)
        self.nbackPhase1HighTestForm1 = NBackTrialForm(name="nback_p1_test5",participant_id=self.participant_id, marker_streamer=self.marker_streamer, phase=1, points=0, n=3, trial_nr=5)
        self.nbackPhase1HighTest2InstructionsForm = AnotherTrialInstructionsForm(name="nback_p1_inst7", marker_streamer=self.marker_streamer)
        self.nbackPhase1HighTestForm2 = NBackTrialForm(name="nback_p1_test6",participant_id=self.participant_id, marker_streamer=self.marker_streamer, phase=1, points=0, n=3, trial_nr=6)
        self.nbackPhase1HighTaskLoadForm = TaskLoadForm("nback_p1_tl3", participant_id=self.participant_id, marker_streamer=self.marker_streamer, n=3)
        self.nbackPhase2InitialInstructionsForm = NBackPhase2InitialInstructionsForm(marker_streamer=self.marker_streamer)
        self.nbackPhase2TrialInformationExample1Form = NBackTrialInformationForm(name="nback_p2_trial_ex1", presentation_mode=NBackTrialInformationPresentationMode.INSTRUCTION, participant_id=self.participant_id, marker_streamer=self.marker_streamer, main_label_text="", phase=2, points=10, n=1, trial_nr=1, instructions="This is an example of what you will see on the screen.")
        self.nbackPhase2TrialInformationExample2Form = NBackTrialInformationForm(name="nback_p2_trial_ex2", presentation_mode=NBackTrialInformationPresentationMode.INSTRUCTION, participant_id=self.participant_id, marker_streamer=self.marker_streamer, main_label_text="", phase=2, points=1, n=2, trial_nr=2, instructions="This is another example of what you will see on the screen.")
        self.nbackPhase2TrialInformationExample3Form = NBackTrialInformationForm(name="nback_p2_trial_ex3", presentation_mode=NBackTrialInformationPresentationMode.INSTRUCTION, participant_id=self.participant_id, marker_streamer=self.marker_streamer, main_label_text="", phase=2, points=5, n=3, trial_nr=3, instructions="This is another example of what you will see on the screen.")
        self.nbackPhase2FinalInstructionsForm = NBackPhase2FinalInstructionsForm(marker_streamer=self.marker_streamer)
        self.eaaPhase1InitialInstructions1Form = EaaPhase1InitialInstructions1Form(marker_streamer=self.marker_streamer)
        self.eaaPhase1InitialInstructions2Form = EaaPhase1InitialInstructions2Form(marker_streamer=self.marker_streamer)
        self.eaaPhase1InitialInstructions3Form = EaaPhase1InitialInstructions3Form(marker_streamer=self.marker_streamer)
        self.eaaPhase1InitialInstructions4Form = EaaPhase1InitialInstructions4Form(marker_streamer=self.marker_streamer)
        self.eaaPhase1Percentage0Form = EaaTrialInformationForm(name="eaa_p1_prob1", presentation_mode=EaaTrialInformationPresentationMode.INSTRUCTION, participant_id=self.participant_id, marker_streamer=self.marker_streamer, main_label_text="", phase=1, points=10, probability_class=1, trial_nr=1, instructions="This is an example.")
        self.eaaPhase1Percentage50Form = EaaTrialInformationForm(name="eaa_p1_prob2", presentation_mode=EaaTrialInformationPresentationMode.INSTRUCTION, participant_id=self.participant_id, marker_streamer=self.marker_streamer, main_label_text="", phase=1, points=0, probability_class=2, trial_nr=2, instructions="This is another example.")
        self.eaaPhase1Percentage100Form = EaaTrialInformationForm(name="eaa_p1_prob3", presentation_mode=EaaTrialInformationPresentationMode.INSTRUCTION, participant_id=self.participant_id, marker_streamer=self.marker_streamer, main_label_text="", phase=1, points=5, probability_class=3, trial_nr=3, instructions="This is another example.")
        self.eaaPhase1Qnr1Form = EaaPhase1Qnr1Form(participant_id=self.participant_id, marker_streamer=self.marker_streamer)
        self.eaaPhase1Qnr2Form = EaaPhase1Qnr2Form(participant_id=self.participant_id, marker_streamer=self.marker_streamer)
        self.eaaPhase1UnpleasantExampleForm = EaaTrialForm(name="eaa_p1_unpleasant", participant_id=self.participant_id, marker_streamer=self.marker_streamer, phase=1, points=1, probability_class=3, trial_nr=1, image_file="2352.jpg")
        self.eaaPhase2InitialInstructionsForm = EaaPhase2InitialInstructionsForm(marker_streamer=self.marker_streamer)
        self.outtroForm = OuttroForm(marker_streamer=self.marker_streamer)
        
        self.stack.addWidget(self.healthHabitsForm)
        self.stack.addWidget(self.recentActivityForm)
        self.stack.addWidget(self.bisbasForm)
        self.stack.addWidget(self.needforcognitionForm)
        self.stack.addWidget(self.stroopInstructions1Form)
        self.stack.addWidget(self.stroopInstructions2Form)
        self.stack.addWidget(self.stroopInstructions3Form)
        self.stack.addWidget(self.stroopTaskForm)
        self.stack.addWidget(self.wisconsinInstructions1Form)
        self.stack.addWidget(self.wisconsinInstructions2Form)
        self.stack.addWidget(self.wisconsinInstructions3Form)
        self.stack.addWidget(self.wisconsinTaskForm)
        self.stack.addWidget(self.nbackPhase1InitialInstructionsForm)
        self.stack.addWidget(self.nbackPhase1LowInstructionsForm)
        self.stack.addWidget(self.nbackPhase1LowTestForm1)
        self.stack.addWidget(self.nbackPhase1LowTest2InstructionsForm)
        self.stack.addWidget(self.nbackPhase1LowTestForm2)
        self.stack.addWidget(self.nbackPhase1LowTaskLoadForm)
        self.stack.addWidget(self.nbackPhase1MediumInstructionsForm)
        self.stack.addWidget(self.nbackPhase1MediumTestForm1)
        self.stack.addWidget(self.nbackPhase1MediumTest2InstructionsForm)
        self.stack.addWidget(self.nbackPhase1MediumTestForm2)
        self.stack.addWidget(self.nbackPhase1MediumTaskLoadForm)
        self.stack.addWidget(self.nbackPhase1HighInstructionsForm)
        self.stack.addWidget(self.nbackPhase1HighTestForm1)
        self.stack.addWidget(self.nbackPhase1HighTest2InstructionsForm)
        self.stack.addWidget(self.nbackPhase1HighTestForm2)
        self.stack.addWidget(self.nbackPhase1HighTaskLoadForm)
        self.stack.addWidget(self.nbackPhase2InitialInstructionsForm)
        self.stack.addWidget(self.nbackPhase2TrialInformationExample1Form)
        self.stack.addWidget(self.nbackPhase2TrialInformationExample2Form)
        self.stack.addWidget(self.nbackPhase2TrialInformationExample3Form)
        self.stack.addWidget(self.nbackPhase2FinalInstructionsForm)
        self.stack.addWidget(self.eaaPhase1InitialInstructions1Form)
        self.stack.addWidget(self.eaaPhase1InitialInstructions2Form)
        self.stack.addWidget(self.eaaPhase1InitialInstructions3Form)
        self.stack.addWidget(self.eaaPhase1InitialInstructions4Form)
        self.stack.addWidget(self.eaaPhase1Percentage0Form)
        self.stack.addWidget(self.eaaPhase1Percentage50Form)
        self.stack.addWidget(self.eaaPhase1Percentage100Form)
        self.stack.addWidget(self.eaaPhase1Qnr1Form)
        self.stack.addWidget(self.eaaPhase1Qnr2Form)
        self.stack.addWidget(self.eaaPhase1UnpleasantExampleForm)
        self.stack.addWidget(self.eaaPhase2InitialInstructionsForm)
        self.stack.addWidget(self.outtroForm)
        
        self.healthHabitsForm.finished.connect(self.onHealthHabitsFinished)
        self.recentActivityForm.finished.connect(self.onRecentActivityFinished)
        self.bisbasForm.finished.connect(self.onBISBASFinished)
        self.needforcognitionForm.finished.connect(self.onNeedForCognitionFinished)
        self.stroopInstructions1Form.finished.connect(self.onStroopInstructions1Finished)
        self.stroopInstructions2Form.finished.connect(self.onStroopInstructions2Finished)
        self.stroopInstructions3Form.finished.connect(self.onStroopInstructions3Finished)
        self.stroopTaskForm.finished.connect(self.onStroopTaskFinished)
        self.wisconsinInstructions1Form.finished.connect(self.onWisconsinInstructions1Finished)
        self.wisconsinInstructions2Form.finished.connect(self.onWisconsinInstructions2Finished)
        self.wisconsinInstructions3Form.finished.connect(self.onWisconsinInstructions3Finished)
        self.wisconsinTaskForm.finished.connect(self.onWisconsinTaskFinished)
        self.nbackPhase1InitialInstructionsForm.finished.connect(self.onNBackPhase1InitialInstructionsFinished)
        self.nbackPhase1LowInstructionsForm.finished.connect(self.onNBackPhase1LowInstructionsFinished)
        self.nbackPhase1LowTestForm1.finished.connect(self.onNBackPhase1LowTest1Finished)
        self.nbackPhase1LowTest2InstructionsForm.finished.connect(self.onNBackPhase1LowTest2InstructionsFinished)
        self.nbackPhase1LowTestForm2.finished.connect(self.onNBackPhase1LowTest2Finished)
        self.nbackPhase1LowTaskLoadForm.finished.connect(self.onNBackPhase1LowTaskLoadFinished)
        self.nbackPhase1MediumInstructionsForm.finished.connect(self.onNBackPhase1MediumInstructionsFinished)
        self.nbackPhase1MediumTestForm1.finished.connect(self.onNBackPhase1MediumTest1Finished)
        self.nbackPhase1MediumTest2InstructionsForm.finished.connect(self.onNBackPhase1MediumTest2InstructionsFinished)
        self.nbackPhase1MediumTestForm2.finished.connect(self.onNBackPhase1MediumTest2Finished)
        self.nbackPhase1MediumTaskLoadForm.finished.connect(self.onNBackPhase1MediumTaskLoadFinished)
        self.nbackPhase1HighInstructionsForm.finished.connect(self.onNBackPhase1HighInstructionsFinished)
        self.nbackPhase1HighTestForm1.finished.connect(self.onNBackPhase1HighTest1Finished)
        self.nbackPhase1HighTest2InstructionsForm.finished.connect(self.onNBackPhase1HighTest2InstructionsFinished)
        self.nbackPhase1HighTestForm2.finished.connect(self.onNBackPhase1HighTest2Finished)
        self.nbackPhase1HighTaskLoadForm.finished.connect(self.onNBackPhase1HighTaskLoadFinished)
        self.nbackPhase2InitialInstructionsForm.finished.connect(self.onNBackPhase2InitialInstructionsFinished)
        self.nbackPhase2TrialInformationExample1Form.finished.connect(self.onNBackPhase2TrialInformationExample1Finished)
        self.nbackPhase2TrialInformationExample2Form.finished.connect(self.onNBackPhase2TrialInformationExample2Finished)
        self.nbackPhase2TrialInformationExample3Form.finished.connect(self.onNBackPhase2TrialInformationExample3Finished)
        self.nbackPhase2FinalInstructionsForm.finished.connect(self.onNBackPhase2FinalInstructionsFinished)
        self.eaaPhase1InitialInstructions1Form.finished.connect(self.onEAAPhase1InitialInstructions1Finished)
        self.eaaPhase1InitialInstructions2Form.finished.connect(self.onEAAPhase1InitialInstructions2Finished)
        self.eaaPhase1InitialInstructions3Form.finished.connect(self.onEAAPhase1InitialInstructions3Finished)
        self.eaaPhase1InitialInstructions4Form.finished.connect(self.onEAAPhase1InitialInstructions4Finished)
        self.eaaPhase1Percentage0Form.finished.connect(self.onEAAPhase1Percentage0Finished)
        self.eaaPhase1Percentage50Form.finished.connect(self.onEAAPhase1Percentage50Finished)
        self.eaaPhase1Percentage100Form.finished.connect(self.onEAAPhase1Percentage100Finished)
        self.eaaPhase1Qnr1Form.finished.connect(self.onEAAPhase1Qnr1Finished)
        self.eaaPhase1Qnr2Form.finished.connect(self.onEAAPhase1Qnr2Finished)
        self.eaaPhase1UnpleasantExampleForm.finished.connect(self.onEAAPhase1UnpleasantExampleFinished)
        self.eaaPhase2InitialInstructionsForm.finished.connect(self.onEAAPhase2InitialInstructionsFinished)
        self.outtroForm.finished.connect(self.onCloseWindow)
    
    def onCloseWindow(self):
        self.close()
    
    def closeEvent(self, event):
        self.close_lsl()
        super().closeEvent(event)  
    
    def close_lsl(self):
        self.marker_streamer.stop()
        self.marker_thread.quit()
        self.marker_thread.wait()
    
    def setupNBackPhase2TrialForms(self):
        generator = TrialOrderGenerator()
        nbackPhase2Trials = generator.generate_trials()
        
        for trial_nr, (n, points) in enumerate(nbackPhase2Trials, start=1):
            tif_name = f"nback_p2_trial_info_{trial_nr}"
            trialInformationForm = NBackTrialInformationForm(name=tif_name, presentation_mode=NBackTrialInformationPresentationMode.EXPERIMENT, participant_id=self.participant_id, marker_streamer=self.marker_streamer, main_label_text="", phase=2, points=points, n=n, trial_nr=trial_nr, instructions="Press the 'up arrow' key to accept this trial or\npress the 'down arrow' key to skip this trial.")
            trialInformationForm.finished.connect(self.onNBackPhase2TrialInformationShown)
            self.nbackPhase2TrialInformationForms.append(trialInformationForm)
            self.stack.addWidget(trialInformationForm)

            tf_name = f"nback_p2_trial_{trial_nr}"
            trialForm = NBackTrialForm(name=tf_name, participant_id=self.participant_id, marker_streamer=self.marker_streamer, phase=2, points=points, n=n, trial_nr=trial_nr)
            trialForm.finished.connect(self.onNBackPhase2TrialShown)
            self.nbackPhase2TrialForms.append(trialForm)
            self.stack.addWidget(trialForm)

        self.showNextNBackPhase2TrialInformation()

    def showNextNBackPhase2TrialInformation(self):
        if self.nbackPhase2TrialInformationForms:
            nextTrialInformationForm = self.nbackPhase2TrialInformationForms.pop(0)
            QApplication.flush()  
            self.stack.setCurrentWidget(nextTrialInformationForm)
        else:
            self.onEndofNBack()

    def showNextNBackPhase2Trial(self):
        if self.nbackPhase2TrialForms:
            nextTrialForm = self.nbackPhase2TrialForms.pop(0)
            QApplication.flush()  
            self.stack.setCurrentWidget(nextTrialForm)
            
    def skipNextNBackPhase2Trial(self):
        if self.nbackPhase2TrialForms:
            self.nbackPhase2TrialForms.pop(0)
            
    def onEndofNBack(self):
        if self.nbackb4eaa:
            QApplication.flush()  
            self.stack.setCurrentWidget(self.eaaPhase1InitialInstructions1Form)
        else:
            self.stack.setCurrentWidget(self.outtroForm)

    def setupEaaPhase1TrialForms(self):
        generator = EaaPhase1TrialGenerator()
        eaaPhase1Trials = generator.generate_trials()

        for trial_nr, (probability_class, accept_enabled, image_to_show) in enumerate(eaaPhase1Trials, start=2):
            
            presentationMode = EaaTrialInformationPresentationMode.MUST_ACCEPT if accept_enabled else EaaTrialInformationPresentationMode.MUST_REJECT
            
            tif_name = f"eaa_p1_trial_info_{trial_nr}"
            trialInformationForm = EaaTrialInformationForm(name=tif_name, presentation_mode=presentationMode, participant_id=self.participant_id, marker_streamer=self.marker_streamer, main_label_text="", phase=1, points=1, probability_class=probability_class, trial_nr=trial_nr)    
            trialInformationForm.finished.connect(self.onEAAPhase1TrialInformationShown)
            self.eaaPhase1TrialInformationForms.append(trialInformationForm)
            self.stack.addWidget(trialInformationForm)

            tf_name = f"eaa_p1_trial_{trial_nr}"
            
            # ensures that an image is shown when probability_class is 2 (i.e., 50% probability of unpleasant image and noise)
            if probability_class == 2:
                probability_class = 3
            
            trialForm = EaaTrialForm(name=tf_name, participant_id=self.participant_id, marker_streamer=self.marker_streamer, phase=1, points=1, probability_class=probability_class, trial_nr=trial_nr, image_file=image_to_show)
            trialForm.finished.connect(self.onEAAPhase1TrialShown)
            self.eaaPhase1TrialForms.append(trialForm)
            self.stack.addWidget(trialForm)

        self.showNextEaaPhase1TrialInformation()
    
    def showNextEaaPhase1TrialInformation(self):
        if self.eaaPhase1TrialInformationForms:
            nextTrialInformationForm = self.eaaPhase1TrialInformationForms.pop(0)
            QApplication.flush()  
            self.stack.setCurrentWidget(nextTrialInformationForm)
        else:
            self.stack.setCurrentWidget(self.eaaPhase2InitialInstructionsForm)
            
    def showNextEaaPhase1Trial(self):
        if self.eaaPhase1TrialForms:
            nextTrialForm = self.eaaPhase1TrialForms.pop(0)
            QApplication.flush()  
            self.stack.setCurrentWidget(nextTrialForm)
            
    def skipNextEaaPhase1Trial(self):
        if self.eaaPhase1TrialForms:
            self.eaaPhase1TrialForms.pop(0)
    
    def setupEaaPhase2TrialForms(self):
        generator = TrialOrderGenerator()
        eaaPhase2Trials = generator.generate_trials()
        eaaImageProvider = EaaImageProvider() 
        
        for trial_nr, (probability_class, points) in enumerate(eaaPhase2Trials, start=1):
            tif_name = f"eaa_p2_trial_info_{trial_nr}"
            trialInformationForm = EaaTrialInformationForm(name=tif_name, presentation_mode=EaaTrialInformationPresentationMode.EXPERIMENT, marker_streamer=self.marker_streamer, participant_id=self.participant_id, main_label_text="", phase=2, points=points, probability_class=probability_class, trial_nr=trial_nr)    
            trialInformationForm.finished.connect(self.onEAAPhase2TrialInformationShown)
            self.eaaPhase2TrialInformationForms.append(trialInformationForm)
            self.stack.addWidget(trialInformationForm)

            tf_name = f"eaa_p2_trial_{trial_nr}"
            trialForm = EaaTrialForm(name=tf_name, participant_id=self.participant_id, marker_streamer=self.marker_streamer, phase=2, points=points, probability_class=probability_class, trial_nr=trial_nr, image_file=eaaImageProvider.getNextImage())
            trialForm.finished.connect(self.onEAAPhase2TrialShown)
            self.eaaPhase2TrialForms.append(trialForm)
            self.stack.addWidget(trialForm)

        self.showNextEaaPhase2TrialInformation()
    
    def showNextEaaPhase2TrialInformation(self):
        if self.eaaPhase2TrialInformationForms:
            nextTrialInformationForm = self.eaaPhase2TrialInformationForms.pop(0)
            self.stack.setCurrentWidget(nextTrialInformationForm)
        else:
            if self.nbackb4eaa:
                self.stack.setCurrentWidget(self.outtroForm)
            else:
                self.stack.setCurrentWidget(self.nbackPhase1InitialInstructionsForm)
            
    def showNextEaaPhase2Trial(self):
        if self.eaaPhase2TrialForms:
            nextTrialForm = self.eaaPhase2TrialForms.pop(0)
            QApplication.flush()  
            self.stack.setCurrentWidget(nextTrialForm)
            
    def skipNextEaaPhase2Trial(self):
        if self.eaaPhase2TrialForms:
            self.eaaPhase2TrialForms.pop(0)
            
    @pyqtSlot()
    def onWisconsinInstructions1Finished(self):
        QApplication.flush()  
        self.stack.setCurrentWidget(self.wisconsinInstructions2Form)
        
    @pyqtSlot()
    def onWisconsinInstructions2Finished(self):
        QApplication.flush()  
        self.stack.setCurrentWidget(self.wisconsinInstructions3Form)
        
    @pyqtSlot()
    def onWisconsinInstructions3Finished(self):
        QApplication.flush()  
        self.stack.setCurrentWidget(self.wisconsinTaskForm)
        
    @pyqtSlot()
    def onWisconsinTaskFinished(self):
        QApplication.flush()
        if self.nbackb4eaa:  
            self.stack.setCurrentWidget(self.nbackPhase1InitialInstructionsForm)            
        else:
            self.stack.setCurrentWidget(self.eaaPhase1InitialInstructions1Form)
            
    @pyqtSlot()
    def onStroopInstructions1Finished(self):
        QApplication.flush()  
        self.stack.setCurrentWidget(self.stroopInstructions2Form)
        
    @pyqtSlot()
    def onStroopInstructions2Finished(self):
        QApplication.flush()  
        self.stack.setCurrentWidget(self.stroopInstructions3Form)
        
    @pyqtSlot()
    def onStroopInstructions3Finished(self):
        QApplication.flush()  
        self.stack.setCurrentWidget(self.stroopTaskForm)
        
    def onStroopTaskFinished(self):
        QApplication.flush()  
        self.stack.setCurrentWidget(self.wisconsinInstructions1Form)
            
    @pyqtSlot(str)
    def onEAAPhase1TrialInformationShown(self, outcome):
        QApplication.flush()
        if outcome == "accepted":
            self.showNextEaaPhase1Trial()
        else:
            self.skipNextEaaPhase1Trial()
            self.showNextEaaPhase1TrialInformation()
        
    @pyqtSlot(int, int)
    def onEAAPhase1TrialShown(self, points, probability_class):
        QApplication.flush()
        self.showNextEaaPhase1TrialInformation()
    
    @pyqtSlot()
    def onEAAPhase1InitialInstructions1Finished(self):
        QApplication.flush()  
        self.stack.setCurrentWidget(self.eaaPhase1Percentage0Form)
        
    @pyqtSlot()
    def onEAAPhase1Percentage0Finished(self):
        QApplication.flush()  
        self.stack.setCurrentWidget(self.eaaPhase1Percentage50Form)
        
    @pyqtSlot()
    def onEAAPhase1Percentage50Finished(self):
        QApplication.flush()  
        self.stack.setCurrentWidget(self.eaaPhase1Percentage100Form)
        
    @pyqtSlot()
    def onEAAPhase1Percentage100Finished(self):
        QApplication.flush()  
        self.stack.setCurrentWidget(self.eaaPhase1InitialInstructions2Form)
        
    @pyqtSlot()
    def onEAAPhase1InitialInstructions2Finished(self):
        QApplication.flush()  
        self.stack.setCurrentWidget(self.eaaPhase1Qnr1Form)
        
    @pyqtSlot()
    def onEAAPhase1Qnr1Finished(self):
        QApplication.flush()  
        self.stack.setCurrentWidget(self.eaaPhase1InitialInstructions3Form)
        
    @pyqtSlot()
    def onEAAPhase1InitialInstructions3Finished(self):
        QApplication.flush()  
        self.stack.setCurrentWidget(self.eaaPhase1UnpleasantExampleForm)
        
    @pyqtSlot()
    def onEAAPhase1UnpleasantExampleFinished(self):
        QApplication.flush()  
        self.stack.setCurrentWidget(self.eaaPhase1Qnr2Form)
        
    @pyqtSlot()
    def onEAAPhase1Qnr2Finished(self):
        QApplication.flush()  
        self.stack.setCurrentWidget(self.eaaPhase1InitialInstructions4Form)
        
    @pyqtSlot()
    def onEAAPhase1InitialInstructions4Finished(self):
        QApplication.flush()
        self.setupEaaPhase1TrialForms()
        
    @pyqtSlot()
    def onEAAPhase2InitialInstructionsFinished(self):
        QApplication.flush()
        self.setupEaaPhase2TrialForms()
        
    @pyqtSlot(str)
    def onEAAPhase2TrialInformationShown(self, outcome):
        QApplication.flush()
        if outcome == "accepted":
            self.showNextEaaPhase2Trial()
        else:
            self.skipNextEaaPhase2Trial()
            self.showNextEaaPhase2TrialInformation()
        
    @pyqtSlot(int, int)
    def onEAAPhase2TrialShown(self, points, probability_class):
        QApplication.flush()
        self.showNextEaaPhase2TrialInformation()

    @pyqtSlot(str)
    def onNBackPhase2TrialInformationShown(self, outcome):
        QApplication.flush()
        if outcome == "accepted":
            self.showNextNBackPhase2Trial()
        else:
            self.skipNextNBackPhase2Trial()
            self.showNextNBackPhase2TrialInformation()

    @pyqtSlot(int, int)
    def onNBackPhase2TrialShown(self, points, n):
        QApplication.flush()
        self.nbackPhase2_accepted_trials.append((points, n))
        self.showNextNBackPhase2TrialInformation()

    @pyqtSlot(str)
    def onDemographicsFinished(self, participant_id):
        QApplication.flush()
        self.participant_id = participant_id
        self.initChildForms()
        
        if self.mode == 'test':
            if self.shortcut == 'nback':
                self.stack.setCurrentWidget(self.nbackPhase1InitialInstructionsForm)
            elif self.shortcut == 'eaa':
                self.stack.setCurrentWidget(self.eaaPhase1InitialInstructions1Form)
            elif self.shortcut == 'stroop':
                self.stack.setCurrentWidget(self.stroopInstructions1Form)
            elif self.shortcut == 'wisconsin':
                self.stack.setCurrentWidget(self.wisconsinInstructions1Form)
            else:
                self.stack.setCurrentWidget(self.healthHabitsForm)
        else:
            self.stack.setCurrentWidget(self.healthHabitsForm)

    @pyqtSlot()
    def onHealthHabitsFinished(self):
        QApplication.flush()  
        self.stack.setCurrentWidget(self.recentActivityForm)

    @pyqtSlot()
    def onRecentActivityFinished(self):
        QApplication.flush()  
        self.stack.setCurrentWidget(self.bisbasForm)

    @pyqtSlot()
    def onBISBASFinished(self):
        QApplication.flush()  
        self.stack.setCurrentWidget(self.needforcognitionForm)
    
    @pyqtSlot()
    def onNeedForCognitionFinished(self):
        QApplication.flush()  
        self.stack.setCurrentWidget(self.stroopInstructions1Form)
    
    @pyqtSlot()
    def onNBackPhase1InitialInstructionsFinished(self):
        QApplication.flush()  
        self.stack.setCurrentWidget(self.nbackPhase1LowInstructionsForm)
    
    @pyqtSlot()
    def onNBackPhase1LowInstructionsFinished(self):
        QApplication.flush()  
        self.stack.setCurrentWidget(self.nbackPhase1LowTestForm1)
    
    @pyqtSlot()
    def onNBackPhase1LowTest1Finished(self):
        QApplication.flush()  
        self.stack.setCurrentWidget(self.nbackPhase1LowTest2InstructionsForm)
        
    @pyqtSlot()
    def onNBackPhase1LowTest2InstructionsFinished(self):
        QApplication.flush()  
        self.stack.setCurrentWidget(self.nbackPhase1LowTestForm2)
        
    @pyqtSlot()
    def onNBackPhase1LowTest2Finished(self):
        QApplication.flush()  
        self.stack.setCurrentWidget(self.nbackPhase1LowTaskLoadForm)
        
    @pyqtSlot()
    def onNBackPhase1LowTaskLoadFinished(self):
        QApplication.flush()  
        self.stack.setCurrentWidget(self.nbackPhase1MediumInstructionsForm)
    
    @pyqtSlot()
    def onNBackPhase1MediumInstructionsFinished(self):
        QApplication.flush()  
        self.stack.setCurrentWidget(self.nbackPhase1MediumTestForm1)
    
    @pyqtSlot()
    def onNBackPhase1MediumTest1Finished(self):
        QApplication.flush()  
        self.stack.setCurrentWidget(self.nbackPhase1MediumTest2InstructionsForm)

    @pyqtSlot()
    def onNBackPhase1MediumTest2InstructionsFinished(self):
        QApplication.flush()  
        self.stack.setCurrentWidget(self.nbackPhase1MediumTestForm2)
        
    @pyqtSlot()
    def onNBackPhase1MediumTest2Finished(self):
        QApplication.flush()  
        self.stack.setCurrentWidget(self.nbackPhase1MediumTaskLoadForm)

    @pyqtSlot()
    def onNBackPhase1MediumTaskLoadFinished(self):
        QApplication.flush()  
        self.stack.setCurrentWidget(self.nbackPhase1HighInstructionsForm)

    @pyqtSlot()
    def onNBackPhase1HighInstructionsFinished(self):
        QApplication.flush()  
        self.stack.setCurrentWidget(self.nbackPhase1HighTestForm1)
        
    @pyqtSlot()
    def onNBackPhase1HighTest1Finished(self):
        QApplication.flush()  
        self.stack.setCurrentWidget(self.nbackPhase1HighTest2InstructionsForm)
        
    @pyqtSlot()
    def onNBackPhase1HighTest2InstructionsFinished(self):
        QApplication.flush()  
        self.stack.setCurrentWidget(self.nbackPhase1HighTestForm2)
        
    @pyqtSlot()
    def onNBackPhase1HighTest2Finished(self):
        QApplication.flush()  
        self.stack.setCurrentWidget(self.nbackPhase1HighTaskLoadForm)    
        
    @pyqtSlot()
    def onNBackPhase1HighTaskLoadFinished(self):
        QApplication.flush()  
        self.stack.setCurrentWidget(self.nbackPhase2InitialInstructionsForm)
    
    @pyqtSlot()
    def onNBackPhase2InitialInstructionsFinished(self):
        QApplication.flush()  
        self.stack.setCurrentWidget(self.nbackPhase2TrialInformationExample1Form)
        
    @pyqtSlot()
    def onNBackPhase2TrialInformationExample1Finished(self):
        QApplication.flush()  
        self.stack.setCurrentWidget(self.nbackPhase2TrialInformationExample2Form)
        
    @pyqtSlot()
    def onNBackPhase2TrialInformationExample2Finished(self):
        QApplication.flush()  
        self.stack.setCurrentWidget(self.nbackPhase2TrialInformationExample3Form)
        
    @pyqtSlot()
    def onNBackPhase2TrialInformationExample3Finished(self):
        QApplication.flush()  
        self.stack.setCurrentWidget(self.nbackPhase2FinalInstructionsForm)   
        
    @pyqtSlot()
    def onNBackPhase2FinalInstructionsFinished(self):
        QApplication.flush()
        self.setupNBackPhase2TrialForms()

    def keyPressEvent(self, event: QKeyEvent):
        super().keyPressEvent(event)
        if event.key() == Qt.Key_Escape and self.mode == 'test':
            self.close()
        
        QApplication.flush()
        
    def changeEvent(self, event):
        if event.type() == QEvent.WindowStateChange:
            if self.windowState() & Qt.WindowMaximized and not self.isFullScreen():
                self.showFullScreen()
        super().changeEvent(event)

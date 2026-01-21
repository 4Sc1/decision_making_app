import os
import sys
import pandas as pd
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QVBoxLayout, QWidget, QLabel, QMessageBox, QHBoxLayout, QGroupBox
from PyQt6.QtGui import QFont

class FolderSelectorApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Experiment Results Analyzer")
        self.setGeometry(100, 100, 600, 400)

        main_layout = QVBoxLayout()

        self.button = QPushButton("Select Participant Folder")
        self.button.setFont(QFont('Arial', 14))
        self.button.clicked.connect(self.open_folder_dialog)
        main_layout.addWidget(self.button)

        self.folder_label = QLabel("No folder selected")
        self.folder_label.setFont(QFont('Arial', 12))
        main_layout.addWidget(self.folder_label)

        self.results_group = QGroupBox("Results")
        self.results_group.setFont(QFont('Arial', 12))
        results_layout = QVBoxLayout()

        self.eaa_label = QLabel("")
        self.eaa_label.setFont(QFont('Arial', 12))
        results_layout.addWidget(self.eaa_label)

        self.nback_label = QLabel("")
        self.nback_label.setFont(QFont('Arial', 12))
        results_layout.addWidget(self.nback_label)

        self.results_group.setLayout(results_layout)
        main_layout.addWidget(self.results_group)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def open_folder_dialog(self):
        initial_folder = os.path.join(os.getenv('LOCALAPPDATA'), 'ExperimentResults')
        folder = QFileDialog.getExistingDirectory(self, "Select Folder", initial_folder)
        if folder:
            self.folder_label.setText(f"Selected folder: {folder}")
            self.load_csv_files(folder)

    def load_csv_files(self, folder):
        nback_file = os.path.join(folder, 'nback_decisions.csv')
        eaa_file = os.path.join(folder, 'eaa_decisions.csv')
        
        if os.path.exists(nback_file) and os.path.exists(eaa_file):
            try:
                nback_df = pd.read_csv(nback_file, sep=';', encoding='utf-8')
                eaa_df = pd.read_csv(eaa_file, sep=';', encoding='utf-8')
                
                eaa_accepted_points = eaa_df[(eaa_df['outcome'] == 'accepted') & (eaa_df['phase'] == 2)]['points'].sum()
                eaa_overall_points = eaa_df[eaa_df['phase'] == 2]['points'].sum()
                eaa_percentage = (eaa_accepted_points / eaa_overall_points * 100) if eaa_overall_points else 0

                nback_accepted_points = nback_df[(nback_df['outcome'] == 'accepted') & (nback_df['phase'] == 2)]['points'].sum()
                nback_overall_points = nback_df[nback_df['phase'] == 2]['points'].sum()
                nback_percentage = (nback_accepted_points / nback_overall_points * 100) if nback_overall_points else 0

                self.eaa_label.setText(f"EAA Score: {eaa_accepted_points} / {eaa_overall_points} ({eaa_percentage:.2f}%)")
                self.nback_label.setText(f"NBack Score: {nback_accepted_points} / {nback_overall_points} ({nback_percentage:.2f}%)")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load and process CSV files: {e}")
        else:
            QMessageBox.warning(self, "Warning", "CSV files not found in the selected folder.")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    try:
        app.setStyleSheet("""
            QWidget {
                font-size: 14pt;
                background-color: #ffffff;
                color: #323130;
                border: none;
            }
            QLabel, QSlider, QSpinBox, QCheckBox {
                font-size: 14pt;
                color: #323130;
                border: none;
            }
            QPushButton {
                font-size: 14pt;
                background-color: #d4d4d4;
                color: #000000;
                border-radius: 4px;
                padding: 8px 16px;
                border: none;
            }
            QPushButton:hover {
                background-color: #b0b0b0;
            }
            QPushButton:pressed {
                background-color: #8c8c8c;
            }
            QPushButton:disabled {
                background-color: #e0e0e0;
                color: #a1a1a1;
            }
            QLineEdit, QTextEdit {
                font-size: 14pt;
                background-color: #f3f3f3;
                border: none;
                padding: 4px;
            }
            QLineEdit:hover, QTextEdit:hover {
                background-color: #d1d1d1;
            }
            QLineEdit:disabled, QTextEdit:disabled {
                background-color: #f3f3f3;
                color: #a1a1a1;
            }
            QComboBox {
                font-size: 14pt;
                background-color: #f3f3f3;
                border: none;
                padding: 4px;
            }
            QComboBox:hover {
                background-color: #d1d1d1;
            }
            QComboBox:disabled {
                background-color: #f3f3f3;
                color: #a1a1a1;
            }
            QListWidget {
                background-color: #ffffff;
                border: none;
                color: #323130;
            }
            QListWidget::item {
                padding: 4px;
                border: none;
            }
            QListWidget::item:selected {
                background-color: #d1d1d1;
                color: #323130;
                border: none;
            }
            QListWidget::item:focus {
                background-color: #d1d1d1;
                border: none;
            }
            QListWidget::item:hover {
                background-color: #d4d4d4;
                color: #323130;
                border: none;
            }
            QDialog {
                background-color: #ffffff;
                font-size: 14pt;
                color: #323130;
                border: none;
            }
            QSlider::groove:horizontal {
                height: 8px;
                background-color: #d1d1d1;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background-color: #d4d4d4;
                border: none;
                width: 14px;
                margin: -3px 0;
                border-radius: 7px;
            }
            QSpinBox {
                padding: 4px;
                background-color: #f3f3f3;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                width: 16px;
                border: none;
                background-color: #d4d4d4;
            }
            QSpinBox::up-arrow, QSpinBox::down-arrow {
                width: 8px;
                height: 8px;
            }
            QCheckBox::indicator {
                width: 14px;
                height: 14px;
                border-radius: 3px;
                background-color: #d4d4d4;
            }
            QCheckBox::indicator:checked {
                background-color: #8c8c8c;
            }
            QTabWidget::pane {
                border: none;
            }
            QTabWidget::tab-bar {
                left: 5px;
            }
            QTabBar::tab {
                background: #f3f3f3;
                padding: 10px;
            }
            QTabBar::tab:selected {
                background: #ffffff;
            }
            QTabBar::tab:hover {
                background: #d1d1d1;
            }
            QGroupBox {
                font-size: 14pt;
                border: none;
                border-radius: 4px;
                margin-top: 20px;
                padding: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 3px;
                color: #323130;
            }
            QMenuBar {
                background-color: #ffffff;
                color: #323130;
                font-size: 12pt;
            }
            QMenuBar::item {
                background: #ffffff;
                padding: 4px 16px;
            }
            QMenuBar::item:selected {
                background: #d1d1d1;
            }
            QMenu {
                background-color: #ffffff;
                color: #323130;
                font-size: 12pt;
                border: none;
            }
            QMenu::item {
                padding: 4px 24px;
            }
            QMenu::item:selected {
                background: #d1d1d1;
            }
            QStatusBar {
                background: #f3f3f3;
                color: #323130;
                font-size: 14pt;
            }
            QToolBar {
                background: #f3f3f3;
                border: none;
                padding: 4px;
            }
            QScrollArea {
                background-color: #ffffff;
                border: none;
            }
            QScrollBar:vertical {
                width: 16px;
                background-color: #f3f3f3;
                border: none;
                margin: 16px 0 16px 0;
            }
            QScrollBar::handle:vertical {
                background-color: #d4d4d4;
                min-height: 20px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #b0b0b0;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                background: none;
                height: 0px;
                width: 0px;
                subcontrol-position: none;
                subcontrol-origin: margin;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
            QScrollBar:horizontal {
                height: 16px;
                background-color: #f3f3f3;
                border: none;
                margin: 0 16px 0 16px;
            }
            QScrollBar::handle:horizontal {
                background-color: #d4d4d4;
                min-width: 20px;
                border-radius: 4px;
            }
            QScrollBar::handle:horizontal:hover {
                background-color: #b0b0b0;
            }
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                background: none;
                height: 0px;
                width: 0px;
                subcontrol-position: none;
                subcontrol-origin: margin;
            }
            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
                background: none;
            }
        """)
    except Exception as e:
        print(f"Failed to load stylesheet: {e}")
    
    window = FolderSelectorApp()
    window.show()
    sys.exit(app.exec())

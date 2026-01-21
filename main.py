import random
import sys
from datetime import datetime
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from gui.main_window import MainWindow

def main():
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    app = QApplication(sys.argv)
    
    app.setStyleSheet("""
        QWidget {
            font-size: 18pt;
            background-color: #ffffff;
            color: #323130;
        }
        QLabel {
            font-size: 18pt;
            color: #323130;
        }
        QPushButton {
            font-size: 18pt;
            background-color: #0078d4;
            color: white;
            border-radius: 8px;
            padding: 8px 16px;
            border: none;
        }
        QPushButton:hover {
            background-color: #005a9e;
        }
        QPushButton:pressed {
            background-color: #004578;
        }
        QPushButton:disabled {
            background-color: #f3f2f1;
            color: #a19f9d;
        }
        QLineEdit, QTextEdit {
            font-size: 18pt;
            background-color: #f3f2f1;
            border: 1px solid #edebe9;
            padding: 4px;
        }
        QLineEdit:hover, QTextEdit:hover {
            background-color: #e1dfdd;
        }
        QLineEdit:disabled, QTextEdit:disabled {
            background-color: #f3f2f1;
            color: #a19f9d;
        }
        QComboBox {
            font-size: 18pt;
            background-color: #f3f2f1;
            border: 1px solid #edebe9;
            padding: 4px;
        }
        QComboBox:hover {
            background-color: #e1dfdd;
        }
        QComboBox:disabled {
            background-color: #f3f2f1;
            color: #a19f9d;
        }
        QScrollBar:vertical {
            width: 16px;
            background-color: #edebe9;
            border: none;
            margin: 16px 0 16px 0;
        }
        QScrollBar::handle:vertical {
            background-color: #c8c6c4;
            min-height: 20px;
            border-radius: 8px;
        }
        QScrollBar::handle:vertical:hover {
            background-color: #a19f9d;
        }
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            background: none;
            height: 0px;
            width: 0px;
        }
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
            background: none;
        }
        QScrollBar:horizontal {
            height: 16px;
            background-color: #edebe9;
            border: none;
            margin: 0 16px 0 16px;
        }
        QScrollBar::handle:horizontal {
            background-color: #c8c6c4;
            min-width: 20px;
            border-radius: 8px;
        }
        QScrollBar::handle:horizontal:hover {
            background-color: #a19f9d;
        }
        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
            background: none;
            height: 0px;
            width: 0px;
        }
        QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
            background: none;
        }
    """)
    
    current_time = datetime.now()
    random.seed(int(current_time.timestamp()))
    
    main_window = MainWindow()
    main_window.showFullScreen()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

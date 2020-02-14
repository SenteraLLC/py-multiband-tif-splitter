import sys
import os
import logging

# For PyInstaller:
import PySide2.QtGui

from app.error_prompt import ErrHandler
from app.finished_dialog import DoneDialog

from scripts.split_5_band import split_5band_tif

from PySide2.QtWidgets import QApplication, QHBoxLayout, QVBoxLayout, QDesktopWidget
from PySide2.QtWidgets import QWidget, QFileDialog, QCheckBox, QPushButton, QLabel, QLineEdit
from PySide2.QtCore import Qt


class TifSelect(QWidget):

    def __init__(self):
        super().__init__()

        self.done_dialog = None

        self.setWindowTitle('Sentera Multiband Splitting Tool')
        self.setGeometry(0, 0, 600, 400)
        frame = self.frameGeometry()
        screen_center = QDesktopWidget().availableGeometry().center()
        frame.moveCenter(screen_center)
        self.move(frame.topLeft())

        input_label = QLabel('Input Folder:')
        self.input_line = QLineEdit()
        input_button = QPushButton('Browse')
        input_button.clicked.connect(self.set_input_folder)

        output_label = QLabel('Output Folder:')
        self.output_line = QLineEdit()
        output_button = QPushButton('Browse')
        output_button.clicked.connect(self.set_output_folder)

        self.delete_check = QCheckBox('Delete Original Multiband Files')

        split_button = QPushButton('Run Splitting')
        split_button.clicked.connect(self.run_split)

        input_layout = QHBoxLayout()
        input_layout.addWidget(input_label)
        input_layout.addWidget(self.input_line)
        input_layout.addWidget(input_button)

        output_layout = QHBoxLayout()
        output_layout.addWidget(output_label)
        output_layout.addWidget(self.output_line)
        output_layout.addWidget(output_button)

        checkbox_layout = QHBoxLayout()
        checkbox_layout.addWidget(self.delete_check)
        checkbox_layout.setAlignment(Qt.AlignHCenter)

        menu_layout = QVBoxLayout()
        menu_layout.addLayout(input_layout)
        menu_layout.addLayout(output_layout)
        menu_layout.addLayout(checkbox_layout)
        menu_layout.addWidget(split_button)

        self.setLayout(menu_layout)

    def set_input_folder(self):
        input_folder = QFileDialog.getExistingDirectory(self, 'Select Input Folder:', os.path.dirname(os.getcwd()))
        self.input_line.setText(input_folder)
        self.output_line.setText(input_folder)
        return

    # Might not allow this
    def set_output_folder(self):
        output_folder = QFileDialog.getExistingDirectory(self, 'Select Output Folder:', self.input_line.text())
        self.output_line.setText(output_folder)
        return

    def run_split(self):
        if self.delete_check.isChecked():
            delete_originals = True
        else:
            delete_originals = False

        try:
            split_5band_tif(self.input_line.text(), self.output_line.text(), delete_originals)
            self.done_dialog = DoneDialog()
        except Exception as e:
            logging.error(e)


def main():
    root_logger = logging.getLogger()
    root_logger.addHandler(ErrHandler())

    app = QApplication(sys.argv)

    window = TifSelect()
    window.show()

    app.exec_()


if __name__ == '__main__':
    main()

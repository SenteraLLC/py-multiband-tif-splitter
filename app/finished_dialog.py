from PySide2.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout
from PySide2.QtCore import Qt


class DoneDialog(QDialog):

    def __init__(self, parent=None):
        super(DoneDialog, self).__init__(parent)

        self.done_label = QLabel('Splitting...')

        self.ok_button = QPushButton('OK')
        self.ok_button.setEnabled(False)
        self.ok_button.clicked.connect(self.close_dialog)

        done_layout = QVBoxLayout()
        done_layout.addWidget(self.done_label)
        done_layout.addWidget(self.ok_button)
        done_layout.setAlignment(Qt.AlignHCenter)

        self.setLayout(done_layout)
        self.show()

    def close_dialog(self):
        self.close()

    def show_completed(self):
        self.done_label.setText('Splitting completed.')
        self.ok_button.setEnabled(True)

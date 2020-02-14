from PySide2.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout
from PySide2.QtCore import Qt


class DoneDialog(QDialog):

    def __init__(self, parent=None):
        super(DoneDialog, self).__init__(parent)

        done_label = QLabel('Splitting completed.')

        ok_button = QPushButton('OK')
        ok_button.clicked.connect(self.close_dialog)

        done_layout = QVBoxLayout()
        done_layout.addWidget(done_label)
        done_layout.addWidget(ok_button)
        done_layout.setAlignment(Qt.AlignHCenter)

        self.setLayout(done_layout)
        self.show()

    def close_dialog(self):
        self.close()

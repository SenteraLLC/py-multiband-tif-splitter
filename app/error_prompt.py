import logging

from PySide2.QtWidgets import QErrorMessage


class ErrHandler(logging.Handler):

    def __init__(self):
        logging.Handler.__init__(self)

    def emit(self, record):
        error_prompt = QErrorMessage()
        error_prompt.setWindowTitle('Error!')
        error_prompt.showMessage(record.getMessage())
        error_prompt.exec_()
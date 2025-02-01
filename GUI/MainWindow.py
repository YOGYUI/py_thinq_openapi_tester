import os
import sys
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import (QMainWindow, QWidget, QLineEdit, QPushButton, QLabel, QMessageBox,
                               QVBoxLayout, QHBoxLayout, QSizePolicy)
CUR_PATH = os.path.dirname(os.path.abspath(__file__))  # {PROJ}/GUI
PROJ_PATH = os.path.dirname(CUR_PATH)  # {PROJ}
THINQ_PATH = os.path.join(PROJ_PATH, "ThinQ")  # {PROJ}/ThinQ
sys.path.extend([THINQ_PATH])
from ThinQ import ThinqCore, ThinqException


class MainWindow(QMainWindow):
    def __init__(self, core: ThinqCore):
        super().__init__()
        self._core = core
        self._editPersonalAccessToken = QLineEdit()
        self._btnInitialize = QPushButton('INITIALIZE')
        self.initControl()
        self.initLayout()
        self.setWindowTitle("ThinQ OpenAPI Tester")

    def initLayout(self):
        central = QWidget()
        self.setCentralWidget(central)

        vbox_main = QVBoxLayout(central)
        vbox_main.setContentsMargins(4, 4, 4, 4)
        vbox_main.setSpacing(4)

        subwgt = QWidget()
        hbox = QHBoxLayout(subwgt)
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.setSpacing(4)
        lbl = QLabel("Personal Access Token")
        lbl.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        hbox.addWidget(lbl)
        hbox.addWidget(self._editPersonalAccessToken)
        vbox_main.addWidget(subwgt)

        subwgt = QWidget()
        hbox = QHBoxLayout(subwgt)
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.setSpacing(4)
        hbox.addWidget(self._btnInitialize)
        vbox_main.addWidget(subwgt)

    def initControl(self):
        self._editPersonalAccessToken.setPlaceholderText("ThinQ API Personal Access Token")
        self._editPersonalAccessToken.setEchoMode(QLineEdit.EchoMode.Password)
        self._editPersonalAccessToken.setText(self._core.get_api_personal_access_token())
        self._btnInitialize.clicked.connect(self._onClickButtonInitialize)

    def release(self):
        self._core.release()

    def closeEvent(self, event: QCloseEvent) -> None:
        self.release()

    def _onClickButtonInitialize(self):
        pat = self._editPersonalAccessToken.text()
        if len(pat) < 1:
            pat = None
        try:
            self._core.initialize(pat)
        except ThinqException as e:
            QMessageBox.warning(self, "ThinQ Exception", f'{e}')
import sys
import json
from PyQt5 import QtWidgets, QtCore
import qdarkstyle
from NetStuff.Network import ClientNetwork

class LoginWindow(QtWidgets.QWidget):
    switch_to_main = QtCore.pyqtSignal()
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        layout = QtWidgets.QVBoxLayout()
        self.user = QtWidgets.QLineEdit(); self.user.setPlaceholderText("Username")
        self.pwd = QtWidgets.QLineEdit(); self.pwd.setPlaceholderText("Password"); self.pwd.setEchoMode(QtWidgets.QLineEdit.Password)
        btn_login = QtWidgets.QPushButton("Login"); btn_login.clicked.connect(self.do_login)
        lbl = QtWidgets.QLabel("No account? <a href='#'>Sign up!</a>"); lbl.setOpenExternalLinks(False)
        lbl.linkActivated.connect(self.do_signup)
        layout.addWidget(self.user); layout.addWidget(self.pwd); layout.addWidget(btn_login); layout.addWidget(lbl)
        self.setLayout(layout)
        self.net = ClientNetwork()

    def do_login(self):
        username = self.user.text(); password = self.pwd.text()
        self.net.send_packet(1, {"username": username, "password": password})
        resp = self.net.recv_packet()
        if resp and resp.get("id") == 2:
            # login OK
            self.switch_to_main.emit()
        else:
            QtWidgets.QMessageBox.warning(self, "Error", "Login failed")

    def do_signup(self):
        # similar flow with packet id 10 for signup
        pass

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Live Translator")
        layout = QtWidgets.QVBoxLayout()
        hl = QtWidgets.QHBoxLayout()
        self.combo_from = QtWidgets.QComboBox(); self.combo_to = QtWidgets.QComboBox()
        for lang in ["en","tr","ru","de","fr"]:
            self.combo_from.addItem(lang); self.combo_to.addItem(lang)
        hl.addWidget(self.combo_from); hl.addWidget(self.combo_to)
        self.text_in = QtWidgets.QTextEdit()
        self.text_out = QtWidgets.QTextEdit(); self.text_out.setReadOnly(True)
        btn = QtWidgets.QPushButton("Translate"); btn.clicked.connect(self.do_translate)
        layout.addLayout(hl); layout.addWidget(self.text_in); layout.addWidget(btn); layout.addWidget(self.text_out)
        self.setLayout(layout)
        self.net = ClientNetwork()

    def do_translate(self):
        txt = self.text_in.toPlainText()
        frm = self.combo_from.currentText(); to = self.combo_to.currentText()
        self.net.send_packet(4, {"text": txt, "from": frm, "to": to})
        resp = self.net.recv_packet()
        if resp and resp.get("id") == 5:
            self.text_out.setPlainText(resp["payload"]["translated"])
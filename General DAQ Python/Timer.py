

from PyQt5 import QtWidgets, QtGui, QtCore

class CustomWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.layout  = QtWidgets.QGridLayout()
        self.button1 = QtWidgets.QPushButton("Start Timer")
        self.button2 = QtWidgets.QPushButton("Stop Timer")
        self.label1  = QtWidgets.QLabel("")
        self.label1.setWordWrap(True)
        self.timer=QtCore.QTimer()
        
        self.layout.addWidget(self.button1, 0, 0)
        self.layout.addWidget(self.button2, 0, 1)
        self.layout.addWidget(self.label1, 1, 0, 1, 3)
        self.setLayout(self.layout)
        self.layout.setColumnStretch(2, 1)
        self.layout.setRowStretch(2, 1)
        self.button1.clicked.connect(self.start_timer)
        self.button2.clicked.connect(self.stop_timer)
    def start_timer(self):
        self.timer.timeout.connect(self.startPressed)
        self.timer.start()
        self.timer.setInterval(500)
        self.timecount=0

    def startPressed(self):
        self.label1.setText(str(self.timecount))
        self.timecount=self.timecount+1
        print(self.timecount)
        #self.label1.setText(self.timecount)
    def stop_timer(self):
        self.timer.stop()
        self.timer.timeout.disconnect(self.startPressed)
    


class App(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.cw = CustomWidget()
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.cw)

        self.setLayout(self.layout)
        self.show()

QtWidgets.QApplication.setStyle(QtWidgets.QStyleFactory.create("Fusion"))
app = QtWidgets.QApplication([])
win = App()
status = app.exec_()
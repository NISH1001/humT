import sys
from PyQt4 import QtGui,QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *

class humUi(QtGui.QMainWindow):
    def __init__(self):
        super(humUi,self).__init__()
        self.initUI()

    def initUI(self):
        QtGui.QToolTip.setFont(QtGui.QFont('SansSerif', 10))

    # record button
        rbtn = QtGui.QPushButton('RECORD', self)
        rbtn.setToolTip('Record Your Hum')
        rbtn.clicked.connect(self.recordBtn)
        rbtn.resize(rbtn.sizeHint())
        rbtn.move(150, 100)

    # stop button
        sbtn = QtGui.QPushButton('STOP', self)
        sbtn.setToolTip('Stop Recording')
        sbtn.clicked.connect(self.stopBtn)
        sbtn.resize(sbtn.sizeHint())
        sbtn.move(250,100)
    # match button
        mbtn = QtGui.QPushButton('SEARCH', self)
        mbtn.setToolTip('Search Hum')
        mbtn.clicked.connect(self.searchBtn)
        mbtn.resize(sbtn.sizeHint())
        mbtn.move(200, 150)
    # quit button
        qbtn=QtGui.QPushButton('Quit',self)
        qbtn.clicked.connect(QtCore.QCoreApplication.instance().quit)
        qbtn.move(350, 200)

    #lcd widget
        self.lcd =QtGui.QLCDNumber(self)
        self.timer=QTimer()
        self.start_time=0
        self.lcd.display("%02d:%02d" %(self.start_time/60,self.start_time/60))
        self.timer.timeout.connect(self.updateLCD)
        self.lcd.move(200,50)


    # actions
        exitAction = QtGui.QAction(QtGui.QIcon('exit24.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(QtGui.qApp.quit)

        updateAction=QtGui.QAction(QtGui.QIcon('update.png'),'Add Songs',self)
        updateAction.setShortcut('Ctrl+a')
        updateAction.triggered.connect(self.addSong)

    # menu-bar
        menubar=self.menuBar()
        updateDB=menubar.addMenu('&Update DB')
        updateDB.addAction(updateAction)
        updateDB.addAction(exitAction)


    # layout
        hbox=QtGui.QHBoxLayout()
        vbox=QtGui.QVBoxLayout()
        hbox.addWidget(self.lcd)
        vbox.addWidget(rbtn)
        vbox.addWidget(sbtn)
        hbox.addLayout(vbox)
        hbox.addWidget(qbtn)
        """
        hbox.addWidget(self.lcd)
        hbox.addWidget(rbtn)

        vbox=QtGui.QVBoxLayout()
        self.setCentralWidget(self.lcd)
        #vbox.addStretch(1)
        vbox.addLayout(hbox)
        vbox.addWidget(qbtn)
        self.setLayout(vbox)
        """

        self.resize(500,250)
        self.center()
        self.statusBar()

        self.setWindowTitle('HumT')
        self.show()
    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def recordBtn(self):
        sender=self.sender()
        # need record function here
        self.restartTimer()
        rbtn=QPushButton("stop",self)
        self.statusBar().showMessage('Recording Started')

    def stopBtn(self):
        self.statusBar().showMessage('Recording Stoped')
        self.timer.stop()
    def searchBtn(self):
        self.statusBar().showMessage('Searching ... ')
        pass

    def restartTimer(self):
        # Reset the timer and the lcd
        self.timer.stop()
        self.start_time = 0
        self.lcd.display("%02d:%02d" % (self.start_time/60,self.start_time % 60))
        # Restart the timer
        self.timer.start(1000)

    def updateLCD(self):
        # Update the lcd
        self.start_time += 1
        if self.start_time >= 0:
            self.lcd.display("%02d:%02d" % (self.start_time/60,self.start_time % 60))
        else:
            print "Error: Time can't be -ve"
    def addSong(self):
        pass


def main():
    app = QtGui.QApplication(sys.argv)

    test=humUi()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

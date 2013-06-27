#!/usr/bin/env python
import sys
import ConfigParser
from PyQt4 import QtGui, QtCore
import time
import os

class Spreader(QtGui.QMainWindow):
    def __init__(self):
        super(Spreader, self).__init__()
        QtCore.QObject.connect(QtGui.qApp, QtCore.SIGNAL('lengthChanged'), self.updateStatus)
        
        self.initUI()
        self.initConfig()
        
    def initUI(self):
    
        #Central Widget
        self.spreading = Example()
        self.setCentralWidget(self.spreading)
        
        
        #Status Bar Stuff
        self.statusBar()
        self.count = QtGui.QLabel("Spreading {0} words at {1} WPM".format(self.spreading.textLength, self.spreading.wpm))
        self.statusBar().addPermanentWidget(self.count)
        
        #Actions
        exitAction = QtGui.QAction(QtGui.QIcon('img/application-exit.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)
        
        startAction = QtGui.QAction(QtGui.QIcon('img/media-playback-start.png'), 'Start', self)
        startAction.setShortcut('F5')
        startAction.setStatusTip('Start (F5)')
        startAction.triggered.connect(self.spreading.play)
        
        stopAction = QtGui.QAction(QtGui.QIcon('img/media-playback-stop.png'), 'Stop', self)
        stopAction.setShortcut('F6')
        stopAction.setStatusTip('Stop (F6)')
        stopAction.triggered.connect(self.spreading.stop)
        
        pauseAction = QtGui.QAction(QtGui.QIcon('img/media-playback-pause.png'), 'Pause', self)
        pauseAction.setShortcut('F7')
        pauseAction.setStatusTip('Pause (F7)')
        pauseAction.triggered.connect(self.spreading.pause)
        
        increaseAction = QtGui.QAction(QtGui.QIcon('img/media-seek-forward.png'), 'Increase Speed', self)
        increaseAction.setShortcut('F9')
        increaseAction.setStatusTip('Increase Speed (F9)')
        increaseAction.triggered.connect(self.spreading.changeSpeed)
        
        decreaseAction = QtGui.QAction(QtGui.QIcon('img/media-seek-backward.png'), 'Decrease Speed', self)
        decreaseAction.setShortcut('F8')
        decreaseAction.setStatusTip('Decrease Speed (F8)')
        decreaseAction.triggered.connect(self.spreading.changeSpeed)
        
        settingsAction = QtGui.QAction(QtGui.QIcon('img/preferences.png'), 'Preferences', self)
        settingsAction.setShortcut('F12')
        settingsAction.setStatusTip('Preferences (F12)')
        settingsAction.triggered.connect(self.spreading.settings)
        
        openAction = QtGui.QAction(QtGui.QIcon('img/document-open.png'), 'Open', self)
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open new file')
        openAction.triggered.connect(self.spreading.showOpen)
        
        saveAction = QtGui.QAction(QtGui.QIcon('img/document-save-as.png'), 'Save As', self)
        saveAction.setShortcut('Ctrl+S')
        saveAction.setStatusTip('Save new file')
        saveAction.triggered.connect(self.spreading.showSave)
        
        #Menu bar
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openAction)
        fileMenu.addAction(saveAction) 
        fileMenu.addAction(settingsAction)
        fileMenu.addAction(exitAction)
        
        #Toolbar
        self.toolbar = self.addToolBar('Tools')
        self.toolbar.addAction(startAction)
        self.toolbar.addAction(pauseAction)
        self.toolbar.addAction(stopAction)
        self.toolbar.addAction(decreaseAction)
        self.toolbar.addAction(increaseAction)
        self.toolbar.addAction(openAction)
        self.toolbar.addAction(saveAction)
        self.toolbar.addAction(settingsAction)
        self.toolbar.addAction(exitAction)
        
        
        #Window Stuff
        self.setWindowIcon(QtGui.QIcon('img/spreader.png'))
        self.resize(650,400)
        self.center()
        self.setWindowTitle('Spreader')    
        self.show()
        
    def initConfig(self):
        Config = ConfigParser.ConfigParser()
        try:
            cfgfile = open("settings.ini",'r')
            Config.readfp(cfgfile)
            Config.sections()
            self.spreading.increment = Config.getint('Settings', 'Increment')
            self.spreading.wpm = Config.getint('Settings', 'WPM')
            self.spreading.reverse = Config.getboolean('Settings', 'Reverse')
            self.spreading.andDrill = Config.getboolean('Settings', 'InsertWord')
            self.spreading.andWord = Config.get('Settings', 'WordToInsert')
            self.spreading.defaultText = Config.get('Settings', 'DefaultText')
            self.spreading.textEdit.setText(self.spreading.defaultText)
        except:
            print('Error reading settings.ini, reverting to default.')
            try:
                if cfgfile:
                    cfgfile.close()
            except:
                pass
            cfgfile = open("settings.ini",'w')
#            self.increment = 10
#            self.wpm = 500
#            self.reverse = False
#            self.andDrill = False
#            self.andWord = 'and'
            self.writeIni(cfgfile)
            cfgfile.close()
            
    def writeIni(self,f):
        Config = ConfigParser.ConfigParser()
        Config.add_section('Settings')
        Config.set('Settings','Increment',self.spreading.increment)
        Config.set('Settings','WPM',self.spreading.wpm)
        Config.set('Settings','Reverse',self.spreading.reverse)
        Config.set('Settings','InsertWord',self.spreading.andDrill)   
        Config.set('Settings','WordToInsert',self.spreading.andWord)
        Config.set('Settings','DefaultText',self.spreading.defaultText) 
        Config.write(f)        
        
    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
    def updateStatus(self,length,wpm):
        self.count.setText("Spreading {0} words at {1} WPM".format(length,wpm))
        
    def closeEvent(self,event):
        f = open('settings.ini','w')
        self.writeIni(f)
        f.close()
#        for item in self.savedSettings.keys():
#            print("{0}={1}".format(item,self.savedSettings[item]))
#        super(Spreader, self).close()

class Example(QtGui.QWidget):
    
    def __init__(self):
        super(Example, self).__init__()
        
        self.initUI()
        
        QtCore.QObject.connect(QtGui.qApp, QtCore.SIGNAL('wpmChanged'), self.changeWpm)
        QtCore.QObject.connect(QtGui.qApp, QtCore.SIGNAL('incrementChanged'), self.changeIncrement)
        QtCore.QObject.connect(QtGui.qApp, QtCore.SIGNAL('reverseChanged'), self.changeReverse)
        QtCore.QObject.connect(QtGui.qApp, QtCore.SIGNAL('andDrillChanged'), self.changeAndDrill)
        QtCore.QObject.connect(QtGui.qApp, QtCore.SIGNAL('andWordChanged'), self.changeAndWord)
        
    def initUI(self):
        
        #Layout              
        vbox = QtGui.QVBoxLayout()
        
        
        #Widgets
        self.textEdit = QtGui.QTextEdit()
        self.defaultText = 'From the longer view offered by a historical-materialist critique of capitalism, the direction that would be taken by U.S. imperialism following the fall of the Soviet Union was never in doubt. Capitalism by its very logic is a globally expansive system. The contradiction between its transnational economic aspirations and the fact that politically it remains rooted in particular nation states is insurmountable for the system. Yet, ill-fated attempts by individual states to overcome this contradiction are just as much a part of its fundamental logic. In present world circumstances, when one capitalist state has a virtual monopoly of the means of destruction, the temptation for that state to attempt to seize full-spectrum dominance and to transform itself into the de facto global state governing the world economy is irresistible.'
        self.textEdit.setText(self.defaultText)
        self.text = unicode(self.textEdit.toPlainText()).split()
        self.textLength = len(self.text)
        QtCore.QObject.connect(self.textEdit, QtCore.SIGNAL('textChanged()'), self.lengthChanged)
        
        self.word = QtGui.QLabel('Hello User')
        font = QtGui.QFont("Georgia", 48, QtGui.QFont.Normal, False)
        self.word.setAlignment(QtCore.Qt.AlignCenter)
        self.word.setFont(font)
        
        self.slider = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        self.slider.setMinimum(0)
        self.slider.setMaximum(self.textLength - 1)
        QtCore.QObject.connect(self.slider, QtCore.SIGNAL('valueChanged(int)'), self.movePosition)
        
        #Add stuff
        vbox.addWidget(self.textEdit)
        vbox.addWidget(self.word)
        vbox.addWidget(self.slider)
        
        self.setLayout(vbox)
        
        #Variables
        self.number = 0
        self.paused = True
        self.playing = False
        
        #Config
        self.increment = 10
        self.wpm = 500
        self.reverse = False
        self.andDrill = False
        self.andWord = 'and'
        
    def settings(self):
        print('Settings')
        self.pause()
        dlg = Settings(self,self.wpm,self.increment,self.reverse,self.andDrill,self.andWord)
        dlg.setModal(True)
        dlg.exec_()
        print('Set settings')
        
    def movePosition(self, newNumber):
        if not self.reverse or not self.playing:
            self.number = newNumber
        else:
            if self.playing:
                self.number = -(self.textLength - 1 - newNumber)    #Force an IndexError
            
        if self.word.text != self.text[self.number]:
                self.word.setText(self.text[self.number])
        
    def play(self):
        if not self.playing:
            self.text = unicode(self.textEdit.toPlainText()).split()
            self.timer = QtCore.QTimer()
            self.timer.timeout.connect(self.changeword)
            try:
                self.newtext = self.text[self.number]
            except IndexError:
                pass
            self.conversionfactor = 12000/self.wpm
            self.paused = False
            self.playing = True
            self.textEdit.setReadOnly(True)
            self.minimum = self.conversionfactor * 5
            self.changeword()
            
#        self.timer.start(self.conversionfactor * len(self.newtext)
        
    def changeword(self):
        if not self.paused:
            try:
                if self.number >= 0:
                    self.slider.setSliderPosition(self.number)
                else:
                    self.slider.setSliderPosition(self.textLength - 1 + self.number)
#                print(self.number)
                self.newtext = self.text[self.number]
                self.word.setText(self.newtext)
                self.changeTime()
            except IndexError:
                self.stop()
            
    def changeTime(self):
#        if self.andDrill and (self.number % 2) == 0:
        if self.andDrill:
            self.delay(self.conversionfactor,len(self.newtext),self.displayAnd, self.minimum)
        else:
            self.delay(self.conversionfactor,len(self.newtext),self.changeword, self.minimum)
            if self.reverse:
                self.number -= 1
            else:
                self.number += 1
            
    def displayAnd(self):
        self.newtext = self.andWord
        self.word.setText(self.newtext)
        self.delay(self.conversionfactor,len(self.newtext),self.changeword, self.minimum + 100)
        if self.reverse:
            self.number -= 1
        else:
            self.number += 1
            
    def delay(self, conversion, length, function,minimum):
        if length > 5:
            self.timer.singleShot(conversion * length, function)
        else:
            self.timer.singleShot(minimum, function)
        
    def pause(self):
        self.paused = True
        self.playing = False
            
    def stop(self):
        self.paused = True
        self.playing = False
        self.text = unicode(self.textEdit.toPlainText()).split()
        self.number = 0
        try:
            self.word.setText(self.text[self.number])
        except IndexError:
            pass
        self.slider.setSliderPosition(self.number)
        self.textEdit.setReadOnly(False)
        print('stop')
        
    def changeSpeed(self):
        sender = self.sender()
        increment = self.increment
        if sender.text() == "Decrease Speed":
            increment = -self.increment
        self.wpm += increment
        if self.wpm < 0:
            self.wpm -= increment
        try:
            self.conversionfactor = 12000/self.wpm
        except ZeroDivisionError:
            self.wpm = 10
            self.conversionfactor = 12000/self.wpm
        QtGui.qApp.emit(QtCore.SIGNAL("lengthChanged"),self.textLength,self.wpm)
        
    def lengthChanged(self):
        self.textLength = len(unicode(self.textEdit.toPlainText()).split())
        self.slider.setMaximum(self.textLength - 1)
        self.stop()
        QtGui.qApp.emit(QtCore.SIGNAL("lengthChanged"),self.textLength,self.wpm)
        
    def changeWpm(self,wpm):
        try:
            self.wpm = int(wpm)            
        except ValueError:
            print("Invalid wpm. Must be integer.")
            self.wpm = 500
        QtGui.qApp.emit(QtCore.SIGNAL("lengthChanged"),self.textLength,self.wpm)
        print("Wpm changed to {0}".format(self.wpm))
        
    def changeIncrement(self,increment):
        try:
            self.increment = int(increment)            
        except ValueError:
            print("Invalid wpm. Must be integer.")
            self.increment = 10
        print("Increment changed to {0}".format(self.increment))
        
    def changeReverse(self,checkstate):
        if checkstate == 2:
            self.reverse = True
        else:
            self.reverse = False
            
    def changeAndDrill(self,checkstate):
        if checkstate == 2:
            self.andDrill = True
        else:
            self.andDrill = False
            
    def changeAndWord(self, word):
        self.andWord = word
        
    def showOpen(self):
        if not self.playing:
            fname = QtGui.QFileDialog.getOpenFileName(self, "Open a file", os.getcwd(), "Plain text files (*.txt)")
            print(fname)
            try:
                f = open(fname, 'r')
                with f:        
                    data = f.read()
                    self.textEdit.setText(data)
            except IOError:
                pass
                
    def showSave(self):
        if not self.playing:
            fname = QtGui.QFileDialog.getSaveFileName(self, "Save a file", os.getcwd(), "Plain text files (*.txt)")
            print(fname)
            try:
                f = open(fname + '.txt', 'w')
                with f:        
                    f.write(str(self.textEdit.toPlainText()))
            except IOError:
                pass   

class Settings(QtGui.QDialog):
    def __init__(self,parent=None,wpm=500,increment=10,reverse=False,andDrill=False,andWord='and'):
        super(Settings, self).__init__()
        self.previousWpm = str(wpm)
        self.previousIncrement = str(increment)
        self.previousReverse = reverse
        self.previousAndDrill = andDrill
        self.previousAndWord = andWord
        self.initUI()
        
    def initUI(self):
        print('Initializing settings')
        
        self.settingsDict = dict()
        validator = QtGui.QIntValidator(1,9999999)
        
        grid = QtGui.QGridLayout()
       
        #Change WPM
        wpm = QtGui.QLabel('WPM')
        self.wpmEdit = QtGui.QLineEdit()
        self.wpmEdit.setValidator(validator)
        self.wpmEdit.setText(self.previousWpm)
        QtCore.QObject.connect(self.wpmEdit, QtCore.SIGNAL('textChanged(QString)'), self.changeSetting)
        self.settingsDict[self.wpmEdit] = 'wpm'
        
        #Change increment
        increment = QtGui.QLabel('Speed change increment')
        self.incrementEdit = QtGui.QLineEdit()
        self.incrementEdit.setValidator(validator)
        self.incrementEdit.setText(self.previousIncrement)
        QtCore.QObject.connect(self.incrementEdit, QtCore.SIGNAL('textChanged(QString)'), self.changeSetting)
        self.settingsDict[self.incrementEdit] = 'increment'
        
        #Change reverse mode
        self.enableReverse = QtGui.QCheckBox("Read backwards")
        if self.previousReverse:
            self.enableReverse.setCheckState(2)
        QtCore.QObject.connect(self.enableReverse, QtCore.SIGNAL('stateChanged(int)'), self.changeSetting)
        self.settingsDict[self.enableReverse] = 'reverse'
        
        #Change and mode
        self.enableAndDrill = QtGui.QCheckBox("Insert word")
        if self.previousAndDrill:
            self.enableAndDrill.setCheckState(2)
        QtCore.QObject.connect(self.enableAndDrill, QtCore.SIGNAL('stateChanged(int)'), self.changeSetting)
        self.settingsDict[self.enableAndDrill] = 'andDrill'
        
        self.andDrillEdit = QtGui.QLineEdit()
        self.andDrillEdit.setText(self.previousAndWord)
        QtCore.QObject.connect(self.andDrillEdit, QtCore.SIGNAL('textChanged(QString)'), self.changeSetting)
        self.settingsDict[self.andDrillEdit] = 'andWord'
        
        #Close button
        self.closeButton = QtGui.QPushButton("Close")
        QtCore.QObject.connect(self.closeButton, QtCore.SIGNAL('clicked()'), self.close)
        
        #Create layout
        grid.addWidget(wpm,0, 0)
        grid.addWidget(self.wpmEdit, 0, 1)
        grid.addWidget(increment,1,0)
        grid.addWidget(self.incrementEdit,1,1)
        grid.addWidget(self.enableReverse,2,0)
        grid.addWidget(self.enableAndDrill,3,0)
        grid.addWidget(self.andDrillEdit, 3, 1)
        grid.addWidget(self.closeButton, 4, 2)
        
        self.setLayout(grid) 
        
        self.setWindowTitle('Preferences')  

    def changeSetting(self, change):
        print(change)
        sender = self.sender()
        print("Emitting " + self.settingsDict[sender] + "Changed")
        QtGui.qApp.emit(QtCore.SIGNAL(self.settingsDict[sender] + "Changed"), (change))

        
def main():
    app = QtGui.QApplication(sys.argv)
    ex = Spreader()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()    

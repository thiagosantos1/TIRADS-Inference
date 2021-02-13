'''
    Author: Thiago Santos

    A simple GUI application to predict TIRADS/ATA based on
    a giving thyroid cancer nodule description - Free text
'''


from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import time
from models import *
from PyQt5.QtCore import Qt



class Ui_TIRADS(QtWidgets.QMainWindow):

    def __init__(self):
        super(Ui_TIRADS, self).__init__()
        self.setObjectName("TIRADS")
        self.setFixedSize(761, 454)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(0, 0, 761, 51))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.ata = QtWidgets.QPushButton(self.frame)
        self.ata.setGeometry(QtCore.QRect(210, 10, 113, 32))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.ata.setFont(font)
        self.ata.setObjectName("ata")
        self.tirads = QtWidgets.QPushButton(self.frame)
        self.tirads.setGeometry(QtCore.QRect(430, 10, 113, 32))  
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.tirads.setFont(font)
        self.tirads.setObjectName("tirads")
        self.nodule_desc = QtWidgets.QTextEdit(self.centralwidget)
        self.nodule_desc.setGeometry(QtCore.QRect(40, 120, 311, 291))
        self.nodule_desc.setObjectName("nodule_desc")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(120, 90, 141, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.predict = QtWidgets.QPushButton(self.centralwidget)
        self.predict.setEnabled(True)
        self.predict.setGeometry(QtCore.QRect(410, 230, 113, 32))
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(False)
        font.setWeight(50)
        self.predict.setFont(font)
        self.predict.setCheckable(False)
        self.predict.setAutoDefault(False)
        self.predict.setFlat(False)
        self.predict.setObjectName("predict")
        self.pred_1 = QtWidgets.QPushButton(self.centralwidget)
        self.pred_1.setEnabled(False)
        self.pred_1.setGeometry(QtCore.QRect(610, 120, 113, 32))
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(False)
        font.setWeight(50)
        self.pred_1.setFont(font)
        self.pred_1.setCheckable(False)
        self.pred_1.setAutoDefault(False)
        self.pred_1.setFlat(False)
        self.pred_1.setObjectName("pred_1")
        self.pred_1.setStyleSheet( "background-color : rgb(235, 236, 240)") 
        self.pred_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pred_2.setEnabled(False)
        self.pred_2.setGeometry(QtCore.QRect(610, 180, 113, 32))
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(False)
        font.setWeight(50)
        self.pred_2.setFont(font)
        self.pred_2.setCheckable(False)
        self.pred_2.setAutoDefault(False)
        self.pred_2.setFlat(False)
        self.pred_2.setObjectName("pred_2")
        self.pred_2.setStyleSheet( "background-color : rgb(235, 236, 240)") 
        self.pred_3 = QtWidgets.QPushButton(self.centralwidget)
        
        self.pred_3.setEnabled(False)
        self.pred_3.setGeometry(QtCore.QRect(610, 240, 113, 32))
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(False)
        font.setWeight(50)
        self.pred_3.setFont(font)
        self.pred_3.setCheckable(False)
        self.pred_3.setAutoDefault(False)
        self.pred_3.setFlat(False)
        self.pred_3.setObjectName("pred_3")
        self.pred_3.setStyleSheet( "background-color : rgb(235, 236, 240)") 

        self.pred_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pred_4.setEnabled(False)
        self.pred_4.setGeometry(QtCore.QRect(610, 300, 113, 32))
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(False)
        font.setWeight(50)
        self.pred_4.setFont(font)
        self.pred_4.setCheckable(False)
        self.pred_4.setAutoDefault(False)
        self.pred_4.setFlat(False)
        self.pred_4.setObjectName("pred_4")
        self.pred_4.setStyleSheet( "background-color : rgb(235, 236, 240)") 

        self.pred_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pred_5.setEnabled(False)
        self.pred_5.setGeometry(QtCore.QRect(610, 360, 113, 32))
        self.pred_5.setStyleSheet( "background-color : rgb(235, 236, 240)") 

        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(False)
        font.setWeight(50)
        self.pred_5.setFont(font)
        self.pred_5.setCheckable(False)
        self.pred_5.setAutoDefault(False)
        self.pred_5.setFlat(False)
        self.pred_5.setObjectName("pred_5")
        self.buttons = [ self.pred_1,self.pred_2,self.pred_3,self.pred_4,self.pred_5]

        self.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

        # progresse bar
        self.progress = QtWidgets.QProgressBar(self)# QtWidgets.QProgressBar(self)
        self.progress.setGeometry(360,250,200,50)

        QtWidgets.QApplication.processEvents() 
        # by default, TIRADS is selected - Let's choose by changing color to blue
        self.model_target = "tirads"
        self.tirads.setStyleSheet( "background-color :  rgb(0, 176, 255)") 
        # if click tirads:
        self.tirads.clicked.connect(self.tirads_clicked)


        # ata option
        self.ata.setStyleSheet( "background-color :  rgb( 242, 250, 254 )") 
        self.ata.clicked.connect(self.ata_clicked)

        # predict action
        self.predict.clicked.connect(self.predict_text)              

        #self.clean_buttons()


        self.model = Models()


        QtWidgets.QApplication.processEvents() 

        self.show()


    '''
        This will be exectuded once you press the button to predict
    '''
    def predict_text(self):
        txt = self.nodule_desc.toPlainText().lower()

        self.clean_buttons()
        if len(txt) >3:
            QtWidgets.QApplication.processEvents() 
            self.progress_bar()
            self.model.predict(txt, model_type=self.model_target)

            pred_colors = ["rgb(0, 255, 0)", "rgb(176, 248, 149)",  "rgb(229, 253, 220)", "rgb(252, 206, 71)","rgb(255, 168, 48)"]

            for index,pred in enumerate(self.model.pred_sorted):
                but = self.buttons[pred]
                QtWidgets.QApplication.processEvents() 
                but.setEnabled(True)
                color = "background-color : " + pred_colors[index]
                but.setStyleSheet( color) #rgb(0,204,103)


    def clean_buttons(self):
        QtWidgets.QApplication.processEvents() 
        for b in self.buttons:
            QtWidgets.QApplication.processEvents() 
            b.setEnabled(False)
            b.setStyleSheet( "background-color : rgb(235, 236, 240)") 
            QtWidgets.QApplication.processEvents() 

    def progress_bar(self):
        self.completed = 0
        while self.completed < 100:
            QtWidgets.QApplication.processEvents() 
            self.completed += 0.001
            self.progress.setValue(self.completed)


    def tirads_clicked(self):
        self.tirads.setStyleSheet( "background-color :  rgb(0, 176, 255)") 
        self.ata.setStyleSheet( "background-color :  rgb( 242, 250, 254 )") 
        self.model_target = "tirads"

        # change labels to tirads
        self.clean_buttons()

        self.pred_1.setGeometry(QtCore.QRect(610, 120, 113, 32))
        self.pred_1.setText(self._translate("TIRADS", "TIRADS 1"))

        self.pred_2.setGeometry(QtCore.QRect(610, 180, 113, 32))
        self.pred_2.setText(self._translate("TIRADS", "TIRADS 2"))

        self.pred_3.setGeometry(QtCore.QRect(610, 240, 113, 32))
        self.pred_3.setText(self._translate("TIRADS", "TIRADS 3"))

        self.pred_4.setGeometry(QtCore.QRect(610, 300, 113, 32))
        self.pred_4.setText(self._translate("TIRADS", "TIRADS 4"))

        self.pred_5.setGeometry(QtCore.QRect(610, 360, 113, 32))
        self.pred_5.setText(self._translate("TIRADS", "TIRADS 5"))

    def ata_clicked(self):
        self.ata.setStyleSheet( "background-color :  rgb(0, 176, 255)") 
        self.tirads.setStyleSheet( "background-color :  rgb( 242, 250, 254 )") 
        self.model_target = "ata"

        self.clean_buttons()
        # change labels to ata
        self.pred_1.setGeometry(QtCore.QRect(570, 120, 161, 32))
        self.pred_1.setText(self._translate("TIRADS", "Benign"))

        self.pred_2.setGeometry(QtCore.QRect(570, 180, 161, 32))
        self.pred_2.setText(self._translate("TIRADS", "Not Suspicious"))

        self.pred_3.setGeometry(QtCore.QRect(570, 240, 161, 32))
        self.pred_3.setText(self._translate("TIRADS", "Mildly Suspicious"))

        self.pred_4.setGeometry(QtCore.QRect(570, 300, 161, 32))
        self.pred_4.setText(self._translate("TIRADS", "Moderately Suspicious"))

        self.pred_5.setGeometry(QtCore.QRect(570, 360, 161, 32))
        self.pred_5.setText(self._translate("TIRADS", "Highly Suspicious"))
        
    def retranslateUi(self):
        self._translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(self._translate("TIRADS", "TIRADS Classifier"))
        self.ata.setText(self._translate("TIRADS", "ATA"))
        self.tirads.setText(self._translate("TIRADS", "TIRADS"))
        self.label.setText(self._translate("TIRADS", "Nodule Description"))
        self.predict.setText(self._translate("TIRADS", "Predict Score"))
        self.pred_1.setText(self._translate("TIRADS", "TIRADS 1"))
        self.pred_2.setText(self._translate("TIRADS", "TIRADS 2"))
        self.pred_3.setText(self._translate("TIRADS", "TIRADS 3"))
        self.pred_4.setText(self._translate("TIRADS", "TIRADS 4"))
        self.pred_5.setText(self._translate("TIRADS", "TIRADS 5"))


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)    
    ui = Ui_TIRADS()
    sys.exit(app.exec_())





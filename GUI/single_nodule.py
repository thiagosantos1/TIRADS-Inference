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
import application as app
'''

Right mid thyroid solid greater than cystic nodule measures 1.3 x 1.2 x 1.2 cm. Mildly hypoechoic. Partial spongiform appearance. Well-defined. Slightly wider than tall.

'''

class TIRADS_Single(object):

    def setupUi(self, TIRADS_Single):
        self.my_obj = TIRADS_Single
        self.my_obj.setObjectName("TIRADS")
        self.my_obj.setFixedSize(761, 454)
        self.centralwidget = QtWidgets.QWidget(self.my_obj)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(0, 0, 761, 51))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.mult = QtWidgets.QPushButton(self.frame)
        self.mult.setGeometry(QtCore.QRect(210, 10, 113, 32))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.mult.setFont(font)
        self.mult.setObjectName("mult")
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

        self.my_obj.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self.my_obj)
        self.statusbar.setObjectName("statusbar")
        self.my_obj.setStatusBar(self.statusbar)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self.my_obj)

        # progresse bar
        self.progress = QtWidgets.QProgressBar(self.my_obj)# QtWidgets.QProgressBar(self)
        self.progress.setGeometry(360,250,200,50)

        QtWidgets.QApplication.processEvents() 
        # by default, TIRADS is selected - Let's choose by changing color to blue
        self.model_target = "tirads"
        #self.tirads.setStyleSheet( "background-color :  rgb(0, 176, 255)") 
        # if click tirads:
        self.tirads.clicked.connect(self.tirads_clicked)


        # predict action
        self.predict.clicked.connect(self.predict_text)   


        # load mult nodule window
        self.mult.clicked.connect(self.load_mult)           

        #self.clean_buttons()


        self.model = Models()


        QtWidgets.QApplication.processEvents() 



    def retranslateUi(self):
        self._translate = QtCore.QCoreApplication.translate
        self.my_obj.setWindowTitle(self._translate("TIRADS", "TI-RADS Classifier"))
        self.mult.setText(self._translate("TIRADS", "Load File"))
        self.tirads.setText(self._translate("TIRADS", "Single Nodule"))
        self.label.setText(self._translate("TIRADS", "Nodule Description"))
        self.predict.setText(self._translate("TIRADS", "Predict Score"))
        self.pred_1.setText(self._translate("TIRADS", "TI-RADS 1"))
        self.pred_2.setText(self._translate("TIRADS", "TI-RADS 2"))
        self.pred_3.setText(self._translate("TIRADS", "TI-RADS 3"))
        self.pred_4.setText(self._translate("TIRADS", "TI-RADS 4"))
        self.pred_5.setText(self._translate("TIRADS", "TI-RADS 5"))


    def load_mult(self):
        
        self.window = QtWidgets.QMainWindow()
        self.ui = app.Ui_TIRADS()
        self.ui.setupUi(self.window)
        self.window.show()
        self.my_obj.close()
        self.ui.load_preprocess()


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
        # self.tirads.setStyleSheet( "background-color :  rgb(0, 176, 255)") 
        # self.ata.setStyleSheet( "background-color :  rgb( 242, 250, 254 )") 
        self.model_target = "tirads"

        # change labels to tirads
        self.clean_buttons()

        self.pred_1.setGeometry(QtCore.QRect(610, 120, 113, 32))
        self.pred_1.setText(self._translate("TIRADS", "TI-RADS 1"))

        self.pred_2.setGeometry(QtCore.QRect(610, 180, 113, 32))
        self.pred_2.setText(self._translate("TIRADS", "TI-RADS 2"))

        self.pred_3.setGeometry(QtCore.QRect(610, 240, 113, 32))
        self.pred_3.setText(self._translate("TIRADS", "TI-RADS 3"))

        self.pred_4.setGeometry(QtCore.QRect(610, 300, 113, 32))
        self.pred_4.setText(self._translate("TIRADS", "TI-RADS 4"))

        self.pred_5.setGeometry(QtCore.QRect(610, 360, 113, 32))
        self.pred_5.setText(self._translate("TIRADS", "TI-RADS 5"))
        
    


if __name__ == "__main__":
    print("\n\t ### Please run file application.py ###\n")
    exit()

    app = QtWidgets.QApplication(sys.argv)
    TIRADS_Signle = QtWidgets.QMainWindow()
    ui = TIRADS_Single()
    ui.setupUi(TIRADS_Signle)
    TIRADS_Signle.show()
    sys.exit(app.exec_())





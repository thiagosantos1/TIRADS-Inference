'''
    Author: Thiago Santos - 02/22/2021

    A BERT GUI application to predict TIRADS nodule category

    pyuic5 -x -o application.py application.ui

'''


from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import time
sys.path.append('../') # add files from previous folder
from main import *
import single_nodule as sn

class Ui_TIRADS(object):
    def setupUi(self, TIRADS):
        self.my_obj = TIRADS
        self.my_obj.setObjectName("TIRADS")
        self.my_obj.setFixedSize(1295, 561)
        self.centralwidget = QtWidgets.QWidget(self.my_obj)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(0, 0, 1301, 51))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.load_tr = QtWidgets.QPushButton(self.frame)
        self.load_tr.setGeometry(QtCore.QRect(490, 10, 131, 32))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.load_tr.setFont(font)
        self.load_tr.setObjectName("load_tr")
        self.single_tr = QtWidgets.QPushButton(self.frame)
        self.single_tr.setGeometry(QtCore.QRect(770, 10, 113, 32))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.single_tr.setFont(font)
        self.single_tr.setObjectName("single_tr")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(1040, 80, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")

        self.predict = QtWidgets.QPushButton(self.centralwidget)
        self.predict.setEnabled(True)
        self.predict.setGeometry(QtCore.QRect(705, 230, 113, 32))
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(False)
        font.setWeight(50)
        self.predict.setFont(font)
        self.predict.setCheckable(False)
        self.predict.setAutoDefault(False)
        self.predict.setFlat(False)
        self.predict.setObjectName("predict")

        self.save_res = QtWidgets.QPushButton(self.centralwidget)
        self.save_res.setEnabled(True)
        self.save_res.setGeometry(QtCore.QRect(705, 330, 113, 32))
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(False)
        font.setWeight(50)
        self.save_res.setFont(font)
        self.save_res.setCheckable(False)
        self.save_res.setAutoDefault(False)
        self.save_res.setFlat(False)
        self.save_res.setObjectName("save_res")

        self.save_nodules = QtWidgets.QPushButton(self.centralwidget)
        self.save_nodules.setEnabled(True)
        self.save_nodules.setGeometry(QtCore.QRect(705, 420, 113, 32))
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(False)
        font.setWeight(50)
        self.save_nodules.setFont(font)
        self.save_nodules.setCheckable(False)
        self.save_nodules.setAutoDefault(False)
        self.save_nodules.setFlat(False)
        self.save_nodules.setObjectName("save_nodules")


        self.table_tr = QtWidgets.QTableWidget(self.centralwidget)
        self.table_tr.setGeometry(QtCore.QRect(0, 110, 691, 421))
        self.table_tr.setObjectName("table_tr")
        self.table_tr.setColumnCount(4)
        self.table_tr.setRowCount(0)

        item = QtWidgets.QTableWidgetItem()
        self.table_tr.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_tr.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_tr.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_tr.setHorizontalHeaderItem(3, item)
        self.table_tr.setColumnWidth(0,190)
        self.table_tr.setColumnWidth(1,300)
        self.table_tr.setColumnWidth(2,85)

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(230, 80, 141, 21))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.results_tr = QtWidgets.QListWidget(self.centralwidget)
        self.results_tr.setGeometry(QtCore.QRect(830, 110, 461, 421))
        self.results_tr.setObjectName("results_tr")
        self.my_obj.setCentralWidget(self.centralwidget)

        self.statusbar = QtWidgets.QStatusBar(self.my_obj)
        self.statusbar.setObjectName("statusbar")
        self.my_obj.setStatusBar(self.statusbar)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self.my_obj)

        # Our code goes after this point

        self.y = []
        self.predictions = []

        # progress bar
        self.progress = QtWidgets.QProgressBar(self.my_obj)
        self.progress.setGeometry(700,260,125,50)

        # progess bar for loading data
        self.progress_data = QtWidgets.QProgressBar(self.my_obj)
        self.progress_data.setGeometry(110,290,500,50)
        self.progress_data.setVisible(False)

        # progess bar for loading single nodule window
        self.progress_window = QtWidgets.QProgressBar(self.my_obj)
        self.progress_window.setGeometry(360,200,700,50)
        self.progress_window.setVisible(False)

        # if click tirads:
        self.load_tr.clicked.connect(self.load_preprocess)

        # predict action
        self.predict.clicked.connect(self.predict_data)  

        # save results
        self.save_res.clicked.connect(self.save_results)  

        # save nodules
        self.save_nodules.clicked.connect(self.save_rep_nod)  

        # load single nodule window
        self.single_tr.clicked.connect(self.load_single)
        

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.my_obj.setWindowTitle(_translate("TIRADS", "TIRADS Classifier"))
        self.load_tr.setText(_translate("TIRADS", "Load File"))
        self.single_tr.setText(_translate("TIRADS", "Single Nodule"))
        self.label.setText(_translate("TIRADS", "Results"))
        self.predict.setText(_translate("TIRADS", "Predict Score"))
        item = self.table_tr.horizontalHeaderItem(0)
        item.setText(_translate("TIRADS", "Report"))
        item = self.table_tr.horizontalHeaderItem(1)
        item.setText(_translate("TIRADS", "Nodule"))
        item = self.table_tr.horizontalHeaderItem(2)
        item.setText(_translate("TIRADS", "Category"))
        item = self.table_tr.horizontalHeaderItem(3)
        item.setText(_translate("TIRADS", "Prediction"))
        self.label_2.setText(_translate("TIRADS", "Nodules Extracted"))
        self.save_res.setText(_translate("TIRADS", "Save Results"))
        self.save_nodules.setText(_translate("TIRADS", "Save Nodules"))


    def data_progress(self, bar, start=0, end=85, reset=True):
        bar.setVisible(True)
        completed = start
        while completed < end:
            QtWidgets.QApplication.processEvents() 
            completed += 0.001
            bar.setValue(completed)
        if reset:
            bar.setValue(0)

    def load_single(self):
        
        self.data_progress(self.progress_window, reset=False)

        self.window = QtWidgets.QMainWindow()
        self.ui = sn.TIRADS_Single()
        self.ui.setupUi(self.window)

        self.data_progress(self.progress_window, start=85, end=100, reset=False)
        self.window.show()
        self.my_obj.close()

    def load_preprocess(self):

        self.table_tr.setRowCount(0)

        file_path = QtWidgets.QFileDialog.getOpenFileName(self.my_obj, 'Open TI-RADS File', '.')[0]
        if len(file_path) <1:
            return

        file_type = file_path.split(".")[1]

        if file_type =='csv':
            self.data_progress(self.progress_data)
            data = pd.read_csv(file_path)
        elif file_type =='xlsx' or file_type =='xls':
            self.data_progress(self.progress_data)
            data = pd.read_excel(file_path)
        else:
            error = QtWidgets.QErrorMessage(self.my_obj)
            error.setWindowTitle("Wrong data Input")
            error.showMessage("Input must be a csv or xlsx file")
            return

        column = 'report'
        output_file = "../data/results.txt"

        if column not in data:
            error = QtWidgets.QErrorMessage(self.my_obj)
            error.setWindowTitle("Wrong column Input")
            error.showMessage("Use a column name \'report\' for describing the nodules")
            return

        self.tr_model = TIRADS_Model(results_out=output_file, path_models="../")

        
        self.nodule_data = extract_nodules(data,demographic=False,search_findings=True, column_text=column,
                                        out = "../data/TIRADS_nodules.xlsx")

        self.X, self.y, self.id_orig_txt,self.origX,_,_,_,_  = preprocess_data(data=self.nodule_data, steam=True, remove_noise=True, 
                                           lemma=True, id_report=True,data_column = "Nodule Text", 
                                           score_column= 'TIRADS Score',remove_reports=[],clean=False,
                                           remove_struct_reports=True)


        # Fill the table with the report and segmentation
        self.data_progress(self.progress_data,start=85, end=100)
        self.progress_data.setVisible(False)
        self.table_tr.setRowCount(len(self.y))
        for index, nodule in enumerate(self.origX):
            report = self.id_orig_txt[index][1]
            label = self.y[index]
            self.table_tr.setItem(index,0,QtWidgets.QTableWidgetItem(report))
            self.table_tr.setItem(index,1,QtWidgets.QTableWidgetItem(nodule))
            self.table_tr.setItem(index,2,QtWidgets.QTableWidgetItem(str(label)))
            #self.table_tr.resizeRowsToContents()


        X_sentences = []
        for x in (self.X):
            out = ""
            out = ' '.join(map(str, x)) 
            X_sentences.append(out)

        self.X_sentences = np.asarray(X_sentences)
        self.y = np.array(self.y) -1 # labels 0 -->1, 4 --> 5, etc

        self.test_data = pd.DataFrame(list(zip(self.X_sentences, self.y)), 
                                columns =['report', 'labels']) 

        if self.test_data.shape[0] <1:
            error = QtWidgets.QErrorMessage(self.my_obj)
            error.setWindowTitle("No Semi-Structured data")
            error.showMessage("No Semi-Structured data available for testing after cleaning pre-process")
            return


    def predict_data(self):
        if len(self.y) <1:
            error = QtWidgets.QErrorMessage(self.my_obj)
            error.setWindowTitle("Load Data")
            error.showMessage("Please load datafile")
            return

        self.data_progress(self.progress,end=80)

        self.predictions = self.tr_model.model.predict(self.test_data['report'])[0]
        
        labels = ['TIRADS 1', 'TIRADS 2', 'TIRADS 3', 'TIRADS 4', 'TIRADS 5']

        cm= confusion_matrix(self.test_data['labels'], self.predictions )

        f1_macro = f1_score(self.test_data['labels'].to_numpy(), self.predictions, average='macro')

        f1_micro = f1_score(self.test_data['labels'].to_numpy(), self.predictions, average='micro')

        f1_wght = f1_score(self.test_data['labels'].to_numpy(), self.predictions, average='weighted')

        acc = accuracy_score(self.test_data['labels'].to_numpy(), self.predictions)

        cr = classification_report(self.test_data['labels'].values.tolist(), self.predictions, target_names=labels)
        
        output_file = self.tr_model.results_out 
        
        
        s = ('\t\t###### Original Results ######\n'
            '\nAccuracy : {}\n' 
            'F1 Macro : {}\n' 
            'F1 Micro : {}\n' 
            'F1 Weighted : {}\n' 
            '\n\tConfusion Matrix\n{}\n'
            '\nTrue Label:\n {}\n'
            '\nPrediction :\n {}\n\n' 
            '\t\tClassification Report per Score\n' 
            '{}\n' 
            '##################################################################################################\n\n'
            )
        self.output_pred = s.format(acc,f1_macro,f1_micro, f1_wght, cm,self.test_data['labels'].to_numpy().tolist(),self.predictions.tolist(),cr)

        y_true,y_pred = self.tr_model.margin_pred(cm)
        cm= confusion_matrix(y_true, y_pred )

        f1_macro = f1_score(y_true, y_pred, average='macro')

        f1_micro = f1_score(y_true, y_pred, average='micro')

        f1_wght = f1_score(y_true, y_pred, average='weighted')

        acc = accuracy_score(y_true, y_pred)

        cr = classification_report(y_true, y_pred, target_names=labels)

        output_file = self.tr_model.results_out 
        
        
        s = ('\t\t###### 1 Margin neighbor Results ######\n'
            '\nAccuracy : {}\n' 
            'F1 Macro : {}\n' 
            'F1 Micro : {}\n' 
            'F1 Weighted : {}\n' 
            '\n\tConfusion Matrix\n{}\n'
            '\t\tClassification Report per Score\n' 
            '{}\n' 
            )
        self.output_1margin = s.format(acc,f1_macro,f1_micro, f1_wght, cm,cr)
        

        self.data_progress(self.progress,start=80, end=100)

        # populate table with predictions
        for index, pred in enumerate(self.predictions):
            self.table_tr.setItem(index,3,QtWidgets.QTableWidgetItem(str(pred+1)))

        # populate view with results    
        QtWidgets.QListWidgetItem(self.output_pred, self.results_tr) 
        QtWidgets.QListWidgetItem("\n", self.results_tr) 
        QtWidgets.QListWidgetItem(self.output_1margin, self.results_tr)

        QtWidgets.QApplication.processEvents() 
        self.table_tr.viewport().update()

    def save_results(self):

        if len(self.y) <1:
            error = QtWidgets.QErrorMessage(self.my_obj)
            error.setWindowTitle("Load Data")
            error.showMessage("Please load datafile")
            return

        if len(self.predictions) <1:
            error = QtWidgets.QErrorMessage(self.my_obj)
            error.setWindowTitle("Make Prediction")
            error.showMessage("Please, make sure to make the predictions first")
            return

        file_path = QtWidgets.QFileDialog.getSaveFileName(self.my_obj, 'Open TI-RADS Results File', '.')[0]

        if len(file_path) <1:
            return

        file_path = file_path.split(".")[0] + ".txt"

        with open(file_path, 'w') as f:
            f.write(self.output_pred)
            f.write(self.output_1margin)


    def save_rep_nod(self):
        if len(self.y) <1:
            error = QtWidgets.QErrorMessage(self.my_obj)
            error.setWindowTitle("Load Data")
            error.showMessage("Please load datafile")
            return

        file_path = QtWidgets.QFileDialog.getSaveFileName(self.my_obj, 'Open TI-RADS Nodule File', '.')[0]

        if len(file_path) <1:
            return

        file_path = file_path.split(".")[0] + ".xlsx"
        self.nodule_data.to_excel(file_path)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    TIRADS = QtWidgets.QMainWindow()
    ui = Ui_TIRADS()
    ui.setupUi(TIRADS)
    TIRADS.show()
    sys.exit(app.exec_())






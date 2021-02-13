'''
    Author: Thiago Santos
    Class to hold models to be used on GUI application

'''
import sys
sys.path.append('../')

import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, classification_report
from simpletransformers.classification import ClassificationModel
from extract_tirads import clean_section
from text_cleaning import text_cleaning
from scipy.special import softmax
import tensorflow as tf
from textualheatmap import *
import torch
from transformers import BertTokenizer


class Models:
    def __init__(self, path_models="../", model_emb = 'bert', num_classes=5,
                    steam=True, remove_noise = True):

        self.path_models = path_models

        self.ata_path = path_models  + "BERT"
        self.tr_path  = path_models  + "BERT"

        self.num_classes = num_classes
        self.model_emb = model_emb
        self.steam=steam 
        self.remove_noise = remove_noise

        self.load_models()

    def load_models(self):
        args = {
        'eval_batch_size': 32,'silent':True
        }
        #self.ata_model = ClassificationModel(self.model_emb, self.ata_path,num_labels=self.num_classes, args=args,use_cuda=False)
        self.tr_model = ClassificationModel(self.model_emb, self.tr_path,num_labels=self.num_classes, args=args,use_cuda=False)


    def predict(self, text, model_type="tirads"):
        clean_txt = text_cleaning(clean_section(text), steam=self.steam, remove_noise=self.remove_noise)
        clean_txt = " ".join(clean_txt)
        self.df_to_pred = pd.DataFrame(list(zip([clean_txt])), 
                columns =['report']) 

        if model_type =="tirads":
            model = self.tr_model
        else:
            model = self.ata_model

        self.prediction, self.raw_prediction = model.predict(self.df_to_pred['report'])

        if model_type =="tirads":
            self.raw_prediction = self.raw_prediction[0][0]
        else:
            self.raw_prediction= self.raw_prediction[0]

        self.prediction = self.prediction[0] +1

        self.best_pred = np.argsort(self.raw_prediction)[-1:-4:-1] # get last 3

        self.pred_sorted = np.flip(np.argsort(self.raw_prediction))

        self.pred_probabilities = np.array([softmax(self.raw_prediction)])



if __name__ == '__main__':
    examples = [ ["Right mid thyroid solid greater than cystic nodule measures 1.3 x 1.2 x 1.2 cm. Mildly hypoechoic. "+
                  "Partial spongiform appearance. Well-defined. Slightly wider than tall.",3], 

                ["Right mid thyroid solid greater than cystic nodule measures 1.3 x 1.2 x 1.2 cm. "+
                 "Mildly hypoechoic. Partial spongiform appearance. Well-defined. Slightly wider "+
                 "than tall.",3],
                ["Anterior middle right thyroid, measuring 0.3 x 0.2 x 0.3 cm " +
                 "(previously measures 0.6 x 0.3 x 0.5, with decreased appreciation of solid "+
                 "component) which is almost entirely cystic and macrocalcifications", 1] ]

    m = Models()

    path_data = "/Users/thiago/Github/Data/TIRADS/data/"
    data_name = "TIRADS_nodules.xlsx"
    from extract_data import preprocess_data
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import confusion_matrix
    from sklearn.metrics import f1_score
    findings, y, id_txt, _, _, _, _ = preprocess_data(file=path_data + data_name, 
                                  bigrams=False, steam=True, remove_noise=True, id_report=True,
                                  data_column = "Nodule Text", score_column= 'TIRADS Score', demographic=False)


    y = np.array(y) -1
    X_findings = []
    print("\tTransform data into flat 1 dimension")
    for x in (findings):
        text = ""
        text = ' '.join(map(str, x)) 
        X_findings.append(text)


    X_find_train, X_find_test, y_train, y_test = train_test_split(X_findings, y,test_size=0.2,random_state=0)

    df_test = pd.DataFrame(list(zip(X_find_test, y_test)), 
                                        columns =['report', 'labels']) 
    predictions = m.tr_model.predict(df_test['report'])[0]
    cm= confusion_matrix(df_test['labels'], predictions )

    f1_macro = f1_score(df_test['labels'].to_numpy(), predictions, average='macro')

    f1_micro = f1_score(df_test['labels'].to_numpy(), predictions, average='micro')

    f1_wght = f1_score(df_test['labels'].to_numpy(), predictions, average='weighted')

    acc = accuracy_score(df_test['labels'].to_numpy(), predictions)

    print(f1_macro,f1_micro,f1_wght,acc)
    print(cm)
'''
Right mid thyroid solid greater than cystic nodule measures 1.3 x 1.2 x 1.2 cm. Mildly hypoechoic.Partial spongiform appearance. Well-defined. Slightly wider than tall.

'''









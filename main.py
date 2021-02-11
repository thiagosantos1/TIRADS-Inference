
'''
    Author: Thiago Santos - 03-02-2021
    This is the main class to execute TI-RADS score prediction - No usage of demografic information
    Usage:
    python3 main.py inputfile.csv column_name output_results.csv
    where:
            * inputfile: full path to a file that contains all report data
            * column_name: must be the column that has the report data
            * output_results: full path to a file to save the results and statistics

'''
import sys

import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, classification_report,confusion_matrix
from sklearn.metrics import f1_score,precision_recall_curve, average_precision_score

from simpletransformers.classification import ClassificationModel
from extract_tirads import clean_section
from text_cleaning import text_cleaning
from scipy.special import softmax
from extract_data import preprocess_data
from extract_tirads import extract_nodules


class TIRADS:
    def __init__(self, path_models="./", model_emb = 'bert', num_classes=5, results_out="results.txt"):

        self.path_models = path_models

        self.tr_path  = path_models + "BERT"

        self.num_classes = num_classes
        self.model_emb = model_emb
        self.results_out = results_out

        self.load_models()

    def load_models(self):
        args = {
        'eval_batch_size': 32,'silent':True
        }
        self.model = ClassificationModel(self.model_emb, self.tr_path,num_labels=self.num_classes, args=args,use_cuda=False)


    def margin_pred(self,cm,margin=True):
        y_true = []
        y_pred = []
        min_ind, max_ind = 0,0
        for index,d in enumerate(cm):
            num_label = np.sum(d)
            x = [index for i in range(num_label)]
            y_true = y_true +x
            label_correct = d[index]
            if margin:
                min_ind = max(0, index -1)
                max_ind = min(len(d)-1, index +1 )+1
                label_correct = np.sum(d[min_ind:max_ind])

            wrong = num_label - label_correct
            y_wrong = []
    
            # get wrong
            if wrong >0:
                for index_d,x in enumerate(d):
                    if index != index_d:
                        if margin ==True and (min_ind == index_d or max_ind-1 == index_d):
                            continue
                        if x != 0:
                            w_l = [index_d for i in range(x)]
                            y_wrong += w_l

            y_correct = [index for i in range(label_correct)]

            y_pred = y_pred + y_correct + y_wrong

        return y_true,y_pred


    def test(self,test_data, save_results=True, margin_results=True):
        print("\n\tEvaluating model for test data of size: ", test_data.shape[0])
        #results, model_outputs, wrong_predictions = self.model.eval_model(test_data, f1=self.f1_multiclass, acc=accuracy_score)

        print("\n\tPredicting.......")
        predictions = self.model.predict(test_data['report'])[0]

        #print("\tResults\n\n", results)

        # print("\n\t##### Wrong predictions #####")
        # for index,x in enumerate(wrong_predictions):
        #   print("ID: \t",x.guid,"\tText: ", x.text_a, "\tLabel: ", x.label , "predict: ", predictions[x.guid])

        
        labels = ['TIRADS 1', 'TIRADS 2', 'TIRADS 3', 'TIRADS 4', 'TIRADS 5']


        print("\n\tSaving predictions and statistics")

        cm= confusion_matrix(test_data['labels'], predictions )

        f1_macro = f1_score(test_data['labels'].to_numpy(), predictions, average='macro')

        f1_micro = f1_score(test_data['labels'].to_numpy(), predictions, average='micro')

        f1_wght = f1_score(test_data['labels'].to_numpy(), predictions, average='weighted')

        acc = accuracy_score(test_data['labels'].to_numpy(), predictions)

        cr = classification_report(test_data['labels'].values.tolist(), predictions, target_names=labels)

        
        if save_results:
            output_file = self.results_out 
            
            with open(output_file, 'w') as f:
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
              output_string = s.format(acc,f1_macro,f1_micro, f1_wght, cm,test_data['labels'].to_numpy().tolist(),predictions.tolist(),cr)
            

              f.write(output_string)


        if margin_results:
            print("\n\tSaving predictions and statistics with 1-margin neighbor")

            y_true,y_pred = self.margin_pred(cm)
            cm= confusion_matrix(y_true, y_pred )

            f1_macro = f1_score(y_true, y_pred, average='macro')

            f1_micro = f1_score(y_true, y_pred, average='micro')

            f1_wght = f1_score(y_true, y_pred, average='weighted')

            acc = accuracy_score(y_true, y_pred)

            cr = classification_report(y_true, y_pred, target_names=labels)

            output_file = self.results_out 
            
            with open(output_file, 'a') as f:
              s = ('\t\t###### 1 Margin neighbor Results ######\n'
                  '\nAccuracy : {}\n' 
                  'F1 Macro : {}\n' 
                  'F1 Micro : {}\n' 
                  'F1 Weighted : {}\n' 
                  '\n\tConfusion Matrix\n{}\n'
                  '\t\tClassification Report per Score\n' 
                  '{}\n' 
                  )
              output_string = s.format(acc,f1_macro,f1_micro, f1_wght, cm,cr)
            

              f.write(output_string)

        
           

if __name__ == '__main__':

    if len(sys.argv) < 4:
        print("Please provide <inputfile>, <text_column_name>, <output_file> \n")
        sys.exit(1)

    input_file = sys.argv[1]
    column = sys.argv[2]
    output_file = sys.argv[3]

    model = TIRADS(results_out=output_file)

    data = pd.read_csv(input_file)
    nodule_data = extract_nodules(data,demographic=False,search_findings=True, column_text=column)

    X, y, _,_,_,_,_  = preprocess_data(data=nodule_data, steam=True, remove_noise=True, 
                                       lemma=True, id_report=False,data_column = "Nodule Text", 
                                       score_column= 'TIRADS Score',remove_reports=[],clean=False,
                                       remove_struct_reports=False)

    X_sentences = []
    all_data = [word for report in X for word in report]
    for x in (X):
        out = ""
        out = ' '.join(map(str, x)) 
        X_sentences.append(out)

    X_sentences = np.asarray(X_sentences)
    y = np.array(y) -1 # labels 0 -->1, 4 --> 5, etc

    df_test = pd.DataFrame(list(zip(X_sentences, y)), 
                            columns =['report', 'labels']) 

    model.test(df_test)
    



    
'''
  Based on the giving data and read nodules
  Return clean data and label
'''

import re
import pickle
import pandas as pd
from itertools import chain
import numpy as np
import matplotlib.pyplot as plt
from text_cleaning import text_cleaning
from extract_tirads import clean_section



def extract_nodule_data(data, data_column="Nodule Text", score_column ='TIRADS Score', lemma=True,
                        scores_=True, clean_text=True, remove_reports=[], remove_struct_reports = False,
                        steam=True,remove_noise=False, min_size_X = 3, id_report = True, demographic = False,clean=True):
  print("\tExtracting and cleaning data from nodule")
  X, y, id_txt = [], [], []
  print("\n\tData original size: ", data.shape[0])
  id_nodules = []
  race, gender, age, clinical = [], [], [], []

  for i in range(data.shape[0]):
    if i >=0:

      txt = data.iloc[i][data_column]
      id_ = data.iloc[i]["ID Report"]

      if id_ not in remove_reports: 

        # print("\n\n", txt, "\n\n")
        # do not add struct reports, if set so
        if remove_struct_reports and  (re.search("\\(\\d\\)", txt) or re.search("nodule #\\d", txt)):
          continue

        if clean_text:
          if re.search("\\(\\d\\)",clean_section(txt)) is not None: 
            id_nodules.append(id_)

          clean_txt = text_cleaning(clean_section(txt), steam=steam,lemma=lemma, remove_noise=remove_noise,clean=clean)
          size_txt = len(clean_txt)
          if size_txt >= min_size_X:
            X.append(clean_txt)
            if scores_:
              y.append(int( data.iloc[i][score_column])) # only get the max score of the report
            if id_report:
              original_txt = data.iloc[i]["Original Radiology Text"]
              id_txt.append([id_,original_txt])

            if demographic:
              not_alloed = ['african', 'american', 'caucasian', 'unavailable', 'unreported',
                            'unrepo', 'ed']
              r = data.iloc[i]["Race"]
              r = text_cleaning(clean_section(r), steam=False, remove_noise=remove_noise)
              r = " ".join(r)
              r = re.sub("multiple", "black", r).split()
              r = [x for x in r if x not in not_alloed]


              g = data.iloc[i]["Gender"]
              g = text_cleaning(clean_section(g), steam=False, remove_noise=remove_noise)

   
              age.append(data.iloc[i]["Patient Age at Visit"])

              c = data.iloc[i]["Clinical Indication"]
              c = text_cleaning(clean_section(c), steam=False, remove_noise=remove_noise)
              
              race.append(r[0])
              gender.append(g[0])
              clinical.append(c)

        else:
          if len(txt.split()) >= min_size_X:
            X.append(txt)
            if scores_:
              y.append(int( data.iloc[i][score_column])) # only get the max score of the report

  print("\n\tCleaned data size: ", len(X))
  # id_nodules = set(id_nodules)
  # print(sorted(id_nodules))
  return X, y, id_txt, race, gender, age, clinical



def preprocess_data(scores_=True, clean_text=True, steam=False, 
                    remove_noise=False, data_column="Nodule Text", score_column ='TIRADS Score', 
                    id_report=False, remove_reports = [], demographic=False,remove_struct_reports=False,
                    clean=True,lemma=False,
                    data=[]):

  X, y,id_txt, race, gender, age, clinical = extract_nodule_data(data, scores_=scores_, clean_text=clean_text, steam=steam, 
                                  remove_reports=remove_reports, id_report = id_report, 
                                  remove_noise=remove_noise, data_column=data_column, 
                                  score_column =score_column, demographic = demographic,lemma=lemma,
                                  remove_struct_reports=remove_struct_reports,clean=clean)
  

  #print(X)
  return X, y, id_txt, race, gender, age, clinical

if __name__ == '__main__':
  pass
  
  





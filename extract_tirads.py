'''
  TIRADS segmentation
  From full data, extract TIRADS data and label
  and save to another file
'''

import re
import pickle
import pandas as pd
from itertools import chain
import numpy as np
import matplotlib.pyplot as plt
from statistics import stdev 
from statistics import variance
from nltk.tokenize import sent_tokenize
from text_cleaning import text_cleaning
# import nltk
# nltk.download('punkt')

# get tirads scores from giving report/section
def get_codes(txt):
  #print("\nbefore", txt)
  txt = txt.lower()
  txt = re.sub("-", "", txt)
  txt = re.sub("category", "", txt)
  txt = re.sub("would be", "", txt)
  txt = re.sub(' +', ' ', txt)
  txt = re.sub('\n+', ' ', txt)
  #print("After\n",txt)
  tr_1 = re.findall("tr \\d+", txt)
  tr_2 = re.findall("tr\\d+", txt)
  tr_3 = re.findall("tr:\\d+", txt)
  tr_4 = re.findall("tr: \\d+", txt)

  tr_5 = re.findall("tirads \\d+", txt)
  tr_6 = re.findall("tirads\\d+", txt) 
  tr_7 = re.findall("tirads:\\d+", txt) 
  tr_8 = re.findall("tirads: \\d+", txt)  

  tirads = list(chain(tr_1,tr_2,tr_3,tr_4,tr_5,tr_6,tr_7,tr_8))
  return tirads


# extract nodule data, per section, as an individual data
def extract_nodules(data, out = "data/TIRADS_nodules.xlsx", demographic=True,
                    search_findings = True, column_text='report'):
  pd.set_option('mode.chained_assignment', None)

  X = np.array([])
  y = np.array([]).astype(int)
  report_id = np.array([]).astype(int)
  original_text = np.array([])
  race_vector = np.array([])
  gender_vector = np.array([])
  age_vector = np.array([])
  clinical_indication_vector = np.array([])
  id_=0
  for i in range(data.shape[0]):
    if i >=0: # for test pourpouse --> 13, 95(more than 1 line), 363, 23, 29, 32, 58, 69, 275, 262
      #print(i)
     
      if demographic:
        race = data.iloc[i]['Race']
        gender = data.iloc[i]['Gender']
        age = data.iloc[i]['Patient Age at Visit']
      
      original_txt = data.iloc[i][column_text]
      if re.search("FINDINGS:", original_txt) or not  search_findings:

        if search_findings:
          txt = original_txt.split("FINDINGS:")[1].lower()
          if re.search("FINDINGS:", original_txt) and re.search("IMPRESSION:", original_txt) :
            txt = original_txt.split("FINDINGS:")[1].split("IMPRESSION:")[0].lower()
        else:
          txt = original_txt

        if demographic:
          clinical_indication = " ".join(original_txt.lower().split("clinical indication:")[1:]).split("\n\n")[0].strip() 

        txt = re.sub(r'(total:)( +)(\d+)( +)(point\w+)', r'total TIRADS \3', txt)
        txt = re.sub(r'(total)( +)(points:)( +)(\d+)', r'total TIRADS \5', txt)
        
        txt = re.sub('tirads:0', 'tirads:1', txt)

        txt = re.sub(r'(nodule)( +)(\d+)', r'nodule #\3', txt)
        
        # get text either from Findinngs or Impression
        tirads = get_codes(txt)
        num_nodes = len(tirads)

        # get from impression as well. Later for now
        # if num_nodes <= 0: # scores my be inside of Impression then
        #   txt = data.iloc[i]['Radiology  Text']
        #   txt = txt.split("FINDINGS:")[1]
        #   tirads = get_codes(txt)
        #   num_nodes = len(tirads)
        
        if num_nodes > 0:
          # get text either from Findinngs or Impression
          X_section, y_section = extract_nodules_data(txt,num_nodes)
          X = np.append(X, X_section)
          y = np.append(y, y_section)
          report_id = np.concatenate( (report_id, np.tile([id_],(len(X_section))) ))
          original_text = np.concatenate( (original_text, np.tile([original_txt],(len(X_section))) ))
          id_+=1
            
          # demographic information
          if demographic:
            race_vector = np.concatenate( (race_vector, np.tile([race],(len(X_section))) ))
            gender_vector = np.concatenate( (gender_vector, np.tile([gender],(len(X_section))) ))
            age_vector = np.concatenate( (age_vector, np.tile([age],(len(X_section))) ))
            clinical_indication_vector = np.concatenate( (clinical_indication_vector, np.tile([clinical_indication],(len(X_section))) ))

  
  if demographic:
    new_data = pd.DataFrame(list(zip(report_id,race_vector,gender_vector ,age_vector,clinical_indication_vector,original_text, X, y)), 
                 columns =['ID Report', 'Race','Gender','Patient Age at Visit','Clinical Indication', 'Original Radiology Text', 'Nodule Text', 'TIRADS Score']) 
  else:
    new_data = pd.DataFrame(list(zip(report_id,original_text, X, y)), 
                 columns =['ID Report', 'Original Radiology Text', 'Nodule Text', 'TIRADS Score']) 
  
  save_data(new_data, out=out)
  return new_data
 
def struct_sentece(sentences):
  new_sentences = []

  for index, sentence in enumerate(sentences):
  
    # if both are in the same sentece, we should remove it
    if re.search("nodule #\\d",sentence) is not None and re.search("tirads:\\d",sentence) is not None:
      sentence_sub = re.sub("total +tirads:\\d", "",sentence)
      if re.search("tirads:\\d",sentence_sub) is not None:
        sentence = sentence_sub

      txt = sentence.split("nodule #")
      tirads_txt = re.split("(tirads:\\d)", sentence)
      # print(sentence,"\n\n")
      # print(txt, "\n\n")
      # print(tirads_txt, "\n\n")
      # exit()
      new_sentences.append(tirads_txt[0] + " " + tirads_txt[1] + " ") # do not add what comes after the score
      new_sentences.append("nodule #" + txt[1]) 
    else:
      if re.search("tirads:\\d",sentence) is not None:
        sentence_sub = re.sub("total +tirads:\\d", "",sentence)
        if re.search("tirads:\\d",sentence_sub) is not None:
          sentence = sentence_sub

        tirads_txt = re.split("(tirads:\\d)", sentence)
        # print("\n", sentence, "\n\n")
        # print(tirads_txt,"\n\n")
        # exit()
        new_sentences.append(tirads_txt[0] + " " + tirads_txt[1] + " ") # do not add what comes after the score
        new_sentences.append(tirads_txt[2])
      else:
        new_sentences.append(sentence)

  return new_sentences

def nodule_data(text_data, sentences, index):
  tirads = get_codes(sentences[index][0])
  tr_score = [min(int(re.findall("\\d+", x)[0]),5) for x in tirads]
  tr_score = [max(1,x) for x in tr_score]
  # if only the word TIRADS and no actually data is presented, then get previous 
  if len(text_data.split()) <4 and sentences.shape[0] >1: 
    if index >0 : # can't be the first sentence
      text_data = sentences[index -1][0] + " " + text_data + " "
    else: # if it happens on the first sentence, join with next then
      text_data +=  " " + sentences[index +1][0] + " "

  text_data = re.sub("tirads:\\d+", ' ', text_data) 
  text_data = re.sub("tirads:", ' ', text_data) 
  text_data = re.sub("tirads", ' ', text_data) 

  return text_data, tr_score

# for structured reports (nodule #1 .... nodule #2....., the data is better disegned)
def structure_nodule_data(text_data):
  tirads = get_codes(text_data)
  tr_score = [min(int(re.findall("\\d", x)[0]),5) for x in tirads]
  tr_score = [max(1,x) for x in tr_score]
  return tr_score

# giving the text, extract the data related to the keywords
def extract_nodules_data(report,num_nodes):

  X_section = np.array([])
  y_section = np.array([]).astype(int)
  
  # print(report,"\n\n")
  report = clean_section( report.lower() )

  nodule_used = 0
  data_parg = report.split("\n\n") # go by paragraph

  #if re.search("nodule #\\d",report) is not None: # if report has a per nodule structure (ex: id 188)
  start_nodule, start_sentence = False, False
  text_data = ""
  nodule,tr_score = 0, 0
  keys = [x for x in range(len(data_parg))]
  # Removed sentences in paragraphs --> happens when you combine current paragraph with next one
  removed_sentence_parag = {key: [] for key in keys} #dict(zip(keys, [[]]*len(keys)))

  for index_parag, paragraph in enumerate(data_parg):
    
    sentences = np.array((sent_tokenize(paragraph))) # fix the split of senteces that my have be wrong
    sentences = sentences.reshape(sentences.shape[0],1)
    #print(sentences,"\n\n")

    for index, sentence in enumerate(sentences):
      #print(sentence)
      if nodule < num_nodes and index not in removed_sentence_parag[index_parag]: 
        
        if re.search("nodule #\\d",sentence[0]) is not None: # different structure
          start_nodule = True
          text_data = sentence[0]
          if re.search("tirads:\\d",sentence[0]) is not None: # if the score is at that sentece, ends data
            text_data, tr_score = nodule_data(text_data, sentences, index)

            X_section = np.append(X_section, [text_data])
            y_section = np.append(y_section, tr_score[0])
            start_nodule = False
            text_data = ""
            nodule += 1
        else:
          if start_nodule:
            if re.search("tirads:\\d",sentence[0]) is not None: # if the score is at that sentece, ends data
              
              if re.search("total +tirads:\\d",sentence[0]) is not None:
                # if none below happens, then this will be the default
                text_data_sub = text_data + " " + sentence[0] + " "
                text_data_sub, tr_score_sub = nodule_data(text_data_sub, sentences, index)
                segmented = False
                if index +1 < len(sentences):
                  if re.search("tirads:\\d",sentences[index+1][0])is not None : # if tirads is giving on next sentence
                    sentence[0] = re.sub("total +tirads:\\d", "",sentence[0])
                    text_data_sub = text_data + " " + sentence[0] + " "
                    text_data_sub = text_data_sub + " " + sentences[index+1][0] + " "
                    tr_score_sub = structure_nodule_data(text_data_sub)
                    removed_sentence_parag[index_parag].append(index+1)
                    segmented = True
                
                if not segmented and index_parag+1 < len(data_parg):
                  sentences_next_parag = np.array(struct_sentece(sent_tokenize(data_parg[index_parag+1]))) # fix the split of senteces that my have be wrong
                  sentences_next_parag = sentences_next_parag.reshape(sentences_next_parag.shape[0],1)
                  if len(sentences_next_parag) >0:
                    if re.search("tirads:\\d",sentences_next_parag[0][0])is not None : 
                      removed_sentence_parag[index_parag+1].append(0)
                      sentence[0] = re.sub("total +tirads:\\d", "", sentence[0])
                      text_data_sub = text_data + " " + sentence[0] + " "
                      text_data_sub = text_data_sub + " " + sentences_next_parag[0][0] + " "
                      tr_score_sub = structure_nodule_data(text_data_sub)
                      removed_sentence_parag[index_parag].append(index+1)

                 
                text_data = text_data_sub
                tr_score = tr_score_sub

              else: # total tirads is not presented, means it's a normal case
                text_data = text_data + " " + sentence[0] + " "
                text_data, tr_score = nodule_data(text_data, sentences, index)

              
              X_section = np.append(X_section, [text_data])
              y_section = np.append(y_section, tr_score[0])
              start_nodule = False
              text_data = ""
              nodule += 1
            else:
              text_data = text_data + " " + sentence[0] + " "

          else: # if looking for a nodule not as nodule #
             # another approach is to get by the word measure
            if re.search("measure\\w+",sentence[0]) is not None: 
              text_data = sentence[0]
              start_sentence = True
            else:
              if start_sentence:
                text_data += " " + sentence[0] + " "
              else:
                text_data = sentence[0]

            # one approach --> # if the score is at that sentece, ends data
            if re.search("tirads:\\d",sentence[0]) is not None: 
              #print("\n\n",sentence[0],"\n\n")                 
              text_data, tr_score = nodule_data(text_data, sentences, index)
              start_sentence = False
              X_section = np.append(X_section, [text_data])
              y_section = np.append(y_section, tr_score[0])
              nodule += 1

    nodule_used = nodule

  return X_section, y_section
  


def clean_section(txt):
  # standarlize mentions of tirads to only one

  txt = re.sub("ti-rads:|ti-rads", "tirads:", txt)
  txt = re.sub("\\s+tr\\s+", "tirads:", txt)

  txt = re.sub("tr\\s+:", "tirads:", txt)
  txt = re.sub("tr\\s+", "tirads:", txt)
  txt = re.sub("tr-", "tirads:", txt)
  txt = re.sub("tr: +", "tirads:", txt)
  txt = re.sub("tr:", "tirads:", txt)
  txt = re.sub("tirads +", "tirads:", txt)
  txt = re.sub("tirads-", "tirads:", txt)
  txt = re.sub("tirads +", "tirads:", txt) 
  txt = re.sub("tirads: +", "tirads:", txt) 
  txt = re.sub("tirads:tirads:", "tirads:", txt) 
  txt = re.sub("tirads:tirads", "tirads:", txt) 
  txt = re.sub("tirads:category", "tirads:", txt) 
  txt = re.sub(r'(score of)(\d)', r'tirads:\2', txt) 
  txt = re.sub(r'(score of:)(\d)', r'tirads:\2', txt) 
  txt = re.sub(r'(score of +)(\d)', r'tirads:\2', txt) 
  txt = re.sub(r'(score of: +)(\d)', r'tirads:\2', txt) 
  txt = re.sub("score:", "tirads:", txt) 
  txt = re.sub(r'(tr)(\d)', r'tirads:\2', txt)

  

  # txt = re.sub("right:.+?.*cm", "", txt)
  # txt = re.sub("left:.+?.*cm", "", txt)
  # print(txt)
  # exit()

  txt = re.sub("nodules as described:", "", txt) 
  txt = re.sub("nodules:", "", txt) 
  txt = re.sub("nodules include as follows:", "", txt)
  txt = re.sub("-", " ", txt)


  txt = re.sub(r'([tirads])(\d+)', r'\1:\2', txt) # tirads3 --> tirads:3
  txt = re.sub(r'(tirads:)(\s+)', r'\1', txt) # tirads: 3 --> tirads:3
  txt = re.sub(": :", "", txt)
  txt = re.sub("::", ":", txt)

  # fix for nodule #
  txt = re.sub(r'(\s+)([#])(\s+)(\d+)', r' \2\4', txt) # nodule # 5 --> nodule #5:
  txt = re.sub(r'(\d)(\.)(\s+)(\d+)', r'nodule #\1: ', txt) # nodule: 1 --> nodule #1:
  txt = re.sub(r'(nodule)(\s+)(\d)(:)', r'\1 #\3: ', txt) # nodule: 1 --> nodule #1:
  
  # if structure has scores but not description, add it
  if re.search('(composition|echogenicity|shape|margin|echogenic foci)(: +)(\\d)', txt):
    txt = insert_desc(txt)


  # remove structure 
  # txt = re.sub("composition:", '', txt)
  # txt = re.sub("echogenicity:", '', txt)
  # txt = re.sub("shape:", '', txt)
  # txt = re.sub("margin:", '', txt)
  # txt = re.sub("echogenic foci:", '', txt) 

  # #txt = re.sub("nodule #", '', txt)
  # txt = re.sub("size:", '', txt)

  txt = re.sub("nomicrocalcifications", 'no microcalcifications', txt)

  txt = re.sub("isthmus: measures", " ", txt)

  # where we have number x number x number to represent measures but did not insert the word
  # make it easy to find later 
  p_ = '(\\d+\\.?\\d* +x +\\d+\\.?\\d* +x +\\d+\\.?\\d*)'
  p_2 = '(\\d+\\.?\\d* +x +\\d+\\.?\\d*)'

  txt = re.sub(p_, r'measures \1', txt)
  txt = re.sub(p_2, r'measures \1', txt)
  
  txt = re.sub("measure\\w+ +measures", "measures", txt)

  return txt


def get_descrip(struct, score):
  desc = ""
  if struct == "CM": # composition
    if score ==0:
      desc = "spongiform or cystic "
    if score ==1:
      desc = "mixed cystic and solid "
    if score ==2:
      desc = "solir or almost completely solid "

  if struct == "ECH": # Echogenicity
    if score ==0:
      desc = "anechonic "
    if score ==1:
      desc = "isoechoic "
    if score ==2:
      desc = "hypoechoic "
    if score ==3:
      desc = "very hypoechoic "

  if struct == "SH": # Shape
    if score ==0:
      desc = "wider than tall "
    if score ==3:
      desc = "taller than wide "

  if struct == "MA": # Margin
    if score ==0:
      desc = "smooth or ill defined "
    if score ==2:
      desc = "lobulated or irregular "
    if score ==3:
      desc = "extra thyrcidal extension "

  if struct == "ECH_FOCI": # Echogenicity Foci
    if score ==0:
      desc = "large comet tail artifacts "
    if score ==1:
      desc = "macrocalcifications "
    if score ==2:
      desc = "peripheral calcification "
    if score ==3:
      desc = "echogenic fod "

  return desc

def insert_desc(txt):
  struct = [ ["composition", "CM"], ["echogenicity", "ECH"], ["shape", "SH"], ["margin", "MA"], ["echogenic foci", "ECH_FOCI"]]

  for data in txt.split("\n\n"):
    # save time if not in this paragraph
    if re.search('(composition|echogenicity|shape|margin|echogenic foci)(: +)(\\d)', data):
      # print("\n\n",data)
      for s in struct:
        pattern = s[0] + ": +\\d+"
        if re.search(pattern, data ):
          #print("\n", re.findall(pattern,data))
          score = re.findall(pattern,data)[0].split(":")[1]
          #print(score)
          desc = get_descrip(s[1], int(score))
          #print(desc)
          txt = re.sub(pattern, desc, txt)

  return txt



def save_data(data, out = "TIRADS_Scores.xlsx", new_col=None):
  
  if new_col is not None:
    data = data.reindex(columns=new_col)

  data.to_excel(out)



if __name__ == '__main__':
  pass





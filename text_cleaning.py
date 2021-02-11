import pandas as pd
from gensim.parsing import preprocessing
from gensim.parsing.preprocessing import strip_tags, strip_punctuation,strip_numeric,remove_stopwords
from os import walk
from os import listdir
from os.path import isfile, join
import numpy as np
import re 
import pickle
from nltk.stem import PorterStemmer
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize

# remove zero scores from Nodule structure --> ACR TI-RADS
def remove_zeros_scores(txt):
  # remove all, one by one

  # composition
    # cystic option

  # margin
  re.findall("smooth .+?(?=\\(0\\))", txt)

def remove_noise_text(txt, remove_noise=False, convert_ACR=True):

  txt = txt.lower()
  txt = re.sub('pts', "", txt) 

  # convert ACR TIRADS Score to text only. Only the sub-category that has a number will be kept
  # According to strucutre, each subcategory would be in a different line
  # if re.search("nodule #\\d",txt) is not None: 
  #   sub = txt.split("\n")
  #   for sub_txt in sub:
  #     search = re.findall("\\(\\d\\)", sub_txt)
  #     if search is not None:
  #       numbers= [int(x[1]) for x in search]
  #       if len(numbers)>0:
  #         number_min = min(numbers)
  #         number_max = max(numbers)
  #         if number_max <1:
  #           return ""

  #         elif number_min <1:
  #           txt = remove_zeros_scores(txt)
            # print("\n########## BEFORE #########\n",txt,"\tNumber: ", number_min, "\n")
            # txt = re.sub(sub_txt, "", txt) 
            # print("\n",sub_txt)
            # print("\n########## After #########\n",txt,"\n")

  # txt = re.sub('\\d', "", txt)
  txt = re.sub('-{2,}', "", txt) # remove dashes
  txt = re.sub(' +', ' ', txt) # remove double+ spaces

  txt = re.sub("impression:", '', txt)
  #txt = re.sub("left", '', txt)
  #txt = re.sub( txt[txt.find("isthmus"):].split("\n")[0], "", txt)
  txt = re.sub("isthmus:", '', txt)
  txt = re.sub("nodules:", '', txt)
  txt = re.sub("nodule #\\d:", '', txt)
  txt = re.sub("measures:", '', txt)
  txt = re.sub("cm", 'centimeters', txt)
  txt = re.sub("measuring", '', txt)
  txt = re.sub("wet read", '', txt)
  #txt = re.sub("within", '', txt)
  txt = re.sub("mm", '', txt)
  #txt = re.sub("right", '', txt)
  txt = re.sub("gt", '', txt)
  txt = re.sub("fna", '', txt)
  txt = re.sub("ct", '', txt)
  txt = re.sub("ml", '', txt)
  txt = re.sub("patient", '', txt)
  #txt = re.sub("mid", '', txt)
  txt = re.sub("total points", '', txt)
  txt = re.sub("points", '', txt)
  txt = re.sub("total", '', txt)
  txt = re.sub("-", "", txt)

  # remove the score
  txt = re.sub("(tirads:)(\\d)( +nodule)", '', txt) 
  txt = re.sub("tirads:\\d", '', txt) 

  # remove tiradas from text
  txt = re.sub("tr ", '', txt)
  txt = re.sub("tr", '', txt)
  txt = re.sub("tr:", '', txt)
  txt = re.sub("tr: ", '', txt)
  txt = re.sub("tirads:", '', txt) 
  txt = re.sub("tirads: ", '', txt) 
  txt = re.sub("ti rads:", '', txt) 
  txt = re.sub("ti rads", '', txt) 
  txt = re.sub("tirads", '', txt)

  # remove structure 
  txt = re.sub("composition:", '', txt)
  txt = re.sub("echogenicity:", '', txt)
  txt = re.sub("shape:", '', txt)
  txt = re.sub("margin:", '', txt)
  txt = re.sub("echogenic foci:", '', txt) 

  txt = re.sub("taller", 'tall', txt) 
  txt = re.sub("solidly", 'solid', txt) 
  
  
  txt = re.sub("nodule #|total", '', txt)
  txt = re.sub("size:", '', txt)
  txt = re.sub("nomicrocalcifications", 'no microcalcifications', txt)
  txt = re.sub("measure\\w+ +measure\\w+", "measures", txt)
  txt = re.sub("measures measures", "measures", txt)

  # remove words consider noise to the text
  if remove_noise:
    txt = re.sub("measures|measure|previous|centimeter|centimeters", '', txt)
    txt = re.sub("follows|follow|right|left|please|note|ly", '', txt)
    # txt = re.sub("nodule|measures|measure|previous|nodule|nodules|centimeter|centimeters", '', txt)
    # txt = re.sub("follows|follow|right|left|none|please|note|ly", '', txt)
  
  txt = re.sub("\\|", ' ', txt)

  txt = re.sub("pt", ' ', txt)
  txt = re.sub("hx", ' ', txt)
  txt = re.sub("bx", ' ', txt)
  txt = re.sub("pet", ' ', txt)
  txt = re.sub("emr", ' ', txt)
  txt = re.sub("sx", ' ', txt)
  txt = re.sub("dr", ' ', txt)
  txt = re.sub("dx", ' ', txt)
  txt = re.sub("per", ' ', txt)
  txt = re.sub("us", ' ', txt)
  txt = re.sub("hy", ' ', txt)
  txt = re.sub("rt", ' ', txt)
  txt = re.sub("fl", ' ', txt)
  txt = re.sub("su", ' ', txt)
  
  return txt

def text_cleaning(txt, steam=True, lemma = True, remove_noise=False,clean=True):
  # print("Before: ",txt,"\n\n")
  orig_txt = txt
  txt = remove_noise_text(txt, remove_noise=remove_noise)
  # print("After: ",txt, "\n\n")
  # exit()
  filters = [lambda x: x.lower(), strip_tags, strip_punctuation, strip_numeric]

  words = preprocessing.preprocess_string(txt, filters)
  stop_words = set(stopwords.words('english'))
  stop_words.remove("no")
  stop_words.remove("than")
  stop_words.remove("not")
  if clean:
    words = [w for w in words if not w in stop_words and re.search("[a-z-A-Z]+\\w+",w) != None and len(w) >1 ] 
  else:
    words = [w for w in words if re.search("[a-z-A-Z]+\\w+",w) != None and len(w) >1 ] 

  c_words = words

  if steam:
    porter = PorterStemmer()
    c_words = [porter.stem(word) for word in c_words]

  if lemma:
    lem = nltk.stem.wordnet.WordNetLemmatizer()
    c_words = [lem.lemmatize(word) for word in c_words]
  
  # if re.search("nodule #\\d",orig_txt) is not None: 
  #   print("\n#### Cleaned: ", c_words)

  return c_words

if __name__ == '__main__':
  main()





# TI-RADS Scoring Inference From Semi-Strucuted Reports
This repository contains the workflow of our proposed algorithm to infer TI-RADS scoring from clinical notes. Based on a given csv file with TI-RADS reports, our solution does:

    1) Segment all nodules in each report
    2) Classify each nodule
    3) Save the results (Accurary, F1, and Confusion Matrix) to a file

## Publication

* Ongoing
	
    
## Pipeline
Our pipilne representation is illustraded bellow:
  <table border=0>
     <tr align='center' > 
        <td><img src="https://github.com/thiagosantos1/TIRADS-Shared/blob/main/Img/pipeline.png" width="500"                  title="hover text"></td>         
     </tr>
  </table>
</br>


## GUI Application
A friendly user interface was developed, using python and PyQt. The interface can handle a single nodule classification as well as prediction over all reports on a file. For a single nodule prediction, the user can input a nodule description and the application will predict the output with the highest probability. In this module, the application also gives the probability of all categories, giving a better indication and explanation to the user. The user can also load a file with multiple reports and perform a classification on all nodules at once. Once the file is loaded, our application automatic segment every report to extract all nodules.

A runing example of the GUI application from a report and also from a single nodule:
<table border=0>
     <tr align='center' > 
        <td><img src="https://github.com/thiagosantos1/TIRADS-Inference/blob/main/Img/GUI_multiple.png" width="600"                  title="hover text"></td>         
       <td><img src="https://github.com/thiagosantos1/TIRADS-Inference/blob/main/Img/GUI_single.png" width="400" title="hover        text"></td>
     </tr>
  </table>
</br>

## GUI Usage:

    cd GUI/
    python3 application.py 


## Terminal Usage:

    python3 main.py -inputfile myfile.csv -column_name report -output_file results.txt
    
    Usage: main.py 	[-inputfile INPUTFILE] - Choose the input CSV file; Default: indiana.csv
    				[-column_name COLUMN_NAME] - Provide the column name for the report text; Default: report
               		[-output_file OUTPUT_FILE] - Choose an output file name; Default: results.txt
               		[-remove_structured True/False] - Choose to remove or not structured reports - If false, only nodules with free-text form of description will be used; Default: True
			
			
## Install Dependencies:

apt-get update && apt-get install -y python3 \ python3-pip


pip3 install --upgrade pip


pip3 install -r requirements.txt


## Install TIRADS-Inference

cd 

git clone https://github.com/thiagosantos1/TIRADS-Inference.git


## Download Our Pre-trained model

Open the following link and download the model

https://drive.google.com/file/d/1qhkilrbjO_heIUMvzCdRdEUcdXjRJVpQ/view?usp=sharing


## Unzip and move all files to TIRADS-Inference/BERT/

cd Downloads(Or folder where file were downloaded)

unzip BERT_model.zip -d BERT_model

mv BERT_model/* TIRADS-Inference/BERT/

## Use model to predict TI-RADS
cd

cd TIRADS-Shared

python3 main.py [usage]



## Contributors



Phd. Thiago Santos

Dr. Imon Banerjee

Dr. Judy Wawira

Dr. Omar Kalls

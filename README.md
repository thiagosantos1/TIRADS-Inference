# TI-RADS Scoring Inference.
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

## Usage:

    python3 main.py -inputfile myfile.csv -column_name report -output_file results.txt
    
    Usage: main.py 	[-inputfile INPUTFILE] - Choose the input CSV file; Default: indiana.csv
    				[-column_name COLUMN_NAME] - Provide the column name for the report text; Default: report
               		[-output_file OUTPUT_FILE] - Choose an output file name; Default: results.txt
               		[-remove_structured True/False] - Choose to remove or not structured reports - If false, only nodules with free-text form of description will be used; Default: True


# GUI Application
At this time, we also have a simple GUI application that can be used for infering TI-RADS scoring from a nodule text. You can provide a single nodule text and the model will rank the labels based on the probabilities predicted by the model. This can be useful as you may want to know how confident the model is and also to know how the model ranked the nodule in each TI-RADS category.

A runing example of the GUI application:
  <table border=0>
     <tr align='center' > 
        <td><img src="https://github.com/thiagosantos1/TIRADS-Shared/blob/main/Img/gui_example.png" width="500"                  title="hover text"></td>         
     </tr>
  </table>
</br>

## Usage:

    application.py is the executable file and it can be found inside of the folder GUI
    Usage:
    python3 application.py 
    
# Install Dependencies:

apt-get update && apt-get install -y python3 \ python3-pip


pip3 install --upgrade pip


pip3 install -r requirements.txt


# Install TIRADS-Shared

cd 

git clone https://github.com/thiagosantos1/TIRADS-Shared.git 


# Download Our Pre-trained model

Open the following link and download the model

https://drive.google.com/file/d/1qhkilrbjO_heIUMvzCdRdEUcdXjRJVpQ/view?usp=sharing


# Unzip and move all files to TIRADS-Shared/BERT/

cd Downloads(Or folder where file were downloaded)

unzip BERT_model.zip -d BERT_model

mv BERT_model/* TIRADS-Shared/BERT/

# Use model to predict TI-RADS
cd

cd TIRADS-Shared

python3 main.py [usage]



## Contributors



Phd. Thiago Santos

Dr. Imon Banerjee

Dr. 

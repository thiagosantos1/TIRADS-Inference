# This is a TIRADS-Shared repository.

# Usage:

    main.py is the main class to execute TI-RADS score prediction - No usage of demografic information
    Usage:
    python3 main.py 
    usage: main.py 	[-inputfile INPUTFILE] - Choose the input CSV file; Default: indiana.csv
    				[-column_name COLUMN_NAME] - Provide the column name for the report text; Default: report
               		[-output_file OUTPUT_FILE] - Choose an output file name; Default: results.txt
               		[-remove_structured True/False] - Choose to remove or not structured reports - If false, only nodules with free-text form of description will be used; Default: True



# Install Dependencies:

apt-get update && apt-get install -y python3 \
	python3-pip


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
# Master thesis 2022
Welcome to my thesis repository for my thesis research in "**Detecting and Classifying cyberbullying Memes in Twitter Posts**". You can find everything what I have used for this research within this repository. 

A small explanation for each folder and file: 

```
├── data
│   └── images
│       └── *all raw images from tweets
|   └── *.csv 
│       └── *all raw tweets from Tweet extraction 
│   └── output.json 
│       └── *labelling output from Amazon SageMaker Ground Truth
├── iteration-1
|   └── data
│       └── *jsonl files for train-dev-test
|   └── 1_data_split.py
│       └── *data split in train-dev-test (80-10-10)
├── iteration-2
|   └── data
│       └── *jsonl files for train-dev-test
|   └── 1_data_split.py
│       └── *data split in train-dev-test (75-10-15)
├── notebooks
|   └── feature_extraction.ipynb
│       └── *notebook for feature extraction of Vilio 
│   └── vilio_end_to_end_process.ipynb
│       └── *end-to-end process for setting up the Vilio model till producing predictions 
|   └── visualbert_end_to_end_process.ipynb
│       └── *end-to-end process for setting up the visualbert model till producing predictions 
├── 1_data_gathering.py
|   └── *script to run for extracting data for Twitter API
├── 2_data_processing.py
|   └── *processing all the raw data from the "data" folder
├── 3_eda.ipynb
|   └── *EDA for monthly report 
├── 4_eda_final_df.ipynb
|   └── *EDA for final dataset
├── hatefulmemes.zip
|   └── *dataset to upload to Google Colab env
```

Every file was run on a local machine, except for the Notebooks, which were setup within Google Colab Pro. Clone the [Vilio](https://github.com/Rchou97/vilio) repository and upload it in the Drive environment to run the Vilio Notebook. 

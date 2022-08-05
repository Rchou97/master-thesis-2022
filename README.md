# Master thesis 2022
Welcome to my thesis repository for my thesis research in "**Detecting and Classifying cyberbullying Memes in Twitter Posts**". You can find everything what I have used for this research within this repository. 

**Abstract**
Cyberbullying and other forms of aggressive conversation on social media have been increasing since the COVID-19 outbreak. This form of content is also depicted in the form of memes, which is a combination of images and text content. Filtering out image-with-text data on social media is more difficult to do since machine learning models can have difficulties detecting the sentiment of the message. This is due to the format in which memes are presented. This research addresses the detection of cyberbullying within image-with-text data that are posted on the Twitter platform. An attempt is done to set up a multi-modal classification model that is capable to analyse the sentiment of the meme and detecting if the content of the Tweet contains cyberbullying content. In comparison to other studies in this field, this research will address the problem specifically focused on image-with-text data in the form of memes that contain these types of content. The purpose of this model would be to serve as an additional filter for detecting harmful content in memes and contribute to the research problem of creating a healthy Twitter environment. The final optimised model manages to retrieve an accuracy score of 91.03 and an F1-score of 66.67.

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
├── Thesis_Richard_Chou_v1_0.pdf
|   └── *delivered report to finalise my studies
|
```

Every file was run on a local machine, except for the ```notebooks```, which were setup within Google Colab Pro. Clone the [Vilio](https://github.com/Rchou97/vilio) repository and upload it in the Drive environment to run the Vilio Notebook. 

If you have any questions, feel free to ask them. 

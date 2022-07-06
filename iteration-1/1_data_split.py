import json
import logging
from pathlib import Path
import random
import tarfile
import tempfile
import warnings

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
# import pandas_path  # Path style access for pandas
from tqdm import tqdm
from sklearn.model_selection import train_test_split 


import torch                    
import torchvision
import fasttext

df = pd.read_csv('data/df_fin_merged.csv')

train_ratio = 0.8
validation_ratio = 0.1
test_ratio = 0.1

columns = ['User', 'Tweet', 'Date', 'Language', 'Hashtags', 'Image', 'Image_jpg', 'Job_name', 'Type', 'Human_annotated', 'Annotation_date', 'Meme_text']
X = df[columns]
y = df.Final_label_class_num

# train is now 75% of the entire data set
# the _junk suffix means that we drop that variable completely
x_train, x_test, y_train, y_test = train_test_split(X, y, test_size = 1 - train_ratio, random_state = 5)

# test is now 10% of the initial data set
# validation is now 15% of the initial data set
x_dev, x_test, y_dev, y_test = train_test_split(x_test, y_test, test_size = test_ratio/(test_ratio + validation_ratio), random_state = 5) 

train_df = x_train.merge(y_train, left_index = True, right_index = True, how = 'inner').reset_index().rename(columns = {'index':'id'})
dev_df = x_dev.merge(y_dev, left_index = True, right_index = True, how = 'inner').reset_index().rename(columns = {'index':'id'})
test_df = x_test.merge(y_test, left_index = True, right_index = True, how = 'inner').reset_index().rename(columns = {'index':'id'})

train_df = train_df.rename(columns = {'Image_jpg':'img', 'Meme_text':'text', 'Final_label_class_num':'label'})
dev_df = dev_df.rename(columns = {'Image_jpg':'img', 'Meme_text':'text', 'Final_label_class_num':'label'})
test_df = test_df.rename(columns = {'Image_jpg':'img', 'Meme_text':'text', 'Final_label_class_num':'label'})

train_df['id'] = train_df['id'].astype(str)
dev_df['id'] = dev_df['id'].astype(str)
test_df['id'] = test_df['id'].astype(str)

train_df['label'] = train_df['label'].astype(int)
dev_df['label'] = dev_df['label'].astype(int)
test_df['label'] = test_df['label'].astype(int)

train_df['text'] = train_df['text'].replace(np.nan, '', regex = True)
dev_df['text'] = dev_df['text'].replace(np.nan, '',regex = True)
train_df['text'] = train_df['text'].replace(np.nan, '',regex = True)

train_df['text'] = train_df['text'].replace({r'\s+$': '', r'^\s+': ''}, regex=True).replace(r'\n',  ' ', regex=True)
dev_df['text'] = dev_df['text'].replace({r'\s+$': '', r'^\s+': ''}, regex=True).replace(r'\n',  ' ', regex=True)
train_df['text'] = train_df['text'].replace({r'\s+$': '', r'^\s+': ''}, regex=True).replace(r'\n',  ' ', regex=True)

train = train_df[['id', 'img', 'label', 'text']].copy()
train['img'] = "img" + "/" + train['img']

dev = dev_df[['id', 'img', 'label', 'text']].copy()
dev['img'] = "img" + "/" + dev['img']

test = test_df[['id', 'img', 'label', 'text']].copy()
test['img'] = "img" + "/" + test['img']

train.to_json('C:\\Users\\richa\\OneDrive\\Documenten\\GitHub\\master_thesis_2022\\iteration1\\data\\train.jsonl', orient='records', lines = True)
dev.to_json('C:\\Users\\richa\\OneDrive\\Documenten\\GitHub\\master_thesis_2022\\iteration1\\data\\dev_seen.jsonl', orient='records', lines = True)
test.to_json('C:\\Users\\richa\\OneDrive\\Documenten\\GitHub\\master_thesis_2022\\iteration1\\data\\test_seen.jsonl', orient='records', lines = True)

train = pd.read_json('C:\\Users\\richa\\OneDrive\\Documenten\\GitHub\\master_thesis_2022\\iteration1\\data\\train.jsonl', lines = True)
dev = pd.read_json('C:\\Users\\richa\\OneDrive\\Documenten\\GitHub\\master_thesis_2022\\iteration1\\data\\dev_seen.jsonl', lines = True)
test = pd.read_json('C:\\Users\\richa\\OneDrive\\Documenten\\GitHub\\master_thesis_2022\\iteration1\\data\\test_seen.jsonl', lines =  True)

test_seen = test[0:33].reset_index(drop = True)
test_unseen = test[34:].reset_index(drop = True)

val_seen = val[0:35].reset_index(drop = True)
val_unseen = val[36:].reset_index(drop = True)

val_seen.to_json('C:\\Users\\richa\\OneDrive\\Documenten\\GitHub\\master_thesis_2022\\iteration1\\data\\dev_seen.jsonl')
val_unseen.to_json('C:\\Users\\richa\\OneDrive\\Documenten\\GitHub\\master_thesis_2022\\iteration1\\data\\dev_unseen.jsonl')

test_seen.to_json('C:\\Users\\richa\\OneDrive\\Documenten\\GitHub\\master_thesis_2022\\iteration1\\data\\test_seen.jsonl', orient='records', lines = True)
test_unseen.to_json('C:\\Users\\richa\\OneDrive\\Documenten\\GitHub\\master_thesis_2022\\iteration1\\data\\test_unseen.jsonl', orient='records', lines = True)

train.to_json('C:\\Users\\richa\\OneDrive\\Documenten\\GitHub\\master_thesis_2022\\iteration1\\data\\train.jsonl')


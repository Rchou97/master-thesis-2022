from urllib.parse import urljoin, urlparse
from requests_oauthlib import OAuth1
from tqdm import tqdm
from pandas.io.json import json_normalize

import pandas as pd 
import numpy as np 
import datetime, time
import os 
import requests
import json

cd = os.path.dirname(os.path.abspath('2_data_processing.py'))

# Dataset merge 
df = pd.read_csv('data\df_dank.csv')
df_1 = pd.read_csv('data\df_dankmeme.csv')
df_2 = pd.read_csv('data\df_dankmemes.csv')
df_3 = pd.read_csv('data\df_dankmemes_2.csv')
df_4 = pd.read_csv('data\df_dankmemes_3.csv')
df_5 = pd.read_csv('data\df_meme.csv')
df_6 = pd.read_csv('data\df_meme_2.csv')
df_7 = pd.read_csv('data\df_meme_3.csv')
df_8 = pd.read_csv('data\df_meme_4.csv')
df_9 = pd.read_csv('data\df_memes.csv')
df_10 = pd.read_csv('data\df_memes_2.csv')
df_11 = pd.read_csv('data\df_memes_3.csv')
df_12 = pd.read_csv('data\df_memes_4.csv')
df_13 = pd.read_csv('data\df_memedaily.csv')
df_14 = pd.read_csv('data\df_memesdaily.csv')
df_15 = pd.read_csv('data\df_memesdaily_2.csv')
df_16 = pd.read_csv('data\df_funnymeme.csv')
df_17 = pd.read_csv('data\df_multiple_hashtag_meme.csv')

# Create/append final dataset
df_fin = df.append([df_1, df_2, df_3, df_4, df_5, df_6, df_7, df_8, df_9, df_10, df_11, df_12, df_13, df_14, df_15, df_16, df_17]).reset_index().drop(columns = 'index')

# Filter & create new columns function
def filter_create_df(df): 
    df = df.drop_duplicates(subset = "Image").reset_index(drop = True)
    df = df[df['Language'] == 'en'].reset_index().drop(columns = 'index')
    
    vid_thumb = df[df.Image.str.startswith('http://pbs.twimg.com/ext_tw_video_thumb/', na = False)]
    vid_thumb2 = df[df.Image.str.startswith('http://pbs.twimg.com/tweet_video_thumb/', na = False)]
    
    df = df[~df.Image.isin(vid_thumb.Image)]
    df = df[~df.Image.isin(vid_thumb2.Image)].reset_index(drop = True)
    df['Image_jpg'] = df['Image'].map(lambda x: x.lstrip('http://pbs.twimg.com/media/'))

    return df

df_fin = filter_create_df(df_fin)
df_fin.to_csv('data/df_fin.csv', index = False)


# Process data labelling function 
df_label = pd.read_json('data\output.json', lines = True)

def process_df_label(json_df): 
    json_df['Image_jpg'] = json_df['source-ref'].map(lambda x: x.lstrip('s3://master-thesis-data-bucket/images/'))
    df1 = json_df['Image_jpg']
    df2 = json_normalize(json_df['cyberbullying-labelling-job-metadata']) 
    df1 = pd.merge(df1, df2, left_index=True, right_index=True)
    return df1

df_label_clean = process_df_label(df_label)
df_fin_merged = df_fin.merge(df_label_clean, on = 'Image_jpg')
df_fin_merged = df_fin_merged.rename(columns = {'job-name':'Job_name', 'creation-date':'Annotation_date', 'human-annotated':'Human_annotated', 'type':'Type', 
                                                'class-map.0':'Class_map_0', 'confidence-map.0':'Confidence_map_0', 
                                                'class-map.1':'Class_map_1', 'confidence-map.1':'Confidence_map_1', 
                                                'class-map.2':'Class_map_2', 'confidence-map.2':'Confidence_map_2', 
                                                'class-map.3':'Class_map_3', 'confidence-map.3':'Confidence_map_3', 
                                                'class-map.4':'Class_map_4', 'confidence-map.4':'Confidence_map_4'})
columns = ['User', 'Tweet', 'Date', 'Language', 'Hashtags', 'Image', 'Image_jpg', 'Job_name', 'Type', 'Human_annotated', 'Annotation_date', 
           'Class_map_0', 'Confidence_map_0', 'Class_map_1', 'Confidence_map_1', 'Class_map_2', 'Confidence_map_2', 'Class_map_3', 'Confidence_map_3', 
           'Class_map_4', 'Confidence_map_4']
df_fin_merged = df_fin_merged[columns]

def final_class_col(row):
    if row['Confidence_map_0'] >= 0.5 and row['Confidence_map_1'] < 0.5 and row['Confidence_map_2'] < 0.5 and row['Confidence_map_3'] < 0.5 and row['Confidence_map_4'] < 0.5:
        return row['Class_map_0']
    elif row['Confidence_map_0'] < 0.5 and row['Confidence_map_1'] >= 0.5 and row['Confidence_map_2'] < 0.5 and row['Confidence_map_3'] < 0.5 and row['Confidence_map_4'] < 0.5:
        return row['Class_map_1']
    elif row['Confidence_map_0'] < 0.5 and row['Confidence_map_1'] < 0.5 and row['Confidence_map_2'] >= 0.5 and row['Confidence_map_3'] < 0.5 and row['Confidence_map_4'] < 0.5:
        return row['Class_map_2']
    elif row['Confidence_map_0'] < 0.5 and row['Confidence_map_1'] < 0.5 and row['Confidence_map_2'] < 0.5 and row['Confidence_map_3'] >= 0.5 and row['Confidence_map_4'] < 0.5:
        return row['Class_map_3']
    elif row['Confidence_map_0'] < 0.5 and row['Confidence_map_1'] < 0.5 and row['Confidence_map_2'] < 0.5 and row['Confidence_map_3'] < 0.5 and row['Confidence_map_4'] >= 0.5:
        return row['Class_map_4']

def final_class_col_2(row):
    if row['Confidence_map_0'] >= 0.5 and row['Confidence_map_1'] < 0.5 and row['Confidence_map_2'] < 0.5 and row['Confidence_map_3'] < 0.5 and row['Confidence_map_4'] < 0.5:
        return 0
    elif row['Confidence_map_0'] < 0.5 and row['Confidence_map_1'] >= 0.5 and row['Confidence_map_2'] < 0.5 and row['Confidence_map_3'] < 0.5 and row['Confidence_map_4'] < 0.5:
        return 1
    elif row['Confidence_map_0'] < 0.5 and row['Confidence_map_1'] < 0.5 and row['Confidence_map_2'] >= 0.5 and row['Confidence_map_3'] < 0.5 and row['Confidence_map_4'] < 0.5:
        return 2
    elif row['Confidence_map_0'] < 0.5 and row['Confidence_map_1'] < 0.5 and row['Confidence_map_2'] < 0.5 and row['Confidence_map_3'] >= 0.5 and row['Confidence_map_4'] < 0.5:
        return 3
    elif row['Confidence_map_0'] < 0.5 and row['Confidence_map_1'] < 0.5 and row['Confidence_map_2'] < 0.5 and row['Confidence_map_3'] < 0.5 and row['Confidence_map_4'] >= 0.5:
        return 4

def fill_na_row(df): 
    mask = (df['Confidence_map_0'] == 0.05) & (df['Confidence_map_1'] == 0) & (df['Confidence_map_2'] == 0.05) & (df['Confidence_map_3'] == 0.05) & (df['Confidence_map_4'] == 0)
    df['Final_label'] = df['Final_label'].mask(mask, df['Final_label'].fillna(df['Class_map_3']))
    df['Final_label_class_num'] = df['Final_label_class_num'].mask(mask, df['Final_label_class_num'].fillna(3))

    mask2 = (df['Confidence_map_0'] == 0.95) & (df['Confidence_map_1'] == 0.05) & (df['Confidence_map_2'] == 0) & (df['Confidence_map_3'] == 0.74) & (df['Confidence_map_4'] == 0)
    df['Final_label'] = df['Final_label'].mask(mask2, df['Final_label'].fillna(df['Class_map_0']))
    df['Final_label_class_num'] = df['Final_label_class_num'].mask(mask2, df['Final_label_class_num'].fillna(0))

    mask3 = (df['Confidence_map_0'] == 0) & (df['Confidence_map_1'] == 0.05) & (df['Confidence_map_2'] == 0.05) & (df['Confidence_map_3'] == 0.1) & (df['Confidence_map_4'] == 0)
    df['Final_label'] = df['Final_label'].mask(mask3, df['Final_label'].fillna(df['Class_map_3']))
    df['Final_label_class_num'] = df['Final_label_class_num'].mask(mask3, df['Final_label_class_num'].fillna(3))

    mask4 = (df['Confidence_map_0'] == 0) & (df['Confidence_map_1'] == 0) & (df['Confidence_map_2'] == 0.05) & (df['Confidence_map_3'] == 0.05) & (df['Confidence_map_4'] == 0.05)
    df['Final_label'] = df['Final_label'].mask(mask4, df['Final_label'].fillna(df['Class_map_3']))
    df['Final_label_class_num'] = df['Final_label_class_num'].mask(mask4, df['Final_label_class_num'].fillna(3))

    mask5 = (df['Confidence_map_0'] == 0.09) & (df['Confidence_map_1'] == 0.49) & (df['Confidence_map_2'] == 0) & (df['Confidence_map_3'] == 0.05) & (df['Confidence_map_4'] == 0.05)
    df['Final_label'] = df['Final_label'].mask(mask5, df['Final_label'].fillna(df['Class_map_1']))
    df['Final_label_class_num'] = df['Final_label_class_num'].mask(mask5, df['Final_label_class_num'].fillna(1))

    mask6 = (df['Confidence_map_0'] == 0) & (df['Confidence_map_1'] == 0.05) & (df['Confidence_map_2'] == 0.05) & (df['Confidence_map_3'] == 0.05) & (df['Confidence_map_4'] == 0.05)
    df['Final_label'] = df['Final_label'].mask(mask6, df['Final_label'].fillna(df['Class_map_3']))
    df['Final_label_class_num'] = df['Final_label_class_num'].mask(mask6, df['Final_label_class_num'].fillna(3))

    mask7 = (df['Confidence_map_0'] == 0) & (df['Confidence_map_1'] == 0.95) & (df['Confidence_map_2'] == 0.95) & (df['Confidence_map_3'] == 0.05) & (df['Confidence_map_4'] == 0)
    df['Final_label'] = df['Final_label'].mask(mask7, df['Final_label'].fillna(df['Class_map_2']))
    df['Final_label_class_num'] = df['Final_label_class_num'].mask(mask7, df['Final_label_class_num'].fillna(2))

    mask8 = (df['Confidence_map_0'] == 0) & (df['Confidence_map_1'] == 0.05) & (df['Confidence_map_2'] == 0.45) & (df['Confidence_map_3'] == 0.05) & (df['Confidence_map_4'] == 0)
    df['Final_label'] = df['Final_label'].mask(mask8, df['Final_label'].fillna(df['Class_map_2']))
    df['Final_label_class_num'] = df['Final_label_class_num'].mask(mask8, df['Final_label_class_num'].fillna(2))

    return df

df_fin_merged = df_fin_merged.replace(np.nan, 0)
df_fin_merged['Final_label'] = df_fin_merged.apply(final_class_col, axis=1)
df_fin_merged['Final_label_class_num'] = df_fin_merged.apply(final_class_col_2, axis=1)
df_fin_merged = fill_na_row(df_fin_merged)


# Extract text from the meme and store it as additional feature
def process_df_meme(df): 
    df_meme = pd.read_csv('data/meme_text.csv')
    df1 = df.merge(df_meme, on = 'Image_jpg', how = 'left')
    return df1

df_fin_merged = process_df_meme(df_fin_merged)
df_fin_merged = df_fin_merged.drop(columns = 'Unnamed: 0')
df_fin_merged.to_csv('data\df_fin_merged.csv')


# Store images from url 
def download(url, pathname):
    if not os.path.isdir(pathname):
        os.makedirs(pathname)
    response = requests.get(url, stream = True)
    file_size = int(response.headers.get("Content-Length", 0))
    filename = os.path.join(pathname, url.split("/")[-1])
    progress = tqdm(response.iter_content(1024), f"Downloading {filename}", total=file_size, unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "wb") as f:
        for data in progress:
            f.write(data)
            progress.update(len(data))

def final(links, path):
    for i in links:
        download(i, path)

df_fin_merged = pd.read_csv('data\df_fin_merged.csv')
df_fin_merged['Image_jpg']
final(df_fin_merged['Image'], 'data\images')
from urllib.parse import urljoin, urlparse
from requests_oauthlib import OAuth1
from tqdm import tqdm

import pandas as pd 
import numpy as np 
import datetime, time
import os 
import requests

cd = os.path.dirname(os.path.abspath('2_data_processing.py'))

# Dataset merge 
df = pd.read_csv('data\df.csv')
df_1 = pd.read_csv('data\df_1.csv')
df_2 = pd.read_csv('data\df_2.csv')

df_fin = df.append([df_1, df_2]).reset_index().drop(columns = 'index')
df_fin = df_fin.drop_duplicates(subset = None).reset_index(drop = True)
df_fin
df_fin.to_csv('data/df_fin.csv', index = False)

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

final(df_fin['Image'], 'data\images')
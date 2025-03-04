# deprecated

from tqdm import tqdm
import os
import json
import pandas as pd
from pymongo import MongoClient
import re
import requests
import numpy as np

# MongoDB URI
uri = 'mongodb://localhost:27017'

def remove_hastag(url):
    # Remove 'https://' or 'http://'
    head = ''
    if url.startswith('https://'):
        head = 'https://'
        url = url[8:]
    elif url.startswith('http://'):
        head = 'http://'
        url = url[7:]
    index = url.rfind('/')
    if index != -1:
        index2 = url.rfind('#')
        if index2 > index:
            url = url[:index2]
    return head + url

def get_extension(url, extensions):
    # Remove 'https://' or 'http://'
    if url.startswith('https://'):
        url = url[8:]
    elif url.startswith('http://'):
        url = url[7:]
    index = url.rfind('/')
    extension = ''
    if index != -1:
        index2 = url.rfind('.')
        if index2 > index:
            extension = url[index2+1:].lower()
            for ext in extensions:
                if extension.startswith(ext):
                    return ext
    return np.nan

def remove_not_isalnum(url):
    while len(url) > 0 and not url[-1].isalnum():
        url = url[:-1]
    while len(url) > 0 and not url[0].isalnum():
        url = url[1:]
    return url
def is_tld(url, tlds):
    # Remove 'https://' or 'http://'
    if url.startswith('https://'):
        url = url[8:]
    elif url.startswith('http://'):
        url = url[7:]
    index = url.find('/')
    if index != -1:
        url = url[:index]
    if '@' in url:
        return False
    index = url.rfind('.')
    if index != -1:
        url = url[index+1:]
        if url.lower() in tlds:
            return True
    return False
def remove_head(url):
    # Remove 'https://' or 'http://'
    if url.startswith('https://'):
        url = url[8:]
    elif url.startswith('http://'):
        url = url[7:]
    # remove 'www.'
    if url.startswith('www.'):
        url = url[4:]
    return url

def is_still_valid(url):
    # se è vuoto ritorna False
    if url == '':
        return False
    # se non ha un punto ritorna False
    if '.' not in url:
        return False
    # se ha due punti consecutivi ritorna False
    if '..' in url:
        return False
    return True

def get_links(text, tlds):
    # text = 'You can view more details at https://uibakery.io, or just ping via email. You can view more details at uibakery.io or just ping via email.'
    urls = []
    # Extract URL from a string
    url_extract_pattern = "https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)"
    urls += re.findall(url_extract_pattern, text)
    for url in urls:
        text = text.replace(url, ' ')
    url_extract_pattern = "[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)"
    urls += re.findall(url_extract_pattern, text)
    urls_cleaned = []
    for url in urls:
        if is_tld(url, tlds):
            url = remove_not_isalnum(url)
            if is_still_valid(url):
                urls_cleaned.append(url)
    return urls_cleaned

def url_request(url, allow_redirects=True, timeout=5):
    history = []
    try:
        response = requests.head(url, allow_redirects=allow_redirects, timeout=timeout)
    except:
        return []
    if response.history != []:
        for hop in response.history:
            history.append(
                {
                    'status_code': hop.status_code, 
                    'url' : hop.url, 
                    'client_headers' : dict(hop.request.headers),
                    'server_heders' : dict(hop.headers)
                }
            )
    history.append(
        {
            'status_code': response.status_code, 
            'url' : response.url, 
            'client_headers' : dict(response.request.headers),
            'server_heders' : dict(response.headers)
        }
    )
    return history

def filter1(url):
    # Remove 'https://' or 'http://'
    if url.startswith('https://'):
        url = url[8:]
    elif url.startswith('http://'):
        url = url[7:]
    return url
def filter2(url):
    # Remove 'www.'
    if url.startswith('www.'):
        url = url[4:]
    return url
def filter3(url):
    # Remove everything after first '/'
    index = url.find('/')
    if index != -1:
        url = url[:index]
    return url
def filter4(url):
    # Remove everything after last '.'
    index = url.rfind('.')
    if index != -1:
        url = url[:index]
    return url
def filter5(url):
    # Remove everything beafore last '.'
    index = url.rfind('.')
    if index != -1:
        url = url[index+1:]
    return url

def slice_clear_url(df, col, filters=[1, 2, 3, 4, 5]):
    df[col+'_filter1'] = df[col].apply(filter1)
    df[col+'_filter2'] = df[col+'_filter1'].apply(filter2)
    df[col+'_filter3'] = df[col+'_filter2'].apply(filter3)
    df[col+'_filter4'] = df[col+'_filter3'].apply(filter4)
    df[col+'_filter5'] = df[col+'_filter4'].apply(filter5)
    for i in range(1, 6):
        if i not in filters:
            df = df.drop(col+'_filter'+str(i), axis=1)
    return df
    
def get_urls_and_data_df(links_per_channels_path, channel_to_language_mapping_path):
    links_per_channels_df = pd.read_csv(links_per_channels_path)
    channel_to_language_mapping_df = pd.read_csv(channel_to_language_mapping_path)
    urls_and_data_df = pd.merge(links_per_channels_df, channel_to_language_mapping_df, on='ch_ID', how='outer')
    return urls_and_data_df

def get_resolved_notsolved_df(data_folder):
    resolved_urls_df = None
    notsolved_urls_df = None

    file_list = []
    for directory, _, files in os.walk(data_folder):
        for file_name in files:
            file_path = os.path.join(directory, file_name)
            if os.path.isfile(file_path) and file_path.endswith(".json"):
                file_list.append(file_path)

    for file_path in tqdm(file_list):
        resolved_urls = []
        notsolved_urls = []
        with open(file_path) as file:
            data = json.load(file)
        for key, value in data.items():
            if value == []:
                notsolved_urls.append((file_path, key))
            else:
                resolved_urls.append((file_path, key, value[-1]['url'], value[-1]['status_code'], len(value)))
        tmp_resolved_urls_df = pd.DataFrame(resolved_urls, columns=['file_path', 'url', 'final_url', 'status_code', 'n_hop'])
        tmp_notsolved_urls_df = pd.DataFrame(notsolved_urls, columns=['file_path', 'url'])
        if type(resolved_urls_df) == type(None) or type(notsolved_urls_df) == type(None):
            resolved_urls_df = tmp_resolved_urls_df.copy()
            notsolved_urls_df = tmp_notsolved_urls_df.copy()
        else:
            resolved_urls_df = pd.concat([resolved_urls_df, tmp_resolved_urls_df])
            notsolved_urls_df = pd.concat([notsolved_urls_df, tmp_notsolved_urls_df])
    resolved_urls_df.reset_index(drop=True, inplace=True)
    notsolved_urls_df.reset_index(drop=True, inplace=True)
    return resolved_urls_df, notsolved_urls_df

def insert_url(data, db_name):
    with MongoClient(uri) as client:
        db = client[db_name]
        channel = db.Link
        channel.insert_one(data)
    return

def insert_urls(data, db_name):
    with MongoClient(uri) as client:
        db = client[db_name]
        channel = db.Link
        channel.insert_many(data)
    return

def import_urls_to_mongoDB(db_name, root_directory):
    file_list = []
    for directory, _, files in os.walk(root_directory):
        for name in files:
            file_path = os.path.join(directory, name)
            if os.path.isfile(file_path) and name.endswith(".json"):
                file_list.append(file_path)
    for json_file in tqdm(file_list):
        with open(json_file) as f:
            print(json_file)
            urls = json.load(f)
        data = []
        for url in urls:
            if urls[url] != []:
                data.append({
                            'url' : url,
                            'hops' : urls[url]
                            })
        insert_urls(data, db_name)
    return

def get_url_data(url, db_name):
    with MongoClient(uri) as client:
        db = client[db_name]
        channel = db.Link
        data = channel.find_one({'url': url})
    return data

def get_all_urls(db_name):
    urls = []
    with MongoClient(uri) as client:
        db = client[db_name]
        urls = [link['url'] for link in db.Link.find({}, {'url'})]
    return urls
    
    
def clear_html(html_string):
    def clear_tag(html_string, tag):
        if html_string.find(f'<{tag}') == -1 or html_string.find(f'</{tag}>') == -1:
            return html_string
        start = html_string.find(f'<{tag}')
        end = start + html_string[start:].find(f'</{tag}>') + len(tag)+3
        html_string = html_string[:start] + ' ' + html_string[end:]
        return html_string
    tags = ['iframe', 'template', 'script', 'style']
    for tag in tags:
        while True:
            new_html_string = clear_tag(html_string, tag)
            if new_html_string == html_string:
                break
            html_string = new_html_string
    html_string = re.sub(r'<[^>]*?>', ' ', html_string)
    html_string = re.sub(r'\s+', ' ', html_string)
    html_string = html_string.strip()
    return html_string

if __name__ == '__main__':
    import_urls_to_mongoDB('TestShortlinks', '../../../data/resolved_en')

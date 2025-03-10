import requests
import json
import pandas as pd
from tqdm import tqdm
from threading import Thread
from multiprocessing import Pool
import os
import math
import time

def request(url, timeout, sleep):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    }
    time.sleep(sleep)
    result = {
        'error': None,
        'response_url': None,
        'status_code': None,
        'headers': None,
        'content': None,
    }
    if not url.startswith('https://') and not url.startswith('http://'):
        try:
            response = requests.get('https://'+url, allow_redirects=True, timeout=timeout, headers=headers)
        except:
            try:
                response = requests.get('http://'+url, allow_redirects=True, timeout=timeout, headers=headers)
            except Exception as e:
                result['error'] = str(e)
                return result
    else:
        try:
            response = requests.get(url, allow_redirects=True, timeout=timeout, headers=headers)
        except Exception as e:
            result['error'] = str(e)
            return result
    result['response_url'] = response.url
    result['status_code'] = response.status_code
    result['headers'] = json.dumps(dict(response.headers))
    result['content'] = str(response.content)
    return result

class Worker(Thread):
    def __init__(self, urls, timeout, sleep):
        Thread.__init__(self)
        self.urls = urls
        self.timeout = timeout
        self.sleep = sleep
        self.subsubdata = []
    def run(self):
        self.subsubdata = [{'url': url, **request(url, self.timeout, self.sleep)} for url in self.urls]
    def join(self):
        Thread.join(self)
        return self.subsubdata
    
def foo(args):
    urls, n_thread_per_core, timeout, sleep = args
    subdata = []
    step = max(1, int(len(urls)/n_thread_per_core))
    threads = []
    for index in range(0, len(urls), step):
        thread = Worker(urls[index:index+step], timeout, sleep)
        thread.start()
        threads.append(thread)
    for thread in threads:
        subsubdata = thread.join()
        subdata += subsubdata
    return subdata

def get_resolved_urls(dst_file):
    solved_urls = []
    if os.path.exists(dst_file):
        solved_urls = pd.read_csv(dst_file, usecols=['url']).drop_duplicates()['url'].tolist()
    return solved_urls
    
def main(src_file, dst_file, n_core, n_url_per_chunk, n_thread_per_core, timeout, sleep, avoid_duplicates):
    urls = pd.read_csv(src_file).filter(['url']).drop_duplicates().sample(frac=1)
    if avoid_duplicates:
        solved_urls = get_resolved_urls(dst_file)
        urls = urls[~urls['url'].isin(solved_urls)]
    urls = urls['url'].dropna().tolist()
    n_url = len(urls)
    n_chunk = math.ceil(n_url/n_url_per_chunk)
    l = []
    for index in range(0, len(urls), n_url_per_chunk):
        l.append((urls[index:index+n_url_per_chunk], n_thread_per_core, timeout, sleep))
    with Pool(n_core) as pool:
        for subdata in tqdm(pool.imap(foo, l), total=n_chunk, desc='Collecting URLs responses'):
            subdata = pd.DataFrame(subdata)
            if not subdata.empty:
                if not os.path.exists(dst_file):
                    subdata.to_csv(dst_file, index=False)
                else:
                    subdata.to_csv(dst_file, mode='a', header=False, index=False)
    return
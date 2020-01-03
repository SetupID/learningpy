#!/usr/bin/env python3
#-*- coding : utf-8 -*-
import requests
from tqdm import tqdm
from datetime import datetime
from bs4 import BeautifulSoup
import sys
import argparse
argm = argparse.ArgumentParser(description='Fbdown.py is tool for download fucking video in facebook')
argm.add_argument('--url',help="URL video U want to download")
args = argm.parse_args()
site = 'https://www.getfvid.com/downloader'
headers = {
"Host": "www.getfvid.com",
"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:71.0) Gecko/20100101 Firefox/71.0",
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
"Accept-Language": "en-US,en;q=0.5",
"Accept-Encoding" : "gzip, deflate, br",
"Content-Type": "application/x-www-form-urlencoded",
"Connection": "keep-alive",
"Referer": "https://www.getfvid.com/"
}
data = {'url' : args.url}

respon = requests.post(site,headers = headers,data = data).text
html = BeautifulSoup(respon, 'html.parser')
try:
	cari = html.find('div', class_ = 'col-md-4 btns-download').a
	link = cari['href']
except AttributeError:
	print("Oh shit can't download,maybe this is private video !")
	sys.exit()
dl = requests.get(link, headers={'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:71.0) Gecko/20100101 Firefox/71.0'}, stream=True)

filename = datetime.now().strftime('fb-vid[%H:%M:%Y].mp4')
total_size = int(dl.headers.get('content-length', 0))
block_size = 1024
t=tqdm(total=total_size, unit='iB', unit_scale=True)
with open(filename, 'wb') as f:
	try: 
		for d in dl.iter_content(block_size):
			t.update(len(d))
			# f.write(dl.content)
			f.write(d)
	except KeyboardInterrupt:
		print("CTRL+C detected, exiting.")
		sys.exit()
t.close()






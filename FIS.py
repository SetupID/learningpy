#!/usr/bin/python3
#-*- visit : <heartscode.net/> -*-

########################################################################
#[installasi termux]
#wget https://raw.githubusercontent.com/SetupID/learningpy/master/FIS.py 
#pip install requests,sys,argparse,bs4,sty
#[installasi linux]
#wget https://raw.githubusercontent.com/SetupID/learningpy/master/FIS.py 
#pip3 install requests,sys,argparse,bs4,sty
########################################################################

import requests,sys,argparse
from bs4 import BeautifulSoup as bs
from sty import fg,rs


argm = argparse.ArgumentParser(description='Note: if the movie u\'r looking for uses spaces, please add a double quote like "Iron Man"')
argm.add_argument('-s',help='Search Query,ex : "IP MAN 4"',metavar='Film/Movie',required=True)
args = argm.parse_args()

#di warnai abang,kuning,ijo ben koyo pelangi 
def abang(str):
	return fg.da_red + str + rs.fg
def kuning(str):
	return fg.li_yellow + str + rs.fg
def ijo(str):
	return fg(34) + str + rs.fg
def golek(film):
	result = {}
	s = 'https://kawanfilm21.online/?s='+film
	header = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:71.0) Gecko/20100101 Firefox/71.0"}
	h2 = header.update({'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8'})
	req = requests.get(s,headers=header).text
	scrap = bs(req,'html.parser')
	try:
		div = scrap.find('div',{'class': 'content-thumbnail text-center'})
		link = div.a.get('href')
		al = requests.get(link,headers=header).text #access link
		scrp = bs(al,'html.parser')
		id = scrp.find('div',{'id':'muvipro_player_content_id'}).get('data-id')
		d = {'action':'muvipro_player_content','tab':'player1','post_id':id}
		pos = requests.post('https://kawanfilm21.online/wp-admin/admin-ajax.php',headers=h2,data=d).text
		result['title'] = scrp.find('h1',{'class':'entry-title'}).get_text()
		result['description'] = scrp.find_all('p')[1].get_text()
		result['quality'] = scrp.find('span',{'class':'gmr-movie-quality'}).a.get_text()
		stream = bs(pos,'html.parser').iframe.get('src')
		result['streaming'] = 'https:'+stream
		gl = []  #get link
		for l in scrp.find_all('ul',{'class':'list-inline gmr-download-list clearfix'}):
			for a in l.find_all('a'):
				gl.append({a.get_text() : a.get('href')})
		result['download_link'] = gl
		return result
	except AttributeError:
		print(abang(f'Film "{args.s}"" not found'))
		sys.exit()
def cetak(hasil):
	print(abang("[Judul] : "+ijo(hasil['title'])))
	print(abang("[Deskripsi] :"+ijo(hasil['description'])))
	print(abang("[Kualitas] :"+ijo(hasil['quality'])))
	print(abang("[link streaming] :"+ijo(hasil['streaming'])))
	print(kuning("\t\t\t..:[Link Download]:.."))
	for i in hasil['download_link']:
		for k,v in i.items():
			print(abang(f"[{k}] : "+ijo(v)))
if __name__ == "__main__":
	try:
		print(kuning("""
              _     _
             ( \---/ )
              ) . . (
________,--._(___Y___)_,--._______
        `--'           `--'
        FIS[FIlm Searcher]
     tool for searching films 
                    """))
		cetak(golek(args.s))
	except KeyboardInterrupt:
		print("TRL+C detected, exiting.")
		sys.exit()

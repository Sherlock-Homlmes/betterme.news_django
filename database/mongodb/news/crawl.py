import requests
from bs4 import BeautifulSoup
import bs4
import time

from .imgbb_image_process import *
#import re


####split date
def split_date(txt):
	x = txt.split()
	date = x[2].split("/")
	
	for i in range(len(date)):
		date[i] = int(date[i])

	return date


def replace_h1(value):
	#title
	value = value.replace('<h1>','<h1 class="w3-center w3-padding-64"><span class="w3-tag w3-wide">')
	value = value.replace('</h1>','</span></h1>')

	#quote
	#value = value.replace('<ul style="user-select: auto;">','<div class="w3-panel w3-leftbar w3-light-grey">')
	#value = value.replace('</ul>','</div>')


	#print(value)
	return(value)

def test_src_process(need_to_clean):
	end_pos = 0 
	while end_pos >= 0 :
		start_pos = need_to_clean.find('<img',end_pos)
		end_pos = need_to_clean.find('/>',start_pos)
		
		img = need_to_clean[start_pos:end_pos+2:]

		#add break line if don't have
		'''
		break_line_pos = need_to_clean.find('<br>',start_pos) 
		print(start_pos,end_pos,break_line_pos)
		if break_line_pos < 0:
			need_to_clean = need_to_clean[:end_pos+2]+"<br>"+need_to_clean[end_pos+2:]
		'''

		data_src_start_pos = need_to_clean.find('data-src',start_pos)
		data_src_end_pos = need_to_clean.find('"',data_src_start_pos+10)
		data_src = need_to_clean[data_src_start_pos+10:data_src_end_pos:]
		if data_src_start_pos >= 0:
			print(data_src)
			need_to_clean = need_to_clean.replace("https://e.khoahoc.tv/photos/image/holder.png",data_src,1)


	return need_to_clean

def src_process(need_to_clean):
	end_pos = 0 
	while end_pos >= 0 :
		start_pos = need_to_clean.find('<img',end_pos)
		end_pos = need_to_clean.find('/>',start_pos)
		img = need_to_clean[start_pos:end_pos+2:]

		'''
		#add break line if don't have
		break_line_pos = need_to_clean.find('<br>',start_pos) 
		print(start_pos,end_pos,break_line_pos)
		if break_line_pos < 0:
			need_to_clean = need_to_clean[:end_pos+2]+"<br>"+need_to_clean[end_pos+2:]
		'''

		data_src_start_pos = need_to_clean.find('data-src',start_pos)
		data_src_end_pos = need_to_clean.find('"',data_src_start_pos+10)
		data_src = need_to_clean[data_src_start_pos+10:data_src_end_pos:]

		if data_src_start_pos >= 0:
			print(data_src)
			link = imgbb_image(data_src)
			print(link)
			need_to_clean = need_to_clean.replace(data_src,link,1)
			need_to_clean = need_to_clean.replace("https://e.khoahoc.tv/photos/image/holder.png",link,1)


	return need_to_clean

def remove_ads_and_ul(need_to_clean):
	###delete ads
	end_pos = 0 
	while end_pos >= 0 :
		start_pos = need_to_clean.find('<div class="adbox',end_pos)
		end_pos = need_to_clean.find('</div>',start_pos)
		if start_pos >= 0:
			need_to_clean = need_to_clean[0 : start_pos : ] + need_to_clean[end_pos + 5 + 1 : :]

	###delete ul
	end_pos = 0
	while end_pos >= 0:
		pos = need_to_clean.find('<ul' , end_pos+1)
		if pos >= 0:
			stable_pos = need_to_clean.find('<ul' , end_pos+1)
		end_pos = pos

	try:
		start_pos = stable_pos
		end_pos = need_to_clean.find('</ul>',start_pos)
		need_to_clean = need_to_clean[0 : start_pos : ] + need_to_clean[end_pos + 4 + 1 : :]
	except Exception as e:
		print(e)
		print("no ul")

	###delete blockquote(if have)
	end_pos = 0 
	while end_pos >= 0 :
		start_pos = need_to_clean.find('<blockquote',end_pos)
		end_pos = need_to_clean.find('</blockquote>',start_pos)
		if start_pos >= 0:
			need_to_clean = need_to_clean[0 : start_pos : ] + need_to_clean[end_pos + 12 + 1 : :]


	return need_to_clean


def add_str_to_str(str_have:str,str_add:str,where:str):
	add_pos = str_have.find(where)
	string = str_have[:add_pos]+str_add+str_have[add_pos:]

	return string


###########################
def test_crawl(url):
	response = requests.get(url)
	soup = BeautifulSoup(response.content, "html.parser")
	div = soup.find('div', class_='postpage clearfix').find("div",class_="content")

	title = div.findAll("h1")
	title = title[0]

	content = div.findAll("div",{"class":"content-detail"})


	content = remove_ads_and_ul(str(content[0]))
	#print(content)
	content = test_src_process(content)

	author = div.findAll("div",{"class": "author-info"})


##xu ly
	content = str(title) + content
	title = str(title).replace('<h1>','')
	title = title.replace('</h1>','')

	author = str(author[0])
	content += author

	start_pos = author.find('<span class="date">')
	end_pos = author.find('</span>',start_pos)

	author = author[start_pos+19 : end_pos : ]
	date = split_date(author)

	#content = re.sub('<ul>?(.*?)</ul>', '', content,  flags=re.DOTALL)

	responsive = div.findAll("div",{"class": "responsive"})
	if len(responsive) > 0:
		responsive = str(responsive[0])
		replace_responsive = str(responsive).replace("data-src","src")
		content = content.replace(responsive,replace_responsive)


	return [title,content,date]

def crawl(url):
	#crawl
	response = requests.get(url)
	soup = BeautifulSoup(response.content, "html.parser")
	div = soup.find('div', class_='postpage clearfix').find("div",class_="content")

	#take title
	title = div.findAll("h1")
	title = title[0]

	#take content
	content = div.findAll("div",{"class":"content-detail"})

	#remove ads
	content = remove_ads_and_ul(str(content[0]))
	content = src_process(content)

	#take author and date
	author = div.findAll("div",{"class": "author-info"})


##xu ly content
	content = str(title) + content
	title = str(title).replace('<h1>','')
	title = title.replace('</h1>','')

##xu ly author and date
	author = str(author[0])
	content += author

	start_pos = author.find('<span class="date">')
	end_pos = author.find('</span>',start_pos)

	author = author[start_pos+19 : end_pos : ]
	date = split_date(author)

##xu ly video
	responsive = div.findAll("div",{"class": "responsive"})
	if len(responsive) > 0:
		responsive = str(responsive[0])
		replace_responsive = str(responsive).replace("data-src","src")
		content = content.replace(responsive,replace_responsive)


	return [title,content,date]

import time
import requests
from bs4 import BeautifulSoup

#meta:title,description,keyword,og:image
from .imgbb_image_process import imgbb_image
from .news_database import *

def crawl_meta(url):
	#start
	start_time = time.time()

	response = requests.get(url)
	soup = BeautifulSoup(response.content, "html.parser")
	head = soup.find('head')
	meta = head.findAll('meta')

	for m in meta:
		if m.get('name') == 'description':
			description = m.get('content')
			#print(m)
		elif m.get('name') == 'keywords':
			#print(m)
			keywords = m
		elif m.get('property') == 'og:image':
			#print(m)
			og_image = m.get('content')
			
	end_time = time.time()
	print('Total all time meta elapsed: %.6f seconds' % (end_time - start_time))

	#print(description)
	#print(keywords)
	return [str(description),str(keywords),str(og_image)]

#internal link
from .news_database import topic_count
import random

def internal_link(topic_list:list,number_select:int):
	all_position = []
	for topic in topic_list:
		all_position.extend(topic_count(topic)["position"])

	random_list = random.sample(all_position, number_select)

	internal_link = find_pos(random_list)

	return internal_link

def seo_blockquote(add_list:list):
	pass

def seo_ul(topic_list:list):
	string_ul = '<ul style="user-select: auto">'
	for topic in topic_list:
		string_ul += '<li style="user-select: auto"><a title={} href="https://betterme.news/{}" style="user-select: auto">{}</a></li>'.format("'"+topic["title"]+"'",topic["name"],topic["title"])
	string_ul += '</ul>'

	return string_ul

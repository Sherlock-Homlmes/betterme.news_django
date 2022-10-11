import requests
from bs4 import BeautifulSoup

import io, json

from database.mongodb.news.crawl import *
from database.mongodb.news.add_new_data import *
from database.mongodb.news.news_database import *

topic = ["khoa-hoc","lich-su","dia-ly","sinh-hoc",
         "10-van-cau-hoi-vi-sao","su-that-thu-vi","1001-bi-an","danh-nhan-the-gioi","the-gioi-dong-vat",
         "y-hoc-suc-khoe","kien-truc-doc-dao"]

def scrap_by_page_number(number):
	response = requests.get(f"https://khoahoc.tv/?p={number}")
	soup = BeautifulSoup(response.content, "html.parser")

	post_view = soup.find('div', class_='slider')
	post_view = post_view.find("ul")

	post_dict = {}
	
	for tempo in post_view:
		#print(tempo.prettify())
		#title
		title = tempo.find('a')
		title_content = title.contents[3].getText()
		href = title.get("href")

		#thumb
		thumb = title.find('img')
		thumb_alt = thumb.get('alt')
		thumb_src = thumb.get('src')

		
		#desc
		desc = ""
		#h
		post_dict[f"{href}"] = {
		"title_content": title_content,
		"thumb_src": thumb_src,
		#"thumb_alt": thumb_alt,
		"description": desc}

	post_view = soup.findAll('div', class_='listview')

	for view in post_view:
		temporary = view.findAll('li', class_='listitem clearfix')
		for tempo in temporary:
			###include: title, thumb, desc

			#title
			title = tempo.find('a','title')
			title_content = title.contents[0]
			href = title.get("href")

			#thumb
			thumb = tempo.find('a',class_='thumb')
			thumb = thumb.find('img')
			thumb_alt = thumb.get('alt')
			thumb_src = thumb.get('data-src')

			
			#desc
			desc = tempo.find('div',class_='desc')
			desc = desc.contents[0]

			#h
			post_dict[f"{href}"] = {
			"title_content": title_content,
			"thumb_src": thumb_src,
			#"thumb_alt": thumb_alt,
			"description": desc
			}

	del_list = None
	del_list = []
	
	for key in post_dict.keys():
		if take_ndb('name',title_process(key)):
			del_list.append(key)
	for key in del_list:
		del post_dict[key]

	with io.open('main/views/check_data.json', 'w', encoding='utf-8') as f:
		json.dump(post_dict, f, ensure_ascii=False, indent=4)
		
	return post_dict

def title_process(title:str) -> str:
	title = title[1::]
	tit = title.split("-")
	tit.pop()

	title = '-'.join(tit)
	return title


##### process after scrap
async def auto_scrap_process(check_list:list,html_type_list:list,tags_list:list):
	#print(check_list,html_type_list,tags_list)
	for check in check_list:
		html = None
		tag = None
		tag  = []
		for html_type in html_type_list:
			if html_type.startswith(check):
				html_type = html_type.split("|||")[1]
				if html_type not in ["normal","horror"]:
					return False
				else:
					html = html_type
					
		for tags in tags_list:
			if tags.startswith(check):
				tags = tags.split("|||")[1]
				if tags not in topic:
					return False
				else:
					tag.append(tags)	
					

		#print(f"html: {html}")
		#print(f"tag: {tag}")

		###create data
		url = "https://khoahoc.tv/"+check
		name =  title_process(check)
		html_type = html

		with open('main/views/check_data.json', encoding='utf-8') as f1:
			all_post = json.load(f1)

		thumb_src = all_post[check]['thumb_src']
		if "650x340" in thumb_src:
			slide_show_link = thumb_src
			thumbnail_link = ""
			print("slide show link")
		else:
			slide_show_link = ""
			thumbnail_link = thumb_src
			print("thumbnail link")
		
		description = all_post[check]['description']
		tags = tag
		
		data = await create_data(url,name,html_type,thumbnail_link,slide_show_link,description,tags)
		ndb(data)



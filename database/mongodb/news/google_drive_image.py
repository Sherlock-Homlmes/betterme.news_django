import wget
import os
import time
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
gauth = GoogleAuth()           
drive = GoogleDrive(gauth) 

def save_image(url):
	image = wget.download(url)
	#print(image)

	return image

def delete_image(image):
	time.sleep(5)
	os.remove(image)
	print("delete done")	

def xu_ly_link(link:str):
	x = link.split("/view")
	x = x[0].split("/")
	view = "https://drive.google.com/uc?export=view&id="+x[5]
	return view

def upload_drive_image(image):
	gfile = drive.CreateFile({'parents': [{'id': '1HklGuq0Oh0LvA5tEG8NBButSqV25_S3n'}]})
	
	gfile.SetContentFile(image)
	gfile.Upload() # Upload the file.

	file_list = drive.ListFile({'q': "'{}' in parents and trashed=false".format('1HklGuq0Oh0LvA5tEG8NBButSqV25_S3n')}).GetList()

	for file in file_list:
		title = file["title"]
		if title == image:
			link = xu_ly_link(file["alternateLink"])
			print(link)
			return link

def drive_image(url:str):
	image = save_image(url)
	link = upload_drive_image(image)
	delete_image(image)

	return link

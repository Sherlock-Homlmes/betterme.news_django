import os
from dotenv import load_dotenv
from facebook import GraphAPI
from facebook import auth_url
import wget
import time

load_dotenv()
page_id = os.getenv("page_id")
access_token = os.getenv("access_token")
app_id = os.getenv("app_id")
app_secret = os.getenv("app_secret")

fb_news_page = GraphAPI(access_token = access_token)

def save_image(url):
    image = wget.download(url)

    return image
def delete_image(image):
    os.remove(image)
    print("delete done")

def fb_post(message:str,picture_url:str,post_url:str):

    if picture_url != "" and post_url != "":
        message += "Xem them chi tiet tai: "+ post_url
        image = save_image(picture_url)
        post = fb_news_page.put_photo(image=open(image, 'rb'),message=message)
        delete_image(image)
    elif picture_url != "":
        image = save_image(picture_url)
        post = fb_news_page.put_photo(image=open(image, 'rb'),message=message)
        delete_image(image)
    elif post_url != "":
        post = fb_news_page.put_object("me","feed",message=message, link=post_url)
    else:
        post = fb_news_page.put_object("me","feed",message=message)

    print(post)
    post_id = post["id"]
    fb_news_page.put_like(object_id=post_id)
    return post_id

#dang bai
message = '''
Hom nay blah blah
'''
#picture_link = "https://i.ibb.co/Jj1nYBk/image.jpg"
hastags = ['khoahoc','lichsu']
picture_link = ""
post_url="https://khoahoc.tv/phat-minh-moi-tai-che-rac-thai-vai-bong-thanh-vai-moi-gia-tri-cao-121714?fbclid=IwAR25wok1dMglv2FamfEQ9sWJpcprjdMzI8QNoSMRSTAWw8_EBmpEdJcjSHQ"

for hastag in hastags:
    message += "#"+hastag+" "
print(message)
#post_id = fb_post(message,picture_link,post_url)

#them comment
comment = "chao cac ong chau"
#print(fb_news_page.put_comment(object_id=post_id,message=comment))

canvas_url = "https://127.0.0.1/facebook/"
perms = ["manage_pages","publish_pages"]
fb_login_url = auth_url(app_id, canvas_url, perms)
print(fb_login_url)
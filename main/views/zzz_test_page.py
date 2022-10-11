#django
from django.http import HttpResponse, JsonResponse
from django.template.response import TemplateResponse

#loader
async def return_data(request):
  data = {
    '0':{
    "name": "Nguyen Van A",
    "job": "Py dev"
    },
    '1':{
    "name": "Nguyen Van B",
    "job": "Nodejs dev"
    },    
  }
    
  return JsonResponse(data)
async def loader(request):
  return TemplateResponse(request,'loader_lion.html',{})

async def video_call(request):
  #return TemplateResponse(request,'video-call.html',{})
  return TemplateResponse(request,'video1.html',{})
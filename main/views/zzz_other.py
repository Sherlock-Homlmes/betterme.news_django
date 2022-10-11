from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.http import HttpResponse

async def robot_txt(request):

    content = '''
<pre style="word-wrap: break-word; white-space: pre-wrap;">
User-agent: *
Allow: /
Crawl-delay: 3 
</pre>
    '''

    return HttpResponse(content)

async def about_us(request):

  return TemplateResponse(request,"other/about-us.html",{"request":request})

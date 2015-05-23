from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def home_page(request):
    html_start = '<html>'
    html_end = '</html>'
    title = '<title>To-Do lists</title>'
    return HttpResponse(html_start + title + html_end)
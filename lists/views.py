from django.http import HttpResponse
from django.shortcuts import render, redirect
from lists.models import Item, List

only_one_url = '/lists/the-only-list-in-the-world/'
def home_page(request):
    return render(request, 'home.html')

def view_list(request):
    items = Item.objects.all()
    return render(request, 'list.html', {'items': items})

def new_view(request):
    list_ = List.objects.create()
    new_item = request.POST['item_text']
    Item.objects.create(text=new_item, list=list_)
    return redirect(only_one_url)

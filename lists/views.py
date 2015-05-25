from django.http import HttpResponse
from django.shortcuts import render, redirect
from lists.models import Item

only_one_url = '/lists/the-only-list-in-the-world/'
def home_page(request):
    return render(request, 'home.html')

def view_list(request):
    items = Item.objects.all()
    return render(request, 'list.html', {'items': items})

def new_view(request):
    new_item = request.POST['item_text']
    Item.objects.create(text=new_item)
    return redirect(only_one_url)

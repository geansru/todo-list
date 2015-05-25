from django.http import HttpResponse
from django.shortcuts import render, redirect
from lists.models import Item, List

only_one_url = '/lists/the-only-list-in-the-world/'
def home_page(request):
    return render(request, 'home.html')

def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    # items = Item.objects.filter(list=list_)
    # return render(request, 'list.html', {'items': items})
    return render(request, 'list.html', {'list': list_})

def new_list(request):
    list_ = List.objects.create()
    new_item = request.POST['item_text']
    Item.objects.create(text=new_item, list=list_)
    url = '/lists/%d/' % (list_.id, )
    return redirect(url)

def new_view(request):
    list_ = List.objects.create()
    new_item = request.POST['item_text']
    Item.objects.create(text=new_item, list=list_)
    url = '/lists/%d/' % (list_.id, )
    return redirect(url)

def add_item(request, list_id):
    list_ = List.objects.get(id=list_id)
    new_item = request.POST['item_text']
    Item.objects.create(text=new_item, list=list_)
    url = '/lists/%d/' % (list_.id, )
    return redirect(url)
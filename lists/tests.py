from django.core.urlresolvers import resolve
from django.template.loader import render_to_string
from django.test import TestCase
from lists.views import home_page
from django.http import HttpRequest
from lists.models import Item, List
# Create your tests here.

class NewListTest(TestCase):
    url_old = '/lists/the-only-list-in-the-world/'
    url = '/lists/new'
    item_text = 'A new list_item'

    def test_saving_a_POST_request(self):
        data={'item_text': self.item_text}
        self.client.post(self.url, data=data)
        self.assertEqual(Item.objects.count(), 1)

        new_item = Item.objects.first()
        self.assertEqual(new_item.text, self.item_text)

    def test_redirects_after_POST(self):
        data={'item_text': self.item_text}
        response = self.client.post(self.url, data=data)
        self.assertRedirects(response, self.url_old)

class ListAndItemModelsTest(TestCase):

    def test_first_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()

        first_item_text = 'The first (ever) list item'
        first_item = Item()
        first_item.text = first_item_text
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item_text = 'Item the second'
        second_item.text = second_item_text
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, first_item_text)
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, second_item_text)
        self.assertEqual(second_saved_item.list, list_)

    def test_home_page_only_saves_item_when_necessary(self):
        request = HttpRequest()
        home_page(request)
        self.assertEqual(Item.objects.count(), 0)

class HomePageTest(TestCase):
    def test_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home.html')
        self.assertEqual(response.content.decode(), expected_html)

class ListViewTest(TestCase):
    url = '/lists/the-only-list-in-the-world/'

    def test_uses_list_temlplate(self):
        response = self.client.get(self.url)
        # print(response.content.decode())
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_all_items(self):
        list_ = List.objects.create()
        Item.objects.create(text='itemey 1', list=list_)
        Item.objects.create(text='itemey 2', list=list_)

        response = self.client.get(self.url)
        content = response.content.decode()

        self.assertIn('itemey 1', content)
        self.assertIn('itemey 2', content)

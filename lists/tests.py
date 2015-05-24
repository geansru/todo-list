from django.core.urlresolvers import resolve
from django.template.loader import render_to_string
from django.test import TestCase
from lists.views import home_page
from django.http import HttpRequest
from lists.models import Item
# Create your tests here.
class SmokeTest(TestCase):
    def test_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home.html')
        self.assertEqual(response.content.decode(), expected_html)

    def test_home_page_can_save_a_POST_request(self):
        request = HttpRequest()
        request.method = 'POST'
        list_item = 'A new list item'
        request.POST['item_text'] = list_item

        response = home_page(request)

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, list_item)

    def test_home_page_redirects_after_POST(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'A new list item'

        response = home_page(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')

class ItemModelsTest(TestCase):

    def test_first_saving_and_retrieving_items(self):
        first_item_text = 'The first (ever) list item'
        first_item = Item()
        first_item.text = first_item_text
        first_item.save()

        second_item = Item()
        second_item_text = 'Item the second'
        second_item.text = second_item_text
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, first_item_text)
        self.assertEqual(second_saved_item.text, second_item_text)

    def test_home_page_only_saves_item_when_necessary(self):
        request = HttpRequest()
        home_page(request)
        self.assertEqual(Item.objects.count(), 0)

    def test_home_page_can_save_a_POST_request(self):
        item_text = 'A new list item'
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = item_text

        response = home_page(request)

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, item_text)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')

class HomePageTest(TestCase):

    def test_home_page_displays_all_list_items(self):
        item_text = 'itemey %d'
        count = 2
        for x in range(count):
            text = item_text % x
            Item.objects.create(text=text)
        # Item.objects.create(text='itemey 2')

        request = HttpRequest()
        response = home_page(request)
        content = response.content.decode()

        self.assertIn('itemey 1', content)
        # self.assertIn('itemey 2', content)

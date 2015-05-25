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
        new_list = List.objects.first()
        url = '/lists/%d/' % (new_list.id, )
        self.assertRedirects(response, url)

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
    lists_url_tmplt = '/lists/%d/'

    def url_helper(self, list_):
        return self.lists_url_tmplt % list_.id

    def helper(self):
        return List.objects.create()

    def test_uses_list_temlplate(self):
        list_ = self.helper()
        url = self.url_helper(list_)
        # print(url)
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_only_items_for_that_list(self):
        correct_list = self.helper()

        # lambda helper's
        count = 2
        itemey = lambda x : "itemey " + str(x)
        itemey_other = lambda x : "other list item " + str(x)
        rng = lambda: range(1, count + 1)

        for x in rng():
            Item.objects.create(text=itemey(x), list=correct_list)

        other_list = self.helper()

        for x in rng():
            Item.objects.create(text=itemey_other(x), list=other_list)

        url = self.url_helper(correct_list)
        response = self.client.get(url)

        for x in rng():
            self.assertContains(response, itemey(x))
            self.assertNotContains(response, itemey_other(x))

    def test_displays_all_items(self):
        list_ = List.objects.create()
        Item.objects.create(text='itemey 1', list=list_)
        Item.objects.create(text='itemey 2', list=list_)

        response = self.client.get(self.url_helper(list_))
        content = response.content.decode()

        self.assertIn('itemey 1', content)
        self.assertIn('itemey 2', content)

    def test_passes_correct_list_to_template(self):
        other_list = self.helper()
        correct_list = self.helper()

        url = self.url_helper(correct_list)
        response = self.client.get(url)

        self.assertEqual(response.context['list'], correct_list)

class NewTestItem(TestCase):

    def helper(self):
        return List.objects.create()

    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = self.helper()
        correct_list = self.helper()
        url_tmplt = '/lists/%d/add_item'
        add_url = url_tmplt % (correct_list.id, )
        text = 'A new item for an existing list'
        data = { 'item_text': text }
        self.client.post(add_url, data=data)

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, text)
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_to_list_view(self):
        other_list = self.helper()
        correct_list = self.helper()
        url_list = '/lists/%d/'
        url_tmplt = url_list + 'add_item'
        add_url = url_tmplt % (correct_list.id, )
        text = 'A new item for an existing list'
        data = { 'item_text': text }

        response = self.client.post(add_url, data=data)
        show_url = url_list % (correct_list.id, )
        self.assertRedirects(response, show_url)

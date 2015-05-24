from django.core.urlresolvers import resolve
from django.template.loader import render_to_string
from django.test import TestCase
from lists.views import home_page
from django.http import HttpRequest

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
        content = response.content.decode()
        self.assertIn(list_item, content)
        expected_html = render_to_string(
            'home.html',
            {'new_item_text': 'A new list item'}
        )
        self.assertEqual(content, expected_html)
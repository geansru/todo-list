# -*- coding: utf-8 -*-
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import time
import sys

__author__ = 'noskill'
from selenium import webdriver
import unittest

class NewVisitorTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
        self.title = 'To-Do'

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Edith has heard about a cool new online to-do app. She goes to check
        # out its homepage
        # self.browser.get(self.live_server_url)
        self.browser.get(self.server_url)

        # She notices the page title and header mention to-do lists
        self.assertIn(self.title, self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn(self.title, header_text)

        # She is invited to enter a to-do item straight away
        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            input_box.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # She types 'Buy peacock feathers' into a text box (Edith's hobby is
        # tying fly-fishing lures)
        input_box.send_keys('Buy peacock feathers')

        asserts = [
            '%d: Buy peacock feathers',
            '%d: Use peacock feathers to make a fly',
        ]

        # When she hits enter, the page updates, and now the page lists
        # "1: Buy peacock feathers" as an item in a to-do list table
        input_box.send_keys(Keys.ENTER)
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')
        self.check_for_row_in_list_table(asserts[0] % 1)

        # There is still a text box inviting her to add another item. She enters
        # "Use peacock feathers to make a fly" (Edith is very methodical)
        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys('Use peacock feathers to make a fly')
        input_box.send_keys(Keys.ENTER)

        # The page updates again, and shows both items on her list
        for i in range(0, len(asserts)):
            number = i + 1
            assert_string = asserts[i] % number
            self.check_for_row_in_list_table(assert_string)

        # Now a new user, Francis, comes along to the site
        # # We use a new browser session to make sure that no information
        # # of Edith's is coming through from cookies etc
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Francis visits the home page. There is no sign of Edith's list
        self.browser.get(self.server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        # Francis starts s new list by entering a new item. He is less
        # interesting that Edith
        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys('Buy milk')
        input_box.send_keys(Keys.ENTER)

        # Francis gets his own unique URL
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEquals(francis_list_url, edith_list_url)

        # Again, there is no trace of Edith's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)

        # Satisfied, they both go back to sleep

        # Edith wonders whether the site will remember her list. Then she sees
        # that the site has generate a unique URL for her -- there is some
        # explanatory text to that effect

        # self.fail('Finish the test!')

        # She visits that URL - her to-do list is still there.

        # Satisfied, she goes back to sleep

    def test_layout_and_stylish(self):
        # Helpers
        delta = 8
        x = 512
        get_input = lambda: self.browser.find_element_by_id('id_new_item')
        get_location = lambda: input_box.location['x'] + input_box.size['width']/2
        check_center = lambda: self.assertAlmostEqual(input_box_location, x, delta=delta)

        # Edith goes to the home page
        self.browser.get(self.server_url)
        self.browser.set_window_size(1024, 768)
        # She notices the input box is nicely centered
        input_box = get_input()
        input_box_location = get_location()
        check_center()

        # She starts a new list and sees the input is nicely centered there too
        input_box.send_keys('testing\n')
        input_box = get_input()
        input_box_location = get_location()
        # self.assertAlmostEqual(input_box_location, x, delta=delta)
        check_center()

    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_url = 'http://' + arg.split('=')[1]
                return
        super().setUpClass()
        cls.server_url = cls.live_server_url

    @classmethod
    def tearDownClass(cls):
        if cls.server_url == cls.live_server_url:
            super().tearDownClass()

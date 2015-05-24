# -*- coding: utf-8 -*-
from selenium.webdriver.common.keys import Keys
import time

__author__ = 'noskill'
from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
        self.title = 'To-Do'

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Edith has heard about a cool new online to-do app. She goes to check
        # out its homepage
        self.browser.get('http://localhost:8000')

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

        # When she hits enter, the page updates, and now the page lists
        # "1: Buy peacock feathers" as an item in a to-do list table
        input_box.send_keys(Keys.ENTER)

        time.sleep(3)
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')

        self.assertTrue(
            any(row.text == '1: Buy peacock feathers' for row in rows),
            msg="New to-do item did not appear in the table -- its text was %s" % (table.text)
        )

        # There is still a text box inviting her to add another item. She enters
        # "Use peacock feathers to make a fly" (Edith is very methodical)
        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys('Use peacock feather to make a fly')
        input_box.send_keys(Keys.ENTER)

        # The page updates again, and shows both items on her list
        table = self.browser.find_elements_by_id('id_list_table')
        rows = self.browser.find_elements_by_tag_name('tr')
        ary = [row.text for row in rows]
        asserts = [
            '%d: Buy peacock feathers',
            '%d: Use peacock feathers to make a fly',
        ]
        for i in range(0, len(asserts)):
            number = i + 1
            assert_string = asserts[i] % number
            # print(assert_string)
            self.assertIn(assert_string , ary)
        # self.assertIn(, ary)




        # [...]
        self.fail('Finish the test!')

if __name__ == '__main__':
    unittest.main(warnings='ignore')
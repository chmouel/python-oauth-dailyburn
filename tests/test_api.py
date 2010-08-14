#!/usr/bin/python
# -*- encoding: utf-8 -*-
#
# Chmouel Boudjnah <chmouel@chmouel.com>
import unittest
from dailyburn.constants import CONSUMER_KEY, CONSUMER_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET
from dailyburn.api import API

class testAPI(unittest.TestCase):
    def setUp(self):
        self.api = API(CONSUMER_KEY, CONSUMER_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

    def test_food_search(self):
        #self.assert_(self.api.FoodSearch("cranberries")[0].has_key('food'))
        pass
    
    def test_user_detail(self):
        from pprint import pprint as p
        p(self.api.UserDetail())

    def test_food_nutrition_label(self):
        #print self.api.NutritionLabel(123841)
        pass

    
        
if __name__ == '__main__':
    unittest.main()

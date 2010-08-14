#!/usr/bin/python
# -*- encoding: utf-8 -*-
#
# Chmouel Boudjnah <chmouel@chmouel.com>
import urllib

from dailyburn.oauth import OAuthApi

class API(object):
    def __init__(self, consumer_key, consumer_secret, token=None, token_secret=None):
        self.oauth = OAuthApi(consumer_key, consumer_secret, token=token, token_secret=token_secret)

    def UserDetail(self):
        return self.oauth.ApiCall("users/current", "GET", {})

    def FoodSearch(self, **dico):
        """Search Food in Database
        Required parameters to pass:
        input - The search term entered by the user.
        Optional parameters:
        page - The page # of results to return.
        per_page - The # of results to return per page (max is 25).
        sort_by - How to order the results; calories, total_fat, total_carbs, protein, or name.
                 (If not set it defaults to a "best match" algorithm.)
        reverse - Set to true to reverse the sorting order.        
        """
        if not 'input' in dico:
            #TODO: APIError
            raise Exception("input is missing") 
        return self.oauth.ApiCall("foods/search", "GET", dico)

    def FoodLabel(self, foodId):
        foodId = int(foodId) #Todo: proper type checking
        foodId = urllib.quote(str(foodId))
        return urllib.urlopen("https://dailyburn.com/api/foods/%s/nutrition_label" % foodId).read()        

    def FoodFavorites(self):
         return self.oauth.ApiCall("foods/favorites", "GET", {})

    def FoodFavoriteAdd(self, foodId):
        foodId = int(foodId) #Todo: proper type checking
        return self.oauth.ApiCall("foods/add_favorite", "POST", { "id" : foodId })
        
    def FoodFavoriteRemove(self, foodId):
        foodId = int(foodId) #Todo: proper type checking
        return self.oauth.ApiCall("foods/delete_favorite", "POST", { "id" : foodId })

    def FoodMeals(self):
        return self.oauth.ApiCall("foods/meal_names", "GET", {})        

    def FoodLog(self, **dico):
        """  Getting Food Log Entries.

        This call accepts 1 optional parameter named
        "date", which should be a date-formatted string (YYYY-MM-DD). If no
        "date" parameter is given then the default is "today" in the current
        user's local timezone."""
        return self.oauth.ApiCall("food_log_entries", "GET", dico)
        
    def FoodLogEntry(self, **dico):
        """Creating Food Log Entries

        Required parameters:
        ====================
        
        food_id - The id of the food the user has eaten.
        servings_eaten - How many servings the user ate of the food.

        Optional parameters
        ===================
        
        logged_on - The user-selected date when they ate the food
        (defaults to "today" for the user).

        meal_name_id - The id of the meal_name that the entry was
        created with (defaults to uncategorized, see "Getting Meal
        Names" call for requesting supported meal_name id's).
        """
        for _type in ('food_id', 'servings_eaten'):
            if not _type in dico:
                raise Exception("%s is missing" % _type) 
        pass

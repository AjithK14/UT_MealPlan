### Algorithm to build a meal from a menu of dishes ###

"""
build_meals(dishes, boundaries_filename)
main algorithm that builds the meal to meet the boundaries

sort_meal(meal, attribute)
for finding meal with highest amount of a nutrient

rank_meals(meals)
input: a list of meals
output: a sorted list of meals with descending avg deviation

-get_food_info(menu_url)
helper method to get foodnames and foodfacts
"""

import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import sys
import re
from Dish import *
from Meal import *
from menu_crawler import *
import random

__author__ = "Ajith Kemisetti"
__email__ = "kemisettia@gmail.com"
__date__ = "8/16/2019"

"""
main algorithm that builds the meal to meet the boundaries

input: list of dishes and spreadsheet of boundaries(row:nutrient,col:LB,IA,etc.)
***not doing spreadsheet, just dict for now
****I'll have to figure out spreadsheet stuff -- hardcode for now
(hardcoding is fine for personal use but to make it an app for everyone...)
output: a single meal
"""
def build_meal(dishes, lower_boundaries, upper_boundaries):
	#reject if there simply aren't enough meals
	if len(dishes) < 10:
		return "NOT ENOUGH DISHES TO MAKE A MEAL"
	nutrient_reject = {x:0 for x in TARGET_NUTRIENTS}
	myMeal = Meal(lower_boundaries)
	#descending list of foods with most of each respective nutrient
	sorted_nutrients = {nutrient: sorted(dishes, 
		key=lambda x: x.nutrition[nutrient],reverse=True) for nutrient in TARGET_NUTRIENTS}
	while True:
		highest_unmet = myMeal.nutrient_totals()[0]
		index = 0
		dish = random.choice(sorted_nutrients[highest_unmet][0:int(len(dishes)/2)])
		while myMeal.containsDish(dish):
			index+=1
			dish = sorted_nutrients[highest_unmet][index]
		# print("We need {} so we add {}".format(highest_unmet,dish.name))
		myMeal.addDish(dish)
		# print(myMeal)
		constraint = myMeal.under_upper_bounds(upper_boundaries)
		if constraint[0]:
			if myMeal.all_nutrients_met():
				return myMeal
		else:
			# print("Too much of the {} nutrient".format(constraint[1]))
			myMeal.removeDish(dish.name)
			# print("Removed {}".format(dish.name))
			nutrient_reject[constraint[1]]+=1
			if nutrient_reject[constraint[1]] > 3 and not myMeal.isEmpty():
				sorted_meal = myMeal.sort_by_nutrient(constraint[1])
				myMeal.removeDish(sorted_meal[-1])
				# print("Also removed {} because of excess {}".format(sorted_meal[-1],
					# constraint[1]))
				nutrient_reject[constraint[1]] = 0
		# print(myMeal.meal_score())
		# print()
	return myMeal
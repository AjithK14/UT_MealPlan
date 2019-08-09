### Meal class ###
""" this class stores a meal of individual dishes """

import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import sys
import re
from menu_crawler import *

__author__ = "Ajith Kemisetti"
__email__ = "kemisettia@gmail.com"
__date__ = "8/16/2019"

class Meal:

	def __init__(self, boundaries):
		self.items = {}
		self.totals = {nutrient: 0 for nutrient in TARGET_NUTRIENTS}
		self.boundaries = boundaries

	def addDish(self,dish):
		""" adds a new dish to the meal """
		self.items[dish.name] = dish
		for nutrient in TARGET_NUTRIENTS:
			self.totals[nutrient]+=dish.nutrition[nutrient]

	def removeDish(self, dishname):
		if dishname not in self.items:
			return
		self.totals = {nutrient: 
		self.totals[nutrient]-self.items[dishname].nutrition[nutrient] 
		for nutrient in TARGET_NUTRIENTS}
		del self.items[dishname]

	def containsDish(self,dish):
		""" returns true if the meal contains the dish """
		return dish.name in self.items.keys()

	def getDishes(self):
		""" returns all dishes currently in the meal """
		return self.items

	def get_nutrient_total(self,nutrient):
		""" returns the total of a particular nutrient """
		return self.totals[nutrient]

	def nutrient_totals(self):
		""" returns ascending list of total nutrients in the meal--for next unmet nutrient"""
		differences = {x:self.totals[x]-self.boundaries[x] for x in TARGET_NUTRIENTS}
		return sorted(TARGET_NUTRIENTS,key=differences.__getitem__)

	def all_nutrients_met(self):
		""" returns a boolean on whether all the nutrient bounds have been met """
		for key in self.boundaries:
			if self.totals[key] < self.boundaries[key]:
				return False
		return True

	def under_upper_bounds(self, upper_bounds):
		""" make sure no nutrient has exceeded upper boundary """
		for key in upper_bounds:
			if self.totals[key] > upper_bounds[key]:
				return False, key
		return True, 0

	def meal_score(self):
		""" for now it is just average deviation from self.boundaries """
		count = 0
		total = 0
		for key in self.boundaries:
			total+=abs(self.totals[key]-self.boundaries[key])
			count+=1
		return total/count

	def sort_by_nutrient(self,nutrient):
		""" sort the meal by the desired nutrient """
		foods = list(self.items.keys())
		foods_nutrients = {x: self.items[x].nutrition[nutrient] for x in foods}
		return sorted(foods, key=foods_nutrients.__getitem__)

	def isEmpty(self):
		""" does the meal have any dishes in it? """
		return len(self.items)==0

	def __str__(self):
		""" print method """
		return_strings = []
		for dish in self.items:
			macros = " ".join(["{}:{}g".format(nutrient, self.items[dish].nutrition[nutrient]) 
				for nutrient in TARGET_NUTRIENTS])
			return_strings.append("{} ({})".format(dish,macros))
		return_strings.append(str(self.totals))
		return "\n".join(return_strings)

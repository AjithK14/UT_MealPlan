"""

   Main program that will take nutrition information
   from a single menu and apply the algorithm to craft a meal

"""
import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import sys
import re
from Dish import *
from Meal import *
from menu_crawler import *
from meal_builder import *
import random

__author__ = "Ajith Kemisetti"
__email__ = "kemisettia@gmail.com"
__date__ = "8/16/2019"

#test url
TEST_MENU = "http://hf-foodapp.austin.utexas.edu/select?meal=Lunch&loc=Jester%202nd%20Floor%20Dining"

TEST_LB = {"Calories": 500, "Protein": 38, "Fats": 19, "Carbs": 44}
TEST_UB = {"Calories": 600, "Protein": 60, "Fats": 27, "Carbs": 75}

OPTIONS = MEALS + ["Quit"]

def print_options(mymenu):
	print()
	for i in range(len(mymenu)):
		print("{}. {}".format(i+1,mymenu[i]))
	print()

def is_invalid(choice,total_choices):
	return ((not choice.isdigit()) or (int(choice)>total_choices) or (int(choice)==0))

def main():
	while True:

		#user picks meal
		print_options(OPTIONS)
		choice = input("Which meal?: ")
		if is_invalid(choice,len(OPTIONS)):
			print()
			print("Please type a number from the menu!")
			print()
			continue
		choice = int(choice)
		if choice == 4:
			print()
			break

		#user picks dining hall
		locations = get_locations(MEALS[choice-1])
		print_options(locations + ["Quit"])
		choice_2 = input("Which available dining hall?: ")
		if is_invalid(choice_2,len(locations)+1):
			print()
			print("Please type a number from the menu!")
			print()
			continue
		choice_2 = int(choice_2)
		if choice_2 == len(locations)+1:
			print()
			break

		#meal is built
		testMeal = Meal({})
		dishes = crawl_menu(get_menu_url(MEALS[choice-1],locations[choice_2-1]),
			red_meat=False,fish=False)
		meal = build_meal(dishes,TEST_LB,TEST_UB)
		print()
		print(meal)
		if not isinstance(meal,str):
			print(meal.meal_score())

if __name__ == "__main__":
	main()
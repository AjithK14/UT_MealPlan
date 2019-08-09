### Web Crawler to extract information from a single menu ###

"""
-create_nutrition_spreadsheet(menu_url)
*method just for display/visualization purposes
returns spreadsheet with nutrition information

-crawl_menu(menu_url, red_meat=False, vegetarian=False)
returns a list of dishes for the algorithm to use

-get_food_info(menu_url)
helper method to get foodnames and foodfacts

-get_locations(meal)
returns all locations currently providing said meal

-get_menu_url(meal, loc)
retreives menu url given meal name and location

Constants:
-MENU_URL
URL of menu being used for testing

-TARGET_NUTRIENTS
All of the nutrients being used to build the meal

-MEALS
All of the possible meals, in chronological order
"""

import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import sys
import re
from Dish import *

__author__ = "Ajith Kemisetti"
__email__ = "kemisettia@gmail.com"
__date__ = "8/16/2019"

#URL of menu for testing
MENU_URL = "http://hf-foodapp.austin.utexas.edu/select?meal=Lunch&loc=Jester%202nd%20Floor%20Dining"

#Target nutrients - all units in grams
TARGET_NUTRIENTS = ["Calories", "Fats", "Carbs", "Protein"]

#All possible meals in chronological order
MEALS = ["Breakfast", "Lunch", "Dinner"]

"""
Retreives menu url given meal name

input: meal string
output: array of locations
"""
def get_locations(meal):

	my_url = "http://hf-foodapp.austin.utexas.edu/location?meal={}".format(meal)

	#GET PAGE HTML
	uClient = uReq(my_url)
	page_html = uClient.read()
	uClient.close()

	#EXTRACT LOCATION INFORMATION
	page_soup = soup(page_html,'html.parser')
	location_bodies = page_soup.findAll("div",attrs={'class':'jumbotron'})

	return [x.find('strong').text for x in location_bodies]

"""
Retreives menu url given meal name

input: meal string and location string
output: array of locations
"""
def get_menu_url(meal, loc):

	if loc not in get_locations(meal):
		return "THIS DINING HALL IS NOT CURRENTLY SERVING FOOD"

	my_url = "http://hf-foodapp.austin.utexas.edu/select?meal={}&loc={}".format(meal,
		loc.replace(" ","%20"))

	return my_url

"""
Helper method to get foodnames and foodfacts

input: menu_url
output: foodnames, foodfacts
"""
def get_food_info(menu_url):

	#GET PAGE HTML
	uClient = uReq(menu_url)
	page_html = uClient.read()
	uClient.close()

	#EXTRACT TABLE INFORMATION
	page_soup = soup(page_html,'html.parser')
	table = page_soup.find("table",attrs={'class':'table table-bordered'})
	table_body = table.find('tbody')
	foodnames = table.findAll('tr',attrs={'id':re.compile('^[0-9]*-row')})
	foodfacts = table.findAll('section',attrs={'class':'performance-facts'})

	return foodnames, foodfacts

"""
Returns a list of dishes for the algorithm to use

input: menu url, eats red meat?, vegetarian?, vegan? (by default eats everything)
output: list of all dishes in menu
"""
def crawl_menu(menu_url, red_meat=True, fish=True, vegetarian=False, vegan=False):
	
	foodnames, foodfacts = get_food_info(menu_url)
	menu_dishes = []

	for i in range(len(foodnames)):
		
		food = foodnames[i].find('span').text
		tags = foodnames[i].findAll('img')
		#for vegetarians or non redmeat eaters
		foodtags = [tags[i]["src"].split("/")[-1].replace('.gif','') for i in range(len(tags))]
		
		if vegetarian and not set(foodtags).intersection({'veggie','vegan'}):
			continue
		if vegan and not set(foodtags).intersection({'vegan'}):
			continue
		if not red_meat and set(foodtags).intersection({'beef','pork'}):
			continue
		if not fish and set(foodtags).intersection({'fish'}):
			continue

		serving_size = " ".join(foodfacts[i].find('p').text.split(" ")[2:])
		calories = foodfacts[i].find('span').text.split(' ')[1]
		stats = foodfacts[i].findAll('th',attrs={'colspan':"2"})
		fat = stats[0].text.strip().split(" ")[-1]
		carb = stats[3].text.strip().split(" ")[-1]
		protein = stats[4].text.strip().split(" ")[-1]
		macros = [calories,fat,carb,protein]
		menu_dishes.append(Dish(food,{TARGET_NUTRIENTS[i]:float(re.sub(r'[a-z]+', ''
			, macros[i]
			, re.I)) 
			for i in range(len(TARGET_NUTRIENTS))}))

	return menu_dishes

"""
Returns spreadsheet with nutrition information

input: menu url
output: filename of spreadsheet 
"""
def create_nutrition_spreadsheet(menu_url):

	foodnames, foodfacts = get_food_info(menu_url)

	f = open("nutrition.csv",'w')

	headers = "Food, Serving Size, Calories/Serving, Total Fat, Total Carbohydrate, Protein\n"
	f.write(headers)

	for i in range(len(foodnames)):
		
		food = foodnames[i].find('span').text
		tags = foodnames[i].findAll('img')
		#for vegetarians or non redmeat eaters
		foodtags = [tags[i]["src"].split("/")[-1].replace('.gif','') for i in range(len(tags))]
		serving_size = " ".join(foodfacts[i].find('p').text.split(" ")[2:])
		calories = foodfacts[i].find('span').text.split(' ')[1]
		stats = foodfacts[i].findAll('th',attrs={'colspan':"2"})
		fat = stats[0].text.strip().split(" ")[-1]
		carb = stats[3].text.strip().split(" ")[-1]
		protein = stats[4].text.strip().split(" ")[-1]

		f.write("{},{},{},{},{},{}\n".format(food,serving_size,calories,fat,carb,protein))

	f.close()

if __name__ == "__main__":
	print(get_locations(MEALS[0]))
### Dish class ###
""" this class stores nutrition information of a menu item """
""" to access, dish.nutrition[nutrient] """

import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import sys
import re

__author__ = "Ajith Kemisetti"
__email__ = "kemisettia@gmail.com"
__date__ = "8/16/2019"

class Dish:
    def __init__(self, name, nutrition_dictionary):
        self.name = name
        self.nutrition = nutrition_dictionary


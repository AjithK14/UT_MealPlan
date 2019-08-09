# UT_MealPlan

### Purpose:
A python interface designed to help find available dining halls at UT for during Breakfast, Lunch, and Dinner, and to build 
balanced meals from their menus. This code implements a Computational Nutrition Algorithm described in 
Pikes and Adams, 2016.

### Program Description:
 * Python command-line interface
 * When run, the user will be asked if he or she is trying to eat Breakfast, Lunch, or Dinner
 * Then, using BeautifulSoup, a script will crawl the UT Nutrition website and get information on all dining halls currently open
 * The user is asked which dining hall he or she prefers
 * The menu of that dining hall is once again scraped using python and BeautifulSoup 
 * Finally, the Computational Algorithm is run on the acquired list of dishes and the results are displayed
 * The result is simply a list of foods that constitutes the meal that most closely matches the user's daily recommended intake of Carbs, Fats, and Protein
 * Note that the results are approximate and the user is being shown the results that are closest to his or her macros requirements

---

While this python interface is fully functional, it is much more practical for me to have such a program on my phone. With this program on my phone, I can conveniently look at which foods to eat on my way to the dining hall. This will ensure that I don't have to stop somewhere, take out my laptop, and run the script. 

**Android app coming soon**

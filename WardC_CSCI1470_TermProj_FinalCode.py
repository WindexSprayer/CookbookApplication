#**********************  WardC_CSCI1470_TermProj_FinalCode.py  *********************
##
## Name: Courtney Ward
##
## Course: CSCI 1470.01
##
## Assignment: Term Project, Final Code
##
## Algorithm(or a brief purpose of the assignment)
##
##  START
##  import os, csv, and namedtuple
##  VARIABLE ASSIGNMENTS
##      Commonly used strings for later use in prompts and menus
##      File Names
##      Fixed lists & dictionaries
##      Empty dictionaries to be updated by program
##  DATA VALIDATION & CHANGES FUNCTIONS
##	Check if input is a positive integer and is in given range
##      Check if input is a positive integer
##	Check if input is a floating-point number
##	Change input from a string to a float; if not numerical, get new input
##	Change input from a string to a float; if not numerical, leave as string
##	Convert a list to a dictionary where list entries alternate between keys and values
##      Convert a list to a dictionary where list entries alternate between keys and values
##            & values are converted to float
##      Convert a list to a nested dictionary where final value is changed to float
##  FILE MANAGEMENT: 
##	If fodmap data csv file doesn’t exist 
##          create one
##          write first row headings
##          close
##	Open fodmap data csv file for reading 
##          populate fodmap data dictionary with data from file 
##	    Close file
##	If food conversion data csv file exists
##          Open it 
##          Populate the food conversion dictionary
##	    Close file
##	If food tracking txt file doesn’t exist
##          create one 
##          write each needed heading, one per line, 
##          close
##	Open food tracking txt file
##          use data to populate the food tracking dictionary
##          close
##	If recipe data csv file exists
##          open for reading
##          use data to populate the recipe dictionary
##          close
##  FUNCTIONS TO SAVE DATA
##	Save fodmap data to csv file
##	Save conversion data to csv file
##	Save food tracking data to txt file 
##	Save recipe data to csv file
##  PROGRAM LOOPING CONTROL FUNCTIONS
##	Continue looping
##	Save data & end program
##  MENU FUNCTIONS
##	Call function based on menu selection
##	Accept user input for menu selection
##	Print formatted menus
##	Print formatted lists
##  FODMAP DATA FUNCTIONS
##	 Look up FODMAP data for food
##	Add FODMAP data for food
##  FOOD TRACKING FUNCTIONS
##	Add food to tracking list
##	View items in tracking list
##  RECIPE FUNCTIONS
##	Print formatted view of saved recipe with calculated FODMAP data
##	Check if recipe exists & display it if it does. Give menu options for recipes
##	List names of all saved recipes
##	Allow user to add an ingredient and all of its data to a recipe
##	Allow user to add conversion factor for ingredients between user unit and grams
##	Allow user to input and save recipe serving and ingredient information
##	Calculate the amount of each type of fodmap in a recipe and per serving of the recipe
##  MENU DICTIONARIES
##	Define namedtuples for menu and function
##	Create function dictionary with namedtuple as value, giving function name, title, and arguments
##      Create menu dictionary with namedtuple as value, giving menu name and list of menu options
##          based on function dictionary
##  MAIN PROGRAM
##      While user wants to continue
##          Print main menu and follow user menu selections to call other functions
##  END   
##        
##    
##**********************************************************

import os
import csv
from collections import namedtuple

#Text for input prompts
not_num_text = "\nPlease only enter a numerical value.\n"
invalid_text = "\nInvalid Selection.\n\nPlease select an option from the menu.\n"
what_to_do = "What would you like to do?"
select_option = "\nPlease select an option from the menu.\n"

#Files for use
fodmapfilename = "fodmapdata.csv"
foodconversionfilename = 'foodconversions.csv'
recipefilename = 'myrecipes.csv'
recipefodmapfilename = 'recipefodmaps.csv'
foodtrackerfilename = 'foodtracker.txt'

#Set Dictionaries & Lists
fodmaps = ["FRUCTANS", "FRUCTOSE", "GALACTANS", "LACTOSE", "POLYOLS"]
fodmapmax = {"FRUCTANS":0, "FRUCTOSE":0, "GALACTANS":0, "LACTOSE":0, "POLYOLS":0} #FIXME: Find actual values

#Dictionary/Lists to be updated/populated
foodlist = {}
foodconversions = {}
trackmyfoods = {}
myrecipes = {}
recipefodmaps = {}


'''Data Validation Functions'''
def check_num_in_range(choice, range_start, range_end):
    allowed_range = range(range_start, range_end)
    in_range = False
    while choice.isdigit() == False or in_range == False:
        while choice.isdigit() == False:
            choice = input(not_num_text)
        if int(choice) not in allowed_range:
            in_range = False
            choice = input(invalid_text)
        else:
            in_range = True
    return int(choice)

def check_if_pos_int(data):
    '''Checks if string is positive integer, converts to int if so, gets new input if not'''
    while data.isdigit() == False:
        data = input(not_num_text)
    return int(data)

def check_if_float(data):
    '''Checks if string is numerical, neg & decimal allowed'''
    decimal_used = False
    isfloat = False
    if len(data) > 0:
        #if not (data[0] == "-" or data[0].isdigit() or data[0] == "."): ##USE INSTEAD if negative numbers okay
        if not (data[0].isdigit() or data[0] == "."):
            isfloat = False
            return isfloat
        elif data[0] == ".":
            decimal_used = True
            isfloat = True
        else:
            isfloat = True

        if len(data) > 1:
            for char in data[1:]:
                if char.isdigit():
                    isfloat = True
                elif char == "." and decimal_used == False:
                    decimal_used = True
                    isfloat = True
                else:
                    isfloat = False
                    return isfloat
    return isfloat

'''Data Type Conversion Functions'''
def change_to_float(data,prompt):
    '''Changes numerical string to float, asks for new input for nonnumerical string'''
    if check_if_float(data):
        return float(data)
    else:
        data = change_to_float(input(prompt),prompt)
        return data

def floatstring_to_float(data):
    '''Changes numerical string to float, returns nonnumerical string unchanged'''
    if check_if_float(data):
        return float(data)
    else:
        return data

def list_to_dict(mylist):
    '''Converts consecutive items in list to key:value pairs in dict'''
    mydict = {mylist[i]:mylist[i+1] for i in range(0, len(mylist), 2)}
    return mydict

def list_to_dict_str_float(mylist, *item):
    '''Converts consecutive items in list to key:float(value) pairs in dict'''
    mydict = {}
    for i in range(0, len(mylist), 2):
        if len(mylist[i]) > 0:
            prompt = f"Data for {mylist[i]} in {item[0]} is currently \'{mylist[i+1]}\'. Please enter a numerical value instead.\n"
            mylist[i+1] = change_to_float(mylist[i+1],prompt)
            mydict[mylist[i].upper().strip()] = mylist[i+1]
    return mydict

def list_to_nested_dict_str_float(mylist, item, step):
    
    mydict = {}
    for i in range(0, len(mylist), step):
        if len(mylist[i]) > 0:
            prompt = f"Data for {mylist[i+1]} of {mylist[i]} in {item} is currently \'{mylist[i+2]}\'. Please enter a numerical value instead.\n"
            mylist[i+2] = change_to_float(mylist[i+2],prompt)
            mydict[mylist[i].upper().strip()] = {mylist[i+1]:mylist[i+2]}
    return mydict



'''File & dictionary opening/creation'''

'''Populate FODMAP data dictionary'''
#if csv file doesn't exist, create file and write first row as column headings
if not os.path.isfile(fodmapfilename):
    with open(fodmapfilename,"w", newline='') as fodmapfile: 
        heading_writer = csv.writer(fodmapfile)
        headings = ["FOOD"] + fodmaps
        heading_writer.writerow(headings)
#open .csv file for reading to populate foods dictionary, set to automatically close
with open(fodmapfilename,"r") as fodmapfile: 
    food_reader = csv.reader(fodmapfile, delimiter = ",")
    #Create Dictionary for FODMAP data

    first_row = True
    for row in food_reader:
        food = row[0].upper()
        #Sets first row as variables for use as dictionary keys for entries
        if first_row:
            for pos, item in enumerate(row):
                vars()[f"heading{pos}"] = item.upper()
            first_row = False

        #Makes nested dictionary entry in foods for each food in file
        else:
            foodlist[food] = {} #sets the food name as key for inner dictionary
            for pos, value in enumerate(row):
                if pos == 0: #skips the food name as value
                    continue
                elif pos in range(len(fodmaps)+1): #itterates over fodmap data columns according to number of fodmaps in list fodmaps
                    
                    my_key = vars()[f"heading{pos}"] #prepares a call to headings from first row
                    prompt = f"Data for grams of {my_key} in 100 grams of {food} is currently \'{value}\'. Please enter a numerical value instead.\n"
                    foodlist[food][my_key] = change_to_float(value, prompt) #creates a dictionary entry for current food and FODMAP value

                
'''Creates foodconversions dictionary & populates it with file data if available'''
if os.path.isfile(foodconversionfilename):
    with open(foodconversionfilename, 'r') as foodconversionfile:
        conversion_reader = csv.reader(foodconversionfile, delimiter = ",")

        for row in conversion_reader:
            food = row[0].upper().strip()
            foodconversions[food] = list_to_dict_str_float(row[1:],food)
            
'''Creates trackmyfoods dictionary & populates it with file data if available'''
if not os.path.isfile(foodtrackerfilename):
    with open(foodtrackerfilename, "w") as foodtrackerfile:
        headings = ["MONASH Certified Foods", "Safe Foods", "Caution Foods", "Foods to Avoid"]
        for heading in headings:
            foodtrackerfile.write(f"{heading}\n")
with open(foodtrackerfilename, "r") as foodtrackerfile:
        for line in foodtrackerfile:
            items = line.split(',') #Splits the heading and each item in list apart to be able to add to dictionary/lists
            trackmyfoods[items[0].strip()] = [item.strip() for item in items[1:]] #Populates food list with saved data


'''Loads recipes from file'''
if os.path.isfile(recipefilename):
    with open(recipefilename, 'r') as recipefile:
        recipe_reader = csv.reader(recipefile, delimiter = ",")

        for row in recipe_reader:
            recipe = row[0].upper().strip()
            serving_size_text = row[1].upper().strip()
            serving_size = row[2].upper().strip()
            num_servings_text = row[3].upper().strip()
            num_servings = row[4].strip()
            prompt = f'Current data says that {recipe} makes \'{num_servings}\' servings, with a serving size of {serving_size}\nPlease enter a numerical amount of {serving_size} sized servings for {recipe}.\n'
            num_servings = change_to_float(num_servings, prompt)

            myrecipes[recipe] = {}
            myrecipes[recipe][serving_size_text] = serving_size
            myrecipes[recipe][num_servings_text] = num_servings
            myrecipes[recipe]['INGREDIENTS'] = list_to_nested_dict_str_float(row[5:],recipe,3)


'''Save Data Functions'''
def save_fodmap_data():
    '''Saves food fodmap data to file'''
    with open(fodmapfilename,"w", newline='') as fodmapfile: 
        data_writer = csv.writer(fodmapfile)
        headings = ["FOOD"] + fodmaps
        data_writer.writerow(headings)
        for food in foodlist:
            food_info = [food] + [str(data) for data in foodlist[food].values()]
            data_writer.writerow(food_info)
            
def save_conversions():
    '''Saves food unit conversions to file'''
    with open(foodconversionfilename, 'w', newline='') as foodconversionfile:
        conversion_writer = csv.writer(foodconversionfile)
        for food in foodconversions:
            row = [food.upper().strip()]
            for unit, conversion in foodconversions[food].items():
                row.extend([unit.strip(), str(conversion).strip()])
            conversion_writer.writerow(row)


def save_trackmyfoods():
    '''Saves food tracking lists from trackmyfoods dict'''
    with open(foodtrackerfilename, "w") as foodtrackerfile:
        for heading, foods in trackmyfoods.items():
            mystring = heading
            for food in foods:
                mystring += f',{food}'
            mystring += "\n"
            foodtrackerfile.write(mystring)

def save_recipes():
    '''Saves recipe, ingredient, and amount data'''
    with open(recipefilename, 'w', newline='') as recipefile:
        recipe_writer = csv.writer(recipefile)
        for recipe, components in myrecipes.items():
            row = [recipe.upper().strip()]

            i = 0
            for heading, data in components.items():
                if i < 2:
                    row.extend([heading.upper().strip(), str(data).strip()])
                    i += 1
                else:
                    for food, amount in data.items():
                        for unit, quantity in amount.items():
                            row.extend([food.upper().strip(), unit.strip(), str(quantity).strip()])
                
            recipe_writer.writerow(row)
                    
'''PROGRAM CONTINUE & END FUNCTIONS'''
def do_something_else():
    '''Allows main program to loop'''
    global do_something
    do_something = True

def end_program():
    '''Stops main program from looping, saves data, and ends program'''
    global do_something
    do_something = False
    save_fodmap_data()
    save_conversions()
    save_trackmyfoods()
    save_recipes()
    print("DATA SAVED\nGOODBYE")

'''MENU SELECTION FUNCTIONS'''
def call_function_from_menu(menu, choice):
    '''Calls functions from menu given user choice'''
    #call functions with no parameters
    if menus[menu].options[choice].parameters == None: 
        menus[menu].options[choice].function()
    #call functions with multiple parameters
    elif type(menus[menu].options[choice].parameters) == tuple:
        values = menus[menu].options[choice].parameters
        menus[menu].options[choice].function(*values)
    #call functions with one parameter
    else:
        menus[menu].options[choice].function(menus[menu].options[choice].parameters)

def make_selection(menu):
    '''Calls function user selects from menu. If user choice is not in menu, asks for new selection.'''
    choice = input(select_option)
    while choice not in menus[menu].options:
        choice = input("\nInvalid Selection.\n\nSelect an option from the menu:\n")
    call_function_from_menu(menu, choice)                   

'''MENU & LIST FORMATTED PRINTING'''    
def print_menu_top(title, menu_width):
    '''Prints top part of menu (Top Border and Heading)'''
    top_border = f'/{"-" * (menu_width - 2)}\\'
    blank_line = f"|{'|':>{menu_width-1}}"

    print()
    print(top_border)
    print(blank_line)
    print(f"|{title.upper():^{menu_width-2}}|")
    print(blank_line)

def print_menu_bottom(menu_width):
    '''Prints bottom part of menu (Bottom Border)'''
    bottom_border = f'\\{"-" * (menu_width - 2)}/'
    blank_line = f"|{'|':>{menu_width-1}}"
    print(blank_line)
    print(bottom_border)

def print_list(heading, items):
    '''Prints formatted list of items with heading'''
    print()
    print(heading)
    print("-" * 30)
    for item in items:
        print(item.upper().strip())
    print()
    
def print_menu(menu):
    '''Prints formatted menu'''
    menu_width = 40
    title = menus[menu].text
    options = menus[menu].options

    print_menu_top(title, menu_width)
    for num, option in options.items():
        print(f"| {num:>2}. {option.text:{menu_width - 7}}|")
    print_menu_bottom(menu_width)
    
    make_selection(menu)
    
def list_menu():
    '''Prints Food Lists Menu'''
    menu_width = 31
    print_menu_top("Food Lists", menu_width)
    num = 0

    for option in trackmyfoods.keys():
        num += 1
        print(f"| {num:>2}. {option:{menu_width - 7}}|")
    print_menu_bottom(menu_width)
    
'''FODMAP DATA FOR FOOD FUNCTIONS'''
def check_food():
    '''Checks for FODMAP data for inputted food'''
    food = input("Enter food:\n").upper().strip()

    if food in foodlist:
        print(f"\nCurrent FODMAP data for {food}")
        print("-" * 30)
        for fodmap,data in foodlist[food].items():
            label = f'{fodmap}:'
            print(f"{label:<10} {data:>3}g/100g {food}")
    else:
        print(f'No data found for {food}.\n')
    print()
    print(what_to_do)
    print_menu("FODMAP")

def add_FODMAP_data(*items):
    '''Allows user to enter FODMAP data for food'''
    if not items:
        food = input("Enter food:\n").upper().strip()
        if food not in foodlist:
                foodlist[food] = {fodmap:change_to_float(input(f"Enter numerical amount of grams of {fodmap} in 100g of {food}\n"), not_num_text) for fodmap in fodmaps} #FIXME:(If unknown, press enter)\n
    else:
        for item in items:
            food = item.upper().strip()
            if food not in foodlist:
                foodlist[food] = {fodmap:change_to_float(input(f"Enter numerical amount of grams of {fodmap} in 100g of {food}\n"), not_num_text) for fodmap in fodmaps} #FIXME:(If unknown, press enter)\n

'''FOOD TRACKING FUNCTIONS'''
def track_food():
    '''Allows user to add food item to tracking lists'''
    list_menu()

    input_text = "\nWhich list would you like to add to?\n"
    choice = check_num_in_range(input(input_text), 1, len(trackmyfoods) + 1)
    index = choice - 1

    my_list = list(trackmyfoods.keys())[index]#Gets name of chosen list for use as key
    food = input(f"Enter food to add to {my_list}:\n").upper().strip() #Gets food input from user
    trackmyfoods[my_list].append(food) #Adds food to chosen list
    print(f'{food} has been added to your {my_list} list.')
    print_list(my_list,trackmyfoods[my_list])
    
def check_lists():
    '''Allows user to view foods on tracking lists'''
    list_menu()

    input_text = "\nWhich list would you like to view?\n"        
    choice = check_num_in_range(input(input_text), 1, len(trackmyfoods) + 1)
    index = choice - 1
    
    my_list = list(trackmyfoods.items()) 
    print_list(my_list[index][0],my_list[index][1])

    
'''RECIPE TRACKING AND CHECKING FUNCTIONS'''
def show_recipe(recipe):
    '''Prints formated table of recipe info (servings, ingredients, FODMAP data)'''
    heading = recipe.upper()
    serving_size = myrecipes[recipe]['SERVING SIZE']
    num_servings = myrecipes[recipe]['NUMBER OF SERVINGS']
    if recipe not in recipefodmaps:
        calc_recipe_fodmap(recipe)
    
    print()
    print(f'{heading:^30}')
    print("-" * 30)
    print(f"{'SERVING SIZE:':<19} {serving_size}\n{'NUMBER OF SERVINGS:':<19} {num_servings}")
    print("-" * 30)
    print()
    print('Ingredients')
    for ingredient, amount in myrecipes[heading]['INGREDIENTS'].items():
        for unit, quantity in amount.items():
            print(f'{quantity:>6} {unit:<7} {ingredient}')
    print()
    print("-" * 30)
    print()
    print(f'FODMAPs Per Serving')
    for fodmap, amount in recipefodmaps[recipe]['FODMAPS PER SERVING'].items():
        fodmap_label = f'{fodmap}:'
        print(f"   {fodmap_label:<10} {amount:>8.2f} g ")
    print()
    print("-" * 30)

def check_recipe():
    '''Checks for existance of recipe'''
    recipe = input("What's the name of your recipe?\n").upper().strip()
    if recipe in myrecipes:
        show_recipe(recipe)
    else:
        print("Recipe not found.\n")
    print_menu("Recipe")

def list_recipes():
    '''Lists all saved recipe names'''
    print_list("Current Recipes".upper(), myrecipes)
    
def add_ingredient(recipe):
    '''Makes an ingredient entry for recipe'''
    ingredient = input("Enter ingredient name.\n").upper().strip()
    myrecipes[recipe]['INGREDIENTS'][ingredient] = {}
    
    if ingredient not in foodlist:
        print(f"There is no FODMAP data for {ingredient}.\nPlease enter it now.")
        add_FODMAP_data(ingredient)

    unit = input("How is this ingredient measured?\n(Enter name of unit of measurement)\n").lower().strip()
 
    mass_unit = ['g', 'gram', 'grams']

    if ingredient not in foodconversions:
        foodconversions[ingredient] = {}

    while (unit not in mass_unit) and (unit not in foodconversions[ingredient]):
        print(f"You don't have a conversion factor between {unit} and grams for {ingredient}.")
        choice = input("Would you like to (1) enter a conversion factor or (2) change unit?\n").strip()

        while choice != '1' and choice != '2':
            choice = input("Invalid choice.\nWould you like to (1) enter a conversion factor or (2) change unit?\n").strip()

        if choice == '1':
            add_conversion(ingredient, unit)
        elif choice == '2':
            unit = input("How is this ingredient measured?").lower().strip()
           
    if unit in mass_unit:
        unit = "grams"

    amount = change_to_float(input(f"How much {ingredient} in {unit} are in this recipe?\n(input number only)\n"), not_num_text)

    myrecipes[recipe]['INGREDIENTS'][ingredient][unit] = amount
     
    
def add_conversion(food, unit):
    '''Adds conversion factor between grams and unit to foodconversions dictionary for food'''
    conversion = check_if_float(input(f"How many grams of {food} are there per {unit}?\n(input number only)\n"))
    if food not in foodconversions:
        foodconversions[food] = {}
    foodconversions[food][unit] = conversion

def make_recipe(*recipe): #FIXME: Figure out how to allow parameter recipe to pass from one function through dictionary to here
    '''allows user to create a new recipe entry'''
    #Gets recipe name from input
    if not recipe:
        recipe_name = input("What's the name of your recipe?\n").upper().strip()
        #Checks for existance of recipe and gives user choices of action if recipe already exists
        if recipe_name in myrecipes:
            choice = input(f"A recipe for \'{recipe_name}\' already exists.\nWhat do you want to do?\n\n1. View existing recipe \'{recipe_name}\'\n2. View list of all saved recipe names\n3. Rename current recipe\n4. Save over current recipe\n5. Return to main menu\n").upper().strip()
            while int(choice.strip()) not in range(1,6):
                choice = input("Invalid input.\nEnter a number 1-5.\nWhat do you want to do?\n")
            if choice == '1':
                show_recipe(recipe_name)
                make_recipe()
                return
            elif choice == '2':
                list_recipes()
                make_recipe()
                return
            elif choice == '3':
                make_recipe()
                return
            elif choice == '4':
                del myrecipes[recipe_name] #gets rid of old recipe entry so it can be replaced by continuing this function
            elif choice == '5':
                return
    #Gets recipe name from argument
    else:
        recipe_name = recipe[0].upper().strip()

    #Sets up nested dictionary for recipe & collects and adds serving information
    myrecipes[recipe_name] = {}
    number_of_servings = check_if_pos_int(input("How many servings does this recipe make?\n(input whole number only)\n"))
    myrecipes[recipe_name]["NUMBER OF SERVINGS"] = number_of_servings
    serving_size = input("How large is a serving?\n")
    myrecipes[recipe_name]["SERVING SIZE"] = serving_size
    myrecipes[recipe_name]['INGREDIENTS'] = {}

    #Adds ingredient information to recipe while there are more ingredients    
    more_ingredients = True
    while more_ingredients:
        add_ingredient(recipe_name)
        
        #Checks for more ingredients
        choice = input("Are there more ingredients?\n(Type 'y' or 'n')\n").lower().strip()
        while choice != 'y' and choice != 'n':
            choice = input("Invalid choice.\nAre there more ingredients?\n(Type 'y' or 'n')\n")
        if choice == 'n':
            more_ingredients = False

    #Calculates the amounts of each fodmap in recipe
    calc_recipe_fodmap(recipe_name)
    #Prints completed recipe with calculated FODMAP data
    show_recipe(recipe_name)
    
def calc_recipe_fodmap(recipe):
    '''Allows user to calculate the amounts of fodmaps in recipe'''
    recipefodmaps[recipe] = {}
    recipefodmaps[recipe]['TOTAL FODMAPS'] = {}
    num_servings = myrecipes[recipe]['NUMBER OF SERVINGS']
    recipefodmaps[recipe]['FODMAPS PER SERVING'] = {}
    
    for fodmap in fodmaps:
        total_fodmap = 0
        for food, amount in myrecipes[recipe]["INGREDIENTS"].items():
            if food not in foodlist:
                print(f"There is no FODMAP data for {food}.\nPlease enter it now.")
                add_FODMAP_data(food)
                
            for unit, quantity in amount.items():
                if unit != 'grams':
                    if food not in foodconversions:
                        add_conversion(food, unit)
                    elif unit not in foodconversions[food]:
                        add_conversion(food, unit)
                    conversion = foodconversions[food][unit]
                    mass_food = quantity * conversion
                else:
                    mass_food = quantity
                
                fodmap_in_food = foodlist[food][fodmap]
                mass_fodmap = mass_food * fodmap_in_food / 100

                if food not in recipefodmaps[recipe]:
                    recipefodmaps[recipe][food] = {}
                recipefodmaps[recipe][food][fodmap] = mass_fodmap

                total_fodmap += mass_fodmap
        
        recipefodmaps[recipe]['TOTAL FODMAPS'][fodmap] = total_fodmap
        recipefodmaps[recipe]['FODMAPS PER SERVING'][fodmap] = total_fodmap / num_servings

              

'''DICTIONARIES FOR MENUS AND FUNCTIONS USED IN MENUS'''
Menu = namedtuple("Menu", "text options")
Function = namedtuple("Function", "function text parameters")

functions = {
    "View or Add FODMAP Data":Function(check_food, "View or Add FODMAP Data", None),
    "Check Recipe":Function(check_recipe, "Check Recipe", None),
    "Track Food":Function(track_food, "Track Food", None),
    "Check Food Lists":Function(check_lists, "Check Food Lists", None),
    "Exit Program":Function(end_program, "Exit Program", None),
    "Add FODMAP Data":Function(add_FODMAP_data, f"Add FODMAP Data", None),
    "Main Menu":Function(do_something_else, "Return to Main Menu", None),
    "Print List":Function(print_list, "Print List", (trackmyfoods.keys(),items)),
    "List Recipes":Function(list_recipes, "List Recipes", None),
    "Make Recipe":Function(make_recipe, "Make Recipe", None)
    #:Function(, , None),
}

menus = {
    "main":
        Menu(
            "Main Menu",
            {
            '1':functions["View or Add FODMAP Data"],
            '2':functions["Check Recipe"],
            '3':functions["Track Food"],
            '4':functions["Check Food Lists"],
            '5':functions["Exit Program"]
            }
        ),
    "FODMAP":
        Menu(
            what_to_do,
            {
            '1':functions["Add FODMAP Data"],
            '2':functions["Main Menu"],
            '3':functions["Exit Program"]
            }
        ),
    "Recipe":
        Menu(
            what_to_do,
            {
            '1':functions["List Recipes"],
            '2':functions["Make Recipe"],
            '3':functions["Main Menu"],
            '4':functions["Exit Program"]
            }
        )
}



'''MAIN PROGRAM'''
#functions[check_food].function()
do_something = True

while do_something:
    print_menu("main")


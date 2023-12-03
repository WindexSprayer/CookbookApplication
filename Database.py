#   Database Function Program
#   Public Functions:
#   open_cookbook() -- used to open the excel file and read in the information, OR create a new excel file 
#   save_dfs() -- used to save the database information at any time to the excel file
#   getRecipeList() -- returns the recipes as a list
#   getRecipeInformation(RecipeName) --returns the recipe details from a given recipe name, returned in a dictionary formatted as:
#           {'RecipeID': id, 'RecipeName': name,...'Ingredients':[{'Name':name,...},...], 'instructions':[step1,step2.......]}
#   addRecipe(recipeInformation) --adds recipe information, given a dictionary formated like the one in getRecipeInformation
#   deleteRecipe(recipeName) --deletes a recipe from the database, given a recipe name
#   editRecipe(recipeInformation, recipeName) --deletes a recipe from the database of a given name, then adds the updated recipe
#   editSteps(newSteps, recipeName) -- updates existing steps given the new steps (in a list of steps), and the recipes name
#   editIngredients(newIngredients, recipeName) -- updates existing ingredients given the new ingredients (list of dictionaries), and the recipe name
###################################################################################################################################
import pandas as pd
#Allows pandas to write to excel
from pandas import ExcelWriter
#allows opening of excel files 
import openpyxl
#& csv files
import csv
#brings in real time - allows us to control length of load screens for messages to display
import time
#restructures strings to keep consistent formatting
import re

#define our dataframes so they are globalized across the functions
global ingredientsdf, recipedf, stepsdf
filename = 'cookbook.xlsx' #filename
#column namesfor our dataframes
columnsRecipes = ['RecipeID', 'RecipeName', 'Description', 'tags', 'foodCat', 'cuisine', 'prepTime','cookTime', 'servings']
columnsIngredients = ['IngredListID', 'Name', 'Amount', 'Unit']
columnsSteps = ['StepListID', 'StepNum', 'Instruction']

#this function will open the dataframes, if the excel does not exist, it will create one
def open_cookbook():
    global ingredientsdf, recipedf, stepsdf #use global variables
    try: 
        ingredientsdf = pd.read_excel(filename, sheet_name='Ingredients') #open the sheet in the file named 'ingredients' to get the ingredientsdf
        recipedf = pd.read_excel(filename, sheet_name='Recipe') #open the sheet in the file named 'recipe' to get the recipedf
        stepsdf = pd.read_excel(filename, sheet_name='Steps') #open the sheet in the file named 'steps' to get the stepsdf
        ingredientsdf = ingredientsdf.fillna("")
        recipedf = recipedf.fillna("")
        stepsdf = stepsdf.fillna("")
    except FileNotFoundError:
        #if the file does not exist, then create the dataframes, then save it
        ingredientsdf = pd.DataFrame(columns = columnsIngredients) #create a dataframe for ingredients, recipes, steps
        recipedf = pd.DataFrame(columns = columnsRecipes)
        stepsdf = pd.DataFrame(columns = columnsSteps)
        
        save_dfs()#save the dataframes to the excel file
    return #end of open_cookbook function

#this function will save the dataframes to the excel file, and reopen them
def save_dfs():
    global ingredientsdf, recipedf, stepsdf, filename #use global variables
    try:
        with ExcelWriter(filename, mode="a", engine="openpyxl",if_sheet_exists= 'replace') as writer:
            recipedf.to_excel(writer, sheet_name='Recipe',index=False)
            ingredientsdf.to_excel(writer,sheet_name='Ingredients',index=False)
            stepsdf.to_excel(writer,sheet_name='Steps',index=False)
    except FileNotFoundError:
        with ExcelWriter(filename) as writer:
            recipedf.to_excel(writer, sheet_name='Recipe',index=False)
            ingredientsdf.to_excel(writer,sheet_name='Ingredients',index=False)
            stepsdf.to_excel(writer,sheet_name='Steps',index=False)
    ingredientsdf = pd.read_excel(filename, sheet_name='Ingredients')
    recipedf = pd.read_excel(filename, sheet_name='Recipe')
    stepsdf = pd.read_excel(filename, sheet_name='Steps')
    ingredientsdf = ingredientsdf.fillna("")
    recipedf = recipedf.fillna("")
    stepsdf = stepsdf.fillna("")
    return #end of save_dfs function

#this function will be called when displaying the dropdown menu of recipes for the user to select
def getRecipeList(): #function creates a list of the recipes
    recipeList = list(recipedf["RecipeName"])
    return recipeList   #end of getRecipeList

def getRecipeInformation(recipeName):
    #get the recipe associated with the  recipe name
    global ingredientsdf, recipedf, stepsdf, filename #use global variables
    recipe = recipedf.loc[recipedf['RecipeName'] == recipeName] #make a df with just the recipe we are searching for
    idNums = recipe['RecipeID'].to_list() #get the id number
    recipeID = idNums[-1] #find the recipeID--this will find the recipes ingredients and steps
    recipe = recipe.drop(columns=['RecipeID']) #drop the recipeID column 
    recipe = recipe.to_dict('records') 
    recipeInformation = dict(recipe[0]) #recipedf is now a dictionary
    #find the ingredients assoicated with the recipe name
    ingredients = ingredientsdf.loc[ingredientsdf['IngredListID'] == recipeID] 
    ingredients = ingredients.drop(columns=['IngredListID']) #drop the ingredlistid col
    ingredients = ingredients.to_dict('records') 
    ingredients = {'ingredients' : ingredients} #ingredients df is now a dictionary
    recipeInformation.update(ingredients) #add ingredients to the existing recipeinfo dictionary
    #find the steps associated with the recipe name
    steps = stepsdf.loc[stepsdf['StepListID'] == recipeID]
    steps = steps['Instruction'].tolist()
    steps = {'instructions': steps} #steps df is now a dictionary
    recipeInformation.update(steps) #add steps to the existing recipeinfo dictionary
    return recipeInformation #end of getRecipeInformation function

def addRecipe(recipeInformation):
    global ingredientsdf, recipedf, stepsdf, filename #use global variables

    ingredients = recipeInformation['ingredients'] #get the ingredients from the dictionary
    stepsList = recipeInformation['instructions'] #get the steps from the dictionary

    del recipeInformation['ingredients'] #remove the ingredients and instructions from the dataframe to have just the recipe information remaining
    del recipeInformation['instructions']

    recipe = recipeInformation #get the recipe information from the dictionary (what is left of the dictionary)
    try:
        last_recipe = recipedf.loc[len(recipedf)-1]
        last_id = last_recipe['RecipeID']
        listID = last_id + 1 #create the unique id num for the recipe information
    except KeyError:
        listID = len(recipedf) + 1
    recipeID = {'RecipeID': listID} 
    recipe.update(recipeID) #add the id num to the recipe information

    recipedf.loc[len(recipedf) + 1] = recipe #save to recipedf
    #update the ingredients information to add the unique id
    for item in ingredients:
        item.update({"IngredListID":listID})
    newIngreddf = pd.DataFrame(columns = columnsIngredients, data = ingredients)
    ingredientsdf = pd.concat([ingredientsdf, newIngreddf], ignore_index = True) #save to the ingredientsdf
    #update the instructions information to add the unique id
    itemNum = 1
    steps = []
    for item in stepsList:
        steps.append( {'StepListID':listID,'StepNum': itemNum,'Instruction': item})
        itemNum += 1
    newStepsdf = pd.DataFrame(columns = columnsSteps, data = steps) 
    stepsdf = pd.concat([stepsdf, newStepsdf], ignore_index = True)#save to the stepsdf
    save_dfs()#save the dataframes to the excel file
    return  #end of addRecipe function

def deleteRecipe(recipeName):
    global ingredientsdf, recipedf, stepsdf, filename #use global variables
    recipe = recipedf.loc[recipedf['RecipeName'] == recipeName]  #find the recipe we are removing
    idNums = recipe['RecipeID'].to_list() #get the id number
    id = idNums[-1] #find the existing ID number, so we can replace the recipe information
    recipedf = recipedf.drop(recipedf[recipedf['RecipeName'] == recipeName].index) #delete the recipe
    ingredientsdf = ingredientsdf.drop(ingredientsdf[ingredientsdf['IngredListID'] == id].index) #delete the ingredients
    stepsdf = stepsdf.drop(stepsdf[stepsdf['StepListID'] == id].index) #delete the instructions
    save_dfs()
    return  #end of addRecipe function

def editRecipe(recipeInformation, recipeName):
    global ingredientsdf, recipedf, stepsdf, filename #use global variables
    recipe = recipedf.loc[recipedf['RecipeName'] == recipeName] #find the existing recipe
    idNums = recipe['RecipeID'].to_list() #get the id number
    id = idNums[-1] #find the existing ID number, so we can replace the recipe information
    recipeInformation.update({'RecipeID': id} ) #update the given information to use the previous recipeID -- allowing us to keep 
                                                #the same ingredients and steps
    recipedf = recipedf.drop(recipedf[recipedf['RecipeName'] == recipeName].index) #delete the old information
    recipedf.loc[len(recipedf) + 1] = recipeInformation #save the new information
    save_dfs()
    return  #end of addRecipe function

def editSteps(newSteps, recipeName):
    global ingredientsdf, recipedf, stepsdf, filename
    recipe = recipedf.loc[recipedf['RecipeName'] == recipeName]  #find the existing recipe id number
    idNums = recipe['RecipeID'].to_list() #get the id number
    id = idNums[-1] #find the id number
    stepsdf = stepsdf.drop(stepsdf[stepsdf['StepListID'] == id].index) #delete the old steps

    itemNum = 1
    steps = []
    for item in newSteps:
        steps.append( {'StepListID':id,'StepNum': itemNum,'Instruction': item})
        itemNum += 1
    newStepsdf = pd.DataFrame(columns = columnsSteps, data = steps) 
    stepsdf = pd.concat([stepsdf, newStepsdf], ignore_index = True)#save to the stepsdf
    save_dfs()
    return

def editIngredients(newIngredients, recipeName):
    global ingredientsdf, recipedf, stepsdf, filename
    recipe = recipedf.loc[recipedf['RecipeName'] == recipeName]  #find the existing recipe id number
    idNums = recipe['RecipeID'].to_list() #get the id number
    id = idNums[-1]#find the id number
    ingredientsdf = ingredientsdf.drop(ingredientsdf[ingredientsdf['IngredListID'] == id].index) #delete the old ingredients
    for item in newIngredients:
        item.update({"IngredListID":id})
    newIngreddf = pd.DataFrame(columns = columnsIngredients, data = newIngredients)
    ingredientsdf = pd.concat([ingredientsdf, newIngreddf], ignore_index = True) #save to the ingredientsdf
    save_dfs()
    return

def getTags():
    global recipedf
    unique_tags = recipedf['tags'].unique().tolist()
    unique_foodCat = recipedf['foodCat'].unique().tolist()
    unique_cuisine = recipedf['cuisine'].unique().tolist()
    all_tags = unique_tags + unique_foodCat + unique_cuisine
    all_tags = list(filter(("").__ne__, all_tags)) 
    tags_filter = {}
    tags_filter.update({"All":recipedf['RecipeName'].tolist()})
    for tag in all_tags:
        resultsList = []

        resultsTags = recipedf.loc[recipedf["tags"] == tag]
        resultsTags = resultsTags['RecipeName'].tolist()
        if len(resultsTags) != 0 :
            resultsList.extend(resultsTags)
        resultsCuisine = recipedf.loc[recipedf["cuisine"] == tag]
        resultsCuisine = resultsCuisine['RecipeName'].tolist()
        if len(resultsCuisine) != 0 :
            resultsList.extend(resultsCuisine)   

        resultsFoodCat = recipedf.loc[recipedf["foodCat"] == tag]
        resultsFoodCat = resultsFoodCat['RecipeName'].tolist()
        if len(resultsFoodCat) != 0 :
            resultsList.extend(resultsFoodCat)  

        tags_filter.update({tag:resultsList})
    return tags_filter

def getLastRecipe():
    #get the recipe associated with the  recipe name
    global ingredientsdf, recipedf, stepsdf, filename #use global variables
    recipes = recipedf['RecipeName'].tolist()
    recipeName = recipes[-1]
    return recipeName

############################################################################################################
#
#
#
#                           The following are used for testing

def getIngredientsdf(): 
    global ingredientsdf
    return ingredientsdf
#get the steps table
def getStepsdf():
    global stepsdf
    return stepsdf
#get the recipetable
def getRecipedf():
    global recipedf
    return recipedf

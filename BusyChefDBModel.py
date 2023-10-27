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
columnsRecipes = ['RecipeID', 'RecipeName', 'Description', 'tags', 'foodCat', 'cuisine', 'prepTime','cookTime', 'servings', 'numIngred', 'numInstruct' ]
columnsIngredients = ['IngredListID', 'Name', 'Amount', 'Unit']
columnsSteps = ['StepListID', 'StepNum', 'Instruction']

#this function will open the dataframes, if the excel does not exist, it will create one
def open_cookbook():
    global filename, ingredientsdf, recipedf, stepsdf #use global variables
    try: 
        ingredientsdf = pd.read_excel(filename, sheet_name='Ingredients') #open the sheet in the file named 'ingredients' to get the ingredientsdf
        recipedf = pd.read_excel(filename, sheet_name='Recipe') #open the sheet in the file named 'recipe' to get the recipedf
        stepsdf = pd.read_excel(filename, sheet_name='Steps') #open the sheet in the file named 'steps' to get the stepsdf

    except FileNotFoundError:
        #if the file does not exist, then create the dataframes, then save it
        ingredientsdf = pd.DataFrame(columns = columnsIngredients) #create a dataframe for ingredients, recipes, steps
        recipedf = pd.DataFrame(columns = columnsRecipes)
        stepsdf = pd.DataFrame(columns = columnsSteps)
    ingredientsdf = ingredientsdf.fillna("")
    recipedf = recipedf.fillna("")
    stepsdf = stepsdf.fillna("")
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
    recipedf = recipedf.fillna("")

    return #end of save_dfs function

#this function will be called when displaying the dropdown menu of recipes for the user to select
def getRecipeList(): #function creates a list of the recipes
    recipeList = list(recipedf["RecipeName"])
    return recipeList   #end of getRecipeList

def getRecipeInformation(recipeName):
    #get the recipe associated with the  recipe name
    global ingredientsdf, recipedf, stepsdf, filename #use global variables
    recipe = recipedf.loc[recipedf['RecipeName'] == recipeName] #make a df with just the recipe we are searching for
    recipeID = recipe.iloc[0]['RecipeID']  #find the recipeID--this will find the recipes ingredients and steps
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
    listID = len(recipedf) + 1 #create the unique id num for the recipe information
    recipeID = {'RecipeID': len(recipedf) + 1} 
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
    id = recipe.iloc[0]['RecipeID'] #get the id number
    recipedf = recipedf.drop(recipedf[recipedf['RecipeName'] == recipeName].index) #delete the recipe
    ingredientsdf = ingredientsdf.drop(ingredientsdf[ingredientsdf['IngredListID'] == id].index) #delete the ingredients
    stepsdf = stepsdf.drop(stepsdf[stepsdf['StepListID'] == id].index) #delete the instructions
    save_dfs()
    return  #end of addRecipe function

def editRecipe(recipeInformation, recipeName):
    deleteRecipe(recipeName)
    addRecipe(recipeInformation)
    save_dfs()
    return  #end of addRecipe function
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

from flask import Flask, render_template, request, send_from_directory
import requests
from urllib.parse import unquote

# import requests makes a call & its checked w/ help of status code that whether our request was successful or not

# API_URL = 'https://api.spoonacular.com'

# Flask constructor takes the name of current module (__name__) as argument.
app = Flask(__name__) # main app instance

API_KEY = '123'


@app.route("/favicon.ico")
def favicon():
        return send_from_directory('static', 'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/', methods=["GET", "POST"]) 

# function handles user searches and displays a list of recipes including their images based on user input
def index():
    # since we're searching for recipes, POST and GET requests need to be handled
    # if user submits a recipe search, activate POST method

    if request.method == "POST": # server request
        query = request.form.get('search_query', '')
        recipes = search_recipes(query)
        return render_template("index.html", recipes=recipes, search_query=query)
    
    else: # if no search submitted, still need to handle this possibility, rendering page w.out searches
        search_query = request.args.get('search_query', '')
        decoded_search_query = unquote(search_query)
        recipes = search_recipes(decoded_search_query)
        return render_template("index.html", recipes=recipes, search_query=decoded_search_query)

# function that searches the API for recipes
def search_recipes(query):
    url = f'https://api.spoonacular.com/recipes/complexSearch'
    params = {
        'apiKey': API_KEY,
        'query': query,
        'number': 10,
        'instructionsRequired': True,
        'addRecipeInformation': True,
        'fillIngredients': True,
    }

    # Send a GET request to the API with the query parameters
    response = requests.get(url, params=params)
    if response.status_code == 200: # server response
        #converts the JSON response from the API into a list
        data = response.json()
        return data['results']
    else:
        return []

        
# takes usr to page for single recipe's info
@app.route('/recipe/<int:recipe_id>')
def view_recipe(recipe_id):
    search_query = request.args.get('search_query', '')

    url = f'https://api.spoonacular.com/recipes/{recipe_id}/information'
    params = {
        'apiKey': API_KEY,
    }

    response = requests.get(url, params=params)
    if response.status_code == 200: # server response
        recipe = response.json()
        return render_template("view_recipe.html", recipe=recipe, search_query=search_query)
    else:
        return "Recipe not found", 404

# main driver function
if __name__ == '__main__':
    app.run(debug=True)
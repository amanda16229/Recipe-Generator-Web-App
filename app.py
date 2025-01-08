from flask import Flask
import requests # makes a call and it is checked with the help of status code that whether our request was successful or not

# Flask constructor takes the name of current module (__name__) as argument.
app = Flask(__name__) # main app instance

API_URL = 'https://api.spoonacular.com/recipes/complexSearch'
API_KEY = '3b85999be9b34d5aa21904bef8cf4749'

# Making the API request
response = requests.get(API_URL)

# what info / data am i accessing and how to translate to usable code?
@app.route('/') # accessing root of app
def home():
    return "Welcome to this Recipe Generator!"


# main driver function
if __name__ == '__main__':
    app.run()
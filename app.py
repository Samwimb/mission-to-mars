from flask import Flask, render_template, jsonify, redirect
# from flask import Flask, render_template
from flask_pymongo import PyMongo
# from pymongo import MongoClient
import os
import scrape_mars

app = Flask(__name__)


# mongo = PyMongo(app, uri="mongodb://localhost:27017/weather_app")
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")
# db =  mongo.mars
# mars = db.mars
#mars = mongo.db.mars

@app.route("/")
def index():
    # print("getting mars data from mongodb")
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)


@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    mars_data = scrape_mars.scrape()
    mars.update({}, mars_data, upsert=True)
    return redirect("/", code=302)
    # print("after scrape; ready to redirect")
    #return redirect("https://mars-mission.herokuapp.com", code=302)
    # return redirect("http://localhost:5000/", code=302)
    # return "scraping successful"

if __name__ == "__main__":
    app.run(debug=True)
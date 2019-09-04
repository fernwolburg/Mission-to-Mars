from flask import Flask, render_template, redirect
import pymongo
import scrape_mars

# Create an instance of our Flask app.
app = Flask(__name__)

# Create connection variable
conn = 'mongodb://localhost:27017/mars_app'

# Pass connection to the pymongo instance.
mongo = pymongo.MongoClient(conn)

# Set route
@app.route("/")
def index():
    mars = mongo.db.collection.find_one()
    return render_template("index.html", mars=mars)

# Scrape 
@app.route("/scrape")
def scrape():

    mars_data = scrape_mars.scrape_website()
    mongo.db.collection.update({}, mars_data, upsert=True)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)


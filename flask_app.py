from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


@app.route('/')
def index():
    marsData = mongo.db.marsData.find_one()
    return render_template("scrape_mars.html", marsData=marsData)

@app.route("/scrape")
def scraper():
    marsData = mongo.db.marsData
    marsData_data = scrape_mars.scrape()
    marsData.update({}, marsData_data, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
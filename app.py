#########################################################
#####SCRIPT TO COMMUNICATE WITH PYMONGO AND THE WEB######
#########################################################

from flask import Flask, render_template, redirect
import pymongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
conn = "mongodb://localhost:27017/"

client = pymongo.MongoClient(conn)

db = client.mars_db



#Route to render index using data from mongo
@app.route("/")
def home():
    mars_data = list(db.mars_data.find())
    print(mars_data)
    
    return render_template("index.html", mars_data = mars_data)

    
#Route for scraping
@app.route("/scrape")
def scrape():
    
    mars_data = scrape_mars.scrape_all()
    db.mars_data.update({}, mars_data, upsert =True)
    
    #Redirect to homepage
    return redirect("/")

if __name__ == "__main__":
    app.run(debug = True)
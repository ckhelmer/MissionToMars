#Dependencies
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import pandas as pd
import pymongo
from flask import Flask

#Retrieve latest news
url = 'https://mars.nasa.gov/news/'
response = requests.get(url)
soup = bs(response.text, 'lxml')
a_titles = soup.find_all('div', class_ = 'content_title')
a_text = soup.find_all('div', class_ = 'article_teaser_body')

#Retrieve latest weather report
url = "https://twitter.com/marswxreport?lang=en"
response = requests.get(url)
soup = bs(response.text, 'lxml')
print(soup.prettify)
weather = soup.find_all('p')
tweet = weather[4].text.strip()

#Featured Image
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
executable_path = {'executable_path': 'C:/Users/Caitlin/Desktop/cwrubootcamp/chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)
browser.visit(url)
browser.click_link_by_partial_text('FULL IMAGE')
html = browser.html
soup = bs(html, 'lxml')
image = soup.find_all('a', class_ = 'button')
image_url = "https://www.jpl.nasa.gov" + (image[0]['data-link'])
browser.visit(image_url)
html = browser.html
soup = bs(html, 'lxml')
links = soup.find_all('div', class_ = 'download_tiff')
link = links[1].a['href']
image_link = "https://www.jpl.nasa.gov" + link[1:]

#Get Mars Table
url = 'https://space-facts.com/mars/'
mars_info = pd.read_html(url)
mars_df = pd.DataFrame.transpose(mars_info[0])
mars_df.columns = ['Equatorial Diameter', 'Polar Diameter', 'Mass', 'Moons', 'Orbit Distance', 'Orbit Period', 'Surface Temperature', 'First Record', 'Recorded By']
mars_df = mars_df.iloc[1:]
mars_html = mars_df.to_html()
mars_html.replace('\n', '')

#Hemisphere Photo Data
executable_path = {'executable_path': 'C:/Users/Caitlin/Desktop/cwrubootcamp/chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)

url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
hemispheres = ['Cerberus', 'Schiaparelli', 'Syrtis Major', 'Valles']

h_names = []
h_urls = []

for hemisphere in hemispheres:
    browser.visit(url)
    browser.click_link_by_partial_text(hemisphere)
    html = browser.html
    soup = bs(html, 'lxml')
    tempname = soup.find_all('h2', class_ = 'title')
    tempurl = soup.find_all('li')
    h_urls.append(tempurl[0].a['href'])
    h_names.append(tempname[0].text)

conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

db = client.Mars_Info
collection = db.Info

db.collection.insert_many( [mars_dict = {
        "Article Titles" : a_titles,
        "Article Text" : a_text,
        "Latest Weather" : tweet,
        "Featured Image" : image_link,
        "Mars Table" : mars_html,
        "Hemisphere Names" : h_names,
        "Hemisphere Images" : h_urls}])

    
#Name the app
app = Flask(__name__)

#Index route
@app.route("/scrape")
def scrape():
    return(mars_dict
    )

@app.route("/")
def index():
    mars = list(db.collection.find())
    
    return render_template("index.html", inventory=inventory)


#Initialize app
if __name__ == "__main__":
    app.run(debug=True)
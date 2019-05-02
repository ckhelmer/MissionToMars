################################################
##########SCRIPT TO SCRAPE AND STORE############
################################################

#Relevant library import
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import pandas as pd

def scrape_news():
    
    #Retrieve:
    url = 'https://mars.nasa.gov/news/'
    response = requests.get(url)
    
    #Parse and assign:
    soup = bs(response.text, 'lxml')
    a_titles = soup.find_all('div', class_ = 'content_title')
    a_text = soup.find_all('div', class_ = 'article_teaser_body')
    
def scrape_weather():
    
    #Retrieve:
    url = "https://twitter.com/marswxreport?lang=en"
    response = requests.get(url)
    
    #Parse and assign variable
    soup = bs(response.text, 'lxml')
    weather = soup.find_all('p')
    tweet = weather[4].text.strip()
    
def init_browser():
    executable_path = {'executable_path':'C:/Users/Caitlin/Desktop/cwrubootcamp/chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=True)
    
def scrape_featured_image():
    #Navigate first page:
    browser = init_browser()
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    browser.click_link_by_partial_text('FULL IMAGE')
    
    #Temporarily store site for navigation
    html = browser.html
    soup = bs(html, 'lxml')
    image = soup.find_all('a', class_ = 'button')
    image_url = "https://www.jpl.nasa.gov" + (image[0]['data-link'])
    
    #Navigation to full-size image:
    browser.visit(image_url)
    html = browser.html
    
    #Parse and assign variable
    soup = bs(html, 'lxml')
    links = soup.find_all('div', class_ = 'download_tiff')
    link = links[1].a['href']
    image_link = "https://www.jpl.nasa.gov" + link[1:]
    
def scrape_facts():
    #Bring table in via pandas
    url = 'https://space-facts.com/mars/'
    mars_info = pd.read_html(url)
    
    #Make it into a dataframe(I MAY CHANGE THIS BACK, I DON'T KNOW)
    mars_df = pd.DataFrame.transpose(mars_info[0])
    mars_df.columns = ['Equatorial Diameter', 'Polar Diameter', 'Mass', 'Moons', 'Orbit Distance', 'Orbit Period', 'Surface Temperature', 'First Record', 'Recorded By']
    mars_df = mars_df.iloc[1:]
    
    #Export as html
    mars_html = mars_df.to_html()
    mars_html.replace('\n', '')
    
def scrape_hemispheres():
    browser = init_browser()
    
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
        
    #Make into dictionary
    hemisphere_dict = {"names" : h_names,
                       "pix" : h_urls,}

def scrape_all():
    news = scrape_news()
    weather = scrape_weather()
    image = scrape_featured_image()
    facts = scrape_facts()
    hemispheres = scrape_hemispheres()
    
    mars_data = {"news" : news, 
                       "weather" : weather,
                       "featured_image" : image,
                       "fact_table" : facts,
                       "hemispheres" : hemispheres}
    
    return mars_data
    
    
    
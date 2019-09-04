# Declare Dependencies 
from bs4 import BeautifulSoup
from splinter import Browser
from selenium import webdriver
import pandas as pd
import requests
import urllib
import urllib.request
from bs4 import BeautifulSoup as bs

# create a method that will scrape the latest news on mars
def mars_news(browser):

    # Visit website
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")
    type(soup)

    # get the news title
    news_title = soup.find('div', class_='bottom_gradient').text
    news_p = soup.find('div', class_='rollover_description_inner').text

    # return the information needed
    return news_title, news_p

# create a method that will find the featured image
def featured_img(browser):
    
    # create the make_soup method to open the url
    def make_soup(url):
        thepage = urllib.request.urlopen(url)
        soupdata = BeautifulSoup(thepage, 'html.parser')
        return soupdata

    # define the link for the website in which the image will be
    featured_image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    soup = make_soup(featured_image_url)

    # create a loop that will find the designation 'article', where the link for the image is located
    for article in soup.findAll('article'):
        
        # define the image string
        image = article.get('style').replace("background-image: url('","").replace("');","")

    # create the link for the image itself
    image_url = 'https://www.jpl.nasa.gov' + image
    return image_url

# create a method that will find the latest mars weather tweet
def mars_tweet(browser):
    
    # define the urls that will be used
    mars_twitter_url = 'https://twitter.com/marswxreport'
    browser.visit(mars_twitter_url)

    # Create BeautifulSoup object
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # find the first tweet in the form of a text
    tweet = soup.find('p', class_='TweetTextSize').text
    return tweet

# create a method to scrape the table for Mars Facts
def mars_facts(browser):

    #scrape the website
    mars_facts_url = 'https://space-facts.com/mars/'
    
    #reat the html table and convert it into a pandas dataframe
    tables = pd.read_html(mars_facts_url)
    df = tables[0]
    df.columns = ['Mars - Earth Comarison', 'Mars', 'Earth']

    # Set the index to the `Description` column without row indexing
    df.set_index('Mars - Earth Comarison', inplace=True)
    #df

    # Convert dataframe into HTML table
    df_html = df.to_html()

    return df_html

# create a method that will scrape information about the mars hemispheres
def hemispheres_info(browser):

    # create the arrays that will be used
    hemisphere_dict = []
    hemisphere_link = []

    # create the make_soup method to open the url
    def make_soup(url):
        thepage = urllib.request.urlopen(url)
        soupdata = BeautifulSoup(thepage, 'html.parser')
        return soupdata
    
    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    
    # create a loop that will store the link to the hemisphere image url
    soup = make_soup(hemispheres_url)

    for href in soup.findAll('a'):
        temp = href['href']
        if temp[:8] == '/search/':
            hemisphere_link.append(temp)

    # create a loop that will loop throuth the 'hemisphere_link_name' array and click on each of the links
    for hemi in hemisphere_link:
        
        #create a link to scrape
        hemi_url = 'https://astrogeology.usgs.gov' + hemi
        
        # Visit the link that contains the full image website 
        browser.visit(hemi_url)
        
        # HTML Object of individual hemisphere information website 
        html = browser.html
        
        # Parse HTML with Beautiful Soup for every individual hemisphere information website 
        soup = BeautifulSoup(html, 'html.parser')
        
        # retrieve the full image and the name
        hemi_img = 'https://astrogeology.usgs.gov' + soup.find('img', class_='wide-image')['src']
        title = soup.find('h2', class_='title').text.replace(' Enhanced', '')
        
        # add link to dictionary
        hemisphere_dict.append({'title': title, 'img': hemi_img})

    return hemisphere_dict
# initialize Chrome
def scrape_website():
    # Inititate executable path
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    browser = Browser('chrome', **executable_path, headless=False)

    news_title, news_p = mars_news(browser)
     
    # store all the scraped information into a dictionary
    mars_dict = {
        "title": news_title,
        "first_paragraph": news_p,
        "featured_img": featured_img(browser),
        "tweet": mars_tweet(browser),
        "mars_facts": mars_facts(browser),
        "hemispheres": hemispheres_info(browser)
    }
    #print(mars_dict)
    #quite the browser
    browser.quit()

    #return the dictionary
    return mars_dict

scrape_website()
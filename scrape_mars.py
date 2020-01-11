# Importing libraries
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from selenium import webdriver
from splinter import Browser
import time
import re
import requests

def scrape():
    # ------------------------------------------
    # 1. Scrapping the headline and sub-headline
    # ------------------------------------------ 
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'

    driver = webdriver.Chrome('/usr/local/bin/chromedriver')
    driver.get(url)

    # Give the JS time to render
    time.sleep(1)

    # Scrap the web with BeautifulSoup
    soup = BeautifulSoup(driver.page_source)

    # Create a dictionary
    marsData = {}

    # Finding all the information that we want regarding the title and news.
    news_title = soup.find(class_='content_title').text
    news_p = soup.find(class_='article_teaser_body').text
    
    # Creating dictionary
    marsData['news_title'] = news_title
    marsData['news_p'] = news_p

    driver.close()

    # ------------------------------------------
    # 2. Scrapping the photo
    # ------------------------------------------ 
    # Scrapping the photo
    driver = webdriver.Chrome('/usr/local/bin/chromedriver')
    driver.get('https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars')
    element = driver.find_element_by_id("full_image")
    element.click()

    # Give the JS time to render
    time.sleep(1)

    soup = BeautifulSoup(driver.page_source)
    images = soup.find_all(class_="fancybox-image")

    for x in images:
        f_image = x['src'];

    featured_image_url = f"https://www.jpl.nasa.gov/{f_image}"

    # Creating dictionary
    marsData['featured_image_url'] = featured_image_url

    # Close the browser
    driver.close()

    # ------------------------------------------
    # 3. Scrapping the weather from twitters
    # ------------------------------------------ 
    # Scrapping the wheather
    response = requests.get('https://twitter.com/marswxreport?lang=en')
    bs = BeautifulSoup(response.text,'html.parser')
    weather = bs.find(class_='TweetTextSize').text

    # Using regrex expression to get rid of the pictures link
    mars_weather = re.sub(r'pic.twitter.com/\w+',"",weather)

    # Creating dictionary
    marsData['mars_weather'] = mars_weather

    # ------------------------------------------
    # 4. Scrapping tables with pandas
    # ------------------------------------------ 
    # Scrapping table with pandas
    marsFactsUrl = "https://space-facts.com/mars/"
    marsFactsTable = pd.read_html(marsFactsUrl)

    # Picking the first table and set index
    MarsFactRename = marsFactsTable[0]
    marsFact = MarsFactRename.rename(columns={0:"Descriptions",1:"Values"})


    # turning the table into html and get rid of \n
    marsFact = marsFact.to_html()
    marsFact = marsFact.replace('\n','')

    # Create dictionary
    marsData['marsFact'] = marsFact

    # ------------------------------------------
    # 5. Scrapping 4 images of the hemisphere
    # ------------------------------------------ 
    # Use splitter
    url_hemisphere = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    browser.visit(url_hemisphere)

    html = browser.html
    soup = BeautifulSoup(html,'html.parser')
    mars_hemis = []

    for i in range(4):
        time.sleep(1)
        
        #Find all the tag that has h3 and store in image
        img = browser.find_by_tag('h3')
        
        # For each img, click on it
        img[i].click()
        
        # Pre work for Splitter
        html = browser.html
        soup = BeautifulSoup(html,'html.parser')
        
        # Finding the image link
        partialLink = soup.find('img',class_="wide-image")['src']
        
        # Finding the title within the page
        imageTitle = soup.find('h2',class_='title').text
        
        # Concatenate the link and image link to create the link for the pics
        imageUrl = 'https://astrogeology.usgs.gov' + partialLink
        
        # Create a dictionary
        dic = {'title':imageTitle, 'img_url':imageUrl}
        
        # Appending the dictionary to mars_hemis
        mars_hemis.append(dic)
        
        # After finding the information go back and find the next imformation
        browser.back()
    
    # Create a dictionary
    marsData['mars_hemis'] = mars_hemis

    return marsData

    

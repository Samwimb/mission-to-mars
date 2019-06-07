#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Dependencies
from bs4 import BeautifulSoup
import requests
import os
import pandas as pd
from splinter import Browser
import time


# In[2]:
def scrape():


    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless = False)


    print("SAM after setting browser")
    #store all the scraped data in a dictionary
    mars_dictionary = {}

    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)


    # In[3]:


    # Retrieve page with the requests module
    html = requests.get(url)


    # In[4]:


    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(html.text, 'lxml')


    # In[5]:


    # news_title = soup.find('div', class_='content_title').text
    # print(news_title)
    # news_p = soup.find('div', class_='image_and_description_container').text
    # print(news_p)

    # print("title: ", news_title) 
    # print("paragraph: ", news_p)


    # In[6]:


    #get the title
    container = soup.find('div', class_="content_title")   
    news_title = container.a.text
            
                
    #get the paragraph description
    container = soup.find('div', class_="image_and_description_container")
    text_tot = container.find('div', class_= "rollover_description_inner")
    news_p = text_tot.text
                    

    print("title: ", news_title) 
    print("paragraph: ", news_p)

    mars_dictionary["news_title"] = news_title
    mars_dictionary["news_para"] = news_p


    # In[7]:


    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)


    # In[8]:


    jpl_url='https://www.jpl.nasa.gov'

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)


    #use splinter to get the URL of the image

    # HTML object
    html = browser.html
        
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')


    # In[9]:


    # Retrieve the article with the featured image
    article = soup.find('article', class_='carousel_item')

    # Use Beautiful Soup's find() method to navigate and retrieve attributes
    h1 = article.find('h1', class_ = 'media_feature_title').text
    print(h1)        

    # # Click the 'Full Image' button 
    # browser.click_link_by_partial_text('FULL IMAGE')


    # In[10]:

    browser.click_link_by_id("full_image")


    # In[11]:


    #then click "more info" to get the full size image
    time.sleep(2)
    browser.click_link_by_partial_text('more info')


    # In[12]:


    #get the html of the new page
    # HTML object
    html = browser.html
        
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')


    # In[13]:


    img_url = soup.find('img', class_="main_image")['src']
    # print(img_url)

    # fig_url = figure['src']

    # print(fig_url)


    # In[14]:


    featured_image_url = jpl_url + img_url
    print(featured_image_url)

    mars_dictionary["featured_img_title"] = h1
    mars_dictionary["featured_img_url"] = featured_image_url


    # In[15]:


    #Save the tweet text for the weather report as a variable called mars_weather.
    url = 'https://twitter.com/marswxreport?lang=en'
    # Retrieve page with the requests module
    response = requests.get(url)
    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(response.text, 'html.parser')


    # In[16]:


    stream = soup.find('div', class_="tweet")
    print(stream)


    # In[17]:


    streams = soup.find_all('div', class_="tweet")
    for tweet in streams:
        mars_weather = tweet.find('p').text
        if 'Sol' and 'pressure' in mars_weather:
            print(mars_weather)
            break
        else:
            pass

    mars_dictionary["weather"] = mars_weather
    # In[18]:


    # streams = soup.find_all('div', class_="tweet")
    # for tweet in streams:
    #     if (tweet['data-screen-name'] == "MarsWxReport"):
    #         #save the tweet
    #         mars_weather = tweet.find('p', class_="tweet-text").text
    #         print(mars_weather) 
    #         break
    #     else:
    #         pass


    # In[19]:


    # mars_weather = stream.find("p", class_="tweet-text").text
    # mars_weather = mars_weather.rstrip("pic.twitter.com/X7ISVrTgLY")
    # print(mars_weather)


    # In[20]:


    url = 'https://space-facts.com/mars/'
    # Retrieve page with the requests module
    response = requests.get(url)
    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(response.text, 'html.parser')

    tables = pd.read_html(url)
    tables[0]

    facts_df = pd.DataFrame(tables[0])

    #change the row headers
    header = pd.Series(["Type","Value"])
    facts_df.rename(columns = header, inplace=True)
    # facts_df.set_index('Type')
    html_table = facts_df.to_html()

    #remove new line characters
    html_table.replace('\n', '')

    # get_ipython().system('open table.html')

    mars_dictionary["html_table"] = html_table

    # In[28]:


    base_url = "https://astrogeology.usgs.gov"
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    # Retrieve page with the requests module
    response = requests.get(url)
    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(response.text, 'html.parser')


    # In[29]:


    hemispheres = soup.find_all('a', class_="itemLink")
    print(hemispheres)


    # In[30]:


    hemisphere_image_urls = []

    for item in hemispheres:
        
    #     try:
            #find title
            title = item.text
    #         print(title)
            
            #find link
            link = item['href']
    #         print(link)
            
            full_link = base_url + link
    #         print(full_link)
            #go to the link to get to the page with the full image 
            response = requests.get(full_link)
            # Create BeautifulSoup object; parse with 'html.parser'
            soup = BeautifulSoup(response.text, 'html.parser')
            
                                    
            #get full image url from href in the <a> in the div class='download'
            high_res = soup.find('div', class_='downloads')

            full_href = high_res.find('a')['href']

    #         print("full_href: ", full_href)

            #put title and image URL into dictionary    
            hemisphere_image_urls.append({"title": title, "img_url": full_href})
            
    #     except Exception as e:
    #         print("e: ",e)
    hemisphere_image_urls

    mars_dictionary["hemispheres"] = hemisphere_image_urls
    print(mars_dictionary)

    return mars_dictionary


# In[ ]:





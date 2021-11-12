# Import Dependencies
import pandas as pd
import requests
from splinter import Browser
from bs4 import BeautifulSoup as bs
import shutil
from IPython.display import Image
from webdriver_manager.chrome import ChromeDriverManager
import scrape_mars
import time

def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
    url = 'http://redplanetscience.com'
    browser.visit(url)
    time.sleep(2)
    soup = bs(browser.html, 'lxml')
    time.sleep(3)
    print(browser.html)
    latestTitle=soup.find_all('div',class_="content_title")[0].text
    latestTeaser=soup.find_all('div',class_="article_teaser_body")[0].text

    url = 'https://spaceimages-mars.com'
    browser.visit(url)
    time.sleep(2)
    soup = bs(browser.html, 'lxml')
    time.sleep(3)

    partial_url = soup.find('a',class_='showimg fancybox-thumbs')['href']
    featured_image_url=url +'/'+partial_url
    browser.quit()



    url = 'https://galaxyfacts-mars.com'
    table = pd.read_html(url)[0]
    header = table.iloc[0]
    table = table[1:]
    ind=table[0].tolist()
    marsList = table[1].tolist()
    earthList = table[2].tolist()
    marsDict = {'Mars':marsList,
                'Earth':earthList}
    table=pd.DataFrame(marsDict,index=ind)
    table

    html_table= table.to_html()
    html_table=html_table.replace('\n', '')
    html_table

    url = 'https://marshemispheres.com/'
    response = requests.get(url)
    soup = bs(response.text, 'lxml')
    results = soup.find_all('div', class_='description')

    hemisphere_image_urls=[]
    for each in results:
        title = each.h3.text    
        response = requests.get(f'https://marshemispheres.com/{each.a["href"]}')
        soup = bs(response.text,'lxml')
        hemiResult=soup.find_all('li')[0].a['href']
        hemisphere_image_urls.append({
            "title":title[0:-9],
            "img_url":f'https://marshemispheres.com/{hemiResult}'
            })
    print(hemisphere_image_urls)

    mission_mars_data = {
            'latestTitle':latestTitle,
            'latestTeaser':latestTeaser,
            'featuredImage':featured_image_url,
            'htmlTable':html_table,
            'hemishpereDict':hemisphere_image_urls
        }
        
    return mission_mars_data
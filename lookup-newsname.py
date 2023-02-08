import requests
from bs4 import BeautifulSoup
# Use requests_html
from requests_html import HTMLSession, AsyncHTMLSession
import asyncio, nest_asyncio
import re
from datetime import datetime
import urllib.parse


# Define the base URL and Query Parameter of the website
BASE_URL = 'https://www2.nhk.or.jp/gogaku/gendaieigo/detail/index.html'
QUERY_PARAM = '?no='

def create_url_from_date_query_param(base_url, query_param):
    # Input date and create the url to access the website for the date
    date = input("Input date:")
    url = base_url + query_param + date
    return url

def getHTMLcontents(url):
    # Get the HTML file from the URL
    html = requests.get(url)
    # Read the HTML file using BeautifulSoup
    content = BeautifulSoup(html.content, "html.parser")
    return content

# Pickup Japan datetime format from string
def pickup_jpn_date(text):
    s = text
    pattern = r'\d{4}年\d{1,2}月\d{1,2}日'
    jpn_date = re.findall(pattern, s)[0]
    return jpn_date

# Convert the strings of Japan datetime format to the datetime object using strptime method
# https://atmarkit.itmedia.co.jp/ait/articles/2111/24/news019.html

def convert_datetime_from_jpn(text):
    date_obj = datetime.strptime(text, '%Y年%m月%d日').date()
    return date_obj

# replace space to underscore
def replace_space_to_underscore(text):
    words = text.split()
    line = ''
    for word in words:
        if line:
            line += word +"_"
        else:
            line += "_" + word
    return line

# Print the created url of the website
url = create_url_from_date_query_param(BASE_URL,QUERY_PARAM)
#print(url)

# --- Using BeautifulSoup4 ---
# Get and Parse the HTML file from the URL
# soup = getHTMLcontents(url)

# Specify the news title using class property
# https://codezine.jp/article/detail/12230
# I use "class_" instead of using "class" because it's reserved by Python

# gendai_hd2_info = soup.find(class_="gendai-hd2-info")
# gendai_hd2_info__cat = soup.find(class_="gendai-hd2-info--cat")

# Print the news title of the date
# print(gendai_hd2_info) # -> <div class ="gendai_hd2_info"></div>
# print(gendai_hd2_info__cat)# -> None
# --- Using BeautifulSoup4 ---

# Next Step
# Use requests-html
# https://gammasoft.jp/blog/how-to-download-web-page-created-javascript/
# https://pypi.org/project/requests-html/

asession = AsyncHTMLSession()

# exec JavaScript using arender()
# https://blog.ikedaosushi.com/entry/2019/09/15/162445
async def exec_js(url):
    r = await asession.get(url)
    # Generate HTML using a browser engine (Chronium Browser)
    await r.html.arender()
    return r

# Neet to solve the error happend when executing "asyncio" in JupyterNotebook
nest_asyncio.apply()

# Execute the function "exec_js"
loop = asyncio.get_event_loop()
r = loop.run_until_complete(exec_js(url))

# CSS Selector for the news title
# wp > div.gendai-hd2 > div > div > p.gendai-hd2-info--cat
sel = '#wp > div.gendai-hd2 > div > div > p.gendai-hd2-info--broadcast'
all_elements = r.html
elements = all_elements.find(sel, first = True).text
lines = {}

# Devide and save text elements into lines list
for i, line in enumerate(elements.split("\n")):
    if i < 4:
        lines[i] = line
        # print('{}:{}'.format(i,lines[i]))
        # print('---'*10)

# Pickup aired date in Japan format from string
jpn_air_date = pickup_jpn_date(lines[0])

# Convert the strings of Japan datetime format to the datetime object using strptime method
# https://atmarkit.itmedia.co.jp/ait/articles/2111/24/news019.html
air_date = convert_datetime_from_jpn(jpn_air_date)

# Pickup news date in Japan format from string
jpn_news_date = pickup_jpn_date(lines[3])

# Convert the strings of Japan datetime format to the datetime object using strptime method
news_date = convert_datetime_from_jpn(jpn_news_date)

# replace spaces in English title with underscore
title = replace_space_to_underscore(lines[2])

# make filename from date and title in the page
filename = str(air_date) + title + str(news_date)
print(filename)

# Extract the iframe element that contains the news movie
movie_sel = "#wp > div.gendai-hd2 > div > div.gendai-hd2-video > div > iframe"
# movie_xpath = "/html/body/div[3]/div[4]/div/div[2]/div/iframe"
iframe = all_elements.find(movie_sel, first=True)
print(iframe)

# Get the 'src' attribute of the iframe dict
video_src = iframe._attrs['src']

# Get the base_url of the page
base_url = iframe.base_url

# Combine the base url and the iframe
# https://ja.stackoverflow.com/questions/45558/web%E3%83%9A%E3%83%BC%E3%82%B8%E3%81%AE%E3%82%BD%E3%83%BC%E3%82%B9%E3%81%AB%E8%B2%BC%E3%82%89%E3%82%8C%E3%81%9F%E3%83%AA%E3%83%B3%E3%82%AF%E5%85%88%E3%81%AEhtml%E3%83%95%E3%82%A1%E3%82%A4%E3%83%AB%E3%82%92%E5%8F%96%E5%BE%97%E3%81%99%E3%82%8B

video_url = urllib.parse.urljoin(base_url, video_src)
print(video_url)
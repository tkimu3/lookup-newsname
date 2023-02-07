import requests
from bs4 import BeautifulSoup
# Use requests_html
from requests_html import HTMLSession, AsyncHTMLSession
import asyncio, nest_asyncio

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
sel = '#wp > div.gendai-hd2 > div > div > p.gendai-hd2-info--cat'
element = r.html.find(sel, first=True)
print(element.text)


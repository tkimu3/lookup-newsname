import requests
from bs4 import BeautifulSoup


# Define the base URL and Query Parameter of the website
BASE_URL = 'https://www2.nhk.or.jp/gogaku/gendaieigo/detail/index.html'
QUERY_PARAM = '?no='

def create_url_from_date_query_param(base_url, query_param):
    # Input date and create the url to access the website for the date
    date = input("Input date:")
    url = base_url + query_param + date
    return url


# Print the created url of the website
url = create_url_from_date_query_param(BASE_URL,QUERY_PARAM)
print(url)

def getHTMLcontents(url):
    # Get the HTML file from the URL
    html = requests.get(url)
    # Read the HTML file using BeautifulSoup
    content = BeautifulSoup(html.content, "html.parser")
    return content


soup = getHTMLcontents(url)

# Specify the news title using class property
# https://codezine.jp/article/detail/12230
# I use "class_" instead of using "class" because it's reserved by Python
gendai_hd2_info = soup.find(class_="gendai-hd2-info")
gendai_hd2_info__cat = soup.find(class_="gendai-hd2-info--cat")

# Print the news title of the date
print(gendai_hd2_info) # -> <div class ="gendai_hd2_info"></div>
print(gendai_hd2_info__cat)# -> None


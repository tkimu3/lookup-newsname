# Define the base url of the website
BASE_URL = 'https://www2.nhk.or.jp/gogaku/gendaieigo/detail/index.html'

# Input date and create the url to access the website for the date
date = input("Input date:")
url = BASE_URL + "?no=" + date

# Print the created url of the website
print(url)

# Get the HTML file from the URL

# Specify the news title of from the file

# Print the news title of the date
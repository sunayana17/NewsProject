import requests
from bs4 import BeautifulSoup

# Making a GET request
r = requests.get('https://www.cnn.com/2023/03/17/politics/war-crime-prosecutions-what-matters/index.html')

# check status code for response received
# success code - 200
print(r)

# Parsing the HTML
soup = BeautifulSoup(r.content, 'html.parser')
#print(soup.prettify())
#print(soup.get_text())
#print(soup.find_all("p"))

s = soup.find('div', class_='article__content-container')
content = s.find_all('p')
# print(soup.find_all("p"))

for line in content:
    print(line.text)
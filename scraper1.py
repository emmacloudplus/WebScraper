import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv

kompas = requests.get('https://www.kompas.com/')
beautify = BeautifulSoup(kompas.content,'html5lib')

news = beautify.find_all('div', {'class','most__list clearfix'})
print(beautify.prettify())
arti = []
for each in news:
  nu = each.find('div', {'class','most__count'}).text
  title = each.find('h4', {'class','most__title'}).text
  lnk = each.a.get('href')
  rcount = each.find('div', {'class','most__read'}).text
  r = requests.get(lnk)
  soup = BeautifulSoup(r.text,'html5lib')
  content = soup.find('div', class_ = "read__content").text.strip()
  print(nu)
  print(title)
  print(lnk)
  print(rcount)

  arti.append({
    'Top Number': nu,
    'Headline': title,
    'Link': lnk,
    'Most Read': rcount,
    'Content':content
  })

print(arti)
df = pd.DataFrame(arti)
print(df)
df.to_csv('kompas.csv', index=False)
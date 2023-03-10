import requests
from bs4 import BeautifulSoup
import pandas as pd

url="https://www.cnn.com/"

page = requests.get("https://dataquestio.github.io/web-scraping-pages/simple.html")
soup = BeautifulSoup(page.content, 'html.parser')
print(page)
print(page.content)
print("Soup Prettify: "+soup.prettify())
print(soup.find('p'))
print("list: ",list(soup.children))
html = list(soup.children)[2]
body = list(html.children)[3]
p = list(body.children)[1]
p.get_text()
soup = BeautifulSoup(page.content, 'html.parser')
print("soup: ",soup)
soup.find_all("p")
soup.find_all('p')[0].get_text()
print(soup.find('p'))

page = requests.get("https://dataquestio.github.io/web-scraping-pages/ids_and_classes.html")
soup = BeautifulSoup(page.content, 'html.parser')
print(soup)
soup.find_all('p', class_='outer-text')
soup.find_all(class_="outer-text")
soup.find_all(id="first")
print(soup.select("div p"))

page = requests.get("https://forecast.weather.gov/MapClick.php?lat=37.7772&lon=-122.4168")
soup = BeautifulSoup(page.content, 'html.parser')
seven_day = soup.find(id="seven-day-forecast")
forecast_items = seven_day.find_all(class_="tombstone-container")
tonight = forecast_items[0]
print(tonight.prettify())

periods = tonight.find(class_="period-name").get_text()
short_desc = tonight.find(class_="short-desc").get_text()
temp = tonight.find(class_="temp").get_text()
print(periods)
print(short_desc)
print(temp)

img = tonight.find("img")
desc = img['title']
print(desc)

short_descs = [sd.get_text() for sd in seven_day.select(".tombstone-container .short-desc")]
temps = [t.get_text() for t in seven_day.select(".tombstone-container .temp")]
descs = [d["title"] for d in seven_day.select(".tombstone-container img")]
print(short_descs)
print(temps)
print(descs)

import pandas as pd
weather = pd.DataFrame({
    "period": periods,
    "short_desc": short_descs,
    "temp": temps,
    "desc":descs
})
print(weather)

temp_nums = weather["temp"].str.extract("(?Pd+)", expand=False)
weather["temp_num"] = temp_nums.astype('int')
print(temp_nums)

weather["temp_num"].mean()
is_night = weather["temp"].str.contains("Low")
weather["is_night"] = is_night
print(is_night)

print(weather[is_night])
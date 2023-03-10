import requests
import urllib.parse
import nltk
import re
import json

from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer


# print(soup.prettify())
def getlinks(soup):
    linkblocks = soup.find_all("a", class_="js-content-viewer")
    links = []
    for linkblock in linkblocks:
        links.append(urllib.parse.urljoin(url, linkblock.get("href")))
    # print(links)
    return links


def getarticle(news):
    title = news.find("title").text
    author = news.find("span", class_="caas-author-byline-collapse").text
    date = news.find("time", class_="caas-attr-meta-time").text
    body = news.find("div", class_="caas-body").text
    article = {"title": title, "author": author, "date": date, "body": body}
    return article



# for link in links:
#     response = requests.get(link)
#     news = BeautifulSoup(response.content,"html5lib")
#     new_links = getlinks(soup=news)
#     print(new_links)
#     # print(news)
#     # title = news.find("title").text
#     # author = news.find("span",class_="caas-author-byline-collapse").text
#     # date = news.find("time",class_="caas-attr-meta-time").text
#     # body = news.find("div",class_="caas-body").text
#     # articles.append({"title":title,"author":author,"data":date,"body":body})
#     articles.append(getarticle(news=news))
# print(len(articles))

def scrapnews(url, count):
    articles = []
    yahoo = requests.get(url)
    soup = BeautifulSoup(yahoo.content, "html5lib")
    links = getlinks(soup=soup)
    i = 0
    while i < len(links):
        link = links[i]
        response = requests.get(link)
        news = BeautifulSoup(response.content, "html5lib")
        article = getarticle(news)
        if len(article["body"].split()) >= 100:
            articles.append(article)
        newslinks = getlinks(news)
        for newslink in newslinks:
            if newslink not in links:
                links.append(newslink)
        i += 1
        print("scraped:", len(articles))
        if len(articles) >= count:
            break
    # print(len(articles))
    return articles

# Lemmatize and Stem and remove stopwords
def preprocessarticles(articles):
    lemmatizer = WordNetLemmatizer()
    ps = nltk.PorterStemmer()

    def preprocess(text):
        text = re.sub('[^a-zA-Z]', ' ', text)
        text = text.lower()
        tokens = word_tokenize(text)
        processed_tokens = [lemmatizer.lemmatize(ps.stem(word)) for word in tokens if
                            word not in set(stopwords.words('english'))]
        processed_text = ' '.join(processed_tokens)
        return processed_text

    for article in articles:
        preprocessed_body =preprocess(article["body"])
        article["preprocessed"]=preprocessed_body
    return articles

def savetofile(filename, articles):
    with open(filename, 'w') as f:
            json.dump(articles, f)

if __name__ == '__main__':
    nltk.download('stopwords')
    nltk.download('punkt')
    nltk.download('wordnet')
    url = "https://news.yahoo.com/politics/"

    articles = scrapnews(url, 100)
    processed_articles = preprocessarticles(articles)
    savetofile("articles.json",processed_articles)


from flask import Flask, jsonify, request
import sys
import codecs
import requests
from bs4 import BeautifulSoup
import json
import struct
app = Flask(__name__)

# install gunicorn


@app.route("/", methods=['GET', 'POST'])
def index():
    if(request.method == 'POST'):
        print(request)
        some_json = request.get_json()
        return jsonify({
            "you send": some_json
        }), 201
    else:
        return jsonify({
            "Seekr": "You Rock"
        })


@app.route('/defination/<message>', methods=['GET'])
def getDefination(message):
    def get_investopedia():
        # let us call and use Dictionary definition
        investopediaMessage = message.replace(' ', '+')
        investopediaMessage = message.replace('-', '+')
        url = 'https://www.investopedia.com/search?q='+investopediaMessage+' definition'
        source_code = requests.get(url)
        soup = BeautifulSoup(source_code.content, "lxml")
        pos = soup.findAll("div", {"id": "search-results__description_1-0"})
        try:
            definition = pos[0].text[1::]
        except:
            definition = "the word cannot be found "
        return (definition)

    def get_dictionary():
        # let us call and use Dictionary definition
        dictionaryMessage = message.replace(' ', '-')
        dictionaryMessage = message.replace('-', '-')
        url = 'https://www.dictionary.com/browse/'+dictionaryMessage
        source_code = requests.get(url)
        soup = BeautifulSoup(source_code.content, "lxml")
        pos = soup.findAll(
            "span", {"class": "one-click-content"})
        try:
            definition = pos[0].text + pos[1].text
        except:
            definition = "the word cannot be found "
        return (definition)

    return jsonify({
        'result': message,
        'dictionary': get_dictionary(),
        'investopedia': get_investopedia()
    })


@app.route('/news/<message>', methods=['GET'])
def getNews(message):
    def get_news():    
        newsMessage = message.replace(' ', '%20')
        newsMessage = message.replace('-', '%20')
        url = "https://www.businesstimes.com.sg/search/"+newsMessage
        source_code = requests.get(url)
        soup = BeautifulSoup(source_code.content, "lxml")
        content = soup.findAll("div", {"class": "media-body"})

        # # wipe the content in javascript
        # send_message(encode_message("W"))
        articles = list()

        for article in content:
            articleTitle = article.findAll("a")
            articleTime = article.findAll("time")
            try:
                title = articleTitle[0].text
                url = articleTitle[0]['href']
                time = articleTime[0].text
            except:
                title = "the word cannot be found "
                url = "the link cannot be found "
                time= "the time cannot be found"
            singleArticle={
                "title": title,
                "url":url,
                "time":time
            }
            articles.append(singleArticle)
        
        return(articles)

    return jsonify({
        'result': message,
        'articles': get_news()
    })


if __name__ == '__main__':
    app.run(debug=True)

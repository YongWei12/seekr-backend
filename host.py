from flask import Flask, jsonify, request
import sys
import codecs
import requests
from bs4 import BeautifulSoup
import json
import struct
app = Flask(__name__)

#install gunicorn


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


@app.route('/test/<message>', methods=['GET'])
def getTest(message):
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
        return ("I:"+definition)

    def get_dictionary():
        # let us call and use Dictionary definition
        dictionaryMessage = message.replace(' ', '-')
        dictionaryMessage = message.replace('-', '-')
        url = 'https://www.dictionary.com/browse/'+dictionaryMessage
        source_code = requests.get(url)
        soup = BeautifulSoup(source_code.content, "lxml")
        pos = soup.findAll(
            "span", {"class": "one-click-content css-1p89gle e1q3nk1v4"})
        try:
            definition = pos[0].text
        except:
            definition = "the word cannot be found "
        return ("D:"+definition)

    print(get_dictionary())
    print(get_investopedia())

    return jsonify({
        'result': message,
        'dictionary':get_dictionary(),
        'investopedia':get_investopedia()
    })


if __name__ == '__main__':
    app.run(debug=True)

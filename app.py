from flask import Flask, jsonify, request
import datetime
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)


@app.route('/keyboard', methods=['GET'])
def keyboard():
    return jsonify({'type': 'text'})

@app.route('/message', methods=["POST"])
def message():
    content = request.json['content']
    response = content

    if response == 'ㅁㅎ' or response == '만화':
        return jsonify(
            {
                'message': {
                    'text': '만화'
                },
                'keyboard': {
                    'type': 'text'
                }

            }
        )
    else:
        return jsonify(
            {
                'message': {
                    'text': response
                },
                'keyboard': {
                    'type': 'text'
                }

            })


def get_jangsisi_crawl():
    date = datetime.date.today()
    today = date.strftime("%m/%d")

    r = requests.get('http://zangsisi.net/')

    plain_text = r.text

    soup = BeautifulSoup(plain_text, 'html.parser')
    recent_list = soup.select('#recent-manga')

    for selector in recent_list:
        for a in selector.select('.list'):
            for b in a.select('.date'):
                if today == b.string:
                    print "★☆★☆" + today + " 만화 리스트★☆★☆"
                    for c in a.select('.contents > a'):
                        print c.contents[0], c.contents[1].string


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)

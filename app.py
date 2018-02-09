from flask import Flask, jsonify, request
from werkzeug.contrib.cache import SimpleCache
import datetime
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
cache = SimpleCache()

@app.route('/keyboard', methods=['GET'])
def keyboard():
    return jsonify({'type': 'text'})

@app.route('/message', methods=["POST"])
def message():
    content = request.json['content']
    response = content

    if response in ['ㅁㅎ','만화','오늘만화', '오늘의 만화','오늘의만화', '오늘만화']:
        text = get_jangsisi_crawl()
        return jsonify(
            {
                'message': {
                    'text': text
                },
                'keyboard': {
                    'type': 'text'
                }

            }
        )
    elif response in ['하이', 'ㅎㅇ', '안녕하세요', '안녕']:
        return jsonify(
            {
                'message': {
                    'text': '해피니스~ 안녕하세요 레드벨벳 아이린입니다.'
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
                    'text': response + "가 무슨말인지 아이린은 몰라요."
                },
                'keyboard': {
                    'type': 'text'
                }

            })


def get_jangsisi_crawl():
    rv = cache.get('item')
    if rv is None:
        date = datetime.date.today()
        today = date.strftime("%m/%d")

        r = requests.get('http://zangsisi.net/')

        plain_text = r.text
    
        soup = BeautifulSoup(plain_text, 'html.parser')
        recent_list = soup.select('#recent-manga')
        text = ''
        for selector in recent_list:
            for a in selector.select('.list'):
                for b in a.select('.date'):
                    if today == b.string:
                        text += "오늘의  만화("+ today + ")\n"
                        for c in a.select('.contents > a'):
                            text += c.contents[0] + c.contents[1].string + "\n"
                            text += "보러가기: " + c['href'] + "\n"
        text += "입니다."
        rv = text
        cache.set('item', rv, timeout=60 * 10)
    return rv

if __name__ == '__main__':
#    print(get_jangsisi_crawl())
    app.run(host='0.0.0.0', port=8081)

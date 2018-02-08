from flask import Flask, jsonify, request

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
                    'text': '만화목록'
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



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)

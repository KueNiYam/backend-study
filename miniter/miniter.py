from flask import Flask, jsonify, request
from flask.json import JSONEncoder

app = Flask(__name__)

class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)

        return JSONEncoder.default(self, obj)

app.json_encoder = CustomJSONEncoder

app.users = {}
app.id_count = 1
app.tweets = []

@app.route('/ping', methods=['GET'])
def ping():
    return 'pong'

@app.route('/sign-up', methods=['POST'])
def sign_up():
    new_user = request.get_json()
    new_user['id'] = app.id_count
    app.users[app.id_count] = new_user
    app.id_count = app.id_count + 1

    return jsonify(new_user)

@app.route('/tweet', methods=['POST'])
def tweet():
    # 페이로드는 사용에 있어서 전송되는 데이터를 뜻한다.
    payload = request.json
    user_id = int(payload['id'])
    tweet = payload['tweet']

    if user_id not in app.users:
        return '사용자가 존재하지 않습니다', 400

    if len(tweet) > 300:
        return '300자를 초과했습니다.', 400

    app.tweets.append({
        'user_id' : user_id,
        'tweet' : tweet
    })

    return '', 200

@app.route('/follow', methods = ['POST'])
def follow():
    payload = request.json
    user_id = int(payload['id'])
    to_follow = int(payload['follow'])

    if user_id not in app.users or to_follow not in app.users:
        return jsonify({'err': '사용자가 존재하지 않습니다.'}), 400

    user = app.users[user_id]
    user.setdefault('follow', set()).add(to_follow)

    return jsonify(user)

@app.route('/unfollow', methods = ['POST'])
def unfollow():
    payload = request.json
    user_id = int(payload['id'])
    to_follow = int(payload['unfollow'])

    if user_id not in app.users or to_follow not in app.users:
        return jsonify({'err': '사용자가 존재하지 않습니다.'}), 400

    user = app.users[user_id]

# discard 메소드는 remove 메소드와 다르게 없는 값의 경우에 대한 예외처리를 하지 않아도 된다.
    user.setdefault('follow', set()).discard(to_follow)

    return jsonify(user)

@app.route('/timeline/<int:user_id>', methods = ['GET'])
def timeline(user_id):
    if user_id not in app.users:
        return jsonify({'err':'사용자가 존재하지 않습니다..'}), 400

    follow_list = app.users[user_id].get('follow', set())
    follow_list.add(user_id)
    timeline = [tweet for tweet in app.tweets if tweet['user_id'] in follow_list]

    return jsonify({
        'user_id': user_id,
        'timeline': timeline
    })

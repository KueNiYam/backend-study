from flask import Flask, jsonify, request
from flask.json import JSONEncoder
from sqlalchemy import create_engine, text

class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)

        return JSONEncoder.default(self, obj)

def create_app(db_config = None):
    app = Flask(__name__)
    app.json_encoder = CustomJSONEncoder

    if db_config is None:
        app.config.from_pyfile("config.py")
    else:
        app.config.update(db_config)

    database = create_engine(app.config['DB_URL'], encoding = 'utf-8', max_overflow = 0)
    app.database = database

    @app.route('/ping', methods=['GET'])
    def ping():
        return 'pong'

    @app.route('/sign-up', methods=['POST'])
    def sign_up():
        new_user = request.get_json()
        new_user_id = app.database.execute(text("""
            INSERT INTO users(
                name,
                email,
                profile,
                hashed_password
            ) VALUES(
                :name,
                :email,
                :profile,
                :password
            )
        """), new_user).lastrowid # lastrowid: AUTO_INCREMENT를 사용하는 테이블일 겨우 새 행에 대한 AUTO_INCREMENT 값을 리턴

        row = app.database.execute(text("""
            SELECT
                id,
                name,
                email,
                profile
            FROM users
            WHERE id = :user_id
        """), {
            'user_id' : new_user_id
        }).fetchone()

        created_user = {
            'id': row['id'],
            'name': row['name'],
            'email': row['email'],
            'profile': row['profile']
        } if row else None

        return jsonify(created_user)

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

    return app # END create_app

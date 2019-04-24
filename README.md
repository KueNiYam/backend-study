Python3/Flask, Windows subsystem for linux(Ubuntu)

## Flask 실행

    FLASK_APP=app.py FLASK_DEBUG=1 flask run

## ping 엔드포인트

주로 API 서버가 현재 운행되고 있는지 아니면 정지된 상태인지를 간단하게 확인할 때 사용된다(Health check endpoint).

    from flask import Flask
    
    app = Flask(__name__)
    
    @app.route("/ping", methods=['GET'])
    def ping():
        return "pong"

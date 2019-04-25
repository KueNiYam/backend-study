"""
ping endpoint:
 - 주로 API 서버가 현재 운행되고 있는지 아니면 정지된 상태인지를 간단하게 확인할 때 사용된다.
 - 이러한 endpoint를 health check endpoint라고 한다.
"""

from flask import Flask

app = Flask(__name__)

@app.route('/ping', methods=['GET'])
def ping():
    """ping"""
    return 'pong'


Python3/Flask, Windows subsystem for linux(Ubuntu)

## Flask 실행

    FLASK_APP=app.py FLASK_DEBUG=1 flask run

# HTTP의 구조 및 핵심 요소

## HTTP
http는 HyperText Transfer Protocol의 약자로서, 웹상에서 서로 다른 서버 간에 하이퍼텍스트 문서, 즉 HTML을 서로 주고받을 수 있도록 만들어진 프로토콜 통신 규약이다

## HTTP 통신 방식
HTTP 통신 방식에는 2가지 특징이 있다. 하나는 HTTP의 요청(request)과 응답(response) 방식이고, 또 다른 특징은 stateless다.

## stateless
stateless는 말 그대로 상태(state)가 없다는 뜻으로, HTTP 통신에서는 상태(state)라는 개념이 존재하지 않는다. HTTP 프로토콜에서는 동일한 클라이언트와 서버가 주고받은 HTTP 통신들이라도 서로 연결되어 있지 않다. 즉, 각각의 HTTP 통신은 독립적이며 그 전에 처리된 HTTP 통신에 대해서 전혀 알지 못한다. 그렇기에 HTTP 프로토콜을 stateless라고 하는것이다.

다만, stateless이기 때문에 매번 HTTP 요청을 보낼 때 해당 요청을 처리하기 위해 필요한 모든 데이터를 매번 포함시켜야 한다는 단점이 있다. 예를 들면, 사용자가 그 전의 HTTP 통신을 통해서 로그인을 한 상태라고 하더라도 새로운 HTTP 요청을 보낼 때 해당 사용자의 로그인 사실 여부를 포함시켜서 보내야 한다. 이러한 점들을 해결하기 위해서 쿠키(cookie)나 세션(session) 등을 사용하여 HTTP 요청을 처리할 때 필요한 진행 과정이나 데이터를 저장한다.

 - 쿠키(cookie)는 웹 브라우저가 웹사이트에서 보내온 정보를 저장할 수 있도록 하는 조그마한 파일을 말한다.
 - 세션(session)은 쿠키와 마찬가지로 HTTP 통신상에서 필요한 데이터를 저장할 수 있게 하는 메커니즘이다. 쿠키와 차이점이라면 쿠키는 웹 브라우저, 즉 클라이언트 측에서 데이터를 저장하는 반면에 세션은 웹 서버에서 데이터를 저장한다.
 
 ## HTTP 요청 구조
 HTTP 요청은 다음과 같은 형태로 되어 있다.
 
     POST /payment-sync HTTP/1.1            ⑴
     
     Accept: application/json               ⑵
     Accept-Encoding: gzip, deflate
     Connection: keep-alive
     Content-Length: 83
     Content-Type: application/json
     Host: intropython.com
     User-Agent:HTTPie/0.9.3
     
     {                                      ⑶
        "imp_uid": "imp_1234567890",
        "merchant_uid": "order_id_8237352",
        "status": "paid"
     }
     
HTTP 요청 메시지는 크게 다음의 세 부분으로 구성되어 있다.
     
 - ⑴: Start Line
 - ⑵: Headers
 - ⑶: Body
     
### Start Line

이름 그대로 HTTP 요청의 시작줄이다. 예를 들어, "search" 엔드포인트에 GET HTTP 요청을 보낸다면 해당 HTTP 요청의 start line은 다음과 같다.

    GET /search HTTP/1.1
    
start line은 세 부분으로 구성되어 있다.

- HTTP 메소드
    - 해당 HTTP 요청이 의도하는 액션(action)을 정의하는 부분이다. HTTP 메소드에는 GET, POST, PUT, DELETE, OPTIONS 등 여러 메소드(method)들이 있다.
- Request target
    - 해당 HTTP 요청이 전송되는 목표 주소를 말한다. 예를 들어 "ping" 엔드포인트에 보내는 HTTP 요청의 경우 request target은 "/ping"이 된다.
- HTTP version

### 헤더

헤더 정보는 HTTP 요청 그 자체에 대한 정보를 담고 있다. key:value로 표현이 된다.

HTTP 헤더는 다양한 헤더가 있는데 그중 자주 사용되는 헤더 정보는 다음과 같다.

- Host
    - 요청이 전송되는 target의 호스트 URL 주소를 알려 주는 헤더다.
    - 예: Host: google.com
- User-Agent
    - 요청을 보내는 클라이언트에 대한 정보
- Accept
    - 해당 요청이 받을 수 있는 응답(response) body 데이터 타입을 알려주는 헤더.
    - MIME(Multipurpose Internet Mail Extensions) type이 value로 지정된다.
    - MIME type은 굉장히 다양하다. 그중 API 에서 자주 사용되는 MIME type은 application/json과 application/octet-stream, test/csv, text/html, image/jpeg, image/png, text/plain, 그리고 application/xml 정도다.
    - MIME type에 대한 더 자세한 정보는 Mozilla의 MIME type 페이지( http://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types_ )를 참고하도록 하자.
- Connection
    - 해당 요청이 끝난 후에 클라이언트와 서버가 계속해서 네트워크 연결(connection)을 유지할 것인지 아니면 끊을 것인지에 대해 알려주는 헤더.
    - HTTP 통신에서 서버 간에 네트워크 연결하는 과정이 다른 작업에 비해 시간이 걸리는 부분이므로 HTTP 요청 때마다 네트워크 연결을 새로 만들지 않고 HTTP 요청이 계속되는 한 처음 만든 연결을 재사용하는 것이 선호되는데, 그에 관한 정보를 전달하는 헤더다.
    - keep-alive이면 계속해서 유지, close이면 연결 닫음
- Content-Type
    - HTTP 요청이 보내는 메시지 body의 타입을 알려주는 헤더이다.
- Content-Length:
    - HTTP 요청이 보내는 메시지 body의 총 사이즈를 알려주는 헤더이다.
    
### Body
HTTP 요청 메시지에서 body 부분은 HTTP 요청이 전송하는 데이터를 담고 있는 부분이다.

## HTTP 응답 구조
HTTP 응답 메시지의 구조도 요청 메시지와 마찬가지로 크게 세 부분으로 구성되어 있다.

    HTTP/1.1 404 Not Found          ⑴
    
    Connection: close
    Content-Length: 1573            ⑵
    
    <!DOCTYPE html>                 ⑶
    ...
    
 - ⑴: Status Line
 - ⑵: Headers
 - ⑶: Body

### Status Line
이름 그대로 HTTP 응답 메시지의 상태를 간략하게 요약하여 알려주는 부분이다. 다음과 같은 형태로 구성되며, HTTP 요청의 start line과 마찬가지로 status line 도 다음과 같은 세 부분으로 구성되어 있다.

    HTTP/1.1 404 Not Found
    ⑴       ⑵       ⑶
    
- ⑴: HTTP Version
- ⑵: Status Code
- ⑶: Status Text

## 자주 사용되는 HTTP 메소드

### GET
GET 메소드는 이름 그대로 어떠한 데이터를 서버로부터 요청(GET)할 떄 주로 사용하는 메소드다. 즉, 데이터의 생성이나 수정 그리고 삭제 등의 변경 사항이 없이 단순히 데이터를 받아 오는 요청이 주로 GET 메소드로 요청된다.

### POST
GET과 다르게 데이터를 생성하거나 수정 및 삭제 요청을 할 때 주로 사용되는 HTTP 메소드다.

### OPTIONS
OPTIONS 메소드는 주로 특정 엔드포인트에서 허용하는 메소드들이 무엇이 있는지 알고자 하는 요청에서 사용되는 HTTP 메소드다. OPTIONS 요청을 보내면 응답에는 Allow 헤더를 통해 해당 엔드포인트가 허용하는 HTTP 메소드를 보내준다.

### PUT
데이터를 새로 생성할 때 사용되는 HTTP 메소드다. POST와 중복되는 의미이므로 데이터를 새로 생성하는 HTTP 요청을 보낼 때 굳이 PUT을 사용하지 않고 모든 데이터 생성 및 수정 관련한 요청은 다 POST로 통일해서 사용하는 시스템이 많아지고 있다.

### DELETE
이름 그대로 데이터 삭제 요청을 보낼 때 사용되는 메소드다. PUT과 마찬가지로 POST에 밀려서 잘 사용되지 않는 메소드다.

## 자주 사용되는 HTTP Status Code와 Text
HTTP 요청에서 HTTP 메소드를 잘 이해하는 것만큼 HTTP 응답에서는 HTTP status code와 text를 잘 이해하여 HTTP 응답을 보낼 때 적절한 status code의 응답을 보내는 것 또한 굉장히 중요하다. HTTP status code도 다양한 status code들이 있는데, 그중 가장 자주 사용되는 status code와 text에 대해서 더 자세히 알아보도록 하자.

### 200 OK
가장 자주 보게 되는~~가장 자주 보고 싶은~~ status code다. HTTP 요청이 문제없이 성공적으로 잘 처리 되었을 때 보내는 status code다.

### 301 Moved Permanently
HTTP 요청을 보낸 엔드포인트의 URL 주소가 바뀌었다는 것을 나타내는 status code다. 301 status code의 HTTP 응답은 Location 헤더가 포함되는 것이 일반적인데, Location 헤더에 해당 엔드포인트의 새로운 주소가 포함되어 나온다. 301 요청을 받은 클라이언트는 Location 헤더의 엔드포인트의 새로운 주소에 해당 요청을 다시 보내게 된다. 이러한 과정을 "redirection"이라고 한다.

    HTTP/1.1 301 Moved Permanently
    Location: http://www.example.org/index.asp
    
### 400 Bad Request
이름 그대로 HTTP 요청이 잘못된 요청일 때 보내는 응답 코드다. 주료 요청에 포함된 인풋(input) 값들이 잘못된 값들이 보내졌을 때 사용된다. 예를 들어, 사용자의 전화번호를 저장하는 HTTP 요청인데, 만일 전화번호에 숫자가 아닌 글자가 포함됐을 경우 해당 요청을 받은 서버에서는 잘못된 전화번호 값이므로 400 응답을 해당 요청을 보낸 클라이언트에게 보내는 것이다.

### 401 Unauthorized
HTTP 요청을 처리하기 위해서 해당 요청을 보내는 주체(사용자 혹은 클라이언트)의 신분(credential)확인이 요구되나 확인할 수 없었을 때 보내는 응답 코드다. 주로 해당 HTTP 요청을 보내는 사용자가 로그인이 필요한 경우 401 응답을 보낸다.

### 403 Forbidden
HTTP 요청을 보내는 주체(사용자 혹은 클라이언트)가 해당 요청에 대한 권한이 없음을 나타내는 응답 코드다.

### 404 Not Found
HTTP 요청을 보내고자 하는 URI가 존재하지 않을 때 보내는 응답코드다. 어떠한 웹 사이트에 잘못된 주소의 페이지를 접속하려고 하면 아마 "해당 페이지를 찾을 수 없습니다"라는 메시지가 있는 것을 본 적이 있을 것이다. 그러한 페이지를 404 페이지라고 한다.

### 500 Internal Server Error
이름 그대로, 내부 서버 오류가 발생했다는 것을 알려주는 응답 코드다. 즉, HTTP 요청을 받은 서버에서 해당 요청을 처리하는 과정에서 서버 오류(error)가 나서 해당 요청을 처리할 수 없을 때 사용하는 응답 코드다. ~~아마, API 개발을 하는 백엔드 개발자들이 가장 싫어하는 응답 코드일 것이다.~~

## API 엔드포인트 아키텍처 패턴
API의 엔드포인트 구조를 구현하는 방식에도 널리 알려지고 사용되는 패턴들이 있다. 크게 2가지가 있는데 하는 REST 방식이고 다른 하나는 GraphQL이다. REST 방식은 가장 널리 사용되는 API 엔드포인트 아키텍처 패턴(architecture pattern)이다. 이미 많은 API 시스템들이 REST 방식으로 구현되어 있다. GraphQL은 페이스북이 개발한 기술이며, 비교적 최근에 나온 기술이다.

### RESTful HTTP API
RESTful API는 API에서 전송하는 리소스(resource)를 URI(uniform resource identifier)로 표현하고 해당 리소스에 행하고자 하는 의도를 HTTP 메소드로 정의하는 방식이다.

예를 들어, 사용자 정보를 리턴하는 "/users"라는 엔드포인트에서 사용자 정보를 받아 오는 HTTP 요청은 다음과 같이 표현할 수 있다.

    HTTP GET /users
    GET /users
    
새로운 사용자를 생성하는 엔드포인트는 URI를 "/user"로 정하고 HTTP 요청은 다음과 같이 표현할 수 있다.

    POST /user
    {
        "name" : "송은우",
        "email" : songew@gmail.com
    }
    
이러한 구조로 설계된 API를 RESTful API라고 한다. RESTful API의 장점은 몇 가지가 있는데, 그중 가장 강한 장점은 자기 설명력(self-descriptiveness)이다. 즉 엔드포인트의 구조만 보더라도 해당 엔드포인트가 제공하는 리소스와 기능을 파악할 수 있다. API를 구현하다 보면 엔드포인트의 수가 많아지면서 엔드포인트들의 역할과 기능을 파악하기가 쉽지 않을 때가 많은데, REST 방식으로 구현하면 구조가 훨씬 직관적이며 간단해진다.

### GraphQL
한동안 REST 방식이 API를 구현하는 데 있어서 정석으로 여겨졌다. 그래서 많은 기업들이 API를 REST 방식으로 구현하였다. 그러나 REST 방식으로 구현해도 여전히 구조적으로 생기는 문제들이 있었다. 특히 가장 자주 생기는 문제는, API의 구조가 특정 클라이언트에 맞추어져서 다른 클라이언트에서 사용하기에 적합하지 않게 된다는 점이다. 페이스북이 2012년에 모바일 앱을 개발하기 시작했을 때 기존의 API는 페이스북의 사이트에 너무 맞추어져 있어서 모바일 앱 개발에 사용하기에는 적합하지 않았고, 모바일 앱용 API를 따로 만들어야 했다. 이러한 문제가 생기는 이유는, REST 방식의 API에서는 클라이언트들이 API가 엔드포인트들을 통해 구현해놓은 틀에 맞추어 사용해야 하다 보니 그 틀에서 벗어나는 사용은 어려워지기 때문이다.

이러한 문제를 해결하기 위해서 페이스북은 GraphQL을 만들게 된다. GraphQL은 REST 방식의 API와는 다르게 엔드포인트가 오직 하나다. 그리고 엔드포인트에 클라이언트가 필요한 것을 정의해서 요청하는 식이다. ~~기존 REST 방식의 API와 반대라고 보면 된다(서버가 정의한 틀에서 클라이언트가 요청하는 것이 아니라 클라이언트가 필요한 것을 서버에 요청하는 방식이다.~~

예를 들어, 아이디가 1인 사용자의 정보와 그의 친구들의 이름 정보를 API로부터 받아와야 한다고 예를 들어보자. 일반적인 REST 방식의 API에서는 다음과 같이 두 번의 HTTP 요청을 보내야 한다.

    GET /users/1
    GET /users/1/friends
    
앞서 본 두번의 요청을 한 번의 HTTP 요청으로 줄이기 위해서는 다음처럼 HTTP 요청을 보내야 한다.

    GET /users/1?include=friends.name
    
둘 다 비효율적이고 불필요하게 복잡한 것을 볼 수 있다. 만일 사용자 정보들 중 다 필요하지 않고 이름만 필요하든가 혹은 어떤 경우에는 친구들의 이름 외에도 친구들의 이메일도 필요하다면 HTTP 요청은 더 복잡해질 것이다. GraphQL을 사용하면 다음과 같이 HTTP 요청을 보내면 된다.

    POST /graphql
    
    {
        user(id: 1) {
            name
            age
            friends {
                name
            }
        }
    }
    
만일 사용자 정보는 이름만 필요하고, 대신 친구들의 이름과 이메일이 필요하다면 다음과 같이 보내면 된다.

    POST /graphql
    
    {
        user(id: 1) {
            name
            friends {
                name
                email
            }
        }
    }
        
----------------------------------------------------------------------------------------------------------------------------------------







    
     
     
     
     
     
     
     
     
     

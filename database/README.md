# 데이터베이스

## RDBMS vs NoSQL

### 관계형 데이터베이스 시스템의 장점

 - 데이터를 더 효율적이고 체계적으로 저장하고 관리할 수 있다.
 - 미리 저장하는 데이터들의 구조(테이블 스키마)를 정의하므로 데이터의 완전성이 보장된다.
 - 트랜잭션(transaction) 기능을 제공한다.

### 관계형 데이터베이스 시스템의 단점

 - 테이블을 미리 정의해야 하므로 테이블 구조 변화 등에 대해 덜 유연하다.
 - 확장이 쉽지 않다. 테이블 구조가 미리 정의되어야 하고 ACID를 보장해야하다 보니 단순히 서버를 늘리는 것만으로 확장하기가 쉽지 않고 서버의 성능 자체도 높여야 한다.
 - 서버를 늘려서 분산 저장하는 것도 쉽지 않다. 주로 스케일 아웃(scale out, 서버 수를 늘려서 확장하는 것)보다는 스케일 업(scale up, 서버의 성능을 높이는 것)으로 확장해야 한다.

### 비관계형 데이터베이스 시스템의 장점

 - 데이터 구조를 미리 정의하지 않아도 되므로 저장하는 데이터의 구조 변화에 유연하다.
 - 데이터베이스 시스템을 확장하기가 비교적 쉽다. 스케일 아웃, 즉 서버 수를 늘리는 방식으로 시스템 확장이 가능하다.
 - 확장하기가 쉽고 데이터의 구조도 유연하다 보니 방대한 양의 데이터를 저장하는데 유리하다.

### 비관계형 데이터베이스 시스템의 단점

 - 데이터의 완전성이 덜 보장된다.
 - 트랜잭션이 안 되거나 되더라도 비교적 불안정하다.

## 정리

관계형 데이터베이스 시스템은 주로 정형화된 데이터들 그리고 데이터의 완전성이 중요한 데이터들을 저장하는데 유리하다. 예를 들어, 전자상거래 정보, 은행 계좌 정보, 거래 정보 등을 저장하고 관리하는 데 사용된다.
반면에 비관계형 데이터베이스 시스템은 주로 비정형화 데이터, 그리고 완전성이 상대적으로 덜 유리한 데이터를 저장하는 데 유리하다. 로그 데이터가 좋은 예가 될 것이다.

-------------------------------------------------------------------------------

## SQL

CRUD - Create, Read, Update, Delete

JOIN

### SELECT

SELECT 구문은 관계형 데이터베이스 시스템에서 데이터를 읽어 들일 때 사용하는 SQL 구문이다. SELECT 구문의 기본적인 문법은 다음과 같다.

    SELECT
        column1,
		column2,
		column3,
		column4
	FROM table_name

예를 들어, users 라는 테이블에서 id, name, age, gender라는 칼럼 값을 읽고 싶다면 다음과 같이 SELECT 구문을 사용하면 된다.

	SELECT
		id,
		name,
		age,
		gender
	FROM users

SELECT 구문은 WHERE 구문과 같이 사용하며 검색이나 필터의 기능 또한 구현할 수 있다. 예를 들어, users라는 테이블에서 이름이 최근휘라는 사용자의 id, name, age, gender라는 칼럼 값을 읽고 싶다면 다음과 같이 구현하면 된다.

	SELECT
		id,
		name,
		age,
		gender
	FROM users
	WHERE name = "최근휘"

### INSERT

관계형 데이터베이스 시스템에서 데이터를 생성할 때 사용하는 INSERT 구문을 사용하게 된다. INSERT 구문의 기본적인 문법은 다음과 같다.

	INSERT INTO table_name (
		column1,
		column2,
		column3
	) VALUES (
		value1,
		value2,
		value3
	)

만일 users 테이블에 아래의 값을 생성해야 한다고 가정해 보자.

	{
		"id"		: 1,
		"name"		: "최근휘",
		"age"		: 26,
		"gender" 	: "남자"
	}

위의 데이터를 users 테이블에 생성하기 위해서는 다음과 같은 INSERT 구문을 사용할 수 있다.

	INSERT INTO users (
		id,
		name,
		age,
		gender
	) VALUES (
		1,
		"최근휘",
		26,
		"남자"
	)

만일 하나 이상의 데이터를 생성하고 싶다면 다음과 같이 INSERT 구문을 사용하면 된다.

	INSERT INTO users (
		id,
		name,
		age,
		gender
	) VALUES (
		1,
		"최근휘",
		26,
		"남자"
	), (
		2,
		"아이유",
		25,
		"여자"
	), (
		3,
		"그니",
		26,
		"남자"
	)

WHERE 구문과 같이 사용하지 않으면 해당 테이블의 모든 로우 값을 수정한다.

### UPDATE

UPDATE 구문은 기존의 데이터를 수정할 때 사용한다. UPDATE의 기본 문법은 다음과 같다.

	UPDATE table_name SET column1 = value1 WHERE column2 = value2

	UPDATE users SET age = 25 WHERE name = "아이유"

### DELETE

	DELETE FROM table_name WHERE column = value

	DELETE FROM users WHERE age < 20

WHERE 구문을 사용하지 않으면 해당 테이블의 모든 로우들을 지우게 된다.

### JOIN

JOIN 구문은 여러 테이블을 연결할 때 사용한다.

	SELECT
		table1.column1,
		table2.column2
	FROM table1 JOIN table2
	ON table1.id = table2.table_id
	
	SELECT
		users.name,
		user_address.address
	FROM users JOIN user_address
	ON users.id = user_address.user_id

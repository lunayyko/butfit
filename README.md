# 수업 예약관리 사이트 구축하기

## 사용 기술 및 tools
> - Back-End :  Python3.8, Django3.2, MySQL 
> - ETC : Git, Github, Postman

## 모델링
<img width="724" alt="Screen Shot 2022-01-06 at 8 30 19 PM" src="https://user-images.githubusercontent.com/8315252/148384686-d2bd5c15-b60e-4117-9fb4-a0ed569f0134.png">

## API
[링크-postman document](https://documenter.getpostman.com/view/16843815/UVXdNyod)

## 실행방법
1.원하는 경로에 해당 프로젝트를 깃 클론 받는다
```terminal
git clone https://github.com/lunayyko/butfit.git
```

2.manage.py가 있는 디렉토리 상에 아래의 내용이 포함된 my_settings.py파일을 추가한다.
```python
SECRET_KEY = '랜덤한 특정 문자열'

DATABASES = {
    'default' : {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'butfitapp',
        'USER': 'root',
        'PASSWORD': '1234',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

ALGORITHM = 'HS256'
```

3. 라이브러리들을 설치한다
```python
pip install -r requirements.txt 
```

4. 서버를 실행한다(파이썬이 설치되어있어야한다)
```python
python manage.py runserver
```




## 구현 기능
### 회원가입, 로그인
- 회원가입시 password 같은 민감정보는 단방향 해쉬 알고리즘인 `bcrypt`를 이용해서 암호화 하여 database에 저장하였습니다.
- 로그인이 성공적으로 완료되면, user정보를 토큰으로 반환할때, 양방향 해쉬 알고리즘인 `JWT`를 사용해서 응답을 하였습니다.

### 수업 셋팅하기(관리자)
- 수업 생성은 로그인시에(header에 token이 있는 상태) 유저의 role이 admin일 때만 가능하도록 하였습니다.
- 같은 이름의 수업이 있는 경우 에러메세지가 출력됩니다.
- 크레딧과 수업정원은 선택적으로 입력받고 디폴트로 1, 20으로 설정했습니다.

### 크레딧 구매 하기(유저)
- 크레딧의 갯수와 유효한 기간을 body에서 json으로 입력받아 크레딧 테이블에 저장되도록 하였습니다.

### 수업 예약 하기(유저)
- 로그인 후 쿼리 파라미터를 이용해 클래스 아이디를 입력해서 예약합니다.
- 같은 클래스 아이디가 부킹 테이블에 있는 경우 에러메세지가 출력됩니다.
- 사용자가 크레딧이 없거나 가용 크레딧이 수업 가격보다 적은 경우 에러메세지가 출력됩니다.
- 예약되면 사용자의 크레딧이 차감되고 부킹로그에 해당 내용이 기록됩니다.

### 수업 예약 취소 하기(유저)
- 로그인 후 쿼리 파라미터를 이용해 클래스 아이디를 입력해서 예약을 취소합니다.
- 수업 당일이면 에러메세지를 출력합니다.
- 수업 1일전이면 50%의 크레딧을 돌려받습니다.
- 수업 3일전이면 크레딧을 모두 돌려받습니다.
- 취소되면 부킹로그에 해당 내용이 기록됩니다.

### 수업 예약 리스트 보기(유저)
- 예약과 취소내역 로그를 모두 볼 수 있습니다.
- 각 로그별 크레딧이 나와있고 마지막에 잔여 크레딧이 출력됩니다.

### 수업 예약 현황 보기(관리자 페이지)
- 시작 날짜와 종료 날짜를 json으로 입력받아서 특정 기간별 취소되지 않고 예약이 진행된 수업들의 리스트를 볼 수 있습니다.
- 각 로그별 크레딧이 나와있고 마지막에 특정 기간별 결제된 크레딧의 총합을 확인할 수 있습니다.

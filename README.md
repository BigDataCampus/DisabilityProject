# DisabilityProject
code implementation


## 할일(8월 5일까지)

* branch1
1. DB(장소, 편의시설 Table) 구축
=> 크롤링 후 sqlite 파일(.db) 만들기

2. DB 연동
=> SQLalchemy-flask 모듈로 DB 연동 후 각 테이블의 데이터를 templates의 html파일에 출력(wtf 사용)

3. flask-admin 연동
=> /admin 접속 가능 하도록

-----------------------

* branch2

4. 장소 테이블의 좌표 구글 지도에 마커로 쭉 뿌려주기
=> 걍 SQLalchemy select 해서 파라미터 줘서 구글api 콜백 날리기

5. 마커 클릭하면 장소가 어떤 편의시설 가지고 있는지 보여줄 수 있도록
=> 난이도 중



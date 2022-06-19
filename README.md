# 1학기 종합 PJT_RC Car
### 프로젝트 개요
- 주제: 제어 가능한 RC카
- 기술스택: Vue.js, node.js, Arduino, QtPy
- 프로젝트 기간: 2021.11.22 ~ 2021.11.25
- 인원: 2명
- 기능
    - 리모콘 컨트롤러를 통한 RC카 제어
    - RC카로 받아온 센서값(온도, 습도) 웹 어플리케션을 통해 시각적으로 확인

### 구조도
![image](https://user-images.githubusercontent.com/97162920/174493435-c772fb68-3c9d-41c5-9fa7-9f2e69da740d.png)
- MySQL DB
- Command table과 Sensing table 사용

### 구현 결과
##### 리모트 컨트롤러
![image](https://user-images.githubusercontent.com/97162920/174493486-125d2144-81c0-4fc9-8fdc-def670f30667.png)

##### 웹 어플리케이션
![image](https://user-images.githubusercontent.com/97162920/174493625-e9592efb-b794-4f20-8183-d31acc847fe6.png)
- RC카의 센서를 통해 얻은 기압, 온도, 습도 데이터를 1초마다 갱신

##### 구동 영상
![video](./assets/RC카구동.mp4)

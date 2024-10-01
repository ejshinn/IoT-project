# 시각장애인을 위한 스마트 지팡이

## 🕰️개발 기간
* 2020.11.26 ~ 2020.12.10

## 📌주요 기능
#### use_stick.py
- 주변 밝기 감지를 통한 LED ON/OFF 구현
- 절사평균을 이용한 거리 측정
- 장애물 거리별 경고음 발생
#### find_stick.py
- DDNS를 이용하여 웹 서버의 도메인 네임 생성
- 지팡이 분실 시 찾기 및 중단 웹 구현
- 웹 페이지에서 FIND 버튼 클릭 -> LED ON, 부저 ON, OLED에 사용자 정보 출력
- 웹 페이지에서 STOP 버튼 클릭 -> LED OFF, 부저 OFF, OLED CLEAR

## 💡회로도
<img src="https://github.com/user-attachments/assets/3663025b-d1e0-4c03-a1dd-d760f482eab7" width="70%" height="30%"></img>

## 🌐웹 페이지
#### FIND 버튼 클릭
<img src="https://github.com/user-attachments/assets/d7485fb7-1d6f-4982-b744-2fc6fac470dc" width="70%" height="30%"></img>

</br>

#### STOP 버튼 클릭
<img src="https://github.com/user-attachments/assets/29a67925-a872-4845-8ee7-4e52b4ac6ecb" width="70%" height="30%"></img>

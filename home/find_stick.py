#-*-coding:utf-8-*-
# 필요한 라이브러리를 불러옴
import Adafruit_SSD1306
from PIL import Image, ImageDraw, ImageFont
import RPi.GPIO as GPIO
from flask import Flask, request
from flask import render_template

# 불필요한 warning 제거, GPIO핀의 번호 모드 설정
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# 사용할 GPIO 핀 번호 설정
led = 21
bz_pin = 18

# LED 핀을 출력으로 설정
GPIO.setup(led, GPIO.OUT, initial=GPIO.LOW)
# GPIO 18번 핀을 출력으로 설정
GPIO.setup(bz_pin, GPIO.OUT)

# OLED 128X64(i2c_address = 연결된 OLED 주소 ) 인스턴스 disp 생성
disp = Adafruit_SSD1306.SSD1306_128_64(rst=None, i2c_address=0x3C)

# OLED 화면 초기화
disp.begin()

# OLED 화면 클리어
disp.clear()
disp.display()

# 주워진 mode('1';흑백화면) 크기(width, height)를 가지고 이미지 생성
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# 이미지 상에 그리기를 수행할 object 생성
draw = ImageDraw.Draw(image)

# 이미지 상에 직사각형 그리기[위치와 크기, 윤곽선 색(outline), 채우기 색(fill) 설정]
draw.rectangle((0, 0, width, height), outline=0, fill=0)    # 0: 검정색, 255: 흰색

# OLED 화면에 출력할 직사각형와 문자열의 left top corner 위치(x,y) 설정
x = 0
padding = -2
y = padding

# OLED 화면에 출력할 문자열의 폰트 설정
font = ImageFont.load_default()

# PWM 인스턴스 p를 만들고 GPIO 18번을 PWM 핀으로 설정하고 주파수는 100Hz로 설정
p = GPIO.PWM(bz_pin, 100)
# duty cycle을 0으로 설정하여 PWM 시작
p.start(0)

app = Flask(__name__)           # flask 웹서버 객체 생성

@app.route("/HongGilDong/1234")
def home():
	return render_template("report_of_loss.html")

@app.route("/HongGilDong/1234/find")
def find():
    try:
        GPIO.output(led, 1)     # LED 켜짐

        # 사용자 정보 OLED 화면에 출력
        draw.text((x, y), 'Please contact me.', font= font, fill=255)
        draw.text((x, y+16), 'name: Hong Gil Dong', font=font, fill=255)
        draw.text((x, y+24), 'Phone: 010-1234-5678', font=font, fill=255)

        # 화면 표시
        disp.image(image)
        disp.display()

        p.ChangeDutyCycle(99)    # duty cycle 변경
        p.ChangeFrequency(523)   # 주파수 변경

        return "ok"    
		
    except expression as identifier:
	    return "fail"
		
@app.route("/HongGilDong/1234/stop")
def stop():
    try:
        p.ChangeDutyCycle(0)    # duty cycle 변경
        GPIO.output(led, 0)     # LED 꺼짐
	
	# OLED 화면 클리어
        disp.clear()
        disp.display()
	
        return "ok"
	
    except expression as identifier:
        return "fail"

if __name__ == "__main__":
    app.run(host="0.0.0.0")    # flask 웹서버 실행

GPIO.output(led, 0)            # LED 꺼짐
p.stop()                       # PWM 종료
GPIO.cleanup()                 # GPIO 설정 초기화

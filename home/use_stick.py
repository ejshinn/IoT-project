#-*-coding:utf-8-*-
# 필요한 라이브러리를 불러옴
import time
import spidev
import RPi.GPIO as GPIO

# 불필요한 warning 제거, GPIO핀의 번호 모드 설정
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# MCP3008 채널 중 센서에 연결한 채널 설정 
ldr_channel = 0

# 사용할 GPIO 핀 번호 설정
led = 21
TRIG = 23
ECHO = 24
bz_pin = 18

# LED 핀을 출력으로 설정
GPIO.setup(led, GPIO.OUT, initial=GPIO.LOW)
# trigger 핀과 echo 핀을 각각 출력과 입력으로 설정
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
# GPIO 18번 핀을 출력으로 설정
GPIO.setup(bz_pin, GPIO.OUT)

# SPI 인스턴스 spi 생성
spi = spidev.SpiDev()
# SPI 통신 시작
spi.open(0,0)
# SPI 통신 속도 설정
spi.max_speed_hz = 100000

# MCP3008의 0~7까지 8개의 채널에 입력된 아날로그 전압값을 MCP3008이 디지털값으로 변환하여 SPI 통신을 통해
# MCP3008에서 라즈베리 파이로 읽어옴
def readadc(adcnum):
    if adcnum > 7 or adcnum < 0:
        return -1
    r = spi.xfer2([1, (8+adcnum) << 4, 0])    # MCP3008의 adcnum번 채널에 입력된 아날로그 전압값을 MCP3008이 디지털로
                                              # 변환한 값을 SPI 통신을 통해 라즈베리 파이로 읽어옴
    data = ((r[1] & 3) << 8) + r[2]           # data: MCP3008를 통해 아날로그 전압값을 디지털로 변환한 값
    return data  # r[0]은 무시됨, r[1]의 하위 2비트는 ADC 값의 상위 2비트가 되고 r[2]의 8비트는 ACD 데이터의 하위 8비트가 됨
                 # 이 비트들을 합쳐서 총 10비트의 데이터가 최종적으로 MCP3008를 통해 아날로그 전압값을 디지털로 변환한 값이 됨

# PWM 인스턴스 p를 만들고 GPIO 18번을 PWM 핀으로 설정하고 주파수는 100Hz로 설정
p = GPIO.PWM(bz_pin, 100)

# 4옥타브 도의 주파수
first = 262
# 4옥타브 도, 미의 주파수
second = [262, 330]
# 4옥타브 도, 미, 솔의 주파수
third = [262, 330, 392]
# 4옥타브 도, 미, 솔, 5옥타브 도의 주파수
forth = [262, 330, 392, 523]

# trigger 핀으로부터 0V(0, False) 출력 (즉, 출력하지 않음)
GPIO.output(TRIG, False)
time.sleep(2)

p.start(0)                                      # duty cycle을 0으로 설정하여 PWM 시작

def ldr_led(ldr_value):                         # ldr_value: MCP3008를 통해 아날로그 전압값을 디지털로 변환한 값
    print("-----------------------------")
    print("LDR Value: %d" % (ldr_value))

    if(ldr_value < 100):                        # ldr_value가 100 미만이면
        print("LED ON!\n")
        GPIO.output(led, 1)                     # LED 켜짐
    else:                                       # ldr_value가 100 이상이면
        print("LED OFF!\n")
        GPIO.output(led, 0)                     # LED 꺼짐
    time.sleep(0.1)

try:
    while True:
        ldr_led(readadc(ldr_channel))           # readadc 함수로 ldr_channel의 SPI 데이터를 읽어옴

        data= [0, 0, 0, 0, 0]                   # 거리 측정값 데이터 리스트
        sum = 0
        distnace = 0
    
        for i in range (len(data)):
            GPIO.output(TRIG, True)             # trigger 핀으로부터 3.3V(1, True) 출력 초음파 발사
            time.sleep(0.00001)
            GPIO.output(TRIG, False)            # trigger 핀으로부터 0V(0, False) 출력 (즉, 출력하지 않음)
        
            while GPIO.input(ECHO) == False:    # echo 핀에 0V(0, False) 입력될 경우
                start = time.time()             # time.time(): 1970년 1월 1일 0시 0분 0초 이후 경과한 시간을 초단위로 반환
            while GPIO.input(ECHO) == True:     # echo 핀에 3.3V(1, True) 입력될 경우 (물체에 반사되어 초음파 수신)
                stop = time.time()
            
            check_time = stop - start           # 초음파가 발사되어 수신될 때까지 걸린 시간
            data[i] = check_time * 34300 / 2    # 초음파 센서와 물체와의 거리 계산
    
        min = data[0]
        max = data[4]
    
        for x in range (len(data)):
            if min > data[x]:
                min = data[x]                   # 최솟값 구하기
            if max < data[x]:
                max = data[x]                   # 최댓값 구하기
            sum += data[x]                      # 거리 측정값들의 합 구하기
            print("data[%d]: %d"%(x,data[x]))
        
        distance = (sum - max - min) / 3        # 이상 값(최댓값, 최솟값)을 제거한 평균 거리 계산
        print("Distance : %.lf cm\n"%(distance))

        
        if(distance <= 100 and distance >= 50): # 평균 거리가 100cm 이하, 50cm 이상이면
            p.ChangeDutyCycle(99)               # duty cycle 변경
            p.ChangeFrequency(first)            # 주파수 변경
            time.sleep(0.1)
        elif(distance < 50 and distance >= 30): # 평균 거리가 50cm 미만, 30cm 이상이면
            for fr in second:
                p.ChangeDutyCycle(99)           # duty cycle 변경
                p.ChangeFrequency(fr)           # 주파수 변경
                time.sleep(0.1)
        elif(distance < 30 and distance >= 10): # 평균 거리가 30cm 미만, 10cm 이상이면
            for fr in third:
                p.ChangeDutyCycle(99)           # duty cycle 변경
                p.ChangeFrequency(fr)           # 주파수 변경
                time.sleep(0.1)
        elif(distance < 10):                    # 평균 거리가 10cm 미만이면
            for fr in forth:
                p.ChangeDutyCycle(99)           # duty cycle 변경
                p.ChangeFrequency(fr)           # 주파수 변경
                time.sleep(0.1)
        else:                                   # 평균 거리가 100cm 초과라면
            p.ChangeDutyCycle(0)                # duty cycle 변경

        time.sleep(0.1)

except KeyboardInterrupt:                       # 키보드 Ctrl+C 눌렀을 때 예외 발생
    pass                                        # 무한반복을 빠져나와 아래의 코드를 실행

GPIO.output(led, 0)                             # LED 꺼짐
p.stop()                                        # PWM 종료
GPIO.cleanup()                                  # GPIO 설정 초기화

import RPi.GPIO as GPIO
from time import sleep, time
trig = 4
echo = 17
def get_pulse_time_v2(trig_pin, echo_pin):
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    GPIO.setup(trig_pin, GPIO.OUT)
    GPIO.setup(echo_pin, GPIO.IN)
    cnt1 = 0
    cnt2 = 0

    GPIO.output(trig_pin, True)
    sleep(0.00001)
    GPIO.output(trig_pin, False)

    start = time()
    while GPIO.input(echo_pin) == 0:
        start = time()
        cnt1 += 1
        if cnt1 > 1000:
            break

    stop = time()
    while GPIO.input(echo_pin) == 1:
        stop = time()
        cnt2 += 1
        if cnt2 > 1000:
            break

    return (stop - start)

def calculate_distance(duration):
    speed = 343
    distance = speed * duration / 2
    return distance
    
    
def calc_dist_cm_v2(trig_pin, echo_pin):
    duration = get_pulse_time_v2(trig_pin, echo_pin)
    distance = calculate_distance(duration)
    distance_cm = int(distance*10000)
    #dis_cm = int(distance_cm)
    #if dis_cm > 150:
     #   dis_cm = 150
    return distance_cm

while True:
    duration = get_pulse_time_v2(trig,echo)
    distance = calculate_distance(duration)
    #distance = calc_dist_cm_v2(trig,echo)
    print(distance)
    sleep(0.5)

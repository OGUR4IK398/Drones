from djitellopy import Tello
from time import sleep
import KeyPressModule as kp
import numpy as np
import cv2
import math

##### Параметры #####
f_speed = 140 / 10
a_speed = 300 / 10
interval = 0.01
d_interval = f_speed * interval
a_interval = a_speed * interval

# init
x, y = 500, 500
a = 0
yaw = 0
kp.init()

c = 0

drone = Tello()
drone.connect()
print(drone.get_battery())
points = [(0, 0), (0, 0)]


def get_keyboard_input():
    global x, y, yaw, a, c
    lr, fb, ud, yv = 0, 0, 0, 0
    speed = 40
    a_speed1 = 70
    d = 0

    if kp.get_key('a'):
        lr = -speed
        d = d_interval
        a = -180
    elif kp.get_key('d'):
        lr = speed
        d = -d_interval
        a = 180

    if kp.get_key('w'):
        fb = speed
        d = d_interval
        a = 270
    elif kp.get_key('s'):
        fb = -speed
        d = -d_interval
        a = -90

    if kp.get_key('q'):
        yv = -a_speed1
        yaw = -a_interval
    elif kp.get_key('e'):
        yv = a_speed1
        yaw = a_interval

    if kp.get_key('LSHIFT'):
        ud = speed
    elif kp.get_key('LCTRL'):
        ud = -speed

    if kp.get_key('1'):
        drone.takeoff()
        sleep(3)
    elif kp.get_key('2'):
        drone.land()
        sleep(3)

    sleep(interval)

    a += yaw
    x += int(d * math.cos(math.radians(a)))
    y += int(d * math.sin(math.radians(a)))

    return [lr, fb, ud, yv, x, y]


def draw_points(img, points):
    for point in points:
        cv2.circle(img, point, 3, (255, 0, 0), cv2.FILLED)
    cv2.circle(img, points[-1], 3, (0, 255, 0), cv2.FILLED)

    cv2.putText(
        img,
        f'({(points[-1][0] - 500) / 100}, {(points[-1][1] - 500) / 100}) m',
        (points[-1][0] + 10, points[-1][1] + 30),
        cv2.FONT_HERSHEY_SIMPLEX, 1,
        (255, 0, 255), 1
    )


while True:
    values = get_keyboard_input()
    drone.send_rc_control(*(values[0:4]))
    img = np.zeros((1000, 1000, 3), np.uint8)
    if points[-1][0] != values[4] or points[-1][1] != values[5]:
        points.append((values[4], values[5]))
    draw_points(img, points)
    cv2.imshow('Output', img)
    cv2.waitKey(1)
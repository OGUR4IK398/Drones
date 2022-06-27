import numpy as np
from djitellopy import Tello
import cv2
import time

drone = Tello()
drone.connect()
print(drone.get_battery())
drone.streamon()
time.sleep(3)
drone.takeoff()

cap = cv2.VideoCapture(1)


file = open('thresholds.txt', 'r')
HSV_values = file.read()
file.close()

sensors = 3
threshold = 0.2

width, height = 480, 360
sensitivity = 3
weights = [-25, -15, 0, 15, 25]
f_speed = 15
curve = 0


# Создаем маску
def thresholding(img):
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower = np.array([*HSV_values[:3]])
    upper = np.array([*HSV_values[3:]])

    # Создание маски
    mask = cv2.inRange(img_hsv, lower, upper)
    return mask


def get_contours(img_tres, img):
    cx = 0

    contours, hier = cv2.findContours(img_tres, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    if len(contours) != 0:
        # Получаем самый большой контур
        biggest = max(contours, key=cv2.contourArea)

        x, y, w, h = cv2.boundingRect(biggest)

        cx = x + w // 2
        cy = y + h // 2

        # Рисуем контуры
        cv2.drawContours(img, biggest, -1, (255, 0, 255), 7)
        cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)

    return cx


def get_sensor_output(img_tres, sensors):
    imgs = np.hsplit(img_tres, sensors)
    total_pixels = (img.shape[1] // sensors) * img.shape[0]

    # то, что return
    sen_out = []

    # Обрабатыаем кол-во белых пикселей
    for x, im, in enumerate(imgs):
        pixel_counter = cv2.countNonZero(im)

        # Создание 3 чисел для 3 сенсоров
        # То есть если найденный элемент занимает более 20% (threshold) площади
        # Сектора, то добавляем для этого сектора значение 1
        if pixel_counter > threshold * total_pixels:
            sen_out.append(1)
        else:
            sen_out.append(0)
    return sen_out


def send_command(sen_out, cx):
    global curve

    # Translation
    lr = (cx - width // 2) // sensitivity
    lr = int(np.clip(lr, -10, 10))
    # Мелко изменение - не учитываем
    if 2 > lr > -2:
        lr = 0

    # Rotation

    ### Refactor!!!
    if sen_out == [1, 0, 0]:
        curve = weights[0]
    elif sen_out == [1, 1, 0]:
        curve = weights[1]
    elif sen_out == [0, 1, 0]:
        curve = weights[2]
    elif sen_out == [0, 1, 1]:
        curve = weights[3]
    elif sen_out == [0, 0, 1]:
        curve = weights[4]
    elif sen_out == [0, 0, 0]:
        curve = weights[2]
    elif sen_out == [1, 1, 1]:
        curve = weights[2]
    elif sen_out == [1, 0, 1]:
        curve = weights[2]

    drone.send_rc_control(lr, f_speed, 0, curve)


while True:
    img = drone.get_frame_read().frame
    img = cv2.resize(img, (width, height))
    img = cv2.flip(img, 0)
    # Получение маски
    img_tres = thresholding(img)

    cx = get_contours(img_tres, sensors)
    sen_out = get_sensor_output(img_tres, sensors)
    send_command(sen_out, cx)

    cv2.imshow("OUTPUT", img)
    cv2.imshow("PATH", img_tres)
    if cv2.waitKey(1) and 0xFF == ord('q'):
        drone.land()
        break

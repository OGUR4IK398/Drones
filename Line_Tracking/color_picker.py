from djitellopy import Tello
import cv2
import numpy as np
import KeyPressModule as kp
import pygame
from time import sleep

kp.init()

frame_width = 480
frame_height = 360


# Подключение дрона
drone = Tello()
drone.connect()
print(drone.get_battery())
drone.streamon()


# Костыль, но неважно :)
def empty():
    pass


# Функция работает при нажатии на кнопку сохранения
def save_thresholds():
    file = open('thresholds.txt', 'w')
    file.write(f"[{h_min}, {s_min}, {v_min}, {h_max}, {s_max}, {v_max}]")
    file.close()


# Настройки окошка
cv2.namedWindow("HSV")
cv2.resizeWindow("HSV", 640, 240)
cv2.createTrackbar("HUE MIN", "HSV", 0, 179, empty)
cv2.createTrackbar("HUE MAX", "HSV", 179, 179, empty)
cv2.createTrackbar("SAT MIN", "HSV", 0, 255, empty)
cv2.createTrackbar("SAT MAX", "HSV", 255, 255, empty)
cv2.createTrackbar("VAL MIN", "HSV", 0, 255, empty)
cv2.createTrackbar("VAL MAX", "HSV", 255, 255, empty)
# cv2.createButton("SAVE", save_thresholds)

frame_counter = 0


while True:
    # Получение и обработка изображения с камеры
    img = drone.get_frame_read().frame
    img = cv2.resize(img, (frame_width, frame_height))
    img = cv2.flip(img, 0)
    img_HSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Получен значений ползунков настройки
    h_min = cv2.getTrackbarPos("HUE MIN", "HSV")
    h_max = cv2.getTrackbarPos("HUE MAX", "HSV")
    s_min = cv2.getTrackbarPos("SAT MIN", "HSV")
    s_max = cv2.getTrackbarPos("SAT MAX", "HSV")
    v_min = cv2.getTrackbarPos("VAL MIN", "HSV")
    v_max = cv2.getTrackbarPos("VAL MAX", "HSV")
    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])

    # Проверка каждого пикселя на соответствие. true - белый, false - черный
    mask = cv2.inRange(img_HSV, lower, upper)

    # Рисование черно-белой картинки на основе маски
    result = cv2.bitwise_and(img, img, mask=mask)
    print(f"[{h_min}, {s_min}, {v_min}, {h_max}, {s_max}, {v_max}]")

    # Обработка сохранения thresholds в файл через нажатие кнопки на клаве (s)
    if kp.get_key('s'):
        save_thresholds()

    # Покраска маски в серый
    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

    # Распологаеем 3 изображения в ряд
    h_stack = np.hstack([img, mask, result])
    cv2.imshow("Horizontal stack", h_stack)

    # Выход из цикла
    if cv2.waitKey(1) and 0xFF == ord('q'):
        break

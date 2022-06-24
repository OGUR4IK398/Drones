import cv2
import numpy as np
from djitellopy import Tello
import time

drone = Tello()
drone.connect()
print(drone.get_battery())
drone.streamon()


drone.takeoff()

time.sleep(2.2)

w, h = 360, 240

fb_range = [6200, 6800]
pid = [0.4, 0.2, 0]
pid_h = [0.6, 0.6, 0]
x_p_error = 0
y_p_error = 0


def find_face(img):
    face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

    # Перекодировка img в серый
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Получение всех види
    faces = face_cascade.detectMultiScale(gray_img, 1.2, 8)
    my_face_list_c = []
    my_face_list_area = []

    # Строим квадраты и центральные круги там, где лица нашел
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cx = x + w // 2
        cy = y + h // 2
        area = w * h
        cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
        my_face_list_c.append([cx, cy])
        my_face_list_area.append(area)

    if len(my_face_list_c) != 0:
        # Получение самого большого (близкого) лица
        i = my_face_list_area.index(max(my_face_list_area))
        return img, [my_face_list_c[i], my_face_list_area[i]]
    else:
        return img, [[0, 0], 0]


def track_face(info, w, pid, p_error):
    area = info[1]
    x, y = info[0]
    # Скорость движения
    fb = 0
    hb = 0
    x_error = x - w // 2
    y_error = y - h // 2
    angle_speed = pid[0] * x_error + pid[1] * (x_error - x_p_error)

    ## Потенциально другой пид
    h_speed = pid_h[0] * y_error + pid_h[1] * (y_error - y_p_error)

    # Ограничения
    angle_speed = int(np.clip(angle_speed, -100, 100))
    h_speed = int(np.clip(h_speed, -100, 100))

    # Настройка движения дрона на основе площади лица
    if fb_range[0] < area < fb_range[1]:
        fb = 0
    elif area > fb_range[1]:
        fb = -20
    elif area < fb_range[0] and area != 0:
        fb = 20


    if x == 0:
        angle_speed = 0
        x_error = 0
    if y == 0:
        h_speed = 0
        y_error = 0

    drone.send_rc_control(0, fb, -h_speed, angle_speed)
    return x_error, y_error


while True:
    img = drone.get_frame_read().frame
    img = cv2.resize(img, (w, h))
    img, info = find_face(img)
    x_p_error = track_face(info, w, pid, x_p_error)[0]
    y_p_error = x_p_error = track_face(info, w, pid, x_p_error)[1]
    cv2.imshow('output', img)

    if cv2.waitKey(1) & 0xFF == ord('2'):
        drone.land()
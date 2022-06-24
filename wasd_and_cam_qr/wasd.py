from djitellopy import Tello
from time import sleep
from wasd_and_cam_qr import KeyPressModule as kp, camModule as cm
import cv2

kp.init()

drone = Tello()
drone.connect()

# Запуск стрима (камеры)
drone.streamon()

# Запуск
detector = cv2.QRCodeDetector()
print(drone.get_battery())


def get_keyboard_input():
    lr, fb, ud, yv = 0, 0, 0, 0
    speed = 60
    ang_speed = 80
    if kp.get_key('a'):
        lr = -speed
    elif kp.get_key('d'):
        lr = speed

    if kp.get_key('w'):
        fb = speed
    elif kp.get_key('s'):
        fb = -speed

    if kp.get_key('q'):
        yv = -ang_speed
    elif kp.get_key('e'):
        yv = ang_speed

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

    return [lr, fb, ud, yv]


while True:
    values = get_keyboard_input()
    drone.send_rc_control(*values)

    # Показ изображения
    img = cm.view(drone)

    # qr-код детектор
    if kp.get_key('g'):
        cm.qr_detect(img, detector)

    # Скриншот
    if kp.get_key('z'):
        cm.screen(img)

    sleep(0.05)

from djitellopy import Tello
import cv2
import time


def view(drone):
    # Получение изрбражения
    img = drone.get_frame_read().frame
    img = cv2.resize(img, (360, 240))
    cv2.imshow("Image", img)
    cv2.waitKey(1)
    return img


def qr_detect(img, detector):
    data, bbox, _ = detector.detectAndDecode(img)
    if data != '':
        file = open('urls.txt', 'a')
        file.seek(0, 2)
        file.write("\n" + str(data))
        file.close()


def screen(img):
    cv2.imwrite(f'Images/{time.time()}.jpg', img)
    time.sleep(0.3)
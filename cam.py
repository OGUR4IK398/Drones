from djitellopy import Tello
import cv2

drone = Tello()
drone.connect()
print(drone.get_battery())

# Запуск стрима (камеры)
drone.streamon()

while True:
    # Получение изрбражения
    img = drone.get_frame_read().frame
    img = cv2.resize(img, (360, 240))
    cv2.imshow("Image", img)
    cv2.waitKey(1)

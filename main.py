from djitellopy import Tello
from time import sleep

drone = Tello()
drone.connect()



drone.land()

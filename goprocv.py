from urllib.request import urlopen

import cv2
import numpy as np
from goprocam import GoProCamera
from goprocam import constants
cascPath="./haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)


class MyCamera(GoProCamera.GoPro):
    def getPassword(self):
        return '12345678'

    def _request(self, path, param="", value="", _timeout=5, _isHTTPS=False, _context=None):
        if param != "" and value == "":
            uri = "%s%s/%s/%s" % ("https://" if _isHTTPS else "http://",
                                  self.ip_addr, path, param)
        elif param != "" and value != "":
            uri = "%s%s/%s/%s/%s" % ("https://" if _isHTTPS else "http://",
                                     self.ip_addr, path, param, value)
        elif param == "" and value == "":
            uri = "%s%s/%s" % ("https://" if _isHTTPS else "http://",
                               self.ip_addr, path)
        print(uri)
        return urlopen(uri, timeout=_timeout, context=_context).read()



gpCam = MyCamera()
#gpCam.gpControlSet(constants.Stream.BIT_RATE, constants.Stream.BitRate.B2_4Mbps)
#gpCam.gpControlSet(constants.Stream.WINDOW_SIZE, constants.Stream.WindowSize.W480)
cap = cv2.VideoCapture("http://10.5.5.9:8080/live/amba.m3u8")
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    # Display the resulting frame
    cv2.imshow("GoPro OpenCV", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
cap.release()
cv2.destroyAllWindows()

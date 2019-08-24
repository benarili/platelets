import cv2
import numpy as np
import time


cap = cv2.VideoCapture('t1.avi')
frameCount = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
frameWidth = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frameHeight = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

buf = np.empty((frameCount, frameHeight, frameWidth, 3), np.dtype('uint8'))

fc = 0
ret = True
gray_array = np.ndarray(shape=(3,), dtype=int, order='F', buffer=np.array([180, 180, 180]))
red_array = np.ndarray(shape=(3,), dtype=int, order='F', buffer=np.array([246, 7, 31]))
while (fc < frameCount  and ret):
    ret, buf[fc] = cap.read()
    col_ctr = 0
    for col in buf[fc]:
        rgb_ctr = 0
        for rgb in col:
            if (rgb == gray_array).all():
                buf[fc][col_ctr][rgb_ctr] = red_array
            rgb_ctr += 1
        col_ctr += 1
    fc += 1
cap.release()

if (gray_array == buf[9][0][0]).all():
    print('yes')
else:
    print('no')
# print(np.ndarray(shape=(3,), dtype=int, order='F', buffer=np.array([180,180,180])))
print(buf[9][0][0])

cv2.namedWindow('frame 10')
cv2.imshow('frame 10', buf[9])

cv2.waitKey(0)
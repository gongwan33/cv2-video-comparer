import cv2
import numpy as np
import sys
import os

filename1 = sys.argv[1]
filename2 = sys.argv[2]

vid1 = cv2.VideoCapture(filename1)
vid2 = cv2.VideoCapture(filename2)

vw = vid1.get(cv2.CAP_PROP_FRAME_WIDTH)
vh = vid1.get(cv2.CAP_PROP_FRAME_HEIGHT)

videoBuf = []
curIndex = 0

while vid1.isOpened() and vid2.isOpened():
    if len(videoBuf) == 0:
        cv2.imshow('Frame', np.zeros((480, 320, 3), np.uint8))

    key = cv2.waitKey(-1)

    if key == 81:
        if len(videoBuf) > 0:
            if curIndex > 0:
                curIndex -= 1

            cv2.imshow('Frame', videoBuf[curIndex])

    elif key == 83:
        curIndex += 1

        if curIndex > len(videoBuf):
            suc1, frame1 = vid1.read()
            suc2, frame2 = vid2.read()

            if not suc1 or not suc2:
                break;

            frame1 = cv2.resize(frame1, (int(vw/2), int(vh/2)))
            frame2 = cv2.resize(frame2, (int(vw/2), int(vh/2)))

            frame = np.concatenate((frame1, frame2), axis = 1)

            videoBuf.append(frame)

        cv2.imshow('Frame', videoBuf[curIndex - 1])

    elif key == 27:
        break

    elif key == 115:
        if curIndex >= 0 and len(videoBuf) > 0:
            if not os.path.exists('snapshot'):
                os.mkdir('snapshot')

            fn = 'cpframes' + os.path.basename(sys.argv[1]) + '.' + str(curIndex) + '.jpg'
            cv2.imwrite('snapshot/' + fn, videoBuf[curIndex - 1])
            print(fn + " saved in current directory.")

vid1.release()
vid2.release()
cv2.destroyAllWindows()


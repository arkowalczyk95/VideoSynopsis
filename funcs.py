# Divide frame
import cv2
import numpy as np


def divide (frame, height, width, element_no):
    #frame = cv2.imread("diff.jpg")
    #height = frame.shape[0]
    #width = frame.shape[1]
    M = height // element_no
    N = width // element_no
    blocks = []
    for y in range(0, height, M):
        for x in range(0, width, N):
            #y1 = y + M
            #x1 = x + N
            block = frame[y:y + M, x:x + N]
            #cv2.rectangle(frame, (x, y), (x1, y1), (0, 255, 0))
            #cv2.imwrite("save" + str(x) + '_' + str(y)+".jpg", tiles)
            #cv2.imwrite("save000.jpg", frame)
            blocks.append(block)
    return blocks


def merge(blocks, element_no):
    rows = []
    for z in range(0,element_no):
        row = np.concatenate(blocks[(z*element_no):(z*element_no+element_no)], axis = 1)
        rows.append(row)
    out = np.concatenate(rows, axis = 0)
    #cv2.imwrite("save001.jpg", out)
    return out


def addframes(frame1, frame2):
    im1arrF = frame1.astype('uint16')
    im2arrF = frame2.astype('uint16')
    additionF = (im1arrF + im2arrF)
    addition = additionF.astype('uint8')
    return addition



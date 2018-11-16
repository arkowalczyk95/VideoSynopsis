# Divide frame
import cv2
import numpy as np
class Text:
    def __init__(self,x):
        self.__x = x

    def get_text(self):
        return self.__x

    def set_text(self, x):
        self.__x = x

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

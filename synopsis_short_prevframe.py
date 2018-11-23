import numpy as np
import cv2
from funcs import divide, merge, addframes, changeto8, changeto16
from itertools import izip_longest

vs = cv2.VideoCapture('video.mp4')
fourcc = cv2.VideoWriter_fourcc(*'h264')
width = int(vs.get(3))
height = int(vs.get(4))
fps = int(vs.get(cv2.CAP_PROP_FPS))

obj = cv2.VideoWriter('Output.mp4', fourcc, fps, (width, height))
obj2 = cv2.VideoWriter('OutputSynopsis.mp4', fourcc, fps, (width, height))
prevText = "Unoccupied"
prevFrame = None
synopsis = []
moves = []
movesLen = []
counter = 0

while True:
    ret, frame = vs.read()
    text = "Unoccupied"
    time = vs.get(cv2.CAP_PROP_POS_MSEC) / 1000

    if frame is None:
        break

    if counter == 0:
        (x, y, w, h) = cv2.selectROI("ROI", frame)
        counter = 1
    frame = cv2.rectangle(frame, (x + w, y + h), (x, y), (0, 0, 0), -1)

    #divide(obj, frame, height, width)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    if prevFrame is None:
        prevFrame = gray
        #prevColFrame = frame
        continue

    diff = cv2.absdiff(prevFrame, gray)
    thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]

    thresh = cv2.dilate(thresh, None, iterations=2)
    cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[1]

    for c in cnts:
        # if cv2.contourArea(c) < 10:
        #     continue
        text = "Occupied"

    cv2.putText(frame, "Status: {}".format(text), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    # cv2.putText(frame, "Time: {}".format(time), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    # cv2.imshow("Original", frame)
    # cv2.imshow("Threshold", thresh)
    # cv2.imshow("Absdiff", diff)

    if text == "Occupied":
        obj.write(frame)
        synopsis.append(frame)
    elif text == "Unoccupied" and prevText == "Occupied":
        moves.append(synopsis)
        synopsis = []
    prevText = text
    prevFrame = gray
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

print len(moves)
# # for frame in moves[0]:
# #     obj.write(frame)
for move in moves:
    movesLen.append(len(move))
print movesLen
maxMovesLen = max(movesLen)

for i in range(0, len(moves)):
    for l in range(0, len(moves[i])):
        moves[i][l] = changeto16(moves[i][l])
one = moves[0]
for i in range(1, len(moves)):
    one = [sum(x) for x in izip_longest(one, moves[i], fillvalue=0)]
    if i == (len(moves) - 1):
        for m in one:
            m = m // len(moves)
            m = changeto8(m)
            obj2.write(m)

obj.release()
vs.release()
cv2.destroyAllWindows()

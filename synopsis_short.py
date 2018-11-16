import numpy as np
import cv2
from divide import divide, merge, Text

vs = cv2.VideoCapture('Video1.mp4')
fourcc = cv2.VideoWriter_fourcc(*'h264')
width = int(vs.get(3))
height = int(vs.get(4))
fps = int(vs.get(cv2.CAP_PROP_FPS))

obj = cv2.VideoWriter('Output.mp4', fourcc, fps, (width, height))
#obj2 = cv2.VideoWriter('OutputSynopsis.mp4', fourcc, fps, (width, height))
prevText = "Unoccupied"
firstFrame = None
synopsis = []
moves = []
movesLen = []

while True:
    ret, frame = vs.read()
    text = "Unoccupied"

    if frame is None:
        break
    #divide(obj, frame, height, width)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    if firstFrame is None:
        firstFrame = gray
        firstColFrame = frame
        continue

    diff = cv2.absdiff(firstFrame, gray)
    thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]

    thresh = cv2.dilate(thresh, None, iterations=2)
    cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[1]

    for c in cnts:
        if cv2.contourArea(c) < 500:
            continue
        text = "Occupied"

    # cv2.putText(frame, "Status: {}".format(text), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    # cv2.imshow("Original", frame)
    # cv2.imshow("Threshold", thresh)
    # cv2.imshow("Absdiff", diff)

    if text == "Occupied":
        #obj.write(frame)
        synopsis.append(frame)
    elif text == "Unoccupied" and prevText == "Occupied":
        moves.append(synopsis)
        synopsis = []
    prevText = text

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

print len(moves)
print len(moves[0])
print len(moves[1])
print len(moves[2])
print len(moves[3])
# for frame in moves[0]:
#     obj.write(frame)
for move in moves:
    movesLen.append(len(move))
print movesLen
maxMovesLen = max(movesLen)
for move in moves:
    while len(move) < maxMovesLen:
        move.append(firstColFrame)
movesLen =[]
for move in moves:
    movesLen.append(len(move))
print movesLen

one = moves[0]
two = moves[1]
three = moves[2]
four = moves[3]
for i in range(0,maxMovesLen):
    outp1 = np.add(one[i], two[i])
    outp2 = np.add(three[i], four[i])
    outp = np.add(outp1, outp2)
    outp = outp // 4
    obj.write(outp)
#print synMoves

obj.release()
vs.release()
cv2.destroyAllWindows()

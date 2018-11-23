import numpy as np
import cv2
from funcs import divide, merge, addframes, changeto8, changeto16
from itertools import izip_longest

vs = cv2.VideoCapture('Video1.mp4')
fourcc = cv2.VideoWriter_fourcc(*'h264')
width = int(vs.get(3))
height = int(vs.get(4))
fps = int(vs.get(cv2.CAP_PROP_FPS))

obj = cv2.VideoWriter('Output.mp4', fourcc, fps, (width, height))
obj2 = cv2.VideoWriter('OutputSynopsis.mp4', fourcc, fps, (width, height))
prevText = "Unoccupied"
firstFrame = None
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

    cv2.putText(frame, "Status: {}".format(text), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(frame, "Time: {}".format(time), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

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

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

print len(moves)
# for frame in moves[0]:
#     obj.write(frame)
for move in moves:
    movesLen.append(len(move))
print movesLen
maxMovesLen = max(movesLen)

# wypelnianie tlem

# for move in moves:
#     while len(move) < maxMovesLen:
#         move.append(firstColFrame)


# one = moves[0]
# two = moves[1]
# three = moves[2]
# four = moves[3]
# for i in range(0, maxMovesLen):
#     outp1 = addframes(one[i], two[i])
#     outp2 = addframes(three[i], four[i])
#     outp = addframes(outp1, outp2)
#     obj2.write(outp)

# for i in range(0, len(moves)):
#     for l in range (0, maxMovesLen):
#         if i == 0:
#             continue
#         # elif i == 1:
#         #     outp1 = addframes(moves[i-1][l], moves[i][l])
#         #     outp = outp1
#         #     obj2.write(outp)
#         else:
#             # outp1 = addframes(outp1, moves[i][l])
#             # outp = outp1
#             # obj2.write(outp)


# for i in range(0, maxMovesLen):
#     one[i] = changeto16(one[i])
#     two[i] = changeto16(two[i])
#     three[i] = changeto16(three[i])
#     four[i] = changeto16(four[i])
# for i in range(0, maxMovesLen):
#     outp1 = (one[i] + two[i]) / 2
#     outp1 = changeto8(outp1)
#     obj2.write(outp1)
# outp1 = [sum(x) for x in izip_longest(one, two, three, four, fillvalue=0)]
# for i in outp1:
#     i = i // len(moves)
#     i = changeto8(i)
#     obj2.write(i)
num_block = 2
blocks = []
blocks_first = divide(firstColFrame, height, width, num_block)

for i in range(0, len(moves)):
    for l in range(0, len(moves[i])):      #maxmoveslen gdy wyrownamy or len(moves[i])
        moves[i][l] = changeto16(moves[i][l])
        blocks.append(divide(moves[i][l], height, width, num_block))
print len(blocks)
print len(blocks[0])
for i in range(0, len(blocks)):
    for l in range(0, len(blocks[i])):
        pass
# dzialanie na kawalku klatki

one = moves[0]
for i in range(1, len(moves)):
    one = [sum(x) for x in izip_longest(one, moves[i], fillvalue=0)]
    if i == (len(moves) - 1):
        for m in one:
            m = m // len(moves)             #dzielenie przez liczbe ramek aktywnych - stad wyczernianie
            m = changeto8(m)
            obj2.write(m)

obj.release()
vs.release()
cv2.destroyAllWindows()

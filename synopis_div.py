import cv2
from divide import divide, merge

vs = cv2.VideoCapture('Video1.mp4')
fourcc = cv2.VideoWriter_fourcc(*'h264')
width = int(vs.get(3))
height = int(vs.get(4))
fps = int(vs.get(cv2.CAP_PROP_FPS))
num_block = 2
obj = cv2.VideoWriter('Output.mp4', fourcc, fps, (width, height))

firstFrame = None

while True:
    ret, frame = vs.read()
    text = "Unoccupied"

    if frame is None:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)  #why

    if firstFrame is None:
        firstFrame = gray
        continue

    blocks = divide(gray, height, width, num_block)
    blocks_first = divide(firstFrame, height, width, num_block)
    for i in range (0, len(blocks)):
        text = "Unoccupied"
        diff = cv2.absdiff(blocks_first[i], blocks[i])
        thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]     #why
        thresh = cv2.dilate(thresh, None, iterations=2)
        cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[1]      #why, how it works
        for c in cnts:
            if cv2.contourArea(c) < 500:    #why
                continue
            text = "Occupied"
    cv2.putText(frame, "Status: {}".format(text), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)  #how
    #if status == 1:
    #    obj.write(frame)
    #out = merge(blocks, num_block)
    cv2.imshow("Original", frame)
    cv2.imshow("Threshold", thresh)
    cv2.imshow("Absdiff", diff)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
obj.release()
vs.release()
cv2.destroyAllWindows()

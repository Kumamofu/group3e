import cv2
import sys

#camera_id = 1
delay = 1
file_path = 'ohiza_result.mov'
window_name = file_path


cap = cv2.VideoCapture(file_path)

if not cap.isOpened():
    sys.exit()

tm = cv2.TickMeter()
tm.start()

count = 0
max_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
fps = 0

while cap.isOpened():
    ret, frame = cap.read()

    if count == max_count:
        tm.stop()
        fps = max_count / tm.getTimeSec()
        tm.reset()
        tm.start()
        #count = 0

    cv2.putText(frame, 'frame: '+str(count)+'/'+str(max_count),
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), thickness=2)

    cv2.imshow(window_name, frame)
    count += 1

    if cv2.waitKey(delay) & 0xFF == ord('q'):
        break
    if count == max_count:
        break
cv2.destroyWindow(window_name)

import cv2
from ultralytics import YOLO

model = YOLO("yolov8n.pt")

cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if not ret: break

    results = model.predict(source=frame, conf=0.25, device="cuda")
    for r in results:
        for box in r.boxes:
            x1,y1,x2,y2 = map(int, box.xyxy[0])
            cls_id = int(box.cls[0])
            score = box.conf[0]
            cx, cy = (x1+x2)//2, (y1+y2)//2

            name = model.names[cls_id]
            cv2.rectangle(frame, (x1,y1),(x2,y2),(0,255,0),2)
            cv2.circle(frame,(cx,cy),5,(0,0,255),-1)
            cv2.putText(frame, f"{name} {score:.2f}", (x1,y1-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0),2)

    cv2.imshow("Field Weed Detector", frame)
    if cv2.waitKey(1)==27: break

cap.release()
cv2.destroyAllWindows()

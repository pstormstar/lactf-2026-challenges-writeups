import cv2
import csv

def track_two_objects(video_path):
    cap = cv2.VideoCapture(video_path)
    
    tracker1 = cv2.TrackerCSRT.create()
    tracker2 = cv2.TrackerCSRT.create()
    
    ret, frame = cap.read()

    roi1 = cv2.selectROI("Select Objects", frame, fromCenter=False, showCrosshair=True)
    roi2 = cv2.selectROI("Select Objects", frame, fromCenter=False, showCrosshair=True)
    cv2.destroyWindow("Select Objects")

    tracker1.init(frame, roi1)
    tracker2.init(frame, roi2)

    with open("results.csv", mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Frame", "Obj1_X", "Obj2_X"])

        frame_count = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            frame_count += 1
            success1, bbox1 = tracker1.update(frame)
            success2, bbox2 = tracker2.update(frame)

            cx1, cx2 = "X", "X"

            if success1:
                x, y, w, h = [int(v) for v in bbox1]
                cx1 = int(x + (w / 2))
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, "Obj 1", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            if success2:
                x, y, w, h = [int(v) for v in bbox2]
                cx2 = int(x + (w / 2))
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.putText(frame, "Obj 2", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

            writer.writerow([frame_count, cx1, cx2])

            cv2.imshow("Multi-Object Tracking", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    track_two_objects('3d.mov')
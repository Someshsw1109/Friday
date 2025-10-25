import time
import cv2
import os
from pathlib import Path

def AuthenticateFace():
    try:
        flag = 0
        
        # base_path = Path("backend/auth")
        base_path = Path(__file__).resolve().parent
        trainer_path = base_path / "trainer" / "trainer.yml"
        cascade_path = base_path / "haarcascade_frontalface_default.xml"
        
        if not trainer_path.exists():
            print(f"Error: Trainer file not found at {trainer_path}")
            print("Please run the sample.py and trainer.py scripts first to create face samples and train the model.")
            return 0
        
        if not cascade_path.exists():
            print(f"Error: Cascade classifier not found at {cascade_path}")
            return 0
        
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read(str(trainer_path))
        
        faceCascade = cv2.CascadeClassifier(str(cascade_path))
        font = cv2.FONT_HERSHEY_SIMPLEX
        id = 2
        names = ['', '', 'Somesh']
        
        try:
            cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            if not cam.isOpened():
                print("Error: Cannot access webcam")
                return 0
            
            cam.set(3, 640)
            cam.set(4, 480)
            minW = 0.1 * cam.get(3)
            minH = 0.1 * cam.get(4)
            
            while True:
                ret, img = cam.read()
                if not ret:
                    print("Error: Failed to read from camera")
                    break
                
                converted_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = faceCascade.detectMultiScale(
                    converted_image,
                    scaleFactor=1.2,
                    minNeighbors=5,
                    minSize=(int(minW), int(minH)),
                )
                
                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    id, accuracy = recognizer.predict(converted_image[y:y+h, x:x+w])
                    if accuracy < 100:
                        id = names[id] if id < len(names) else "unknown"
                        accuracy = "  {0}%".format(round(100 - accuracy))
                        flag = 1
                    else:
                        id = "unknown"
                        accuracy = "  {0}%".format(round(100 - accuracy))
                        flag = 0
                    
                    cv2.putText(img, str(id), (x+5, y-5), font, 1, (255, 255, 255), 2)
                    cv2.putText(img, str(accuracy), (x+5, y+h-5), font, 1, (255, 255, 0), 1)
                
                cv2.imshow('camera', img)
                k = cv2.waitKey(10) & 0xff
                if k == 27:
                    break
                if flag == 1:
                    break
        finally:
            cam.release()
            cv2.destroyAllWindows()
        
        return flag
    
    except Exception as e:
        print(f"Error in AuthenticateFace: {str(e)}")
        return 0
 
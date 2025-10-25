import cv2
from pathlib import Path

try:
    # base_path = Path("backend/auth")
    base_path = Path(__file__).resolve().parent
    samples_dir = base_path / "samples"
    cascade_path = base_path / "haarcascade_frontalface_default.xml"
    
    if samples_dir.exists() and not samples_dir.is_dir():
        samples_dir.unlink()
    samples_dir.mkdir(exist_ok=True, parents=True)
    
    if not cascade_path.exists():
        print(f"Error: Cascade classifier not found at {cascade_path}")
        exit(1)
    
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    
    if not cam.isOpened():
        print("Error: Cannot access webcam")
        exit(1)
    
    cam.set(3, 640)
    cam.set(4, 480)
    
    detector = cv2.CascadeClassifier(str(cascade_path))
    
    try:
        face_id = input("Enter a Numeric user ID here: ").strip()
        if not face_id.isdigit():
            print("Error: Please enter a valid numeric ID")
            exit(1)
        
        print("Taking samples, look at camera. Press ESC to stop or 100 samples will be collected...")
        count = 0
        
        while True:
            ret, img = cam.read()
            if not ret:
                print("Error: Failed to read from camera")
                break
            
            converted_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(converted_image, 1.3, 5)
            
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
                count += 1
                
                sample_file = samples_dir / f"face.{face_id}.{count}.jpg"
                cv2.imwrite(str(sample_file), converted_image[y:y+h, x:x+w])
                
                cv2.imshow('image', img)
            
            k = cv2.waitKey(100) & 0xff
            if k == 27:
                print(f"\nStopped by user. {count} samples collected.")
                break
            elif count >= 100:
                print(f"\nCollected {count} samples.")
                break
        
        print("Samples saved successfully!")
        print(f"Total samples collected: {count}")
        if count < 30:
            print("Warning: Collected less than 30 samples. More samples improve accuracy.")
    
    finally:
        cam.release()
        cv2.destroyAllWindows()

except Exception as e:
    print(f"Error: {str(e)}")
    exit(1)
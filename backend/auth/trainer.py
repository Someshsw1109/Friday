import cv2
import numpy as np
from PIL import Image
import os
from pathlib import Path

try:
    # base_path = Path("backend/auth")
    base_path = Path(__file__).resolve().parent
    samples_path = base_path / "samples"
    trainer_dir = base_path / "trainer"
    trainer_file = trainer_dir / "trainer.yml"
    cascade_path = base_path / "haarcascade_frontalface_default.xml"
    
    if not samples_path.exists():
        print("Error: Samples directory not found. Please run sample.py first to collect face samples.")
        exit(1)
    
    sample_count = len(list(samples_path.glob("*.jpg")))
    if sample_count == 0:
        print("Error: No face samples found in the samples directory.")
        print("Please run sample.py first to collect face samples.")
        exit(1)
    
    if not cascade_path.exists():
        print(f"Error: Cascade classifier not found at {cascade_path}")
        exit(1)
    
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    detector = cv2.CascadeClassifier(str(cascade_path))
    
    def Images_And_Labels(path):
        imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
        faceSamples = []
        ids = []
        
        for imagePath in imagePaths:
            try:
                gray_img = Image.open(imagePath).convert('L')
                img_arr = np.array(gray_img, 'uint8')
                id = int(os.path.split(imagePath)[-1].split(".")[1])
                faces = detector.detectMultiScale(img_arr)
                for (x, y, w, h) in faces:
                    faceSamples.append(img_arr[y:y+h, x:x+w])
                    ids.append(id)
            except Exception as e:
                print(f"Error processing {imagePath}: {str(e)}")
                continue
        
        return faceSamples, ids
    
    print("Training faces. It will take a few seconds. Wait ...")
    faces, ids = Images_And_Labels(str(samples_path))
    
    if len(faces) == 0:
        print("Error: No faces detected in samples. Please ensure images are clear and contain visible faces.")
        exit(1)
    
    recognizer.train(faces, np.array(ids))
    trainer_dir.mkdir(exist_ok=True)
    recognizer.write(str(trainer_file))
    print(f"Model trained successfully! Saved to {trainer_file}")
    print(f"Trained on {len(faces)} face samples from {len(set(ids))} user(s).")

except Exception as e:
    print(f"Error during training: {str(e)}")
    exit(1)
 
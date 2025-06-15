# Mengimport package yang diperlukan
import cv2, os
import numpy as np
from PIL import Image

# Membuat variabel recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create()

# Untuk detector menggunakan file haarcascade_frontalface_default.xml
detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

# Membuat fungsi getImagesWithLabels dengan parameter path
def getImagesWithLabels(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)
                  if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    faceSamples = []
    Ids = []
    for imagePath in imagePaths:
        pilImage = Image.open(imagePath).convert('L')  # ubah ke grayscale
        imageNp = np.array(pilImage, 'uint8')
        Id = int(os.path.split(imagePath)[-1].split(".")[1])
        faces = detector.detectMultiScale(imageNp)
        for (x, y, w, h) in faces:
            faceSamples.append(imageNp[y:y+h, x:x+w])
            Ids.append(Id)
    return faceSamples, Ids

# Latih data
faces, Ids = getImagesWithLabels('Dataset')
recognizer.train(faces, np.array(Ids))

# Simpan model hasil training
recognizer.save('Dataset/training.xml')

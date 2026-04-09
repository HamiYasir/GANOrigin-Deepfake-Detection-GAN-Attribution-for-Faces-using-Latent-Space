from retinaface import RetinaFace
import cv2

image_path = r"D:\VIT Projects\Sem 4 Project\Implementation\gan-attribution-app\backend\test2.jpg"   # put any face image here

img = cv2.imread(image_path)

faces = RetinaFace.detect_faces(img)

print("Faces detected:", faces)
import pyrebase
import cv2
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
import numpy as np
import math

config = {
    "apiKey": "AIzaSyAE38otRLjYxs8lh7rCTzsABj5qJ60CRdo",
    "authDomain": "ping-pong-7ac82.firebaseapp.com",
    "projectId": "ping-pong-7ac82",
    "storageBucket": "ping-pong-7ac82.appspot.com",
    "messagingSenderId": "722295549568",
    "appId": "1:722295549568:web:fd90e542cab146cf4d8065",
    "measurementId": "G-PDN25HK2TV",
    "databaseURL": "https://ping-pong-7ac82-default-rtdb.asia-southeast1.firebasedatabase.app",
}

firebase = pyrebase.initialize_app(config)

database = firebase.database()


def gesture_detect():
    cap = cv2.VideoCapture(0)
    detector = HandDetector(maxHands=1)
    classifier = Classifier("Model/keras_model.h5", "Model/labels.txt")

    offset = 25
    imgSize = 300

    labels = ["Up", "Down"]

    while True:
        success, img = cap.read()
        imgOutput = img.copy()
        hands, img = detector.findHands(img)
        if hands:
            hand = hands[0]
            x, y, w, h = hand["bbox"]

            imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255
            imgCrop = img[y - offset:y + h + offset, x - offset:x + w + offset]
            imgCropShape = imgCrop.shape

            aspectRatio = h / w
            if aspectRatio > 1:
                k = imgSize / h
                wCal = math.ceil(w * k)
                imgResize = cv2.resize(imgCrop, (wCal, imgSize))
                imgResizeShape = imgResize.shape
                wGap = math.ceil((imgSize - wCal) / 2)
                imgWhite[:, wGap:wCal + wGap] = imgResize
                prediction, index = classifier.getPrediction(imgWhite, draw=False)
                data = {"Status": str(index)}
                database.child("Motion").set(data)
                cv2.putText(imgOutput, labels[index], (x, y - 20), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 255), 2)
            cv2.rectangle(imgOutput, (x - offset, y - offset), (x + w + offset, y + h + offset), (255, 0, 255), 4)
            cv2.imshow("ImageCrop", imgCrop)
            cv2.imshow("ImageWhite", imgWhite)

        cv2.imshow("Image", imgOutput)
        cv2.waitKey(1)

gesture_detect()
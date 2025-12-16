import cv2
import numpy as np
# 1. Reading and Displaying Images

# Load an image
# image = cv2.imread("apple.jpg")

# # Resize the image and store the result
# resized_image = cv2.resize(image, (100, 100))

# # Convert to grayscale and store the result
# gray_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)

# # Display the images
# # cv2.imshow("Resized Image", resized_image)
# cv2.imshow("Grayscale Image", gray_image)

# # Wait for keypress and close
# if cv2.waitKey(0) == 27:
#     cv2.destroyAllWindows()



# 2. Drawing Shapes on Images
# import cv2
# import numpy as np

# # Create a blank image
# canvas = np.zeros((500, 500, 3), dtype="uint8")
# # canvas=cv2.imread("apple.jpg")
# # Draw a rectangle
# cv2.rectangle(canvas, (50, 50), (200, 200), (0, 255, 0), 3)

# # Draw a circle
# cv2.circle(canvas, (300, 300), 50, (255, 0, 0), -1)

# # Draw a line
# cv2.line(canvas, (100, 100), (400, 400), (0, 0, 255), 5)

# cv2.imshow("Shapes", canvas)
# if cv2.waitKey(0) == 27:
#     cv2.destroyAllWindows()
    
    
    #image Processing with OpenCV
# img = cv2.imread('output.jpg', cv2.IMREAD_GRAYSCALE)
# print(img.shape)  # Image shape
# img[50:100, 50:100] = 255  # Modify pixels to white
# cv2.imshow('Modified Image', img)
# if cv2.waitKey(0) == 27:
#     cv2.destroyAllWindows()
    
    
  #  Video Capture with OpenCV 
  
  
# import cv2
# import os

# # Create images folder if it doesn't exist
# os.makedirs("images", exist_ok=True)

# # Open webcam
# cap = cv2.VideoCapture(0)

# frame_count = 0
# while True:
#     ret, frame = cap.read()
#     if not ret:
#         break
    
#     # Save frame to images folder
#     cv2.imwrite(f"images/frame_{frame_count}.jpg", frame)
#     frame_count += 100
    
#     cv2.imshow("Webcam Feed", cv2.Canny(frame, 100, 200) )
    
#     # Press 'q' to exit
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()




# import cv2

# # Load pre-trained face detection model
# face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# # Load an image
# image = cv2.imread("face.jpg")
# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# # Detect faces
# faces = face_cascade.detectMultiScale(gray, 1.1, 4)

# # Draw rectangles around faces
# for (x, y, w, h) in faces:
#     cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 3)

# cv2.imshow("Face Detection", image)
# if cv2.waitKey(0) == 27:
#     cv2.destroyAllWindows()

import cv2

# Load the pre-trained Haar cascade classifier for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Capture video from webcam
cap = cv2.VideoCapture(0)  # 0 = Default webcam

while True:
    # Read a frame from the webcam
    ret, frame = cap.read()
    if not ret:
        break

    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the grayscale frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4, minSize=(30, 30))

    # Draw rectangles around detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)  # Green rectangle

    # Display the frame with detected faces
    cv2.imshow("Live Face Detection", frame)

    # Exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all windows
cap.release()
cv2.destroyAllWindows()
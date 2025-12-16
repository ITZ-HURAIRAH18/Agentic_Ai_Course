import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

# # # import cv2
# # # import numpy as np

# # # cap = cv2.VideoCapture(0)

# # # while True:
# # #     ret, frame = cap.read()
# # #     hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

# # #     # Define color range (blue in this case)
# # #     lower_blue = np.array([100, 150, 0])
# # #     upper_blue = np.array([140, 255, 255])

# # #     mask = cv2.inRange(hsv, lower_blue, upper_blue)

# # #     cv2.imshow("Original", frame)
# # #     cv2.imshow("Masked", mask)

# # #     if cv2.waitKey(1) & 0xFF == ord('q'):
# # #         break

# # # cap.release()
# # # cv2.destroyAllWindows()


# # # In this project, students will use color detection to draw on the screen using their fingers or a colored object (like a red pen cap).

# # # Concepts Covered
# # # ✅ Color detection
# # # ✅ Contours and shape tracking
# # # ✅ Drawing on a blank canvas

# # import cv2
# # import numpy as np

# # # Capture video from webcam
# # cap = cv2.VideoCapture(0)

# # # Define the color range for detection (e.g., Blue)
# # lower_color = np.array([100, 150, 0])  # Lower HSV boundary
# # upper_color = np.array([140, 255, 255])  # Upper HSV boundary

# # # Initialize canvas (it will be resized to match the frame size)
# # canvas = None  

# # while True:
# #     ret, frame = cap.read()
# #     if not ret:
# #         break

# #     # Convert frame to HSV color space
# #     hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

# #     # Create mask to detect the specified color
# #     mask = cv2.inRange(hsv, lower_color, upper_color)

# #     # Find contours of the detected color
# #     contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# #     # Initialize canvas after getting frame size
# #     if canvas is None:
# #         canvas = np.zeros_like(frame)  # Ensure same size & channels as frame

# #     if contours:
# #         largest_contour = max(contours, key=cv2.contourArea)
# #         if cv2.contourArea(largest_contour) > 1000:  # Minimum area threshold
# #             x, y, w, h = cv2.boundingRect(largest_contour)
# #             center = (x + w // 2, y + h // 2)

# #             # Draw on canvas
# #             cv2.circle(canvas, center, 5, (255, 0, 0), -1)  # Blue dot

# #     # Merge canvas with frame
# #     blended = cv2.addWeighted(frame, 0.7, canvas, 0.3, 0)

# #     # Display the result
# #     cv2.imshow("Virtual Painter", blended)
# #     cv2.imshow("Mask", mask)  # Show the color mask

# #     # Exit if 'q' is pressed
# #     if cv2.waitKey(1) & 0xFF == ord('q'):
# #         break

# # cap.release()
# # cv2.destroyAllWindows()


# # . Real-Time Motion Detection System
# # A security-style project that detects motion and highlights moving objects. This is useful for surveillance and security applications.

# # Concepts Covered
# # ✅ Background subtraction
# # ✅ Contour detection
# # ✅ Motion detection

# import cv2

# # Initialize webcam
# cap = cv2.VideoCapture(0)

# # Background subtractor
# fgbg = cv2.createBackgroundSubtractorMOG2()

# while True:
#     ret, frame = cap.read()
#     if not ret:
#         break

#     # Apply background subtraction
#     fgmask = fgbg.apply(frame)

#     # Find contours of moving objects
#     contours, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#     for contour in contours:
#         if cv2.contourArea(contour) > 1000:  # Ignore small movements
#             x, y, w, h = cv2.boundingRect(contour)
#             cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

#     cv2.imshow("Motion Detection", frame)
#     cv2.imshow("Mask", fgmask)

#     if cv2.waitKey(30) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()



# 3. AI Face Mask Detection
# A COVID-era project where students can detect whether a person is wearing a mask or not.

# Concepts Covered
# ✅ Haar cascades for face detection
# ✅ Machine learning for mask classification
# ✅ Real-time video processing
# NOTE: This section requires a pre-trained model file 'mask_detector_model.h5'
# Comment out until you have the model file
import cv2
import numpy as np
import tensorflow as tf

# Load pre-trained face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Load pre-trained mask detection model (TensorFlow/Keras)
model = tf.keras.models.load_model("mask_detector_model.h5")

# Open webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    for (x, y, w, h) in faces:
        face = frame[y:y + h, x:x + w]
        face_resized = cv2.resize(face, (100, 100)) / 255.0
        face_resized = np.expand_dims(face_resized, axis=0)

        # Predict mask/no mask
        prediction = model.predict(face_resized)[0][0]
        label = "Mask" if prediction > 0.5 else "No Mask"
        color = (0, 255, 0) if label == "Mask" else (0, 0, 255)

        # Draw rectangle and label
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
        cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

    cv2.imshow("Face Mask Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
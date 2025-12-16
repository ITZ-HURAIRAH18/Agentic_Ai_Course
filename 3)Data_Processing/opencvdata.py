import cv2
import numpy as np
# 1. Reading and Displaying Images

# Load an image
image = cv2.imread("apple.jpg")

# Resize the image and store the result
resized_image = cv2.resize(image, (100, 100))

# Display the resized image
cv2.imshow("Resized Image", resized_image)

# Wait for keypress and close
if cv2.waitKey(0) == 27:
    cv2.destroyAllWindows()
# Code to run on RPI4

import cv2
import serial
import serial.tools.list_ports
import time

# Create a cascade classifier
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Open the webcam
cap = cv2.VideoCapture(0) # RPi camera is generally at index 0

def find_arduino(baud):
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        if 'ttyACM' in p.description or 'ttyUSB' in p.description:  # typical identifier for arduinos
            return serial.Serial(p.device, baud)
    return None

arduino = find_arduino(9600)

if arduino is None:
    print("Arduino not found. Exiting.")
    exit()

while True:
    # Read frame from camera
    ret, frame = cap.read()

    if not ret:
        break

    # Convert the image to grayscale
    grayscale_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image using the haar cascade
    faces = face_cascade.detectMultiScale(
        grayscale_image,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )

    # Draw a rectangle around each face
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
        # Normalized coordinates and send to Arduino
        normalized_coordinates = (x/frame.shape[1], y/frame.shape[0])
        arduino.write(str(normalized_coordinates).encode())

    # Display the image with faces detected
    cv2.imshow('Video - Faces Detected', frame)

    # Quit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close windows
cap.release()
cv2.destroyAllWindows()
arduino.close()
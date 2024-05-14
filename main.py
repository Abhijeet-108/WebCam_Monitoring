import glob
import os

import cv2
import time
from Sender import send_email
from threading import Thread

# Open the default camera (index 0)
video = cv2.VideoCapture(0, cv2.CAP_DSHOW)
time.sleep(1)

first_frame = None
status_list = []
count = 1

def clean():
    images = glob.glob("images/*.png")
    for image in images:
        os.remove(image)

while True:
    status = 0
    # Capture frame-by-frame
    check, frame = video.read()

    # coverting the frame to gray pixel frame
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2GRAY)
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0)

    if first_frame is None:
        first_frame = gray_frame_gau

    delta_frame = cv2.absdiff(first_frame, gray_frame_gau)

    # Check if the frame is captured successfully
    if not check:
        print("Error: Could not capture frame.")
        break

    thresh_frame = cv2.threshold(delta_frame, 60, 255, cv2.THRESH_BINARY)[1]
    dil_frame = cv2.dilate(thresh_frame, None, iterations=2)
    # Display the resulting frame
    #cv2.imshow("My video", dil_frame)

    contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) < 3000:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        rectangle = cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 3)
        if rectangle.any():
            status = 1
            cv2.imwrite(f"images/{count}.png", frame)
            count = count + 1
            all_images = glob.glob("images/*.png")
            index = int(len(all_images) / 2)
            image_with_object = all_images[index]

    status_list.append(status)
    status_list = status_list[-2:]

    if status_list[0] == 1 and status_list[1] == 0:
        email_thread = Thread(target=send_email, args=(image_with_object, ))
        email_thread.daemon = True
        clean_thread = Thread(target=clean)
        clean_thread.daemon = True

        email_thread.start()

    cv2.imshow("video", frame)

    # Check for 'q' key press to exit
    key = cv2.waitKey(1)
    if key == ord("q"):
        break

# Release the video capture object
video.release()

clean_thread.start()


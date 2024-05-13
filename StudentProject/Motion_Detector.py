import streamlit as st
import cv2
from datetime import datetime
import  time

st.title("Motion Detector")
start = st.button("Start Camera")

# Open the default camera (index 0)
video = cv2.VideoCapture(0, cv2.CAP_DSHOW)
time.sleep(1)

first_frame = None
status_list = []

if start:
    streamlit_image = st.image([])

    while True:
        status = 0
        check, frame = video.read()
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

        contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            if cv2.contourArea(contour) < 3000:
                continue
            x, y, w, h = cv2.boundingRect(contour)
            rectangle = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
            if rectangle.any():
                status = 1

        status_list.append(status)
        status_list = status_list[-2:]

        now = datetime.now()

        cv2.putText(img=frame, text=now.strftime("%A"), org=(30, 80),
                    fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=1,
                    color=(30, 120, 180), thickness=2, lineType=cv2.LINE_AA)
        cv2.putText(img=frame, text=now.strftime("%H:%M:%S"), org=(30, 140),
                    fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=1,
                    color=(30, 120, 180), thickness=2, lineType=cv2.LINE_AA)

        streamlit_image.image(frame)

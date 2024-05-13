import streamlit as st
import cv2

st.title("Motion Detector")
start = st.button("Start Camera")

if start:
    streamlit_image = st.image([])
    camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    while True:
        check, frame = camera.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2YCrCb)

        cv2.putText(img=frame, text="Namaste", org=(50,50),
                    fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=2,
                    color=(30,120,180), thickness=2, lineType=cv2.LINE_AA)

        streamlit_image.image(frame)
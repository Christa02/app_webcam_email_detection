import os
import cv2
import time
import glob
from threading import Thread
from emailing import send_email

original_frame = None
status_list = []
count = 1

def clean_images():
    images = glob.glob(f"images/*.png")
    for each in images:
        os.remove(each)

video = cv2.VideoCapture(0)
time.sleep(1)

while True:
    status = 0
    check, frame = video.read()
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gau_gray_frame = cv2.GaussianBlur(gray_frame, (21, 21), 0)

    if original_frame is None:
        original_frame = gau_gray_frame

    del_frame = cv2.absdiff(original_frame, gau_gray_frame)
    thresh_frame = cv2.threshold(del_frame, 60, 255, cv2.THRESH_BINARY)[1]
    dil_frame = cv2.dilate(thresh_frame, None, iterations=3)
    contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for contour in contours:
        if cv2.contourArea(contour) < 5000:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        rect_frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
        if rect_frame.any():
            status = 1
            cv2.imwrite(f"images/{count}.png", frame)
            count = count + 1
            image_file_paths = glob.glob("images/*.png")
            index = int(len(image_file_paths)/2)
            image_with_object = image_file_paths[index]

    status_list.append(status)
    status_list = status_list[-2:]
    if status_list[0] == 1 and status_list[1] == 0:
        email_thread = Thread(target=send_email, args=(image_with_object, ))
        email_thread.daemon = True
        clean_thread = Thread(target=clean_images)
        clean_thread.daemon = True

        email_thread.start()
        print('Email Sent Here................')

    cv2.imshow('My Video', frame)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break

video.release()
clean_thread.start()
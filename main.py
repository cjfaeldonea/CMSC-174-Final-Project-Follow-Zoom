from os import X_OK
from turtle import distance
import cv2
import numpy as np
import PySimpleGUI as sg


def main():

    sg.theme('Black')

    # define the window layout
    layout = [[sg.Text('Follow Face Filter', size=(40, 1), justification='center', font='Helvetica 20')],
              [sg.Image(filename='', key='image')],
              [sg.Image(filename='', key='image')],
              [sg.Button('Start', size=(10, 1), font='Helvetica 14'),
               sg.Button('Exit', size=(10, 1), font='Helvetica 14'), ]]


    # create the window and show it without the plot
    window = sg.Window('CMSC 174 - Final Project - Follow Face',
                       layout, location=(800, 400))

    # ---===--- Event LOOP Read and display frames, operate the GUI --- #
    open = False

    while True:
        event, values = window.read(timeout=20)
        if event == sg.WIN_CLOSED or event == 'Exit':
            break

        elif event == 'Start':
            open = True


        if open:
            cam = cv2.VideoCapture(0)
            width  = cam.get(3)
            height = cam.get(4)

            while True:
                _, img = cam.read(0)
                img = cv2.flip(img, 1)

                original_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                # loading the classifier
                face_cascade = cv2.CascadeClassifier(
                    cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

                # face detection
                def detect_face(gray_image, original_image, face_cascade):
                    detected_faces = face_cascade.detectMultiScale(
                        image=gray_image, scaleFactor=1.3, minNeighbors=8)
                    face = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)

                    for (x, y, w, h) in detected_faces:
                        cv2.rectangle(original_image, pt1=(x, y), pt2=(x+w, y+h), color=(255, 255, 255), thickness=2)

                        width_ratio = w/width
                        height_ratio = (h/height)


                        y_dist = min(y, height-y, 0.1*(height))
                        x_dist = min(x, width-x *width_ratio, 0.2*(width))

                        max_width = (w*3)*width_ratio
                        side = (max_width-w)/2
                        
                        right = int(x_dist)+side+w
                        left = int(x_dist) + side
                        
                        if x < w:
                            right += (w-x)

                        if (width-x) < w:
                            left += (w+x)

                        face = img[y - int(y_dist):y + int(y_dist)+h , x-int(left):x+int(right)]
                        

                    
                    imgbytes = cv2.imencode('.png', face)[1].tobytes()  # ditto
                    window['image'].update(data=imgbytes)
                    return face
                    # cv2.imshow("cropped face", face)

                    # return cv2.cvtColor(original_image, cv2.COLOR_RGB2BGR)

                # displaying the results
                cv2.namedWindow('Cam', cv2.WINDOW_NORMAL)
                cv2.resizeWindow('Cam', int(width), int(height))
                cv2.namedWindow('cropped face', cv2.WINDOW_NORMAL)
                cv2.resizeWindow('cropped face', int(width), int(height))
                detect_face(gray_image, original_image, face_cascade)
                # cv2.imshow("Cam", image_with_detections)
                k = cv2.waitKey(30)
                if k == 27:
                    break
            cv2.destroyAllWindows()
            open = False
            


main()

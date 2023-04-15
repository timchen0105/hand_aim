import cv2
import mediapipe as mp
import time
import serial

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1)
mpDraw = mp.solutions.drawing_utils

arduino = serial.Serial(port='COM11', baudrate=9600)
arduino.write_timeout = 0
arduino.timeout = 0

pTime = 0
cTime = 0

sensitivity = 0.8

def pos_to_aim(pos):
    res = pos * sensitivity
    res = int(res)
    return res


while True:
    ret, img = cap.read()
    if ret:
        img = cv2.flip(img, 1)
        landmarks = [[0, 0, 0] for i in range(22)]
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        result = hands.process(imgRGB)

        imgHeight = img.shape[0]
        imgWidth = img.shape[1]

        aimX = 0
        aimY = 0

        point0 = [0,0,0]
        point4 = [0,0,0]
        point8 = [0,0,0]

        vector1 = [0,0,0]
        vector2 = [0,0,0]

        vector_dot = 0

        isFire = 0

        if result.multi_hand_landmarks:
            for handLms in result.multi_hand_landmarks:
                # mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
                for i, lm in enumerate(handLms.landmark):
                    xPos = int(lm.x*imgWidth)
                    yPos = int(lm.y*imgHeight)
                    zPos = int(lm.z*100)
                    # cv2.putText(img, str(i), (xPos-25, yPos-5), cv2.FONT_HERSHEY_COMPLEX, 0.4, (0, 0, 255), 2)
                    if i == 0:
                        point0 = [xPos, yPos, zPos]
                    elif i == 4:
                        point4 = [xPos, yPos, zPos]
                    elif i == 8:
                        aimX = pos_to_aim(xPos - 320)
                        aimY = pos_to_aim(yPos - 240)
                        point8 = [xPos, yPos, zPos]
                        cv2.circle(img, (xPos, yPos), 10, (0, 0, 255), cv2.FILLED)

            vector1[0] = point4[0] - point0[0]
            vector1[1] = point4[1] - point0[1]
            vector1[2] = point4[2] - point0[2]

            vector2[0] = point8[0] - point0[0]
            vector2[1] = point8[1] - point0[1]
            vector2[2] = point8[2] - point0[2]
            
            vector_dot = vector1[0] * vector2[0] + vector1[1] * vector2[1] + vector1[2] * vector2[2]

            if vector_dot > 0:
                isFire = 1

        else:
            aimX = 0
            aimY = 0

            isFire = 0

        cTime = time.time()
        fps = 1/(cTime - pTime)
        pTime = cTime

        isFire = 0

        cv2.putText(img, f"FPS : {int(fps)}", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
        cv2.putText(img, f"aim : {int(aimX)}, {int(aimY)}", (30, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
        
        arduino.write(bytes(str(aimX), encoding='utf-8'))
        arduino.write(bytes(',', encoding='utf-8'))
        arduino.write(bytes(str(aimY), encoding='utf-8'))
        arduino.write(bytes(',', encoding='utf-8'))
        arduino.write(bytes(str(isFire), encoding='utf-8'))
        arduino.write(bytes('\n', encoding='utf-8'))
        
        cv2.imshow('img', img)
        

    if cv2.waitKey(1) == ord('q'):
        break

arduino.close()
    
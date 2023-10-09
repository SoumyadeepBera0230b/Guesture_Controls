import cv2
import mediapipe as mp

import time
from directkeys import right_pressed, left_pressed, up_pressed, down_pressed
from directkeys import PressKey, ReleaseKey

time.sleep(2)
current_key_pressed = set()

mp_draw = mp.solutions.drawing_utils
mp_hand = mp.solutions.hands
hands = mp_hand.Hands()

video = cv2.VideoCapture(0)

tipIds = [4, 8, 12, 16, 20]

while True:
    keyPressed = False
    left_side_pressed = False
    right_side_pressed = False
    up_side_pressed = False
    down_side_pressed = False
    key_count = 0
    key_pressed = 0
    ret, image = video.read()
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False

    results = hands.process(image)

    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    lmList = []
    if results.multi_hand_landmarks:
        for hand_landmark in results.multi_hand_landmarks:
            for id, lm in enumerate(results.multi_hand_landmarks[0].landmark):
                h, w, c = image.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
                # print(lmList)
            mp_draw.draw_landmarks(image, hand_landmark,
                                   mp_hand.HAND_CONNECTIONS)

    fingers = []
    if len(lmList) != 0:
        if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        for i in range(1, 5):
            if lmList[tipIds[i]][2] < lmList[tipIds[i] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        total = fingers.count(1)
        # print(total)

        if total == 4:
            print("Closed")
            cv2.rectangle(image, (20, 300), (270, 425),
                          (182, 33, 45), cv2.FILLED)
            cv2.putText(
                image,
                "STOP",
                (45, 375),
                cv2.FONT_HERSHEY_SIMPLEX,
                2,
                (255, 255, 255),
                5,
            )
            PressKey(left_pressed)
            left_side_pressed = True
            current_key_pressed.add(left_pressed)
            key_pressed = left_pressed
            keyPressed = True
            key_count = key_count + 1

        elif total == 1:
            print("Up")
            cv2.rectangle(image, (20, 300), (270, 425),
                          (23, 127, 117), cv2.FILLED)
            cv2.putText(
                image,
                "Up",
                (45, 375),
                cv2.FONT_HERSHEY_SIMPLEX,
                2,
                (255, 255, 255),
                5,
            )
            PressKey(up_pressed)
            key_pressed = up_pressed
            up_side_pressed = True
            keyPressed = True
            current_key_pressed.add(up_pressed)
            key_count = key_count + 1

        elif total == 3:
            print("Down")
            cv2.rectangle(image, (20, 300), (270, 425),
                          (23, 127, 117), cv2.FILLED)
            cv2.putText(
                image,
                "Down",
                (45, 375),
                cv2.FONT_HERSHEY_SIMPLEX,
                2,
                (255, 255, 255),
                5,
            )
            PressKey(down_pressed)
            key_pressed = down_pressed
            down_side_pressed = True
            keyPressed = True
            current_key_pressed.add(down_pressed)
            key_count = key_count + 1

        elif total == 2:
            print("Opened")
            cv2.rectangle(image, (20, 300), (270, 425),
                          (23, 127, 117), cv2.FILLED)
            cv2.putText(
                image,
                "MOVE",
                (45, 375),
                cv2.FONT_HERSHEY_SIMPLEX,
                2,
                (255, 255, 255),
                5,
            )
            PressKey(right_pressed)
            key_pressed = right_pressed
            right_side_pressed = True
            keyPressed = True
            current_key_pressed.add(right_pressed)
            key_count = key_count + 1

    if not keyPressed and len(current_key_pressed) != 0:
        for key in current_key_pressed:
            ReleaseKey(key)
        current_key_pressed = set()
    elif key_count == 1 and len(current_key_pressed) == 2:
        for key in current_key_pressed:
            if key_pressed != key:
                ReleaseKey(key)
        current_key_pressed = set()
        for key in current_key_pressed:
            ReleaseKey(key)
        current_key_pressed = set()

        # if lmList[8][2] < lmList[6][2]:
        #     print("Open")
        # else:
        #     print("Close")

    cv2.imshow("Frame", image)
    cv2.waitKey(1)

print("Terminating")

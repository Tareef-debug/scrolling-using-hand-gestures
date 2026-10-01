import cv2
import mediapipe as mp
import pyautogui
import time
mp_hands=mp.solutions.hands
hands=mp_hands.Hands(max_num_hands=1)
mp_draw=mp.solutions.drawing_utils
cam=cv2.VideoCapture(0)
prev_y=None 
while True:
    success,frame=cam.read()
    if not success:
        print("Error : could not use cam")
        break
    frame=cv2.flip(frame,1)
    rgb=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    result=hands.process(rgb)
    if result.multi_hand_landmarks:
        hand=result.multi_hand_landmarks[0]
        mp_draw.draw_landmarks(frame,hand,mp_hands.HAND_CONNECTIONS)
        finger=hand.landmark[8]
        h,w,_=frame.shape
        y=int(finger.y*h)
        if prev_y is not None:
            movement=y-prev_y
            if movement>8:
                pyautogui.scroll(-25)
            elif movement<-8:
                pyautogui.scroll(25)
        prev_y=y
    else:
        prev_y=None
    cv2.imshow("Scrolling using gestures",frame)
    cv2.waitKey(1)
cam.release()
cv2.destroyAllWindows()
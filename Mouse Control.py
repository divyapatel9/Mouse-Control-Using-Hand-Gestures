import cv2
import mediapipe
import pyautogui
import time

camera_input = cv2.VideoCapture(0)
detect_hands = mediapipe.solutions.hands.Hands()
drawing_option = mediapipe.solutions.drawing_utils
screen_w, screen_h = pyautogui.size()
x1_left = y1_left = x2_left = y2_left = 0
x1_right = y1_right = x2_right = y2_right = 0
click_counter = 0

while True:
    _, input_image = camera_input.read()
    input_image = cv2.flip(input_image, 1)  # To make the video capture act as mirror
    input_image_height, input_image_width, _ = input_image.shape
    rgb_input_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2RGB)  # Converting to RGB image
    output_hands = detect_hands.process(rgb_input_image)
    hand_landmarks = output_hands.multi_hand_landmarks
    
    if hand_landmarks:
        for hand in hand_landmarks:
            for id, lm in enumerate(hand.landmark):
                x = int(lm.x * input_image_width)
                y = int(lm.y * input_image_height)
                if id == 8:  # id for tip of first finger (index finger)
                    mouse_x = int(screen_w / input_image_width * x)
                    mouse_y = int(screen_h / input_image_height * y)
                    if hand == hand_landmarks[0]:  # Left hand
                        x1_left = x
                        y1_left = y
                        cv2.circle(input_image,(x,y),10,(0,255,0))
                        pyautogui.moveTo(mouse_x,mouse_y)
                    else:  # Right hand
                        x1_right = x
                        y1_right = y
                        cv2.circle(input_image,(x,y),10,(0,255,0))
                elif id == 4:  # id for tip of thumb finger
                    if hand == hand_landmarks[0]:  # Left hand
                        x2_left = x
                        y2_left = y
                        cv2.circle(input_image,(x,y),10,(0,255,0))
                    else:  # Right hand
                        x2_right = x
                        y2_right = y
                        cv2.circle(input_image,(x,y),10,(0,255,0))

        dist_index_diff = abs(y1_left - y1_right)
        dist_thumb_index_left = abs(y2_left - y1_left)

        # Perform mouse click if thumb and index finger of left hand are close together
        if dist_thumb_index_left < 23:
            pyautogui.click()
            click_counter+=1
            if click_counter>=2: # Perform double click if clicked two times
                pyautogui.doubleClick()

        # Draw landmarks and hand markings on the input image
        for hand in hand_landmarks:
            drawing_option.draw_landmarks(input_image, hand)

        # Adjust volume based on the difference in the distance between both hands' index fingers
        if len(hand_landmarks) >= 2:  # Ensure detection of at least two hands
            if dist_index_diff < 18:
                pyautogui.press("volumedown", presses=5, interval=0.1)
            elif dist_index_diff > 27:
                pyautogui.press("volumeup", presses=5, interval=0.1)

    cv2.imshow("Hand Movements Video Capture", input_image)
    key = cv2.waitKey(100)
    if key == 27:  # value of escape key
        break

camera_input.release()
cv2.destroyAllWindows()

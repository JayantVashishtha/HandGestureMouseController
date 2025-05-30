
import random
import cv2
import mediapipe as mp
import util
import pyautogui
from pynput.mouse import Button, Controller

mouse = Controller()
screen_width, screen_height = pyautogui.size()

mpHands = mp.solutions.hands
hands = mpHands.Hands(
    static_image_mode=False,
    model_complexity=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7,
    max_num_hands=1
)

def find_finger_tip(processed):
    if processed.multi_hand_landmarks:
        hand_landmarks = processed.multi_hand_landmarks[0]
        return hand_landmarks.landmark[mpHands.HandLandmark.INDEX_FINGER_TIP]
    return None

def move_mouse(index_finger_tip):
    if index_finger_tip:
        x = int(index_finger_tip.x * screen_width)
        y = int(index_finger_tip.y * screen_height)
        pyautogui.moveTo(x, y)

def is_left_click(landmarks, dist):
    return (
        util.get_angle(landmarks[5], landmarks[6], landmarks[8]) < 50 and
        util.get_angle(landmarks[9], landmarks[10], landmarks[12]) > 90 and
        dist > 50
    )

def is_right_click(landmarks, dist):
    return (
        util.get_angle(landmarks[9], landmarks[10], landmarks[12]) < 50 and
        util.get_angle(landmarks[5], landmarks[6], landmarks[8]) > 90 and
        dist > 50
    )

def is_double_click(landmarks, dist):
    return (
        util.get_angle(landmarks[5], landmarks[6], landmarks[8]) < 50 and
        util.get_angle(landmarks[9], landmarks[10], landmarks[12]) < 50 and
        dist > 50
    )

def is_screenshot(landmarks, _):
    return (
        util.get_angle(landmarks[2], landmarks[3], landmarks[4]) > 150 and
        util.get_angle(landmarks[5], landmarks[6], landmarks[8]) > 160 and
        util.get_angle(landmarks[9], landmarks[10], landmarks[12]) > 160 and
        util.get_angle(landmarks[13], landmarks[14], landmarks[16]) > 160 and
        util.get_angle(landmarks[17], landmarks[18], landmarks[20]) > 160
    )


def detect_gestures(frame, landmarks, processed):
    if len(landmarks) >= 21:
        index_finger_tip = find_finger_tip(processed)
        thumb_index_dist = util.get_distance([landmarks[4], landmarks[5]])

        if thumb_index_dist < 50 and util.get_angle(landmarks[5], landmarks[6], landmarks[8]) > 90:
            move_mouse(index_finger_tip)

        elif is_left_click(landmarks, thumb_index_dist):
            mouse.press(Button.left)
            mouse.release(Button.left)
            cv2.putText(frame, "Left Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        elif is_right_click(landmarks, thumb_index_dist):
            mouse.press(Button.right)
            mouse.release(Button.right)
            cv2.putText(frame, "Right Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        elif is_double_click(landmarks, thumb_index_dist):
            pyautogui.doubleClick()
            cv2.putText(frame, "Double Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

        elif is_screenshot(landmarks, thumb_index_dist):
            screenshot = pyautogui.screenshot()
            label = random.randint(1, 1000)
            screenshot.save(f'my_screenshot_{label}.png')
            cv2.putText(frame, "Screenshot", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

def main():
    cap = cv2.VideoCapture(0)
    draw = mp.solutions.drawing_utils

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            processed = hands.process(frameRGB)
            landmarks = []

            if processed.multi_hand_landmarks:
                hand_landmarks = processed.multi_hand_landmarks[0]
                draw.draw_landmarks(frame, hand_landmarks, mpHands.HAND_CONNECTIONS)

                for lm in hand_landmarks.landmark:
                    landmarks.append((lm.x, lm.y))  # Only (x, y) as per util.py

            detect_gestures(frame, landmarks, processed)
            cv2.imshow('Gesture Control', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()


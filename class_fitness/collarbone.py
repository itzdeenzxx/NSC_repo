import cv2
import math
import mediapipe as mp
import time
from google.protobuf.json_format import MessageToDict

mp_hands = mp.solutions.hands
mp_pose = mp.solutions.pose
starting_time = 0
continue_time = 0
elapsed_time = 0
set_time = 1
class Colarbone_finger:
    def __init__(self):
        self.hands = mp_hands.Hands(min_detection_confidence=0.3)
        self.pose = mp_pose.Pose(min_detection_confidence=0.5)
        self.confirm_left = False
        self.confirm_right = False
        self.count = 0
        self.threshold = 0.05
        self.continue_count = 0

    def calculate_distance(self, lm1, lm2):
        return math.sqrt((lm1.x - lm2.x)**2 + (lm1.y - lm2.y)**2)

    def detect_and_coloarbone_finger_distance(self, frame):
        global starting_time , continue_time , elapsed_time , set_time
        self.confirm_left = False
        self.confirm_right = False
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results_hands = self.hands.process(rgb_frame)
        results_pose = self.pose.process(rgb_frame)
        
        if results_hands.multi_hand_landmarks and results_pose.pose_landmarks:
            for hand_landmarks_inner, handedness_inner in zip(results_hands.multi_hand_landmarks, results_hands.multi_handedness):
                label = MessageToDict(handedness_inner)['classification'][0]['label']
                for landmark in results_pose.pose_landmarks.landmark:
                    right_sh = results_pose.pose_landmarks.landmark[12]
                    left_sh = results_pose.pose_landmarks.landmark[11]
                    index_tip = hand_landmarks_inner.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                    thumb_tip = hand_landmarks_inner.landmark[mp_hands.HandLandmark.THUMB_TIP]
                    middle_tip = hand_landmarks_inner.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
                    if (right_sh.x < index_tip.x and right_sh.x < thumb_tip.x and
                        left_sh.x > index_tip.x and left_sh.x > thumb_tip.x and
                        left_sh.y > index_tip.y and middle_tip.y > thumb_tip.y
                         ):
                        self.confirm_left = True
                        self.confirm_right = True
        
        if self.confirm_left and self.confirm_right:
            # cv2.putText(frame, "success", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            if self.count == 0 :
                starting_time = time.time()
                self.count += 1
        if self.count >= 1 :
            elapsed_time = int(time.time() - starting_time) + 1
        if results_pose.pose_landmarks:
            for landmark in results_pose.pose_landmarks.landmark:
                height, width, _ = frame.shape
                cx, cy = int(landmark.x * width), int(landmark.y * height)
                cv2.circle(frame, (cx, cy), 5, (255, 0, 0), -1)
        print(elapsed_time)
        return elapsed_time
        
# Example usage
# if __name__ == "__main__":
#     detector = Hand_L_Detector()
#     cap = cv2.VideoCapture(0)

#     while cap.isOpened():
#         ret, frame = cap.read()
#         if not ret:
#             break

#         detector.detect_and_head_finger_distance(frame)

#         cv2.imshow('Hand and Torso Detection', frame)
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     cap.release()
#     cv2.destroyAllWindows()

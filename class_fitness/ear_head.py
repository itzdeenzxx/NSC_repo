import cv2
import math
import mediapipe as mp
from google.protobuf.json_format import MessageToDict

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
confirm_right = 0
confirm_left = 0
count_right = 0
count_left = 0
count_final = 0

class Head_Ear_Detector:
    def __init__(self):   
        self.mp_pose = mp.solutions.pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.threshold = 0.05
        
    def calculate_distance(self, lm1, lm2):
        return math.sqrt((lm1.x - lm2.x)**2 + (lm1.y - lm2.y)**2)

    def detect_and_head_finger_distance(self, frame , count):
            global confirm_right , confirm_left , count_right , count_left , count_final

            count_final = count

            check_count = count
            if check_count == 0 :
                count_left , count_right = 0 , 0
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            results_pose = self.mp_pose.process(rgb_frame)
            if results_pose.pose_landmarks is not None:
                mp_drawing.draw_landmarks(rgb_frame, results_pose.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                landmark_drawing_spec=mp_drawing.DrawingSpec(color=(255,255,255), thickness=2, circle_radius=1),
                                connection_drawing_spec=mp_drawing.DrawingSpec(color=(255,255,255), thickness=2, circle_radius=1))
                
                
                #เพิ่มจุด 15 16 ใช้แกน y คำนวณจากท่า
                cv2.putText(frame, str(count_final), (100, 130), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 7)

                if count_final == 10 :
                    return 10
            
                right_index_knuckle = results_pose.pose_landmarks.landmark[20]
                left_index_knuckle = results_pose.pose_landmarks.landmark[19]
                right_ear = results_pose.pose_landmarks.landmark[8]
                left_ear = results_pose.pose_landmarks.landmark[7]
                if confirm_left == 0 or confirm_right == 0 : 
                        distance1 = self.calculate_distance(right_index_knuckle, left_ear)
                        distance2 = self.calculate_distance(left_index_knuckle, right_ear)
                        if distance1 < self.threshold and distance2 < self.threshold:
                            cv2.putText(frame, "great1", (10, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                            confirm_right += 1
                            if confirm_right == 1 :
                                count_right += 1
                            confirm_left += 1
                            if confirm_left == 1 :
                                count_left += 1
                        if count_left == count_right:
                            count_final = count_left

                elif confirm_left >= 1 and confirm_right >= 1 :
                            distance1 = self.calculate_distance(right_index_knuckle, left_ear)
                            distance2 = self.calculate_distance(left_index_knuckle, right_ear)
                            if distance1 < self.threshold and distance2 < self.threshold:
                                cv2.putText(frame, "great2", (10, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                                confirm_right += 1
                                if confirm_right == 1 :
                                    count_right += 1
                                confirm_left += 1
                                if confirm_left == 1 :
                                    count_left += 1
                                    
                            if count_left == count_right and count_right % 2 == 0 and count_left % 2 == 0:
                                count_final = count_left
                                confirm_right , confirm_left = 0,0
                            
            return count_final
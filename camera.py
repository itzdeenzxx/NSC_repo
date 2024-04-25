import cv2
import numpy as np
import mediapipe as mp
import time
from PIL import ImageFont, ImageDraw, Image 
from datetime import datetime, timedelta
from class_fitness.L_pose import Hand_L_Detector
from class_fitness.thumb_pink import thumb_pinky
from class_fitness.header import Header_finger
from class_fitness.ear_head import Head_Ear_Detector

      
mp_hands = mp.solutions.hands
# set in fitness
set_of_Hand_L = 0
set_of_thumb_pinky = 0
set_of_Header = 0
set_of_Ear = 0
#var tutorail
select_player = True
pass_check = 0
video_path = "static/video/video-test3.mp4"
# var time 30sec
confirm_timer = False
timer_started = False
countdown_time = 30 # countdown
remaining_time_continue = 30 # countdown output
start_time = 30
start_stop_continue = True
pause_requested = False  
timer_paused = False  
pause_time = 0 
resume_requested = False
elapsed_time = 0
start_stop = False

class VideoCamera(object):
    def __init__(self):
        self.camera_index = 0 
        self.video = cv2.VideoCapture(self.camera_index)
        self.L_pose = Hand_L_Detector()
        self.thumb_pink = thumb_pinky()
        self.header_finger = Header_finger()
        self.ear = Head_Ear_Detector()
        self.check_count = True
        self.count_final_main = 0
        self.set_main = 1

    def __del__(self):
        self.video.release()
    
    def draw_text(self,image, text, position, font_scale=1, font_thickness=2):
        pil_im = Image.fromarray(image) 
        draw = ImageDraw.Draw(pil_im)
        font = ImageFont.truetype("static/font/Prompt-Regular.ttf", 50)  
        draw.text((50, 50), text, font=font)  
        cv2_im_processed = np.array(pil_im)
        return cv2_im_processed
    def get_frame(self):
        global set_of_Hand_L , set_of_thumb_pinky , set_of_Header
        global remaining_time_continue
        global set_main , pass_check

        remaining_time = remaining_time_continue
        ret, frame = self.video.read()
        
        if self.count_final_main < 10 and set_of_Hand_L < 3 and self.set_main == 1:
            self.count_final_main = self.L_pose.detect_and_count_finger_distance(frame,self.count_final_main)

        elif self.count_final_main >= 10 and set_of_Hand_L <= 3:
            # self.show_overlay()
            set_of_Hand_L +=1
            print(set_of_Hand_L)
            self.count_final_main = 0

        if self.count_final_main < 10 and set_of_thumb_pinky < 3 and self.set_main == 2:
            self.count_final_main = self.thumb_pink.detect_and_count_finger_distance(frame,self.count_final_main)

        elif self.count_final_main >= 10 and set_of_thumb_pinky <= 3 and set_of_Hand_L > 3:
            # self.show_overlay()
            set_of_thumb_pinky +=1
            self.count_final_main = 0
            
        if self.set_main == 3 and set_of_Header == 0:
            remaining_time_continue = self.header_finger.detect_and_head_finger_distance(frame)
            text = f"เวลา : {int(remaining_time_continue)} วินาที"
            frame = self.draw_text(frame, text, (frame.shape[1] // 2, 50))
            if remaining_time_continue == 30 :
                set_of_Header += 1
        if self.set_main == 4 and set_of_Ear < 3:
            self.count_final_main = self.ear.detect_and_head_finger_distance(frame,self.count_final_main)
            
        elif self.count_final_main >= 10 and set_of_Ear <= 3 and set_of_Header > 3:
            # self.show_overlay()
            set_of_thumb_pinky +=1
            self.count_final_main = 0
            
        ret, jpeg = cv2.imencode('.jpg', frame)

        if not ret:
            return None
        
        return jpeg.tobytes()
    
    def set_of_main(self,check):
        self.set_main = check
        self.count_final_main = 0
            
    def gen(self):
        while True:
            frame = self.get_frame()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
    
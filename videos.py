####aiworkout
import cv2
import time
import numpy as np
import poseDetector_2 as pm


score = 0
stage = None
count = 0
pose_ =str(input("Enter your exercise : "))
cap = cv2.VideoCapture('test/bench_old.mp4')
detector = pm.poseDetector()



min_ang = 0
max_ang = 0
min_ang_hip = 0
max_ang_hip = 0
angle_min = []
angle_min_hip = []
while True:

    ref, img_user = cap.read()
    #img = cv2.resize(img, (1280,720))
    img_user = detector.findPose(img_user)
    lmList = detector.findPosition(img_user , False)
    #print(lmList)
    if len(lmList) != 0:
        if pose_ == 'squat':
            try:
                squat_mins = {} #include all angles
                #shoulder to knee
                squat_mins['squat_hip_right'] = detector.findAngle(img_user, 26, 24, 23)
                squat_mins['squat_hip_left'] = detector.findAngle(img_user, 25, 23, 24)


                angle_knee = detector.findAngle(img_user ,24, 26, 28) #Knee joint angle
                angle_knee = round(angle_knee,2)

                angle_hip =detector.findAngle(img_user ,12, 24, 26)
                angle_hip = round(angle_hip,2)

                hip_angle = angle_hip
                knee_angle = angle_knee


                angle_min.append(angle_knee)
                angle_min_hip.append(angle_hip)

                #print(angle_knee)



                cv2.putText(img_user, str(angle_knee),
                            tuple(np.multiply(lmList[26][0], [1500, 800]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (145,46,46), 2, cv2.LINE_AA
                                    )

                cv2.putText(img_user, str(angle_hip),
                            tuple(np.multiply(lmList[24][0], [1500, 800]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5,(145,46,46) , 2, cv2.LINE_AA
                                    )

                    ######rep counts and display stage
                if angle_knee > 169:
                    stage = "up"
                if angle_knee <= 90 and stage =='up':
                    stage="down"
                    count +=1
                    print(count)
                    min_ang  =min(angle_min)
                    max_ang = max(angle_min)

                    min_ang_hip  =min(angle_min_hip)
                    max_ang_hip = max(angle_min_hip)

                    print(min(angle_min), " _ ", max(angle_min))
                    print(min(angle_min_hip), " _ ", max(angle_min_hip))
                    angle_min = []
                    angle_min_hip = []

            except:
                pass
            #####-------####
            cv2.rectangle(img_user, (20,20), (235,160), (57, 107, 272), -1)

            cv2.putText(img_user, "Reps : " + str(count),
                    (30,60),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
          #Knee angle:

            cv2.putText(img_user, "Stage : " + str(stage),
                    (30,100),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)



        elif pose_ == 'deadlift':

            deadlift_mins = {}

            #shoulder to ankle
            deadlift_shoulder_to_ankle_right = detector.findAngle(img_user, 12, 26, 28)
            deadlift_shoulder_to_ankle_left = detector.findAngle(img_user,  11, 25, 27)
            if int(deadlift_shoulder_to_ankle_right) <= int(deadlift_shoulder_to_ankle_left):
                deadlift_mins['shoulder_to_ankle()'] = int(deadlift_shoulder_to_ankle_right)
            else:
                deadlift_mins['shoulder_to_ankle()'] = int(deadlift_shoulder_to_ankle_left)

            #head_to_hip
            deadlift_head_to_hip_right = detector.findAngle(img_user, 8, 12, 24)
            deadlift_head_to_hip_left = detector.findAngle(img_user, 7, 11, 23)
            if int(deadlift_head_to_hip_right) <= int(deadlift_head_to_hip_left):
                deadlift_mins['head_to_hip()'] = int(deadlift_head_to_hip_right)
            else:
                deadlift_mins['head_to_hip()'] = int(deadlift_head_to_hip_left)

            #hip_to_ankle
            deadlift_hip_to_ankle_right = detector.findAngle(img_user, 24, 26, 28)
            deadlift_hip_to_ankle_left = detector.findAngle(img_user, 23, 25, 27)
            if int(deadlift_hip_to_ankle_right) <= int(deadlift_hip_to_ankle_left):
                deadlift_mins['hip_to_ankle()'] = int(deadlift_hip_to_ankle_right)
            else:
                deadlift_mins['hip_to_ankle()'] = int(deadlift_hip_to_ankle_left)

            #algorithm for deadlift
            if len(deadlift_mins) == 3:
                if deadlift_mins['hip_to_ankle()'] >= 170:
                    if deadlift_mins['head_to_hip()'] >=170:
                        #score+=100
                        #_userprint(f"score = {score}")
                        print('nice deadlift,keep your core tighten()')
                    else:
                        #score-=50
                        #print(f"score = {score}")
                        print('back straight up,tighten your abs()')
                else:
                    if deadlift_mins['shoulder_to_ankle()'] <= 170:
                        #score+=50
                        #print(f"score = {score}")
                        print('back straight up,you are half way to 100!()')
            else:
                print('Unable to detect. Sorry. ')


            if deadlift_mins['hip_to_ankle()'] > 169:
                    stage = "up"
            if deadlift_mins['hip_to_ankle()'] <= 90 and stage =='up':
                    stage="down"
                    count +=1
            print(count)
            print(deadlift_mins['hip_to_ankle()'])

            cv2.rectangle(img_user, (20,20), (235,160), (57, 107, 272), -1)

            cv2.putText(img_user, "Reps : " + str(count),
                    (30,60),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
          #Knee angle:

            cv2.putText(img_user, "Stage : " + str(stage),
                    (30,100),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)



        elif pose_ == 'bench':

            bench_mins = {}

            #arm to shoulder
            bench_arm_to_shoulder_right = detector.findAngle(img_user, 16, 14, 12)
            bench_arm_to_shoulder_left = detector.findAngle(img_user, 15, 13, 11)
            if int(bench_arm_to_shoulder_right) <= int(bench_arm_to_shoulder_left):
                bench_mins['arm_to_shoulder()'] = int(bench_arm_to_shoulder_right)
            else:
                bench_mins['arm_to_shoulder()'] = int(bench_arm_to_shoulder_left)

            #arm to hip
            bench_arm_to_hip_right = detector.findAngle(img_user, 14, 12, 24)
            bench_arm_to_hip_left = detector.findAngle(img_user, 13, 11, 23)
            if int(bench_arm_to_hip_right) <= int(bench_arm_to_hip_left):
                bench_mins['arm_to_hip()'] = int(bench_arm_to_hip_right)
            else:
                bench_mins['arm_to_hip()'] = int(bench_arm_to_hip_left)

            #shoulder to knee
            bench_shoulder_to_knee_right = detector.findAngle(img_user, 12, 24, 26)
            bench_shoulder_to_knee_left = detector.findAngle(img_user, 11, 23, 25)
            if int(bench_shoulder_to_knee_right) <= int(bench_shoulder_to_knee_left):
                bench_mins['shoulder_to_knee()'] = int(bench_shoulder_to_knee_right)
            else:
                bench_mins['shoulder_to_knee()'] = int(bench_shoulder_to_knee_left)

            #algorithm for bench
            if len(bench_mins) == 3:
                if bench_mins['arm_to_shoulder()'] >= 100:
                    if bench_mins['shoulder_to_knee()'] <=250:
                        # score+=100
                        # print(f"score = {score}")
                        print('nice bench press,keep your core tighten()')
                    else:
                        # score-=50
                        # print(f"score = {score}")
                        print('tighten your abs,try to keep waist stick to seat()')
                else:
                    if bench_mins['arm_to_hip()'] >= 200 or bench_mins['arm_to_hip()'] <=100:
                        # score+=50
                        # print(f"score = {score}")
                        print('tighten your abs,you are half way to 100!()')
            else:
                print('Unable to detect. Sorry. ')


            if bench_mins['arm_to_shoulder()'] > 169:
                    stage = "up"
            if bench_mins['arm_to_shoulder()'] <= 90 and stage =='up':
                    stage="down"
                    count +=1
                    print(count)

            cv2.rectangle(img_user, (20,20), (235,160), (57, 107, 272), -1)

            cv2.putText(img_user, "Reps : " + str(count),
                    (30,60),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
          #Knee angle:

            cv2.putText(img_user, "Stage : " + str(stage),
                    (30,100),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)


        elif pose_ == 'pushup':

            pushup_mins = {}


        elif pose_ == 'hip bridge':

            bridge_mins = {}


    cv2.imshow('image',img_user)
    cv2.waitKey(1)
    #cv2.destroyAllWindows()

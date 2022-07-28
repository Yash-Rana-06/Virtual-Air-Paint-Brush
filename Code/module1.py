import mediapipe as mp
import cv2
import time



class handD():
    def __init__(self,static_image_mode=False,max_num_hands=1,
               min_detection_confidence=0.7,
               min_tracking_confidence=0.7):


        self.mode=static_image_mode
        self.nhands=max_num_hands
        self.mind=min_detection_confidence
        self.mint=min_tracking_confidence

        # hand detection : object
        self.hand_temp = mp.solutions.hands
        self.hand = self.hand_temp.Hands(self.mode,self.nhands,self.mind,self.mint)
        self.draw = mp.solutions.drawing_utils

        self.tip=[4,8,12,16,20]

    def fhands(self,img,draw=True):
        imgrgb=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.result=self.hand.process(imgrgb)
        # if self.result.multi_hand_landmarks:
        #     for i in self.result.multi_hand_landmarks:
        #         if draw:
        #             self.draw.draw_landmarks(img, i, self.hand_temp.HAND_CONNECTIONS)
        return img
    def posLandmarks(self,img,hno=0,draw=True):
        self.lis=[]
        if self.result.multi_hand_landmarks:
            myhand=self.result.multi_hand_landmarks[hno]
            for id,lm in enumerate(myhand.landmark):
                h,w,c=img.shape
                cx,cy=int(lm.x*w),int(lm.y*h)
                self.lis.append([id,cx,cy])
                # if draw:
                #     cv2.circle(img,(cx,cy),2,(0,0,0),4,cv2.FILLED)
                    # cv2.line(img,(10,10),(cx,cy),(0,0,0),3)
                    # cv2.putText(img,'Yash',(cx,cy),cv2.FONT_HERSHEY_SIMPLEX,3,(0,255,0),3)
                # if id==4:
                #     cv2.circle(img, (cx, cy), 5, (0, 0, 255), 4, cv2.FILLED)
                # print(id,lm)
            # self.draw.draw_landmarks(img, myhand, self.hand_temp.HAND_CONNECTIONS)

        return self.lis

    def fUp(self):
        l = []
        if self.lis[self.tip[0]][1] < self.lis[self.tip[0] - 2][1]:  # Thumb
            l.append(1)
        else:
            l.append(0)
        for id in range(1, 5):
            if self.lis[self.tip[id]][2] < self.lis[self.tip[id] - 2][2]:
                l.append(1)
            else:
                l.append(0)
        return l


def main():

    video = cv2.VideoCapture(0)
    pre_time, curt_time = 0, 0
    obj_hand=handD()
    while True:
        _, img = video.read()
        img=cv2.flip(img,1)
        img=obj_hand.fhands(img)
        obj_hand.posLandmarks(img)

        curt_time = time.time()
        fps = 1 / (curt_time - pre_time)
        pre_time = curt_time

        cv2.imshow('Hand', img)
        if cv2.waitKey(2) & 0xFF == ord('q'):
            break

    video.release()
    cv2.destroyAllWindows()


if __name__=="__main__":
    main()


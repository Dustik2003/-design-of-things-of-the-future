import time

import cv2
print(cv2.__version__)
cap =cv2.VideoCapture('sample.mp4')
leftCounter=rightCounter=0
flag=None
tmpx=0
tmpy=0
counter=0
while True:
    ret,frame=cap.read()
    if not ret:
        break

    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray=cv2.GaussianBlur(gray,(21,21),0)
    ret,thresh=cv2.threshold(gray,100,255,cv2.THRESH_BINARY_INV)

    contours,hierarchy=cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

    if len(contours)>0:
        c=max(contours,key=cv2.contourArea)
        x,y,w,h=cv2.boundingRect(c)
        counter+=1
        tmpx+=x
        tmpy+=y
        if x+w//2>320:
            rightCounter+= 0 if flag else 1
            color = (255, 0, 0)
            flag=True
        else:
            leftCounter+=1 if flag else 0
            color=(0, 0, 255)
            flag=False

        cv2.circle(frame,(x+w//2,y+h//2),w//2,color,2)
        cv2.line(frame, (0,y+h//2), (640,y+h//2), color, 1)
        cv2.line(frame, (x+w//2,0), (x+w//2,480), color, 1)
        cv2.putText(frame,"x: "+str(x)+" y: "+str(y)+" w: "+str(w)+" h: "+str(h),(0,20),cv2.FONT_HERSHEY_SIMPLEX,0.8,(0, 0, 0))
        cv2.putText(frame,"left: "+str(leftCounter)+" right: "+str(rightCounter),(0,40),cv2.FONT_HERSHEY_SIMPLEX,0.8,(0, 0, 0))
        cv2.putText(frame,"Distance: "+str(((x+w//2-320)**2+(y+h//2-240)**2)**0.5),(0,60),cv2.FONT_HERSHEY_SIMPLEX,0.8,(0, 0, 0))
        cv2.putText(frame,"Area percentage: "+str(100*h*w/640/480)+" %",(0,80),cv2.FONT_HERSHEY_SIMPLEX,0.8,(0, 0, 0))

        cv2.rectangle(frame,(220,140),(420,340),(0,0,0),2)




    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break
    time.sleep(0.05)


print("x:",tmpx/counter,"y:" ,tmpy/counter)

cap.release()
cv2.destroyAllWindows()
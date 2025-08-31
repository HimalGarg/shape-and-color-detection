import argparse
import imutils
import cv2



def findCentroid(c):

    M=cv2.moments(c) #moments returns a dictionary of many characterstics of the nparray passed
    cX=int(M["m10"]/M["m00"])  #m10 is sum of all x coords which get divided by total points (m00) to get centroid's x coords
    cY=int(M["m01"]/M["m00"])  #similar
    return cX, cY


if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("-i","--image",required=True,help="path to the input image")
    args=vars(ap.parse_args())

    image=cv2.imread(args["image"])
    gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    blurred=cv2.GaussianBlur(gray,(5,5),0)
    thresh=cv2.threshold(blurred,70,255,cv2.THRESH_BINARY)[1]
    cnts=cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    cnts=imutils.grab_contours(cnts)
    for c in cnts:
        M=cv2.moments(c) #moments returns a dictionary of many characterstics of the nparray passed
        cX=int(M["m10"]/M["m00"])  #m10 is sum of all x coords which get divided by total points (m00) to get centroid's x coords
        cY=int(M["m01"]/M["m00"])  #similar
        

        cv2.drawContours(image,[c],-1,(0,255,0),2)
        cv2.circle(image,(cX,cY),7,(255,255,255),-1)
        cv2.putText(image,"centre",(cX-20,cY-20),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),2)

        cv2.imshow("Image",image)
        cv2.waitKey(0)
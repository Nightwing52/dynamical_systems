import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

#returns normalized distance between pixel and a target color; default is green
def dist(pix, tar=(0, 255, 0)):
    return ((pix[0]-tar[0])**2+(pix[1]-tar[1])**2+(pix[2]-tar[2])**2)/196608

#video capture
cap = cv.VideoCapture("out.mp4")

y = []
#loop
f = open("coord.txt", "w")
num_frames = 0
while cap.isOpened():
    #next frame
    num_frames += 1
    print(num_frames/1000.0)
    ret, frame = cap.read()
    if not ret:
        print("Exiting...")
        break

    #filtering
    gray = np.zeros((90, 160), dtype="uint8")
    cen_x = 0.0
    num_white = 0
    for i in range(90):
        for j in range(160):
            pix_dist = dist(frame[i, j])
            if pix_dist < 0.2: #turn white
                num_white += 1
                cen_x += j
                gray[i, j] = 255
            else: #turn black
                gray[i, j] = 0

    cen_x = cen_x/num_white
    y.append(cen_x)      
    f.write(str(cen_x)+" ")
    
    #display
    '''cv.imshow("frame", gray)
    if cv.waitKey(1) == ord("q"):
        break
    '''

#release
cap.release()
cv.destroyAllWindows()

#plot
plt.plot(np.linspace(0, len(y), len(y)), y)
plt.show()

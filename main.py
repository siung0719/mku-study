# importing libraries
import numpy as np
import cv2
import matplotlib.pyplot as plt
# capture frames from a camera

# frame= cv2.imread('visual/visual_servo/cross.png')
# t_val=0.7
# frame[frame<t_val*np.mean(frame)]=0
# # frame[frame>=t_val*np.mean(frame)]=255
# c_pos=np.where(frame==0)
# p_y=(c_pos[0][-1]+c_pos[0][0])//2
# p_x=(c_pos[1][-1]+c_pos[1][0])//2
# print(p_y,p_x)

cap=cv2.VideoCapture(0)
t_val=0.7
while cap.isOpen():
	_,frame=cap.read()
	frame[frame<t_val*np.mean(frame)]=0
	c_pos=np.where(frame==0)
	cv2.imshow('_',frame)
	if cv2.waitKey(1) & 0xff==27:
     	break
cap.release()
cv2.destroyAllWindows()
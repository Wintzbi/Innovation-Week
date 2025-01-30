import cv2
def point_milieu(pts1, pts2):
    xm = (pts1[0] + pts2[0]) / 2
    ym = (pts1[1] + pts2[1]) / 2
    return (int(xm), int(ym))

def dist_and_angle(detector,lmList,img,marquers,color):
    # Calculate the distance between landmarks 11 and 15 and draw it on the image
    length, img, info = detector.findDistance(lmList[marquers[0]][0:2],
                                                lmList[marquers[2]][0:2],
                                                img=img,
                                                color=color,
                                                scale=10)

    # Calculate the angle between landmarks 11, 13, and 15 and draw it on the image
    angle, img = detector.findAngle(lmList[marquers[0]][0:2],
                                    lmList[marquers[1]][0:2],
                                    lmList[marquers[2]][0:2],
                                    img=img,
                                    color=color,
                                    scale=10)
    return length,angle,img
    
def hands_up(detector,lmList,img,color):
    #Je prends l'avant bras comme repère car la taille de lenght dépend de la distance par rapport à la caméra
    Length_limit,_,_=detector.findDistance(lmList[13][0:2],
                                                lmList[15][0:2],
                                                img=None,
                                                color=color,
                                                scale=10)
    condition=False
    R_hand_marquers=[12,14,16]
    L_hand_marquers=[11,13,15]
    R_length,R_angle,img=dist_and_angle(detector,lmList,img,R_hand_marquers,color)
    L_length,L_angle,img=dist_and_angle(detector,lmList,img,L_hand_marquers,color)


    head_lenght_L,_,img=length, img, info = detector.findDistance(lmList[11][0:2],
                                                lmList[9][0:2],
                                                img=img,
                                                color=color,
                                                scale=10)
    head_lenght_R,_,img=length, img, info = detector.findDistance(lmList[12][0:2],
                                                lmList[10][0:2],
                                                img=img,
                                                color=color,
                                                scale=10)
    # Afficher la distance sur l'image
    font = cv2.FONT_HERSHEY_SIMPLEX
    ptsR=point_milieu(lmList[12][0:2], lmList[10][0:2])
    cv2.putText(img, f"Distance: {head_lenght_R:.2f} px", (ptsR[0], ptsR[1]), font, 1, (255, 0, 0), 2)
    # Afficher la distance sur l'image
    font = cv2.FONT_HERSHEY_SIMPLEX
    ptsL=point_milieu(lmList[11][0:2], lmList[9][0:2])
    cv2.putText(img, f"Distance: {head_lenght_L:.2f} px", (ptsL[0], ptsL[1]), font, 1, (255, 0, 0), 2)
    if R_angle>170 and R_angle<190:
        if L_angle>170 and L_angle<190: 
            if head_lenght_R <= head_lenght_L < 300 : condition=True
    return condition,img

from Uebung01_DetectPylons import DetectPylons
import cv2
import os
import numpy

def main():
    detect_pylons = DetectPylons()
    #directories = ["images/bottom", "images/top"]
    directories = ["images/test"]
    for directory in directories:
        for filename in os.listdir(directory):
            curr_file = str(filename)
            read_img = cv2.imread(os.path.join(directory,filename), 1)
            convert_img = cv2.GaussianBlur(read_img, (3, 3), 0)
            convert_img =  cv2.cvtColor(read_img, cv2.COLOR_BGR2HSV)

            yellow_mask = detect_pylons.createMask(convert_img, [20, 100, 100], [33, 255, 255])
            yellow_mask = cv2.erode(yellow_mask, None, iterations=2)
            yellow_mask = cv2.dilate(yellow_mask, None, iterations=4)
            red_mask_180 = detect_pylons.createMask(convert_img, [170, 120, 120], [180, 255, 255])
            red_mask_0 = detect_pylons.createMask(convert_img, [0, 30, 30], [5, 255, 255])
            blue_mask = detect_pylons.createMask(convert_img, [80, 92, 92], [125, 255, 255])
            blue_mask = cv2.erode(blue_mask, None, iterations=2)
            blue_mask = cv2.dilate(blue_mask, None, iterations=4)
            red_mask =  red_mask_180 + red_mask_0
            red_mask = cv2.erode(red_mask, None, iterations=2)
            red_mask = cv2.dilate(red_mask, None, iterations=4)

            contours_yellow, hierarchy = cv2.findContours(yellow_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            contours_red, hierarchy = cv2.findContours(red_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            contours_blue, hierarchy = cv2.findContours(blue_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

            contours = [contours_blue, contours_red, contours_yellow]

            bounding_boxes = detect_pylons.makeBoundingBoxes(contours, convert_img)
            detect_pylons.findPylon(curr_file, convert_img, bounding_boxes, contours)

            #bgr = cv2.cvtColor(convert_img, cv2.COLOR_HSV2BGR)
            #cv2.imshow("img", bgr)
            #cv2.waitKey(0)

if  __name__ =='__main__':
    main()

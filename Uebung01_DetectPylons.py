import cv2
import os
import numpy

class DetectPylons:

    def __init__(self):
        pass

    def createMask(self, image, lower_color, upper_color):
        lower_color = numpy.array(lower_color, dtype = "uint8")
        upper_color = numpy.array(upper_color, dtype = "uint8")
        mask = cv2.inRange(image, lower_color, upper_color)
        return mask

    #make sure the same pylon doesn't appear twice
    def uniquify(self, list):
        newlist = ()
        for x, y in list:
            if x not in newlist and y not in newlist:
                newlist += (x, y)
        return newlist

    #finds bounding boxes near a given bounding box
    def findNearbyContour(self, filename, image, contour, center, x, y, w, h):
        pylons = []
        x_upper = x
        y_upper = y
        top_coordinates = tuple((x_upper, y_upper))
        width_upper_contour = w
        line = ""
        details = ""
        for cont in contour:
            if cv2.pointPolygonTest(cont, (center[0], center[1] + h/1.25), False) == 1:
                x, y, w, h = cv2.boundingRect(cont)
                if w >= 15 and h >= 15 and w <= 150 and h <= 150 and width_upper_contour <= w + 20 and width_upper_contour >= w - 20:
                    cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)
                    bottom_coordinates = tuple((x + w, y + h))
                    pylons.extend((top_coordinates, bottom_coordinates))
                    return pylons


    #finds bounding boxes which are within the color thresholds
    global bounding_boxes
    bounding_boxes = []
    def makeBoundingBoxes(self, contours, image):
        for contour in contours:
            for c in contour:
                x,y,w,h = cv2.boundingRect(c)
                #only add bounding rect if width and height are >= 10 and <=150 pixels
                if w >= 15 and h >= 15 and w <= 150 and h <= 150:
                    bounding_boxes.append(tuple((x,y,w,h)))
                    cv2.rectangle(image,(x,y),(x+w,y+h),(255,255,255),2)
        return bounding_boxes

    #loops through list of bounding boxes to find pylons
    def findPylon(self, filename, image, bounding_boxes, contours):
        pylons_found = []
        print filename
        for box in bounding_boxes:
            center = (box[0] + (box[2]/2), box[1] + (box[3]/2))
            width_next_center = (center[0] + box[2], center[1])
            height_next_center = (center[0], center[1] + box[3])
            count = 0

            for cont in contours:
                for c in cont:
                    if cv2.pointPolygonTest(c, center, False) == 1: #and box != c: #exclude identical boxes
                        x,y,w,h = cv2.boundingRect(c)
                        if w >= 15 and h >= 15 and w <= 150 and h <= 150:
                            center = (x+(w/2), y+(h/2))
                            if numpy.array_equal(cont, contours[0]):
                                find_red = self.findNearbyContour(filename, image, contours[1], center, x, y, w, h)
                                if find_red:
                                    pylons_found.append(find_red)
                                    print "found blue and red pylon"
                                find_yellow = self.findNearbyContour(filename, image, contours[2], center, x, y, w, h)
                                if find_yellow:
                                    pylons_found.append(find_yellow)
                                    print "found blue and yellow pylon"

                            elif numpy.array_equal(cont, contours[1]):
                                find_blue = self.findNearbyContour(filename, image, contours[0], center, x, y, w, h)
                                if find_blue:
                                    pylons_found.append(find_blue)
                                    print "found red and blue pylon"
                                find_yellow = self.findNearbyContour(filename, image, contours[2], center, x, y, w, h)
                                if find_yellow:
                                    pylons_found.append(find_yellow)
                                    print "found red and yellow pylon"

                            elif numpy.array_equal(cont, contours[2]):
                                find_blue = self.findNearbyContour(filename, image, contours[0], center, x, y, w, h)
                                if find_blue:
                                    pylons_found.append(find_blue)
                                    print "found yellow and blue pylon"
                                find_red = self.findNearbyContour(filename, image, contours[1], center, x, y, w, h)
                                if find_red:
                                    pylons_found.append(find_red)
                                    print "found yellow and red pylon"
        if pylons_found:
            pylons_unique = self.uniquify(pylons_found)
            line = str(filename + ", " + str(len(pylons_unique)/2) + ", " + str(pylons_unique) + "\n")
            self.writeToFile(line)

    def writeToFile(self, line):
        file = open("pylons_found.txt", "a")
        file.write(str(line))
        file.close()

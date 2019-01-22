import math

import cv2
import numpy as np
import threading
from networktables import NetworkTables
'''
cond = threading.Condition()
notified = [False]

# listen for a connection to the robot
def connectionListener(connected, info):
    print(info, '; Connected=%s' % connected)
    with cond:
        notified[0] = True
        cond.notify()

NetworkTables.initialize(server='10.52.88.10')
NetworkTables.addConnectionListener(connectionListener, immediateNotify=True)

# as long as the Jetson has not connected, wait for a connection
with cond:
    print("Waiting")
    if not notified[0]:
        cond.wait()
# At this point, the jetson has connected.
print("Connected!")
'''

np.set_printoptions(threshold=np.inf)
# define the HSV threshold ranges.
hue_range = [28,85]
saturation_range = [23,255]
value_range = [96,255]

def hsv_threshold(input, hue, saturation, value):
    """Segment an image based on hue, saturation, and value ranges.
    Args:
        input: A BGR numpy.ndarray.
        hue: A list of two numbers the are the min and max hue.
        saturation: A list of two numbers the are the min and max saturation.
        value: A list of two numbers the are the min and max value.
    Returns:
        A black and white numpy.ndarray.
    """
    out = cv2.cvtColor(input, cv2.COLOR_BGR2HSV)

    # this function goes through the input numpy.ndarray (the image)
    # and separates it based on its hsv values, according to my inputs.
    # it only returns HSV points that are within the range given in parameters. Returns them as a new image.
    return cv2.inRange(out, (hue[0], saturation[0], value[0]), (hue[1], saturation[1], value[1]))


cap = cv2.VideoCapture(0)
test = True
while test:
    #test = False
    ret, bgr_img = cap.read()
    # read in the image
    #bgr_img = cv2.imread('testimages/retroreflectivetapegreen.jpg')


    # resize the image to 300x300, 0.5 interpolation if (300,300) does not work correctly
    imageResized = cv2.resize(bgr_img, (300, 300), fx=0.5, fy=0.5)

    # Gaussian blur the image.
    blurred_image = cv2.GaussianBlur(imageResized, (191, 191), 1)
    # cv2.imshow("BLURRED", blurred_image)

    # define the erosion kernel and erode the image
    # eroding eliminates inconsistencies between pixels, like small flares or bits
    kernel = np.ones((5,5),'uint8')
    erode = cv2.erode(blurred_image,kernel,iterations=1)

    # Run an HSV threshold on the image to isolate the retroreflective tape.
    thresholded_image = hsv_threshold(blurred_image,hue_range,saturation_range,value_range)
    #print(thresholded_image)


    contours, hierarchy = cv2.findContours(thresholded_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    index = -1
    thickness = 4
    color = (255, 0, 255)

    objects = np.zeros([thresholded_image.shape[0], thresholded_image.shape[1], 3],'uint8')
    for c in contours:
        # draw contours of the thresholded image one by one, do not do the inner fill of the image
        cv2.drawContours(objects,[c],-1,color,1)
        area = cv2.contourArea(c)
        perimeter = cv2.arcLength(c, True)

        M = cv2.moments(c)
        # centroid: exact middle points
        #cx = int(M['m10']/M['m00'])
        #cy = int(M['m01']/M['m00'])
        #cv2.circle(objects, (cx,cy), 4, (0,0,255),-1)

         #print("Area: {}, perimeter: {}".format(area,perimeter))
    print(contours)
    rect = cv2.minAreaRect(c)
    #get rectangle information
    # https://stackoverflow.com/questions/36293335/using-bounding-rectangle-to-get-rotation-angle-not-working-opencv-python
    center = rect[0]
    angle = rect[2]
    rot = cv2.getRotationMatrix2D(center, angle - 90, 1)
    print(angle)
    #img = cv2.warpAffine(img, rot, (rows, cols))
    #
    box = cv2.boxPoints(rect)
    points = cv2.boxPoints(rect)
    #widthOfBox = sqrt(points[0][0])

    box = np.int0(box)
    cv2.drawContours(objects, [box], 0, (0, 0, 255), 2)

    bottom_left = points[1]
    bottom_right = points[0]
    top_left = points[2]
    top_right = points[3]
    width_in_pixels = math.sqrt((bottom_left[0]-bottom_right[1])**2 + (bottom_left[1]- bottom_right[1])**2)
    print(bottom_left, bottom_right)
    print(width_in_pixels)

    # bottom right: points[0]
    cv2.circle(objects,(points[0][0],points[0][1]),20,(255,0,0),thickness=1, lineType=8, shift=0)
    # bottom left: points[1]
    cv2.circle(objects, (points[1][0], points[1][1]), 20, (255, 0, 0), thickness=1, lineType=8, shift=0)
    # top left: points[2]
    cv2.circle(objects, (points[2][0], points[2][1]), 20, (255, 0, 0), thickness=1, lineType=8, shift=0)
    #top right: points[3]
    cv2.circle(objects, (points[3][0], points[3][1]), 20, (255, 0, 0), thickness=1, lineType=8, shift=0)




     #corners = cv2.goodFeaturesToTrack(rec,4,0.01,10)

    #corners = np.int0(corners)
    #for corner in corners:
    #   x,y = corner.ravel()
    #   cv2.circle(thresholded_image,(x,y),90,30,-1)

    givenKey = cv2.waitKey(10)
     #   if givenKey == ord('x'):
     #       break

    cv2.imshow("Image",thresholded_image)
    cv2.imshow("Objects",objects)

    #cv2.imshow("Thresholded image",thresholded_image)
cap.release()
cv2.destroyAllWindows()

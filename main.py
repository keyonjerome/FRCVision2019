import cv2
import numpy as np
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


cap = cv2.VideoCapture(1)

while True:
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
    print(thresholded_image)


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

        rect = cv2.minAreaRect(c)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        cv2.drawContours(objects, [box], 0, (0, 0, 255), 2)

        cv2.imshow("Objects",objects)

        givenKey = cv2.waitKey(1)
        if givenKey == ord('x'):
            break



    #cv2.imshow("Thresholded image",thresholded_image)
cap.release()
cv2.destroyAllWindows()

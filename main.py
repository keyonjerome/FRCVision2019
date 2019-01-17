import cv2

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


# read in the image
bgr_img = cv2.imread('testimages/retroreflectivetapegreen.jpg')


# resize the image to 300x300, 0.5 interpolation if (300,300) does not work correctly
imageResized = cv2.resize(bgr_img, (300, 300), fx=0.5, fy=0.5)
# Gaussian blur the image.
blurred_image = cv2.GaussianBlur(imageResized, (191, 191), 1)
cv2.imshow("BLURRED", blurred_image)

# Run an HSV threshold on the image to isolate the retroreflective tape.
thresholded_image = hsv_threshold(blurred_image,hue_range,saturation_range,value_range)
print(thresholded_image)
cv2.imshow("Thresholded image",thresholded_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
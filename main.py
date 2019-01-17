import cv2


# read in the image
testImage = cv2.imread('testimages/retroreflectivetapenormal.jpg')

# resize the image to 300x300, 0.5 interpolation if (300,300) does not work correctly
imageResized = cv2.resize(testImage,(300,300),fx=0.5,fy=0.5)

imageBlurred = cv2.GaussianBlur(imageResized,(191,191),1)
cv2.imshow("BLURRED",imageBlurred)

cv2.waitKey(0)
cv2.destroyAllWindows()
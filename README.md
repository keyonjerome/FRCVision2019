## Keyon Jerome

# Jetson TX1 for FRC

# 2019 

**January 23, 2019**

## Overview

Program the Jetson TX1 Development Module with an OpenCV/NetworkTables Python file that
runs on startup and connects with an FRC robot. This program will take in a video stream from a
camera mounted to the Jetson and detect FRC 2019 field elements- their distance from the
robot, their co-ordinates, etc. This information will then be relayed across the robot’s network
using NetworkTables and the robot will be programmed to take in this information and position
itself based on the vision input. The Jetson has been pre-installed with the OpenCV library and
almost all other prerequisites, except for NetworkTables.

## Goals

1. **Learn OpenCV for Python: ​** Use this Lynda course ​ **​** to continue.
2. **Isolate field elements using OpenCV:​** Isolate the elements within a camera image using
    tools such as blurs, gradients, masks, RGB/HSV filters, etc. Use HSV filters primarily as
    RGB does not play as well with FRC field elements (reflective tape).
3. **Find contours of the field elements:​** Find the contours (edges) of the reflective tape.
    Documentation here​.
4. **Apply bounding rectangles:​** Use the contours to put rectangles around the reflective
    tape, further estimating their position. ​Documentation here.
5. **Identify whether the rectangle is veering left, or veering right: ​** On the FRC 2019
    shuttles and rockets, there are two rectangles surrounding each hatch for vision
    processing reasons. Identify which rectangle is in camera view; left or right, or both?
6. **Find distance from camera to reflective tape:​** Use pixel trigonometry to find the
    approximate distance from the camera to the rectangle(s).
7. **Find angles from camera to reflective tape:​** Use pixel trigonometry to find the
    approximate angle from the camera to the rectangles. Where is the camera in space?
    The left side of the shuttle? The right side?
8. **Set-up NetworkTables:​** Setup and install ​PyNetworkTables​ on the Jetson TX1.
9. **Set-up the IPs of the robot’s network:​** Assign static IPs to the robot’s network for
    communication. May need to use an additional router for the Jetson to work. Look into
    how to wire it to the robot, if this is the case.
10. **Write NetworkTables code on the :​** Setup and install ​PyNetworkTables​ on the Jetson
    TX1.
11.

## Image Isolation & Data Retrieval Plan

I have completed the required chapters of the Lynda.com course. Here are the functions I’m
going to use to try and isolate the image of the tape, as well as do the trigonometry for getting
its distance:

1. Gaussian Blur
2. Erode (1-2 iterations)
3. HSV Threshold
4. Find contours, taking only the ​ **top-level​** contours.
5. Draw rectangle around the top level contours, which should be the FRC vision target
    rectangle. Use cv2.BoundingRect and cv2.rotatedRect documentation.
6. Get data about rectangle: its area, width, and height. OpenCV has functions for this
    (ex:cv2.area I believe)

## Milestones

### 1. Finished up to Chapter 3 of the Lynda.com course

```
The rest of the course is not totally relevant to my project, as it is facial detection. The
blurring, filtering, and other image manipulation that I’ve learned thus far is huge, though.
```
### 2. Dolor sit amet

```
Lorem ipsum dolor sit amet, consectetuer adipiscing elit, sed diam nonummy nibh
euismod tincidunt ut laoreet dolore magna aliquam erat volutpat.
```
### 3. Consectetur adipiscing elit

```
Lorem ipsum dolor sit amet, consectetuer adipiscing elit, sed diam nonummy nibh
euismod tincidunt ut laoreet dolore magna aliquam erat volutpat.
```


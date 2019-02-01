## Keyon Jerome

# Jetson TX1 for FRC 2019

**January 23, 2019**

**Overview**

 Program the Jetson TX1 Development Module with an OpenCV/NetworkTables Python file that runs on startup and connects with an FRC robot. This program will take in a video stream from a camera mounted to the Jetson and detect FRC 2019 field elements- their distance from the robot, their co-ordinates, etc. This information will then be relayed across the robot&#39;s network using NetworkTables and the robot will be programmed to take in this information and position itself based on the vision input. The Jetson has been pre-installed with the OpenCV library and almost all other prerequisites, except for NetworkTables.

**Project Info:**

**View the main OpenCV file on GitHub:** [https://github.com/Keyon-Jerome/JetsonVision2019](https://github.com/Keyon-Jerome/JetsonVision2019)

**View the 2019 robot&#39;s code on GitHub (includes the roboRIO&#39;s side of the NetworkTables code):** [https://github.com/5288TheSpartans/DeepSpace2019](https://github.com/5288TheSpartans/DeepSpace2019)

**Goals**

1. **Learn OpenCV for Python:** [Use this Lynda course](https://www.lynda.com/Python-tutorials/OpenCV-Python-Developers/601786-2.html) ** ** to continue.
2. **Isolate field elements using OpenCV:** Isolate the elements within a camera image using tools such as blurs, gradients, masks, RGB/HSV filters, etc. Use HSV filters primarily as RGB does not play as well with FRC field elements (reflective tape).
3. **Find contours of the field elements:** Find the contours (edges) of the reflective tape. [Documentation here](https://docs.opencv.org/3.1.0/d4/d73/tutorial_py_contours_begin.html).
4. **Apply bounding rectangles:** Use the contours to put rectangles around the reflective tape, further estimating their position. [Documentation here.](https://docs.opencv.org/3.4.2/dd/d49/tutorial_py_contour_features.html)
5. **Identify whether the rectangle is veering left, or veering right:** On the FRC 2019 shuttles and rockets, there are two rectangles surrounding each hatch for vision processing reasons. Identify which rectangle is in camera view; left or right, or both?
6. **Find distance from camera to reflective tape:** Use pixel trigonometry to find the approximate distance from the camera to the rectangle(s).
7. **Find angles from camera to reflective tape:** Use pixel trigonometry to find the approximate angle from the camera to the rectangles. Where is the camera in space? The left side of the shuttle? The right side? **Difficult.**
8. **Set-up NetworkTables &amp; OpenCV:** Setup and install [PyNetworkTables](https://robotpy.readthedocs.io/projects/pynetworktables/en/stable/) and OpenCV on the Jetson TX1. The Jetson TX1 has a specific OpenCV4Tegra build to aid with vision processing, but it may be difficult to put onto the Jetson.
9. **Set-up the IPs of the robot&#39;s network:** Assign static IPs to the robot&#39;s network for communication. I may need to use an additional router for the Jetson to work. Look into how to wire it to the robot, if this is the case.
10. **Write NetworkTables code on the robot itself :** Add NetworkTables code to the 2018 or 2019 robot&#39;s repository.
11. **Get the Jetson&#39;s program to run on startup:** I won&#39;t be able to access the Jetson every time the robot starts up. Therefore, I need to make the Python OpenCV/NetworkTables program run immediately on startup.
12. **PID to distance :** Add NetworkTables code to the 2018 or 2019 robot&#39;s repository, and use PID to turn parallel to the target, then drive forward until the target is met, turn perpendicular to the target, and drive forward to meet it.

Image Isolation &amp; Data Retrieval Plan

I have completed the required chapters of the Lynda.com course. Here are the functions I&#39;m going to use to try and isolate the image of the tape, as well as do the trigonometry for getting its distance:

1. Gaussian Blur
2. Erode (1-3 iterations)
3. HSV Threshold
4. Find contours, taking only the **top-level** contours.
5. Draw rectangle around the top level contours, which should be the FRC vision target rectangle. Use cv2.BoundingRect and cv2.rotatedRect documentation.
6. Get data about rectangle: its area, width, and height, angle.
7. Use similar triangles and known widths and heights, and distance to calculate the focal length of the camera (F = (PxD)/W). Then, flip the equation to isolate for D. Add this to code to calculate distance to the

**Milestones**

1. Finished up to Chapter 3 of the Lynda.com course

The rest of the course is not totally relevant to my project, as it is facial detection. The blurring, filtering, and other image manipulation that I&#39;ve learned thus far is huge, though.

1. Isolated video

Used HSV thresholds, erosions, Gaussian blurs, resizing, and contour isolation to isolate for rectangles within the live video feed. The HSV values depend on the lighting environment, and thus it may need to be recalibrated at competition for the FRC field.

1. Data retrieval - Calculated focal length (and thus, distance)

Retrieved data about the detected rectangles- height, width, the angle (and thus direction it faces!), and even distance from the camera! This is done by creating a ratio between the amount of pixels and real distance.

1. Added NetworkTables to Jetson code

Added sample NetworkTables to the Jetson&#39;s code. It reports the found distance across the network.

1. Flashed the Jetson.

Flashing the Jetson via a Virtual Machine was a nightmare. The Jetpack Installer (flasher) can only be used on Ubuntu 16.04 (or later?) systems. I managed to put Ubuntu 16.04 onto an old laptop and flash it using that instead, but it took quite a while to make that switch.

Next Steps

1. Install git, pip, OpenCV and pynetworktables onto the Jetson.

There are a couple different OpenCV builds for the Jetson. The best one, OpenCV4Tegra, needs to be downloaded via Nvidia&#39;s GitHub and then manually built using Cmake. It allows for the image processing code to be greatly accelerated compared to the generic build. I tried this but the Jetson did not have enough storage to build it. I then tried to delete &quot;unused&quot; files, and this led me to needing to actually reflash the Jetson.

I need Git so that I don&#39;t have to manually edit the vision program&#39;s code on the Jetson itself. It&#39;d be much easier to do all the rough work on a laptop and then pull the code onto the Jetson when I need to update it.

I need pip on the Jetson to install OpenCV and pyNetworktables.

I need OpenCV on the Jetson for obvious reasons; the program needs it. Instead of trying to build the fancy best version of OpenCV, I should use pip and install the generic version. The Jetson is already powerful, I can worry about increasing the speed of my program later.

I need pynetworktables for networking from the roboRIO to the Jetson.

1. Get the vision program to run on startup.

1. Assign a static IP to the Jetson.

This is needed for communication between the two. The roboRIO already has a static IP, but the Jetson does not.

1. Add angle vision

Right now, distance is calculated via a linear ratio between pixels and distance. This is not useful to FRC vision as we&#39;re almost never going to be perpendicular to the target. There is a ton of documentation on doing this math; teams have done it before. [Here&#39;s a whitepaper from another team that I&#39;ll be looking into.](https://www.chiefdelphi.com/t/a-step-by-step-run-through-of-frc-vision-processing/341012)

**Mistakes &amp; Setbacks**

1. OpenCV course

The Lynda course did not use up-to-date OpenCV. The course appeared to be &quot;updated&quot;, but most example files would not run without modification to work with OpenCV 4.

1. Flashing the Jetson.

Last year, I used a virtual machine to flash the Jetson and had the same problem. Using a virtual machine, the flashing process would always freeze at different points. Sometimes, it would be [1.2034], and sometimes [5.6074]. Completely arbitrarily. The worst part was that it doesn&#39;t tell you that it&#39;s frozen or have any timeouts; you couldn&#39;t tell whether it was frozen or just taking a long time.

1. Building OpenCV for the Jetson.

 The Jetson Tegra series boards (e.g: Jetson TX1, TX2, TK2) have a specific build of OpenCV made by Nvidia to optimize it on their devices, called OpenCV4Tegra. The Jetson flasher, JetPack, installs this for you, but only the Python 2.7 version. Trying to build OpenCV4Tegra from source gave me a multitude of errors on Ubuntu. I eventually decided that it wasn&#39;t worth it, as I can&#39;t use the GPU on the Jetson with an OpenCV Python program anyways. The CPU would have still benefitted, but it was too much hassle within my time frame.

1. Storage space on the Jetson.

 I would try to fix an error by reinstalling a package and it would fail because storage was full. I would try to clone something from GitHub (e.g: OpenCV source) and it would fail due to storage being full. The Jetson TX1 only has 14GB of storage. I tried to mount an SD card, but it&#39;s difficult if the Jetson has already been flashed with a ton of libraries off JetPack. The worst part of this is that some commands would fail due to no storage but still give you an unrelated error; it would only be when you run &quot;df -h&quot; that you see there&#39;s no storage left. I now know that I&#39;ll need to build OpenCV on the SD card, and then link it to my Python environment.

1. Not properly using resources

[ChiefDelphi](http://chiefdelphi.com), the FRC Discord, and other resources [like this](https://medium.com/@christopherariagno/vision-tracking-in-frc-what-ive-learned-this-year-2bbb2e713794) should have been my first look before even thinking about vision. I laid out a very good plan, and had some mentors (i.e: Kyrel) look over it, but it still missed the most important parts.

The hardest part of my project was flashing and installing all libraries to the Jetson, but it&#39;s obviously been done before. Many other teams use the Tegra series boards since they were available on FIRST Choice.  After the first or second day I should&#39;ve reached out on ChiefDelphi, Reddit, or somewhere for help, but I waited longer. I&#39;ve been in contact with a programming lead from another team that uses the Jetson on Reddit since only two days ago.

**What I Learned**

OpenCV, Jetson Ubuntu, and more!

I&#39;m very, very happy to have learned OpenCV. I&#39;m definitely going to go back to that Lynda.com course and finish Chapter 4 so I can do cool things with facial detection. I&#39;ve also learned a lot about troubleshooting within Ubuntu, the terminal, and also using CMake to build from source.

import json
import cv2

with open('output.json') as json_file:
    data = json.load(json_file)
    # print(data)
    right_tape_world_coords = [[0,0,0],[5,1.1,0],[1.9,14.8,0],[-2.8,13.6,0],]
    camera_matrix = data['camera_matrix']
    dist = data['distortion']
    print(camera_matrix)
    print(dist)
    retval, rvec, tvec = cv2.solvePnP(right_tape_world_coords,points,camera_matrix, dist)
    # for info in data:
    #     print(info,": ", data[info])
    #     print("\n")

    (success, rotation_vector, translation_vector) = cv2.solvePnP(model_points, image_points, camera_matrix, dist_coeffs, flags=cv2.CV_ITERATIVE)
    
    # print "Rotation Vector:\n {0}".format(rotation_vector)
    # print "Translation Vector:\n {0}".format(translation_vector)
    
    
    # Project a 3D point (0, 0, 1000.0) onto the image plane.
    # We use this to draw a line sticking out of the nose
    
    
    (nose_end_point2D, jacobian) = cv2.projectPoints(np.array([(0.0, 0.0, 1000.0)]), rotation_vector, translation_vector, camera_matrix, dist_coeffs)
    
    for p in image_points:
        cv2.circle(im, (int(p[0]), int(p[1])), 3, (0,0,255), -1)
    
    
    p1 = ( int(image_points[0][0]), int(image_points[0][1]))
    p2 = ( int(nose_end_point2D[0][0][0]), int(nose_end_point2D[0][0][1]))
    
    cv2.line(im, p1, p2, (255,0,0), 2)
    
    # Display image
    cv2.imshow("Output", im)
    cv2.waitKey(0)
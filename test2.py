def compute_output_values(self, rvec, tvec):
        '''Compute the necessary output distance and angles'''

        x_r_w0 = np.matmul(RRTargetFinder2019.rot_robot, tvec) + RRTargetFinder2019.t_robot
        x = x_r_w0[0][0]
        z = x_r_w0[2][0]

        # distance in the horizontal plane between robot center and target
        distance = math.sqrt(x**2 + z**2)

        # horizontal angle between robot center line and target
        angle1 = math.atan2(x, z)

        rot, _ = cv2.Rodrigues(rvec)
        rot_inv = rot.transpose()

        # location of Robot (0,0,0) in World coordinates
        x_w_r0 = np.matmul(rot_inv, RRTargetFinder2019.camera_offset_rotated - tvec)

        angle2 = math.atan2(x_w_r0[0][0], x_w_r0[2][0])

        return distance, angle1, angle2
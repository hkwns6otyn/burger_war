# https://qiita.com/srs/items/99d1ff2207772859763c

import rospy
import cv2
import numpy as np
from sensor_msgs.msg import Image, CameraInfo
from cv_bridge import CvBridge, CvBridgeError
from burger_war.msg import CvCam


class Cv_cam():
    def __init__(self):
        rospy.init_node("cv_cam")
        rospy.on_shutdown(self.cleanup)
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("image_raw", Image, self.image_callback)
        self.cvcam_pub = rospy.Publisher('cv_cam', CvCam, queue_size=1)

    def image_callback(self, ros_image):
        try:
            frame = self.bridge.imgmsg_to_cv2(ros_image, "bgr8")
        except CvBridgeError, e:
            print e
        input_image = np.array(frame, dtype=np.uint8)

        rect_center = self.process_image(input_image, True)

        cvcam = CvCam()
        cvcam.red_center = rect_center[0]
        cvcam.green_center = rect_center[1]
        cvcam.blue_center = rect_center[2]
        self.cvcam_pub.publish(cvcam)

        print(rect_center)
        cv2.waitKey(1)

    def process_image(self, image, debug=False):

        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        lower = np.array([175, 10, 0])
        upper = np.array([179, 255, 255])
        mask_red1 = cv2.inRange(hsv, lower, upper)
        lower = np.array([0, 10, 0])
        upper = np.array([5, 255, 255])
        mask_red2 = cv2.inRange(hsv, lower, upper)
        mask_red = mask_red1 + mask_red2

        lower = np.array([55, 10, 0])
        upper = np.array([65, 255, 255])
        mask_green = cv2.inRange(hsv, lower, upper)

        lower = np.array([115, 10, 0])
        upper = np.array([125, 255, 255])
        mask_blue = cv2.inRange(hsv, lower, upper)

        # # cv2.__version__ > 2.x
        # _, contours_red, _ = cv2.findContours(mask_red, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # _, contours_green, _ = cv2.findContours(mask_green, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # _, contours_blue, _ = cv2.findContours(mask_blue, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # cv2.__version__ = 2.x
        contours_red, _ = cv2.findContours(mask_red, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours_green, _ = cv2.findContours(mask_green, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours_blue, _ = cv2.findContours(mask_blue, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # if debug:
        #     display = np.zeros(mask.shape, dtype=np.uint8)
        #     for c in contours:
        #         for elem in c:
        #             display[elem[0, 1], elem[0, 0]] = 255
        #     cv2.imshow("make contours", display)

        # make region
        rects_red = []
        rects_green = []
        rects_blue = []
        RECT_AREA_THRESHOLD = 50
        red_area_max = RECT_AREA_THRESHOLD
        green_area_max = RECT_AREA_THRESHOLD
        blue_area_max = RECT_AREA_THRESHOLD
        red_max = []
        green_max = []
        blue_max = []
        red_center = (-1, -1)
        green_center = (-1, -1)
        blue_center = (-1, -1)

        for contour in contours_red:
            approx = cv2.convexHull(contour)
            rect = cv2.boundingRect(approx)
            rects_red.append(rect)
            red_area = rect[2] * rect[3]
            if red_area > red_area_max:
                red_area_max = red_area
                red_center = (rect[0] + rect[2] / 2.0, rect[1] + rect[3] / 2.0)
                red_max = rect

        for contour in contours_green:
            approx = cv2.convexHull(contour)
            rect = cv2.boundingRect(approx)
            rects_green.append(rect)
            green_area = rect[2] * rect[3]
            if green_area > green_area_max:
                green_area_max = green_area
                green_center = (rect[0] + rect[2] / 2.0, rect[1] + rect[3] / 2.0)
                green_max = rect

        for contour in contours_blue:
            approx = cv2.convexHull(contour)
            rect = cv2.boundingRect(approx)
            rects_blue.append(rect)
            blue_area = rect[2] * rect[3]
            if blue_area > blue_area_max:
                blue_area_max = blue_area
                blue_center = (rect[0] + rect[2] / 2.0, rect[1] + rect[3] / 2.0)
                blue_max = rect

        if debug:
            display = image.copy()
            # for rect in rects_red:
            #     cv2.rectangle(display, (rect[0], rect[1]), (rect[0]+rect[2], rect[1]+rect[3]), (0, 255, 0), thickness=5)
            if red_area_max > RECT_AREA_THRESHOLD:
                cv2.rectangle(display, (red_max[0], red_max[1]), (red_max[0] + red_max[2], red_max[1] + red_max[3]), (100, 100, 255), thickness=3)
            if green_area_max > RECT_AREA_THRESHOLD:
                cv2.rectangle(display, (green_max[0], green_max[1]), (green_max[0]+green_max[2], green_max[1]+green_max[3]), (100, 255, 100), thickness=3)
            if blue_area_max > RECT_AREA_THRESHOLD:
                cv2.rectangle(display, (blue_max[0], blue_max[1]), (blue_max[0]+blue_max[2], blue_max[1]+blue_max[3]), (255, 100, 100), thickness=3)
            cv2.imshow("make region", display)

        # return rects_red
        return [red_center, green_center, blue_center]

    def cleanup(self):
        cv2.destroyAllWindows()


if __name__ == '__main__':
    Cv_cam()
    rospy.spin()

#!/usr/bin/env python3

import rospy
import cv2
import numpy as np
from cv_bridge import CvBridge
from pathlib import Path
import os
import sys
from rostopic import get_topic_type

from sensor_msgs.msg import Image, CompressedImage
from detection_msgs.msg import segmentationMask

from typing import List, Dict

from ultralytics import YOLO
from ultralytics.engine.results import Results
from ultralytics.engine.results import Boxes
from ultralytics.engine.results import Masks
from ultralytics.engine.results import Keypoints

class Yolov8Segmentation:
    def __init__(self):
        weights = rospy.get_param('~weights', 'yolov8s.pt')
        self.device = str(rospy.get_param('~device', ''))
        self.conf_threshold = rospy.get_param('~conf_threshold')

        # Initialize subscriver to Image/CompressedImage topic
        input_image_type, input_image_topic, _ = get_topic_type(rospy.get_param('~input_image_topic', '/camera/color/image_raw'), blocking = True)
        self.compressed_input = input_image_type == 'sensor_msgs/CompressedImage'

        # Initialize CV_Bridge
        self.bridge = CvBridge()

        self.yolo = YOLO(weights)

        if self.compressed_input:
            self.image_sub = rospy.Subscriber(input_image_topic, CompressedImage, self.callback, queue_size=1)
        else:
            self.image_sub = rospy.Subscriber(input_image_topic, Image, self.callback, queue_size=1)

        # Initialize prediction publisher
        self.prediction_pub = rospy.Publisher(rospy.get_param("~output_topic"), SegmentationMasks, queue_size=10)

        # Initialize image publisher
        self.publish_image = rospy.get_param('~publish_image')
        if self.publish_image:
            self.image_pub = rospy.Publisher(rospy.get_param("~output_image_topic"), Image, queue_size=10)
        
        self.latest_image = None
        self.done_image = None

    def callback(self, data):
        self.latest_image = data

    def prediction(self, data):
        if self.compressed_input:
            im = self.bridge.compressed_imgmsg_to_cv2(data, desired_encoding='bgr8')
        else:
            im = self.bridge.imgmsg_to_cv2(data, desired_encoding='bgr8')

        results = self.yolo.predict(
            source = im,
            device = self.device,
            show = False,
            conf = self.conf_threshold
        )

        self.done_image = data

        results: Results = results[0].cpu()
        plots = results.plot()

        self.image_pub.publish(self.bridge.cv2_to_imgmsg(plots, encoding='bgr8'))



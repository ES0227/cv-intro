import lane_detection_code
import cv2
import matplotlib.pyplot as plt

def closest_lane(lanes):
    max_thickness = 0
    for detected_lane in lanes:
        thickness = abs(detected_lane[0][0] - detected_lane[0][1])
        if max_thickness < thickness:
            max_thickness = thickness
            center_lane = detected_lane

    return center_lane




def get_lane_center(lanes):
    center_lane = closest_lane(lanes)

    center_intercept = (center_lane[0][0] + center_lane[0][1]) / 2
    x1, y1, x2, y2 = center_lane[0]
    slope1 = (y2-y1)/(x2-x1)
    x1, y1, x2, y2 = center_lane[1]
    slope2 = (y2-y1) / (x2-x1)

    center_slope = (slope1 + slope2) / 2

    return center_intercept, center_slope


def recommend_direction (center, slope):
    image_midline = 3824/2
    if center == image_midline:
        movement = "forward"  
    elif center < image_midline:
        movement = "left"
    else:
        movement = "right"
    
    return movement

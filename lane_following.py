import lane_detection_code
import cv2
import matplotlib.pyplot as plt

def closest_lane(lanes):
    min_distFromCenter = float(40000)
    center_lane = None
    #max_thickness = 0
    
    for detected_lane in lanes: #get the average of the x intercepts of the lines making up a lane and then compare them  to see which one is closest to half the resolution
        lane_center = abs(detected_lane[0][0] + detected_lane[1][0])/2 #FIX THIS!!!!!!!!!!
        print(detected_lane[0][0])
        distFromCenter = abs(2138-lane_center)
        if distFromCenter < min_distFromCenter:
            min_distFromCenter = distFromCenter
            center_lane = detected_lane
    
        # if max_thickness < thickness:
        #     max_thickness = thickness
        #     center_lane = detected_lane

    return center_lane

def get_lane_center(lanes):
    center_lane = closest_lane(lanes)
    
    if center_lane != None:
        x_1, y1, x2, y2 = center_lane[0]
        print (center_lane[0])
        slope1 = (y1-y2)/(x_1-x2)
        x1, y1, x2, y2 = center_lane[1]
        print (center_lane[1])
        slope2 = (y1-y2)/(x1-x2)
        center_slope = 1/ (((1/slope1) + (1/slope2)) / 2)
        center_intercept = (x_1+x1)/2
    else:
        return None, None
    

    return center_intercept, center_slope


def recommend_direction (center, slope):
    image_midline = 3824/2
    if center == image_midline:
        movement = "forward"  
    elif center < image_midline:
        movement = "left"
    else:
        movement = "right"

    if 1/slope > 0:
        print("turn right")
    if 1/slope < 0:
        print("turn Left")
    
    return movement


def draw_center_line (img, lanes):
    center_intercept, center_slope = get_lane_center(lanes)

    if center_intercept != None:
        center_intercept = int(center_intercept)
        center_lane = closest_lane(lanes)
        z1 = center_intercept
        z1 = int(z1)    
        x_1, y_1, x_2, y_2 = center_lane[0]
        x_1, y_1, x_2, y_2 = int(x_1), int(y_1), int(x_2), int(y_2)
        x1, y1, x2, y2 = center_lane[1]
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        x_intercept_center = (x_2 + x2)/2
        x_intercept_center = int(x_intercept_center)
        cv2.line(img, (z1, y_1), (x_intercept_center, y_2), (0, 255, 255), 2)

    return img








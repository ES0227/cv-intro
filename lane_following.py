import lane_detection_code
import cv2
import matplotlib.pyplot as plt
import math


def find_closest_lane(lanes):
    if not lanes:
        return None

    min_dist_from_center = float('inf')
    center_lane = None

    for detected_lane in lanes:
        print(len(detected_lane))
        if detected_lane is not None and len(detected_lane[0]) >= 1: #and len(detected_lane[0]) == 4 and len(detected_lane[1]) == 2:
            lane_center = abs(detected_lane[0][0] + detected_lane[1][0]) / 2
            dist_from_center = abs(2138 - lane_center)
            if dist_from_center < min_dist_from_center:
                min_dist_from_center = dist_from_center
                center_lane = detected_lane
        # else: 
        #     return "invalid length"


    return center_lane

def get_lane_center(closest_lane):
    # print(f"closest_lane: {closest_lane}")
    # print(f"length of closest_lane: {len(closest_lane)}")
    if closest_lane is not None:
        x_1, y_1, x_2, y_2 = closest_lane[0]
        x1, y1, x2, y2 = closest_lane[1]
        center_intercept = (x_1 + x1) / 2
        slope1 = (y_2 - y_1)/(x_2 - x_1)
        slope2 = (y2 - y1)/(x2 - x1)
        center_slope = (1/((1/slope1 + 1/slope2)/2))
        return center_intercept, center_slope

    return 0.0, 0.0

# Rest of your code...

# def closest_lane(lanes):
#     min_distFromCenter = float(40000)
#     center_lane = None
#     #max_thickness = 0
    
#     for detected_lane in lanes: #get the average of the x intercepts of the lines making up a lane and then compare them  to see which one is closest to half the resolution
#         lane_center = abs(detected_lane[0][0] + detected_lane[1][0])/2 #FIX THIS!!!!!!!!!!
#         print(detected_lane[0][0])
#         distFromCenter = abs(2138-lane_center)
#         if distFromCenter < min_distFromCenter:
#             min_distFromCenter = distFromCenter
#             center_lane = detected_lane
    
#         # if max_thickness < thickness:
#         #     max_thickness = thickness
#         #     center_lane = detected_lane

#     return center_lane

# def get_lane_center(closest_lane):
    
    
#     if closest_lane != None:
#         x_1, y1, x2, y2 = closest_lane[0]
#         print (closest_lane[0])
#         slope1 = (y1-y2)/(x_1-x2)
#         x1, y1, x2, y2 = closest_lane[1]
#         print (closest_lane[1])
#         slope2 = (y1-y2)/(x1-x2)
#         center_slope = 1/ (((1/slope1) + (1/slope2)) / 2)
#         center_intercept = (x_1+x1)/2
#     else:
#         return None, None
    

#     return center_intercept, center_slope

def angle_between_lines(m1, m2):
    tan_theta = abs((m2 - m1) / (1 + m1 * m2))
    theta = math.atan(tan_theta)
    return math.degrees(theta)

def recommend_direction (center, slope):
    image_midline = 1912
    center_int = None

    if center is not None:
        center_int = int(center)
    if center is None: 
        return "No lane detected"

    horizontal_distance = image_midline - center_int
    max_distance = 3
    if abs(horizontal_distance) <= max_distance:
        movement = "forward"  
    elif horizontal_distance < 0:
        movement = "left for " + str(abs(horizontal_distance))
    else:
        movement = "right" + str(horizontal_distance)


    angleOfAUV = 90 - angle_between_lines(slope, 0)  
    if slope > 0:
        angleOfAUV = -angleOfAUV
        movement += "," + str(angleOfAUV) + " degrees to the left"
        #pass
    elif slope < 0:
        movement += "," + str(angleOfAUV) + " degrees to the right"
        #pass
    return movement
    


def draw_center_line (img, lanes):
    center_intercept, center_slope = get_lane_center(lanes)

    if center_intercept != None:
        center_intercept = int(center_intercept)
        center_lane = find_closest_lane(lanes)
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








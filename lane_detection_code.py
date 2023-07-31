import cv2
import numpy as np
import matplotlib.pyplot as plt
import random


def detect_lines(img, threshold1 = 30, threshold2 = 43, apertureSize = 3, minLineLength = 667, maxLineGap = 33):
    
    img = img
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, threshold1, threshold2, apertureSize) 
    #lines_list = []
    lines = cv2.HoughLinesP(
            edges,
            rho = 1,
            theta = np.pi/180,
            threshold = 100,
            minLineLength = minLineLength,
            maxLineGap = maxLineGap,
            )
    # try:
    #     for points in lines:
    #         x1,y1,x2,y2=points[0]
    #         lines_list.append([(x1,y1),(x2,y2)])
    #     # for line in lines:
    #     #     x1, y1, x2, y2 = line[0]
    #     #     cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
    #     #     line_list += [()]
    # except TypeError:
    #     pass

    return lines

def drawLines(img, lines, color = (0, 255, 0)):
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 30, 43, apertureSize=3)
    lines = cv2.HoughLinesP(edges, 2, np.pi/180, 100, minLineLength=667, maxLineGap=33)
    try:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(img, (x1, y1), (x2, y2), color, 2)
            slope = (y2-y1)/(x2-x1)
            print(str(slope))
    except TypeError:
        print ("error")
    
    return img

def get_slopes_intercepts(lines):
    slopes = []
    intercepts = []
    try:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            slope = (y2-y1)/(x2-x1)
            slopes.append(slope)
            intercept = ((2138-y1)/slope + x1)
            #intercept = (y2-y1)/slope + x1
            intercepts.append(intercept)
    except TypeError:
        pass


    return slopes, intercepts


def detect_lanes(lines):

    '''
    takes a list of lines as an input and returns a list of lanes

    parameters:
        lines: the list of lines to process
    
    '''

    slopeList, xInterceptList = get_slopes_intercepts(lines)
    # print (f"slopeList:{slopeList}")
    # print (f"xInterceptList:{xInterceptList}")
    lanes = []
    #check of the lines intersect on the screen
    if len(slopeList)> 1:
        for i in range(0,len(slopeList)):
           
            for j in range (i+1,len(slopeList)):
                
                interceptDist = abs(xInterceptList[i]-xInterceptList[j])
                slopeDiff = abs((1/ slopeList[i]) - (1/slopeList[j]))
               
                if (interceptDist > 1 and interceptDist< 10000 and slopeDiff< 5):
                    xPoint = ((slopeList[i] * xInterceptList[i]) - (slopeList[j] * xInterceptList[j]))/(slopeList[i]-slopeList[j])
                    yPoint = slopeList[i]*(xPoint - xInterceptList[i]) + 2138
                    
                  
                    # line1 = [xInterceptList[i], 2138, xPoint,yPoint]
                    # line2 = [xInterceptList[j], 2138, xPoint,yPoint]
                    # lane = [line1,line2]

                    line1 = [xInterceptList[i], 2138, xPoint,yPoint]
                    line2 = [xInterceptList[j], 2138, xPoint,yPoint]
                    lane = [line1,line2]

                    lanes.append(lane)


    return lanes


def draw_lanes (img, lanes):
    for lane in lanes:
        for line in lane:
            x1, y1, x2, y2 = line
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

            cv2.line(img,(x1,y1),(x2,y2),(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),2)

    return img


    # for i in slopes:
    #     idx = lines.index(i)
    #     for j in range(len(lines)):
    #         if(idx - j < 1.7):
    #             lanes.append([idx, j])
    # return lanes


# def get_slopes_intercepts (lines):
#     img = cv2.imread('lanes.png')
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     edges = cv2.Canny(gray, 50, 150, 3)
#     lines_list = []
#     slopes = []
#     x_intercepts = []
#     lines = cv2.HoughLinesP(
#                     edges, 
#                     1, 
#                     np.pi/180, 
#                     10, 
#                     100,
#                     10,
#             )
#     try:
#         for points in lines:
#             x1,y1,x2,y2=points[0]
#             lines_list.append([(x1,y1),(x2,y2)])
#     except TypeError:
#         pass
#     try: 
#         for line in lines:
#             x1, y1, x2, y2 = line[0]
#             cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
#             slope = (y2-y1)/(x2-x1)
#             print(str(slope))
#     except TypeError:
#         pass
     
#     for i in range (len(slopes)):
#         x1, y1 = lines_list[i]
#         slope = slopes[i]
#         b = x1[1] - (slope*x1[0])
#         x_intercepts.append(b)

#     #return x_intercepts and slopes
#     #return slopes
#     #return x_intercepts


# def detect_lanes (lines: list):
#     x_intercepts, slopes = get_slopes_intercepts (lines)
#     for i in slopes:
#         lanes = []
#         idx = lines.index(i)
#         for j in range(len(lines)):
#             if(idx - j < 1.7):
#                 lanes.append([[idx, j]])
    
#     return lanes

# def draw_lanes (img, lines: list):
#     img = cv2.imread('rov_pool.jpg')
#     lanes = detect_lanes (lines)
#     try:
#         for points in lines:
#             x1,y1,x2,y2=points[0]
#             lines_list.append([(x1,y1),(x2,y2)])
#     except TypeError:
#         pass

#     color1 = random.randint(0, 255)
#     color2 = random.randint(0, 255)
#     color3 = random.randint(0, 255)
#     cv2.line(img,(x1,y1),(x2,y2),(color1, color2, color3),2)

#     return img

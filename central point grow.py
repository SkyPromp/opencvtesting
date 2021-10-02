import cv2 as cv
import numpy as np
from copy import deepcopy
import random
from matplotlib import pyplot as plt


points = []
matrix = np.zeros((1080, 1920, 1), dtype='uint8')
matrix[matrix.shape[0] // 2][matrix.shape[1] // 2] = 255
white = 1
total = matrix.shape[1] * matrix.shape[0]


out = cv.VideoWriter('growHD.mp4', cv.VideoWriter_fourcc(*'mp4v'), 20, (matrix.shape[1], matrix.shape[0]), False)

play = True
while play:
    point_count = 0
    play = False
    copy = deepcopy(matrix)
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == 255:
                point_count += 1
                if i - 1 >= 0 and random.random() < 0.3 and copy[i - 1][j] != 255:
                    copy[i - 1][j] = 255
                    white += 1
                if i + 1 < len(matrix) and random.random() < 0.3 and copy[i + 1][j] != 255:
                    copy[i + 1][j] = 255
                    white += 1
                if j - 1 >= 0 and random.random() < 0.3 and copy[i][j - 1] != 255:
                    copy[i][j - 1] = 255
                    white += 1
                if j + 1 < len(matrix[0]) and random.random() < 0.3 and copy[i][j + 1] != 255:
                    copy[i][j + 1] = 255
                    white += 1
            else:
                play = True

    points.append(point_count)

    # show = cv.resize(copy, (copy.shape[1]*4, copy.shape[0]*4), interpolation=cv.INTER_CUBIC)
    # cv.imshow("Growing", show)
    # out.write(show)
    out.write(copy)
    print(round(1000*white/total)/10, "%")
    # cv.waitKey(1)
    matrix = deepcopy(copy)
    #plt.plot([i for i in range(len(points))], points)
    #plt.show()

print('done')

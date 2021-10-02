import cv2 as cv
import numpy as np
from copy import deepcopy
import random


matrix = np.zeros((100, 100, 1), dtype='uint8')

check = True
while check:
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if random.random() < 0.001:
                check = False
                matrix[i][j] = 255

play = True
while play:
    play = False
    copy = deepcopy(matrix)
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == 255:
                if i - 1 >= 0 and random.random() < 0.3:
                    copy[i - 1][j] = 255
                if i + 1 < len(matrix) and random.random() < 0.3:
                    copy[i + 1][j] = 255
                if j - 1 >= 0 and random.random() < 0.3:
                    copy[i][j - 1] = 255
                if j + 1 < len(matrix[0]) and random.random() < 0.3:
                    copy[i][j + 1] = 255
            else:
                play = True

    show = cv.resize(copy, (copy.shape[1] * 10, copy.shape[0] * 10), interpolation=cv.INTER_CUBIC)
    cv.imshow("Growing", show)
    cv.waitKey(50)
    matrix = deepcopy(copy)

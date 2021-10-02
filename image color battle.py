import cv2 as cv
import numpy as np
from copy import deepcopy
import random


img = cv.imread("Photos/picture.png")
matrix = cv.resize(img, (img.shape[1]//4, img.shape[0]//4), interpolation=cv.INTER_AREA)

play = True
while play:
    play = False
    copy = deepcopy(matrix)
    check = copy[0][0]
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            color = matrix[i][j]
            if i - 1 >= 0 and random.random() < 0.3:
                copy[i - 1][j] = color
            if i + 1 < len(matrix) and random.random() < 0.3:
                copy[i + 1][j] = color
            if j - 1 >= 0 and random.random() < 0.3:
                copy[i][j - 1] = color
            if j + 1 < len(matrix[0]) and random.random() < 0.3:
                copy[i][j + 1] = color

            if not np.array_equal(copy[i][j], check):
                play = True

    show = cv.resize(copy, (copy.shape[1] * 4, copy.shape[0] * 4), interpolation=cv.INTER_CUBIC)
    cv.imshow("Growing", show)
    cv.waitKey(1)
    matrix = deepcopy(copy)

import cv2 as cv
from copy import deepcopy
import random


img = cv.imread("Photos/roddel.png")
img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
matrix = cv.resize(img, (img.shape[1]//4, img.shape[0]//4), interpolation=cv.INTER_AREA)
matrix = cv.Canny(matrix, 125, 175)
(_, matrix) = cv.threshold(matrix, 127, 255, cv.THRESH_BINARY)

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

    show = cv.resize(copy, (copy.shape[1] * 4, copy.shape[0] * 4), interpolation=cv.INTER_CUBIC)
    cv.imshow("Growing", show)
    cv.waitKey(250)
    matrix = deepcopy(copy)

import cv2 as cv
import numpy as np
import random
import math


class Vector:
    def __init__(self, direction, stepsize, position, board_size):
        self.x, self.y = position
        self.size = stepsize
        self.direction = direction
        self.width, self.height = board_size

    def wall(self, length):
        if self.x + math.cos(self.direction) * length < 0:
            self.direction = math.pi - self.direction

        if self.y + math.sin(self.direction) * length < 0:
            self.direction *= -1

        if self.x + math.cos(self.direction) * length >= self.width - 1:
            self.direction = math.pi - self.direction

        if self.y + math.sin(self.direction) * length >= self.height - 1:
            self.direction *= -1

    def next(self):
        if not self.wall(self.size):
            self.x += math.cos(self.direction) * self.size
            self.y += math.sin(self.direction) * self.size


# Summon the starting vectors
def createVectors(amount=500, radius=0):
    vectors_out = []
    for k in range(amount):
        vectors_out.append(
                    Vector(k/amount * 2 * math.pi,  # direction
                    1,  # stepsize
                    (img.shape[0] // 2 + radius * math.cos(k/amount * 2 * math.pi),  # x coordinate of the vector
                     img.shape[1] // 2 + radius * math.sin(k/amount * 2 * math.pi)),  # y coordinate of the vector
                    (img.shape[0], img.shape[1])))  # shape of the image

    return vectors_out


# Create empty canvas
img = np.zeros((135, 240, 1), dtype='uint8')

# make mp4 file with correct specifications
# out = cv.VideoWriter('recording.mp4', cv.VideoWriter_fourcc(*'mp4v'), 60, (img.shape[1], img.shape[0]), False)

vectors = createVectors()

for _ in range(500):
    # img = cv.GaussianBlur(img, (3, 3), cv.BORDER_DEFAULT)
    cv.imshow("img", cv.resize(img, (img.shape[1]*8, img.shape[0]*8)))  # show blurred image
    # out.write(img)
    cv.waitKey(1)

    trail_shortness = 2
    for i in range(len(img)):
        for j in range(len(img[i])):
            if img[i][j] >= trail_shortness:
                img[i][j] -= trail_shortness

    for i in vectors:
        img[round(i.x)][round(i.y)] = 255
        i.next()


# out.release()

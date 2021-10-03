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


img = np.zeros((135, 240, 1), dtype='uint8')

# out = cv.VideoWriter('recording.mp4', cv.VideoWriter_fourcc(*'mp4v'), 60, (img.shape[1], img.shape[0]), False)

# Summon a central vector
vector = Vector(random.random() * 2 * math.pi, 1, (img.shape[0]//2, img.shape[1]//2), (img.shape[0], img.shape[1]))

vectors = [vector]

# Summon the starting vectors
check = True
while check:
    for i in range(len(img)):
        for j in range(len(img[i])):
            if random.random() < 0.001:
                check = False
                vectors.append(Vector(random.random() * 2 * math.pi, 1, (i, j), (img.shape[0], img.shape[1])))


for progress in range(8000):
    print(100*progress/8000, "%", sep="")
    cv.imshow("img", img)  # show blurred image
    # out.write(img)
    cv.waitKey(1)

    # Fades out the color until it becomes black
    trail_shortness = 1
    img[:, :] -= trail_shortness
    img[:][img[:] > 255 - trail_shortness] = 0

    for i in vectors:
        img[round(i.x)][round(i.y)] = 255
        i.next()

    # blank = np.zeros((1000, 1000, 1), dtype='uint8')
    # blank[round(vector.x)][round(vector.y)] = 255
    # cv.imshow("img", blank)
    # cv.waitKey(1)
    # img[round(vector.x)][round(vector.y)] = 255
    # vector.next()

# out.release()
cv.destroyAllWindows()

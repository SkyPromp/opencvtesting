import cv2 as cv
import numpy as np
import random
import math


# Define vectors and their movement
class Vector:
    def __init__(self, direction, stepsize, position, board_size):
        self.x, self.y = position
        self.size = stepsize
        self.direction = direction
        self.width, self.height = board_size

    def wall(self, length, direction):
        if self.x + math.cos(direction) * length < 0:
            self.direction = math.pi - direction

        elif self.x + math.cos(direction) * length >= self.width - 1:
            self.direction = math.pi - direction

        if self.y + math.sin(direction) * length < 0:
            self.direction = -1 * direction

        elif self.y + math.sin(direction) * length >= self.height - 1:
            self.direction = -1 * direction

    def wallRandomAngle(self, length, direction):
        if self.x + math.cos(direction) * length < 0:
            self.direction = random.random() * math.pi - math.pi / 2

        elif self.x + math.cos(direction) * length >= self.width - 1:
            self.direction = random.random() * math.pi - math.pi / 2

        if self.y + math.sin(direction) * length < 0:
            self.direction = math.pi * random.random()

        elif self.y + math.sin(direction) * length >= self.height - 1:
            self.direction = -1 * math.pi * random.random()

    def nextCentral(self):
        self.wallRandomAngle(self.size, self.direction)

        self.x += math.cos(self.direction) * self.size
        self.y += math.sin(self.direction) * self.size

    def getRelativePositions(self, angle, radius, image):
        center_x = round(self.x + math.cos(self.direction) * radius)
        center_y = round(self.y + math.sin(self.direction) * radius)

        if center_x > image.shape[0] - 1:
            center_x = image.shape[0] - 1
        elif center_x < 0:
            center_x = 0
        if center_y > image.shape[1] - 1:
            center_y = image.shape[1] - 1
        elif center_y < 0:
            center_y = 0

        left_x = round(self.x + math.cos(self.direction + angle) * radius)
        left_y = round(self.y + math.sin(self.direction + angle) * radius)

        if left_x > image.shape[0] - 1:
            left_x = image.shape[0] - 1
        elif left_x < 0:
            left_x = 0
        if left_y > image.shape[1] - 1:
            left_y = image.shape[1] - 1
        elif left_y < 0:
            left_y = 0

        right_x = round(self.x + math.cos(self.direction - angle) * radius)
        right_y = round(self.y + math.sin(self.direction - angle) * radius)

        if right_x > image.shape[0] - 1:
            right_x = image.shape[0] - 1
        elif right_x < 0:
            right_x = 0
        if right_y > image.shape[1] - 1:
            right_y = image.shape[1] - 1
        elif right_y < 0:
            right_y = 0

        # afraid of the dark
        left_weight = random.random() * image[left_x][left_y]/255
        center_weight = random.random() * image[center_x][center_y]/255
        right_weight = random.random() * image[right_x][right_y]/255

        # left_weight = random.random() * (1/255 + image[left_x][left_y]/255)
        # center_weight = random.random() * (1/255 + image[center_x][center_y]/255)
        # right_weight = random.random() * (1/255 + image[right_x][right_y]/255

        if center_weight >= left_weight:
            if center_weight >= right_weight:
                self.nextCentral()
            else:
                self.wall(self.size, self.direction - angle)
                self.x += math.cos(self.direction - angle) * self.size
                self.y += math.sin(self.direction - angle) * self.size

        elif center_weight >= right_weight:
            if center_weight >= left_weight:
                self.nextCentral()
            else:
                self.wall(self.size, self.direction + angle)
                self.x += math.cos(self.direction + angle) * self.size
                self.y += math.sin(self.direction + angle) * self.size

        else:
            if right_weight > left_weight:
                self.wall(self.size, self.direction - angle)
                self.x += math.cos(self.direction - angle) * self.size
                self.y += math.sin(self.direction - angle) * self.size
            elif left_weight > right_weight:
                self.wall(self.size, self.direction + angle)
                self.x += math.cos(self.direction + angle) * self.size
                self.y += math.sin(self.direction + angle) * self.size

            elif random.random() < 0.5:
                self.wall(self.size, self.direction - angle)
                self.x += math.cos(self.direction - angle) * self.size
                self.y += math.sin(self.direction - angle) * self.size
            else:
                self.wall(self.size, self.direction + angle)
                self.x += math.cos(self.direction + angle) * self.size
                self.y += math.sin(self.direction + angle) * self.size

        if self.x > self.width - 1:
            self.x = self.width - 1
        elif self.x < 0:
            self.x = 0

        if self.y > self.height - 1:
            self.y = self.height - 1
        elif self.y < 0:
            self.y = 0


        # return (left_x, left_y), (center_x, center_y), (right_x, right_y)


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
# out = cv.VideoWriter('slime480p.mp4', cv.VideoWriter_fourcc(*'mp4v'), 60, (img.shape[1], img.shape[0]), False)

vectors = createVectors(500)

frames = 3000
for progress in range(frames):
    print(100 * progress/frames, "%", sep="")
    img = cv.GaussianBlur(img, (3, 3), cv.BORDER_DEFAULT)
    cv.imshow("img", cv.resize(img, (img.shape[1]*4, img.shape[0]*4)))  # show blurred image
    # out.write(img)
    cv.waitKey(1)

    trail_shortness = 2
    for i in range(len(img)):
        for j in range(len(img[i])):
            if img[i][j] >= trail_shortness:
                img[i][j] -= trail_shortness
            else:
                img[i][j] = 0

    for i in vectors:
        img[round(i.x)][round(i.y)] = 255
        i.getRelativePositions(math.pi/4, 10, img)


# out.release()

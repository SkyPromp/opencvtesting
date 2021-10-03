import cv2 as cv
import numpy as np
import random
import math
import winsound


# Define vectors and their movement
class Vector:
    def __init__(self, direction, position, board_size):
        self.x, self.y = position
        self.direction = direction
        self.width, self.height = board_size

    def wall(self, direction):
        if self.x + math.cos(direction) < 0 or self.x + math.cos(direction) >= self.width - 1:
            self.direction = math.pi - direction

        if self.y + math.sin(direction) < 0 or self.y + math.sin(direction) >= self.height - 1:
            self.direction = -direction

    # TODO: Fix this method
    def wallRandomAngle(self, length, direction):
        if self.x + math.cos(direction) * length < 0:
            self.direction = random.random() * math.pi - math.pi / 2

        elif self.x + math.cos(direction) * length >= self.width - 1:
            self.direction = random.random() * math.pi - math.pi / 2

        if self.y + math.sin(direction) * length < 0:
            self.direction = math.pi * random.random()

        elif self.y + math.sin(direction) * length >= self.height - 1:
            self.direction = -1 * math.pi * random.random()

    def coordsInBounds(self, x, y):
        if x > self.width - 1:
            x = self.width - 1
        elif x < 0:
            x = 0
        if y > self.height - 1:
            y = self.height - 1
        elif y < 0:
            y = 0

        return x, y

    def calculateNextPosition(self, angle, radius):
        x = round(self.x + math.cos(self.direction + angle) * radius)
        y = round(self.y + math.sin(self.direction + angle) * radius)
        return self.coordsInBounds(x, y)

    def getRelativePositions(self, angle, radius, image):
        center_x, center_y = self.calculateNextPosition(0, radius)
        left_x, left_y = self.calculateNextPosition(angle, radius)
        right_x, right_y = self.calculateNextPosition(-angle, radius)

        # Will not consider going to a dark square, if all squares are dark, go straight
        weights = [random.random() * image[center_x][center_y]/255,  # Center weight
                   random.random() * image[left_x][left_y]/255,  # Left weight
                   random.random() * image[right_x][right_y]/255]  # Right weight
        rotation = [0, angle, -angle][max(range(len(weights)), key=weights.__getitem__)]

        self.wall(self.direction + rotation)
        self.x += math.cos(self.direction + rotation)
        self.y += math.sin(self.direction + rotation)

        # TODO: Find a way to remove this check
        self.x, self.y = self.coordsInBounds(self.x, self.y)


# Summon the starting vectors (direction should be 1 or -1
def createVectorRing(amount=500, radius=0, direction=1):
    vectors_out = []
    for k in range(amount):
        vectors_out.append(
                    Vector(k/amount * 2 * math.pi,  # direction
                    (img.shape[0] // 2 + direction * radius * math.cos(k/amount * 2 * math.pi),  # x coordinate of the vector
                     img.shape[1] // 2 + direction * radius * math.sin(k/amount * 2 * math.pi)),  # y coordinate of the vector
                    (img.shape[0], img.shape[1])))  # shape of the image

    return vectors_out


def createVectorCircle(amount=500, radius=0, direction=1):
    vectors_out = []
    for k in range(amount):
        vectors_out.append(
            Vector(k/amount * 2 * math.pi,  # direction
                   (img.shape[0] // 2 + direction * random.random() * radius * math.cos(k/amount * 2 * math.pi),  # x coordinate of the vector
                    img.shape[1] // 2 + direction * random.random() * radius * math.sin(k/amount * 2 * math.pi)),  # y coordinate of the vector
                   (img.shape[0], img.shape[1])))  # shape of the image

    return vectors_out


# Create empty canvas
img = np.zeros((270, 480, 1), dtype='uint8')

# make mp4 file with correct specifications
# out = cv.VideoWriter('slimeHD60fps.mp4', cv.VideoWriter_fourcc(*'mp4v'), 60, (img.shape[1], img.shape[0]), False)

vectors = createVectorRing(8000, 100, -1)
frames = 7200
trail_shortness = 2
vector_view_angle = math.pi/4
for progress in range(frames):
    # print(100 * progress/frames, "%", sep="")
    img = cv.GaussianBlur(img, (3, 3), cv.BORDER_DEFAULT)
    cv.imshow("img", cv.resize(img, (img.shape[1]*2, img.shape[0]*2)))  # show blurred image
    # out.write(img)
    cv.waitKey(1)

    # Fades out the color until it becomes black
    img[:, :] -= trail_shortness
    img[:][img[:] > 255 - trail_shortness] = 0

    for vector in vectors:
        img[round(vector.x)][round(vector.y)] = 255
        vector.getRelativePositions(vector_view_angle, 10, img)


# out.release()
winsound.Beep(440, 200)

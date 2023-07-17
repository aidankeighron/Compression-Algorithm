import numpy as np
import cv2, math, random

image = [[1,0,1,1,0],
         [0,1,1,0,1],
         [1,0,1,1,0],
         [0,1,0,1,0],
         [1,0,1,0,1]]
digits = 6

image = np.array(image, dtype="uint8")

def convert_image(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.threshold(image, 180, 255, cv2.THRESH_BINARY)[1]
    image[:] //= 255
    return image

def zero(input):
    num_zeroes = digits-len(str(input))
    return '0'*num_zeroes+str(input)
def compress(image):
    image_string = ""
    for row in image:
        for colum in row:
            image_string += str(colum)
            
    iterations = 0
    random.seed(1)
    while True:
        iterations += 1
        print(iterations)
        key = ""
        for _ in range(0, len(image_string)*2):
            key += str(random.choice([0,1]))

        if image_string in str(key):
            index = str(key).find(image_string)
            length = len(image_string)
            return zero(index)+zero(length)+zero(iterations), image_string
# 3x3 100
# 4x4 10,000
# 5x5 100,000
def decompress(key):
    random.seed(1)
    index, length, iterations = [int(''.join(key[x:x+digits])) for x in range(0, len(key), digits)]
    for _ in range(0, iterations):
        key = ""
        for _ in range(0, length*2):
            key += str(random.choice([0,1]))
        image = key[index:index+length]
    image = np.array([int(pixel) for pixel in image], dtype="uint8")
    image[:] *= 255
    image = image.reshape(int(math.sqrt(length)), int(math.sqrt(length)))
    return image

result, answer = compress(image)
print(result)
print(answer)
decompressed_image = decompress(result)
image[:] *= 255
cv2.imshow("original image", cv2.resize(image, (500, 500), interpolation=cv2.INTER_NEAREST))
cv2.imshow("decompressed image", cv2.resize(decompressed_image, (500, 500), interpolation=cv2.INTER_NEAREST))
cv2.waitKey(0)

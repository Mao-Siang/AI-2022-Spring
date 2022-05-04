import os
import cv2
from cv2 import waitKey
import matplotlib.pyplot as plt

def detect(dataPath, clf):
    """
    Please read detectData.txt to understand the format. Load the image and get
    the face images. Transfer the face images to 19 x 19 and grayscale images.
    Use clf.classify() function to detect faces. Show face detection results.
    If the result is True, draw the green box on the image. Otherwise, draw
    the red box on the image.
      Parameters:
        dataPath: the path of detectData.txt
      Returns:
        No returns.
    """
    # Begin your code (Part 4)
    # raise NotImplementedError("To be implemented")
    '''
    First, open file by the given datapath.
    We read the first line and get the path of picture and numbers of faces to be detected.
    Second, we read the original image using imread function.
    Third, we read the coordinates , width, and height from the txt file.
    Crop the image into certain size, and convert the color to grayscale using cvtColor().
    Then, resize the image to 19*19, and finally use the classifier to classify the image.
    if the result is face, we draw a green rectangle using cv2.rectangle()
    otherwise, we draw a red one
    when we finish reading the file, the process ends.
    '''
    with open(dataPath, "r") as f:
      while True:
        curline = f.readline()
        if curline == "": break
        picPath, num = [i for i in curline.split()]
        img = cv2.imread(os.path.join("data/detect",picPath), cv2.IMREAD_COLOR)
        
        for _ in range(int(num)):
          x1, y1, w, h = [int(i) for i in f.readline().split()]
          croped = img[y1:y1+h, x1:x1+w]
          gray = cv2.cvtColor(croped,cv2.COLOR_BGR2GRAY)
          resized = cv2.resize(gray,(19,19),interpolation=cv2.INTER_AREA)
          if clf.classify(resized) == 1:
            result = cv2.rectangle(img,(x1,y1),(x1+w,y1+h),(0,255,0),2)
          else:
            result = cv2.rectangle(img,(x1,y1),(x1+w,y1+h),(0,0,255),2)
      
        cv2.imshow("result", result)
        cv2.waitKey(0)  
    # End your code (Part 4)

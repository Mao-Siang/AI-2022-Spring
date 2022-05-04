import os
import cv2
import numpy as np

from scipy.misc import face

def loadImages(dataPath):
    """
    load all Images in the folder and transfer a list of tuples. The first 
    element is the numpy array of shape (m, n) representing the image. 
    The second element is its classification (1 or 0)
      Parameters:
        dataPath: The folder path.
      Returns:
        dataset: The list of tuples.
    """
    # Begin your code (Part 1)
    # raise NotImplementedError("To be implemented")
    '''
    First create a empty list called dataset.
    Then read the images from given datapath in grayscale.
    label the image 0 if it is from the folder called non-face, otherwise 1.
    Finally, append them into dataset list. 
    '''
    NON_FACE, FACE = 0, 1
    
    dataset = []
    for folder in os.listdir(dataPath):
      label = NON_FACE if folder.find('non') != -1 else FACE
      folder = os.path.join(dataPath,folder)
      for imgfile in os.listdir(folder):
        f = cv2.imread(os.path.join(folder, imgfile), cv2.IMREAD_GRAYSCALE)
        dataset.append((f, label))
        
    # End your code (Part 1)
    
    return dataset

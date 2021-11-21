# -*- coding: utf-8 -*-

'''
Created on Apr 22, 2015

@author: Daniel Oñoro Rubio
'''

# File storage
import h5py
import pickle
import scipy.io as sio

# System
import signal
import sys, getopt
signal.signal(signal.SIGINT, signal.SIG_DFL)
import time

# Vision and maths
import numpy as np
from spatialAverage import *
from utils import *
from gen_features import formMultispectralPos
from sklearn.ensemble import ExtraTreesRegressor
from skimage import io

class DEstimator(object):
    '''
    Density estimator class for TRANCOS dataset.
    '''

    def __init__(self, rf_file, pw = 9):
        '''
        Constructor
        @param rf_file: Random forest trained file (pkl file).
        @param pw: training patch width
        '''
        
        # Load forest
        self.rf_ = pickle.load(open(rf_file, 'r'))
        self.rf_.verbose = 0 # We don't want to talk here
        self.pw_ = pw
    
    def testOnImg(self, im, batch_size = 50000):
    
        # Compute dense positions
        [heith, width] = im.shape
        pos = get_dense_pos(heith, width, self.pw_, stride=self.pw_/3)
    
        if(batch_size <= 0):
            batch_size = pos.shape[0]
    
        pred = []    
        for batch_pos in batch(pos, batch_size):
            # Extract features
            fMatrixTest = formMultispectralPos(im, batch_pos, self.pw_) 
            
            # Predict
            fMatrixTest = fMatrixTest.astype(np.float64)
            pred.append( self.rf_.predict(fMatrixTest) )
        
        pred = np.vstack(pred)
        
        # Recover density map
        resImg=spatialAverage((heith,width),pos,pred,pw=self.pw_) #spatial average of the prediction

        npred=resImg.sum()
    
        return npred, resImg
    
    def predict(self, in_im_path, out_im_path):
        '''
        Take an image from its path and generate its vehicle count as an output
        and as a image file.
        @param in_im_path: input image path.
        @param out_im_path: output image path.
        @return: vehicle count.
        '''
        # Read image
        im = io.imread(in_im_path, as_grey=True)
        im = np.asarray(im)
        
        # Compute prediction
        count, dens = self.testOnImg(im)
        
        # Normalize and convert to gray
        dens = dens / dens.max() * 255
        dens = dens.astype( np.uint8 )
        
        # Save image
        io.imsave(out_im_path, dens)
        
        return count

if __name__ == "__main__":
    print "Running test"
    stm = DEstimator('models/rf_model_multi.pkl')
    count = stm.predict('image-3-000012.jpg','image-3-000012_dens.jpg')
    print "Test density count %.2f vehicles" % count

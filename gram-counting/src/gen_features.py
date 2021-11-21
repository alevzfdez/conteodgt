# -*- coding: utf-8 -*-

'''
    @author: Daniel Oñoro Rubio
    @contact: daniel.onoro@edu.uah.es
    @date: 26/02/2015
    @note: Fiachi code was used as a baseline.
'''

#===========================================================================
# Dependency loading
#===========================================================================

# Parallel computing
from joblib import Parallel, delayed  
import multiprocessing

# System
import signal
import sys, getopt
signal.signal(signal.SIGINT, signal.SIG_DFL)
import time

# File storage
import h5py

# Vision and maths
import vigra
import numpy as np
from spatialAverage import *
from utils import *
from skimage import color

# Plotting
import matplotlib.pyplot as plt


'''
    @brief: This function gets an image and returns its multipsectral feature 
    image.
    @param im: annotated dot image list.
    @return: multipsectral feature image.
'''
def formMultispectral(img):
    # Extract the features responses on the image

    if np.ndim(img) == 3:
        im_gray = color.rgb2grey(img)
    else:
        im_gray = img.copy()
        
    im_gray = im_gray.astype(np.float32)

    a = []    
    a.append(im_gray)
    
    N = 3
    base = 0.8
    r2 = 2
    for n in range(N):
        f = base * (r2 ** n)
        gg = vigra.filters.gaussianGradientMagnitude(im_gray, f).view(np.ndarray)
        a.append(gg)
        te = vigra.filters.structureTensorEigenvalues(im_gray, f, f * 2).view(np.ndarray)
        a.append(te)
        
        lg = vigra.filters.laplacianOfGaussian(im_gray, f).view(np.ndarray)
        a.append(lg)

    res = np.dstack(a)
    return res

'''
    @brief: Extract multispectral features from given positions.
    @param im: input color image.
    @param pos: (x,y) input position 
    @return: multipsectral feature list.
'''
def formMultispectralPos(img, pos, pw):
    
    feat_im = formMultispectral(img)
    
    return extract_at_pos(feat_im, pos, pw=pw)

'''
    @brief: This function gets a dotted image and returns its density map.
    @param dots: annotated dot image.
    @param sigmadots: density radius.
    @return: density map for the input dots image.
'''
def genDensity(dot_im, sigmadots):
    # Take only red channel
    dot = dot_im[:, :, 0]
    
    # print dot.max(),dot.min()
    dot /= 255
    dot = vigra.filters.gaussianSmoothing(dot, sigmadots).squeeze()
        
    return dot.view(np.ndarray).astype(np.float32)

def getGtPos(dot_im):
    '''
    @brief: This function gets a dotted image and returns the ground truth positions.
    @param dots: annotated dot image.
    @return: matrix with the notated object positions.
'''
    dot = dot_im[:, :, 0]
    
    # Find positions
    pos = np.where(dot == 1)
    
    pos = np.asarray( (pos[0],pos[1]) ).T
    
    return pos

def disp_help():
    print "======================================================"
    print "                       Usage"
    print "======================================================"
    print "\t-h display this message"
    print "\t--imfolder <image folder>"
    print "\t--names <image names txt file>"
    print "\t--ending <dot image ending pattenr>"
    print "\t--output <features file>"
    print "\t--pw <patch size. Default 7>"
    print "\t--nr <number of patches per image. Default 500. If it is lower than 1 it will be performed a dense extraction>"
    print "\t--sig <sigma for the density images. Default 2.5>"
    print "\t--prototxt <caffe prototxt file>"
    print "\t--caffemodel <caffe caffemodel file>"
    print "\t--meanim <mean image npy file>"
    print "\t--usecaffe <use caffe features>"
    
    
def main(argv):
    # Set default values
    stop = -1 
    im_folder = '../data/TRANCOS/images/'
    output_file = '../genfiles/train_multipsectral_feat.h5'
    im_list_file = '../data/TRANCOS/image_sets/training.txt'
    prototxt_path = '../models/deploy.prototxt'
    caffemodel_path = '../models/bvlc_reference_caffenet.caffemodel'
    mean_im_path = '../models/ilsvrc_2012_mean.npy'
    feat_layer = 'pool5'
    use_caffe = False
    
    # Img patterns
    dot_ending = 'dots.png'

    # Features extraction vars
    pw = 9  # Patch width 
    Nr = 500  # Number of patches extracted from the training images
    sigmadots = 15.0  # Densities sigma
        
    # Get parameters
    try:
        opts, _ = getopt.getopt(argv, "h:", ["imfolder=", "output=", "names=",
          "ending=", "pw=", "nr=", "sig=", "prototxt=", "caffemodel=",
          "meanim=", "layer=", "usecaffe"])
    except getopt.GetoptError:
        disp_help()
        return
    
    for opt, arg in opts:
        if opt == '-h':
            disp_help(argv[0])
            return
        elif opt in ("--imfolder"):
            im_folder = arg
        elif opt in ("--output"):
            output_file = arg
        elif opt in ("--names"):
            im_list_file = arg
        elif opt in ("--ending"):
            dot_ending = arg
        elif opt in ("--pw"):
            pw = int(arg)
        elif opt in ("--nr"):
            Nr = int(arg)
        elif opt in ("--sig"):
            sigmadots = float(arg)
        elif opt in ("--prototxt"):
            prototxt_path = arg
        elif opt in ("--caffemodel"):
            caffemodel_path = arg
        elif opt in ("--meanim"):
            mean_im_path = arg
        elif opt in ("--layer"):
            feat_layer = arg
        elif opt in ("--usecaffe"):
            use_caffe = True
    
    print "Choosen parameters:"
    print "-------------------"
    print "Data base location: ", im_folder
    print "Image names file: ", im_list_file 
    print "Output file:", output_file
    print "Dot image ending: ", dot_ending
    print "Patch width (pw): ", pw
    print "Number of patches per image: ", Nr
    print "Sigma for each dot: ", sigmadots
    print "Prototxt path: ", prototxt_path
    print "Caffemodel path: ", caffemodel_path
    print "Mean image path: ", mean_im_path
    print "Feature layer: ", feat_layer
    print "Use Caffe: ", use_caffe
    print "==================="
    
    print "Reading image file names:"
    im_names = np.loadtxt(im_list_file, dtype='str')

    # Init feature extractor
    ############################################################################
    extractor = formMultispectralPos
    ############################################################################
    
    fmatrix = []
    odens = []
    allpos = []
    lables = []
    for name in im_names:
        print "Processing image: ", name
        # Get image paths
        im_path = extendName(name, im_folder)
        dot_im_path = extendName(name, im_folder, use_ending=True, pattern=dot_ending)
        
        # Read image files
        im = caffe.io.load_image(im_path)
        dot_im = vigra.impex.readImage(dot_im_path).view(np.ndarray).swapaxes(0, 1).squeeze()
        
        # Collect features from random locations
        dens_im = genDensity(dot_im, sigmadots)
        
        gtpos = getGtPos(dot_im)
        
        ih=dens_im.shape[0]
        iw=dens_im.shape[1]
        
        dx=dy=pw/2
        gtdens = []
        gtpos2 = []
        for el in gtpos:
            x,y=el
            sx=slice(x-dx,x+dx+1,None)
            sy=slice(y-dy,y+dy+1,None)
            
            t=dens_im[sx,sy,...]
            
            if t.shape[0] != pw or t.shape[1] != pw:
                continue
            
            gtpos2.append(el)                
            gtdens.append(t.ravel())
        
        gtdens = np.vstack(gtdens)
        gtpos = np.vstack(gtpos2)

        gtfeat = extractor(im, gtpos, pw)

        fmatrix.append(gtfeat)
        odens.append(gtdens)
        allpos.append(gtpos)
        lables.append( np.ones( (gtfeat.shape[0], 1) ) )
        
        if Nr > 0 :
            dens_patches, pos = extract_at_random(dens_im, pw=pw, N=Nr)
        else:
            dens_patches, pos = extract_dense(dens_im, pw=pw)

        # Generate features
        ofeat = extractor(im, pos, pw)
        
        lables.append( -1*np.ones((ofeat.shape[0], 1)) )
        
        # Store features and densities 
        fmatrix.append(ofeat)
        odens.append(dens_patches)
        allpos.append(pos)
        
    fmatrix = np.vstack(fmatrix)
    odens = np.vstack(odens)
    allpos = np.vstack(allpos)
    lables = np.vstack(lables)
   
    print "Saving data..."
    print  "The dimension of the feature matrix is ", fmatrix.shape
    print "The dimension of the density matrix is ", odens.shape
    data = h5py.File(output_file, 'w')
    data["feat"] = fmatrix
    data["dens"] = odens
    data["pos"] = allpos
    data["pw"] = pw
    data["sig"] = sigmadots
    data["lables"] = lables
    data.close()
    
    print "--------------------"    
    print "Finish!"
    
if __name__ == "__main__":
    main(sys.argv[1:])

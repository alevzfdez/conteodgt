import os 
import glob
import vigra
import numpy as np
import scipy.io

'''
    @brief: Batch an iterable object.
    Example:
        for x in batch(range(0, 10), 3):
        ...     print x
        ... 
        [0, 1, 2]
        [3, 4, 5]
        [6, 7, 8]
        [9]
    @param iterable: iterable object.
    @param n: batch size.
    @return splits: return the iterable object splits
'''
def batch(iterable, n = 1):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx+n, l)]

'''
    @brief: This gets a file name format and adds the root directory and change 
    the extension if needed
    @param fname: file name.
    @param im_folder: im_folder path to add to each file name.
    @param use_ending: flag use to change the file extension.
    @param pattern: string that will substitute the original file ending. 
    @return new_name: list which contains all the converted names.
'''
def extendName(name, im_folder, use_ending=False, pattern=[]):
    
    final_name = im_folder + os.path.sep + name
    
    if use_ending:
        l_dot = final_name.rfind('.')
        final_name = final_name[0:l_dot] + pattern
    
    return final_name

'''
    @brief: This function gets a txt file that contains a list of file names 
    and extend each name with the path to the root folder and/or change the 
    extension.
    @param txt_file: text file which contains a file name list.
    @param im_folder: im_folder path to add to each file name.
    @param use_ending: flag use to change the file extension.
    @param pattern: string that will substitute the original file ending. 
    @return: names_list: list which contains all the converted names.
'''
def extendImNames(txt_file, im_folder, use_ending=False, pattern=[]):
    txt_names = np.loadtxt(txt_file, dtype='str')
    
    names = []
    for name in txt_names:
        final_name = extendName(name, im_folder, use_ending, pattern)
        names.append(final_name)
    
    return names

def importImagesFolder(im_names, skip=1, stop=-1, verbose=True):
    '''import all images from a folder that follow a certain pattern'''
    
    count = 0
    imgs = []
    for name in im_names[::skip]:
        if verbose: print name
        img = vigra.impex.readImage(name).view(np.ndarray).swapaxes(0, 1).squeeze()
        imgs.append(img)
        count += 1
        if count >= stop and stop != -1:
            break
    
    return imgs

def getMasks(fnames):
    
    masks = []
    for name in fnames:
        bw = scipy.io.loadmat(name, chars_as_strings=1, matlab_compatible=1)
        masks.append(bw.get('BW'))
    
    return masks


def shuffleWithIndex(listv, seed=None):
    # Shuffle a list and return the indexes
    if seed != None: np.random.seed(seed)
    listvp = np.asarray(listv, dtype=object)
    ind = np.arange(len(listv))
    ind = np.random.permutation(ind)
    listvp = listvp[ind]
    listvp = list(listvp)
    return listvp, ind
    

def takeIndexFromList(listv, ind):
    listvp = np.asarray(listv, dtype=object)
    return list(listvp[ind])


def shuffleRows(array):
    ind = np.arange(array.shape[0])
    np.random.shuffle(ind)
    array = np.take(array, ind, axis=0)
    return array, ind
    
def generateRandomOdd(pwbase, treeCount):
    # Generate random odd numbers in the interavel [0,pwbase]
    res = []
    count = 0
    while count < treeCount:
        ext = np.random.randint(0, pwbase, 1)
        if np.mod(ext, 2) == 1:
            res.append(ext)
            count += 1
    
    return res

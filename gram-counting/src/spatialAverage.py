import numpy as np
#from tools import showCC
from cythonf import _spatialAverage, _extract_dense2D
from cythonf import _e, _extract_dense3D, _extract_at_pos2D, _extract_at_pos3D
from utils import shuffleRows

def cartesian(arrays, out=None):
    """
    Generate a cartesian product of input arrays.

    Parameters
    ----------
    arrays : list of array-like
        1-D arrays to form the cartesian product of.
    out : ndarray
        Array to place the cartesian product in.

    Returns
    -------
    out : ndarray
        2-D array of shape (M, len(arrays)) containing cartesian products
        formed of input arrays.

    Examples
    --------
    >>> cartesian(([1, 2, 3], [4, 5], [6, 7]))
    array([[1, 4, 6],
           [1, 4, 7],
           [1, 5, 6],
           [1, 5, 7],
           [2, 4, 6],
           [2, 4, 7],
           [2, 5, 6],
           [2, 5, 7],
           [3, 4, 6],
           [3, 4, 7],
           [3, 5, 6],
           [3, 5, 7]])

    """

    arrays = [np.asarray(x) for x in arrays]
    dtype = arrays[0].dtype

    n = np.prod([x.size for x in arrays])
    if out is None:
        out = np.zeros([n, len(arrays)], dtype=dtype)

    m = n / arrays[0].size
    out[:,0] = np.repeat(arrays[0], m)
    if arrays[1:]:
        cartesian(arrays[1:], out=out[0:m,1:])
        for j in xrange(1, arrays[0].size):
            out[j*m:(j+1)*m,1:] = out[0:m,1:]
    return out

def get_dense_pos(heith, width, pw, stride = 1):
    
    # Compute patch halfs
    dx=dy=pw/2

    # Create a combination which corresponds to all the points of a dense
    # extraction        
    return cartesian( (range(dx, heith - dx, stride), range(dy, width -dy, stride) ) )

def extract_stats(patch):
    nchannels=patch.shape[2]
    r=[]
    for i in range(nchannels):
        m=np.mean(patch[:,:,i])
        s=np.std(patch[:,:,i])
        
        r.append(m)
        r.append(s)
    
    r=np.hstack(r)
    r.reshape(1,-1)
    return r


def extract_at_pos_average(img,pos,pw=15):
    #extract dense patches on the image at determined pos
    # pos should be an array N*2, the positions should be inside
    #the image so that the patch does notgo outside
    im=img.view(np.ndarray)
    ih=im.shape[0]
    iw=im.shape[1]
    
    if img.ndim==3:
        nchannels=im.shape[2]
    else:
        nchannels=1
    
    plist=[]
    
    dx=dy=pw/2
    for el in pos:
        x,y=el    
        
        sx=slice(x-dx,x+dx+1,None)
        sy=slice(y-dy,y+dy+1,None)
        
        t=im[sx,sy,...]
        tt=extract_stats(t)
        plist.append(tt)
            
            
    plist=np.vstack(plist)
    return plist


def spatialAverage(imshape,pos,pred,pw):
    h,w=imshape
    pos=np.vstack(pos)
    
    return _spatialAverage(h,w,pos.astype(np.int32),pred,int(pw))


def extract_at_pos(img,pos,pw=15):
    img=img.view(np.ndarray)
    pos=pos.astype(np.uint32)

    if img.ndim==2:
        return _extract_at_pos2D(img.astype(np.float64),pos,pw)
    else:
        return _extract_at_pos3D(img.astype(np.float64),pos,pw)
    
    
    
def extract_dense_average(img,pw=15,stride=1):
    #extract dense patches on the image
    
    im=img.view(np.ndarray)
    ih=im.shape[0]
    iw=im.shape[1]
    
    dx=dy=pw/2
    
    if img.ndim==3:
        nchannels=im.shape[2]
    else:
        nchannels=1
    
    plist=[]
    pos=[]
    for y in range(dy,iw-dy)[::stride]:
        for x in range(dx,ih-dx)[::stride]:
            
            
            
            sx=slice(x-dx,x+dx+1,None)
            sy=slice(y-dy,y+dy+1,None)
            
            t=im[sx,sy,...]
            tt=extract_stats(t)

            #print t.shape,'hehe'
            #pylab.imshow(t)
            #pylab.show()
            
            #t=t.reshape(-1,2*nchannels)
            
           
            plist.append(tt)
            pos.append([x,y])
            
            
    plist=np.vstack(plist)
    pos=np.vstack(pos)
    return plist,pos


def extract_dense(img,pw=15,stride=1):
    #extract dense patches on the image
    if img.ndim==2:
        return _extract_dense2D(img.astype(np.float64),pw,stride)
    else:
        return _extract_dense3D(img.astype(np.float64),pw,stride)



def extract_at_random(img,pw=15,N=100):
    #extract dense patches on the image at random positions
    im=img.view(np.ndarray)
    ih=im.shape[0]
    iw=im.shape[1]
    
    dx=dy=pw/2
    
    
    if img.ndim==3:
        nchannels=im.shape[2]
    else:
        nchannels=1
    
    y=np.random.randint(dy,iw-dy,N).reshape(N,1)
    x=np.random.randint(dx,ih-dx,N).reshape(N,1)
    
    pos=np.hstack((x,y))
    
    
    plist=[]
    for el in pos:
        x,y=el
        sx=slice(x-dx,x+dx+1,None)
        sy=slice(y-dy,y+dy+1,None)
        
        t=im[sx,sy,...]
        
        t=t.reshape(-1,pw*pw)
        plist.append(t)
        
            
    plist=np.vstack(plist)
    return plist,pos

def extract_at_random_average(img,pw=15,N=100):
    #extract dense patches on the image at random positions
    # 
    im=img.view(np.ndarray)
    ih=im.shape[0]
    iw=im.shape[1]
    
    dx=dy=pw/2
    
    
    if img.ndim==3:
        nchannels=im.shape[2]
    else:
        nchannels=1
    
    y=np.random.randint(dy,iw-dy,N).reshape(N,1)
    x=np.random.randint(dx,ih-dx,N).reshape(N,1)
    
    pos=np.hstack((x,y))
    
    
    plist=[]
    for el in pos:
        x,y=el
        sx=slice(x-dx,x+dx+1,None)
        sy=slice(y-dy,y+dy+1,None)
        
        t=im[sx,sy,...]
        tt=extract_stats(t)
        #t=t.reshape(-1,pw*pw)
        plist.append(tt)
        
            
    plist=np.vstack(plist)
    return plist,pos


    




if __name__=="__main__":
    #Small test
    import pylab
    
    pred=np.ones((4,5*5))
    
    pred[1,:]=2
    pred[2,:]=3
    pred[3,:]=4
    
    
#    print pred.reshape((10,10))
#    print 
#    pos=[(4,4),(2,7),(7,2),(7,7)]
#    
#    res=spatialAverage((10,10),pos,pred,pw=5)
#    print res
#    showCC(res)
    #pylab.show()
    
    
    
    pos=[(2,2),(2,7),(7,2),(7,7)]
    orig=spatialAverageOld((10,10),pos,pred,pw=5)
    
    #pylab.subplot(1,2,1)
    #pylab.title("original")
    #showCC(orig)
    
    print "original"
    print orig
 
    
    pred,pos=extract_dense(orig,pw=5)
    res=spatialAverage((10,10),pos,pred,pw=5)
   
    
    print "reconstructed"
    print res
    
    

    
import numpy as np
from matplotlib import pyplot as plt
def findCoordinate(iX,iY,Dict,shape):
#  print iX,iY,Dict,shape
  xx=round((iX-Dict['dec_centre'])/Dict['dec_delta']+shape[2]/2)
  yy=round((iY-Dict['ra_centre'])/Dict['ra_delta']+shape[1]/2)
#  print xx,yy
  return xx,yy 
def plotKiyoMap(data,Dict,fig,freq,vmax,vmin):
   """ 
   Make a 2D_plot of Kiyo's Map 
   Parameters
       ----------
       data: plotArray
       metaDic= data.meta
       fig: pyplot Figure object
       freq: an integer indicating the frequency slice
       vmax=maximun
       vmin=minmum
   Returns
       ----------
       axis object
   """
   ax=fig.add_subplot(1,1,1)
   Dec_Axis=np.arange(data.shape[2])-data.shape[2]/2
   Dec_Axis=Dec_Axis*Dict['dec_delta']+Dict['dec_centre']
   Ra_Axis=np.arange(data.shape[1])-data.shape[1]/2
   Ra_Axis=Ra_Axis*Dict['ra_delta']+Dict['ra_centre']
   ax1=ax.imshow(data[freq],\
             extent=[Dec_Axis[0],Dec_Axis[-1],Ra_Axis[0],Ra_Axis[-1]],\
              origin='lowerright',vmax=vmax,vmin=vmin)
   ax.set_title("Freq=%s"%repr(freq))
   cb = fig.colorbar(ax1)
   cb.set_label('T(K)')
   ax.set_ylabel("RA (deg)")
   ax.set_xlabel("DEC (deg)")
   ax.autoscale(enable=False)
   return ax


#-*- coding: utf-8 -*-
'''
Module for calculations used in data reduction and automatic algorithms.
'''

from numpy import *
from scipy.stats.mstats import mquantiles
from .mreduce import Reflectivity, MRDataset, DETECTOR_X_REGION
from .mpfit import mpfit
from .peakfinder import PeakFinder

__all__=['RefCollection', 'get_total_reflection', 'get_scaling', 'get_xpos', 'get_yregion']

class RefCollection(object):
  '''
  Representation of a collection of datasets used to calculate
  a full reflectivity pattern.
  If a list or MRDataset objects is given, the normalization and
  scaling is automatically calculated.
  '''

  def __init__(self, datasets=None):
    self.norm=[]
    self.refl=[]
    if datasets is not None:
      for ds in datasets:
        self.autoadd(ds)
      self.scale()

  def autoadd(self, ds):
    '''
    Add a dataset, automatically selecting normalization or
    reflectivity.
    '''
    norm=self.getNorm(ds)
    if norm:
      region=where(norm.Rraw>=(norm.Rraw.max()*0.1))[0]
      P0=len(norm.Rraw)-region[-1]
      PN=region[0]
    else:
      P0=0
      PN=0
    x_pos=get_xpos(ds)
    y_pos, y_width, ignore=get_yregion(ds)
    refl=Reflectivity(ds, normalization=norm, P0=P0, PN=PN,
                      x_pos=x_pos, y_pos=y_pos, y_width=y_width)
    if (refl.ai*180./pi)<0.05:
      self.norm.append(refl)
    else:
      self.refl.append(refl)

  def getNorm(self, ds):
    for norm in self.norm:
      if len(norm.Rraw)==len(ds.tof) and norm.lambda_center==ds.lambda_center:
        return norm
    return None

  def scale(self):
    '''
    Scale all reflectivities by total reflection or stitching to previous dataset.
    '''
    s1=get_total_reflection(self.refl[0])
    self.refl[0].rescale(s1)
    for i, refl1 in enumerate(self.refl[1:]):
      refl2=self.refl[i]
      scale, ignore, ignore=get_scaling(refl1, refl2)
      refl1.rescale(scale)


def get_total_reflection(refl, return_npoints=False):
  """
  Calculate the intensity of the total reflection plateau in one dataset.
  Starting from low Q points it searches for a drop in intensity to 
  locate the andge and than returns the weighted mean.
  
  :param refl: Reflectivity object
  
  :returns: scaling, (number of points used for weighted mean)
  """
  if not type(refl) is Reflectivity:
    raise ValueError, "'refl' needs to be a Reflectiviy object"
  last=refl.options['PN']
  first=len(refl.R)-refl.options['P0']
  R=refl.R[last:first]
  dR=refl.dR[last:first][R>0]
  R=R[R>0]
  wmean=1.
  # Start from low Q and search for the critical edge
  for i in range(len(R)-5, 0,-1):
    wmean=(R[i:]/dR[i:]).sum()/(1./dR[i:]).sum()
    Ri=R[i-1]
    if Ri<wmean*0.9:
      break
  if return_npoints:
    return 1./wmean, i
  else:
    return 1./wmean

def get_scaling(refl1, refl2, add_points=0):
  """
  Calculate the scaling factor needed to stich one dataset to another.
  
  :param refl1/2: Reflectivity objects
  
  :returns: scaling, array of fitted x and y
  """
  if not (type(refl1) is Reflectivity and type(refl2) is Reflectivity):
    raise ValueError, "'refl1' and 'refl2' need to be Reflectiviy objects"
  last=refl1.options['PN']
  first=len(refl1.R)-refl1.options['P0']
  R1=refl1.R[last:first]
  dR1=refl1.dR[last:first][R1>0]
  Q1=refl1.Q[last:first][R1>0]
  R1=R1[R1>0]
  last=refl2.options['PN']
  first=len(refl2.R)-refl2.options['P0']
  R2=refl2.R[last:first]
  dR2=refl2.dR[last:first][R2>0]
  Q2=refl2.Q[last:first][R2>0]
  R2=R2[R2>0]
  reg1=max(0, where(Q1<=Q2.max())[0][0]-add_points)
  reg2=where(Q2>=Q1.min())[0][-1]+1+add_points
  # try to match both datasets by fitting a polynomial to the overlapping region
  return _refineOverlap(Q1[reg1:], R1[reg1:], dR1[reg1:],
                        Q2[:reg2], R2[:reg2], dR2[:reg2])

def get_xpos(data, dangle0_overwrite=None, direct_pixel_overwrite=-1,
             snr=5, min_width=2, max_width=20, ridge_length=15, return_pf=False, refine=True):
  """
  Calculate the specular or direct beam peak position from data x-projection.
  
  :param data: MRDataset object
  
  :returns: x_center, (Peakfinder)
  """
  if type(data) is not MRDataset:
    raise ValueError, "'data' needs to be a MRDataset object"
  xproj=data.xdata
  # calculate approximate peak position
  if dangle0_overwrite is not None:
    tth_bank=(data.dangle-dangle0_overwrite)*pi/180.
  else:
    tth_bank=(data.dangle-data.dangle0)*pi/180.
  ai=data.sangle*pi/180.
  if direct_pixel_overwrite>=0:
    dp=direct_pixel_overwrite
  else:
    dp=data.dpix
  rad_per_pixel=data.det_size_x/data.dist_sam_det/data.xydata.shape[1]
  pix_position=dp-(ai*2-tth_bank)/rad_per_pixel

  # locate peaks using CWT peak finder algorithm
  pf=PeakFinder(arange(DETECTOR_X_REGION[1]-DETECTOR_X_REGION[0]),
                xproj[DETECTOR_X_REGION[0]:DETECTOR_X_REGION[1]])
  # Signal to noise ratio, minimum width, maximum width, algorithm ridge parameter
  peaks=pf.get_peaks(snr=snr, min_width=min_width, max_width=max_width,
                     ridge_length=ridge_length)
  try:
    x_peaks=array([p[0] for p in peaks])+DETECTOR_X_REGION[0]
    delta_pix=abs(pix_position-x_peaks)
    x_peak=x_peaks[delta_pix==delta_pix.min()][0]
  except:
    x_peak=pix_position
  if refine:
    # refine position with gaussian
    x_peak=refine_gauss(xproj, x_peak, 6.)
  if return_pf:
    return float(x_peak), pf
  else:
    return float(x_peak)

def get_yregion(data):
  """
  Calculate the beam y region from data y-projection.
  
  :param data: MRDataset object
  
  :returns: y_center, y_width, y_bg
  """
  yproj=data.ydata
  if type(data) is not MRDataset:
    raise ValueError, "'data' needs to be a MRDataset object"
  # find the central peak reagion with intensities larger than 10% of maximum
  y_bg=mquantiles(yproj, 0.5)[0]
  y_peak_region=where((yproj-y_bg)>yproj.max()/10.)[0]
  yregion=(y_peak_region[0], y_peak_region[-1])
  return (yregion[0]+yregion[1]+1.)/2., yregion[1]+1.-yregion[0], y_bg


def refine_gauss(data, pos, width):
  '''
    Fit a gaussian function to a given dataset and return the x0 position.
  '''
  p0=[data[int(pos)], pos, width]
  parinfo=[{'value':0., 'fixed':0, 'limited':[0, 0],
            'limits':[0., 0.]} for ignore in range(3)]
  parinfo[0]['limited']=[True, False]
  parinfo[0]['limits']=[0., None]
  parinfo[2]['fixed']=True
  res=mpfit(_gauss_residuals, p0, functkw={'data':data}, nprint=0, parinfo=parinfo)
  parinfo[2]['fixed']=False
  parinfo[2]['limited']=[True, True]
  parinfo[2]['limits']=[1., 4.*width]
  p0=[data[int(res.params[1])], res.params[1], width]
  res=mpfit(_gauss_residuals, p0, functkw={'data':data}, nprint=0, parinfo=parinfo)
  return res.params[1]

######## helper functions ###############
def _gauss_residuals(p, fjac=None, data=None, width=1):
  '''
    Gaussian of I0, x0 and sigma parameters minus the data.
  '''
  xdata=arange(data.shape[0])
  I0=p[0]
  x0=p[1]
  sigma=p[2]/5.
  G=exp(-0.5*((xdata-x0)/sigma)**2)
  return 0, data-I0*G

def _refineOverlap(x1, y1, dy1, x2, y2, dy2):
  '''
    Refine a polynomial to the logarithm of two datasets while
    scaling the first dataset as well. Return the resulting
    scaling parameter and the refined function for plotting.
    
    :returns: scaling, array of fitted x and y
  '''
  result=mpfit(_overlapResiduals, [1., 0.,-40., 0.],
               functkw=dict(
                            x1=x1, y1=y1, dy1=dy1,
                            x2=x2, y2=y2, dy2=dy2
                            ),
               nprint=0)
  xfit=hstack([x1, x2])
  xfit.sort()
  yscale, a, b, c=result.params
  yfit=10**(a*xfit**2+b*xfit+c)
  return yscale, xfit, yfit

def _overlapResiduals(p, fjac=None, x1=None, y1=None, dy1=None,
                                    x2=None, y2=None, dy2=None):
  yscale, a, b, c=p
  part1=(log10(yscale*y1)-a*x1**2-b*x1-c)/(dy1/y1)
  part2=(log10(y2)-a*x2**2-b*x2-c)/(dy2/y2)
  return 0, hstack([part1, part2])


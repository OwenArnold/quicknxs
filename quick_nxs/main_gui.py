#-*- coding: utf-8 -*-
'''
  Module including main GUI class with all signal handling and plot creation.
'''

import os, sys
from glob import glob
from numpy import where, pi, newaxis, arange, exp, log10, array, hstack
from scipy.stats.mstats import mquantiles
from cPickle import load, dump
from matplotlib.lines import Line2D
from PyQt4 import QtGui, QtCore, QtWebKit

from .version import str_version
from .main_window import Ui_MainWindow
from .gui_utils import ReduceDialog, DelayedTrigger
from .error_handling import ErrorHandler
from .mreduce import NXSData, Reflectivity, OffSpecular, DETECTOR_X_REGION, RAD_PER_PIX
from .mpfit import mpfit
from .peakfinder import PeakFinder

BASE_FOLDER='/SNS/REF_M'
BASE_SEARCH='*/data/REF_M_%s_'

class MainGUI(QtGui.QMainWindow):
  '''
    The program top level window with all direct event handling.
  '''
  active_folder=BASE_FOLDER
  active_file=u''
  _active_data=None
  ref_list_channels=[] #: Store which channels are available for stored reflectivities
  _refl=None #: Reflectivity of the active dataset
  ref_norm={} #: Store normalization data with extraction information
  auto_change_active=False
  reduction_list=[] #: Store information and data of reflectivities from different files
  color=None
  open_plots=[] #: to keep non modal dialogs open when their caller is destroyed
  channels=[] #: Available channels of the active dataset
  active_channel='x' #: Selected channel for the overview and projection plots
  _control_down=False

  ##### for IPython mode, keep namespace up to date ######
  @property
  def active_data(self): return self._active_data
  @active_data.setter
  def active_data(self, value):
    if self.ipython:
      self.ipython.namespace['data']=value
    self._active_data=value
  @property
  def refl(self): return self._refl
  @refl.setter
  def refl(self, value):
    if self.ipython:
      self.ipython.namespace['refl']=value
    self._refl=value
  ##### for IPython mode, keep namespace up to date ######

  def __init__(self, argv=[]):
    QtGui.QMainWindow.__init__(self)

    self.auto_change_active=True
    self.ui=Ui_MainWindow()
    self.ui.setupUi(self)
    self.setWindowTitle(u'QuickNXS   %s'%str_version)
    self.eventProgress=QtGui.QProgressBar(self.ui.statusbar)
    self.eventProgress.setMinimumSize(20, 14)
    self.eventProgress.setMaximumSize(80, 100)
    self.ui.statusbar.addPermanentWidget(self.eventProgress)
    # perhaps use this in the future?
    self.ui.xprojQuantiles.hide()
    self.ui.xprojUseQuantiles.hide()
    self.ui.label_16.hide()

    self.toggleHide()
    self.readSettings()
    self.ui.plotTab.setCurrentIndex(0)
    # start a separate thread for delayed actions
    self.trigger=DelayedTrigger()
    self.trigger.activate.connect(self.processDelayedTrigger)
    self.trigger.start()
    self.ui.bgCenter.setValue((DETECTOR_X_REGION[0]+100.)/2.)
    self.ui.bgWidth.setValue((100-DETECTOR_X_REGION[0]))

    self._path_watcher=QtCore.QFileSystemWatcher([self.active_folder], self)
    self._path_watcher.directoryChanged.connect(self.folderModified)
    self.connect_plot_events()
    # watch folder for changes
    self.auto_change_active=False

    # open file after GUI is shown
    if '-ipython' in argv:
      argv.remove('-ipython')
      from .ipython_widget import IPythonConsoleQtWidget
      self.ipython=IPythonConsoleQtWidget(self)
      self.ui.plotTab.addTab(self.ipython, 'IPython')
    else:
      # catch python errors with error handling from stderr
      sys.stderr=ErrorHandler(self)
      self.ipython=None
    if len(argv)>0:
      # delay action to be run within event loop, this allows the error handling to work
      if argv[0][-4:]=='.nxs':
        if len(argv)==1:
          self.trigger('fileOpen', argv[0])
        else:
          self.trigger('automaticExtraction', argv)
      if argv[0][-4:]=='.dat':
        self.trigger('loadExtraction', argv[0])
    else:
      self.ui.numberSearchEntry.setFocus()

  def processDelayedTrigger(self, item, args):
    '''
      Calls private method after delay action was
      triggered.
    '''
    getattr(self, str(item))(*args)

  def connect_plot_events(self):
    '''
      Connect matplotlib mouse events.
    '''
    for plot in [self.ui.xy_pp, self.ui.xy_mp, self.ui.xy_pm, self.ui.xy_mm,
           self.ui.xtof_pp, self.ui.xtof_mp, self.ui.xtof_pm, self.ui.xtof_mm,
           self.ui.xy_overview, self.ui.xtof_overview,
           self.ui.x_project, self.ui.y_project, self.ui.refl]:
      plot.canvas.mpl_connect('motion_notify_event', self.plotMouseEvent)
    self.ui.x_project.canvas.mpl_connect('motion_notify_event', self.plotPickX)
    self.ui.x_project.canvas.mpl_connect('button_press_event', self.plotPickX)
    self.ui.y_project.canvas.mpl_connect('motion_notify_event', self.plotPickY)
    self.ui.y_project.canvas.mpl_connect('button_press_event', self.plotPickY)
    self.ui.refl.canvas.mpl_connect('scroll_event', self.scaleOnPlot)
    self.ui.xy_overview.canvas.mpl_connect('button_press_event', self.plotPickXY)
    self.ui.xy_overview.canvas.mpl_connect('motion_notify_event', self.plotPickXY)
    self.ui.xtof_overview.canvas.mpl_connect('button_press_event', self.plotPickXToF)
    self.ui.xtof_overview.canvas.mpl_connect('motion_notify_event', self.plotPickXToF)

  def fileOpen(self, filename, do_plot=True):
    '''
      Open a new datafile and plot the data.
    '''
    folder, base=os.path.split(filename)
    if folder!=self.active_folder:
      self.onPathChanged(base, folder)
    self.active_file=base
    data=NXSData(filename,
                bin_type=str(self.ui.eventBinMode.currentText()),
                bins=self.ui.eventTofBins.value(),
                callback=self.updateEventReadout)
    if data is None:
      self.ui.currentChannel.setText(u'<b>!!!NO DATA IN FILE %s!!!</b>'%base)
      return
    self.channels=data.keys()

    desiredChannel=self.ui.selectedChannel.currentText().split('/')
    self.active_channel=self.channels[0]
    for channel in self.channels:
      if channel in desiredChannel:
        self.active_channel=channel
        break
    self.active_data=data

    self.updateLabels()
    self.calcReflParams()
    if do_plot:
      self.plotActiveTab()
      self.plot_projections()
    self.last_mtime=os.path.getmtime(filename)
    self.ui.statusbar.showMessage(u"%s loaded"%(filename), 1500)

####### Plot related methods

  def plotActiveTab(self):
    '''
      Select the appropriate function to plot all visible images.
    '''
    if self.auto_change_active or not self.active_data:
      return
    color=str(self.ui.color_selector.currentText())
    if color!=self.color and self.color is not None:
      self.color=color
      plots=[self.ui.xy_pp, self.ui.xy_mp, self.ui.xy_pm, self.ui.xy_mm,
             self.ui.xtof_pp, self.ui.xtof_mp, self.ui.xtof_pm, self.ui.xtof_mm,
             self.ui.xy_overview, self.ui.xtof_overview]
      for plot in plots:
        plot.clear_fig()
    elif self.color is None:
      self.color=color
    if self.ui.plotTab.currentIndex()==0:
      self.plot_overview()
    if self.ui.plotTab.currentIndex()==1:
      self.plot_xy()
    if self.ui.plotTab.currentIndex()==2:
      self.plot_xtof()
    if self.ui.plotTab.currentIndex()==3:
      self.plot_offspec()
    if self.ui.plotTab.currentIndex()==4:
      self.update_daslog()

  def plot_overview(self):
    '''
      X vs. Y and X vs. Tof for main channel.
    '''
    data=self.active_data[self.active_channel]
    xy=data.xydata
    xtof=data.xtofdata
    ref_norm=self.getNorm()
    if self.ui.normalizeXTof.isChecked() and ref_norm is not None:
      ref_norm=ref_norm.Rraw
      # normalize ToF dataset for wavelength distribution
      ref_norm=where(ref_norm>0., ref_norm, 1.)
      xtof=xtof.astype(float)/ref_norm[newaxis, :]
    xy_imin=xy[xy>0].min()
    xy_imax=xy.max()
    tof_imin=xtof[xtof>0].min()
    tof_imax=xtof.max()
    # XY plot
    if self.ui.tthPhi.isChecked():
      phi_range=xy.shape[0]*RAD_PER_PIX*180./pi
      tth_range=xy.shape[1]*RAD_PER_PIX*180./pi
      phi0=self.ui.refYPos.value()*RAD_PER_PIX*180./pi
      tth0=(data.dangle-data.dangle0)-(304-data.dpix)*RAD_PER_PIX*180./pi
      self.ui.xy_overview.clear()

      self.ui.xy_overview.imshow(xy, log=self.ui.logarithmic_colorscale.isChecked(),
                               aspect='auto', cmap=self.color,
                               extent=[tth_range+tth0, tth0, phi0-phi_range, phi0])
      self.ui.xy_overview.set_xlabel(u'2θ [°]')
      self.ui.xy_overview.set_ylabel(u'φ [°]')
      self.ui.xy_overview.cplot.set_clim([xy_imin, xy_imax])
    else:
      self.ui.xy_overview.imshow(xy, log=self.ui.logarithmic_colorscale.isChecked(),
                               aspect='auto', cmap=self.color)
      self.ui.xy_overview.set_xlabel(u'x [pix]')
      self.ui.xy_overview.set_ylabel(u'y [pix]')
      self.ui.xy_overview.cplot.set_clim([xy_imin, xy_imax])
    # XToF plot
    if self.ui.xLamda.isChecked():
      self.ui.xtof_overview.imshow(xtof[::-1], log=self.ui.logarithmic_colorscale.isChecked(),
                                   aspect='auto', cmap=self.color,
                                   extent=[data.lamda[0], data.lamda[-1], 0, data.x.shape[0]-1])
      self.ui.xtof_overview.set_xlabel(u'λ [Å]')
    else:
      self.ui.xtof_overview.imshow(xtof[::-1], log=self.ui.logarithmic_colorscale.isChecked(),
                                   aspect='auto', cmap=self.color,
                                   extent=[data.tof[0]*1e-3, data.tof[-1]*1e-3, 0, data.x.shape[0]-1])
      self.ui.xtof_overview.set_xlabel(u'ToF [ms]')
    self.ui.xtof_overview.set_ylabel(u'x [pix]')
    self.ui.xtof_overview.cplot.set_clim([tof_imin, tof_imax])
#    if self.tline is None:
#      self.tline=Line2D([20, 20], [0, 300], color='red')
#      self.ui.xy_overview.canvas.ax.add_line(self.tline)
    if self.ui.show_colorbars.isChecked() and self.ui.xy_overview.cbar is None:
      self.ui.xy_overview.cbar=self.ui.xy_overview.canvas.fig.colorbar(self.ui.xy_overview.cplot)
      self.ui.xtof_overview.cbar=self.ui.xtof_overview.canvas.fig.colorbar(self.ui.xtof_overview.cplot)
    self.ui.xy_overview.draw()
    self.ui.xtof_overview.draw()

  def plot_xy(self):
    '''
      X vs. Y plots for all channels.
    '''
    plots=[self.ui.xy_pp, self.ui.xy_mm, self.ui.xy_pm, self.ui.xy_mp]
    for i in range(len(self.active_data), 4):
      if plots[i].cplot is not None:
        plots[i].clear()
        plots[i].draw()
    imin=1e20
    imax=1e-20
    xynormed=[]
    for dataset in self.active_data:
      d=dataset.xydata/dataset.proton_charge
      xynormed.append(d)
      imin=min(imin, d[d>0].min())
      imax=max(imax, d.max())

    if len(xynormed)>1:
      self.ui.frame_xy_mm.show()
      if len(xynormed)==4:
        self.ui.frame_xy_sf.show()
      else:
        self.ui.frame_xy_sf.hide()
    else:
      self.ui.frame_xy_mm.hide()
      self.ui.frame_xy_sf.hide()

    for i, datai in enumerate(xynormed):
      if self.ui.tthPhi.isChecked():
        plots[i].clear()
        phi_range=datai.shape[0]*RAD_PER_PIX*180./pi
        tth_range=datai.shape[1]*RAD_PER_PIX*180./pi
        phi0=self.ui.refYPos.value()*RAD_PER_PIX*180./pi
        tth0=(dataset.dangle-dataset.dangle0)-(304-dataset.dpix)*RAD_PER_PIX*180./pi

        plots[i].imshow(datai, log=self.ui.logarithmic_colorscale.isChecked(), imin=imin, imax=imax,
                             aspect='auto', cmap=self.color,
                             extent=[tth_range+tth0, tth0, phi0-phi_range, phi0])
        plots[i].set_xlabel(u'2θ [°]')
        plots[i].set_ylabel(u'φ [°]')
      else:
        plots[i].imshow(datai, log=self.ui.logarithmic_colorscale.isChecked(), imin=imin, imax=imax,
                             aspect='auto', cmap=self.color)
        plots[i].set_xlabel(u'x [pix]')
        plots[i].set_ylabel(u'y [pix]')
      plots[i].set_title(self.channels[i])
      if plots[i].cplot is not None:
        plots[i].cplot.set_clim([imin, imax])
      if plots[i].cplot is not None and self.ui.show_colorbars.isChecked() and plots[i].cbar is None:
        plots[i].cbar=plots[i].canvas.fig.colorbar(plots[i].cplot)
      plots[i].draw()

  def plot_xtof(self):
    '''
      X vs. ToF plots for all channels.
    '''
    imin=1e20
    imax=1e-20
    xtofnormed=[]
    ref_norm=self.getNorm()
    if ref_norm is not None:
      ref_norm=ref_norm.Rraw
      ref_norm=where(ref_norm>0, ref_norm, 1.)

    for dataset in self.active_data:
      d=dataset.xtofdata/dataset.proton_charge
      if self.ui.normalizeXTof.isChecked() and ref_norm is not None:
        # normalize all datasets for wavelength distribution
        d=d/ref_norm[newaxis, :]
      xtofnormed.append(d)
      imin=min(imin, d[d>0].min())
      imax=max(imax, d.max())
    lamda=self.active_data[self.active_channel].lamda
    tof=self.active_data[self.active_channel].tof

    plots=[self.ui.xtof_pp, self.ui.xtof_mm, self.ui.xtof_pm, self.ui.xtof_mp]
    for i in range(len(self.active_data), 4):
      if plots[i].cplot is not None:
        plots[i].clear()
        plots[i].draw()

    if len(xtofnormed)>1:
      self.ui.frame_xtof_mm.show()
      if len(xtofnormed)==4:
        self.ui.frame_xtof_sf.show()
      else:
        self.ui.frame_xtof_sf.hide()
    else:
      self.ui.frame_xtof_mm.hide()
      self.ui.frame_xtof_sf.hide()
    for i, datai in enumerate(xtofnormed):
      if self.ui.xLamda.isChecked():
        plots[i].imshow(datai[::-1], log=self.ui.logarithmic_colorscale.isChecked(), imin=imin, imax=imax,
                             aspect='auto', cmap=self.color, extent=[lamda[0], lamda[-1], 0, datai.shape[0]-1])
        plots[i].set_xlabel(u'λ [Å]')
      else:
        plots[i].imshow(datai[::-1], log=self.ui.logarithmic_colorscale.isChecked(), imin=imin, imax=imax,
                             aspect='auto', cmap=self.color, extent=[tof[0]*1e-3, tof[-1]*1e-3, 0, datai.shape[0]-1])
        plots[i].set_xlabel(u'ToF [ms]')
      plots[i].set_title(self.channels[i])
      plots[i].set_ylabel(u'x [pix]')
      if plots[i].cplot is not None:
        plots[i].cplot.set_clim([imin, imax])
      if plots[i].cplot is not None and self.ui.show_colorbars.isChecked() and plots[i].cbar is None:
        plots[i].cbar=plots[i].canvas.fig.colorbar(plots[i].cplot)
      plots[i].draw()

  def plot_projections(self, preserve_lim=False):
    self.trigger('_plot_projections', preserve_lim)

  def _plot_projections(self, preserve_lim):
    '''
      Create projections of the data on the x and y axes.
      The x-projection can also be done be means of quantile calculation,
      which means that the ToF intensities are calculation which are
      exceeded by a certain number of points. This can be helpful to better
      separate the specular reflection from bragg-sheets
    '''
    data=self.active_data[self.active_channel]
    if self.ui.xprojUseQuantiles.isChecked():
      d2=data.xtofdata
      xproj=mquantiles(d2, self.ui.xprojQuantiles.value()/100., axis=1)
    else:
      xproj=data.xdata
    yproj=data.ydata

    x_peak=self.ui.refXPos.value()
    x_width=self.ui.refXWidth.value()
    y_pos=self.ui.refYPos.value()
    y_width=self.ui.refYWidth.value()
    bg_pos=self.ui.bgCenter.value()
    bg_width=self.ui.bgWidth.value()

    if preserve_lim:
      xview=self.ui.x_project.canvas.ax.axis()
      yview=self.ui.y_project.canvas.ax.axis()
    xxlim=(0, len(xproj)-1)
    xylim=(xproj[xproj>0].min(), xproj.max()*2)
    yxlim=(0, len(yproj)-1)
    yylim=(yproj[yproj>0].min(), yproj.max()*2)
    self.ui.x_project.clear()
    self.ui.y_project.clear()

    self.ui.x_project.plot(xproj, color='blue')[0]
    self.ui.x_project.set_xlabel(u'x [pix]')
    self.ui.x_project.set_ylabel(u'I$_{max}$')
    xpos=Line2D([x_peak, x_peak], [xylim[0], xylim[1]], color='black')
    xleft=Line2D([x_peak-x_width/2., x_peak-x_width/2.], [xylim[0], xylim[1]], color='red')
    xright=Line2D([x_peak+x_width/2., x_peak+x_width/2.], [xylim[0], xylim[1]], color='red')
    self.ui.x_project.canvas.ax.add_line(xpos)
    self.ui.x_project.canvas.ax.add_line(xleft)
    self.ui.x_project.canvas.ax.add_line(xright)
    xleft_bg=Line2D([bg_pos-bg_width/2., bg_pos-bg_width/2.], [xylim[0], xylim[1]], color='green')
    xright_bg=Line2D([bg_pos+bg_width/2., bg_pos+bg_width/2.], [xylim[0], xylim[1]], color='green')
    self.ui.x_project.canvas.ax.add_line(xleft_bg)
    self.ui.x_project.canvas.ax.add_line(xright_bg)

    self.ui.y_project.plot(yproj, color='blue')[0]
    self.ui.y_project.set_xlabel(u'y [pix]')
    self.ui.y_project.set_ylabel(u'I$_{max}$')
    yreg_left=Line2D([y_pos-y_width/2., y_pos-y_width/2.], [yylim[0], yylim[1]], color='red')
    yreg_right=Line2D([y_pos+y_width/2., y_pos+y_width/2.], [yylim[0], yylim[1]], color='red')
    self.ui.y_project.canvas.ax.add_line(yreg_left)
    self.ui.y_project.canvas.ax.add_line(yreg_right)
    y_bg=Line2D([0, yxlim[1]], [self.y_bg, self.y_bg], color='green')
    self.ui.y_project.canvas.ax.add_line(y_bg)
    if preserve_lim:
      self.ui.x_project.canvas.ax.axis(xview)
      self.ui.y_project.canvas.ax.axis(yview)
    if self.ui.logarithmic_y.isChecked():
      self.ui.x_project.set_yscale('log')
      self.ui.y_project.set_yscale('log')
    else:
      self.ui.x_project.set_yscale('linear')
      self.ui.y_project.set_yscale('linear')
    self.ui.x_project.canvas.ax.set_xlim(*xxlim)
    self.ui.x_project.canvas.ax.set_ylim(*xylim)
    self.ui.y_project.canvas.ax.set_xlim(*yxlim)
    self.ui.y_project.canvas.ax.set_ylim(*yylim)

    self.ui.x_project.draw()
    self.ui.y_project.draw()
    self.proj_lines=(xleft, xpos, xright, xleft_bg, xright_bg, yreg_left, yreg_right)
    self.plot_refl()

  def calc_refl(self):
    if self.active_data is None:
      return False
    data=self.active_data[self.active_channel]
    if self.ui.directPixelOverwrite.value()>=0:
      dpix=self.ui.directPixelOverwrite.value()
    else:
      dpix=None
    try:
      tth=data.dangle-float(self.ui.dangle0Overwrite.text())
    except ValueError:
      tth=None
    number=str(self.active_data.number)
    options=dict(
                x_pos=self.ui.refXPos.value(),
                x_width=self.ui.refXWidth.value(),
                y_pos=self.ui.refYPos.value(),
                y_width=self.ui.refYWidth.value(),
                bg_pos=self.ui.bgCenter.value(),
                bg_width=self.ui.bgWidth.value(),
                scale=10**self.ui.refScale.value(),
                extract_fan=self.ui.fanReflectivity.isChecked(),
                P0=self.ui.rangeStart.value(),
                PN=self.ui.rangeEnd.value(),
                number=number,
                tth=tth,
                dpix=dpix,
                bg_tof_constant=self.ui.bgToFConstant.isChecked(),
                normalization=self.getNorm(),
                  )

    self.refl=Reflectivity(data, **options)
    self.ui.datasetAi.setText(u"%.3f°"%(self.refl.ai*180./pi))
    self.ui.datasetROI.setText(u"%.4g"%(self.refl.Iraw.sum()))
    return True

  def plot_refl(self, preserve_lim=False):
    '''
      Calculate and display the reflectivity from the current dataset
      and any dataset stored. Intensities from direct beam
      measurements can be used for normalization.
    '''
    if not self.calc_refl():
      return
    options=self.refl.options
    P0=len(self.refl.Q)-self.ui.rangeStart.value()
    PN=self.ui.rangeEnd.value()

    if preserve_lim:
      view=self.ui.refl.canvas.ax.axis()

    self.ui.refl.clear()
    if options['normalization']:
      ymin=1e50
      ymax=1e-50
      for refli in self.reduction_list:
        #self.ui.refl.semilogy(x, y/self.ref_norm, label=str(settings['index']))
        P0i=len(refli.Q)-refli.options['P0']
        PNi=refli.options['PN']
        ynormed=refli.R[PNi:P0i]
        try:
          ymin=min(ymin, ynormed[ynormed>0].min())
        except ValueError:
          pass
        ymax=max(ymax, ynormed.max())
        self.ui.refl.errorbar(refli.Q[PNi:P0i], ynormed,
                              yerr=refli.dR[PNi:P0i], label=str(refli.options['number']))
      ynormed=self.refl.R[PN:P0]
      try:
        ymin=min(ymin, ynormed[ynormed>0].min())
      except ValueError:
        pass
      ymax=max(ymax, ynormed.max())
      self.ui.refl.errorbar(self.refl.Q[PN:P0], ynormed,
                            yerr=self.refl.dR[PN:P0], label=options['number'])
      self.ui.refl.set_ylabel(u'I')
      self.ui.refl.canvas.ax.set_ylim((ymin*0.9, ymax*1.1))
      self.ui.refl.set_xlabel(u'Q$_z$ [Å⁻¹]')
    else:
      ymin=min(self.refl.BG[self.refl.BG>0].min(), self.refl.I[self.refl.I>0].min())
      ymax=max(self.refl.BG.max(), self.refl.I.max())
      self.ui.refl.errorbar(self.refl.lamda, self.refl.I, yerr=self.refl.dI, label='I-'+options['number'])
      self.ui.refl.errorbar(self.refl.lamda, self.refl.BG, yerr=self.refl.dBG, label='BG-'+options['number'])
      self.ui.refl.set_ylabel(u'I')
      self.ui.refl.canvas.ax.set_ylim((ymin*0.9, ymax*1.1))
      self.ui.refl.set_xlabel(u'λ [Å]')
    if self.ui.logarithmic_y.isChecked():
      self.ui.refl.set_yscale('log')
    else:
      self.ui.refl.set_yscale('linear')
    self.ui.refl.legend()
    if preserve_lim:
      self.ui.refl.canvas.ax.axis(view)
    self.ui.refl.draw()

  def plot_offspec(self):
    '''
      Create an offspecular plot for all channels of the datasets in the
      reduction list. The user can define upper and lower bounds for the 
      plotted intensity and select the coordinates to be ither kiz-kfz vs. Qz,
      Qx vs. Qz or kiz vs. kfz.
    '''
    plots=[self.ui.offspec_pp, self.ui.offspec_mm,
           self.ui.offspec_pm, self.ui.offspec_mp]
    for plot in plots:
        plot.clear()
    for i in range(len(self.active_data), 4):
      if plots[i].cplot is not None:
        plots[i].draw()
    Imin=10**self.ui.offspecImin.value()
    Imax=10**self.ui.offspecImax.value()
    Qzmax=0.01
    for item in self.reduction_list:
      fname=item.origin[0]
      data_all=NXSData(fname, **item.read_options)
      for i, channel in enumerate(self.ref_list_channels):
        plot=plots[i]
        selected_data=data_all[channel]
        offspec=OffSpecular(selected_data, **item.options)
        P0=len(selected_data.tof)-item.options['P0']
        PN=item.options['PN']
        Qzmax=max(offspec.Qz[int(item.options['x_pos']), PN:P0].max(), Qzmax)
        ki_z, kf_z, Qx, Qz, S=offspec.ki_z, offspec.kf_z, offspec.Qx, offspec.Qz, offspec.S
        if self.ui.kizmkfzVSqz.isChecked():
          plot.pcolormesh((ki_z-kf_z)[:, PN:P0],
                                        Qz[:, PN:P0], S[:, PN:P0], log=True,
                                        imin=Imin, imax=Imax, cmap=self.color,
                                        shading='gouraud')
        elif self.ui.qxVSqz.isChecked():
          plot.pcolormesh(Qx[:, PN:P0],
                                        Qz[:, PN:P0], S[:, PN:P0], log=True,
                                        imin=Imin, imax=Imax, cmap=self.color,
                                        shading='gouraud')
        else:
          plot.pcolormesh(ki_z[:, PN:P0],
                                        kf_z[:, PN:P0], S[:, PN:P0], log=True,
                                        imin=Imin, imax=Imax, cmap=self.color,
                                        shading='gouraud')
    for i, channel in enumerate(self.ref_list_channels):
      plot=plots[i]
      if self.ui.kizmkfzVSqz.isChecked():
        plot.canvas.ax.set_xlim([-0.03, 0.03])
        plot.canvas.ax.set_ylim([0., Qzmax])
        plot.set_xlabel(u'k$_{i,z}$-k$_{f,z}$ [Å⁻¹]')
        plot.set_ylabel(u'Q$_z$ [Å⁻¹]')
      elif self.ui.qxVSqz.isChecked():
        plot.canvas.ax.set_xlim([-0.001, 0.001])
        plot.canvas.ax.set_ylim([0., Qzmax])
        plot.set_xlabel(u'Q$_x$ [Å⁻¹]')
        plot.set_ylabel(u'Q$_z$ [Å⁻¹]')
      else:
        plot.canvas.ax.set_xlim([0., Qzmax/2.])
        plot.canvas.ax.set_ylim([0., Qzmax/2.])
        plot.set_xlabel(u'k$_{i,z}$ [Å⁻¹]')
        plot.set_ylabel(u'k$_{f,z}$ [Å⁻¹]')
      plot.set_title(channel)
      if plot.cplot is not None:
        plot.cplot.set_clim([Imin, Imax])
        if self.ui.show_colorbars.isChecked() and plots[i].cbar is None:
          plots[i].cbar=plots[i].canvas.fig.colorbar(plots[i].cplot)
      plot.draw()

  def update_daslog(self):
    '''
      Write parameters from all file daslogs to the tables in the 
      daslog tab.
    '''
    table=self.ui.daslogTableBox
    table.setRowCount(0)
    table.setColumnCount(len(self.channels)+2)
    table.setHorizontalHeaderLabels(['Name']+self.channels+['Unit'])
    for j, key in enumerate(sorted(self.active_data[0].logs.keys())):
      table.insertRow(j)
      table.setItem(j, 0, QtGui.QTableWidgetItem(key))
      table.setItem(j, len(self.channels)+1,
                    QtGui.QTableWidgetItem(self.active_data[0].log_units[key]))
      for i, _channel, data in self.active_data.numitems():
        table.setItem(j, i+1, QtGui.QTableWidgetItem(str(data.logs[key])))
    table.resizeColumnsToContents()

###### GUI actions

  def fileOpenDialog(self):
    '''
      Show a dialog to open a new file.
    '''
    if self.ui.histogramActive.isChecked():
      filter_=u'Histo Nexus (*histo.nxs);;All (*.*)'
    else:
      filter_=u'Event Nexus (*event.nxs);;All (*.*)'
    filenames=QtGui.QFileDialog.getOpenFileNames(self, u'Open NXS file...',
                                               directory=self.active_folder,
                                               filter=filter_)
    if filenames:
      filenames=map(unicode, filenames)
      if len(filenames)==1:
        self.fileOpen(filenames[0])
      else:
        self.automaticExtraction(filenames)

  def fileOpenList(self):
    '''
      Called when a new file is selected from the file list.
    '''
    item=self.ui.file_list.currentItem()
    name=unicode(item.text())
    try:
      mtime=os.path.getmtime(os.path.join(self.active_folder, self.active_file))
    except OSError:
      mtime=1e10
    if name!=self.active_file or mtime>self.last_mtime:
      # only reload if filename was actually changed or file was modifiede
      self.fileOpen(os.path.join(self.active_folder, name))

  def openByNumber(self):
    '''
      Search the data folders for a specific file number and open it.
    '''
    number=self.ui.numberSearchEntry.text()
    self.ui.statusbar.showMessage('Trying to locate file number %s...'%number)
    QtGui.QApplication.instance().processEvents()
    if self.ui.histogramActive.isChecked():
      search=glob(os.path.join(BASE_FOLDER, (BASE_SEARCH%number)+u'histo.nxs'))
    else:
      search=glob(os.path.join(BASE_FOLDER, (BASE_SEARCH%number)+u'event.nxs'))
    if search:
      self.ui.numberSearchEntry.setText('')
      self.fileOpen(search[0])
    else:
      self.ui.statusbar.showMessage('Could not locate %s...'%number, 2500)

  def nextFile(self):
    item=self.ui.file_list.currentRow()
    if (item+1)<self.ui.file_list.count():
      self.ui.file_list.setCurrentRow(item+1)

  def prevFile(self):
    item=self.ui.file_list.currentRow()
    if item>0:
      self.ui.file_list.setCurrentRow(item-1)

  def loadExtraction(self, filename=None):
    '''
      Analyse an already extracted dataset header to reload all settings
      used for this extraction for further processing.
    '''
    if filename is None:
      filename=QtGui.QFileDialog.getOpenFileName(self, u'Create extraction from file header...',
                                               directory=self.active_folder,
                                               filter=u'Extracted Dataset (*.dat)')
    if filename!=u'':
      self.clearRefList(do_plot=False)
      text=open(filename, 'r').read()
      split1='# Parameters used for extraction of normalization:'
      split2='# Parameters used for extraction of reflectivity:'
      split3='# Column Units:'
      normdata=text.split(split1)[1].split(split2)[0]
      refdata=text.split(split2)[1].split(split3)[0]
      normlines=[line.strip('# \t').split() for line in normdata.splitlines()]
      reflines=[line.strip('# \t').split() for line in refdata.splitlines()]
      norms={}
      refs=[]
      for entry in normlines:
        if len(entry)==0 or entry[0]=='I0':
          continue
        I0, P0, PN=entry[:3]
        x0, xw, y0, yw, bg0, bgw=entry[3:9]
        dpix, tth, number, nidx=entry[9:13]
        filename=entry[14]
        options=dict(
                x_pos=float(x0),
                x_width=float(xw),
                y_pos=float(y0),
                y_width=float(yw),
                bg_pos=float(bg0),
                bg_width=float(bgw),
                scale=float(I0),
                extract_fan=False,
                P0=int(P0),
                PN=int(PN),
                number=number,
                tth=float(tth),
                dpix=float(dpix),
                bg_tof_constant=False,
                normalization=None,
                     )
        data=NXSData(filename)
        norms[nidx]=Reflectivity(data[0], **options)
        self.refl=norms[nidx]
        self.active_file=filename
        self.active_data=data
        self.setNorm(do_plot=False, do_remove=False)
      for entry in reflines:
        if len(entry)==0 or entry[0]=='I0':
          continue
        I0, P0, PN=entry[:3]
        x0, xw, y0, yw, bg0, bgw=entry[3:9]
        dpix, tth, number, nidx, fan=entry[9:14]
        filename=entry[14]
        options=dict(
                x_pos=float(x0),
                x_width=float(xw),
                y_pos=float(y0),
                y_width=float(yw),
                bg_pos=float(bg0),
                bg_width=float(bgw),
                scale=float(I0),
                extract_fan=bool(int(fan)),
                P0=int(P0),
                PN=int(PN),
                number=number,
                tth=float(tth),
                dpix=float(dpix),
                bg_tof_constant=False,
                normalization=norms[nidx],
                     )
        data=NXSData(filename)
        self.channels=data.keys()
        desiredChannel=self.ui.selectedChannel.currentText().split('/')
        self.active_channel=self.channels[0]
        for channel in self.channels:
          if channel in desiredChannel:
            self.active_channel=channel
            break
        self.active_data=data
        self.active_file=filename
        ref=Reflectivity(data[0], **options)
        refs.append(ref)
        self.refl=ref
        self.addRefList()

    self.ui.actionAutoYLimits.setChecked(True)
    self.fileOpen(filename)
    self.ui.actionAutoYLimits.setChecked(False)

  def automaticExtraction(self, filenames):
    '''
      Make use of all automatic algorithms to reduce a full set of data in one run.
      Normalization files are detected by the tth angle to the selected peak position.
      
      The result is shown in the table and can be modified by the user.
    '''
    self.clearRefList(do_plot=False)
    for filename in sorted(filenames):
      # read files data and extract reflectivity
      self.fileOpen(filename, do_plot=False)
      self.calc_refl()
      if (self.refl.ai*180./pi)<0.05:
        self.setNorm(do_plot=False, do_remove=False)
      else:
        norm=self.getNorm()
        if norm is None:
          QtGui.QMessageBox.warning(self, 'Automatic extraction failed',
            'There is a dataset without fitting normalization, automatic extraction stopped!')
          break
        # cut regions where the incident intensity drops below 10% of the maximum
        region=where(norm.Rraw>=(norm.Rraw.max()*0.1))[0]
        P0=len(norm.Rraw)-region[-1]
        PN=region[0]
        self.ui.rangeStart.setValue(P0)
        self.ui.rangeEnd.setValue(PN)
        # normalize total reflection or stich together adjecent scans
        self.normalizeTotalReflection()
        self.addRefList()
    # rest cut options and show the file, which was added last
    self.ui.rangeStart.setValue(0)
    self.ui.rangeEnd.setValue(0)
    self.fileOpen(filename)

  def onPathChanged(self, base, folder):
    '''
      Update the file list and create a watcher to update the list again if a new file was
      created.
    '''
    self._path_watcher.removePath(self.active_folder)
    self.active_folder=folder
    self.updateFileList(base, folder)
    self._path_watcher.addPath(self.active_folder)

  def folderModified(self, flist=None):
    '''
      Called by the path watcher to update the file list when the folder
      has been modified.
    '''
    self.updateFileList(self.active_file, self.active_folder)

  def updateFileList(self, base, folder):
    '''
      Create a new filelist if the folder has changes.
    '''
    if self.ui.histogramActive.isChecked():
      newlist=glob(os.path.join(folder, '*histo.nxs'))
    else:
      newlist=glob(os.path.join(folder, '*event.nxs'))
    newlist.sort()
    newlist=map(lambda name: os.path.basename(name), newlist)
    self.ui.file_list.clear()
    for item in newlist:
      listitem=QtGui.QListWidgetItem(item, self.ui.file_list)
      if item==base:
        self.ui.file_list.setCurrentItem(listitem)

  def updateLabels(self):
    '''
      Write file metadata to the labels in the overview tab.
    '''
    d=self.active_data[self.active_channel]

    try:
      tth=u"%.3f° (%.3f°)"%(d.dangle-float(self.ui.dangle0Overwrite.text()), d.dangle-d.dangle0)
    except ValueError:
      tth=u"%.3f°"%(d.dangle-d.dangle0)
    if self.ui.directPixelOverwrite.value()>=0:
      dpix=u"%.1f (%.1f)"%(self.ui.directPixelOverwrite.value(), d.dpix)
    else:
      dpix=u"%.1f"%d.dpix
    self.ui.datasetLambda.setText(u"%.2f Å"%self.active_data.lambda_center)
    self.ui.datasetPCharge.setText(u"%.3e"%d.proton_charge)
    self.ui.datasetTotCounts.setText(u"%.4e"%d.total_counts)
    self.ui.datasetDangle.setText(u"%.3f°"%d.dangle)
    self.ui.datasetTth.setText(tth)
    self.ui.datasetSangle.setText(u"%.3f°"%d.sangle)
    self.ui.datasetDirectPixel.setText(dpix)
    self.ui.currentChannel.setText('<b>%s</b> (%s)&nbsp;&nbsp;&nbsp;Type: %s&nbsp;&nbsp;&nbsp;Current Channel: <b>%s</b>'%(
                                                      self.active_data.number,
                                                      self.active_data.experiment,
                                                      self.active_data.measurement_type,
                                                      self.active_channel))

  def toggleColorbars(self):
    if not self.auto_change_active:
      plots=[self.ui.xy_pp, self.ui.xy_mp, self.ui.xy_pm, self.ui.xy_mm,
             self.ui.xtof_pp, self.ui.xtof_mp, self.ui.xtof_pm, self.ui.xtof_mm,
             self.ui.xy_overview, self.ui.xtof_overview,
             self.ui.offspec_pp, self.ui.offspec_mp, self.ui.offspec_pm, self.ui.offspec_mm]
      for plot in plots:
        plot.clear_fig()
      self.plotActiveTab()

  def toggleHide(self):
    plots=[self.ui.frame_xy_mm, self.ui.frame_xy_sf, self.ui.frame_xtof_mm, self.ui.frame_xtof_sf]
    if self.ui.hide_plots.isChecked():
      for plot in plots:
        plot.do_hide=True
    else:
      for plot in plots:
        plot.show()
        plot.do_hide=False

  def changeRegionValues(self):
    '''
      Called when the reflectivity extraction region has been changed.
      Sets up a trigger to replot the reflectivity with a delay so
      a subsequent change can occur without several replots.
    '''
    if self.auto_change_active:
      return
    lines=self.proj_lines
    x_peak=self.ui.refXPos.value()
    x_width=self.ui.refXWidth.value()
    y_pos=self.ui.refYPos.value()
    y_width=self.ui.refYWidth.value()
    bg_pos=self.ui.bgCenter.value()
    bg_width=self.ui.bgWidth.value()

    lines[0].set_xdata([x_peak-x_width/2., x_peak-x_width/2.])
    lines[1].set_xdata([x_peak, x_peak])
    lines[2].set_xdata([x_peak+x_width/2., x_peak+x_width/2.])
    lines[3].set_xdata([bg_pos-bg_width/2., bg_pos-bg_width/2.])
    lines[4].set_xdata([bg_pos+bg_width/2., bg_pos+bg_width/2.])
    lines[5].set_xdata([y_pos-y_width/2., y_pos-y_width/2.])
    lines[6].set_xdata([y_pos+y_width/2., y_pos+y_width/2.])
    self.ui.x_project.draw()
    self.ui.y_project.draw()
    self.trigger('plot_refl')

  def replotProjections(self):
    self.plot_projections(preserve_lim=True)

  def setNorm(self, do_plot=True, do_remove=True):
    '''
      Add dataset to the available normalizations or clear the normalization list.
    '''
    if self.refl is None:
      return
    if str(self.active_data.number) not in self.ref_norm:
      lamda=self.active_data.lambda_center
      number=str(self.active_data.number)
      opts=self.refl.options
      self.ref_norm[number]=self.refl
      idx=sorted(self.ref_norm.keys()).index(number)
      self.ui.normalizeTable.insertRow(idx)
      item=QtGui.QTableWidgetItem(number)
      item.setTextColor(QtGui.QColor(100, 0, 0))
      item.setBackgroundColor(QtGui.QColor(200, 200, 200))
      self.ui.normalizeTable.setItem(idx, 0, QtGui.QTableWidgetItem(item))
      self.ui.normalizeTable.setItem(idx, 1, QtGui.QTableWidgetItem(str(lamda)))
      item=QtGui.QTableWidgetItem(str(opts['x_pos']))
      item.setBackgroundColor(QtGui.QColor(200, 200, 200))
      self.ui.normalizeTable.setItem(idx, 2, QtGui.QTableWidgetItem(item))
      self.ui.normalizeTable.setItem(idx, 3, QtGui.QTableWidgetItem(str(opts['x_width'])))
      item=QtGui.QTableWidgetItem(str(opts['y_pos']))
      item.setBackgroundColor(QtGui.QColor(200, 200, 200))
      self.ui.normalizeTable.setItem(idx, 4, QtGui.QTableWidgetItem(item))
      self.ui.normalizeTable.setItem(idx, 5, QtGui.QTableWidgetItem(str(opts['y_width'])))
      item=QtGui.QTableWidgetItem(str(opts['bg_pos']))
      item.setBackgroundColor(QtGui.QColor(200, 200, 200))
      self.ui.normalizeTable.setItem(idx, 6, QtGui.QTableWidgetItem(item))
      self.ui.normalizeTable.setItem(idx, 7, QtGui.QTableWidgetItem(str(opts['bg_width'])))
      self.ui.normalizationLabel.setText(u",".join(map(str, sorted(self.ref_norm.keys()))))
    elif do_remove:
      number=str(self.active_data.number)
      idx=sorted(self.ref_norm.keys()).index(number)
      del(self.ref_norm[number])
      self.ui.normalizeTable.removeRow(idx)
      self.ui.normalizationLabel.setText(u",".join(map(str, sorted(self.ref_norm.keys()))))
    if do_plot:
      self.plot_refl()

  def getNorm(self, data=None):
    '''
      Return a fitting normalization (same ToF channels and wavelength) for 
      a dataset.
    '''
    fittings=[]
    indices=[]
    if data is None:
      data=self.active_data[self.active_channel]
    for index, norm in sorted(self.ref_norm.items()):
      if len(norm.Rraw)==len(data.tof) and norm.lambda_center==data.lambda_center:
        fittings.append(norm)
        indices.append(str(index))
    if len(fittings)==0:
      return None
    elif len(fittings)==1:
      return fittings[0]
    elif str(self.active_data.number) in indices:
      return fittings[indices.index(str(self.active_data.number))]
    else:
      result=QtGui.QInputDialog.getItem(self, 'Select Normalization',
                                        'There are more than one normalizations\nfor this wavelength available,\nplease select one:',
                                        indices, editable=False)
      if not result[1]:
        return None
      else:
        return fittings[indices.index(result[0])]

  def clearNormList(self):
    '''
      Remove all items from the reduction list.
    '''
    self.ui.normalizeTable.setRowCount(0)
    self.ui.normalizationLabel.setText(u"Unset")
    self.ref_norm={}

  def normalizeTotalReflection(self):
    '''
      Extract the scaling factor from the reflectivity curve.
    '''
    if self.refl is None or not self.refl.options['normalization']:
      QtGui.QMessageBox.information(self, 'Select other dataset',
            'Please select a dataset with total reflection plateau\nand normalization.')
      return
    is_first=True
    first=len(self.refl.R)-self.ui.rangeStart.value()
    y=self.refl.R[:first]
    x=self.refl.Q[:first][y>0]
    dy=self.refl.dR[:first][y>0]
    y=y[y>0]
    for refli in self.reduction_list:
      last=refli.options['PN']
      y_other=refli.R[last:]
      dy_other=refli.dR[last:][y_other>0]
      x_other=refli.Q[last:][y_other>0]
      y_other=y_other[y_other>0]
      # try to find overlapping regions
      if not (x_other.min()<x.min() and x_other.max()>x.min()):
        continue
      else:
        is_first=False
        break
    if not is_first:
      reg_this=max(0, where(x<=x_other.max())[0][0]-self.ui.addStitchPoints.value())
      reg_other=where(x_other>=x.min())[0][-1]+1+self.ui.addStitchPoints.value()
      # try to match both datasets by fitting a polynomiral to the overlapping region
      rescale, xfit, yfit=self.refineOverlap(x[reg_this:], y[reg_this:], dy[reg_this:],
                                x_other[:reg_other], y_other[:reg_other], dy_other[:reg_other])
      self.ui.refScale.setValue(self.ui.refScale.value()+log10(rescale)) #change the scaling factor
      self.ui.refl.plot(xfit, yfit)
    else:
      # normalize total reflection plateau
      # Start from low Q and search for the critical edge
      for i in range(len(y)-5, 0,-1):
        wmean=(y[i:]/dy[i:]).sum()/(1./dy[i:]).sum()
        yi=y[i-1]
        if yi<wmean*0.9:
          break
      self.ui.refScale.setValue(self.ui.refScale.value()+log10(1./wmean)) #change the scaling factor
      # show a line in the plot corresponding to the extraction region
      totref=Line2D([x.min(), x[i]], [1., 1.], color='red')
      self.ui.refl.canvas.ax.add_line(totref)
    ymin, ymax=self.ui.refl.canvas.ax.get_ylim()
    ymax=max(ymax, 1.1)
    self.ui.refl.canvas.ax.set_ylim((ymin, ymax))
    self.ui.refl.draw()

  def addRefList(self):
    '''
      Collect information about the current extraction settings and store them
      in the list of reduction items.
    '''
    if self.refl is None:
      return
    if self.refl.options['normalization'] is None:
      QtGui.QMessageBox.information(self, u'Data not normalized',
                                    u"You can only add reflectivities (λ normalized)!",
                                    QtGui.QMessageBox.Close)
      return
    # collect current settings
    channels=self.channels
    if self.reduction_list==[]:
      self.ref_list_channels=list(channels)
    elif self.ref_list_channels!=channels:
      QtGui.QMessageBox.information(self, u'Wrong Channels',
u'''The active dataset has not the same channels 
as the ones already in the list:

%s  ≠  %s'''%(u" / ".join(channels), u' / '.join(self.ref_list_channels)),
                                    QtGui.QMessageBox.Close)
      return
    # options used for the extraction
    opts=self.refl.options

    Pstart=len(self.refl.R)-where(self.refl.R>0)[0][-1]-1
    Pend=where(self.refl.R>0)[0][0]
    opts['P0']=max(Pstart, opts['P0'])
    opts['PN']=max(Pend, opts['PN'])

    if len(self.reduction_list)==0:
      # use the same y region for all following datasets (can be changed by user if desired)
      self.ui.actionAutoYLimits.setChecked(False)
    self.reduction_list.append(self.refl)
    self.ui.reductionTable.setRowCount(len(self.reduction_list))
    idx=len(self.reduction_list)-1
    self.auto_change_active=True

    item=QtGui.QTableWidgetItem(opts['number'])
    item.setTextColor(QtGui.QColor(100, 0, 0))
    item.setBackgroundColor(QtGui.QColor(200, 200, 200))
    self.ui.reductionTable.setItem(idx, 0, item)
    self.ui.reductionTable.setItem(idx, 1,
                                   QtGui.QTableWidgetItem("%.4f"%(opts['scale'])))
    self.ui.reductionTable.setItem(idx, 2,
                                   QtGui.QTableWidgetItem(str(opts['P0'])))
    self.ui.reductionTable.setItem(idx, 3,
                                   QtGui.QTableWidgetItem(str(opts['PN'])))
    item=QtGui.QTableWidgetItem(str(opts['x_pos']))
    item.setBackgroundColor(QtGui.QColor(200, 200, 200))
    self.ui.reductionTable.setItem(idx, 4, item)
    self.ui.reductionTable.setItem(idx, 5,
                                   QtGui.QTableWidgetItem(str(opts['x_width'])))
    item=QtGui.QTableWidgetItem(str(opts['y_pos']))
    item.setBackgroundColor(QtGui.QColor(200, 200, 200))
    self.ui.reductionTable.setItem(idx, 6, item)
    self.ui.reductionTable.setItem(idx, 7,
                                   QtGui.QTableWidgetItem(str(opts['y_width'])))
    item=QtGui.QTableWidgetItem(str(opts['bg_pos']))
    item.setBackgroundColor(QtGui.QColor(200, 200, 200))
    self.ui.reductionTable.setItem(idx, 8, item)
    self.ui.reductionTable.setItem(idx, 9,
                                   QtGui.QTableWidgetItem(str(opts['bg_width'])))
    self.ui.reductionTable.setItem(idx, 10,
                                   QtGui.QTableWidgetItem(str(opts['dpix'])))
    self.ui.reductionTable.setItem(idx, 11,
                                   QtGui.QTableWidgetItem("%.4f"%opts['tth']))
    self.ui.reductionTable.setItem(idx, 12,
                                   QtGui.QTableWidgetItem(str(opts['normalization'].options['number'])))
    self.ui.reductionTable.resizeColumnsToContents()
    self.auto_change_active=False

  def reductionTableChanged(self, item):
    '''
      Perform action upon change in data reduction list.
    '''
    if self.auto_change_active:
      return
    entry=item.row()
    column=item.column()
    refl=self.reduction_list[entry]
    options=dict(refl.options)
    # reset options that can't be changed
    if column==0:
      item.setText(str(options['number']))
      return
    elif column==12:
      item.setText(str(options['normalization'].options['number']))
      return
    # update settings from selected option
    elif column in [1, 4, 5, 6, 7, 8, 9, 10]:
      key=[None, 'scale', None, None,
           'x_pos', 'x_width',
           'y_pos', 'y_width',
           'bg_pos', 'bg_width',
           None, 'dp'][column]
      try:
        options[key]=float(item.text())
      except ValueError:
        item.setText(str(options[key]))
      else:
        refl_new=self.recalculateReflectivity(refl, options)
        self.reduction_list[entry]=refl_new
    elif column==2:
      try:
        refl.options['P0']=int(item.text())
      except ValueError:
        item.setText(str(options['P0']))
    elif column==3:
      try:
        refl.options['PN']=int(item.text())
      except ValueError:
        item.setText(str(options['PN']))
    elif column==11:
      try:
        options['tth']=float(item.text())*pi/180.
      except ValueError:
        item.setText(str(options['tth']*180./pi))
      else:
        Qz, R, dR=self.recalculateReflectivity(refl, options)
        self.reduction_list[entry][1:]=[Qz, R, dR]
    self.ui.reductionTable.resizeColumnsToContents()
    self.plot_refl(preserve_lim=True)

  def changeActiveChannel(self):
    '''
      The overview and reflectivity channel was changed. This
      recalculates already extracted reflectivities.
    '''
    desiredChannel=self.ui.selectedChannel.currentText().split('/')
    for channel in self.channels:
      if channel in desiredChannel:
        self.active_channel=channel
        break
    if self.active_channel in self.ref_list_channels:
      for i, refli in enumerate(self.reduction_list):
        refli=self.recalculateReflectivity(refli)
        self.reduction_list[i]=refli
    self.updateLabels()
    self.plotActiveTab()
    self.plot_projections()

  def clearRefList(self, do_plot=True):
    '''
      Remove all items from the reduction list.
    '''
    self.reduction_list=[]
    self.ui.reductionTable.setRowCount(0)
    self.ui.actionAutoYLimits.setChecked(True)
    if do_plot:
      self.plot_refl()

  def removeRefList(self):
    '''
      Remove one item from the reduction list.
    '''
    index=self.ui.reductionTable.currentRow()
    if index<0:
      return
    self.reduction_list.pop(index)
    self.ui.reductionTable.removeRow(index)
    #self.ui.reductionTable.setRowCount(0)
    self.plot_refl()

  def overwriteDirectBeam(self):
    '''
      Take the active x0 and Dangle values as overwrite parameters
      to be used with other datasets as well.
    '''
    self.auto_change_active=True
    self.ui.directPixelOverwrite.setValue(self.ui.refXPos.value())
    self.ui.dangle0Overwrite.setText(str(self.active_data[self.active_channel].dangle))
    self.auto_change_active=False
    self.overwriteChanged()

  def clearOverwrite(self):
    '''
      Reset overwrite to use values from the .nxs files.
    '''
    self.auto_change_active=True
    self.ui.directPixelOverwrite.setValue(-1)
    self.ui.dangle0Overwrite.setText("None")
    self.auto_change_active=False
    self.overwriteChanged()

  def overwriteChanged(self):
    '''
      Recalculate reflectivity based on changed overwrite parameters.
    '''
    if not self.auto_change_active:
      self.updateLabels()
      self.calcReflParams()
      self.plot_projections(preserve_lim=True)

  def reduceDatasets(self):
    '''
      Open a dialog to select reduction options for the current list of
      reduction items.
    '''
    if len(self.reduction_list)==0:
      QtGui.QMessageBox.information(self, u'Select a dataset',
                                    u'Please select at least\none dataset to reduce.',
                                    QtGui.QMessageBox.Close)
      return
    dialog=ReduceDialog(self, self.ref_list_channels, self.reduction_list)
    dialog.exec_()
    dialog.destroy()

  def plotMouseEvent(self, event):
    '''
      Show the mouse position of any plot in the main window
      status bar, as the single plot status indicator is only
      visible for larger plot toolbars.
    '''
    if event.inaxes is None:
      return
    self.ui.statusbar.showMessage(u"x=%15g    y=%15g"%(event.xdata, event.ydata))

  def plotPickX(self, event):
    '''
      Plot for x-projection has been clicked.
    '''
    if event.button is not None and self.ui.x_project.toolbar._active is None and \
        event.xdata is not None:
      if event.button==1:
        xcen=self.ui.refXPos.value()
        bgc=self.ui.bgCenter.value()
        bgw=self.ui.bgWidth.value()
        bgl=bgc-bgw/2.
        bgr=bgc+bgw/2.
        if event.xdata<bgr and abs(event.xdata-bgl)<abs(event.xdata-bgr):
          # left of right background bar and closer to left one
          bgl=event.xdata
          bgc=(bgr+bgl)/2.
          bgw=(bgr-bgl)
          self.auto_change_active=True
          self.ui.bgCenter.setValue(bgc)
          self.auto_change_active=False
          self.ui.bgWidth.setValue(bgw)
        elif event.xdata<bgr or abs(event.xdata-bgr)<abs(event.xdata-xcen):
          # left of right background bar or closer to right background than peak
          bgr=event.xdata
          bgc=(bgr+bgl)/2.
          bgw=(bgr-bgl)
          self.auto_change_active=True
          self.ui.bgCenter.setValue(bgc)
          self.auto_change_active=False
          self.ui.bgWidth.setValue(bgw)
        else:
          self.ui.refXPos.setValue(event.xdata)
          if self.ui.actionRefineX.isChecked():
            self.refineXpos()
      elif event.button==3:
        self.ui.refXWidth.setValue(abs(self.ui.refXPos.value()-event.xdata)*2.)

  def plotPickY(self, event):
    '''
      Plot for y-projection has been clicked.
    '''
    if event.button==1 and self.ui.y_project.toolbar._active is None and \
        event.xdata is not None:
      ypos=self.ui.refYPos.value()
      yw=self.ui.refYWidth.value()
      yl=ypos-yw/2.
      yr=ypos+yw/2.
      if abs(event.xdata-yl)<abs(event.xdata-yr):
        yl=event.xdata
      else:
        yr=event.xdata
      ypos=(yr+yl)/2.
      yw=(yr-yl)
      self.auto_change_active=True
      self.ui.refYPos.setValue(ypos)
      self.auto_change_active=False
      self.ui.refYWidth.setValue(yw)

  def plotPickXY(self, event):
    '''
      Plot for xy-map has been clicked.
    '''
    if event.button==1 and self.ui.xy_overview.toolbar._active is None and \
        event.xdata is not None:
      self.ui.refXPos.setValue(event.xdata)
    elif event.button==3 and self.ui.xy_overview.toolbar._active is None and \
        event.ydata is not None:
      ypos=self.ui.refYPos.value()
      yw=self.ui.refYWidth.value()
      yl=ypos-yw/2.
      yr=ypos+yw/2.
      if abs(event.ydata-yl)<abs(event.ydata-yr):
        yl=event.ydata
      else:
        yr=event.ydata
      ypos=(yr+yl)/2.
      yw=(yr-yl)
      self.auto_change_active=True
      self.ui.refYPos.setValue(ypos)
      self.auto_change_active=False
      self.ui.refYWidth.setValue(yw)

  def plotPickXToF(self, event):
    if event.button==1 and self.ui.xtof_overview.toolbar._active is None and \
        event.ydata is not None:
      self.ui.refXPos.setValue(event.ydata)
    elif event.button==3 and self.ui.xtof_overview.toolbar._active is None and \
        event.ydata is not None:
      xpos=self.ui.refXPos.value()
      self.ui.refXWidth.setValue(abs(xpos-event.ydata)*2.)

  def scaleOnPlot(self, event):
    steps=event.step
    xpos=event.xdata
    if xpos is None:
      return
    for i, refl in enumerate(self.reduction_list):
      if (refl.Q[len(refl.Q)-refl.options['P0']]<xpos) and (refl.Q[refl.options['PN']]>xpos):
        Ival=refl.options['scale']
        if self._control_down:
          Inew=Ival*10**(0.05*steps)
        else:
          Inew=Ival*10**(0.01*steps)
        self.ui.reductionTable.setItem(i, 1,
                                   QtGui.QTableWidgetItem("%.4f"%(Inew)))
        return

  def keyPressEvent(self, event):
    if event.modifiers()==QtCore.Qt.ControlModifier:
      self._control_down=True
    else:
      self._control_down=False

  def keyReleaseEvent(self, event):
    self._control_down=False

  def updateEventReadout(self, progress):
    '''
      When reading event mode data this is the callback
      used after each finished channel to indicate the progress.
    '''
    self.eventProgress.setValue(progress*100)
    app=QtGui.QApplication.instance()
    app.processEvents()

####### Calculations and data treatment

  def calcReflParams(self):
    '''
      Calculate x and y regions for reflectivity extraction and put them in the
      entry fields.
    '''
    data=self.active_data[self.active_channel]
    if self.ui.xprojUseQuantiles.isChecked():
      d2=data.xtofdata
      xproj=mquantiles(d2, self.ui.xprojQuantiles.value()/100., axis=1).flatten()
    else:
      xproj=data.xdata
    yproj=data.ydata

    # calculate approximate peak position
    try:
      tth_bank=(data.dangle-float(self.ui.dangle0Overwrite.text()))*pi/180.
    except ValueError:
      tth_bank=(data.dangle-data.dangle0)*pi/180.
    ai=data.sangle*pi/180.
    if self.ui.directPixelOverwrite.value()>=0:
      dp=self.ui.directPixelOverwrite.value()
    else:
      dp=data.dpix
    pix_position=dp-(ai*2-tth_bank)/RAD_PER_PIX

    self.auto_change_active=True
    if self.ui.actionAutomaticXPeak.isChecked():
      try:
        # locate peaks using CWT peak finder algorithm
        self.pf=PeakFinder(arange(DETECTOR_X_REGION[1]-DETECTOR_X_REGION[0]),
                            xproj[DETECTOR_X_REGION[0]:DETECTOR_X_REGION[1]])
        # Signal to noise ratio, minimum width, maximum width, algorithm ridge parameter
        peaks=self.pf.get_peaks(snr=self.ui.pfSNR.value(),
                                min_width=self.ui.pfMinWidth.value(),
                                max_width=self.ui.pfMaxWidth.value(),
                                ridge_length=self.ui.pfRidgeLength.value())
        x_peaks=array([p[0] for p in peaks])+DETECTOR_X_REGION[0]


        delta_pix=abs(pix_position-x_peaks)
        x_peak=x_peaks[delta_pix==delta_pix.min()][0]
      except:
        # if there was any error finding the peak, use the position from the file
        x_peak=pix_position
      # refine gaussian to this peak position
      x_width=self.ui.refXWidth.value()
      x_peak=self.refineGauss(xproj, x_peak, x_width)
      self.ui.refXPos.setValue(x_peak)

    if self.ui.actionAutoYLimits.isChecked():
      # find the central peak reagion with intensities larger than 10% of maximum
      y_bg=mquantiles(yproj, 0.5)[0]
      self.y_bg=y_bg
      y_peak_region=where((yproj-y_bg)>yproj.max()/10.)[0]
      yregion=(y_peak_region[0], y_peak_region[-1])
      self.ui.refYPos.setValue((yregion[0]+yregion[1]+1.)/2.)
      self.ui.refYWidth.setValue(yregion[1]+1-yregion[0])
    else:
      self.y_bg=0.
    self.auto_change_active=False

  def visualizePeakfinding(self):
    '''
      Show a graphical representation of the peakfinder process.
    '''
    self.pf.visualize(snr=self.ui.pfSNR.value(),
                      min_width=self.ui.pfMinWidth.value(),
                      max_width=self.ui.pfMaxWidth.value(),
                      ridge_length=self.ui.pfRidgeLength.value())


  def refineXpos(self):
    '''
      Fit the selected x position to the closest peak.
    '''
    if self.ui.actionRefineX.isChecked():
      data=self.active_data[self.active_channel].xydata
      if self.ui.xprojUseQuantiles.isChecked():
        d2=self.active_data[self.active_channel].xtofdata
        xproj=mquantiles(d2, self.ui.xprojQuantiles.value()/100., axis=1).flatten()
      else:
        xproj=data.mean(axis=0)
      # refine gaussian to this peak position
      x_width=self.ui.refXWidth.value()
      x_peak=self.ui.refXPos.value()
      x_peak=self.refineGauss(xproj, x_peak, x_width)
      self.ui.refXPos.setValue(x_peak)

  def refineGauss(self, data, pos, width):
    '''
      Fit a gaussian function to a given dataset and return the x0 position.
    '''
    p0=[data[int(pos)], pos, width]
    parinfo=[{'value':0., 'fixed':0, 'limited':[0, 0],
              'limits':[0., 0.]} for ignore in range(3)]
    parinfo[0]['limited']=[True, False]
    parinfo[0]['limits']=[0., None]
    parinfo[2]['fixed']=True
    res=mpfit(self.gauss_residuals, p0, functkw={'data':data}, nprint=0, parinfo=parinfo)
    parinfo[2]['fixed']=False
    parinfo[2]['limited']=[True, True]
    parinfo[2]['limits']=[1., 4.*width]
    p0=[data[int(res.params[1])], res.params[1], width]
    res=mpfit(self.gauss_residuals, p0, functkw={'data':data}, nprint=0, parinfo=parinfo)
    return res.params[1]

  def gauss_residuals(self, p, fjac=None, data=None, width=1):
    '''
      Gaussian of I0, x0 and sigma parameters minus the data.
    '''
    xdata=arange(data.shape[0])
    I0=p[0]
    x0=p[1]
    sigma=p[2]/5.
    G=exp(-0.5*((xdata-x0)/sigma)**2)
    return 0, data-I0*G

  def refineOverlap(self, x1, y1, dy1, x2, y2, dy2):
    '''
      Refine a polynomial to the logarithm of two datasets while
      scaling the first dataset as well. Return the resulting
      scaling parameter and the refined function for plotting.
    '''
    result=mpfit(self.overlapResiduals, [1., 0.,-40., 0.],
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

  def overlapResiduals(self, p, fjac=None, x1=None, y1=None, dy1=None,
                                           x2=None, y2=None, dy2=None):
    yscale, a, b, c=p
    part1=(log10(yscale*y1)-a*x1**2-b*x1-c)/(dy1/y1)
    part2=(log10(y2)-a*x2**2-b*x2-c)/(dy2/y2)
    return 0, hstack([part1, part2])

  def recalculateReflectivity(self, old_object, overwrite_options=None):
    '''
      Use parameters to calculate and return the reflectivity
      of one file.
    '''
    filename, _channel=old_object.origin
    data=NXSData(filename, **old_object.read_options)[self.active_channel]
    if overwrite_options:
      refl=Reflectivity(data, **overwrite_options)
    else:
      refl=Reflectivity(data, **old_object.options)
    return refl

###### Window initialization and exit

  def readSettings(self):
    '''
      Restore window and dock geometry.
    '''
    path=os.path.join(os.path.expanduser('~/.quicknxs'), 'window.pkl')
    if os.path.exists(path):
      try:
        obj=load(open(path, 'rb'))
      except:
        return
    else:
      obj=load(open(os.path.join(os.path.dirname(__file__), 'window.pkl'), 'rb'))
    try:
      self.restoreGeometry(obj[0])
      self.restoreState(obj[1])
      self.ui.splitter.setSizes(obj[2])
      self.ui.color_selector.setCurrentIndex(obj[3])
      self.ui.show_colorbars.setChecked(obj[4])
      self.ui.normalizeXTof.setChecked(obj[5])
      for i, fig in enumerate([
                              self.ui.xy_overview,
                              self.ui.xtof_overview,
                              self.ui.refl,
                              self.ui.x_project,
                              self.ui.y_project,
                              ]):
        fig.set_config(obj[6][i])
    except:
      return

  def closeEvent(self, event):
    '''
      Save window and dock geometry.
    '''
    # join delay thread
    self.trigger.stay_alive=False
    self.trigger.wait()
    # store geometry and setting parameters
    figure_params=[]
    for fig in [
                self.ui.xy_overview,
                self.ui.xtof_overview,
                self.ui.refl,
                self.ui.x_project,
                self.ui.y_project,
                ]:
      figure_params.append(fig.get_config())
    obj=(self.saveGeometry(), self.saveState(),
         self.ui.splitter.sizes(),
         self.ui.color_selector.currentIndex(),
         self.ui.show_colorbars.isChecked(),
         self.ui.normalizeXTof.isChecked(),
         figure_params,
         )
    path=os.path.expanduser('~/.quicknxs')
    if not os.path.exists(path):
      os.makedirs(path)
    dump(obj, open(os.path.join(path, 'window.pkl'), 'wb'))
    QtGui.QMainWindow.closeEvent(self, event)

  def helpDialog(self):
    '''
      Open a HTML page with the program documentation and place it on the right
      side of the current screen.
    '''
    dia=QtGui.QDialog(self)
    dia.setWindowTitle(u'QuickNXS Manual')
    verticalLayout=QtGui.QVBoxLayout(dia)
    dia.setLayout(verticalLayout)
    webview=QtWebKit.QWebView(dia)
    index_file=os.path.join(os.path.dirname(__file__), u'htmldoc/QuickNXS_Users_Manual.html')
    webview.load(QtCore.QUrl(index_file))
    verticalLayout.addWidget(webview)
    # set width of the page to fit the document and height to the same as the main window
    dia.resize(700, self.height())
    pos=-700
    dw=QtGui.QDesktopWidget()
    for i in range(dw.screenCount()):
      pos+=dw.screenGeometry(i).width()
      if pos>self.pos().x():
        break
    dia.move(pos, dia.pos().y())
    dia.show()

  def aboutDialog(self):
    from numpy.version import full_version as npversion
    from matplotlib import __version__ as mplversion
    from h5py.version import version as h5pyversion
    from h5py.version import hdf5_version as hdf5version
    from PyQt4.pyqtconfig import Configuration
    pyqtversion=Configuration().pyqt_version_str

    QtGui.QMessageBox.about(self, 'About QuickNXS',
'''
QuickNXS - SNS Magnetism Reflectometer data reduction program
  Version %s

Library Versions:
  Numpy %s
  Matplotlib %s
  Qt %s
  PyQt4 %s
  H5py %s
  HDF5 %s
'''%(str_version, npversion, mplversion, QtCore.QT_VERSION_STR, pyqtversion, h5pyversion, hdf5version))

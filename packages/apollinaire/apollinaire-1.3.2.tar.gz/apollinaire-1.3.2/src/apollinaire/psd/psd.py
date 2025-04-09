import numpy as np
from astropy.io import fits
from astropy.table import Table
import matplotlib
from matplotlib import colors
import matplotlib.pyplot as plt
import pandas as pd
from scipy.interpolate import interp1d

'''
Module to compute power spectra density (PSD) from
  timeseries (series_to_psd) or Fourier transform 
  (tf_to_psd).

PSD can then be saved as fits file with the psd_to_fits
  function.

PSD saved into fits file can be directly plotted with the 
  plot_fits function.

The echelle_diagram function allow to compute and optionnally
  plot the echelle diagram of the PSD.
'''

def tf (series, dt) :

  """
  Take a timeseries and compute its properly normalised
  Fourier transform.

  :param series: input timeseries
  :type series: ndarray

  :param dt: sampling of the timeseries
  :type dt: float

  :return: frequency and psd array
  :rtype: tuple of ndarray
  """
  freq = np.fft.rfftfreq (series.size, d=dt)
  tf = np.fft.rfft (series) / (series.size / 2.)

  return freq, tf

def series_to_psd (series, dt, correct_dc=True) :

  """
  Take a timeseries and compute its PSD

  :param series: input timeseries.
  :type series: ndarray

  :param dt: sampling of the timeseries, in seconds.
  :type dt: float

  :param correct_dc: if set to True, will compute the duty_cycle
    to adjust the psd values. Optional, default False.
  :type correct_dc: bool

  :return: frequency and psd array. The frequency units are in ``Hz`` and
    the PSD in ``series_units**2/Hz``. Note that the ``apollinaire.peakbagging``
    submodule works with frequency in ``muHz`` and PSD in ``ppm**2/muH`` 
    (or ``(m/s)**2/muHz`` for radial velocity PSD), frequency array and PSD 
    should therefore be normalised accordingly before using the peakbagging
    functions. 
  :rtype: tuple of ndarray
  """
  freq = np.fft.rfftfreq (series.size, d=dt)
  tf = np.fft.rfft (series) / (series.size / 2.)
  T = series.size * dt
  PSD = np.abs (tf) * np.abs (tf) * T / 2.

  if correct_dc :
    dc = np.count_nonzero (series) / series.size
    PSD = PSD / dc

  return freq, PSD

def tf_to_psd (tf, T) :

  '''
  :param tf: complex Fourier transform from which to
    compute the PSD.
  :type tf: ndarray 

  :param T: resolution of the Fourier transform.
  :type T: float

  :return: corresponding PSD
  :rtype: ndarray
  '''

  PSD = np.abs (tf) * np.abs (tf) * T / 2.
  return PSD 


def psd_to_fits (freq, psd, filename) :
  '''
  Save frequency and power vector into a fits file.

  :param freq: frequency vector.
  :type freq: ndarray

  :param psd: psd vector.
  :type psd: ndarray

  :param filename: name of the fits file to create.
  :type filename: str
  '''

  data = np.c_[freq,psd]
  hdu = fits.PrimaryHDU (data)
  hdu.writeto (filename)

  return

def psd_second (freq, psd, resampling_length=1000) :
  '''
  Compute PS2, that is the PSD of a given PSD. The returned
  power spectrum PS2 is normalised by its standard deviation.

  :param freq: frequency vector.
  :type freq: ndarray

  :param psd: psd vector.
  :type psd: ndarray

  :return: period and second PSD vector 
  :rtype: tuple of arrays
  '''

  period = 1 / freq[freq>0]
  func = interp1d (period, psd[freq>0])
  resampled_period = np.linspace (period[0], period[-1], resampling_length)
  resampled_psd = func (resampled_period)
  resampled_period = np.flip (resampled_period)
  resampled_psd = np.flip (resampled_psd)
  d = resampled_period[1] - resampled_period[0]

  dft = 2 *  np.fft.rfft (resampled_psd) / resampled_psd.size 
  ps2 = np.abs (dft) [1:]
  freq2 = np.fft.rfftfreq (resampled_psd.size, d=d)
  period2 = 1 / freq2[1:]
  ps2 = np.flip (ps2)
  period2 = np.flip (period2)
  ps2 = ps2 / np.std (ps2)

  return period2, ps2


def plot_psd_fits (filename, rv=True, index=0) :
  '''
  Plot the PSD of a fits file containing frequency and power 
  array. The frequency in the file are supposed to be in Hz and
  the power in (m/s)^2/Hz (spectroscopy) or ppm^2/Hz (photometry)

  :param filename: name of the fits file
  :type filename: str

  :param rv: set to True if it is a radial velocity PSD, to False
    if it is a photometric PSD.
  :type rv: bool

  :param index: index of the hdulist of the fits file where the PSD can
    be found. Default is 0.
  :type index: int
  '''

  hdu = fits.open (filename) [index]
  data = np.array (hdu.data)
  fig = plt.figure (figsize=(12,6))
  ax = fig.add_subplot (111)
  ax.plot (data[:,0]*1.e6, data[:,1]*1.e-6)
  ax.set_xlabel (r'Frequency ($\mu$Hz)')
  if rv==True :
     ax.set_ylabel (r'PSD ((m/s)$^2$/$\mu$Hz)')
  else :
     ax.set_ylabel (r'PSD (ppm$^2$/$\mu$Hz)')

  return

def echelle_diagram (freq, PSD, dnu, twice=False, fig=None, index=111,
                     figsize=(16,16), title=None,
                     smooth=10, cmap='cividis', cmap_scale='linear', 
                     mode_freq=None, mode_freq_err=None,
                     vmin=None, vmax=None, scatter_color='white', fmt='+', ylim=None,
                     shading='gouraud', mfc='none', ms=20, index_offset=None, 
                     mec=None, xlabel=None, ylabel=None, **kwargs) :

  '''
  Build the echelle diagram of a given PSD.  

  :param freq: input vector of frequencies.
  :type freq: ndarray

  :param PSD: input vector of power. Must be of same size than freq.
  :type PSD: ndarray

  :param dnu: the large frequency separation use to cut slices 
    into the diagram. 
  :type dnu: float

  :param twice: slice using 2 x *dnu* instead of *dnu*, default False.
  :type twice: bool

  :param fig: figure on which the echelle diagram will be plotted. If ``None``, a new figure 
    instance will be created. Optional, default ``None``. 
  :type fig: matplotlib Figure

  :param index: position of the echelle diagram Axe in the figure. Optional, default ``111``.
  :type index: int

  :param figsize: size of the echelle diagram to plot.
  :type figsize: tuple

  :param title: title of the figure. Optional, default ``(16, 16)``
  :type title: str

  :param smooth: size of the rolling window used to smooth the PSD. Default 10.
  :type smooth: int

  :param cmap: select one available color map provided by matplotlib, default ``cividis``
  :type cmap: str

  :param cmap_scale: scale use for the colormap. Can be 'linear' or 'logarithmic'.
    Optional, default 'linear'.
  :type cmap_scale: str

  :param mode_freq: frequency array of the modes to represent on the diagram. It can be single 
    array or a tuple of array.
  :type mode_freq: ndarray or tuple of array

  :param mode_freq_err: frequency uncertainty of the modes to represent on the diagram. It can be
    a single array or a tuple of array.
  :type mode_freq_err: ndarray or tuple of array

  :param vmin: minimum value for the colormap.
  :type vmin: float

  :param vmax: maximum value for the colormap.
  :type vmax: float

  :param scatter_color: color of the scatter point of the mode frequencies. Optional, default ``white``.
  :type scatter_color: str

  :param fmt: the format of the errorbar to plot. Can be a single string or a tuple of string with the same
    dimension that ``mode_freq``.
  :type fmt: str or tuple

  :param ylim: the y-bounds of the echelle diagram.
  :type ylim: tuple

  :param mew: marker edge width. Optional, default 1.
  :type mew: float

  :param markersize: size of the markers used for the errorbar plot. Optional, default 10.
  :type markersize: float

  :param capsize: length of the error bar caps. Optional, default 2.
  :type capsize: float

  :return: the matplotlib Figure with the echelle diagram.
  :rtype: matplotlib Figure
  '''

  if cmap_scale not in ['linear', 'logarithmic'] :
    raise Exception ("cmap_scale should be set to 'linear' or 'logarithmic'.")

  if cmap_scale=='logarithmic':
    norm = colors.LogNorm (vmin=vmin, vmax=vmax)
  elif cmap_scale=='linear' :
    norm = colors.Normalize (vmin=vmin, vmax=vmax)

  if smooth != 1 :
    PSD = pd.Series(data=PSD).rolling (window=smooth, min_periods=1, 
                             center=True).mean().to_numpy()

  if twice==True :
    dnu = 2.*dnu

  res = freq[2]-freq[1]

  if index_offset is not None :
    PSD = PSD[index_offset:]
    freq = freq[index_offset:]


  n_slice = int (np.floor_divide (freq[-1]-freq[0], dnu))
  len_slice = int (np.floor_divide (dnu, res))

  if (n_slice*len_slice > PSD.size) :
    len_slice -= 1

  ed = PSD[:len_slice*n_slice]
  ed = np.reshape (ed, (n_slice, len_slice))

  freq_ed = freq[:len_slice*n_slice]
  freq_ed = np.reshape (freq_ed, (n_slice, len_slice))
  x_freq = freq_ed[0,:] - freq_ed[0,0]
  y_freq = freq_ed[:,0]


  if fig is None : 
    fig = plt.figure (figsize=figsize)
  ax = fig.add_subplot (index)
  ax.pcolormesh (x_freq, y_freq, ed, cmap=cmap,  
                 norm=norm, shading=shading)

  if mode_freq is not None :
    if type (mode_freq) is not tuple :
      mode_freq = (mode_freq,)
      mode_freq_err = (mode_freq_err,) 
    if type (scatter_color) is str :
      scatter_color = np.repeat (scatter_color, len (mode_freq))
    if type (fmt) is str :
      fmt = np.repeat (fmt, len (mode_freq))
    if type (ms) in [float, int] :
      ms = np.repeat (ms, len (mode_freq))
    if type (mfc) is str :
      mfc = np.repeat (mfc, len (mode_freq))
    if mec is None :
      mec = scatter_color
    if type (mec) is str :
      mec = np.repeat (mec, len (mode_freq))

    for m_freq, m_freq_err, color, m_fmt, s, fc, edge in zip (mode_freq, mode_freq_err, 
                                                              scatter_color, fmt, ms, mfc, mec) :
      x_mode = np.zeros (m_freq.size)
      y_mode = np.zeros (m_freq.size)
      for ii, elt in enumerate (m_freq) :
          aux_1 = elt - y_freq 
          aux_2 = y_freq[aux_1>0]
          aux_1 = aux_1[aux_1>0]
          jj = np.argmin (aux_1)
          x_mode[ii] = aux_1[jj] 
          y_mode[ii] = aux_2[jj]  
          #print (x_mode[ii], y_mode[ii], x_mode[ii]+y_mode[ii], elt)
      ax.errorbar (x=x_mode, y=y_mode, xerr=m_freq_err, fmt=m_fmt, color=color, barsabove=True,
                   mfc=fc, ms=s, mec=edge, **kwargs)

  if xlabel is None :
    xlabel = r'$\nu$ mod. {:.1f} $\mu$Hz'.format (len_slice*res)
  if ylabel is None :
    ylabel = r'$\nu$ ($\mu$Hz)'
  ax.set_xlabel (xlabel)
  ax.set_ylabel (ylabel)

  ax.set_xlim (left=0, right=x_freq[-1])

  if ylim is not None :
    ax.set_ylim (ylim[0], ylim[1])

  if title is not None :
    ax.set_title (title)

  return fig

def mean_psd(series, dt, len_chunk=90) :
    """
    Compute mean PSD of a time series, by subdividing it
    into chunks of equal length. The time series sampling
    is assumed to be regular.
    
    :param series: Input time series
    :type series: ndarray

    :param dt: Temporal sampling in seconds
    :type dt: float
      
    :param len_chunk: Length of the chunks in days. Optional, default 90
    :type len_chunk: float
      
    :return: A tuple with frequency and power spectral density vectors.
    :rtype: tuple of arrays
    """
    size_chunk = int(len_chunk * 86400 / dt)
    n_chunk = series.size // size_chunk
   
    # Removing the final points of the time series
    # to have the length being a multiple of n_chunk
    # and reshaping
    series = series[:size_chunk*n_chunk].reshape((n_chunk, size_chunk))
    
    # Initialising with first chunk
    freq, psd = series_to_psd (series[0], dt, correct_dc=True)
    for chunk in series :
        _, aux = series_to_psd (chunk, dt, correct_dc=True) 
        psd += aux
    psd /= n_chunk
    return freq, psd, n_chunk


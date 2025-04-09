# coding: utf-8

import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from astropy.io import fits
from apollinaire.psd import echelle_diagram
import apollinaire.peakbagging.templates as templates
from .analyse_window import sidelob_param
from .ampl_mode import ampl_mode
from .a2z_no_pandas import  wrapper_a2z_to_pkb_nopandas
from .header import make_header_pkb
from os import sys
from os import path
import os
import importlib.resources
import glob
import corner
import numba
import warnings

def get_order_list (df_a2z) :
  """
  Get the list of order from an a2z 
  DataFrame.
  """
  aux_o = df_a2z.loc[(df_a2z[1]!='a')&(df_a2z[0]!='a')&((df_a2z[1]=='0')|(df_a2z[1]=='1')), 0].astype (int)
  orders = np.unique (aux_o)
  return orders

def get_template_path (filename="input_golf.a2z") :
  """
  Get template file path as context managers for tutorials.
  """
  return importlib.resources.as_file(importlib.resources.files(templates).joinpath(filename))

def scaling_laws (numax, dnu, teff, 
                  dnu_sun=135, numax_sun=3050, 
                  teff_sun=5770) :
  '''
  Compute stellar mass and radius from scaling 
  laws (output returned in solar mass and radius).
  '''

  r = (dnu_sun / dnu)**2 * numax/numax_sun * (teff/teff_sun)**(1/2)
  m = (dnu_sun / dnu)**4 * (numax/numax_sun)**3 * (teff/teff_sun)**(3/2)

  return r, m

def test_a2z (a2z_file, verbose=True) :

    '''
    Test a a2z file to check that it is valid. The function
    checks the bounds set for the parameters, convert the a2z
    DataFrame to pkb
  
    :param a2z_file: path of the a2z file to test.
    :type a2z_file: str
  
    :return: a2z DataFrame and pkb array.
    :rtype: tuple
    '''

    df_a2z = read_a2z (a2z_file)
    check_a2z (df_a2z, verbose=verbose)
    pkb = a2z_to_pkb (df_a2z)
    df_pkb = pd.DataFrame (data=pkb)

    if verbose :
      print (df_a2z)
      print (df_pkb.to_string ())
      print (get_list_order (df_a2z))

    assert ~np.any (np.isnan (pkb)), 'The pkb array contains NaN.'

    return df_a2z, pkb

def make_header_utility_file () :
  header = 'Utility file with normalisation parameters and parameters info'
  return header

def apodisation (dt, filename=None, show=False,
                 logscale=False) :
  '''
  Compute apodisation power attenuation function
  related to sampling and plot corresponding 
  figure.
  '''
  
  fig, ax = plt.subplots (1, 1, figsize=(12, 6))
  if not isinstance(dt, (list, tuple, np.ndarray)) :
    dt = [dt]

  for elt in dt :
    nyquist = 1 / (2*elt)
    freq = np.linspace (0, nyquist, 10000, endpoint=True)
    power = np.sinc (freq / (2*nyquist))
    power = power**2
 
    ax.plot (freq*1e6, (1-power)*100, label='dt = {:.0f} s'.format (elt))

  ax.set_xlabel ('Frequency ($\mu$Hz)')
  ax.set_ylabel ('Power attenuation (%)')

  ax.legend ()

  if logscale :
    ax.set_xscale ('log')

  if filename is not None :
    plt.savefig (filename)
  if show :
    plt.show ()

  return 
  

def a2z_to_cf (df) :
  '''
  Convert a a2z DataFrame into a centile DataFrame.
  '''

  cf = pd.DataFrame (index=np.copy (df.index), columns=list (range (7)))
  cf[0] = df[0].copy ()
  cf[1] = df[1].copy ()
  cf[2] = df[2].copy ()
  cf[3] = df[3].copy ()
  cf[4] = df[4].copy ()
  cf[5] = df[5].copy ()
  cf[6] = df[5].copy ()

  return cf

def amp_to_height (a, gamma) :
  '''
  Convert a mode amplitude parameter to corresponding height.
  '''
  
  h = 2 * a**2 / (np.pi * gamma)

  return h

def height_to_amp (h, gamma) :
  '''
  Convert a mode height parameter to corresponding amplitude.
  '''

  a = np.sqrt (np.pi * gamma * h / 2)

  return a

def fill_hw_with_ref (df, l, l_ref) :
  '''
  Fill height and width values for l=4 and l=5 pkb lines
  when using complete_pkb function.
  '''

  aux = df.loc[df[1]==l, [4,6]]
  aux.update (df.loc[df[1]==l_ref, [4,6]], overwrite=False)
  df.loc[df[1]==l, [4,6]] = aux

  return df

def complete_pkb (pkb, l1_as_ref) :

  '''
  Allow to complete a given pkb with the residuals l=4 and l=5 informations
  for which the default feed is only frequency (useful for GOLF data). The function
  replace the NaN in height, and width and 0 in splittings by adequate parameters.  

  :param pkb: pkb input array
  :type pkb: ndarray

  :param l1_as_ref: if set to True, l1 will be used as a reference for width and height 
    of l4 and l5 modes. To use when l0 modes are not fitted (typically when fitting a pair 
    13).
  :type l1_as_ref: bool

  :return: pkb with l4 and l5 parameters completed.
  :rtype: ndarray
  '''
 
  df = pd.DataFrame (data=pkb)
  df[0] = df[0].map (int)
  df[1] = df[1].map (int)
  n = np.copy (df[0].to_numpy ())
  ratio_4 = 0.0098
  ratio_5 = 0.001

  if l1_as_ref :
    l_ref = 1 
    ref_ratio = 1.8
  else :
    l_ref = 0 
    ref_ratio = 1.

  n[df[1]==4] = n[df[1]==4] + 2
  n[df[1]==5] = n[df[1]==5] + 2

  df = df.set_index (n)
  df = df.sort_values (2, ascending=True)

  df = fill_hw_with_ref (df, 4, l_ref)
  df = fill_hw_with_ref (df, 5, l_ref)

  df.loc[(df[1]==4)&(df[10].isna()), 10] = 0.4 #use fixed splittings
  df.loc[(df[1]==5)&(df[10].isna()), 10] = 0.4 #use fixed splittings
  df.loc[df[1]==4, [5, 7]] = 0. 
  df.loc[df[1]==5, [5, 7]] = 0. 

  df.loc[df[1]==4, 4] = df.loc[df[1]==4, 4] * ratio_4 / ref_ratio
  df.loc[df[1]==5, 4] = df.loc[df[1]==5, 4] * ratio_5 / ref_ratio

  pkb = df.to_numpy ()

  return pkb

def check_a2z (df, strategy='order', verbose=False) :

  '''
  Check bound validity for any a2z DataFrame. Line with ``global`` mention
  will not be checked.
  '''

  df = df.loc[df[3]!='global'] 

  if strategy!='pair':
    if np.any (df[3]=='even') or np.any (df[3]=='odd') :
      raise Exception ('a2z input odd and even keywords can be used only with strategy=pair')

  if np.any (df[4] < df[7]) :
    print ('Guess in a2z DataFrame below low_bounds')
    print (df.loc[df[4]<df[7]])
  if np.any (df[4] > df[8]) :
    print ('Guess in a2z DataFrame below low_bounds')
    print (df.loc[df[4]>df[8]])

  if (np.any (df[4] < df[7]) | np.any (df[4] > df[8]) ) :
    raise Exception ('Guess in a2z DataFrame is outside of provided bounds')

  if verbose :
    print ('Input bounds are ok.')

  return  

def check_bounds (param, low_bounds, up_bounds, labels=None) :
  '''
  Check validity of guess and bounds for pattern and backgrounds fit.
  '''

  if np.any (param > up_bounds) | np.any (param < low_bounds) :
    message = 'Guess is outside of bounds. '
    if np.any (param < low_bounds) :
      message = message + 'The following parameters are below low bounds: '
      message = message + str (labels[param < low_bounds]) + '. '

    if np.any (param > up_bounds) :
      message = message + 'The following parameters are above up bounds: '
      message = message + str (labels[param > up_bounds]) + '. '
    raise Exception (message)

  return

def param_name_to_latex (label, order, degree) :
  '''
  Convert parameter name to Latex formatted
  strings for plotting purpose. 
  '''
  new = None 
  if label=='freq' :
    new = r'$\nu'
  if label=='height' :
    new = r'$H'
  if label=='amplitude' :
    new = r'$A'
  if label=='width' :
    new = r'$\Gamma'
  if label=='split' :
    new = r'$s'
  if label=='proj_split' :
    new = r'$\sin i . s'
  if label=='angle' :
    new = r'$i'
  if label=='asym' :
    new = r'$\alpha'
  if label=='background' :
    new = r'$B'
  if label=='amp_l' :
    new = r'$V'

  if label=='background' or label=='angle' :
    new = new + '$'
  elif label=='amp_l' :
    if degree=='a' :
      # This case should not occur
      warnings.warn ('amp_l parameter has degree set to a.')
      new = new + '_\ell / V_0$'
    else :
      new = new + '_{' + degree + '} / V_0$'
  else :
    if order=='a' :
      new = new + '_{n,'
    else :
      new = new + '_{' + order + ','
    if degree=='a' :
      new = new + '\ell}$'
    else :
      new = new + degree + '}$'

  # ensuring that anyway the function will return a label
  if new is None :
    new = label + '_' + order + '_' + degree
  return new

def param_array_to_latex (labels, orders, degrees) :
  '''
  Convert a list of parameter names to Latex formatted
  strings for plotting purpose. 
  '''
  formatted = []
  for label, order, degree in zip (labels, orders, degrees) :
    formatted.append (param_name_to_latex (label, order, degree))

  return formatted
    

def cornerplot_wrapper (sampler, discard, thin, labels, 
                        norm=None, filemcmc=None, bins=100,
                        format_cornerplot='pdf', flat_input=False,
                        plot_datapoints=True, figsize=(12,12), 
                        fontsize=10, tickfontsize=6, transform=False, 
                        **kwargs) :
  '''
  Wrapper to make cornerplots.

  :param sampler: ``emcee`` sampler.
  :type sampler: Ensemble Sampler

  :param discard: number of steps to discard in the sample 
    when computing the flat chain.
  :type discard: int

  :param thin: chain thinning parameter.
  :type thin: int

  :param labels: parameters labels.
  :type labels: array-like

  :param norm: normalisation factors used for the parameters. 
    Optional, default ``None``. 
  :type norm: ndarray.

  :param transform: if set to ``True``, the exponential of the chain
    will be considered. Optional, default ``False``.
  '''

  if flat_input :
    sample_to_plot = sampler
  else :
    sample_to_plot = sampler.get_chain(discard=discard, thin=thin, flat=True)
  if norm is not None :
    sample_to_plot = sample_to_plot*norm
  if transform :
    sample_to_plot = np.exp (sample_to_plot)
  with plt.rc_context ({'font.size':fontsize, 'xtick.labelsize':tickfontsize, 
                        'ytick.labelsize':tickfontsize}):
    fig = corner.corner(sample_to_plot, bins=bins, labels=labels, quantiles=[0.16,0.5,0.84], 
                        show_titles=True, title_fmt='.2f', plot_datapoints=plot_datapoints,
                        fill_contours=True)
    fig.set_size_inches(*figsize)
    if filemcmc is not None :
      plt.savefig (path.splitext (filemcmc)[0]+'_cornerplot.{}'.format(format_cornerplot), **kwargs) 
    plt.close ()

  return

def update_a2z (old, new) :
  '''
  Update inplace a given a2z DataFrame with the parameters of a second one.
  The way to process is the following: lines of the second for which uncertainties
  are not zero will be used to update the corresponding lines in the old DataFrame.
  
  :param old: a2z DataFrame to update.
  :type old: pandas DataFrame
 
  :param new: a2z DataFrame that will be used for the update. Must be of the same dimension
   and ordered the same way than ``old`` (the function do not perform any order check of the
   elements in both DataFrames). 
  :type new: pandas DataFrame

  :return: None
  '''

  mask = new[5]!=0
  old.loc[mask] = new.loc[mask]

  return

def sort_a2z (df) :
  '''
  Sort a2z DataFrame.
  '''

  df = df.sort_values ([1,0,4,2])

  return df

def sort_pkb (pkb) :
  '''
  Sort pkb array by frequency.
  '''
  
  indexes = np.argsort (pkb[:,2])
  pkb = pkb[indexes]

  return pkb

def read_a2z (a2z_file) :
  '''
  Read a file with a a2z standard syntax (doc to be written) and return
  a2z-style parameters (sorted by orders and degrees).

  :param a2z_file: name of the file to read the parameters.
  :type a2z_file: string

  :return: input parameters as a pandas DataFrame with the a2z syntax.
  :rtype: pandas DataFrame
  '''

  df_a2z = pd.read_csv (a2z_file, sep=' ', header=None)
  df_a2z = sort_a2z (df_a2z)

  return df_a2z

def merge_a2z_df (df1, df2) :
  '''
  Merge two a2z DataFrame.

  :return: a2z merged DataFrame
  :rtype: pandas DataFrame
  '''
 
  columns = [0, 1, 2, 3, 4, 5, 6, 7, 8]
  df1 = df1[columns]
  df2 = df2[columns]

  df = pd.concat ([df1, df2])

  return df

def merge_a2z_file (file1, file2) :
  '''
  Read a2z file and merge a2z corresponding DataFrame.

  :return: a2z merged DataFrame
  :rtype: pandas DataFrame
  '''
 
  df1 = read_a2z (file1)
  df2 = read_a2z (file2)

  df = merge_a2z_df (df1, df2)

  return df

def save_pkb (filename, pkb, author=None, spectro=False, extended=False,
              fmt=None, projected_splittings=False, nwalkers=None, nsteps=None,
              discard=None, fit_amp=False) :
  '''
  Save pkb file with dedicated header.
  '''

  header = make_header_pkb (extended=extended, author=author, spectro=spectro,
                            projected_splittings=projected_splittings, nwalkers=nwalkers,
                            nsteps=nsteps, discard=discard, fit_amp=fit_amp)
  if fmt is None :
    if extended :
      fmt = ['%.0f', '%.0f', '%.4f', '%.4f', '%.4f', '%.4f', '%.4f', '%.4f',
             '%.4f', '%.4f', '%.4f', '%.4f', '%.4f', '%.4f', '%.4f', '%.4f',
             '%.4f', '%.4f', '%.4f', '%.4f',]
    else :
      fmt = ['%.0f', '%.0f', '%.4f', '%.4f', '%.4f', '%.4f', '%.4f', '%.4f',
             '%.4f', '%.4f', '%.4f', '%.4f', '%.4f', '%.4f']
  np.savetxt (filename, pkb, header=header, fmt=fmt)

  return

def save_a2z (filename, df) :
  '''
  Write with a a2z standard syntax (doc to be written).

  :param filename: name of the file where to write the parameters.
  :type filename: string
  '''

  df.to_csv (filename, sep=' ', header=False, index=False)
  
  return

def a2z_df_to_param (df, give_n_l=False, fit_amp=False) :
  '''
  Convert df_a2z to param_a2z tuple useful to feed the log_likelihood and the
  scipy minimize function.

  :param df: input parameters as a pandas DataFrame with the a2z syntax.
  :type df: pandas DataFrame

  :param give_degree: if set to ``True``, will also send back a vector with the
  degree of the corresponding parameters. Optional, default ``False``. 
  :type give_degrees: bool

  :param fit_amp: if fit_amp, height values will be transformed according to gamma values.
    Optional, default ``False``.
  :type fit_amp: bool
  '''
  df_to_fit = df.loc[df[6]==0].copy ()
      

  param_to_fit = df_to_fit[4].to_numpy ()
  param_type = df_to_fit[2].to_numpy ()
  bounds_to_fit = df_to_fit [[7,8]].to_numpy ()

  orders = df_to_fit[0].to_numpy ()
  degrees = df_to_fit[1].to_numpy ()

  if fit_amp :
    for ii, (p_type, o, d) in enumerate (zip (param_type, orders, degrees)) :
      if p_type=='height' :
         if np.any ( (df[0]==o) & (df[1]==d) & (df[2]=='width') ) :
           gamma = df.loc[(df[0]==o) & (df[1]==d) & (df[2]=='width'), 4].to_numpy () [0]
         elif np.any ( (df[0]==o) & (df[1]=='a') & (df[2]=='width') ) :
           gamma = df.loc[(df[0]==o) & (df[1]=='a') & (df[2]=='width'), 4].to_numpy () [0]
         elif np.any ( (df[0]=='a') & (df[1]=='a') & (df[2]=='width') ) :
           gamma = df.loc[(df[0]=='a') & (df[1]=='a') & (df[2]=='width'), 4].to_numpy () [0]
         param_to_fit[ii] = height_to_amp (param_to_fit[ii], gamma)
         bounds_to_fit[ii, 0] = height_to_amp (bounds_to_fit[ii, 0], gamma)
         bounds_to_fit[ii, 1] = height_to_amp (bounds_to_fit[ii, 1], gamma)
   
  if give_n_l :
    return param_to_fit, param_type, bounds_to_fit, degrees, orders
  else :
    return param_to_fit, param_type, bounds_to_fit

def a2z_to_pkb (df_a2z, nopandas=True) :
  '''
  Take a2z dataframe and return pkb_style parameters. Frequency units are given in µHz and not Hz. pkb format is the following: 

  +------------+---+---+-----+----------+-----------+--------------+-------+-------------+--------+-------------+-------+-------------+------+------------+
  | parameters | n | l | nu  | nu_error | height    | height_error | width | width_error | angle  | angle_error | split | split_error | asym | asym_error |
  +------------+---+---+-----+----------+-----------+--------------+-------+-------------+--------+-------------+-------+-------------+------+------------+
  | units      | . | . | µHz | µHz      | power/µHz | power/µHz    | µHz   | µHz         | degree | degree      | µHz   | µHz         | .    | .          |
  +------------+---+---+-----+----------+-----------+--------------+-------+-------------+--------+-------------+-------+-------------+------+------------+

  :param df_a2z: input parameters as a pandas DataFrame with the a2z syntax.
  :type df_a2z: pandas DataFrame

  :return: array under pkb format. 
  :rtype: ndarray
  '''
  
  if nopandas :
    return wrapper_a2z_to_pkb_nopandas (df_a2z)
  else :
    raise Exception ('nopandas=False is deprecated and cannot be used anymore.')
    
def pkb_to_df (pkb, latex_names=True) :
  '''
  Convert a pkb array into a tabular latex string

  :param pkb: pkb array
  :type: ndarray

  :return: latex tabular
  :rtype: str
  '''

  if pkb.shape[1]==20 :
    if latex_names :
      columns = [r'$n$', r'$\ell$', r'$\nu$', r'$\sigma_{\nu,-}$', r'$\sigma_{\nu,+}$',
                 r'$H$', r'$\sigma_{H,-}$', r'$\sigma_{H,+}$', 
                 r'$\Gamma$', r'$\sigma_{\Gamma,-}$', r'$\sigma_{\Gamma,+}$',
                 r'$i$', r'$\sigma_{i,-}$', r'$\sigma_{i,+}$',
                 r'$s$', r'$\sigma_{s,-}$', r'$\sigma_{s,+}$',
                 r'$\alpha$', r'$\sigma_{\alpha,-}$', r'$\sigma_{\alpha,+}$'] 
    else :
      columns = ['n', 'l', 'nu', 'sigma_nu_-', 'sigma_nu_+',
                 'H', 'sigma_H_-', 'sigma_H_+', 
                 'Gamma', 'sigma_Gamma_-', 'sigma_Gamma_+',
                 'i', 'sigma_i_-', 'sigma_i_+',
                 's', 'sigma_s_-', 'sigma_s_+', 
                 'alpha', 'sigma_alpha_-', 'sigma_alpha_+'] 
  else :
    if latex_names :
      columns = [r'$n$', r'$\ell$', r'$\nu$', r'$\sigma_{\nu}$',
                 r'$H$', r'$\sigma_{H}$' 
                 r'$\Gamma$', r'$\sigma_{\Gamma}$',
                 r'$i$', r'$\sigma_{i}$',
                 r'$s$', r'$\sigma_{s}$',
                 r'$\alpha$', r'$\sigma_{\alpha}$'] 
    else :
      columns = ['n', 'l', 'nu', 'sigma_nu',
                 'H', 'sigma_H', 
                 'Gamma', 'sigma_Gamma',
                 'i', 'sigma_i', 
                 's', 'sigma_s', 
                 'alpha', 'sigma_alpha'] 
  df = pd.DataFrame (data=pkb, columns=columns)
  if latex_names :
    df[r'$n$'] = df[r'$n$'].map (int)
    df[r'$\ell$'] = df[r'$\ell$'].map (int)
  else :
    df['n'] = df['n'].map (int)
    df['l'] = df['l'].map (int)

  return df

def pkb_to_latex (pkb, buf=None, caption=None, label=None) :
  '''
  Convert a pkb array into a tabular latex string.

  :param pkb: pkb array
  :type: ndarray

  :return: latex tabular
  :rtype: str
  '''

  df = pd.DataFrame (data=pkb)
  df[0] = df[0].map (int)
  df[1] = df[1].map (int)
  tab = df[[0,1]].copy ()
  tab = tab.rename (columns={0:r'$n$', 1:r'$\ell$'})
  if pkb.shape[1]==20 :
    txt = '${0:.2f}_{{-{1:.2f}}}^{{+{2:.2f}}}$'
    tab[r'$\nu$'] = df.apply (lambda df : txt.format (df[2], df[3], df[4]), axis=1)
    tab[r'$H$'] = df.apply (lambda df : txt.format (df[5], df[6], df[7]), axis=1)
    tab[r'$\Gamma$'] = df.apply (lambda df : txt.format (df[8], df[9], df[10]), axis=1)
    tab[r'$i$'] = df.apply (lambda df : txt.format (df[11], df[12], df[13]), axis=1)
    tab[r'$s$'] = df.apply (lambda df : txt.format (df[14], df[15], df[16]), axis=1)
    tab[r'$\alpha$'] = df.apply (lambda df : txt.format (df[17], df[18], df[19]), axis=1)
  else :
    txt = '${{0:.2f}} \pm {{1:.2f}}$'
    tab[r'$\nu$'] = df.apply (lambda df : txt.format (df[2], df[3]), axis=1)
    tab[r'$H$'] = df.apply (lambda df : txt.format (df[4], df[5]), axis=1)
    tab[r'$\Gamma$'] = df.apply (lambda df : txt.format (df[6], df[7]), axis=1)
    tab[r'$i$'] = df.apply (lambda df : txt.format (df[8], df[9]), axis=1)
    tab[r'$s$'] = df.apply (lambda df : txt.format (df[10], df[11]), axis=1)
    tab[r'$\alpha$'] = df.apply (lambda df : txt.format (df[12], df[13]), axis=1)

  latex_tabular = tab.to_latex (index=False, escape=False, buf=buf,
                                caption=caption, label=label)

  return latex_tabular

def input_to_pkb (param_to_fit, df_info_modes, df_global) :
  '''
  Take a2z parameter and corresponding auxiliary array (giving modes information
  that are not supposed to change when minimising, e.g. order, degree, etc.) 
  and return pkb_style parameters useful to feed the compute_model
  function.

  :return: input parameter using pkb syntax
  :rtype: ndarray
  '''
  df_info_modes[4] = param_to_fit
  df_a2z = pd.concat([df_info_modes, df_global])
  param_pkb = a2z_to_pkb (df_a2z)

  return param_pkb


def smooth (vector, smoothing, win_type='triang',
            statistic='mean') :
  '''
  Smooth routines. Uses triangle smoothing by default

  :param vector: vector to smooth.
  :type vector: ndarray

  :param smoothing: size of the rolling window used for the smooth.
  :type smoothing: int

  :param win_type: see ``scipy.signal.windows``. Optional, default ``triang``.
  :type win_type: str

  :param statistic: Allow choosing between ``mean`` and ``median``.
     If ``median`` is chosen , ``win_type=None`` will automatically beused.
     Optional, default ``mean``.
  :type statistic: str

  :return: smoothed vector
  :rtype: ndarray
  '''
  smoothed = pd.Series (data=vector)
  if statistic=='mean' : 
    smoothed = smoothed.rolling (smoothing, min_periods=1, 
                                 center=True, win_type=win_type).mean ()
  elif statistic=='median' : 
    smoothed = smoothed.rolling (smoothing, min_periods=1, 
                                 center=True, win_type=None).median ()
  return smoothed

def read_pkb (pkb_file) :
  '''
  Read a pkb file and return the parameters.
  :param pkb_file: name of the pkb file.
  :type pkb_file: str

  :return: an array with the parameters given by the file.  
  :rtype: ndarray

  ..note:: format reminder :
  parameters=[n,l,nu,nu_error,height,height_error,width,width_error,angle,angle_error,split, split_error]
  units=[integer,integer,uHz,uHz,ppm2uHz,ppm2uHz,uHz,uHz,deg,deg,uHz,uHz]
  '''
  param_pkb = np.loadtxt (pkb_file, skiprows=4)
  return param_pkb

@numba.jit (nopython=True)
def compute_model (freq, param_pkb, param_wdw=None, correct_width=1., instr='kepler',
                   use_sinc=False, asym_profile='nigam-kosovichev', fit_amp=False, 
                   projected_splittings=False) :

  '''
  Compute a p-mode model from a given set of parameters.

  :param freq: frequency vector.
  :type freq: ndarray

  :param param_pkb: parameters contained in the pkb files.
  :type param_pkb: ndarray

  :param param_wdw: parameters given by the analysis of the window.
  :type param_wdw: ndarray

  :param correct_width: param to adjust the width of the Lorentzian if it has been manually modified 
    during the fitting
  :type correct_width: float 

  :param instr: instrument to consider (amplitude ratio inside degrees depend on geometry 
    AND instrument and should be adaptated). Possible argument : ``geometric``, ``kepler``, ``golf``, ``virgo``.
  :type instr: str

  :param use_sinc: if set to ``True``, mode profiles will be computed using cardinal sinus and not Lorentzians.
    No asymmetry term will be used if it is the case. Optional, default ``False``.
  :type use_sinc: bool

  :param asym_profile: depending on the chosen argument, asymmetric profiles will be computed following Korzennik 2005 (``korzennik``)
    or Nigam & Kosovichev 1998 (``nigam-kosovichev``). 
  :type asym_profile: str

  :param fit_amp: if set to ``True``, the function consider that it got amplitudes and not heights as input parameters.
    Optional, default ``False``.
  :type fit_amp: bool

  :param projected_splittings: if set to ``True``, the function will consider that the ``split`` parameters of the input are projected 
    splittings and will build the model consequently. Optional, default ``False``. 
  :type projected_splittings: bool

  :return: computed model
  :rtype: ndarray
  '''

  model = np.zeros (freq.size)

  if param_pkb.shape[1]==20 :
    subset = np.array ([0,1,2,3,5,6,8,9,11,12,14,15,17,18])
    param_pkb = param_pkb[:,subset]

  for elt in param_pkb :
  
    angle = 2 * np.pi * elt[8] / 360.

    if projected_splittings :
      if elt[8] != 0 :
        splitting = elt[10] / np.sin (angle)
      else :
        splitting = 0 
    else :
      splitting = elt[10]

    for m in range (int(-1*elt[1]), int (elt[1]) + 1) :

      if fit_amp :
        H = 2 * elt[4]**2 / (np.pi * elt[6]) 
      else :
        H = elt[4]

      if param_wdw is not None :
        for elt_wdw in param_wdw :
          nu0 = elt[2] + m*splitting + elt_wdw[1] 
          G = elt[6] * correct_width
          asym = elt[12]
          A = ampl_mode (int(elt[1]), m, angle, np.sin (angle), np.cos (angle), instr=instr) * H * elt_wdw[0] 

          if A > 0 : #avoid computing null terms
            xxx = (freq - nu0) / G
            if not use_sinc :
              if asym_profile=='korzennik' :
                num = A * (1 + asym*(xxx - asym/2.))
              if asym_profile=='nigam-kosovichev' :
                num = A * ((1 + asym*xxx)*(1 + asym*xxx) + asym*asym)
              if np.any (num < 0) :
                return np.full (model.size, np.inf) #avoid case where asymetries make a negative height
              model += num / (1. + 4. * xxx * xxx) 
            else :
              model += A * np.sinc (xxx) * np.sinc (xxx)

      else :
        nu0 = elt[2] + m*splitting
        G = elt[6]
        asym = elt[12]
        A = ampl_mode (int (elt[1]), m, angle, np.sin (angle), np.cos (angle), instr=instr) * H 

        if A > 0 : #avoid computing null terms
          xxx = (freq - nu0) / G
          if not use_sinc :
            if asym_profile=='korzennik' :
              num = A * (1 + asym*(xxx - asym/2.))
            if asym_profile=='nigam-kosovichev' :
              num = A * ((1 + asym*xxx)*(1 + asym*xxx) + asym*asym)
            if np.any (num < 0) :
              return np.full (model.size, np.inf) #avoid case where asymetries make a negative height
            model += num / (1. + 4. * xxx * xxx) 
          else :
            model += A * np.sinc (xxx) * np.sinc (xxx)

  return model

def plot_from_param (param_pkb, freq, psd, back=None, wdw=None, smoothing=50, spectro=True, correct_width=1.,
                     show=False, filename=None, instr='geometric', use_sinc=False, asym_profile='korzennik',
                     projected_splittings=False, **kwargs) :
  """
  Plot the results of a fit according to an input given with a pkb format.

  :param param_pkb: parameters contained in the pkb files.
  :type param_pkb: ndarray

  :param freq: frequency vector, must be given in muHz.
  :type freq: ndarray

  :param psd: real power vector of the observed data. 
  :type psd: ndarray

  :param back: real power vector of the fitted background. 
  :type back: ndarray

  :param wdw: set to ``True`` if the mode have been fitted using the sidelobes fitting method, default ``False``.
  :type wdw: bool

  :param smoothing: size of the rolling window used to smooth the psd in the plot.
  :type smoothing: int

  :param spectro: set to ``True`` if the instruments uses spectroscopy, set the units in m/s instead of ppm, default ``True``.
  :type spectro: bool

  :param correct_width: param to adjust the width of the Lorentzian if it has been manually modified 
    during the fitting
  :type correct_width: float 

  :param show: automatically show the plot, default ``False``.
  :type show: bool

  :param instr: instrument to consider (amplitude ratio inside degrees depend on geometry 
    AND instrument and should be adaptated). Possible argument : ``geometric``, ``kepler``, ``golf``,
    ``virgo``. Optional, default ``geometric``. 
  :type instr: str

  :param use_sinc: if set to ``True``, mode profiles will be computed using cardinal sinus and not Lorentzians.
    No asymmetry term will be used if it is the case. Optional, default ``False``.
  :type use_sinc: bool

  :param asym_profile: depending on the chosen argument, asymmetric profiles will be computed following Korzennik 2005 (``korzennik``)
    or Nigam & Kosovichev 1998 (``nigam-kosovichev``). 
  :type asym_profile: str

  :return: ``None``
  """

  if wdw is not None :
    param_wdw = sidelob_param (wdw, dt=1./(2*1.e-6*freq[-1]), do_tf=True)
    model = compute_model (freq, param_pkb, param_wdw=param_wdw, correct_width=correct_width, instr=instr,
                           use_sinc=use_sinc, asym_profile=asym_profile, projected_splittings=projected_splittings) 
  else :  
    model = compute_model (freq, param_pkb, instr=instr, use_sinc=use_sinc, asym_profile=asym_profile,
                           projected_splittings=projected_splittings) 

  if back is not None :
    model = model + back

  #Computing residuals, smoothed PSD, etc.
  quot_residuals = psd / model 
  smooth_psd = smooth (psd, smoothing)
  freq_peak = param_pkb [:,2]
  if param_pkb.shape[1]==20 :
    height_peak = param_pkb [:,5]
    height_error_peak = param_pkb [:,[6,7]] 
    width_peak = param_pkb [:,8]
    width_error_peak = param_pkb [:,[9,10]] 
    freq_error = param_pkb [:,[3,4]]
  else :
    height_peak = param_pkb [:,4]
    height_error_peak = param_pkb [:,5] 
    width_peak = param_pkb [:,6]
    width_error_peak = param_pkb [:,7] 
    freq_error = param_pkb [:,3]
  l_peak = param_pkb [:,1].astype (int)

  # Sub ensembles for with and height representation
  # (one color for each l value)
  i0, = np.where (l_peak == 0)
  i1, = np.where (l_peak == 1)
  i2, = np.where (l_peak == 2)
  i3, = np.where (l_peak == 3)
  f0 = freq_peak[i0]
  f1 = freq_peak[i1]
  f2 = freq_peak[i2]
  f3 = freq_peak[i3]
  ef0 = np.transpose (freq_error[i0])
  ef1 = np.transpose (freq_error[i1])
  ef2 = np.transpose (freq_error[i2])
  ef3 = np.transpose (freq_error[i3])
  h0 = height_peak[i0]
  h1 = height_peak[i1]
  h2 = height_peak[i2]
  h3 = height_peak[i3]
  eh0 = np.transpose (height_error_peak[i0])
  eh1 = np.transpose (height_error_peak[i1])
  eh2 = np.transpose (height_error_peak[i2])
  eh3 = np.transpose (height_error_peak[i3])
  w0 = width_peak[i0]
  w1 = width_peak[i1]
  w2 = width_peak[i2]
  w3 = width_peak[i3]
  ew0 = np.transpose (width_error_peak[i0])
  ew1 = np.transpose (width_error_peak[i1])
  ew2 = np.transpose (width_error_peak[i2])
  ew3 = np.transpose (width_error_peak[i3])

  fig = plt.figure (figsize=(10,10))
  capsize=2.5
  labelpad=0
  slabel=9

  #PSD centered on fitted p-mode
  ax1 = fig.add_subplot (321) 
  cond = (freq > np.amin (param_pkb[:,2])-50.)&(freq < np.amax (param_pkb[:,2])+50.)

  ax1.plot (freq[cond], psd[cond], color='grey') 
  ax1.plot (freq[cond], smooth_psd[cond], color='black') 
  ax1.plot (freq[cond], model[cond], color='red') 

  #Global PSD (log-scale)
  ax2 = fig.add_subplot (322) 
  ax2.set_xscale ('log')
  ax2.set_yscale ('log')

  ax2.plot (freq, psd, color='grey') 
  ax2.plot (freq, smooth_psd, color='black') 
  ax2.plot (freq, model, color='red') 

  #Residual / (background+mode)
  ax3 = fig.add_subplot (323, sharex=ax1) 
  ax3.plot (freq[cond], quot_residuals[cond], color='black') 
  ax3.plot (freq[cond], smooth(quot_residuals, 20)[cond], color='blue') 
  ax3.plot (freq[cond], smooth(quot_residuals, 50)[cond], color='cornflowerblue') 
  ax3.plot (freq[cond], smooth(quot_residuals, 100)[cond], color='lightsteelblue') 

  ax3.set_ylim (0., 10)

  #Height
  ax4 = fig.add_subplot (324, sharex=ax1) 
  ax4.errorbar (f0, h0, yerr=eh0, marker='x', fmt=' ', color='red', label=r'$\ell = 0$', capsize=capsize)
  ax4.errorbar (f1, h1, yerr=eh1, marker='x', fmt=' ', color='blue', label=r'$\ell = 1$', capsize=capsize)
  ax4.errorbar (f2, h2, yerr=eh2, marker='x', fmt=' ', color='deepskyblue', label=r'$\ell = 2$', capsize=capsize)
  ax4.errorbar (f3, h3, yerr=eh3, marker='x', fmt=' ', color='gold', label=r'$\ell = 3$', capsize=capsize)
  ax4.legend (fontsize=slabel, ncol=2)

  #Width
  ax5 = fig.add_subplot (325, sharex=ax1) 
  ax5.errorbar (f0, w0, yerr=ew0, marker='x', fmt=' ', capsize=capsize, color='red')
  ax5.errorbar (f1, w1, yerr=ew1, marker='x', fmt=' ', capsize=capsize, color='blue')
  ax5.errorbar (f2, w2, yerr=ew2, marker='x', fmt=' ', capsize=capsize, color='deepskyblue')
  ax5.errorbar (f3, w3, yerr=ew3, marker='x', fmt=' ', capsize=capsize, color='gold')

  #label

  ax1.set_xlabel (r'Frequency ($\mu$Hz)', labelpad=labelpad, size=slabel)
  ax2.set_xlabel (r'Frequency ($\mu$Hz)', labelpad=labelpad, size=slabel)
  ax3.set_xlabel (r'Frequency ($\mu$Hz)', labelpad=labelpad, size=slabel)
  ax4.set_xlabel (r'Frequency ($\mu$Hz)', labelpad=labelpad, size=slabel)
  ax5.set_xlabel (r'Frequency ($\mu$Hz)', labelpad=labelpad, size=slabel)
  ax5.set_ylabel (r'Width ($\mu$Hz)', size=slabel)
  if spectro == True :
    ax1.set_ylabel (r'PSD (m$^2$.s$^{-2}$/$\mu$Hz)', size=slabel)
    ax2.set_ylabel (r'PSD (m$^2$.s$^{-2}$/$\mu$Hz)', size=slabel)
    ax3.set_ylabel (r'PSD/(back+model)', size=slabel)
    ax4.set_ylabel (r'Height (m$^2$.s$^{-2}$/$\mu$Hz)', size=slabel)
  else :
    ax1.set_ylabel (r'PSD (ppm$^2$/$\mu$Hz)', size=slabel)
    ax2.set_ylabel (r'PSD (ppm$^2$/$\mu$Hz)', size=slabel)
    ax3.set_ylabel (r'PSD/(back+model)', size=slabel)
    ax4.set_ylabel (r'Height (ppm$^2$/$\mu$Hz)', size=slabel)

  ax1.tick_params(direction='in', labelsize=8, top=True, right=True)
  ax2.tick_params(direction='in', labelsize=8, top=True, right=True)
  ax3.tick_params(direction='in', labelsize=8, top=True, right=True)
  ax4.tick_params(direction='in', labelsize=8, top=True, right=True)
  ax5.tick_params(direction='in', labelsize=8, top=True, right=True)

  #Echelle diagram
  try :
    dnu = np.median (np.diff (param_pkb[param_pkb[:,1]==0,2]))
    n_order_fitted = param_pkb[param_pkb[:,1]==0].shape[0]
    n_dnu = max (n_order_fitted, 6)
    center = np.mean (param_pkb[:,2])
    vmin = np.amin ((psd/back)[(freq > center - n_dnu * dnu)&(freq < center + n_dnu * dnu)])
    vmax = 0.1 * np.amax ((psd/back)[(freq > center - n_dnu * dnu)&(freq < center + n_dnu * dnu)])
    if vmin > vmax :
      vmin = 0
    echelle_diagram (freq, psd/back, dnu, twice=False, fig=fig, index=326,
                     smooth=20, 
                     cmap='Greys', 
                     mode_freq=(f0, f1, f2, f3), 
                     mode_freq_err=(ef0, ef1, ef2, ef3), 
                     scatter_color=('red', 'blue', 'deepskyblue', 'gold'),
                     mec=('red', 'blue', 'deepskyblue', 'gold'),
                     capsize=3, 
                     fmt=('o', 'D', '^', 'h'), 
                     mfc='none', ms=8,
                     vmin=vmin,  
                     vmax=vmax,
                     ylim=(freq[(freq > center - n_dnu * dnu)&(freq < center + n_dnu * dnu)][0],
                           freq[(freq > center - n_dnu * dnu)&(freq < center + n_dnu * dnu)][-1]),
                     shading='gouraud')
    ax6 = fig.get_axes ()[-1]
    ax6.tick_params(direction='in', labelsize=8, top=True, right=True)
    ax6.xaxis.label.set_size (slabel)
    ax6.yaxis.label.set_size (slabel)
   
  except (FloatingPointError, RuntimeWarning, ValueError) :
    warnings.warn ("Echelle diagram could not be computed on summary plot.", Warning)

  if filename is not None :
    plt.savefig (filename, **kwargs)
  if show==True :
    plt.show()
  plt.close ()
  return 


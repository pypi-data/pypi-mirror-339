import numpy as np
import pandas as pd
import emcee
import corner
from .likelihood import log_likelihood, cond_transf
from .fit_tools import *
from .analyse_window import sidelob_param
from .save_chain import save_sampled_chain
import matplotlib
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
import dill
from pathos.multiprocessing import ProcessPool
from multiprocessing import Pool
from os import path
import glob
import os
from os import path

def log_prior (bounds, param=None, param_type=None) :

  '''
  Compute the positive log prior probability of the parameters to estimate.
  By default, uniform distribution laws are assumed.

  :param bounds: for parameters with assumed prior uniform distribution, bounds of 
  the uniform distribution.
  :type bounds: ndarray

  :param param: parameters to fit. Optional, default None.
  :type param: 1d ndarray

  :param param_type: array of string giving the param type of the param to fit, eg
  'freq', 'height', 'width', 'amp_l', 'split'. Optional, default None.  
  :type param_type: ndarray

  :return: prior value for the given parameters.
  :rtype: float
  '''

  cond = (param<bounds[:,0])|(param>bounds[:,1])
  if np.any (cond) :
    return - np.inf

  individual_prior = np.ones (param.size) #assuming uniform law for all given parameters.

  if param_type is not None :
    angle = param_type=='angle'
    individual_prior[angle] = np.sin (2*np.pi*param[angle]/360.)

  prior = np.prod (individual_prior) 
  l_prior = np.log (prior)

  return l_prior

def log_probability (param_to_fit, param_type, freq, psd, back, df_a2z, transform, bounds, param_wdw=None,
                     norm=None, instr='kepler', use_sinc=False, asym_profile='korzennik', fit_amp=False,
                     projected_splittings=False) :
  '''
  Compute the positive posterior log probability (unnormalised) of the parameters to fit. 

  :param_to_fit: parameter that scipy.optimize minimize will use to find the
  minimum of the function. Created by a2z_df_to_param function.
  :type param_to_fit: 1d ndarray
 
  :param param_type: array of string giving the param type of the param to fit, eg
  'freq', 'height', 'width', 'amp_l', 'split'. 
  :type param_type: ndarray

  :param freq: frequency vector
  :type freq: ndarray

  :param psd: real power vector
  :type freq: ndarray

  :param df_a2z: global pandas DataFrame wrapping global parameters needed to design the model.
  :type df_a2z: pandas DataFrame.

  :param transform: list of parameter that are given in natural log by the calling routine and that
  will be retransformed. If None, the function will consider that all parameters have been give as
  logarithm. 
  :type transform: tuple of strings

  :param bounds: for parameters with assumed prior uniform distribution, bounds of 
  the uniform distribution.
  :type bounds: ndarray

  :param param_wdw: parameters of the observation window timeseries. Optional, default None. 
  :type wdw: ndarray.

  :param norm: if given, the param_to_fit and bounds input vectors will be multiplied by this vector. 
  Optional, default None.
  :type norm: ndarray

  :param instr: instrument to consider (amplitude ratio inside degrees depend on geometry 
  AND instrument and should be adaptated). Possible argument : 'kepler', 'golf', 'virgo'.
  :type instr: str

  :param use_sinc: if set to ``True``, mode profiles will be computed using cardinal sinus and not Lorentzians.
    No asymmetry term will be used if it is the case. Optional, default ``False``.
  :type use_sinc: bool

  :param asym_profile: depending on the chosen argument, asymmetric profiles will be computed following Korzennik 2005 (``korzennik``)
    or Nigam & Kosovichev 1998 (``nigam-kosovichev``). 
  :type asym_profile: str

  :return: posterior probability value
  :rtype: float
  '''

  if norm is not None :
    param_to_fit = param_to_fit * norm
    bounds[:,0] = bounds[:,0] * norm
    bounds[:,1] = bounds[:,1] * norm

  l_prior = log_prior (bounds, param_to_fit, param_type)

  if not np.isfinite (l_prior) :
    return - np.inf 

  l_likelihood = - log_likelihood (param_to_fit, param_type, freq, psd, back, df_a2z, transform, instr=instr,
                                   param_wdw=param_wdw, use_sinc=use_sinc, asym_profile=asym_profile, fit_amp=fit_amp,
                                   projected_splittings=projected_splittings)

  l_proba = l_prior + l_likelihood

  return l_proba

def sort_chain (labels, degrees, flatchain) :
  '''
  Sort chains to have fitted parameters in alphabetical order in the corner plot.
  '''

  aux_flat = np.copy (flatchain)

  sort1 = np.argsort (labels)
  labels = labels[sort1]
  degrees = degrees[sort1]
  aux_flat = aux_flat[:,sort1]

  sort2 = np.argsort(degrees)
  labels = labels[sort2]  
  degrees = degrees[sort2]
  aux_flat = aux_flat[:,sort2]

  return labels, degrees, aux_flat

def explore_distribution (result, param_type, freq, psd, back, df_a2z, bounds,
                          low_bound_freq=1500, up_bound_freq=5000, param_wdw=None, nsteps=1000,
                          filename=None, parallelise=False, progress=False, nwalkers=64, normalise=False,
                          degrees=None, orders=None, instr='kepler', use_sinc=False,
                          asym_profile='korzennik', save_only_after_sampling=False, fit_amp=False,
                          projected_splittings=False, existing_chains='read') :

  '''
  Use a MCMC to explore the distribution around the maximum likelihood estimation results. 

  :param result: result vector of the MLE process. Be careful that the right parameters are 
  given in log (those with assumed posterior log-normal distribution).
  :type result: ndarray

  :param param_type: array of string giving the param type of the param to fit, eg
  'freq', 'height', 'width', 'amp_l', 'split'. 
  :type param_type: ndarray

  :param freq: frequency vector
  :type freq: ndarray

  :param psd: real power vector
  :type freq: ndarray

  :param df_a2z: global pandas DataFrame wrapping global parameters needed to design the model.
  :type df_a2z: pandas DataFrame.

  :param transform: list of parameter that are given in natural log by the calling routine and that
  will be retransformed. If None, the function will consider that all parameters have been give as
  logarithm. 
  :type transform: tuple of strings

  :param bounds: for parameters with assumed prior uniform distribution, bounds of 
  the uniform distribution.
  :type bounds: ndarray

  :param param_wdw: parameters of the observation window timeseries. Optional, default None. 
  :type wdw: ndarray.

  :param filename: name of the hdf5 where to store the chain. If filename is None, the name will not
  be stored. Optional, default None.
  :type filename: string

  :param parallelise: If set to True, use Python multiprocessing tool to parallelise process.
  Optional, default False.
  :type parallelise: bool

  :param degrees: vector containing degrees of the parameters to fit. If given, will be stored in the .dat
  file. Optional, default None.
  :type degrees: ndarray

  :param instr: instrument to consider (amplitude ratio inside degrees depend on geometry 
  AND instrument and should be adaptated). Possible argument : 'kepler', 'golf', 'virgo'.
  :type instr: str

  :param use_sinc: if set to ``True``, mode profiles will be computed using cardinal sinus and not Lorentzians.
    No asymmetry term will be used if it is the case. Optional, default ``False``.
  :type use_sinc: bool

  :param asym_profile: depending on the chosen argument, asymmetric profiles will be computed following Korzennik 2005 (``korzennik``)
    or Nigam & Kosovichev 1998 (``nigam-kosovichev``). 
  :type asym_profile: str

  :return: the MCMC sampler after exploring the distribution.
  :rtype: emcee.EnsembleSampler
  '''
 
  if save_only_after_sampling and existing_chains=='sample' :
    raise Exception ("save_only_after_sampling=True and existing_chains='sample' are incompatible options.")
 
  psd_to_fit = psd / back

  aux_freq = freq[(freq>low_bound_freq)&(freq<up_bound_freq)]
  aux_psd = psd_to_fit[(freq>low_bound_freq)&(freq<up_bound_freq)]
  aux_back = back[(freq>low_bound_freq)&(freq<up_bound_freq)]

  transform = ('height', 'width')
  cond = cond_transf (param_type, transform=transform)
  result[cond] = np.log (result[cond])

  lower_bounds = bounds [:,0]
  upper_bounds = bounds [:,1]
  lower_bounds[cond] = np.log(lower_bounds[cond])
  upper_bounds[cond] = np.log(upper_bounds[cond])

  # adding free constant for background
  result = np.append (result, 1.)
  lower_bounds = np.append (lower_bounds, 1e-6)
  upper_bounds = np.append (upper_bounds, 5.)
  param_type = np.append (param_type, 'background')
  degrees = np.append (degrees, 'a')
  orders = np.append (orders, 'a')

  #normalisation step
  if normalise :
    norm = np.abs (result)
  else :
    norm = np.ones (result.size)
  result = result / norm
  lower_bounds = lower_bounds / norm
  upper_bounds = upper_bounds / norm

  bounds = np.c_[lower_bounds, upper_bounds]

  pos = result + 1e-4 * np.random.randn(nwalkers, result.size)
  nwalkers, ndim = pos.shape

  if filename is not None :
    if path.exists (filename) :
      if existing_chains=='read' :
        print (filename + " already exists, existing chains set to 'read', no sampling has been performed, proceeding to next step.")
        sampler = emcee.backends.HDFBackend(filename, read_only=True)
        return sampler, norm, param_type, orders, degrees
      elif existing_chains=='ignore' :
        print (filename + " already exists, existing chains set to 'ignore', proceeding to next step.")
        return None, None, None, None #this way, no sampling is performed and the existing file is left untouched
      elif existing_chains=='reset' :
        os.remove (filename)
        backend = emcee.backends.HDFBackend(filename)
        backend.reset(nwalkers, ndim)  
        print (filename + " already exists, existing chains set to 'reset', file has been deleted and a new file has been created instead.")
      elif existing_chains=='sample' :
        backend = emcee.backends.HDFBackend(filename)
        pos = None
        print (filename + " already exists, existing chains set to 'sample', sampling will restart from where it stopped.")
    else :
      backend = emcee.backends.HDFBackend(filename)
      backend.reset(nwalkers, ndim)  
    if save_only_after_sampling :
      # I have deliberately created the file to signal to other process that this chain is being
      # sampled
      backend = None
    #saving parameters name and normalisation information
    filename_info = filename[:len(filename)-3] + '.dat'
    if degrees is not None :
      np.savetxt (filename_info, np.c_[param_type, norm, degrees], fmt='%-s',
                  header=make_header_utility_file ()) 
    else :
      np.savetxt (filename_info, np.c_[param_type, norm], fmt='%-s',
                  header=make_header_utility_file ()) 
  else :
    backend = None

  if parallelise :
    pool = ProcessPool ()
  else :
    pool = None

  sampler = emcee.EnsembleSampler(nwalkers, ndim, log_probability, 
                                  args=(param_type, aux_freq, aux_psd, aux_back, 
                                        df_a2z, transform, bounds, param_wdw, norm, instr,
                                        use_sinc, asym_profile, fit_amp, projected_splittings),
                                  backend=backend, pool=pool)
  sampler.run_mcmc(pos, nsteps, progress=progress)

  if filename is not None :
    if save_only_after_sampling :
      save_sampled_chain (filename, sampler, ndim, nwalkers, nsteps)

  return sampler, norm, param_type, orders, degrees 

def wrap_explore_distribution (df_a2z, freq, psd, back, low_bound_freq=1500, up_bound_freq=5000, wdw=None,
                               nsteps=1000, discard=200, show_corner=False, format_cornerplot='pdf', 
                               filename=None, parallelise=False, progress=False, thin=1, 
                               estimate_autocorrelation=False, plot_datapoints=True,  
                               nwalkers=64, normalise=False, instr='kepler', use_sinc=False,
                               asym_profile='korzennik', save_only_after_sampling=False, fit_amp=False,
                               projected_splittings=False, bins=100, existing_chains='read', **kwargs) :

  '''
  A small wrapper to call and exploit restult of the explore_distribution function inside the peakbagging
  framework.

  :param df_a2z: global pandas DataFrame wrapping global parameters needed to design the model.
  :type df_a2z: pandas DataFrame.

  :param freq: frequency vector
  :type freq: ndarray

  :param psd: real power vector
  :type freq: ndarray

  :param filename: name of the hdf5 where to store the chain. If filename is None, the name will not
  be stored. Optional, default None.
  :type filename: string

  :param parallelise: If set to True, use Python multiprocessing tool to parallelise process.
  Optional, default False.
  :type parallelise: bool

  :param instr: instrument to consider (amplitude ratio inside degrees depend on geometry 
  AND instrument and should be adaptated). Possible argument : 'kepler', 'golf'
  :type instr: str

  :param use_sinc: if set to ``True``, mode profiles will be computed using cardinal sinus and not Lorentzians.
    No asymmetry term will be used if it is the case. Optional, default ``False``.
  :type use_sinc: bool

  :param asym_profile: depending on the chosen argument, asymmetric profiles will be computed following Korzennik 2005 (``korzennik``)
    or Nigam & Kosovichev 1998 (``nigam-kosovichev``). 
  :type asym_profile: str

  :param bins: number of bins for each cornerplot panel. Optional, default 100.
  :type bins: int

  :return: the 16, 50 and 84th percentiles values for each parameter 
  :rtype: ndarray

  :param estimate_autocorrelation: if set to ``True``, the autocorrelation time
    of the sampled chains will be estimated by ``emcee``. Optional, default
    ``False``. 
  :type estimate_autocorrelation: bool

  :param plot_datapoints: data points outside contours will be drawn if set to ``True``. 
    Optional, default ``True``.
  :type plot_datapoints: bool
  '''

  df_to_pass = df_a2z.copy ()

  result, param_type, bounds, degrees, orders = a2z_df_to_param (df_a2z, give_n_l=True, 
                                                                 fit_amp=fit_amp)

  param_wdw = None
  if wdw is not None :
    dt = 1 / (2*freq[-1])
    param_wdw = sidelob_param (wdw, dt=dt)

  cp_result = np.copy (result)
  cp_bounds = np.copy (bounds)

  sampler, norm, labels, orders, degrees = explore_distribution (cp_result, param_type, freq, psd, back,
                            df_to_pass, cp_bounds, low_bound_freq=low_bound_freq, filename=filename, 
                            up_bound_freq=up_bound_freq, param_wdw=param_wdw, nsteps=nsteps, 
                            parallelise=parallelise, progress=progress, nwalkers=nwalkers, normalise=normalise,
                            degrees=degrees, orders=orders, instr=instr, use_sinc=use_sinc, asym_profile=asym_profile,
                            save_only_after_sampling=save_only_after_sampling, fit_amp=fit_amp, 
                            projected_splittings=projected_splittings, existing_chains=existing_chains)
  if sampler is None : 
    #sampler is None mean the hdf5 file already existed and no sampling has been performed 
    # (due to ``ignore`` option)
    return None 

  # Now exploiting results from the sampler
  flat_samples = sampler.get_chain(discard=discard, thin=thin, flat=True)

  # Estimating autocorrelation time
  if estimate_autocorrelation :
    taus = sampler.get_autocorr_time (discard=discard, thin=thin, quiet=True)

  if show_corner :
    if fit_amp :
      labels[labels=='height'] = 'amplitude'
    if projected_splittings :
      labels[labels=='split'] = 'proj_split'
    labels = labels.astype (str)
    flat_samples = flat_samples * norm
    labels, degrees, flatchain = sort_chain (labels, degrees, flat_samples)
    formatted_labels = param_array_to_latex (labels, orders, degrees) 

    cornerplot_wrapper (flatchain, 0, 1, formatted_labels, flat_input=True,
                        norm=None, filemcmc=filename, bins=bins,
                        format_cornerplot=format_cornerplot, 
                        plot_datapoints=plot_datapoints,
                        **kwargs)

  centiles = np.percentile(flat_samples, [16, 50, 84], axis=0) * norm 

  return centiles


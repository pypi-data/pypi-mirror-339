# coding: utf-8

import numpy as np
import pandas as pd
from scipy.optimize import minimize
from .modified_optimize import _minimize_powell
from .fit_tools import *
from pathos.multiprocessing import ProcessPool
import sys
import matplotlib
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
import emcee
import corner
import numba
from apollinaire.psd import degrade_psd
from .background import (background_model, extract_param,
                        log_prior, harvey)
from .save_chain import save_sampled_chain
import warnings

#numba settings
nopython=True

def convert_prot (prot) :
  '''
  Convert input prot (in days) to frequency (in µHz).
  '''
  f = 1e6 / (prot*86400)

  return f

def create_label (n_harmonic, freeze_background=True,
                  k_start=1) :
  '''
  Create label of fitted parameters.
  '''

  labels = ['f1']
  for ii in range (n_harmonic-k_start+1) :
    index = ii + k_start
    labels.append ('$h_{}$'.format (index))
    labels.append ('$w_{}$'.format (index))
    labels.append ('$\epsilon_{}$'.format (index))
  if not freeze_background :
    labels.append ('noise')

  return labels


def compute_cut (f1, n_harmonic) :
  '''
  Useful frequency cuts on the PSD.
  '''

  cut_peak = (n_harmonic+2) * f1

  return cut_peak

def create_vector_to_fit (freq, psd, back, n_harmonic, low_cut, f1) :
  '''
  Compute background, power and frequency vectors that will be used for the fit. 
  '''

  cut_peak = compute_cut (f1, n_harmonic)

  psd_fit = psd[(freq>low_cut)&(freq<cut_peak)]
  freq_fit = freq[(freq>low_cut)&(freq<cut_peak)]
  back_fit = back[(freq>low_cut)&(freq<cut_peak)]

  return freq_fit, psd_fit, back_fit

def retype_vectors (freq, psd, back) :

  freq = freq.astype (np.float64)
  psd = psd.astype (np.float64)
  back = back.astype (np.float64)

  return freq, psd, back

def create_param_vector (f1, log_height, log_width, n_harmonic=1,
                         freeze_background=True, k_start=1) :
  '''
  Create input param vector for rotation peak fit.

  :param f1: initial guess for first harmonic frequency value.
  :type f1: float

  :param log_height: logarithm of height of the first harmonic
  :type height: float
 
  :param log_width: logarithm of width of the first harmonic
  :type width: float

  :return: input parameters
  :rtype: ndarray
  '''

  if freeze_background :
    input_param = np.empty (1+3*(n_harmonic-k_start+1), dtype=float)
  else :
    input_param = np.empty (1+3*(n_harmonic-k_start+1) + 1, dtype=float)
  
  input_param[0] = f1 
  for ii in range (n_harmonic-k_start+1) :
    input_param [1+3*ii] = log_height - np.log (ii+1)
    input_param [2+3*ii] = log_width
    input_param [3+3*ii] = 0
  if not freeze_background :
    input_param[-1] = 1 #flat noise parameter

  return input_param

def create_fitting_window (freq, psd, param, s=.5,
                           freeze_background=True, k_start=1) :
  '''
  Create fitting window from initial window size ``s``.
  '''
 
  if freeze_background :
    aux_param=param[1:]
  else :
    aux_param=param[1:-1]
  f0 = param[0]
  aux_param = np.reshape (aux_param, (aux_param.size//3, 3))
  cond = np.zeros (freq.size, dtype=bool)
  for ii, elt in enumerate (aux_param) :
    aux_cond = (freq>(ii+k_start)*f0-s)&(freq<(ii+k_start)*f0+s)
    cond = cond + aux_cond
  aux_freq = freq[cond]
  aux_psd = psd[cond]

  return aux_freq, aux_psd


def create_rotation_guess (freq, psd, back, prot, n_harmonic=1,
                           freeze_background=True, k_start=1) :
  '''
  Compute guess values for rotation fit.
  '''

  f1 = convert_prot (prot)
  w = max (1e-2, 1e-2 * f1)
  aux = psd / back
  h = np.mean (aux[(freq>f1*k_start-w)&(freq<f1*k_start+w)])  
  if np.isnan (h) :
    h = 1e-1
  log_h = np.log (h) 
  log_w = np.log (w)
  guess = create_param_vector (f1, log_h, log_w, n_harmonic=n_harmonic,
                               freeze_background=freeze_background,
                               k_start=k_start)

  return guess

def get_low_bounds (guess, low_cut, n_harmonic=1,
                    freeze_background=True, tolerance_freq=0.01,
                    k_start=1) :

  '''
  Low bounds for prior on fitted values.
  '''

  low_bounds = np.empty (guess.size)
  low_bounds[0] = 0.95 * guess[0]
  for ii in range (n_harmonic-k_start+1) :
    low_bounds[1+3*ii] = -50 #log
    low_bounds[2+3*ii] = -50 #log
    low_bounds[3+3*ii] = - guess[0]*(ii+k_start)*tolerance_freq 
  if not freeze_background :
    low_bounds[-1] = 0.

  return low_bounds

def get_up_bounds (guess, n_harmonic=1,
                   freeze_background=True, tolerance_freq=0.01,
                   k_start=1) :
  '''
  Up bounds for prior on fitted values.
  '''

  up_bounds = np.empty (guess.size)
  up_bounds [0] = 1.05 * guess[0]
  for ii in range (n_harmonic-k_start+1) :
    up_bounds[1+3*ii] = np.log (50.) + guess[1+3*ii]
    up_bounds[2+3*ii] = np.log (50.) + guess[2+3*ii]
    up_bounds[3+3*ii] = guess[0]*(ii+k_start)*tolerance_freq 
  if not freeze_background :
    up_bounds [-1] = 10

  return up_bounds

@numba.jit (nopython=nopython)
def peak_model (freq, param_rot, n_harmonic, profile=1,
                common_width=False, k_start=1) :
  '''
  Peak model used to fit the rotation.
  
  :param profile: type of profile to use. 0: lorentzian, 1: sinc, 2: gaussian.
  '''

  model = np.zeros (freq.size, dtype=np.float64)

  f1 = param_rot[0]

  for ii in range (n_harmonic-k_start+1) :
    A = np.exp (param_rot[1+3*ii]) 
    if common_width :
      w = np.exp (param_rot[2])
    else :
      w = np.exp (param_rot[2+3*ii]) 
    epsilon_f = param_rot[3+3*ii]
    xxx = (freq - (ii+k_start)*f1 - epsilon_f) / w
    if profile == 0 :
      model += A / (1 + 4. * xxx * xxx)
    if profile == 1 :
      model += A * np.sinc (xxx) * np.sinc (xxx)
    if profile == 2 :
      model += A * np.exp (- xxx * xxx)

  return model

@numba.jit (nopython=nopython)
def rotation_model (freq, param, n_harmonic, profile=1,
                    freeze_background=True, k_start=1) :
  '''
  Wrapper for peak model. 
  '''

  param_rot = param[:-1]
  model = peak_model (freq, param_rot, n_harmonic, 
                      profile=profile, k_start=k_start)
  if freeze_background :
    model += 1
  else :
    model += param[-1]

  return model

@numba.jit (nopython=nopython)
def log_likelihood_rotation (param, freq, psd, back, n_harmonic, profile=1,
                             freeze_background=True, k_start=1) :
  '''
  Compute negative log_likelihood for fitting model on 
  background.

  :param param: param to fit passed by perform_mle_back. Param are given in 
  the following order: Harvey law parameters, power law parameters, Gaussian p-mode 
  envelope parameters, noise constant. 

  :param freq: frequency vector in µHz.
  :type freq: ndarray

  :param psd: power density vector in ppm^2/µHz or (m/s)^2/muHz.
  :type psd: ndarray

  :param n_harmonic: number of Harvey laws to use to build the background
  model.  
  :type n_harmonic: int
  '''

  model = rotation_model (freq, param, n_harmonic, profile=profile,
                          freeze_background=freeze_background, 
                          k_start=k_start)

  aux = psd / model + np.log (model)
  log_l = np.sum (aux)

  return log_l

def log_probability_rotation (param_to_fit, freq, psd, back, bounds, n_harmonic, norm=None, profile=1,
                              freeze_background=True, k_start=1) :
  '''
  Compute the positive posterior log probability (unnormalised) of the parameters to fit. 

  :param_to_fit: backgrounds parameters to fit.
  :type param_to_fit: 1d ndarray
 
  :param param: param to fit passed by perform_mle_back.  

  :param freq: frequency vector in µHz.
  :type freq: ndarray

  :param psd: power density vector in ppm^2/µHz or (m/s)^2/muHz.
  :type psd: ndarray

  :param n_harmonic: number of Harvey laws to use to build the background
  model.  
  :type n_harmonic: int

  :param norm: if given, the param_to_fit and bounds input vectors will be multiplied by this vector. 
  Optional, default ``None``.
  :type norm: ndarray

  :return: posterior probability value
  :rtype: float
  '''

  #param_to_fit = np.copy (param_to_fit) #make a copy to not modify the reference array
  param_to_fit = param_to_fit.astype (np.float64) 
  bounds = np.copy (bounds)

  if norm is not None :
    param_to_fit = param_to_fit * norm
    bounds[:,0] = bounds[:,0] * norm
    bounds[:,1] = bounds[:,1] * norm

  l_prior = log_prior (param_to_fit, bounds)

  if not np.isfinite (l_prior) :
    return - np.inf
  l_likelihood = - log_likelihood_rotation (param_to_fit, freq, psd, back, n_harmonic, profile,
                                            freeze_background, k_start)

  l_proba = l_prior + l_likelihood

  return l_proba

def visualise_rotation (freq, psd, back, low_cut, f1, param_fitted=None, guess=None, 
                        n_harmonic=3, filename=None, spectro=True, alpha=1., show=False,
                        profile=1, k_start=1) :

  '''
  Plot fitted rotation peaks against real PSD (and possibly against initial guess).
  '''

  cut_peak = compute_cut (f1, n_harmonic)

  if (param_fitted is None) and (guess is None) :
    raise Exception ('No pattern was given to plot !')
 

  fig = plt.figure (figsize=(12,6))
  ax = fig.add_subplot (111)
  
  aux_freq = freq[(freq>low_cut)&(freq<cut_peak)]

  ax.plot (freq[(freq>low_cut)&(freq<cut_peak)], 
           psd[(freq>low_cut)&(freq<cut_peak)] / back[(freq>low_cut)&(freq<cut_peak)], 
           color='black')
  if guess is not None :
    guess_model = rotation_model (aux_freq, guess, n_harmonic, 
                                  profile=profile, k_start=k_start) 
    ax.plot (aux_freq, guess_model, color='green')
  if param_fitted is not None :
    fitted_model = rotation_model (aux_freq, param_fitted, n_harmonic, 
                                   profile=profile, k_start=k_start) 
    ax.plot (aux_freq, fitted_model, color='red', alpha=alpha)

  ax.set_xlabel (r'Frequency ($\mu$Hz)')
  ax.set_ylabel (r'PSD (SNR)')

  ax.set_xscale ('log')

  if filename is not None:
    plt.savefig (filename, format='pdf')

  if show :
    plt.show ()

  plt.close ()

  return


def perform_mle_rotation (freq, psd, back, prot, n_harmonic=3, low_cut=1., 
                          guess=None, low_bounds=None, up_bounds=None, 
                          method=_minimize_powell, filename=None, spectro=False, 
                          show=True, show_guess=False, profile=1, 
                          freeze_background=True, s=1, k_start=1) :

  '''
  Perform MLE over rotation model. 

  :param freq: frequency vector in µHz.
  :type freq: ndarray

  :param psd: power density vector in ppm^2/µHz or (m/s)^2/muHz.
  :type psd: ndarray

  :param n_harmonic: number of Harvey laws to use to build the background
    model. Optional, default 3.  
  :type n_harmonic: int

  :param guess: first guess directly passed by the users. If guess is ``None``, the 
    function will automatically infer a first guess. Optional, default ``None``.
    Parameters given in the following order:
    *first harmonic frequency value, height, width, alpha, beta*
  :type guess: array-like.

  :param low_cut: Spectrum below this frequency will be ignored for the fit. The frequency value
    must be given in µHz. Optional, default 1.
  :type low_cut: float

  :param method: minimization method used by the scipy minimize function. Optional, default _minimize_powell
    (modified version allowing to use bounds)

  :param low_bounds: lower bounds to consider in the parameter space exploration. Must have the same structure
    than guess.
  :type low_bounds: ndarray

  :param up_bounds: upper bounds to consider in the parameter space exploration. Must have the same structure
    than guess.
  :type up_bounds: ndarray

  :param show: if set to ``True``, will show at the end a plot summarising the fit. Optional, default ``True``.
  :type show: bool

  :param filename: if given, the summary plot will be saved under this filename. Optional, default ``None``.
    ``show`` argument must have been set to ``True``. 
  :type filename: str

  :param spectro: if set to ``True``, make the plot with unit consistent with radial velocity, else with 
    photometry. Automated guess will also be computed consistently with spectroscopic measurements. 
    Optional, default ``False``.
  :type spectro: bool

  :param show: if set to ``True``, will show at the end a plot summarising the fit. Optional, default ``True``.
  :type show: bool

  :param show_guess: if set to ``True``, will show at the beginning a plot summarising the guess. Optional, default ``False``.
  :type show_guess: bool

  :param profile: model profile for rotation peak. 0:Lorentzian, 1:sinc, 2:Gaussian. Optional, default 1.
  :type profile: int

  :return: fitted rotation model and corresponding parameters.
  :rtype: tuple of array
  '''

  freq, psd, back = retype_vectors (freq, psd, back)

  if guess is None :
    guess = create_rotation_guess (freq, psd, prot, n_harmonic=n_harmonic,
                                   freeze_background=freeze_background,
                                   k_start=k_start)
  if up_bounds is None :
    up_bounds = get_up_bounds (guess, n_harmonic=n_harmonic, k_start=k_start,
                               freeze_background=freeze_background)
  if low_bounds is None :
    low_bounds = get_low_bounds (guess, low_cut, n_harmonic=n_harmonic,
                                 freeze_background=freeze_background, k_start=k_start)
  if method is _minimize_powell :
    bounds = (low_bounds, up_bounds)
  else :
    bounds = np.c_[low_bounds, up_bounds]

  labels = create_label (n_harmonic, freeze_background, k_start=k_start)

  aux_freq, aux_psd, aux_back = create_vector_to_fit (freq, psd, back, 
                                                      n_harmonic, low_cut, guess[0])
  aux_psd = aux_psd / aux_back

  aux_freq, aux_psd = create_fitting_window (aux_freq, aux_psd, guess, s=s,
                                             freeze_background=freeze_background,
                                             k_start=k_start)

  if show_guess :
    visualise_rotation (freq, psd, back, low_cut, guess[0], param_fitted=None, guess=guess, profile=profile,
                        n_harmonic=n_harmonic, filename=None, spectro=spectro, alpha=0.8, show=True,
                        k_start=k_start)

  print ('Beginning fit')
  param = np.copy (guess)
  result = minimize (log_likelihood_rotation, param,
                     args=(aux_freq, aux_psd, aux_back, n_harmonic, 
                           profile, freeze_background, k_start), 
                     bounds=bounds,
                     method=method)

  print (result.message)
  param_model = result.x

  fitted_model = rotation_model (freq, param_model, n_harmonic, 
                                 profile=profile, k_start=k_start)

  visualise_rotation (freq, psd, back, low_cut, guess[0], 
                      param_fitted=param_model, guess=guess, profile=profile,
                      n_harmonic=n_harmonic, filename=filename, 
                      spectro=spectro, alpha=0.8, show=show,
                      k_start=k_start)

  return fitted_model, param_model


def explore_distribution_rotation (freq, psd, back, prot, n_harmonic=3, low_cut=1., guess=None, 
                                   low_bounds=None, up_bounds=None, 
                                   filename=None, spectro=False, show=True, show_guess=False,
                                   show_corner=True, nsteps=1000, discard=200, parallelise=False, 
                                   progress=False, nwalkers=64, filemcmc=None,
                                   thin=1, save_only_after_sampling=True, profile=1,
                                   bins=10, existing_chains='read', freeze_background=True, s=1, k_start=1) :

  '''
  Use a MCMC framework to fit the rotation model. 

  :param freq: frequency vector in µHz.
  :type freq: ndarray

  :param psd: power density vector in ppm^2/µHz or (m/s)^2/muHz.
  :type psd: ndarray

  :param n_harmonic: number of Harvey laws to use to build the background
    model. Optional, default 3.  
  :type n_harmonic: int

  :param guess: first guess directly passed by the users. If guess is ``None``, the 
    function will automatically infer a first guess. Optional, default ``None``.
    Parameters given in the following order:
    *first harmonic frequency value, height, width, alpha, beta*
  :type guess: array-like.

  :param low_cut: Spectrum below this frequency will be ignored for the fit. The frequency value
    must be given in µHz. Optional, default 1.
  :type low_cut: float

  :param low_bounds: lower bounds to consider in the parameter space exploration. Must have the same structure
    than guess.
  :type low_bounds: ndarray

  :param up_bounds: upper bounds to consider in the parameter space exploration. Must have the same structure
    than guess.
  :type up_bounds: ndarray

  :param show: if set to ``True``, will show at the end a plot summarising the fit. Optional, default ``True``.
  :type show: bool

  :param filename: if given, the summary plot will be saved under this filename. Optional, default ``None``.
    ``show`` argument must have been set to ``True``. 
  :type filename: str

  :param spectro: if set to ``True``, make the plot with unit consistent with radial velocity, else with 
    photometry. Automated guess will also be computed consistently with spectroscopic measurements. 
    Optional, default ``False``.
  :type spectro: bool

  :param show_guess: if set to ``True``, will show at the beginning a plot summarising the guess. Optional, default ``False``.
  :type show_guess: bool

  :param filemcmc: name of the hdf5 where to store the chain. If filename is ``None``, the name will not
    be stored. Optional, default ``None``.
  :type filename: string

  :param parallelise: If set to ``True``, use Python multiprocessing tool to parallelise process.
    Optional, default ``False``.
  :type parallelise: bool

  :param show: if set to ``True``, will show at the end a plot summarising the fit. Optional, default ``True``.
  :type show: bool

  :param show_corner: if set to ``True``, will show the corner plot summarising the MCMC process. 
    Plot will be saved as a pdf is ``filemcmc`` is also specified. Optional, default ``True``.
  :type show: bool

  :param nsteps: number of steps that will be discarded in the MCMC sampling.
  :type nsteps: int

  :param discard: number of discarded steps in the MCMC sampling.
  :type nsteps: int

  :param show_guess: if set to ``True``, will show at the beginning a plot summarising the guess. Optional, default ``False``.
  :type show_guess: bool

  :param thin: take only every ``thin`` steps from the chain. Optional, default 1. 
  :type thin: int

  :param profile: model profile for rotation peak. 0:Lorentzian, 1:sinc, 2:Gaussian. Optional, default 1.
  :type profile: int

  :return: fitted rotation model, corresponding parameters and sigma obtained by MCMC exploration.
  :rtype: tuple of array
  '''

  freq, psd, back = retype_vectors (freq, psd, back)

  if guess is None :
    guess = create_rotation_guess (freq, psd, back, prot, n_harmonic=n_harmonic,
                                   freeze_background=freeze_background, k_start=k_start)
  if up_bounds is None :
    up_bounds = get_up_bounds (guess, n_harmonic=n_harmonic, k_start=k_start,
                               freeze_background=freeze_background)
  if low_bounds is None :
    low_bounds = get_low_bounds (guess, low_cut, n_harmonic=n_harmonic, 
                                 freeze_background=freeze_background, k_start=k_start)

  labels = create_label (n_harmonic, freeze_background, k_start=k_start)

  aux_freq, aux_psd, aux_back = create_vector_to_fit (freq, psd, back, 
                                                      n_harmonic, low_cut, guess[0])
  aux_psd = aux_psd / aux_back

  aux_freq, aux_psd = create_fitting_window (aux_freq, aux_psd, guess, s=s,
                                             freeze_background=freeze_background,
                                             k_start=k_start)

  if show_guess :
    visualise_rotation (freq, psd, back, low_cut, guess[0], 
                        param_fitted=None, guess=guess, profile=profile, 
                        n_harmonic=n_harmonic, filename=None, 
                        spectro=spectro, alpha=0.8, show=True,
                        k_start=k_start)

  print ('Beginning fit')

  bounds = np.c_[low_bounds, up_bounds]

  norm = np.ones (guess.size)

  if parallelise :
    pool = ProcessPool ()
  else :
    pool = None

  param_to_pass = np.copy (guess)
  bounds_to_pass = np.copy (bounds)

  #normalisation step
  param_to_pass = param_to_pass / norm
  bounds_to_pass[:,0] = bounds_to_pass[:,0] / norm
  bounds_to_pass[:,1] = bounds_to_pass[:,1] / norm

  pos = param_to_pass + 1e-4 * np.random.randn(nwalkers, param_to_pass.size)
  nwalkers, ndim = pos.shape

  run_sampler = True
  if filemcmc is not None :
    if path.exists (filemcmc) :
      if existing_chains=='read' :
        print (filemcmc + " already exists, existing chains set to 'read', no sampling has been performed, proceeding to next step.")
        sampler = emcee.backends.HDFBackend(filemcmc, read_only=True)
        run_sampler = False
      elif existing_chains=='reset' :
        os.remove (filemcmc)
        backend = emcee.backends.HDFBackend(filemcmc)
        backend.reset(nwalkers, ndim)
        print (filemcmc + " already exists, existing chains set to 'reset', file has been deleted and a new file has been created instead.")
      elif existing_chains=='sample' :
        backend = emcee.backends.HDFBackend(filemcmc)
        pos = None
        print (filemcmc + " already exists, existing chains set to 'sample', sampling will restart from where it stopped.")
    else :
      backend = emcee.backends.HDFBackend(filemcmc)
      backend.reset(nwalkers, ndim)

    #saving parameters name and normalisation information
    filemcmc_info = filemcmc[:len(filemcmc)-3] + '.dat'
    np.savetxt (filemcmc_info, np.c_[norm, labels], fmt='%-s',
                header=make_header_utility_file ())

    if save_only_after_sampling :
      # I have deliberately created the file to signal to other process that this chain is being
      # sampled
      backend = None
  else :
    backend = None

  if run_sampler :
    sampler = emcee.EnsembleSampler(nwalkers, ndim, log_probability_rotation,
                                    args=(aux_freq, aux_psd, aux_back, bounds_to_pass, n_harmonic,
                                          norm, profile, freeze_background, k_start),
                                    backend=backend, pool=pool)
    sampler.run_mcmc(pos, nsteps, progress=progress, skip_initial_state_check=True)

    if filemcmc is not None :
      if save_only_after_sampling :
        save_sampled_chain (filemcmc, sampler, ndim, nwalkers, nsteps)

  if show_corner :
    cornerplot_wrapper (sampler, discard, thin, labels, norm, filemcmc=filemcmc,
                        bins=bins)

  flat_samples = sampler.get_chain(discard=discard, thin=thin, flat=True)
  centiles = np.percentile(flat_samples, [16, 50, 84], axis=0) * norm

  param_model = centiles[1,:]
  sigma_model = np.maximum (centiles[1,:] - centiles[0,:], centiles[2,:] - centiles[1,:])

  fitted_model = rotation_model (freq, param_model, n_harmonic, 
                                 profile=profile, k_start=k_start)

  visualise_rotation (freq, psd, back, low_cut, guess[0], param_fitted=param_model, 
                      guess=guess, profile=profile, k_start=k_start, 
                      n_harmonic=n_harmonic, filename=filename, 
                      spectro=spectro, alpha=0.8, show=show)

  return fitted_model, param_model, sigma_model




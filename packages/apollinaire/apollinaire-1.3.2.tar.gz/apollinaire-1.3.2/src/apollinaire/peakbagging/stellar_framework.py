# coding: utf-8

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from os import path
from .background import (perform_mle_background, explore_distribution_background, 
                         dnu_scale, numax_scale, background_guess)
from .global_pattern import (perform_mle_pattern, explore_distribution_pattern,
                             list_order_to_fit, pattern_to_a2z, first_guess_mcmc)
from .mode_selection import select_mode_to_fit
from .peakbagging import peakbagging
from .fit_tools import *
from .header import *
import warnings


def stellar_framework (freq, psd, r=1, m=1, teff=5770, nwalkers=64, dnu=None, back=None, wdw=None,
                       numax=None, Hmax=None, Wenv=None, epsilon=None, width=None, 
                       alpha=None, d02=None, d01=None, d13=None, n_harvey=2, low_cut=10.,
                       guess_back=None, low_bounds_back=None, up_bounds_back=None, 
                       frozen_param_back=None, power_law=False, high_cut_plaw=20., spectro=False, 
                       filename_back='background.png', back_mcmc=True, back_mle=False,
                       filemcmc_back='mcmc_sampler_background.h5', nsteps_mcmc_back=1000,
                       guess_pattern=None, low_bounds_pattern=None, up_bounds_pattern=None,
                       pattern_mcmc=True, pattern_mle=False, n_order=3, n_order_peakbagging=3,
                       h0_screening=False, format_cornerplot='pdf',  
                       filename_pattern='pattern.png', filemcmc_pattern='mcmc_sampler_pattern.h5',
                       nsteps_mcmc_pattern=1000, parallelise=False, fit_l1=True, fit_l3=False,
                       use_numax_back=False,  progress=False, a2z_file='modes_param.a2z', a2z_in=None,
                       nsteps_mcmc_peakbagging=1000, mcmcDir='.', instr='geometric', amp_l=[1., 1.5, 0.7, 0.2],
                       filename_peakbagging='summary_peakbagging.png', nopeakbagging=False,
                       discard_back=200, discard_pattern=200, discard_pkb=200,
                       thin_back=1, thin_pattern=1, thin_pkb=1, quickfit=False, num=500, num_numax=500,
                       reboxing_behaviour='advanced_reboxing', reboxing_strategy='median',
                       save_only_after_sampling=False, apodisation=False, fit_angle=False,
                       guess_angle=90, fit_splittings=False, fit_splittings_per_order_in_global=False, 
                       guess_split=0, fit_amplitude_ratio=False, frozen_harvey_exponent=False, 
                       fit_amp=False, extended=False, author=None,
                       pkb_fmt=None, projected_splittings=False, bins=100,
                       existing_chains_back='read', existing_chains_pattern='read',
                       existing_chains_pkb='read', strategy='order', common_width=False,
                       save_background_vector=True, dpi=300, show_corner=True, estimate_autocorrelation=False,
                       plot_datapoints=True, show_gaussian=True) :

  '''
  Framework for stellar peakbagging considering only a few input parameters.
  Background, global pattern and individual mode parameters are successively fitted.

  :param freq: frequency vector
  :type freq: ndarray

  :param psd: real power or power spectral density vector
  :type psd: ndarray

  :param r: stellar radius. Given in solar radius. Optional, default 1.
  :type r: float

  :param m: stellar mass. Given in solar masses.  
    Optional, default 1.
  :type m: float

  :param teff: stellar effective temperature. Given in Kelvins.  
    Optional, default 5770.
  :type teff: float

  :param nwalkers: number of walkers for the MCMC process. Optional, default 64.
  :type nwalkers: int

  :param dnu: large frequency separation. Must be given in µHz. 
    If ``None``, will be computed through scaling laws. 
    Optional, default ``None``.
  :type dnu: float

  :param back: array of fitted background, of same length as ``freq`` 
    and ``psd``. If given, no fit will be performed on background
    and the pattern step will directly take place. ``Hmax``, ``Wenv`` 
    and ``numax`` must in this case also be given. 
    Optional, default ``None``.
  :type back: ndarray

  :param wdw: observational window of the light curve to take into account 
    the side lobes pattern in the modes. Must be 1 when an actuak observation
    is acquired and zero otherwise. Optional, default ``None``.
  :type wdw: ndarray

  :param numax: maximum of power in p-mode envelope. Must be given in µHz. 
    Optional, default ``None``.
  :type numax: float

  :param Hmax: amplitude of p-mode envelope. Optional, default ``None``.
  :type Hmax: float

  :param Wenv: width of p-mode envelope. Optional, default ``None``.
  :type Wenv: float

  :param epsilon: epsilon guess value of mode patterns. If given, 
    will override the value computed by the automatic guess. 
    Optional, default ``None``.
  :type epsilon: float

  :param width: width guess value of mode patterns. If given, 
    will override the value computed by the automatic guess. 
    Optional, default ``None``.
  :type width: float

  :param alpha: alpha value for global pattern guess. 
    If specified, this value will override guess value
    computed by the automatic guess. Optional, default ``None``. 
  :type alpha: float

  :param d02: d02 value for global pattern guess. 
    If specified, this value will override guess value
    computed by the automatic guess. Optional, default ``None``. 
  :type d02: float

  :param d01: d01 value for global pattern guess. 
    If specified, this value will override guess value
    computed by the automatic guess. Optional, default ``None``. 
  :type d01: float

  :param d13: d13 value for global pattern guess. 
    If specified, this value will override guess value
    computed by the automatic guess. Optional, default ``None``. 
  :type d13: float

  :param n_harvey: number of Harvey laws to use to build the background model.
    Optional, default 2. With more than two Harvey laws, it is strongly recommended
    to manually feed the 'guess' parameter.  
  :type n_harvey: int

  :param guess_back: first guess directly passed by the user. If guess is
    ``None``, the function will automatically infer a first guess. Optional,
    default ``None``.  Backgrounds parameters given in the following order:
    *param_harvey (3* ``n_harvey`` *), param_plaw (2), param_gaussian (3), white
    noise (1)*. You can use ``create_background_guess_arrays`` to create guess 
    and bounds arrays with proper structure.  
  :type guess_back: array-like.

  :param low_bounds_back: lower bounds to consider in the background parameters
    space exploration. Must have the same dimension than ``guess_back``.
  :type low_bounds_back: ndarray

  :param up_bounds_back: upper bounds to consider in the background parameters
    space exploration. Must have the same dimension than ``guess_back``.
  :type up_bounds_back: ndarray

  :param frozen_param_back: boolean array of the same size as ``guess_back``.
    Components set to ``True`` will not be fitted.
  :type frozen_param_back: boolean array

  :param power_law: set to ``True`` to fit a power law on the background.
    Optional, default ``False``.
  :type power_law: bool

  :param high_cut_plaw: if ``power_law=True``, the function will consider
    the PSD segment between ``low_cut`` and ``high_cut_plaw`` to 
    compute the power law parameters initial guess.
  :type high_cut_plaw: float

  :param spectro: if set to ``True``, make the plot with unit consistent with
    radial velocity, else with photometry. Optional, default ``False``.
  :type spectro: bool

  :param filename_back: name of the of the dat file of the fitted background, 
    the background parameters pdf file where the plot will be stored.
    Optional, default ``background``.
  :type filename_back: str

  :param back_mcmc: If set to ``False``, no MCMC sampling will be performed 
    for the background. Optional, default ``True``.
  :type back_mcmc: bool

  :param back_mle: If set to ``False``, no MLE optimisation 
    will be performed for the background. Optional, default ``True``.
  :type back_mle: bool
  
  :param filemcmc_back: Name of the hdf5 file where the MCMC background chain will 
    be stored. Optional, default ``mcmc_sampler_background.h5``.
  :type filemcmc_back: str

  :param nsteps_mcmc_back: number of MCMC steps for the
    background parameters exploration. Optional, default 1000.
  :type nsteps_mcmc_back: int

  :param guess_pattern: first guess directly passed by the user. If guess is
    ``None``, the function will automatically infer a first guess. Optional,
    default ``None``.  Pattern parameters have to be given in the following order:
    ``eps``, ``alpha``, ``Dnu``, ``numax``,  ``Hmax``, ``Wenv``, ``w``, ``d02``, 
    ``b02``, ``d01``, ``b01``, ``d13``, ``b03``. A first version of the guess
    and bounds array can be created through the ``create_pattern_guess_arrays``.
  :type guess_pattern: array-like.

  :param low_bounds_pattern: lower bounds to consider in the background parameters
    space exploration. Must have the same dimension than ``guess_pattern``.
  :type low_bounds_pattern: ndarray

  :param up_bounds_pattern: upper bounds to consider in the background parameters
    space exploration. Must have the same dimension than ``guess_pattern``.
  :type up_bounds_pattern: ndarray

  :param pattern_mle: If set to ``False``, no MLE optimisation 
    will be performed for the pattern. Optional, default ``True``.
  :type pattern_mle: bool

  :param pattern_mcmc: If set to ``False``, no MCMC sampling will 
    be performed for the pattern. Optional, default ``True``.
  :type pattern_mcmc: bool
  
  :param n_order: number of orders to consider for the global pattern fit.
    Optional, default 3. 
  :type n_order: int

  :param n_order_peakbagging: number of orders to fit at the 
    individual mode parameters step. Optional, default 3. 
  :type n_order_peakbagging: int

  :param h0_screening: if set to ``True``, a fast frequency screening of the
    p-mode region will be performed in order to determine the mode that it possible
    to fit. ``n_order_peakbagging`` value will be ignored in this case. Optional,
    default ``False``.
  :type h0_screening: bool

  :param format_cornerplot: set cornerplot file format. Optional, default ``pdf``.
  :type format_cornerplot: str

  :param filename_pattern: name of the pdf file where the fitted global pattern parameters 
    and the plot of the fitted global pattern will be stored.
    Optional, default ``pattern``.
  :type filename_pattern: str
  
  :param filemcmc_pattern: Name of the hdf5 file where the MCMC pattern chain will be 
    stored. Optional, default ``mcmc_sampler_pattern.h5``.
  :type filemcmc_pattern: str

  :param nsteps_mcmc_pattern: number of MCMC steps for the pattern parameters exploration. 
    Optional, default 1000.
  :type nsteps_mcmc_pattern: int

  :param parallelise: if set to ``True``, multiprocessing will 
    be used to sample the MCMC. Optional, default ``False``.
  :type parallelise: bool

  :param fit_l1: set to ``True`` to fit the d01 and b03 param and 
    create guess for l=1 modes. Optional, default ``True``.
  :type fit_l1: bool

  :param fit_l3: set to ``True`` to fit the d03 and b03 param and 
    create guess for l=3 modes. Optional, default ``False``.
    ``fit_l1`` must be set to ``True``. 
  :type fit_l3: bool

  :param use_numax_back: if set to ``True``, the ``numax`` values 
    computed with the background fit will be used as input guess for the pattern fit.
    Otherwise, the initial ``numax`` for the pattern fit will be taken 
    from the ``numax`` argument or computed with the scaling laws. 
  :type use_numax_back: bool

  :param progress: show progress bar in terminal. Optional, default ``False``.
  :type progress: bool

  :param a2z_file: name of the a2z file where the individual parameters 
    will be stored. This will also be used to name the output pkb file.
    Optional, default ``modes_param.a2z``
  :type a2z_file: str

  :param a2z_in: a2z file with guess input for individual parameters. If
    provided, the global pattern step will be ignored and the function will
    directly sample individual modes parameters (after sampling the background if
    it has not been provided too). Optional, default ``None``. 
  :type a2z_in: str

  :param nsteps_mcmc_peakbagging: number of MCMC steps for 
    the peakbagging parameters exploration. Optional, default 1000.
  :type nsteps_mcmc_peakbagging: int

  :param mcmcDir: Name of the directory where the MCMC of the individual 
    parameters should be stored. Optional, default ``.``.
  :type mcmcDir: str

  :param instr: name of the instrument for which m-amplitude ratios will 
    be computed. ``geometric``, ``golf`` and ``virgo`` are available.
  :type instr: str

  :param amp_l: amplitude ratio between harmonic degrees (relative to l=0 mode).
    Optional, default [1., 1.5, 0.7, 0.2].
  :type amp_l: array-like
  
  :param filename_peakbagging: name of the file where the plot summary 
    of the individual mode parameters peakbagging will be stored.
    Optional, default ``summary_peakbagging.pdf``.
  :type filename_peakbagging: str

  :param nopeakbagging: if set to ``True``, individual modes parameters will
    not be fitted. Optional, default ``False``.  
  :type nopeakbagging: bool

  :param discard_back: number of step to discard for the background sampling.
    Optional, default 200.
  :type discard_back: int

  :param discard_pattern: number of step to discard for the pattern sampling.
    Optional, default 200.
  :type discard_pattern: int

  :param discard_pkb: number of step to discard for the peakbagging sampling.
    Optional, default 200.
  :type discard_pkb: int

  :param thin_back: take only every ``thin`` steps from the chain sampled for
    backgrounds parameters. Optional, default 10. 
  :type thin_back: int

  :param thin_pattern: take only every ``thin`` steps from the chain sampled
    for pattern parameters. Optional, default 10. 
  :type thin_pattern: int

  :param quickfit: if set to ``True``, the fit will be performed over a
    smoothed and logarithmically resampled background.  Optional, default
    ``False``. 
  :type quickfit: bool

  :param num: Only considered if ``quickfit=True``. 
    Number of point in the resampled PSD, or target number of point
    for region away from ``numax`` if ``advanced_reboxing`` is selected.
    Optional, default ``5000``.
  :type num: int

  :param num_numax: Only considered if ``quickfit=True`` 
    and ``reboxing_behaviour=advanced_reboxing``. 
    Number of resampling points in the ``numax`` region.
    Optional, default ``1000``.
  :type num_numax: int

  :param reboxing_behaviour: behaviour for ``quickfit`` new power vector
    computation. It can be ``smoothing``, ``reboxing`` or ``advanced_reboxing``.
    Optional, default ``advanced_reboxing``. 
  :type reboxing_behaviour: str

  :param reboxing_strategy: reboxing strategy to take box values when using
    ``quickfit`` and ``reboxing_behaviour=reboxing``.  Can be ``median`` or
    ``mean``. Optional, default ``median``.
  :type reboxing_strategy: str

  :param save_only_after_sampling: if set to True, hdf5 file with chains
    information will only be saved at the end of the sampling process. If set to
    False, the file will be saved step by step (see ``emcee`` documentation).
  :type saveon_only_after_sampling: bool

  :param apodisation: if set to ``True``, distort the model to take the
    apodisation into account. Optional, default ``False``.
  :type apodisation: bool

  :param fit_angle: if set to ``True``, the peakbagging process will include
    inclination angle of the star in the parameters to fit.  Optional, default
    ``False``.
  :type fit_angle: bool

  :param guess_angle: initial guess value for angle. Will be taken into account
    only if ``fit_angle`` is ``True``.  Optional, default 90.
  :type guess_angle: float

  :param fit_splittings: if set to ``True``, the peakbagging process will
    include mode splittings in the parameters to fit.  Optional, default ``False``.
  :type fit_splittings: bool

  :param fit_splittings_per_order_in_global: if set to ``True`` and
    ``fit_splittings=True`` with ``strategy='global'``, the peakbagging process
    will include one mode splittings per order in the parameters to fit.  Optional,
    default ``False``.
  :type fit_splittings_per_order_in_global: bool

  :param guess_split: initial guess value for splittings. Will be taken into
    account only if ``fit_splittings`` is ``True``.  Optional, default 0.
  :type guess_split: float

  :param fit_amplitude_ratio: if the selected strategy is ``global``, the global
    ``amp_l`` amplitude ratio between degrees parameters will be fitted only if
    this parameter is set to ``True``.  Optional, default ``False``. 
  :type fit_amplitude_ratio: bool

  :param frozen_harvey_exponent: set to True to have the Harvey models 
    exponent fixed to 4. Optional, default ``False``.
  :type frozen_harvey_exponent: bool

  :param fit_amp: if set to ``True``, amplitude of the modes will be fitted 
    instead of heights (input heights will be transformed inside
    the code and retransformed as outputs).
  :type fit_amp: bool

  :param extended: if set to ``True``, the returned pkb array will be 
    extended to contain asymmetric uncertainties over each parameter.
  :type extended: bool

  :param author: identifier of the peakbagger, if given it will be specified 
    in the header of the output pkb file. Optional, default ``None``.
  :type author: str

  :param pkb_fmt: float formatting of the pkb file that will be created by 
    the function. Optional, default ``None``.
  :type fmt: str or array-like

  :param projected_splittings: if set to ``True``, the function will consider 
    that the ``split`` parameters of the input are projected 
    splittings and will build the model consequently. Optional, default ``False``. 
  :type projected_splittings: bool

  :param bins: number of bins for each cornerplot panel. Optional, default 100.
  :type bins: int

  :param existing_chains_back: controls the behaviour of the function
    concerning a background parameters existing hdf5 file. If, ``read``, existing
    files will be read without sampling and function output will be updated
    consequently, if ``reset``, the backend will be cleared and the chain will be
    sampled from scratch, if ``sample`` the function will sample the chain from
    where the previous exploration was stopped, if ``ignore``, the chain is not
    read. Optional, default ``read``.  The option ``ignore`` will apply only to
    individual mode chains, it will be changed to ``read`` for background and
    pattern steps. 
  :type existing_chains: str

  :param existing_chains_pattern: Same as ``existing_chains_back`` but for a 
    global pattern parameters existing hdf5 file. 
  :type existing_chains_pattern: str

  :param existing_chains_pkb: Same as ``existing_chains_back`` but for individual mode 
    parameters existing hdf5 files. 
  :type existing_chains_pkb: str

  :param strategy: fitting strategy for individual modes. Can be ``order`` or 
    ``global``. Optional, default ``order``. Note that the ``global`` behaviour
    is experimental. 
  :type strategy: str

  :param common_width: if set to ``True``, only a global width parameter will be set in the a2z
    DataFrame. Optional, default ``False``.
  :type common_width: bool

  :param save_background_vector: the full background vector will be saved only if 
    this option is set to ``True``. Optional, default ``True``.
  :type save_background_vector: bool

  :param dpi: dot per inch value for figures.
  :type dpi: int 

  :param show_corner: if set to ``True``, corner plots will be shown and saved.
    Optional, default ``True``.
  :type show_corner: bool

  :param estimate_autocorrelation: if set to ``True``, the autocorrelation time
    of the sampled chains will be estimated by ``emcee``. Optional, default
    ``False``. 
  :type estimate_autocorrelation: bool

  :param plot_datapoints: data points outside contours will be drawn if set to ``True``. 
    Optional, default ``True``.
  :type plot_datapoints: bool

  :param show_gaussian: If set to ``True``, show p-mode acoustic hump modelled by a Gaussian
    function in the background summary plot. Optional, default ``True``.
  :type show_gaussian: bool


  :return: ``None``
  '''

  norm_back = None
  norm_pattern = None

  if existing_chains_back in ['sample', 'read'] and back_mcmc:
    if path.exists (filemcmc_back) :
      back_mle=False
      if guess_back is None :
        if dnu is None :
          dnu = dnu_scale (r, m)
        if numax is None :
          numax = numax_scale (r, m, teff)
        guess_back = background_guess (freq, psd, numax, dnu, 
                              m_star=m, n_harvey=n_harvey, 
                              spectro=spectro, power_law=power_law,
                              high_cut_plaw=high_cut_plaw)
      norm_back = np.loadtxt (path.splitext (filemcmc_back)[0] + '.dat', usecols=0)

  if back_mle==False and back_mcmc==False :
    raise Exception ('You must set at least pattern_mcmc=True or pattern_mle=True')

  if pattern_mle==False and pattern_mcmc==False :
    raise Exception ('You must set at least pattern_mcmc=True or pattern_mle=True')

  if strategy=='pair' :
    raise Exception ("stellar_framework is unable to use 'pair' fitting strategy."\
                     "You need to manually build your a2z file and to use the 'peakbagging' function.")

  if strategy=='order' and common_width : 
    common_width = False
    warnings.warn ("Parameter common_width=True is not compatible with strategy='order' and has been automatically set to False.",
                  Warning)

  if back is None :
    if back_mle :
      fitted_back, param_back = perform_mle_background (freq, psd, n_harvey=n_harvey, r=r, m=m, teff=teff, guess=guess_back, 
                                dnu=dnu, numax=numax, frozen_param=frozen_param_back, power_law=power_law,
                                frozen_harvey_exponent=frozen_harvey_exponent, low_cut=low_cut, fit_log=True, quickfit=quickfit,
                                low_bounds=low_bounds_back, up_bounds=up_bounds_back, no_bounds=False, high_cut_plaw=high_cut_plaw,
                                show=False, show_guess=False, filename=filename_back, spectro=spectro,
                                apodisation=apodisation, num=num, num_numax=num_numax, show_gaussian=show_gaussian, 
                                reboxing_behaviour=reboxing_behaviour, reboxing_strategy=reboxing_strategy,
                                transparent=False, facecolor='white', dpi=dpi)
      np.savetxt (path.splitext (filename_back)[0]+'_parameters.dat', param_back, fmt='%-s', 
                  header=make_header_background_param (n_harvey=n_harvey, author=author, mcmc=False))
    else :
      param_back = guess_back

    if back_mcmc :
      fitted_back, param_back, sigma_back = explore_distribution_background (freq, psd, dnu=dnu, 
                                       n_harvey=n_harvey, r=r, m=m, teff=teff, guess=param_back, frozen_param=frozen_param_back, power_law=power_law,
                                       frozen_harvey_exponent=frozen_harvey_exponent, low_cut=low_cut, fit_log=True, quickfit=quickfit,
                                       low_bounds=low_bounds_back, up_bounds=up_bounds_back, spectro=spectro, 
                                       show=False, show_guess=False, show_corner=show_corner, estimate_autocorrelation=estimate_autocorrelation,
                                       nsteps=nsteps_mcmc_back, filename=filename_back, parallelise=progress, progress=progress, nwalkers=nwalkers, 
                                       filemcmc=filemcmc_back, discard=discard_back, thin=thin_back, norm=norm_back, 
                                       save_only_after_sampling=save_only_after_sampling, high_cut_plaw=high_cut_plaw,
                                       apodisation=apodisation, num=num, num_numax=num_numax, reboxing_behaviour=reboxing_behaviour,
                                       reboxing_strategy=reboxing_strategy, bins=bins, existing_chains=existing_chains_back,
                                       transparent=False, facecolor='white', dpi=dpi, format_cornerplot=format_cornerplot,
                                       plot_datapoints=plot_datapoints, show_gaussian=show_gaussian)
      np.savetxt (path.splitext (filename_back)[0]+'_parameters.dat', np.c_[param_back, sigma_back], fmt='%-s', 
                  header=make_header_background_param (n_harvey=n_harvey, author=author, apodisation=apodisation,
                                                       low_cut=low_cut, nwalkers=nwalkers, nsteps=nsteps_mcmc_back, discard=discard_back,
                                                       reboxing_behaviour=reboxing_behaviour, quickfit=quickfit))
    
    if use_numax_back :
      numax = param_back[n_harvey*3+3]
    Wenv = param_back[n_harvey*3+4] 

    if save_background_vector :
      np.savetxt (path.splitext(filename_back)[0]+'.dat', fitted_back, fmt='%-s', 
                  header=make_header_background_vector (author=author,apodisation=apodisation,
                                                        low_cut=low_cut, nwalkers=nwalkers, nsteps=nsteps_mcmc_back, 
                                                        discard=discard_back,
                                                        reboxing_behaviour=reboxing_behaviour, quickfit=quickfit))

  else :
    fitted_back = back


  if dnu is None :
    dnu = dnu_scale (r, m)

  if numax is None :
    numax = numax_scale (r, m, teff)

  if Hmax is None :
    Hmax = 0.5 * np.max (psd[(freq>0.99*numax)&(freq<1.01*numax)]) 


  if a2z_in is None :

    if existing_chains_pattern in ['sample', 'read'] and pattern_mcmc:
      if path.exists (filemcmc_pattern) :
        pattern_mle=False
        if guess_pattern is None :
          guess_pattern = first_guess_mcmc (dnu, numax, teff, Hmax, Wenv, mass=m)
        norm_pattern = np.loadtxt (path.splitext (filemcmc_pattern)[0] + '.dat', usecols=0)
       

    if pattern_mle :
      df_a2z, pattern = perform_mle_pattern (dnu, numax, Hmax, Wenv, teff, freq, psd, back=fitted_back, 
                                             wdw=wdw, epsilon=epsilon, width=width, alpha=alpha, d01=d01,
                                             d02=d02, d13=d13, guess=guess_pattern, low_bounds=low_bounds_pattern,
                                             up_bounds=up_bounds_pattern, amp_l=amp_l,
                                             n_order=n_order, split=0, angle=90, fit_l1=fit_l1, 
                                             fit_l3=fit_l3, mass=m, show=False, filename=filename_pattern,
                                             transparent=False, facecolor='white', dpi=dpi)
      # Setting value to None to avoid overriding the MLE results at the MCMC step
      epsilon = None
      alpha = None
      d01 = None
      d02 = None 
      d13 = None
      width = None
      
    else :
      pattern = guess_pattern

    if pattern_mcmc :
      df_a2z, pattern, sigma_pattern = explore_distribution_pattern (dnu, numax, Hmax, Wenv, teff, freq, psd, back=fitted_back, wdw=wdw,
                                                                     n_order=n_order, split=0, angle=90, fit_l1=fit_l1, 
                                                                     fit_l3=fit_l3, mass=m, guess=pattern, low_bounds=low_bounds_pattern,
                                                                     up_bounds=up_bounds_pattern, show=False, norm=norm_pattern,
                                                                     show_corner=show_corner, nsteps=nsteps_mcmc_pattern, 
                                                                     estimate_autocorrelation=estimate_autocorrelation,
                                                                     filename=filename_pattern, parallelise=parallelise, progress=progress,
                                                                     nwalkers=nwalkers, filemcmc=filemcmc_pattern, discard=discard_pattern, 
                                                                     thin=thin_pattern, save_only_after_sampling=save_only_after_sampling, 
                                                                     bins=bins, existing_chains=existing_chains_pattern,
                                                                     epsilon=epsilon, alpha=alpha, width=width,
                                                                     d02=d02, d01=d01, d13=d13, amp_l=amp_l, 
                                                                     format_cornerplot=format_cornerplot, plot_datapoints=plot_datapoints,
                                                                     transparent=False, facecolor='white', dpi=dpi)

      np.savetxt (path.splitext (filename_pattern)[0]+'.dat', np.c_[pattern, sigma_pattern], fmt='%-s', 
                  header=make_header_pattern (author=author, fit_l1=fit_l1, fit_l3=fit_l3))

    else : 
      np.savetxt (path.splitext (filename_pattern)[0]+'.dat', pattern, fmt='%-s', 
                  header=make_header_pattern (author=author, fit_l1=fit_l1, fit_l3=fit_l3,
                                              nwalkers=nwalkers, nsteps=nsteps_mcmc_pattern, 
                                              discard=discard_pattern,
                                              n_order=n_order))
    if h0_screening :
      n_order_peakbagging = 20
    orders_for_peakbagging = list_order_to_fit (numax, dnu, n_order=n_order_peakbagging) 
    if strategy=='global' :
      # This will avoid creating an angle and splittings parameter per order if the fitting
      # strategy is set on 'global'. Remember that ``fit_splittings_per_order_in_global``
      # allows fitting one splittings per order even in ``strategy='global'``.
      fit_a = fit_angle
      fit_s = fit_splittings
      fit_angle = False
      fit_splittings = fit_splittings_per_order_in_global
    df_a2z = pattern_to_a2z (*pattern, split=guess_split, angle=guess_angle, orders=orders_for_peakbagging, angle_order=fit_angle, 
                             splitting_order=fit_splittings, common_width=common_width, amp_l=amp_l)
    if strategy=='global' :
      fit_angle = fit_a
      fit_splittings = fit_s

    if h0_screening :
      #Max rebinning is at 5 muHz (arbitrary) or 99 bin
      tmax = min (5 / np.median (np.diff (freq)), 99)
      df_a2z = select_mode_to_fit (freq, psd, fitted_back, df_a2z, tmax=tmax)
    save_a2z (a2z_file, df_a2z)

  if not nopeakbagging :
    if a2z_in is None :
      a2z_to_read = a2z_file
    else :
      a2z_to_read = a2z_in
     
    df_a2z, pkb = peakbagging (a2z_to_read, freq, psd, back=fitted_back,
                               wdw=wdw, spectro=spectro, nsteps_mcmc=nsteps_mcmc_peakbagging,
                               show_corner=show_corner, store_chains=True, mcmcDir=mcmcDir, order_to_fit=None,
                               parallelise=parallelise, progress=progress, strategy=strategy,
                               nwalkers=nwalkers, normalise=False, instr=instr, thin=thin_pkb,
                               filename_summary=filename_peakbagging, show_summary=False,
                               discard=discard_pkb, format_cornerplot=format_cornerplot,
                               save_only_after_sampling=save_only_after_sampling, restrict=True,
                               fit_amp=fit_amp, extended=extended, projected_splittings=projected_splittings,
                               bins=bins, existing_chains=existing_chains_pkb, fit_splittings=fit_splittings,
                               fit_angle=fit_angle, fit_amplitude_ratio=fit_amplitude_ratio, dpi=dpi,
                               estimate_autocorrelation=estimate_autocorrelation, plot_datapoints=plot_datapoints)

    save_a2z (a2z_file, df_a2z)

  if nopeakbagging :
    pkb = a2z_to_pkb (df_a2z)
    pkb = sort_pkb (pkb)
    extended = False
  
  save_pkb (path.splitext (a2z_file)[0]+'.pkb', pkb, fmt=pkb_fmt, 
            author=author, extended=extended, spectro=spectro, 
            projected_splittings=projected_splittings, nwalkers=nwalkers, nsteps=nsteps_mcmc_peakbagging, 
            discard=discard_pkb, fit_amp=fit_amp) 

  return 

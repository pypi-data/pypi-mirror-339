import os, pytest
import glob
import warnings 
import apollinaire as apn
import apollinaire.peakbagging as apn_pb
import apollinaire.peakbagging.templates as templates
import apollinaire.peakbagging.test_data as test_data
import apollinaire.timeseries as timeseries
import importlib.resources
import pandas as pd
import numpy as np

# Defining some environment variables
ignore_deprecation = os.environ.get('APN_TEST_IGNORE_DEPRECATION_WARNING', 'True')
if ignore_deprecation :
  #Ignore deprecation warning 
  warnings.simplefilter('ignore', category=[DeprecationWarning,
                                            PendingDeprecationWarning])

class TestDataManipulation :
  '''
  A collection of tests to check that data manipulation
  methods behave correctly.
  '''

  @pytest.fixture(scope="class")
  def df_a2z (self) :
    '''
    Load data for test and proceed for a first a2z check.
    '''
    f = importlib.resources.path (templates, 'test.a2z')
    with f as filename :
      df = apn_pb.read_a2z (filename)
      apn_pb.check_a2z (df, verbose=False)
    return df
    
  @pytest.fixture(scope="class")
  def pkb (self, df_a2z) :
    return apn_pb.a2z_to_pkb (df_a2z)

  @pytest.fixture(scope="class")
  def verif_pkb (self) :
    f = importlib.resources.path (templates, 'verif.pkb')
    with f as filename :
      return np.loadtxt (filename)

  def test_a2z_pkb_validity (self, df_a2z, pkb, verif_pkb) :
    assert (~np.any (np.isnan (pkb)))
    assert (np.all (apn_pb.get_list_order (df_a2z)==[5, 21, 22]))
    # Test if the pkb array contains the expected values.'
    residual = np.abs (pkb - verif_pkb)
    error = np.linalg.norm (residual.ravel(), ord=np.inf)
    assert (error < 1.e-6,) 

  def test_compute_model (self, pkb) :
    freq = np.linspace (0, 5000, 10000)
    model = apn_pb.compute_model (freq, pkb)
    # Test if the model built from the test pkb array contains NaN.
    assert (~np.any (np.isnan (model)))

  def test_psd_computation (self) :
    t, v = timeseries.load_light_curve (star='006603624')
    assert (t.shape == (1684776,))
    assert (v.shape == (1684776,))
    assert (~np.any (np.isnan (t)))
    assert (~np.any (np.isnan (v)))
    dt = np.median (t[1:] - t[:-1]) * 86400
    freq, psd = apn.psd.series_to_psd (v, dt=dt, correct_dc=True)
    freq, psd, n_chunk = apn.psd.mean_psd (v, dt)

  def test_light_curve_and_guess (self) :
    # Test importation and light curves management function
    t, v = timeseries.load_light_curve (star='006603624')
    assert (t.shape == (1684776,))
    assert (v.shape == (1684776,))
    assert (~np.any (np.isnan (t)))
    assert (~np.any (np.isnan (v)))
    dt = np.median (t[1:] - t[:-1]) * 86400
    freq, psd = apn.psd.series_to_psd (v, dt=dt, correct_dc=True)
    freq, psd = freq*1e6, psd*1e-6
    guess, low_bounds, up_bounds, labels = apn_pb.create_background_guess_arrays (freq, psd, r=1.162, m=1.027, teff=5671.,
                                                                                  n_harvey=2, spectro=False, power_law=False,
                                                                                  high_cut_plaw=100., return_labels=True)
    # Test if the background guess array contains NaN
    assert (~np.any (np.isnan (guess))) 
    # Test if the background low bounds array contains NaN
    assert (~np.any (np.isnan (low_bounds))) 
    # Test if the background up bounds array contains NaN
    assert (~np.any (np.isnan (up_bounds))) 
    # Test if the resulting background model contains NaN
    back = apn_pb.build_background(freq, guess, n_harvey=2, 
                                   apodisation=False, remove_gaussian=True)
    assert (~np.any (np.isnan (back))) 

  def test_load_golf_timeseries (self) :
    v = apn.timeseries.load_golf_timeseries ()
    assert (~np.any (np.isnan (v)))

  def test_formatting (self) :
    labels=['freq', 'freq', 'freq', 'freq', 
             'width', 'height', 'angle', 
             'width', 'height', 'amplitude', 
             'split', 'proj_split',
             'background', 'asym',
             'amp_l']
    orders=['18', '19', '20', '21',
            'a', 'a', 'a',
            '18', '18', '18',
            'a', 'a', 
            'a', '20',
            'a']
    degrees=['0', '1', '2', '3', 
             'a', 'a', 'a',
             '1', '1', 'a',
             'a', 'a', 
             'a', 'a',
             '1']
    formatted = apn_pb.param_array_to_latex (labels, orders, degrees)
    expected = ['$\\nu_{18,0}$', '$\\nu_{19,1}$', '$\\nu_{20,2}$', '$\\nu_{21,3}$', 
                '$\\Gamma_{n,\\ell}$', '$H_{n,\\ell}$', '$i$', 
                '$\\Gamma_{18,1}$', '$H_{18,1}$', '$A_{18,\\ell}$', 
                '$s_{n,\\ell}$', '$\\sin i . s_{n,\\ell}$', 
                '$B$', '$\\alpha_{20,\\ell}$', '$V_{1} / V_0$']
    assert (formatted==expected)
     

class TestChainReading :
  '''
  A class to test chain reading methods.
  '''
  def test_chain_reading (self) :
    f1 = importlib.resources.path (test_data, 'mcmc_background.h5')
    f2 = importlib.resources.path (test_data, 'mcmc_pattern.h5')
    f3 = importlib.resources.path (test_data, 'mcmc_sampler_order_20.h5')
    with f1 as filename :
      flatchain, labels = apn_pb.read_chain (filename, thin=1, discard=0, read_order=True,
                                             chain_type='background', fit_amp=False,
                                             projected_splittings=False)
      assert (np.all (labels==['A_H_1', 'nuc_H_1', 'alpha_H_1', 
                                        'A_H_2', 'nuc_H_2', 'alpha_H_2', 
                                        'A_Gauss', 'numax', 'Wenv', 'noise']))
    with f2 as filename :
      flatchain, labels = apn_pb.read_chain (filename, thin=1, discard=0, read_order=True,
                                             chain_type='pattern', fit_amp=False,
                                             projected_splittings=False)
      assert (np.all (labels==['eps', 'alpha', 'Dnu', 'numax', 'Hmax',
                               'Wenv', 'w', 'd02', 'b02', 'd01', 'b01', 'd13', 'b03']))
    with f3 as filename :
      flatchain, labels, degrees, order = apn_pb.read_chain (filename, thin=1, discard=0, read_order=True,
                                                             chain_type='peakbagging', fit_amp=False,
                                                             projected_splittings=False)
      assert (np.all (labels==['freq', 'freq', 'freq', 'freq', 'width', 'height', 'background']))
      assert (np.all (degrees==['0', '1', '2', '3', 'a', 'a', 'a']))
      assert (order==20)

  def test_hdf5_to_a2z (self) :
    pkb = apn_pb.hdf5_to_pkb (workDir=os.path.dirname (test_data.__file__), 
                       pkbname=None, discard=0, thin=10, 
                       instr='geometric', extended=False)
    assert (~np.any (np.isnan (pkb)))
    assert (pkb.shape[1]==14)
    pkb = apn_pb.hdf5_to_pkb (workDir=os.path.dirname (test_data.__file__), 
                       pkbname=None, discard=0, thin=10, 
                       instr='geometric', extended=True)
    assert (~np.any (np.isnan (pkb)))
    assert (pkb.shape[1]==20)
    
class TestIntegration :
  '''
  A class to execute integration tests and check that they
  finish without raising any exception. 
  '''

  @pytest.fixture(scope="class")
  def tmp_dir (self, tmp_path_factory) :
    tmp = tmp_path_factory.mktemp ("tmp")
    return tmp

  def test_stellar_framework (self, tmp_dir) :
    t, v = timeseries.load_light_curve (star='006603624')
    dt = np.median (t[1:] - t[:-1]) * 86400
    freq, psd = apn.psd.series_to_psd (v, dt=dt, correct_dc=True)
    freq = freq*1e6
    psd = psd*1e-6
    r, m, teff = 1.162, 1.027, 5671

    filename_back = os.path.join (tmp_dir, "background.png")
    filemcmc_back = os.path.join (tmp_dir, "mcmc_background.h5")
    filename_pattern = os.path.join (tmp_dir, "pattern.png")
    filemcmc_pattern = os.path.join (tmp_dir, "mcmc_pattern.h5")
    a2z_file = os.path.join (tmp_dir, "modes_param.a2z")
    mcmcDir = tmp_dir
    filename_peakbagging = os.path.join (tmp_dir, "summary_peakbagging.png")

    apn_pb.stellar_framework (freq, psd, r, m, teff, n_harvey=2, low_cut=50., filename_back=filename_back,
                                   filemcmc_back=filemcmc_back, nsteps_mcmc_back=10, n_order=3, 
                                   n_order_peakbagging=3, filename_pattern=filename_pattern, fit_l3=True,
                                   filemcmc_pattern=filemcmc_pattern, nsteps_mcmc_pattern=10, parallelise=True, 
                                   quickfit=True, num=500, discard_back=1, discard_pattern=1, discard_pkb=1, 
                                   progress=True, bins=50, extended=True, mcmcDir=mcmcDir, 
                                   a2z_file=a2z_file, format_cornerplot='png', nsteps_mcmc_peakbagging=10, 
                                   filename_peakbagging=filename_peakbagging, dpi=100, plot_datapoints=False)







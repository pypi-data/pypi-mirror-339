"""
Implementation of Grid class
Extends and modifies Ed's GridModel to contain the raster data to be fit
"""
import warnings
import numpy as np
from copy import deepcopy
from itertools import product
from collections import namedtuple
from astropy.modeling.fitting import TRFLSQFitter, parallel_fit_dask
from .util import _none_to_nan, eliminate_axis
from multiprocessing import Pool, cpu_count, Manager

class Grid:
    """
    Represents raster data to be fit and array of models 
    each of which can have different fit values but all with 
    the same structure	
    """
    _worker_ret_val = namedtuple('_worker_ret_val', ('fit', 'chi_sq', 'fit_info')) 

    def __init__(self, model, wavelength, intensity, uncertainty=None, mask=None, user_mask=None) :
        """
        model:        (astropy.Model) Description of the underlying model to use for fitting
                      Initial parameters at all points will be set to match it.
        wavelength:   (np.array) The independent variable.  Most likely wavelength.  (N,)
        intensity:    (np.array) The dependent variable.  Most likely intensity.  (N,X,Y)
        uncertainty:  (np.array) Uncertainty of the independent variable.  (N,X,Y)
        mask:         (boolean np.array) Indicates data to ignore during fitting. (N,X,Y) [Default is no mask]
                                         Use is driven by bad data or data filters
        user_mask:    (boolean np.array) Location points to ignore / not fit.  (X,Y)  [Default is no mask]
                                         Use is driven by User not wanting to fit the spectra at a given location
        fitter_type   (astropy.modeling.fitting._FitterMeta) Fitter type to be used.  Default is TRFLSQ
        """
        self.shape = Grid._check_dimensions(wavelength, intensity, model)
        self._wavelength = wavelength.copy()
        self._intensity = intensity.copy()
        self._data_mask = Grid._load_mask(mask, self._intensity.shape) # To block bad data points within a spectra
        self._user_mask = Grid._load_mask(user_mask, self.shape)  # To block fitting of an entire spectra/ key (a.k.a. one (x,y) location)
        self._fitter_weights = Grid._load_weights(uncertainty, self._intensity.shape)
        self._fitter_type = TRFLSQFitter
        self._has_fit = False
        self._last_fit_parallel = False # Used to track whether last fit was with dask call (no uncertainty avail.)
        self.analysis_point = AnalysisPoint()

        # chi squared and number of degress of freedom at each point
        # TODO: initialize on fill?
        self.chi_sq = np.full(self.shape, np.nan) #Can only set after a fit
        self.dof    = np.full(self.shape, -1, dtype=np.int32)  #I think yes this could be initialized once _model is set
        self.cov_matrix = np.empty(self.shape, dtype=object)
        self.fit_info = np.empty(self.shape, dtype=object)

        # model values and std arrays by parameter name
        self._values = dict()
        self._stds = dict()
        self._model = model.copy()
        for param_name in self._model.param_names :
            parameter = getattr(self._model, param_name)
            self._values[param_name] = np.full(self.shape, parameter.value)
            self._stds[param_name] = np.full(self.shape, _none_to_nan(parameter.std))
        self.param_names = list(self._model.param_names)
        self._model.sync_constraints = True # Allow us to make changes to the model and its parameters TODO:verify
        self._free_param_count = sum(1 for param_name in self.param_names if not (self._model.fixed[param_name] or self._model.tied[param_name]))

    # # State used for pickling. Needed for working of the thread Pool (at least as implemented now)
    def __getstate__(self) :
        return {'shape' : self.shape,
                'param_names' : self.param_names,
                '_model'      : self._model,
                '_values'     : self._values,
                '_stds'       : self._stds,
                '_free_param_count' : self._free_param_count,
                '_wavelength' :  self._wavelength,
                '_intensity' :  self._intensity,
                '_data_mask' :  self._data_mask,
                '_user_mask' :  self._user_mask,
                '_fitter_weights' :  self._fitter_weights,
                '_fitter_type' :  self._fitter_type,
                '_has_fit' :  self._has_fit,
                '_last_fit_parallel' : self._last_fit_parallel,
                'analysis_point' :  self.analysis_point,
                'chi_sq' : self.chi_sq,
                'dof' : self.dof,
                'cov_matrix' : self.cov_matrix,
                'fit_info' : self.fit_info,
        }

    # For un-pickling (again, needed for the thread Pool())
    def __setstate__(self, state) : self.__dict__.update(state)
    
    # Get a model for the key specified
    def __getitem__(self, key) :
        if key is None:
            key = (self.analysis_point.get_index('x_index'), self.analysis_point.get_index('y_index'))

        if self._user_mask[key]:
            return None
        
        model = self._model.copy()
        model.sync_constraints = True

        for param_name in self.param_names :
            parameter = getattr(model, param_name)
            parameter.value = self._values[param_name][key]
            parameter.std   = self._stds[param_name][key]
        
        return model
    
    # Set the values and stds for the point from the passed model (fit) 
    def __setitem__(self, key, fit) :
        for param_name in self.param_names :
            parameter = getattr(fit, param_name)
            
            self._values[param_name][key] = parameter.value
            self._stds[param_name][key] = _none_to_nan(parameter.std)
    
    
    # Get the _GridParameter object the represents the parameter asked for in name
    def __getattr__(self, name) :
        if name in self.param_names :
            return _GridParameter(getattr(self._model, name), self, name)
        
        raise AttributeError(f"'Grid' object has no attribute '{name}'")


    def set_mask(self, key):
        self._user_mask[key] = True
        self.chi_sq[key] = np.nan
        self.dof[key] = -1
        self.cov_matrix[key] = None
        self.fit_info[key] = None

    def unset_mask(self, key):
        self._user_mask[key] = False

    def toggle_mask(self, key):
        current = self._user_mask[key]
        self._user_mask[key] = not current


    def is_fitted(self):
        """
        Return state of whether the whole grid has been fitted or not
        """
        return self._has_fit
    

    def fit(self, key=None, calc_uncertainties=True, parallel=False, **kwds):
        """
        Adjust Grid fitting in place

        key:    (2 item tuple) If passed, fit only at this point.  
                Default is to fit all the points in the Grid
                
        calc_uncertainties:  (boolean) Should std and uncertainties by calculated

        parallel: (boolean) should astropy parallel_fit_dask function be used

        all other keywords are passed to the fitter        
        """
        fitter = self._fitter_type(calc_uncertainties=calc_uncertainties)

        if key is None:
            print("Fitting across the grid. This may take a few minutes . . . ")
            if parallel:
                self._last_fit_parallel = True
                if 'diagnostics_path' not in kwds.keys():
                    diagnostics_path = None
                else:
                    diagnostics_path = kwds['diagnostics_path']
                self._fit_parallel(fitter, diagnostics_path=diagnostics_path)
            else:
                self._last_fit_parallel = False
                kwds.pop('diagnostics_path', None) 
                for key in product(*(range(s) for s in self.shape)) : # Loop over all points
                    if not self._user_mask[key]:
                        self._fit_one(key, fitter, from_grid_fit=True, **kwds)
            if not self._has_fit: self._has_fit = True
        else:
            if self._user_mask[key]:
                print(f"{key} is masked out. No fitting performed.")
            else:
                self._fit_one(key, fitter, **kwds)
        self.calc_model_grid(parallel=parallel) #TODO -this stores the model vals for easier retrieval. Why not do this within the earlier parts of the fit call?
        self.calc_residuals()


    @staticmethod
    def _load_model(model):
        if type(model) == Grid:
            newmodel = model._model.copy()
        else:
            newmodel = model.copy()
        newmodel.sync_constraints = True # Allow us to make changes to the model and its parameters TODO:verify
        return newmodel
        
    @staticmethod
    def _check_dimensions(wavelength, intensity, model):
        assert wavelength.ndim == 1, "wavelength should be 1D"
        assert intensity.ndim == 3, "intensity should be 3D"
        assert wavelength.shape[0] == intensity.shape[0], "wavelength and intensity dimensions don't match"
        grid_shape = eliminate_axis(intensity.shape, axis=0)
        if type(model) == Grid:
            assert model.shape == grid_shape, "model grid dimension does not match" 
        return grid_shape

    @staticmethod
    def _load_mask(mask, shape):
        if mask is None:
            return np.full(shape, False)
        elif mask.shape != shape:
            warnings.warn('Mask shape does not match.  Removing mask.')
            return np.full(shape, False)
        else:
            return mask.astype(bool)

    @staticmethod
    def _load_weights(uncertainty, shape):
        if uncertainty is None:
            return np.ones(shape)
        elif uncertainty.shape != shape:
            warnings.warn('Uncertainty shape does not match.  All fitting weights set to 1')
            return np.ones(shape)
        else:
            return 1 / uncertainty

    # Do the work of fitting
    @staticmethod
    def _fit_worker(fitter, model, x, y, weights, **kwds) :
        fit = fitter(model, x, y, weights=weights, **kwds)
        chi_sq = np.sum(((fit(x) - y) * weights)**2)
        return Grid._worker_ret_val(fit, chi_sq, deepcopy(fitter.fit_info))

    def _fit_one(self, key, fitter, from_grid_fit=False, **kwds):
        # set keyword from_grid_fit to True if this is being called in a loop to fit the entire grid
        in_key = (slice(None),) + key
        include = np.invert(self._data_mask[in_key]) # Points to include (not masked)

        self.dof[key] = np.sum(include) - self._free_param_count # Degrees of freedom
        
        # If there are non-negative DoF and all values are not NaN
        if self.dof[key] >= 0 and not any(np.isnan(self._values[param_name][key]) for param_name in self.param_names) :  #TODO - I don't think this is checking what it says it's checking - AAN 4/2025
            # Execute the fit and set the values and chi squared
            ret_val = Grid._fit_worker(fitter, 
                                       self[key], 
                                       self._wavelength[include], 
                                       self._intensity[in_key][include], 
                                       self._fitter_weights[in_key][include], 
                                       **kwds) 
            self[key] = ret_val.fit
            self.chi_sq[key] = ret_val.chi_sq
            self.cov_matrix[key] = ret_val.fit.cov_matrix
            self.fit_info[key] = ret_val.fit_info
            
        else :
            self.set_mask(key)  # Mask it if insufficient degrees of freedom so we can handle these missing Parameters later
        if not from_grid_fit:
            self.calc_model_point(key)
            self.calc_residuals(grid_key=key)
    
    def _fit_parallel(self, fitter, diagnostics_path=None):
        lambda_tuple = (self._wavelength,)
        fit_mask = deepcopy(self._data_mask)
        data = deepcopy(self._intensity)
        nandata = np.isnan(data)
        data[nandata] = 0 # These points are masked, setting them to 0 so the function can be fit (still requires non-NaN values even for masked points)
        fit_mask[nandata] = True # Make sure NaN values are masked for fitting
        fit_mask[:, self._user_mask] = True # Also same compution time by not fitting unwanted spectra

        if self.is_fitted(): # Make the fit start with existing initial settings for parameters at each grid point if they exist
            model = deepcopy(self._model) 
            model.sync_constraints = True
            for param_name in self.param_names :
                parameter = getattr(model, param_name)
                parameter.value = self._values[param_name]  # These are numpy arrays
                parameter.std   = self._stds[param_name]
        
        if diagnostics_path is None:
            fit = parallel_fit_dask(model=self._model, fitter=fitter, mask=fit_mask, world=lambda_tuple, data=data, fitting_axes=0)
        else:
            fit = parallel_fit_dask(model=self._model, fitter=fitter, mask=fit_mask, world=lambda_tuple, data=data, fitting_axes=0, diagnostics='all', diagnostics_path=diagnostics_path)
        for param in fit.param_names:
            self.__getattr__(param).value = fit.__getattr__(param).value

 
    def calc_residuals(self, grid_key=None):
        """
        if grid_key is not given, residuals will be calculated for the whole grid
        
        if grid_key is given, self.residual_vals must already exist, and residuals will only be calculated for thay point
        grid_key must be a list or tuple of length 2 to represent (x_index, y_index)
        """
        if grid_key is None:
            self.residual_vals = self._intensity - self.model_vals
        else:
            xi, yi = grid_key
            for li, _ in enumerate(self._wavelength):
                self.residual_vals[li, xi, yi] = self._intensity[li, xi, yi] - self.model_vals[li, xi, yi]

    def calc_model_grid(self, parallel=True):  # Can we just do this inside the Pool() fit loop or dask call?
        data_shape = np.shape(self._intensity)
        grid_keys = product(range(data_shape[1]), range(data_shape[2]))
        if parallel:
            manager = Manager()
            model_vals = manager.dict()
            f_inputs = [(key, model_vals) for key in grid_keys if not self._user_mask[key]] # Just process for unmasked keys
            with Pool(processes=(cpu_count() - 1)) as pool:
                pool.starmap(self.calc_model_point_from_map, f_inputs)
            self.model_vals_as_list(model_vals)
        else:
            self.model_vals = np.zeros_like(self._intensity)      # ? Make this NaN?
            for grid_key in grid_keys:
                if not self._user_mask[grid_key]:
                    self.calc_model_point(grid_key)

    def calc_model_point_from_map(self, key, model_vals):
        x_index, y_index = key
        model = self.__getitem__((x_index, y_index))
        model_vals[key] = model(self._wavelength)

    def calc_model_point(self, key):
        if key is None:
            x_index = self.analysis_point.get_index('x_index')
            y_index = self.analysis_point.get_index('y_index')
        else:
            x_index, y_index = key
        model = self.__getitem__((x_index, y_index))
        model_vals_subset = model(self._wavelength)
        for lambda_index, model_val in enumerate(model_vals_subset):
            self.model_vals[lambda_index, x_index, y_index] = model_val

    def model_vals_as_list(self, model_vals_dict):
        self.model_vals = np.zeros_like(self._intensity)
        for grid_key, model_spectra_vals in model_vals_dict.items():
            xi, yi = grid_key
            for li, model_val in enumerate(model_spectra_vals):
                self.model_vals[li, xi, yi] = model_val

    def get_data_subset(self, data, fixed_lambda=False, fixed_x=False, fixed_y=False):
        assert len(data.shape) in (2, 3), 'Data has invalid shape'
        fixed = {'lambda': fixed_lambda, 'x': fixed_x, 'y': fixed_y}
        ap_vars = vars(self.analysis_point)
        index_dict = {}
        for var in fixed.keys():
            if  var == 'lambda' and len(data.shape) == 2: # Data slice - ignore lambda
                continue
            if fixed[var]:
                for ap_var in ap_vars.keys():
                    if var + '_' in ap_var:
                        index = self.analysis_point.get_index(ap_var)
                        assert index is not None, 'Index {} in AnalysisPoint Object cannot be set to None'.format(ap_var)
                        index_dict[var] = index
            else:
                index_dict[var] = slice(None)
        if len(data.shape) == 3:
            return data[index_dict['lambda'], index_dict['x'], index_dict['y']]
        elif len(data.shape) == 2:
            return data[index_dict['x'], index_dict['y']]


    def get_results(self):
        """
        Return a simple structure holding the model description and the 
        parameter arrays for each x,y grid point.
        Masked points will have np.nan parameter values
        """
        results_dict = dict()
        results_dict['model'] = self._model.copy() 
        results_dict['mask'] = self._user_mask.copy()
        results_dict['fit_info'] = self.fit_info.copy()
        for param_name in self.param_names:
            results_dict[param_name] = self.__getattr__(param_name).value # This should handle masking out _user_mask-ed points
        if self._last_fit_parallel:
            # Uncertainty wasn't computed in this case
            results_dict['chi_sq'] = None
            results_dict['cov_matrix'] = None
        else:
            results_dict['chi_sq'] = self.chi_sq.copy() 
            results_dict['cov_matrix'] = self.cov_matrix.copy()
        
        return results_dict



class AnalysisPoint:
    def __init__(self):
        self.lambda_index = None
        self.x_index = None
        self.y_index = None

    def get_point(self):
        return (self.get_index('lambda_index'), self.get_index('x_index'), self.get_index('y_index'))

    def get_index(self, index_name):
        assert index_name in self.__dict__.keys(), '{} is not a valid index name'.format(index_name)
        return self.__dict__[index_name]

    def set_index(self, index_name, index):
        assert index_name in self.__dict__.keys(), '{} is not a valid index name'.format(index_name)
        assert type(index) is int, 'index must be an integer' # TODO: Instead of error, create dialog window with warning, keep index the same.
        self.__dict__[index_name] = index
    
    def set_point(self, point):
        index_list = ['lambda_index', 'x_index', 'y_index']
        for i, index_name in enumerate(index_list):
            self.set_index(index_name, point[i])

class _GridParameter :
    """ Represents one parameter in a Grid """
    def __init__(self, parameter, grid_model, param_name) :
        self._parameter = parameter # Corresponding parameter from model
        self._grid_model = grid_model # Corresponding Grid object
        self._param_name = param_name # Name
    
    # Get/Set the value array from the Grid 
    @property
    def value(self) :
        masked_vals = self._grid_model._values[self._param_name]
        masked_vals[self._grid_model._user_mask] = np.nan
        return masked_vals
    
    @value.setter
    def value(self, value) :
        self._grid_model._values[self._param_name] = value
    
    # Get std from the Grid
    @property
    def std(self) :
        masked_stds = self._grid_model._stds[self._param_name]
        masked_stds[self._grid_model._user_mask] = np.nan
        return masked_stds
    
    # Calculate uncertainty TODO:??
    @property
    def uncertainty(self) :
        masked_unc = np.sqrt(self._grid_model.dof / self._grid_model.chi_sq) * self._grid_model._stds[self._param_name]
        masked_unc[self._grid_model._user_mask] = np.nan
        return masked_unc
    
    # Get/Set properties of the parameter
    # Pass though
    @property
    def fixed(self) : return self._parameter.fixed
    
    @fixed.setter
    def fixed(self, value) : self._parameter.fixed = value
    
    @property
    def tied(self) : return self._parameter.tied
    
    @tied.setter
    def tied(self, value) : self._parameter.tied = value
    
    @property
    def bounds(self) : return self._parameter.bounds
    
    @bounds.setter
    def bounds(self, value) : self._parameter.bounds = value
    
    @property
    def min(self) : return self._parameter.min
    
    @min.setter
    def min(self, value) : self._parameter.min = value
    
    @property
    def max(self) : return self._parameter.max
    
    @max.setter
    def max(self, value) : self._parameter.max = value
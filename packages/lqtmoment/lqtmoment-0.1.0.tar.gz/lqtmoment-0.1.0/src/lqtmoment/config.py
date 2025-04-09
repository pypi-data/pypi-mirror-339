"""
Configuration module for the lqt-moment-magnitude package.

This module defines the `CONFIG` singleton, which provides configuration parameters for
magnitude calculations, spectral fitting, and performance options. Configurations are
organized into three dataclasses: `MagnitudeConfig`, `SpectralConfig`, and `PerformanceConfig`.
Default values are defined in the dataclasses, but users can override them by providing a
`config.ini` file in the parent directory of this module.

Usage:
    The `CONFIG` object is automatically loaded when the module is imported. To use the default
    configuration:

    ```python
    from lqt_moment_magnitude.config import CONFIG
    print(CONFIG.magnitude.SNR_THRESHOLD)  # Access magnitude configuration
    print(CONFIG.spectral.F_MIN)          # Access spectral configuration
    ```

    To override the configuration, create a `config.ini` file in the parent directory with the
    following structure:

    ```ini
        [Magnitude]
        snr_threshold = 2.0
        pre_filter = 0.01,0.02,55,60
        velocity_model_file = "data/config/velocity_model.json"

        [Spectral]
        f_min = 0.5
        f_max = 40.0
        default_n_samples = 2000

        [Performance]
        use_parallel = true
        logging_level = "DEBUG"
    ```

    For custom velocity model, the "velocity_model.json" file should have the 
    following structure:

    ```json
    {
        "layer_boundaries": [[-3.00, -1.90], [-1.90, -0.59], [-0.59, 0.22], [0.22, 2.50]],
        "velocity_vp": [2.68, 2.99, 3.95, 4.50],
        "velocity_vs": [1.60, 1.79, 2.37, 2.69],
        "density": [2700, 2700, 2700, 2700]
    }
    ```

    You can also reload the configuration from a custom file:

    ```python
    CONFIG.reload(config_file="new_config.ini")
    ```
"""

import importlib.resources as pkg_resources
from contextlib import contextmanager
from dataclasses import dataclass
from configparser import ConfigParser
from typing import List, Tuple
from pathlib import Path
import json

@contextmanager
def _package_file(filename):
    """ Helper function to access package files using importlib.resources. """
    with pkg_resources.path("lqtmoment.data", filename) as file_path:
        yield file_path

@dataclass
class MagnitudeConfig:
    """
    Configuration for magnitude calculation parameters.

    Attributes:
        SNR_THRESHOLD (float): Minimum signal-to-noise ratio for trace acceptance (default: 1.5).
        WATER_LEVEL (int): Water level for deconvolution stabilization (default: 30).
        PRE_FILTER (List[float]): Bandpass filter corners [f1,f2,f3,f4] in Hz (default: placeholder, override in config.ini).
        POST_FILTER_F_MIN (float): Minimum post-filter frequency in Hz (default: 0.1).
        POST_FILTER_F_MAX (float): Maximum post-filter frequency in Hz (default: 50).
        PADDING_BEFORE_ARRIVAL (float): Padding before arrival in seconds (default: 0.1).
        NOISE_DURATION (float): Noise window duration in seconds (default: 0.5).
        NOISE_PADDING (float): Noise window padding in seconds (default: 0.2).
        R_PATTERN_P (float): Radiation pattern for P-waves (default: 0.52).
        R_PATTERN_S (float): Radiation pattern for S-waves (default: 0.63).
        FREE_SURFACE_FACTOR (float): Free surface amplification factor (default: 2.0).
        K_P (float): Geometric spreading factor for P-waves (default: 0.32).
        K_S (float): Geometric spreading factor for S-waves (default: 0.21).
        LAYER_BOUNDARIES (List[Tuple[float, float]]): Depth boundaries in km (default: placeholder).
        VELOCITY_VP (List[float]): P-wave velocities in km/s (default: placeholder).
        VELOCITY_VS (List[float]): S-wave velocities in km/s (default: placeholder).
        DENSITY (List[float]): Densities in kg/m³ (default: placeholder).
        TAUP_MODEL (str): ObsPy 1-D Velocity model.
        VELOCITY_MODEL_FILE (str): Path to a JSON file defining the velocity model (default: "", uses built-in model).
    """
    SNR_THRESHOLD: float = 1.5
    WATER_LEVEL: int = 30
    PRE_FILTER: List[float] = None
    POST_FILTER_F_MIN: float = 0.1
    POST_FILTER_F_MAX: float = 50
    PADDING_BEFORE_ARRIVAL: float = 0.1
    NOISE_DURATION: float = 0.5
    NOISE_PADDING: float = 0.2
    R_PATTERN_P: float = 0.52
    R_PATTERN_S: float = 0.63
    FREE_SURFACE_FACTOR: float = 2.0
    K_P: float = 0.32
    K_S: float = 0.21
    LAYER_BOUNDARIES: List[List[float]] = None 
    VELOCITY_VP: List[float] = None
    VELOCITY_VS: List[float] = None
    DENSITY: List[float] = None
    TAUP_MODEL: str = 'iasp91'
    VELOCITY_MODEL_FILE: str = None
    MW_CONSTANT: float = 6.07

    def __post_init__(self):
        self.PRE_FILTER = self.PRE_FILTER or [0.01, 0.02, 55, 60]
        self.LAYER_BOUNDARIES = self.LAYER_BOUNDARIES or [
                [-3.00, -1.90], [-1.90, -0.59], [-0.59, 0.22], [0.22, 2.50],
                [2.50, 7.00], [7.00, 9.00], [9.00, 15.00], [15.00, 33.00], [33.00, 9999]
            ]
        self.VELOCITY_VP = self.VELOCITY_VP or [2.68, 2.99, 3.95, 4.50, 4.99, 5.60, 5.80, 6.40, 8.00]
        self.VELOCITY_VS = self.VELOCITY_VS or [1.60, 1.79, 2.37, 2.69, 2.99, 3.35, 3.47, 3.83, 4.79]
        self.DENSITY = self.DENSITY or [2700] * 9

        # Load velocity model from a defautl package JSON data
        if self.VELOCITY_MODEL_FILE == 'None' or self.VELOCITY_MODEL_FILE is None:
            try:
                with _package_file("velocity_model.json") as velocity_model_path:
                    with open(velocity_model_path, "r") as f:
                        model = json.load(f)
                    required_keys = {"layer_boundaries", "velocity_vp", "velocity_vs", "density"}
                    if not all(key in model for key in required_keys):
                        raise KeyError(f"Missing keys: {required_keys - set(model.keys())}")
                    self.LAYER_BOUNDARIES = model["layer_boundaries"]
                    self.VELOCITY_VP = model["velocity_vp"]
                    self.VELOCITY_VS = model["velocity_vs"]
                    self.DENSITY = model["density"]
            except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
                print(f"Failed to load velocity model: {e}. Using defaults")
                    
        else:
            # Load from user-specified file
            try:
                with open(self.VELOCITY_MODEL_FILE, "r") as f:
                    model = json.load(f)
                required_keys = {"layer_boundaries", "velocity_vp", "velocity_vs", "density"}
                if not all(key in model for key in required_keys):
                    raise KeyError(f"Missing keys: {required_keys - set(model.keys())}")
                self.LAYER_BOUNDARIES = model["layer_boundaries"]
                self.VELOCITY_VP = model["velocity_vp"]
                self.VELOCITY_VS = model["velocity_vs"]
                self.DENSITY = model["density"]
            except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
                print(f"Failed to load velocity model: {e}. Using defaults.")

        # Validation
        if not(len(self.LAYER_BOUNDARIES) == len(self.VELOCITY_VP) == len(self.VELOCITY_VS) == len(self.DENSITY)):
            raise ValueError("LAYER_BOUNDARIES, VELOCITY_VP, VELOCITY_VS, and DENSITY must have the same length")
        if any(vp <= 0 for vp in self.VELOCITY_VP) or any(vs <= 0 for vs in self.VELOCITY_VS):
            raise ValueError("Velocities must be positive")
        if any(d <= 0 for d in self.DENSITY):
            raise ValueError("Densities must be positive")
        if self.R_PATTERN_P <= 0 or self.R_PATTERN_S <= 0:
            raise ValueError("R_PATTERN_P and R_PATTERN_S must be positive")
        if self.K_P <= 0 or self.K_S <= 0:
            raise ValueError("K_P and K_S must be positive")

@dataclass
class SpectralConfig:
    """
    Configuration for spectral fitting parameters.
    
    Attributes:
        F_MIN (float): Minimum frequency for fitting in Hz (default: 1.0).
        F_MAX (float): Maximum frequency for fitting in Hz (default: 45.0).
        OMEGA_0_RANGE_MIN (float): Minimum Omega_0 in nm/Hz (default: 0.01).
        OMEGA_0_RANGE_MAX (float): Maximum Omega_0 in nm/Hz (default: 2000.0).
        Q_RANGE_MIN (float): Minimum quality factor Q (default: 50.0).
        Q_RANGE_MAX (float): Maximum quality factor Q (default: 250.0).
        FC_RANGE_BUFFER (float): Buffer factor for corner frequency range (default: 2.0).
        DEFAULT_N_SAMPLES (int): Default number for stochastic random sampling (default: 3000).
        N_FACTOR (int): Brune model n factor for spectral decay (default: 2).
        Y_FACTOR (int): Brune model y factor for spectral decay (default: 1).
    """
    F_MIN: float = 1.0
    F_MAX: float = 45.0
    OMEGA_0_RANGE_MIN: float = 0.01
    OMEGA_0_RANGE_MAX: float = 2000.0
    Q_RANGE_MIN: float = 50.0
    Q_RANGE_MAX: float = 250.0
    FC_RANGE_BUFFER: float = 2.0
    DEFAULT_N_SAMPLES: int = 3000
    N_FACTOR: int = 2
    Y_FACTOR: int = 1


@dataclass
class PerformanceConfig:
    """
    Configuration for performance options.

    Attributes:
        USE_PARALLEL (bool): Enable parallel processing (default: False)
        LOGGING_LEVEL (str): Logging verbosity (DEBUG, INFO, WARNING, ERROR, default: INFO)

    """
    USE_PARALLEL: bool = False
    LOGGING_LEVEL: str = "INFO"


class Config:
    """
    A config class for combines magnitude, spectral, and performance configurations with loading from INI file.

    The configuration is loaded from a `config.ini` file, with fallback to defaults if the file
    or specific parameters are not found. The INI file should have the following structure:

    Example:
        ```ini
            [Magnitude]
            snr_threshold = 2.0
            pre_filter = 0.01,0.02,55,60
            velocity_model_file = "data/config/velocity_model.json"

            [Spectral]
            f_min = 0.5
            f_max = 40.0
            default_n_samples = 2000

            [Performance]
            use_parallel = true
            logging_level = "DEBUG"
        ```
    
    The `velocity_model.json` file should have the following structure:
    ```json
    {
        "layer_boundaries": [[-3.00, -1.90], [-1.90, -0.59], [-0.59, 0.22], [0.22, 2.50]],
        "velocity_vp": [2.68, 2.99, 3.95, 4.50],
        "velocity_vs": [1.60, 1.79, 2.37, 2.69],
        "density": [2700, 2700, 2700, 2700]
    }
    ```    
    """
    def __init__(self):
        self.magnitude = MagnitudeConfig()
        self.spectral = SpectralConfig()
        self.performance = PerformanceConfig()
    

    def _parse_float(self, config_section, key, fallback):
        """
        Parsing method for float values from config with validation.
        
        Args:
            config_section: ConfigParser section object to parse from.
            key (str): Key to parse.
            fallback: Fallback value if key is not found.
        
        Returns: 
            float: Parsed float value.
        
        Raises:
            ValueError: If the value cannot be parsed as a float.     
        """
        try:
            value = config_section.getfloat(key, fallback=fallback)
            return value
        except ValueError as e:
            raise ValueError(f"Invalid float for {key} in config.ini: {e}")
    

    def _parse_int(self, config_section, key, fallback):
        """
        Parsing method for int values from config with validation.
        
        Args:
            config_section: ConfigParser section object to parse from.
            key (str): key to parse.
            fallback: Fallback value if key is not found.
        
        Returns:
            int: Parsed integer value.
        
        Raises:
            ValueError: If the value cannot be parsed as an integer.
        """
        try:
            value = config_section.getint(key, fallback=fallback)
            return value
        except ValueError as e:
            raise ValueError(f"Invalid int for {key} in config.ini: {e}")
    

    def _parse_list(self, config_section, key, fallback, delimiter=","):
        """
        Parsing method for list values from config with validation.
        
        Args:
            config_section: ConfigParser section object to parse from.
            key (str): Key to Parse.
            fallback: Fallback value if key is not found.
            delimiter (str): Delimiter to split the string (default: ",").
        
        Returns:
            List[float]: List of parsed float values.
        
        Raises:
            ValueError: If the value cannot be parsed as a list of floats.
        """
        try:
            return [float(x) for x in config_section.get(key, fallback=fallback).split(delimiter)]
        except ValueError as e:
            raise ValueError(f"Invalid format for {key} in config.ini: {e}")


    def load_from_file(self, config_file: str = None) -> None:
        """
        Load configuration from an INI file, with fallback to defaults.
        
        Args:
            config_file (str, optional): Path to configuration file.
            Defaults to 'config.ini' in parent directory.
        
        Raises:
            FileNotFoundError: If the configuration file is not found or unreadable.
            ValueError: If configuration parameters are invalid.       
        """
        config  = ConfigParser()
        if config_file is None:
            # Load the default config.ini from package default data
            with _package_file("config.ini") as default_config_path:
                if not config.read(default_config_path):
                    raise FileNotFoundError(f"Default configuration file {default_config_path} not found in package")
        else:
            config_file = Path(config_file)
            if not config.read(config_file):
                raise FileNotFoundError(f"Configuration file {config_file} not  found or unreadable")
            
        # Load magnitude config section
        if "Magnitude" in config:
            mag_section = config["Magnitude"]
            snr_threshold = self._parse_float(mag_section, "snr_threshold", self.magnitude.SNR_THRESHOLD)
            if snr_threshold <= 0:
                raise ValueError("snr_threshold must be positive")
            water_level = self._parse_int(mag_section, "water_level", self.magnitude.WATER_LEVEL)
            if water_level <=0:
                raise ValueError("water_level must be positive, otherwise mathematically meaningless")
            pre_filter = self._parse_list(mag_section, "pre_filter", "0.01,0.02,55,60")
            if len(pre_filter) != 4 or any(f <=0 for f in pre_filter):
                raise ValueError("pre_filter must be four positive frequencies (f1, f2, f3, f4)")
            post_filter_f_min = self._parse_float(mag_section, "post_filter_f_min", self.magnitude.POST_FILTER_F_MIN)
            if post_filter_f_min <= 0:
                raise ValueError("post_filter_f_min must be positive")
            post_filter_f_max = self._parse_float(mag_section, "post_filter_f_max", self.magnitude.POST_FILTER_F_MAX)
            if post_filter_f_max <= post_filter_f_min:
                raise ValueError("post_filter_f_max must be greater than post_filter_f_min")
            padding_before_arrival = self._parse_float(mag_section, "padding_before_arrival", self.magnitude.PADDING_BEFORE_ARRIVAL)
            if padding_before_arrival < 0:
                raise ValueError("padding_before_arrival must be non-negative")
            noise_duration = self._parse_float(mag_section, "noise_duration", self.magnitude.NOISE_DURATION)
            if noise_duration <= 0:
                raise ValueError("noise_duration must be positive")
            noise_padding = self._parse_float(mag_section, "noise_padding", self.magnitude.NOISE_PADDING)
            if noise_padding < 0:
                raise ValueError("noise_padding must be non-negative")
            r_pattern_p = self._parse_float(mag_section, "r_pattern_p", self.magnitude.R_PATTERN_P)
            r_pattern_s = self._parse_float(mag_section, "r_pattern_s", self.magnitude.R_PATTERN_S)
            free_surface_factor = self._parse_float(mag_section, "free_surface_factor", self.magnitude.FREE_SURFACE_FACTOR)
            if free_surface_factor <= 0:
                raise ValueError("free_surface_factor must be positive")
            k_p = self._parse_float(mag_section, "k_p", self.magnitude.K_P)
            k_s = self._parse_float(mag_section, "k_s", self.magnitude.K_S)
            taup_model = mag_section.get("taup_model", fallback=self.magnitude.TAUP_MODEL)
            velocity_model_file = mag_section.get("velocity_model_file", fallback=self.magnitude.VELOCITY_MODEL_FILE)
            mw_constant = mag_section.get("mw_constant", fallback=self.magnitude.MW_CONSTANT)

            # Reconstruct MagnitudeConfig to trigger __post_init__
            self.magnitude = MagnitudeConfig(
                SNR_THRESHOLD=snr_threshold,
                WATER_LEVEL=water_level,
                PRE_FILTER=pre_filter,
                POST_FILTER_F_MIN=post_filter_f_min,
                POST_FILTER_F_MAX=post_filter_f_max,
                PADDING_BEFORE_ARRIVAL=padding_before_arrival,
                NOISE_DURATION=noise_duration,
                NOISE_PADDING=noise_padding,
                R_PATTERN_P=r_pattern_p,
                R_PATTERN_S=r_pattern_s,
                FREE_SURFACE_FACTOR=free_surface_factor,
                K_P=k_p,
                K_S=k_s,
                TAUP_MODEL=taup_model,
                VELOCITY_MODEL_FILE=velocity_model_file,
                MW_CONSTANT=mw_constant
            )

            # Validate TAUP_MODEL
            from obspy.taup import TauPyModel
            try:
                TauPyModel(model=self.magnitude.TAUP_MODEL)
            except Exception as e:
                raise ValueError(f"Invalid taup_model '{self.magnitude.TAUP_MODEL}': {e}")

        # Load spectral config section
        if "Spectral" in config:
            spec_section = config["Spectral"]
            self.spectral.F_MIN = self._parse_float(spec_section, "f_min", self.spectral.F_MIN)
            if self.spectral.F_MIN <= 0:
                raise ValueError("f_min must be positive")
            self.spectral.F_MAX = self._parse_float(spec_section, "f_max", self.spectral.F_MAX)
            if self.spectral.F_MAX < self.spectral.F_MIN:
                raise ValueError("f_max must be greater than f_min")
            self.spectral.OMEGA_0_RANGE_MIN = self._parse_float(spec_section, "omega_0_range_min", self.spectral.OMEGA_0_RANGE_MIN)
            if self.spectral.OMEGA_0_RANGE_MIN <= 0:
                raise ValueError("omega_0_range_min must be positive")
            self.spectral.OMEGA_0_RANGE_MAX = self._parse_float(spec_section, "omega_0_range_max", self.spectral.OMEGA_0_RANGE_MAX)
            if self.spectral.OMEGA_0_RANGE_MAX <= self.spectral.OMEGA_0_RANGE_MIN:
                raise ValueError("omega_0_range_max must be greater than omega_0_range_min")
            self.spectral.Q_RANGE_MIN = self._parse_float(spec_section, "q_range_min", self.spectral.Q_RANGE_MIN)
            if self.spectral.Q_RANGE_MIN <= 0:
                raise ValueError("q_range_min must be positive")
            self.spectral.Q_RANGE_MAX = self._parse_float(spec_section, "q_range_max", self.spectral.Q_RANGE_MAX)
            if self.spectral.Q_RANGE_MAX <= self.spectral.Q_RANGE_MIN:
                raise ValueError("q_range_max must be greater than q_range_min")
            self.spectral.FC_RANGE_BUFFER = self._parse_float(spec_section, "fc_range_buffer", self.spectral.FC_RANGE_BUFFER)
            if self.spectral.FC_RANGE_BUFFER <= 0:
                raise ValueError("fc_range_buffer must be positive")
            self.spectral.DEFAULT_N_SAMPLES = self._parse_int(spec_section, "default_n_samples", self.spectral.DEFAULT_N_SAMPLES)
            if self.spectral.DEFAULT_N_SAMPLES <= 0:
                raise ValueError("default_n_samples must be positive")
            self.spectral.N_FACTOR = self._parse_int(spec_section, "n_factor", self.spectral.N_FACTOR)
            self.spectral.Y_FACTOR = self._parse_int(spec_section, "y_factor", self.spectral.Y_FACTOR)
        
        # Load performance config section
        if "Performance" in config:
            perf_section = config["Performance"]
            self.performance.USE_PARALLEL = perf_section.getboolean("use_parallel", fallback=self.performance.USE_PARALLEL)
            self.performance.LOGGING_LEVEL = perf_section.get("logging_level", fallback=self.performance.LOGGING_LEVEL)
            valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR"]
            if self.performance.LOGGING_LEVEL not in valid_levels:
                raise ValueError(f"logging_level must be one of: {valid_levels}")
    
    def reload(self, config_file: str = None) -> None:
        """
        Reload configuration from INI file, resetting to defaults first.

        Args:
            config_file (str, optional): Path to the configuration file.
        """
        self.__init__()
        self.load_from_file(config_file)

# Singleton instance for easy access
CONFIG = Config()
CONFIG.load_from_file()
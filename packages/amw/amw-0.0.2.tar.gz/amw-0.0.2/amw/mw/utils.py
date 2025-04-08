"""
Utils for spectral magnitude estimation of close events
-------------------------------------------------------

..
    :copyright:
        Jan Wiszniowski (jwisz@igf.edu.pl)
    :license:
        GNU Lesser General Public License, Version 3
        (https://www.gnu.org/copyleft/lesser.html)
    :version 0.0.1:
        2024-11-07

"""

from obspy.signal.invsim import cosine_taper
from obspy.core.event.origin import Pick
import numpy as np
import string
from math import ceil, log2, sqrt
from amw.core.utils import get_hypocentral_distance, get_units
from amw.mw.source_models import BoatwrightSourceModel
from amw.mw.MinimizeInGrid import grid_search

class SpectralMwException(Exception):
    """
    The spectral magnitude estimation exception class
    """
    def __init__(self, message="other"):
        self.message = "mw estimation error: " + message
        super().__init__(self.message)


class DefaultParameters(object):
    """
    The class to read optionally the named configuration parameters from the list or general configuration.
    It is dedicated to station parameters or defined for any station.

    :param parameters: The key of parameters list
    :type parameters: str
    :param name: The name of the parameters group in the list
    :type name: str
    :param configuration: The configuration container including the parameters list
    :type configuration: dict
    """

    def __init__(self, parameters, name, configuration):
        """

        :param parameters: The key of parameters list
        :type parameters: str
        :param name: The name of the parameters group in the list. The station name
        :type name: str
        :param configuration: The configuration container including the parameters list
        :type configuration: dict

        """
        self.this_parameter = configuration[parameters].get(name)
        self.default_parameter = configuration[parameters].get('any')
        if not self.this_parameter:
            self.this_parameter = self.default_parameter
        if not self.default_parameter:
            self.default_parameter = self.this_parameter

    def __call__(self, parameter_key, default_value=None):
        """
        Get the station parameters if the parameter_key key exist for the station.
        If not get the parameter key from the configuration named 'any',
        otherwise return the default value.

        :param parameter_key: The key of the parameter_key in the station configuration
        :type parameter_key: str
        :param default_value:
            Default value of the parameter_key
            if the key do not exit both in station and default configuration
            (optional, default None)
        :type default_value: parameter_key dependent

        :return: The parameter_key value
        :rtype: parameter_key dependent

        """
        if not self.default_parameter:
            return default_value
        if parameter_key in self.this_parameter:
            return self.this_parameter[parameter_key]
        return self.default_parameter.get(parameter_key, default_value)


class DefaultSubParameters(object):
    """
    The class to read optionally the named subconfiguration parameters from the DefaultParameters object.
    It is dedicated to phase configuration defined for station configuration.

    :param parameters: The key of parameters list
    :type parameters: str
    :param name: The name of the parameters group in the list. The phase name
    :type name: str
    :param main_config: The configuration object with the default option
    :type main_config: DefaultParameters

    """
    def __init__(self, parameters, name, main_config):
        """

        :param parameters: The key of parameters list
        :type parameters: str
        :param name: The name of the parameters group in the list. The phase name
        :type name: str
        :param main_config: The configuration object with the default option
        :type main_config: DefaultParameters
        """
        if parameters in main_config.this_parameter:
            self.this_parameter = DefaultParameters(parameters, name, main_config.this_parameter)
        if parameters in main_config.default_parameter:
            self.default_parameter = DefaultParameters(parameters, name, main_config.default_parameter)

    def __call__(self, parameter_key, default_value=None):
        """
        It gets the phase parameters if the parameter_key key exist for the phase.
        Otherwise, it gets the parameter key from the phase configuration named 'any'.
        Otherwise, it tries to get the parameter from the phase configuration in 'any' station.
        If it can't find the key anywhere, it returns the default value.

        :param parameter_key: The key of the parameter_key in the station configuration
        :type parameter_key: str
        :param default_value:
            Default value of the parameter_key
            if the key do not exit both in station and default configuration
            (optional, default None)
        :type default_value: parameter_key dependent

        :return: The parameter_key value
        :rtype: parameter_key dependent

        """
        value = self.this_parameter(parameter_key)
        if value is None:
            value = self.default_parameter(parameter_key, default_value)
        return value


def get_phase_window(pick_name, picks, origin, station_inventory, station_parameters):
    """
    If phase configuration include the window configuration, the window time is computed according the formula

    .. math::
            T = r^{b_1} / 10^{b_2},

    where :math:`b_1` and :math:`b_2` are defined parameters
    If not the window is computed

    .. math::
        T^{(P)} = 0.9(T_S-T_P)

        T^{(S)} = 1.8(T_S-T_P)

    The S phase window con not be shorter than the defined minimum value
     and the P windows cannot be longer than :math:`T_S-T_P`

    :param pick_name: 'P', 'S'. In case of P+S window use 'S'
    :param picks: list of picks of the event
    :param origin: The origin of the event
    :type origin: ObsPy.Origin
    :param station_inventory:
        The inventory of the station that the signal was picked on
    :type station_inventory: ObsPy.Inventory
    :param station_parameters: Configuration of the station with any station option
    :type station_parameters: DefaultParameters

    :return: Thw window for the spectrum calculation period
    :rtype: float

    """
    phase_config = DefaultSubParameters('phase_parameters', pick_name, station_parameters)
    window_par = phase_config('window')
    min_window = phase_config('length', 2.0)
    ps_relative = phase_config('P-S', 0.8)
    if len(picks) == 2:
        if picks[0] is not None and picks[1] is not None:
            max_p_window = picks[1].time - picks[0].time
        elif pick_name == 'P':
            max_p_window = get_theoretical_s(picks[0], origin).time - picks[0].time
        else:
            max_p_window = picks[1].time - get_theoretical_p(picks[1], origin).time
    elif pick_name == 'P':
        max_p_window = get_theoretical_s(picks[0], origin).time - picks[0].time
    else:
        max_p_window = picks[0].time - get_theoretical_p(picks[0], origin).time
    if window_par:
        b1 = window_par['b1']
        b2 = window_par['b2']
        r, _ = get_hypocentral_distance(origin, station_inventory)
        window_length = r ** b1 / 10.0 ** b2
        if pick_name == 'P':
            return min(max(window_length, min_window), max_p_window)
        else:
            return max(window_length, min_window)
    if pick_name == 'P':
        return max_p_window * ps_relative
    else:
        return max(max_p_window * ps_relative * 2.0, min_window)


def get_spectrum(stream, configuration):
    """
    Calculate the single station spectrum of seismic signal.
    It can be single phase spectrum oo multiphase spectrum.

    :param stream: The 3D stream with the one station seismic signal, the spectrum is calculated.
    :type stream: ObsPy.Stream
    :param configuration: The configuration container of all parameters dictionary required for the program to work.
    :type configuration: dict
    :return: The signal spectrum  and frequencies of the spectrum
    :rtype: tuple(numpy.array(float), numpy.array(float))
    """
    spec = None
    freq = None
    for trace in stream:
        delta = trace.stats.delta
        s, f = spectrum1(trace.data, delta, configuration, True)
        units = get_units(trace)
        if units == 'm/s' or units == 'counts':
            s, f = spectrum1(trace.data, delta, configuration, True)
        elif units == 'm':
            s, f = spectrum1(trace.data, delta, configuration, False)
        else:
            raise SpectralMwException(f"Wrong signal units '{units}'")
        if spec is None:
            spec = np.square(s)
            freq = f
        else:
            spec = np.add(spec, np.square(s))
    return np.sqrt(spec), freq


def next_power_of_2(x):
    """
    It returns the power of two value greater or equal to x

    :param x: The number of signal samples
    :type x: int

    :return: The power of two value greater than the number of signal samples
    :rtype x: int

    """
    return 1 if x == 0 else 2 ** ceil(log2(x))


def spectrum1(samples, dt, configuration, integration):
    r"""
    The spectrum for one trace signal is calculated. Signal is tapered and the spectrum
    is scaled to fulfil the Parseval's theorem

    ..math:
        \int_{-\infty }^{-\infty}\left| x\left ( t \right )\right|^2dt=
        \int_{-\infty }^{-\infty}\left| X\left ( f \right )\right|^2df

    :param samples: Array of samples
    :type samples: numpy.array(float)
    :param dt: sampling period
    :type dt: float
    :param configuration: The configuration container of all parameters dictionary required for the program to work.
    :type configuration: dict
    :param integration: Information whether integrate the signal in frequency domain
    :type integration: bool

    :return: Spectrum values and spectrum frequencies.
    """
    samples_without_offset = samples - np.mean(samples)
    xw = apply_tapper(samples_without_offset, configuration)
    nf = next_power_of_2(len(xw))
    s = np.fft.rfft(xw, nf)
    # ns = len(s) // 2 + 1
    ns = len(s)
    spec = np.absolute(s[1:ns])
    df = 1.0 / nf / dt
    frequencies = np.array([df * f for f in range(1, ns)])
    # correction = sqrt(2.0*np.square(samples_without_offset).sum() * dt / np.square(np.abs(s)).sum() / df)
    # spec = np.divide(spec, frequencies)
    # spec *= correction / 2.0 / pi
    correction = sqrt(np.square(samples_without_offset).sum() * dt / np.square(spec).sum() / df)
    spec *= correction
    if integration:
        spec = np.divide(spec, 2.0 * np.pi * frequencies)
    return spec, frequencies


def noise_spectrum2(samples, window_size, delta, configuration, integration):

    """
    Compute noise spectra in as many as possible windows of the same size as signal window
    for the single component of the waveform

    :param samples: Array of samples
    :type samples: numpy.array(float)
    :param window_size: The window size in samples
    :type window_size:
    :param delta: Sampling period
    :type delta: float
    :param configuration: The configuration container of all parameters dictionary required for the program to work.
    :type configuration: dict
    :param integration: Information whether integrate the signal in frequency domain
    :type integration: bool

    :return: The square of mean noise,  noise variation, and number of noise windows
    :rtype: tuple(numpy.array(float), numpy.array(float), int)

    """
    noise_list = list()
    freq_size = 0
    for idx in range(0, samples.size - window_size + 1, window_size):
        tn, _ = spectrum1(samples[idx:idx + window_size], delta, configuration, integration)
        freq_size = len(tn)
        noise_list.append(tn)
    no_windows = len(noise_list)
    # ----------------------------------------------
    # Removing the highest noise spectrum values
    # Protect against the disturbance or other picks
    if no_windows > 1:
        for idx in range(freq_size):
            max_noise = -1.0
            noise_kdx = -1
            for kdx in range(no_windows):
                tn = noise_list[kdx]
                if tn[idx] > max_noise:
                    max_noise = tn[idx]
                    noise_kdx = kdx
            noise_list[noise_kdx][idx] = 0.0
        no_windows -= 1
    # ----------------------------------------------
    # Compute the mean and standard deviation of noise values
    noise_mean = np.zeros(freq_size)
    noise_std = np.zeros(freq_size)
    for tn in noise_list:
        noise_mean = np.add(noise_mean, tn)
        noise_std = np.add(noise_std, np.square(tn))
    noise_mean2 = np.square(np.divide(noise_mean, no_windows))
    if no_windows > 1:
        noise_std2 = np.divide(np.subtract(noise_std, noise_mean2 * no_windows), no_windows - 1)
    else:
        noise_std2 = np.zeros(len(noise_std))
    return noise_mean2, noise_std2, no_windows


def get_noise_spectrum(stream, window_size, configuration):
    """
    Compute 3D mean noise spectra and 3D standard deviation of noise spectra
    of as many as possible windows of the same size as signal window
    for the single component of the waveform

    :param stream: The 3D stream with the one station seismic signal, the spectrum is calculated.
    :type stream: ObsPy.Stream
    :param window_size: The window size in samples
    :type window_size:
    :param configuration: The configuration container of all parameters dictionary required for the program to work.
    :type configuration: dict

    :return: The 3D mean noise,  3D noise variation, and number of noise windows
    :rtype: tuple(numpy.array(float), numpy.array(float))

    """
    noise_mean = None
    noise_std = None
    no_windows = 0.0
    for trace in stream:
        delta = trace.stats.delta
        n_mean2, n_std2, no_windows = noise_spectrum2(trace.data, window_size, delta, configuration, True)
        units = get_units(trace)
        if units == 'm/s' or units == 'counts':
            n_mean2, n_std2, no_windows = noise_spectrum2(trace.data, window_size, delta, configuration, True)
        elif units == 'm':
            n_mean2, n_std2, no_windows = noise_spectrum2(trace.data, window_size, delta, configuration, False)
        else:
            raise SpectralMwException(f"Wrong signal units '{units}'")
        if noise_mean is None:
            noise_std = n_std2
            noise_mean = n_mean2
        else:
            noise_std = np.add(noise_std, n_std2)
            noise_mean = np.add(noise_mean, n_mean2)
    return np.sqrt(noise_mean), np.sqrt(noise_std), no_windows


def get_simple_taper(signal, configuration):
    """
    Get the signal taper. This procedure is rather for the taper visualisation.
    For computation use rather apply taper

    :param signal: The signal
    :type signal: numpy.array
    :param configuration: The configuration container of all parameters dictionary required for the program to work.
    :type configuration: dict

    :return: The taper
    :rtype: numpy.array(float)

    """
    if 'taper' not in configuration:
        return np.ones(len(signal))
    taper_config = configuration['taper']
    if taper_config['type'] == 'cosine_taper':
        p = taper_config.get('percentage', 10.0) / 100.0
        half_cosine = taper_config.get('half_cosine', True)
        tapper = cosine_taper(len(signal), p=p, halfcosine=half_cosine)
        return tapper
    raise SpectralMwException('Undefined taper type')


def apply_tapper(signal, configuration):
    """
    :param signal: The signal
    :type signal: numpy.array(float)
    :param configuration: The configuration container of all parameters dictionary required for the program to work.
    :type configuration: dict

    :return: The signal multiplied by taper
    :rtype: numpy.array(float)

    """
    if 'taper' not in configuration:
        return signal
    taper_config = configuration['taper']
    if taper_config['type'] == 'cosine_taper':
        p = taper_config.get('percentage', 10.0) / 100.0
        half_cosine = taper_config.get('half_cosine', True)
        tapper = cosine_taper(len(signal), p=p, halfcosine=half_cosine)
        return np.multiply(tapper, signal)
    raise 'Undefined taper type'


def get_margin(window, configuration):
    """
    Gets the margins over the signal window
    :param window: The window size
    :type window: int/float
    :param configuration: The configuration container of all parameters dictionary required for the program to work.
    :type configuration: dict

    :return: The margins length
    :rtype: float

    """
    if 'taper' not in configuration:
        return 0.0
    taper_config = configuration['taper']
    if taper_config['type'] == 'cosine_taper':
        return taper_config.get('percentage', 10.0) * window / 100.0
    raise 'Undefined taper type'


def get_theoretical_s(pick_p, origin):
    r"""
    Calculate the theoretical S pick time according to:

    .. math::
        t_S=t_0 + \sqrt{3}\left( t_P - t_0 \righ)

    where :math:`t_0` is the origin time and :math:`t_P` is the pick P.

    :param pick_p: The P wave pick.
    :type pick_p: ObsPy.Pick
    :param origin: The origin parameter_key. Only origin time is required.
    :type origin: ObsPy.Origin

    :return: The theoretical S pick
    :rtype: ObsPy.Pick

    """
    return Pick(time=origin.time + sqrt(3.0) * (pick_p.time - origin.time),
                waveform_id=pick_p.waveform_id, phase_hint='S', comment=['Artificial S phase for mw estimation'])


def get_theoretical_p(pick_s, origin, offset=None):
    r"""
    Calculate the theoretical S pick time according to:

    .. math::
        t_P=t_0 + \left( t_S - t_0 \righ) / \sqrt{3}

    where :math:`t_0` is the origin time and :math:`t_S` is the pick S.
    The returning pick time is modified by the offset,
    which is the parameter_key offset multiplied by the :math:`t_S-t_P` difference.
    The offset is used when we need to point to the noise's end and ensure the noise's end is before the P wave onset.

    :param pick_s: The S wave pick.
    :type pick_s: ObsPy.Pick
    :param origin: The origin parameter_key. Only origin time is required.
    :type origin: ObsPy.Origin
    :param offset: The offset as a part of S-P picks time difference (optional)
    :type offset: float

    :return: The theoretical P pick optionally modified bey the offset.
    :rtype: ObsPy.Pick

    """
    pick_p = Pick(time=origin.time + (pick_s.time - origin.time) / sqrt(3.0),
                  waveform_id=pick_s.waveform_id, phase_hint='P', comment=['Artificial S phase for mw estimation'])
    if offset is not None:
        pick_p.time += (pick_s.time - pick_p.time) * offset
    return pick_p


class SourceParameters:
    """
    The class SourceParameters. The derived from this class object contains the origin reference,
    and method *fault_v()* and *rho()*, which return the wave velocity and density at the source.

    :param origin: The origin of the event
    :type origin: ObsPy.Origin
    :param configuration: The configuration container of all parameters dictionary required for the program to work.
    :type configuration: dict

    """
    def __init__(self, origin, configuration):
        """

        :param origin: The origin informations of the event
        :type origin: ObsPy.Origin
        :param configuration: The configuration container of all parameters dictionary required for the program to work.
        :type configuration: dict

        """
        self.origin = origin
        self.default_vs = configuration['default_vs']
        self.default_vp = configuration['default_vp']
        self.default_rho = configuration['default_rho']
        pass

    def fault_v(self, wave_name):
        """
        Return the wave velocity at the source

        :param wave_name: The wave name. Usually 'P' and 'S' wave names are used.
        :type wave_name: str
        :return: The wave velocity [m/s]
        :rtype: float
        """
        if wave_name == 'P':
            return self.default_vp
        else:
            return self.default_vs

    def rho(self):
        """
        Return the density at the source

        :return: The density [kg/m^3]
        :rtype: float
        """
        return self.default_rho


def get_source_par(origin, configuration):
    """
    Create the SourceParameters object based on configutatin

    :param origin: The origin of the event
    :type origin: ObsPy.Origin
    :param configuration: The configuration container of all parameters dictionary required for the program to work.
    :type configuration: dict

    :return: A source parameters object
    :rtype: SourceParameters
    """
    velocity_model = configuration.get('velocity_model', 'constant')
    if velocity_model == 'constant':
        return SourceParameters(origin, configuration)
    else:
        raise 'Velocity model {} not implemented'.format(configuration['velocity_model'])


def method_id(configuration):
    """
    Defines the QuakeML magnitude method id for describing the StationMagnitude object
    containing computed in this program moment magnitude
    The id contain the information of metric and whether single or multiple phase mw is estimated.

    :param configuration: The configuration container of all parameters dictionary required for the program to work.
    :type configuration: dict

    :return: Return the method id
    :rtype: str

    """
    if configuration['method'] != 'separate_phases':
        return f"smi:igf.edu.pl/spectral_Mw_{configuration.get('metric','p_norm')}"
    return f"smi:igf.edu.pl/spectral_Mw_PS_{configuration.get('metric','p_norm')}"


def method_id_ph(phase_name, configuration):
    """

    :param phase_name: The phase name
    :type phase_name: str
    :param configuration: The configuration container of all parameters dictionary required for the program to work.
    :type configuration: dict

    :return: Return the method id
    :rtype: str

    """
    return '{}_{}'.format(method_id(configuration), phase_name)


def get_minimization_method(configuration):
    """
    Get the optimization function

    :param configuration: The configuration container of all parameters dictionary required for the program to work.
    :type configuration: dict

    :return: The minimization function
    :rtype: func

    """
    module_name = configuration.get('module')
    if module_name is None:
        return grid_search
    module = __import__(module_name)
    return getattr(module, configuration.get('method', 'minimize'))


def get_source_model(frequencies, configuration):
    """
    Get the source model object based on configuration
    :param frequencies: The list of frequencies the source model values will be calculated
    :type frequencies: numpy.array(float)
    :param configuration: The configuration container of all parameters dictionary required for the program to work.
    :type configuration: dict

    :return: The source model object
    :rtype: e.g. BoatwrightSourceModel

    """
    source_model_name = configuration.get('source_model', 'Brune')
    if source_model_name == 'Brune':
        return BoatwrightSourceModel(frequencies)
    if source_model_name == 'Boatwright':
        gamma = configuration.get('Boatwright gamma', 1.0)
        n = configuration.get('Boatwright n', 2.0)
        return BoatwrightSourceModel(frequencies, gamma=gamma, n=n)
    raise Exception(f'Source model {source_model_name} has not been implemented')


def format_filename(s):
    """
    """
    valid_chars = f'-_.() {string.ascii_letters}{string.digits}'
    filename = ''
    for c in s:
        if c in valid_chars:
            filename += c
        else:
            filename += '_'
    # filename = ''.join(c for c in s if c in valid_chars)
    filename = filename.replace(' ', '_')
    filename = filename.replace('..', '_')
    return filename

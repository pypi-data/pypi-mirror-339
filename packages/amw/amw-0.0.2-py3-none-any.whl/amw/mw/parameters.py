"""
Functions and classes for preparation of mw estimation procedure parameters
---------------------------------------------------------------------------

..
    :copyright:
        Jan Wiszniowski (jwisz@igf.edu.pl)
    :license:
        GNU Lesser General Public License, Version 3
        (https://www.gnu.org/copyleft/lesser.html)
    :version 0.0.1:
        2024-11-07

"""

from amw.mw.utils import DefaultParameters, DefaultSubParameters, get_source_model
from amw.mw.utils import get_hypocentral_distance
import numpy as np
import obspy.geodetics.base as geo


def get_travel_time(pick, source_parameters, station_inventory, use_arrivals=False):
    """
    Calculate the travel time of the picket wave from the source to the station,
    hipocentral distance to the station, and phase velocity at the fault

    :param use_arrivals: Option whether to get travel time from origin arrivals.
        If it is false thr travel time is computed from source and station coordinates.
    :type use_arrivals: bool
    :param pick: The pick of the wave that the travel time is assessed
    :type pick: ObsPy Pick
    :param source_parameters: The seismic source parameters required for of mw estimation procedure
    :type source_parameters: SourceParameters
    :param station_inventory:
        The inventory of the station that the signal was picked and mw is estimated
    :type station_inventory: ObsPy Inventory

    :return: The phase travel time [s], hipocentral distance [m], phase velocity at the fault [m/s].
    :rtype: tuple(float, float, float)

    """
    phase_name = pick.phase_hint[0:1]
    origin = source_parameters.origin
    travel_time = None
    r = None
    fault_v = source_parameters.fault_v(phase_name)
    if use_arrivals:
        for arrival in source_parameters.origin.arrivals:
            if arrival.phase == pick.phase_hint:
                if pick.resource_id == arrival.pick_id:
                    if arrival.time_residual:
                        travel_time = pick.time - origin.time - arrival.time_residual
                    if arrival.distance:
                        delta = arrival.distance
                        distance = geo.degrees2kilometers(delta) * 1000.0
                        r = np.sqrt(distance ** 2 + (origin.depth) ** 2)
                    break
    if not r:
        r, delta = get_hypocentral_distance(origin, station_inventory)
    if not travel_time:
        travel_time = pick.time - origin.time
    return travel_time, r, fault_v


def get_far_response(travel_time, rho, r, fault_v, omega):
    r"""
    The get_far_response function calculates the Green function in the far field :math:`G^{\left(c\right)far}`
    except the internal dumping and surface effect for phase P or S marked as :math:`\left(c\right)` according to:

    .. math::

        G^{\left(c\right)far}=\frac{\omega \exp\left(-\omega T_c\right)}{4\pi\rho rv_c^3},

    where
    :math:`c` is the wave name (P or S),
    :math:`\omega` is the circular frequency, :math:`\omega = 2j\pi f`,
    :math:`r` is the hypocentral distance,
    :math:`T_c` is the phase travel time,
    :math:`v_c` is the phase velocity at the source,
    :math:`\rho` is the density at the source.

    :param travel_time: The phase travel time
    :type travel_time: float
    :param rho: The density at the source [kg/m^3]
    :type rho: float
    :param r: The hipocentral distance [m]
    :type r: float
    :param fault_v: The phase velocity at the source [m/s]
    :param fault_v: float
    :param omega: The circular frequencies, for which the response is counted. :math:`\omega = 2j\pi f`
    :type omega: numpy.array(complex)

    :return: The far field part Green one phase function
    :rtype: numpy.array(complex)

    """
    far_response = np.exp(-omega * travel_time)
    far_response /= 4.0 * np.pi * rho * r * fault_v ** 3
    far_response = np.multiply(far_response, omega)
    return far_response


def get_intermediate_response(travel_time, rho, r, fault_v, omega):
    r"""
    The get_intermediate_response function calculates the radial or transversal component of Green function
    for phase P or S in the intermediate field :math:`G_x^{\left(c\right)inter}`
    except the internal dumping and surface effect for phase P or S marked as :math:`\left(c\right)` according to:

    .. math::

        G_x^{\left(c\right)inter}=\frac{exp\left(-\omega T_c\right)}{4\pi\rho r^2 v_c^2},

    where
    :math:`c` is the wave name (P or S),
    :math:`\omega` is the circular frequency, :math:`\omega = 2j\pi f`,
    :math:`r` is the hipocentral distance,
    :math:`T_c` is the phase travel time,
    :math:`v_c` is the phase velocity at the source,
    :math:`\rho` is the density at the source
    :math:`x` describes the signal component (radial or transversal).

    :param travel_time: The phase travel time
    :type travel_time: float
    :param rho: The density at the source [kg/m^3]
    :type rho: float
    :param r: The hipocentral distance [m]
    :type r: float
    :param fault_v: The phase velocity at the source [m/s]
    :type fault_v: float
    :param omega: The circular frequencies, for which the response is counted. :math:`\omega = 2j\pi f`
    :type omega: numpy.array(complex)

    :return: The intermediate field part Green function of one phase
    :rtype: numpy array(complex)

    """
    intermediate_response = np.exp(-omega * travel_time)
    intermediate_response /= 4.0 * np.pi * rho * r ** 2 * fault_v ** 2
    return intermediate_response


def get_near_response(picks, source_parameters, station_inventory, omega):
    r"""
    The get_near_response function calculates the common (radial and) transversal component of Green function
    in the intermediate field except the internal dumping and surface according to:

    .. math::
        G^{near}=\frac{\left(\omega T_P+1\right)exp\left(-\omega T_P\right)
        -\left(\omega T_S+1\right)exp\left(-\omega T_S\right)}{4\pi\omega ^2\rho r^4}

    where :math:`\omega` is the circular frequency, :math:`\omega = 2j\pi f`, :math:`r` is the hipocentral distance,
    :math:`T_P` is the P phase travel time, :math:`T_S` is the P phase travel time, :math:`\rho` is the density
    at the source

    :param picks:
        A list of picks of waves in the near field.
        It must consist of two pick P or S and P must the first.
    :type picks: list(ObsPy Pick)
    :param source_parameters:
        The seismic source parameters required for of mw estimation procedure
    :type source_parameters: SourceParameters
    :param station_inventory:
        The inventory of the station that the signal was picked and mw is estimated
    :type station_inventory: ObsPy Inventory
    :param omega: The circular frequencies, for which the response is counted. :math:`\omega = 2j\pi f`
    :type omega: numpy.array(complex)

    :return: The near field part Green function
    :rtype: numpy.array(complex)

    """
    travel_time_p, r, _ = get_travel_time(picks[0], source_parameters, station_inventory)
    travel_time_s, _, _ = get_travel_time(picks[1], source_parameters, station_inventory)
    rho = source_parameters.rho()
    element_p = np.multiply(omega * travel_time_p + 1.0, np.exp(-omega * travel_time_p))
    element_s = np.multiply(omega * travel_time_s + 1.0, np.exp(-omega * travel_time_s))
    near_response = np.divide(element_p - element_s, 4.0 * np.pi * rho * r ** 4 * np.square(omega))
    return near_response


def get_correction(phase_name, station_parameters, frequencies, travel_time):
    """
    Calculate the internal dumping, near surface amplification and frequency dumping in frequency domain

    :param phase_name: The name of the phase ('P or 'S'). In the case of 'P' the internal dumping, etc. are calculating
        for radial component of the signal, which is the P wave in far field. In the case of 'S' the internal dumping,
        etc. is calculating for transversal component of the signal, which is the S wave in far field.
    :type phase_name: str
    :param station_parameters: The station parameter
    :type station_parameters: DefaultParameters
    :param frequencies: Frequencies for which the correction is calculated
    :type frequencies: numpy.array(float)
    :param travel_time: The signal travel time
    :type travel_time: float

    :return: The correction in frequency domain
    :rtype: numpy.array(float)

    """
    phase_parameters = DefaultSubParameters('phase_parameters', phase_name, station_parameters)
    q_0 = phase_parameters('Q_0')
    q_theta = phase_parameters('Q_theta', 0.0)
    q_corner = phase_parameters('Q_corner', -1.0)
    if q_corner > 0.0:
        eval_q = q_0 * pow(1 + frequencies / q_corner, q_theta)
    else:
        eval_q = q_0 * pow(frequencies, q_theta)
    q_correction = np.exp(-np.pi * travel_time * np.divide(frequencies, eval_q))
    kappa = phase_parameters('kappa', 0.0)
    kappa_correction = np.exp(-np.pi * kappa * frequencies)
    correction = np.multiply(q_correction, kappa_correction)
    correction *= phase_parameters('surface_correction', 1.0)
    return correction


def get_phase_response(pick, source_parameters, station_inventory, station_parameters, frequencies):
    r"""
    Function get_phase_response computes radial and transversal frequency responses of the seismic phase
    at the station to the source frequency function:
    
    .. math::
        G^{\left(c\right)}\left(f\right)A^{\left(c\right)}\left(f\right)R\left(f\right)I\left(f\right),

    where :math:`\left(c\right)` is the phase name

    The response consists of:
     * Green function :math:`G^{\left(c\right)}`, which for P wave is defined as
     
    .. math::

        G_R^{\left(P\right)}\left(f\right)= G_R^{\left(P\right)far}\left(f\right)
        +G_R^{\left(P\right)inter}\left(f\right)

        G_T^{\left(P\right)}\left(f\right) = G_T^{\left(P\right)inter}\left(f\right)

    where :math:`G_R^{\left(P\right)far} = G^{\left(P\right)far}R_R^{far}`
    is the radial component of the P wave in the far field,
    :math:`G_R^{\left(P\right)inter} = G^{\left(P\right)inter}R_R^{inter}`
    is the radial component of the P wave in the intermediate field,
    and :math:`G_T^{\left(P\right)inter} = G^{\left(P\right)inter}R_T^{inter}`
    is the transversal component of the P wave in intermediate field.
    :math:`R_R^{far}= R^{(P)}` is the P wave average radiation coefficient in the far field.
    For S wave, it is defined as

    .. math::

        G_R^{(S)}\left(f\right) = G_R^{\left(S\right)inter}\left(f\right)

        G_T^{(S)}\left(f\right) = G_T^{\left(S\right)far}\left(f\right)+G_T^{\left(S\right)inter}\left(f\right)

    where :math:`G_R^{\left(S\right)inter} = G^{\left(S\right)inter}R_R^{inter}`
    is the radial component of the S wave in intermediate field,
    :math:`G_T^{\left(S\right)far} = G^{\left(S\right)far}R_T^{far}`
    is the transversal component of the S wave in the far field,
    and :math:`G_T^{\left(S\right)inter} = G^{\left(S\right)inter}R_T^{inter}`
    is the transversal component of the S wave in the intermediate field.
    :math:`R_T^{far}= R^{(S)}` is the S wave average radiation coefficient in the far field.

    Inelastic (internal) dumping :math:`A^{\left(c\right)}` is defined as
    
    .. math::
        A\left(f\right)=exp\left(\frac{-\pi T_cf}{Q^{\left(c\right)}\left(f\right)}\right),

    where

    .. math::

        Q^{\left(c\right)}\left(f\right)=Q_0^{\left(c\right)}\left(\frac{f_q+f}{f_q}\right)^\vartheta;

    or

    .. math::

        Q\left(f\right)=Q_0^{\left(c\right)}f^\vartheta;

    The near-surface losses and free surface amplification is assumed by

    .. math::

        R\left(f\right)=R_c\exp\left(-\pi \kappa f\right).

    The instrument response is :math:`I\left(f\right)`.

    :param pick: The P or S pick name
    :type pick: str
    :param source_parameters: The seismic source parameters required for of mw estimation procedure
    :type source_parameters: SourceParameters
    :param station_inventory:
        The inventory of the station that the signal was picked and mw is estimated
    :type station_inventory: ObsPy Inventory
    :param station_parameters:  The reference to the station_name (or default)
    :param frequencies: The frequencies, for which the response is counted
    :type frequencies: numpy.array(float)

    :return: Tuple of two numpy arrays of complex radial and transversal response in frequency domain.
    :rtype: tuple(numpy.array(float), numpy.array(float))

    """
    phase_name = pick.phase_hint[0:1]

    travel_time, r, fault_v = get_travel_time(pick, source_parameters, station_inventory)
    rho = source_parameters.rho()

    far_radial_average_radiation = station_parameters('far_radial_average_radiation', 0.52)
    far_transversal_average_radiation = station_parameters('far_transversal_average_radiation', 0.63)
    omega = 2.0 * np.pi * 1j * frequencies
    if phase_name == 'P':
        # Radial (P) far
        radial_response = get_far_response(travel_time, rho, r, fault_v, omega) * far_radial_average_radiation
        if station_parameters('consider_intermediate_field', False):
            intermediate_response = get_intermediate_response(travel_time, rho, r, fault_v, omega)
            # Radial (P) intermediate
            radial_response += intermediate_response * station_parameters(
                'intermediate_p_radial_average_radiation', 4.0 * far_radial_average_radiation)
            # Transversal (P) intermediate
            transversal_response = intermediate_response * station_parameters(
                'intermediate_p_transversal_average_radiation', -2.0 * far_transversal_average_radiation)
        else:
            # Transversal (P) intermediate is zero
            transversal_response = np.zeros(len(frequencies), dtype=complex)
    else:
        # Transversal (S) far
        transversal_response = get_far_response(travel_time, rho, r, fault_v, omega) * far_transversal_average_radiation
        if station_parameters('consider_intermediate_field', False):
            intermediate_response = get_intermediate_response(travel_time, rho, r, fault_v, omega)
            # Radial (S) intermediate
            radial_response = intermediate_response * station_parameters(
                'intermediate_s_radial_average_radiation', -3.0 * far_radial_average_radiation)
            # Transversal (S) intermediate
            transversal_response += intermediate_response * station_parameters(
                'intermediate_s_transversal_average_radiation', 3.0 * far_transversal_average_radiation)
        else:
            # Radial (P) intermediate is zero
            radial_response = np.zeros(len(frequencies), dtype=complex)
    radial_correction = get_correction('P', station_parameters, frequencies, travel_time)
    transversal_correction = get_correction('S', station_parameters, frequencies, travel_time)
    radial_response = np.multiply(radial_response, radial_correction)
    transversal_response = np.multiply(transversal_response, transversal_correction)
    return radial_response, transversal_response


def get_phases_response(picks, source_parameters, station_inventory, station_parameters, frequencies):
    r"""
    Function get_phases_response computes radial and transversal frequency responses
    of the cumulated seismic phases P and S at the station to the source frequency function:

    .. math::

        G_R^{(P+S)}\left(f\right)=G_R^{(P)far}\left(f\right)+G_R^{\left(P\right)inter}\left(f\right)
        +G_R^{\left(S\right)inter}\left(f\right)+G_R^{near}\left(f\right)

        G_T^{(P+S)}\left(f\right)=G_T^{\left(P\right)inter}\left(f\right)+G_T^{(S)far}\left(f\right)
        +G_T^{\left(S\right)inter}\left(f\right)+G_T^{near}\left(f\right),

    where
    :math:`G_T^{near} = G^{near}R_T^{near}`
    is the transversal component in the near field
    and :math:`G_R^{near} = G^{near}R_R^{near}`
    is the radial component in the near field.
    The remaining components are defined in the get_phase_response function.

    :param picks: List of two P and S picks
    :param source_parameters: The seismic source parameters required for of mw estimation procedure
    :type source_parameters: SourceParameters

    :param station_inventory:
        The inventory of the station that the signal was picked and mw is estimated
    :type station_inventory: ObsPy Inventory

    :param station_parameters:  The reference to the station_name (or default)
    :param frequencies: The frequencies, for which the response is counted

    :return: Tuple of two numpy arrays of complex radial and transversal response in frequency domain.
    :rtype: tuple(numpy.array(float), numpy.array(float))
    
    """

    radial_response = np.zeros(len(frequencies), dtype=complex)
    transversal_response = np.zeros(len(frequencies), dtype=complex)
    omega = 2.0 * np.pi * 1j * frequencies
    for pick in picks:
        rs, ts = get_phase_response(pick, source_parameters, station_inventory, station_parameters, frequencies)
        radial_response += rs
        transversal_response += ts
    if station_parameters('consider_near_field', False):
        resp = get_near_response(picks, source_parameters, station_inventory, omega)
        resp = np.multiply(resp, np.exp(- np.pi * station_parameters('kappa', 0.0) * frequencies))
        radial_response += resp * station_parameters(
            'near_radial_average_radiation',
            9.0 * station_parameters('far_radial_average_radiation', 0.52))
        transversal_response += resp * station_parameters(
            'near_transversal_average_radiation',
            -6.0 * station_parameters('far_transversal_average_radiation', 0.63))
    return radial_response, transversal_response


class MwFunctionParameters(object):
    """
    The class keeps all parameters used to estimate the mw and its object is used as optimised function.

    :param picks: List of two picks P and S. The P pick must be firsts .
    :type picks: list(ObsPy.Pick)
    :param station_name:
        The station name in the form required to find the configuration for the station
    :type station_name: str
    :param signal_spec: The signal spectrum
    :type signal_spec: numpy.array(float)
    :param noise_mean: The noise mean spectrum
    :type noise_mean: numpy.array(float)
    :param noise_sd: The standard deviation of noise spectrum
    :type noise_sd: numpy.array(float)
    :param freq: The frequencies that the spectra are compared
    :type freq: numpy.array(float)
    :param source_parameters: The seismic source parameters required for of mw estimation procedure
    :type source_parameters: SourceParameters
    :param station_inventory:
        The inventory of the station that the signal was picked and mw is estimated
    :type station_inventory: ObsPy Inventory
    :param configuration: The configuration container of all parameters dictionary required for the program to work.
    :type configuration: dict

    **Warning! signal_spectrum, noise_spectrum, noise_sd, frequencies must have the same size**

    """

    def __init__(self, picks, station_name, signal_spec, noise_mean, noise_sd, freq, source_parameters,
                 station_inventory, configuration):
        """
        The MwFunctionParameters constructor

        :param picks: List of two picks P and S. The P pick must be firsts .
        :type picks: list(ObsPy.Pick)
        :param station_name:
            The station name in the form required to find the configuration for the station
        :type station_name: str
        :param signal_spec: The signal spectrum
        :type signal_spec: numpy.array(float)
        :param noise_mean: The noise mean spectrum
        :type noise_mean: numpy.array(float)
        :param noise_sd: The standard deviation of noise spectrum
        :type noise_sd: numpy.array(float)
        :param freq: The frequencies that the spectra are compared
        :type freq: numpy.array(float)
        :param source_parameters: The seismic source parameters required for of mw estimation procedure
        :type source_parameters: SourceParameters
        :param station_inventory:
            The inventory of the station that the signal was picked and mw is estimated
        :type station_inventory: ObsPy Inventory
        :param configuration: The configuration container of all parameters dictionary required for the program to work.
        :type configuration: dict

        """
        self.configuration = configuration
        station_parameters = DefaultParameters('station_parameters', station_name, configuration)
        phase_parameters = DefaultSubParameters('phase_parameters', picks[0].phase_hint[0:1], station_parameters)
        self.mw_correction = station_parameters('mw_correction', 0.0)
        self.low_frequency = phase_parameters('low_frequency', 0.5)
        self.high_frequency = phase_parameters('high_frequency', 20.0)
        # -------------------------------------------------------------------------------------------------------------
        # Cutting the stream to the frequency limits
        lf = self.low_frequency
        hf = self.high_frequency
        self.signal_spectrum = np.array([s for idx, s in enumerate(signal_spec) if lf <= freq[idx] <= hf])
        self.noise_spectrum = np.array([s for idx, s in enumerate(noise_mean) if lf <= freq[idx] <= hf])
        self.noise_std = np.array([s for idx, s in enumerate(noise_sd) if lf <= freq[idx] <= hf])
        self.frequencies = np.array([f for f in freq if lf <= f <= hf])
        # -------------------------------------------------------------------------------------------------------------
        # Calculation the noise correction including the artificial bias
        correct_rate = 1.0
        given_correct_rate = configuration.get('correct_frequencies_rate')
        noise_correction = self.noise_spectrum.copy()
        noise_bias = phase_parameters('noise_bias', -1.0)
        if noise_bias > 0.0:
            noise_freq_bias = phase_parameters('noise_freq_bias')
            if noise_freq_bias is not None:
                noise_correction *= (1.0 + np.multiply(noise_bias, self.frequencies ** noise_freq_bias))
            else:
                noise_correction *= (1.0 + noise_bias)

        noise_std_bias = phase_parameters('noise_std_bias', -1.0)
        if noise_std_bias > 0.0:
            noise_correction += self.noise_std * noise_std_bias
        self.noise_correction_2 = np.square(noise_correction)
        # -------------------------------------------------------------------------------------------------------------
        # Compute the station_name response to the source spectrum model including the gradient Green's function
        if len(picks) == 1:
            radial_response, transversal_response = get_phase_response(picks[0], source_parameters, station_inventory,
                                                                       station_parameters, self.frequencies)
        else:
            radial_response, transversal_response = get_phases_response(picks, source_parameters, station_inventory,
                                                                        station_parameters, self.frequencies)
        self.response = np.sqrt(np.square(np.absolute(radial_response)) + np.square(np.absolute(transversal_response)))
        # instrument_response = station_inventory.get_response(picks[0].waveform_id.id, picks[0].time)
        # instrument_correction = np.absolute(instrument_response.get_evalresp_response_for_frequencies(self.frequencies,
        #                                                                                               output='VEL'))
        # self.response = np.multiply(self.response, instrument_correction)

        # -------------------------------------------------------------------------------------------------------------
        # Metric weights calculation
        weights_parameters = phase_parameters('weights')
        if weights_parameters is not None:
            weights = np.ones(self.frequencies.size, dtype=float)
            threshold = weights_parameters.get('use_threshold')
            std_weight = weights_parameters.get('use_std')
            noise_spectrum_bias = self.noise_spectrum * (1.0 + weights_parameters.get('use_bias', 0.0))
            if weights_parameters.get('use_logarithm', False):
                if std_weight:
                    delta = np.divide(self.signal_spectrum, noise_spectrum_bias + std_weight * self.noise_std)
                else:
                    delta = np.divide(self.signal_spectrum, noise_spectrum_bias)
                delta = np.log10(delta)
                if threshold:
                    weights[delta < threshold] = 0
                else:
                    delta[delta < 0.0] = 0.0
                    delta[delta > 1.0] = 1.0
                    weights = delta
            else:
                if std_weight:
                    delta = np.divide(self.signal_spectrum - noise_spectrum_bias - std_weight * self.noise_std,
                                      self.signal_spectrum)
                else:
                    delta = np.divide(self.signal_spectrum - noise_spectrum_bias, self.signal_spectrum)

                if threshold:
                    weights[delta < threshold] = 0
                else:
                    delta[delta < 0.0] = 0
                    weights = delta

            frequency_weight = weights_parameters.get('use_frequency')
            main_frequency = weights_parameters.get('use_main_frequency', 0.0)
            if frequency_weight:
                fw = np.power((1.0 + np.square(self.frequencies - main_frequency)), frequency_weight / 2.0)
                weights = np.multiply(weights, fw)
                correct_rate = np.sum(weights) / np.sum(fw) / len(weights)
            else:
                correct_rate = np.sum(weights) / len(weights)

        else:
            weights = 1.0
            correct_rate = np.sum(np.greater_equal(self.signal_spectrum, noise_correction)) / len(noise_correction)
        if given_correct_rate is not None:
            if correct_rate < given_correct_rate:
                raise ValueError(f"To small correct frequencies rate: {correct_rate:.2f}<{given_correct_rate:.2f}")
            else:
                print(f"Correct frequencies rate {correct_rate:.2f}")

        # -------------------------------------------------------------------------------------------------------------
        # Metric setting
        metric_name = configuration.get('metric', 'p-norm')
        self.metric = None
        if metric_name == 'p-norm' or metric_name == 'lin':
            self.metric = PNormMetric(configuration.get('p_value', 2.0), weights)
        elif metric_name == 'log':
            self.metric = LogMetric(configuration.get('p_value', 2.0), weights)
        else:
            raise Exception(f'Metric {metric_name} has not been implemented')
        # -------------------------------------------------------------------------------------------------------------
        # Source model setting
        self.source_model = get_source_model(self.frequencies, configuration)

    def __call__(self, source_parameters):
        """
        The function calculates the inaccuracy between the signal spectrum at the station_name and the signal spectrum
        calculated for the station_name from the source based on the magnitude mw and the corner frequency f_0.

        :param source_parameters: The tuple of seismic source parameters :math:`mw` and :math:`f_0`
        :type source_parameters: tuple or list

        :return: The difference between the signal spectrum at the station_name and the signal spectrum.
        :rtype: float

        """
        # Test begin
        mw = source_parameters[0]
        m_0 = 10.0 ** ((mw + 6.07) * 3.0 / 2.0)
        f_0 = 10.0 ** source_parameters[1]
        source_spectrum = self.source_model(m_0, f_0)
        # Test end
        # source_spectrum = self.SourceModel(*source_parameters, **kwargs)
        source_spectrum = np.multiply(source_spectrum, self.response)
        source_spectrum = np.sqrt(np.square(source_spectrum) + self.noise_correction_2)
        # plt.loglog(self.frequencies, source_spectrum, color=self.color)
        error = self.metric(self.signal_spectrum, source_spectrum)
        return error


class PNormMetric(object):
    r"""
    The p-norm metric class. It computes the distance
    
    .. math::

        \left\| \textbf{x},\textbf{y} \right\|=
        \left[\sum_{f=f_{low}}^{f_{high}}{\left|x\left(f\right)-y\left(f\right)\right|^p\cdot
        w\left(f\right)}\right]^\frac{1}{p}

    :param p: The power of the p-norm metric class
    :type p:
    :param weights:
        Weights for spectra frequency comparison. The size must be the same as spectra.
        Optional parameter. If missing no weight are applied.
    :type weights: np.array(float)

    """

    def __init__(self, p: float, weights: np.array = None):
        """

        :param p: The power of the p-norm metric class
        :type p:
        :param weights:
            Weights for spectra frequency comparison. The size must be the same as spectra.
            Optional parameter. If missing no weight are applied.
        :type weights: np.array(float)

        """
        self.p = p
        if weights:
            self.weights = weights
        else:
            self.weights = 1.0

    def __call__(self, x1, x2):
        return np.sum(np.multiply(np.fabs((x1 - x2)) ** self.p, self.weights)) ** (1 / self.p)


class LogMetric(object):
    r"""
    The logarithmic metric class. It computes the distance

    .. math::

        \left\| \textbf{x},\textbf{y} \right\|=
        \left[\sum_{f=f_{low}}^{f_{high}}{\left| \log\left( x\left(f\right) \right)-
        \log\left( y\left(f\right) \right)\right|^p\cdot
        w\left(f\right)}\right]^\frac{1}{p}

    :param p: The power of the p-norm metric class
    :type p:
    :param weights:
        Weights for spectra frequency comparison. The size must be the same as spectra.
        Optional parameter. If missing no weight are applied.
    :type weights: np.array(float)

    """

    def __init__(self, p, weights=None):
        """

        :param p: The power of the p-norm metric class
        :type p:
        :param weights:
            Weights for spectra frequency comparison. The size must be the same as spectra.
            Optional parameter. If missing no weight are applied.
        :type weights: np.array(float)
        """
        self.p = p
        if weights is None:
            self.weights = 1.0
        else:
            self.weights = weights

    def __call__(self, x1, x2):
        return np.sum(np.multiply(np.absolute(np.log(x1) - np.log(x2)) ** self.p, self.weights)) ** (1 / self.p)


def get_minimum_function_parameters(picks, station_name, signal_spectrum, noise_mean, noise_std, frequencies,
                                    source_parameters, station_inventory, configuration):
    return MwFunctionParameters(picks, station_name, signal_spectrum, noise_mean, noise_std, frequencies,
                                source_parameters, station_inventory, configuration)

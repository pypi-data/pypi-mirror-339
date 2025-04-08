"""
The general spectral magnitude estimation
-----------------------------------------

..
    :copyright:
        Jan Wiszniowski (jwisz@igf.edu.pl)
    :license:
        GNU Lesser General Public License, Version 3
        (https://www.gnu.org/copyleft/lesser.html)
    :version 0.0.1:
        2024-11-07

"""

import numpy as np
from amw.mw.utils import get_phase_window, get_spectrum, get_margin, get_noise_spectrum, DefaultParameters
from amw.mw.utils import get_source_par, get_minimization_method
from amw.core.utils import get_station_name
from amw.mw.parameters import MwFunctionParameters, get_travel_time
from obspy.core.event.base import TimeWindow


def estimate_mw(signal, begin_signal, picks, origin, station_inventory, configuration):
    """
    Function estimate_mw estimates either single phase or cumulated phases spectral moment magnitude.

    :param signal:
        The signal is the 3D seismic displacement stream, which must cover both the P wave, the S wave,
        and the noise before the P onset.

    :param signal:
        The signal is the 3D seismic displacement stream, which must cover both the P wave, the S wave,
        and the noise before the P onset.
    :type signal: ObsPy Stream
    :param begin_signal:
        The first phase time (usually it is P wave) required to select noise before seismic waves onset
    :type  begin_signal: ObsPy UTCDateTime
    :param picks:
        A list of picks of waves is used for moment magnitude estimation.
        It can consist of a single pick P or S, then the magnitude estimation method from the single wave is used,
        or two picks P and S for the magnitude estimation based on both waves.
    :type picks: list(ObsPy Pick)
    :param origin:
        The event origin.
    :type origin: ObsPy Origin
    :param station_inventory:
        The inventory of the station that the signal was picked on
    :type  station_inventory: ObsPy Inventory
    :param configuration: The configuration container of all parameters dictionary required for the program to work.
    :type configuration: dict

    :return:
        mw : Estimated moment magnitude
        f0 : Source function corner frequency
        m0 : Scalar moment
        time_window : The assessed time window of P and S waves
    :rtype: tuple

    Uses classes :
        DefaultParameters
        MwFunctionParameters
    Uses functions :
        get_source_par :
        get_margin :
        get_station_name :
        get_phase_window
        get_spectrum
        get_noise_spectrum
        get_minimization_method
        minimization_method
        
    """
    source_parameters = get_source_par(origin, configuration)
    plotter = configuration.get('Plotter')
    # Seismic signal cutting to window
    taper_margin = get_margin(1.0, configuration)
    station_name = get_station_name(picks[0].waveform_id)
    station_parameters = DefaultParameters('station_parameters', station_name, configuration)
    if len(picks) == 2:
        phases_window = get_phase_window('S', picks, origin, station_inventory,
                                         station_parameters) + (picks[-1].time - picks[0].time)
    else:
        phases_window = get_phase_window(picks[0].phase_hint[0:1], picks, origin, station_inventory,
                                         station_parameters)
    begin_signal = begin_signal - phases_window * taper_margin * 0.35
    begin_phases = picks[0].time - phases_window * taper_margin * 0.35
    end_phases = picks[0].time + phases_window * (1.0 + taper_margin * 0.35)

    time_window = TimeWindow(reference=picks[0].time, begin=picks[0].time - begin_phases,
                             end=end_phases - picks[0].time)
    # seismic signal
    seismic_signal = signal.copy()
    seismic_signal.trim(starttime=begin_phases, endtime=end_phases)
    # noise signal
    noise_signal = signal.copy()
    noise_signal.trim(starttime=None, endtime=begin_signal)
    # checking consistency
    if len(noise_signal) != 3 or len(seismic_signal) != 3:
        print('Signal inconsistent')
        return None, None, None, time_window, None
    # offset remove
    for idx in range(3):
        offset = np.mean(noise_signal[idx].data)
        noise_signal[idx].data -= offset
        seismic_signal[idx].data -= offset
    # seismic spectrum
    seismic_spectrum, frequencies = get_spectrum(seismic_signal, configuration)
    # noise spectrum
    noise_mean, noise_std, noise_n = get_noise_spectrum(noise_signal, len(seismic_signal[0].data), configuration)
    # plot
    if plotter:
        plotter.plot_seismogram(picks, seismic_signal, signal, noise_n+1)
    # Searching for optimal source configuration
    x0 = np.array([1.0, 1.0])
    function_parameters = MwFunctionParameters(picks, station_name, seismic_spectrum, noise_mean,
                                               noise_std, frequencies, source_parameters,
                                               station_inventory, configuration)
    minimization_method = get_minimization_method(configuration['optimization'])
    result = minimization_method(function_parameters, x0, args=configuration)
    if result.success:
        mw = result.x[0]
        m0 = 10.0 ** ((mw + 6.07) * 3.0 / 2.0)
        mw += function_parameters.mw_correction
        f0 = 10.0 ** result.x[1]
        _, r, _ = get_travel_time(picks[0], source_parameters, station_inventory)
        if len(picks) == 2:
            print(f"\tMw={mw:.1f}, f_0={f0:.2f}, M_0={m0:.2e}, error={result.error:.2e}")
        else:
            print(f"\t{picks[0].phase_hint}: Mw={mw:.1f}, f_0={f0:.2f}, M_0={m0:.2e}, error={result.error:.2e}")
        if plotter:
            plotter.plot_results(m0, f0, function_parameters)
        return mw, f0, m0, time_window, r
    else:
        return None, None, None, time_window, None

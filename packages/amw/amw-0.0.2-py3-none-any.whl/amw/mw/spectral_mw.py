# -*- coding: utf-8 -*-
"""
Spectral magnitude estimation for all event in the catalog
----------------------------------------------------------

..
    :copyright:
        Jan Wiszniowski <jwisz@igf.edu.pl>
    :license:
        GNU Lesser General Public License, Version 3
        (https://www.gnu.org/copyleft/lesser.html)
    :version: 0.0.1
        2024-11-07

"""

from abc import ABC
import numpy as np
from amw.mw.utils import SpectralMwException, DefaultParameters, get_margin, get_phase_window, get_theoretical_s
from amw.mw.utils import get_theoretical_p, method_id_ph, method_id
from amw.mw.plot import PlotMw
from amw.core.utils import get_station_id, get_station_name, get_origin, get_magnitude
from amw.core.signal_utils import get_inventory, StreamLoader, load_inventory, StreamPreprocessing
from math import log10
from obspy.core.event.magnitude import StationMagnitude, StationMagnitudeContribution, Magnitude
from amw.mw.double_phase_mw import estimate_double_phase_mw
from amw.mw.single_phase_mw import estimate_single_phase_mw
import json
from obspy.core.event import read_events
import argparse
import warnings


# from amw._version import get_versions


class MwStreamPreprocessing(StreamPreprocessing, ABC):
    def __init__(self, configuration, inventory):
        super().__init__('Mw_preprocessing_1')
        self.inventory = None
        self.water_level = None
        self.prefilter = None
        self.allowed_channels = configuration.get('allowed_channels')
        rm = configuration.get('remove_response')
        if rm:
            self.inventory = inventory
            self.water_level = rm.get('water_level', 128)
            self.prefilter = rm.get('prefilter')
            self.output = rm.get('output', 'VEL')

    def _process(self, stream):
        if self.allowed_channels is not None:
            for chan_name in self.allowed_channels:
                chan_count = 0
                for trace in stream:
                    if chan_name == trace.meta.channel[:-1]:
                        chan_count += 1
                if chan_count < 3:
                    continue
                if chan_count > 3:
                    raise ValueError(f"Inconsistent data: {chan_count} traces of {chan_name}?")
                for trace in stream:
                    if chan_name != trace.meta.channel[:-1]:
                        stream.remove(trace)
                break
            else:
                raise ValueError(f"No allowed_channels")
        if self.inventory:
            # stream.plot()
            stream.remove_response(inventory=self.inventory, output=self.output,
                                   water_level=self.water_level, pre_filt=self.prefilter)
            # stream.plot()
        else:
            raise ValueError(f"No inventory")


def station_moment_magnitude(station_name, picks, event, origin, inventory, configuration):
    """
    Function estimate the mw magnitude for one event having origin and picks
    according the configuration.

    :param station_name:
        The station name in the form 'NN.SSSS', where NN is the network code and SSSS is the station_name code.
    :param station_name: str
    :param picks:
        The list of two picks: P and S. The P wave_name is first the S wave_name is second.
        If the wave_name is missing there should be None value. At list one wave_name is required,
        but wo picks P and S are recommended. At least one wave_name must be given. If the P or S wave_name is missing,
        the function tries to determine it based on the earthquake time at the focus and the remaining wave_name time.
    :type picks: ObsPy Pick
    :param event: The event object
    :type event: ObsPy Event
    :param origin:
        The event origin.
    :type origin: ObsPy Origin
    :param inventory:
        The inventory Object. It must contain the station_name inventory
    :type inventory: ObsPy Inventory
    :param configuration: The configuration container of all parameters dictionary required for the program to work.
    :type configuration: dict
    :return: The station magnitude object or None, if the magnitude can not be estimated.
    :rtype: ObsPy.StationMagnitude

    """
    station_inventory = get_inventory(station_name, origin.time, inventory)
    no_noise_windows = float(configuration.get('no_noise_windows', 6))
    if not station_inventory:
        raise SpectralMwException(f'Missing inventory for {station_name} at {origin.time}')
    if not picks[0] and not picks[1]:
        raise SpectralMwException(f'Missing P and S wave_name for {station_name}')
    print(f"Station {station_name}")
    station_parameters = DefaultParameters('station_parameters', station_name, configuration)
    taper_margin = get_margin(0.5, configuration)
    picks_pars = picks.copy()
    stream_loader = StreamLoader(configuration, MwStreamPreprocessing(configuration, inventory))
    # stream_loader = StreamLoader(configuration)
    if configuration['method'] == 'multiphase':
        if picks_pars[1] is None:
            picks_pars[1] = get_theoretical_s(picks_pars[0], origin)
        if picks_pars[0] is None:
            picks_pars[0] = get_theoretical_p(picks_pars[1], origin)
        window_length = get_phase_window('S', picks_pars, origin, station_inventory,
                                         station_parameters) + (picks_pars[1].time - picks_pars[0].time)
        signal_end = picks_pars[0].time + window_length * (1.0 + taper_margin) + 0.1
        signal_begin = picks_pars[0].time - no_noise_windows * window_length - (
                    2.0 * no_noise_windows + 1.0) * window_length * taper_margin - 0.1
        signal = stream_loader.get_signal(signal_begin, signal_end,
                                          event.resource_id.id + '_' + station_name, [station_name])
        signal = signal_by_phase(signal, picks_pars[0])
        if not signal:
            print(f'Missing signal for {station_name}')
            return None
        try:
            mw_ps, f0, m0, time_window, r = estimate_double_phase_mw(signal, picks_pars, origin,
                                                                     station_inventory, configuration)
        except ValueError as er:
            print(f"Mw estimation on S at {station_name}: {er}")
            return None
        except RuntimeWarning as er:
            print(f"Mw estimation on S at {station_name}: {er}")
            return None
        return StationMagnitude(mag=mw_ps, station_magnitude_type="mw", waveform_id=get_station_id(station_name),
                                origin_id=origin.resource_id, method_id=method_id(configuration))
    elif configuration['method'] == 'separate_phases':
        new_phases = picks_pars.copy()
        if not picks_pars[0]:
            new_phases[0] = get_theoretical_p(picks_pars[1], origin)

        if picks_pars[1]:
            s_length = get_phase_window('S', picks_pars, origin, station_inventory, station_parameters)
            s_full_length = s_length * (1.0 + taper_margin)
            signal_end = picks_pars[1].time + s_full_length + 0.1
            signal_begin = new_phases[0].time - no_noise_windows * s_full_length - 0.2
            signal = stream_loader.get_signal(signal_begin, signal_end,
                                              event.resource_id.id + '_' + station_name, [station_name])
        else:
            new_phases[1] = get_theoretical_p(picks_pars[0], origin)
            p_length = get_phase_window('P', new_phases, origin, station_inventory, station_parameters)
            p_full_length = p_length * (1.0 + taper_margin)
            signal_end = picks_pars[0].time + p_full_length + 0.1
            signal_begin = new_phases[0].time - no_noise_windows * p_full_length - 2.0
            signal = stream_loader.get_signal(signal_begin, signal_end,
                                              event.resource_id.id + '_' + station_name, [station_name])
        signal = signal_by_phase(signal, picks_pars[0])
        if not signal:
            print(f'Missing signal for {station_name}')
            return None
        m0_ps = 0.0
        f0_ps = 0.0
        n_ps = 0
        # station_magnitude = None
        if picks[0]:
            configuration['Plotter'].set_plot(station_name, event.resource_id.id, pick_name='P')
            try:
                mw_p, f0_p, m0_p, omega0_p, r = estimate_single_phase_mw(signal, 'P', new_phases, origin,
                                                                         station_inventory, configuration)
                m0_ps += m0_p
                f0_ps += f0_p
                n_ps += 1
            except ValueError as er:
                print(f"Mw estimation on P at {station_name}: {er}")
            except RuntimeWarning as er:
                print(f"Mw estimation on P at {station_name}: {er}")
        if picks[1]:
            configuration['Plotter'].set_plot(station_name, event.resource_id.id, pick_name='S')
            try:
                mw_s, f0_s, m0_s, omega0_s, r = estimate_single_phase_mw(signal, 'S', new_phases, origin,
                                                                         station_inventory, configuration)
                m0_ps += m0_s
                f0_ps += f0_s
                n_ps += 1
            except ValueError as er:
                print(f"Mw estimation on S at {station_name}: {er}")
            except RuntimeWarning as er:
                print(f"Mw estimation on S at {station_name}: {er}")
        if n_ps == 0:
            return None
        if n_ps == 2:
            m0_ps /= n_ps
            mw_ps = 2.0 / 3.0 * log10(m0_ps) - 6.07
            f0_ps /= n_ps
            return StationMagnitude(mag=mw_ps, station_magnitude_type="mw", waveform_id=get_station_id(station_name),
                                    origin_id=origin.resource_id, method_id=method_id(configuration))
    else:
        raise SpectralMwException('Unknown method')


def signal_by_phase(signal, pick):
    if not signal:
        return signal
    pick_id = pick.waveform_id
    for trace in signal:
        trace_meta = trace.meta
        if trace_meta.network != pick_id.network_code:
            signal.remove(trace)
            continue
        if trace_meta.station != pick_id.station_code:
            signal.remove(trace)
            continue
        if pick_id.location_code and trace_meta.location != pick_id.location_code:
            signal.remove(trace)
            continue
        if pick_id.channel_code and trace_meta.channel[:-1] != pick_id.channel_code[:-1]:
            signal.remove(trace)
    if len(signal) < 3:
        print(f'The signal has only {len(signal)} components')
        return None
    if len(signal) != 3:
        print(f'Signal inconsistent')
        return None
    return signal


def catalog_moment_magnitudes(catalog, configuration):
    r"""
    Function estimate the mw magnitude for all events having origin and picks according the configuration.
    As a result the function modifies the catalog and adds mw magnitude to events

    :param catalog:
        The seismic catalog of event the magnitude will be estimated.
        The estimated magnitudes will be added to the catalog magnitude.
    :type catalog: ObsPy Catalog
    :param configuration: The configuration container of all parameters dictionary required for the program to work.
    :type configuration: dict
    :return: None

    """
    inventory = load_inventory(configuration)
    preprocessing = MwStreamPreprocessing(configuration, inventory)
    stream_loader = StreamLoader(configuration, preprocessing)
    # stream_loader = StreamLoader(configuration)
    taper_margin = get_margin(0.5, configuration)
    no_events = len(catalog)
    nsw = float(configuration.get('no_noise_windows', 6))
    if no_events > 10:
        plot_parameters = configuration.get('plot')
        if plot_parameters is not None and not plot_parameters.get('do_not_draw', False):
            answer = input(f'There are {no_events} events\n Turn off plotting? [yes/no] >')
            if answer and answer[0] == 'y':
                plot_parameters['do_not_draw'] = True
    temporary_backup = configuration.get("temporary_backup", 1000000)
    for event_no, event in enumerate(catalog):
        if event_no > temporary_backup and event_no % temporary_backup == 1:
            catalog.write("temporary_backup.xml")
            print("Temporary backup")
        print(f"Event '{event.resource_id}' {event_no + 1}/{no_events}")
        origin = get_origin(event)
        if not origin:
            print(f'No origin for event {event.resource_id}')
            continue
        previous_mw = get_magnitude(event, magnitude_type='Mw')
        if previous_mw is None:
            print(f"{origin.time.ctime()}")
        else:
            print(f"{origin.time.ctime()}, previous Mw = {previous_mw.mag:.1f}")
        sta_picks_pars = {}
        for pick in event.picks:
            sta_name = get_station_name(pick.waveform_id)
            if sta_name not in sta_picks_pars:
                sta_picks_pars[sta_name] = [None, None]
            if pick.phase_hint[0:1] == 'P':
                sta_picks_pars[sta_name][0] = pick
            elif pick.phase_hint[0:1] == 'S':
                sta_picks_pars[sta_name][1] = pick
        if not sta_picks_pars:
            print(f'No picks for event {event.resource_id}')
            continue
        configuration['Plotter'] = PlotMw(configuration)
        configuration['Plotter'].start_plot(list(sta_picks_pars.keys()))
        station_magnitudes = []
        for sta_name, picks_pars in sta_picks_pars.items():
            print(f"Station {sta_name}")
            configuration['Plotter'].start_plot(sta_name)
            station_parameters = DefaultParameters('station_parameters', sta_name, configuration)
            station_inventory = get_inventory(sta_name, origin.time, inventory)
            if not station_inventory:
                print('Missing inventory for {} at {}'.format(sta_name, origin.time))
                continue
            if not picks_pars[0] and not picks_pars[1]:
                print('Missing P and S wave_name for {}'.format(sta_name))
                continue
            if configuration['method'] == 'multiphase':
                configuration['Plotter'].set_plot(sta_name, event.resource_id.id)
                # Counting the required samples period
                if picks_pars[1] is None:
                    picks_pars[1] = get_theoretical_s(picks_pars[0], origin)
                if picks_pars[0] is None:
                    picks_pars[0] = get_theoretical_p(picks_pars[1], origin)
                wl = get_phase_window('S', picks_pars, origin, station_inventory,
                                      station_parameters) + (picks_pars[1].time - picks_pars[0].time)
                signal_end = picks_pars[0].time + wl * (1.0 + taper_margin) + 0.2
                signal_begin = picks_pars[0].time - nsw * wl - (2.0 * nsw + 1.0) * wl * taper_margin - 0.2
                signal = stream_loader.get_signal(signal_begin, signal_end,
                                                  event.resource_id.id + '_' + sta_name, [sta_name])
                signal = signal_by_phase(signal, picks_pars[0])
                if not signal:
                    print(f'Missing signal for {sta_name}')
                    continue
                # signal.plot()
                try:
                    mw_ps, f0, m0, time_window, r = estimate_double_phase_mw(signal, picks_pars, origin,
                                                                             station_inventory, configuration)
                    # spectral_parameters = SpectralParameters()
                    station_magnitude = StationMagnitude(mag=mw_ps, station_magnitude_type="mw",
                                                         waveform_id=get_station_id(sta_name),
                                                         origin_id=origin.resource_id,
                                                         method_id=method_id(configuration))
                    station_magnitudes.append(station_magnitude)
                except ValueError as er:
                    print(f"Mw estimation on PS at {sta_name}: {er}")
                except RuntimeWarning as er:
                    print(f"Mw estimation on PS at {sta_name}: {er}")
            elif configuration['method'] == 'separate_phases':
                new_phases = picks_pars.copy()
                if not picks_pars[0]:
                    new_phases[0] = get_theoretical_p(picks_pars[1], origin)

                if picks_pars[1]:
                    s_length = get_phase_window('S', picks_pars, origin, station_inventory, station_parameters)
                    s_full_length = s_length * (1.0 + taper_margin)
                    signal_end = picks_pars[1].time + s_full_length + 0.1
                    signal_begin = new_phases[0].time - (nsw + 0.1) * s_full_length - 0.2
                    signal = stream_loader.get_signal(signal_begin, signal_end,
                                                      event.resource_id.id + '_' + sta_name, [sta_name])
                else:
                    new_phases[1] = get_theoretical_s(picks_pars[0], origin)
                    p_length = get_phase_window('P', new_phases, origin, station_inventory, station_parameters)
                    p_full_length = p_length * (1.0 + taper_margin)
                    signal_end = picks_pars[0].time + p_full_length + 0.1
                    signal_begin = new_phases[0].time - (nsw + 0.2) * p_full_length - 0.2
                    signal = stream_loader.get_signal(signal_begin, signal_end,
                                                      event.resource_id.id + '_' + sta_name, [sta_name])
                signal = signal_by_phase(signal, picks_pars[0])
                if not signal:
                    print(f'Missing signal for {sta_name}')
                    continue
                m0_ps = 0.0
                f0_ps = 0.0
                n_ps = 0
                if picks_pars[0]:
                    configuration['Plotter'].set_plot(sta_name, event.resource_id.id, pick_name='P')
                    try:
                        mw_p, f0_p, m0_p, omega0_p, r = estimate_single_phase_mw(signal, 'P', new_phases, origin,
                                                                                 station_inventory, configuration)
                        station_magnitude = StationMagnitude(mag=mw_p, station_magnitude_type="mw",
                                                             waveform_id=get_station_id(sta_name),
                                                             origin_id=origin.resource_id,
                                                             method_id=method_id_ph('P', configuration))
                        station_magnitudes.append(station_magnitude)
                        # print(f"\t{2.0 / 3.0 * log10(m0_p) - 6.27:.1f}")
                        m0_ps += m0_p
                        f0_ps += f0_p
                        n_ps += 1
                    except ValueError as er:
                        print(f"Mw estimation on P at {sta_name}: {er}")
                    except RuntimeWarning as er:
                        print(f"Mw estimation on P at {sta_name}: {er}")
                    # show_plot(configuration)
                    # block_plot()
                if picks_pars[1]:
                    configuration['Plotter'].set_plot(sta_name, event.resource_id.id, pick_name='S')
                    try:
                        mw_s, f0_s, m0_s, omega0_s, r = estimate_single_phase_mw(signal, 'S', new_phases, origin,
                                                                                 station_inventory, configuration)
                        station_magnitude = StationMagnitude(mag=mw_s, station_magnitude_type="mw",
                                                             waveform_id=get_station_id(sta_name),
                                                             origin_id=origin.resource_id,
                                                             method_id=method_id_ph('S', configuration))
                        station_magnitudes.append(station_magnitude)
                        # print(f"\t{2.0 / 3.0 * log10(m0_s) - 6.07:.1f}")
                        m0_ps += m0_s
                        f0_ps += f0_s
                        n_ps += 1
                    except ValueError as er:
                        print(f"Mw estimation on S at {sta_name}: {er}")
                    except RuntimeWarning as er:
                        print(f"Mw estimation on S at {sta_name}: {er}")
                if n_ps == 0:
                    continue
                if n_ps == 2:
                    m0_ps /= n_ps
                    mw_ps = 2.0 / 3.0 * log10(m0_ps) - 6.07
                    f0_ps /= n_ps
                    # station_magnitude = StationMagnitude(mag=mw_ps, station_magnitude_type="mw",
                    #                                      waveform_id=get_station_id(sta_name),
                    #                                      origin_id=origin.resource_id,
                    #                                      method_id=method_id(configuration))
                    # station_magnitudes.append(station_magnitude)
                    print(f"\tXX: mw={mw_ps:.1f}, f_0={f0_ps:.2f}, M_0={m0_ps:.2e}")
            else:
                raise SpectralMwException('Unknown method')
            print(f"\tr={r / 1000.0:.1f} km")
            configuration['Plotter'].format_plot('many figures')
            configuration['Plotter'].format_plot('many figures inline')
            # block_plot()
        if not station_magnitudes:
            continue
        remove_outliers = configuration.get('remove_outliers')
        if remove_outliers is not None:
            mags = [sm.mag for sm in station_magnitudes]
            quantile = remove_outliers.get('quantile', [0.25, 0.75])
            if len(mags) > 3:
                q25 = np.quantile(mags, quantile[0])
                q75 = np.quantile(mags, quantile[1])
                mags = [x for x in mags if q25 <= x <= q75]
            mean_mag = np.mean(mags)
            var_std = np.std(mags) * remove_outliers.get('multiple_deviation', 3.0)
            low_limit = mean_mag - var_std
            high_limit = mean_mag + var_std
            station_magnitudes = [sm for sm in station_magnitudes if low_limit <= sm.mag <= high_limit]
        mw = Magnitude(mag=0.0, magnitude_type="mw", origin_id=origin.resource_id,
                       method_id=method_id(configuration))
        sum_weights = 0.0
        for station_magnitude in station_magnitudes:
            event.station_magnitudes.append(station_magnitude)
            sta_name = get_station_name(station_magnitude.waveform_id)
            station_parameters = DefaultParameters('station_parameters', sta_name, configuration)
            weight = station_parameters('weight', 1.0)
            smc = StationMagnitudeContribution(station_magnitude_id=station_magnitude.resource_id, weight=weight)
            mw.station_magnitude_contributions.append(smc)
            sum_weights += weight
            mw.mag += station_magnitude.mag * weight
        mw.mag /= sum_weights
        mw.station_count = len(mw.station_magnitude_contributions)
        event.magnitudes.append(mw)
        print(f"New mw = {mw.mag:.1f}")
        configuration['Plotter'].format_plot('single figure')
        configuration['Plotter'].show_plot('many figures')
        configuration['Plotter'].show_plot('many figures inline')
        configuration['Plotter'].show_plot('single figure')


def main():
    # Raise specific warning type
    warnings.filterwarnings("error", category=RuntimeWarning)

    # __version__ = get_versions()['version']
    # __release_date__ = get_versions()['date']

    # Argument parsing
    parser = argparse.ArgumentParser(
        prog='spectral_mw',
        description='Program estimates moment magnitudes from P-, S- or cumulate PS-waves'
                    'in far, intermediate, and near fields')
    # epilog='End of help')
    parser.add_argument('config', help='Configuration file in JSON format')
    # WARNING!!! When you use -S option the file is not overwritten.
    # It must be not existing file name'
    parser.add_argument('-c', '--catalog', metavar='catalog_name.xml', help='Catalog file in QuakeML XML format')
    # parser.add_argument('-e', '--evid', metavar='smi:local\...',
    #                     help='The one event id that magnitude will be estimated')
    parser.add_argument('-s', '--stream', metavar='stream_file_name',
                        help='Stream file of waveforms of all stations for one event instead of read from server'
                             'The signal must have enough pre-P-wave period for noise estimation.')
    parser.add_argument('-o', '--output', metavar='output_catalog.xml', help='Output catalog file name')
    parser.add_argument('-f', '--output_format', default='QUAKEML', help='Output catalog format')
    parser.add_argument('-i', '--input_format', default='QUAKEML', help='Output catalog format')
    # parser.add_argument('-v', '--verbose',
    #                     action='store_true')
    # parser.print_help()
    args = parser.parse_args()
    with open(args.config, "r") as f:
        configuration = json.load(f)
    if args.catalog is None:
        catalog = read_events(configuration['catalog_file'], format=args.input_format)
    else:
        catalog = read_events(args.catalog, format=args.input_format)
    if args.stream is not None:
        configuration['stream'] = {'source': 'file', 'pathname': args.stream}
    # Magnitude computing
    catalog_moment_magnitudes(catalog, configuration)
    # Result saving
    if args.output is None:
        catalog.write(configuration.get('output_file', 'output.xml'), format=args.output_format)
    else:
        catalog.write(args.output, format=args.output_format)


if __name__ == '__main__':
    main()

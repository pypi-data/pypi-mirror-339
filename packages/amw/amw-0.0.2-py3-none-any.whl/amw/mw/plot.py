"""
The plot functions
------------------

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
import matplotlib.pyplot as plt
from matplotlib.dates import date2num, DateFormatter, SecondLocator
from amw.mw.utils import get_simple_taper
from amw.mw.utils import format_filename
# from amw.mw.utils import get_source_model


class PlotMw(object):
    """
    Class used to plot results of spectral magnitude estimation

    :param configuration: The full local mw configuration. The class uses the 'plot' subdirectory
        and 'method' describing the magnitude estimation method for preparing appropriate figure.
    :type configuration: dict
    """
    def __init__(self, configuration):
        """
        :param configuration: The full local mw configuration. The class uses the ``plot`` subdirectory
            and ``method`` describing the magnitude estimation method for preparing appropriate figure.
        :type configuration: dict
        """
        self.configuration = configuration
        self.plot_parameters = None
        self.axs = None  # Directory of axes
        self.ax = None  # Current spectrum's axis
        self.sax = None  # Current signal axis
        self.fig = None  # Figure
        self.view_begin = None
        self.view_end = None
        plot_parameters = configuration.get('plot')
        if plot_parameters is None:
            return
        if plot_parameters.get('do_not_draw', False):
            return
        self.plot_parameters = plot_parameters
        self.how_to_show = self.plot_parameters.get('how_to_show', 'single figure')
        self.method = configuration['method']
        self.station = ''
        self.pick = ''
        self.event_id = '-'

    def set_plot(self, station_name, event_id, pick_name=None):
        """
        The method sets the plot area for station and optional the string.
        In the case of magnitude estimation on single phase the ``pick`` must be the phase name ``P`` or ``S``.
        In the case of magnitude estimation on many phases together the ``pick`` must be None or omitted.

        :param station_name: The station name in the form "NN.SSSS" where NN is the network
            code and SSSS is the station code
        :type station_name: str
        :param event_id: Event id
        :type event_id: str
        :param pick_name: The pick name. It must be ``P`` or ``S`` for single phase mw or None for many phases mw
        :type pick_name: str
        """
        if self.plot_parameters is None:
            return
        if pick_name is None:
            self.ax = self.axs[station_name]['spec']
        else:
            self.ax = self.axs[station_name][pick_name]
        self.sax = self.axs[station_name]['signal']
        self.pick = pick_name
        self.station = station_name
        self.event_id = event_id

    def start_plot(self, stations):
        """
        The method configures the plots, defines figures and axis. The way of plotting depends
        on the ``plot``, ``how_to_show`` parameter in the configuration file.
        There are three possibilities:

        * ``single figure`` - results of magnitude estimation of all station are in plot one figure,
          station under station. On the left is seismogram and the left are spectra,

        * ``many figures`` - results of magnitude estimation of all station are in one figure.
          On the left is the seismogram and the bottom are spectra,

        * ``many figures inline`` - results of magnitude estimation of all station are in one figure.
          On the left is the seismogram and the left are spectra,

        :param stations: List of station names
        :type stations: list(str)
        """
        if self.plot_parameters is None:
            return
        self.ax = None  # Current spectrum's axis
        self.sax = None  # Current signal axis
        self.view_begin = None
        self.view_end = None
        fig = None
        if self.how_to_show == 'single figure':
            if isinstance(stations, str):
                return
            if self.fig:
                return
            self.axs = {}  # Clear directory of axes
            ns = len(stations)
            if self.method == 'multiphase':
                fig, axs = plt.subplots(nrows=ns, ncols=3, sharex='row')
                fig.set_size_inches(10, 3*ns)
                for idx in range(len(stations)):
                    gs = axs[idx, 0].get_gridspec()
                    for ax in axs[idx, 0:2]:
                        ax.remove()
                    sax = fig.add_subplot(gs[idx, 0:2])
                    self.axs[stations[idx]] = {'spec': axs[idx, 2], 'signal': sax}
                    axs[idx, 2].set(ylabel='[m*s]')
                    if idx == 0:
                        axs[idx, 2].set(title='Spectra')
                        sax.set(title='Waveforms')
                    elif idx == ns-1:
                        axs[idx, 2].set(xlabel='Frequency [Hz]')
            else:
                fig, axs = plt.subplots(nrows=len(stations), ncols=4, sharex='row')
                fig.set_size_inches(13, 3*ns)
                for idx in range(len(stations)):
                    gs = axs[idx, 0].get_gridspec()
                    for ax in axs[idx, 0:2]:
                        ax.remove()
                    sax = fig.add_subplot(gs[idx, 0:2])
                    self.axs[stations[idx]] = {'P': axs[idx, 2], 'S': axs[idx, 3], 'signal': sax}
                    axs[idx, 2].set(ylabel='[m*s]')
                    if idx == 0:
                        axs[idx, 2].set(title='P spectra')
                        axs[idx, 3].set(title='S spectra')
                        sax.set(title='Waveforms')
                    elif idx == ns-1:
                        axs[idx, 2].set(xlabel='Frequency [Hz]')
                        axs[idx, 3].set(xlabel='Frequency [Hz]')
        elif self.how_to_show == 'many figures inline':
            if not isinstance(stations, str):
                return
            self.axs = {}  # Clear directory of axes
            if self.method == 'multiphase':
                fig, axs = plt.subplots(nrows=1, ncols=3)
                fig.set_size_inches(10, 3)
                self.axs[stations] = {'spec': axs[2]}
                axs[2].set(title='Spectra')
                axs[2].set(xlabel='Frequency [Hz]')
            else:
                fig, axs = plt.subplots(nrows=1, ncols=4)
                fig.set_size_inches(13, 3)
                self.axs[stations] = {'P': axs[2], 'S': axs[3]}
                axs[2].set(title='P spectra')
                axs[3].set(title='S spectra')
                axs[2].set(xlabel='Frequency [Hz]')
                axs[3].set(xlabel='Frequency [Hz]')
            gs = axs[0].get_gridspec()
            for ax in axs[0:2]:
                ax.remove()
            sax = fig.add_subplot(gs[0:2])
            self.axs[stations]['signal'] = sax
            sax.set(title='Waveforms')
            sax.set(xlabel='Time')
            axs[2].set(ylabel='[m*s]')
        elif self.how_to_show == 'many figures':
            if not isinstance(stations, str):
                return
            self.axs = {}  # Clear directory of axes
            if self.method == 'multiphase':
                fig, axs = plt.subplots(nrows=2, ncols=1)
                self.axs[stations] = {'spec': axs[1], 'signal': axs[0]}
                # fig, axs = plt.subplots(nrows=2, ncols=2, sharex=True)
                # gs = axs[0, 0].get_gridspec()
                # for ax in axs[0, :]:
                #     ax.remove()
                # axs[1, 1].axis('off')
                # sax = fig.add_subplot(gs[0, :])
                # self.axs[stations] = {'spec': axs[1, 0], 'signal': sax}

            else:
                fig, axs = plt.subplots(nrows=2, ncols=2)
                gs = axs[0, 0].get_gridspec()
                for ax in axs[0, :]:
                    ax.remove()
                sax = fig.add_subplot(gs[0, :])
                self.axs[stations] = {'P': axs[1, 0], 'S': axs[1, 1], 'signal': sax}
        self.fig = fig

    def format_plot(self, how_to_show):
        """
        Does nothing. Prepared to reformat final view

        :param how_to_show: Condition what to show. I can be only values 'single figure', 'many figures' or
            'many figures inline'. Format is performed if the parameter equals with the 'what to show' 'plot'
            parameter in the configuration.
        :type how_to_show: str
        """
        if self.plot_parameters is None or self.fig is None:
            return
        if self.plot_parameters.get('do_not_draw', False):
            return
        if self.view_begin and self.sax is not None:
            self.sax.set_xlim(date2num(self.view_begin.datetime), date2num(self.view_end.datetime))
        if how_to_show == self.how_to_show:
            self.fig.tight_layout()
            if self.how_to_show == 'single figure':
                self.fig.savefig(f'All_{format_filename(self.event_id)}.png')
            else:
                self.fig.savefig(f'{self.station}_{format_filename(self.event_id)}.png')

        # plt.tight_layout()

    def plot_results(self, m0, f0, function_parameters):
        """
        Plots spectra of estimation results. It can plot:

        * The signal spectrum,
        * The source spectrum at the station
        * The mean value of the noise spectrum
        * The uncertainty range of the noise spectrum


        :param m0: Scalar moment magnitude :math:`M_0`
        :type m0: float
        :param f0: Cornel focal function frequency :math:`f_0`
        :type f0: float
        :param function_parameters: All parameters used to estimate the mw
        :type function_parameters: MwFunctionParameters
        """
        if self.plot_parameters is None or self.fig is None or self.ax is None:
            return
        if self.plot_parameters.get('do_not_draw', False):
            return
        if self.plot_parameters.get('draw_the_signal_spectrum', True):
            self.ax.loglog(function_parameters.frequencies, function_parameters.signal_spectrum, color='k')
        source_spectrum = function_parameters.source_model(m0, f0)
        if self.plot_parameters.get('draw_the_noise', False):
            self.ax.loglog(function_parameters.frequencies, function_parameters.noise_spectrum, color='b')
        if self.plot_parameters.get('draw_the_noise_correction', False):
            self.ax.loglog(function_parameters.frequencies, np.sqrt(function_parameters.noise_correction_2),
                           color='c', linestyle='--')
        if self.plot_parameters.get('draw_the_noise_uncertainty', False):
            self.ax.loglog(function_parameters.frequencies,
                           function_parameters.noise_spectrum + function_parameters.noise_std,
                           color='b', linestyle=':')
            # self.ax.loglog(function_parameters.frequencies,
            #                function_parameters.noise_spectrum - function_parameters.noise_std,
            #                color='b', linestyle=':')
        source_spectrum = np.multiply(source_spectrum, function_parameters.response)
        if self.plot_parameters.get('draw_source_spectrum_without_the_noise', False):
            self.ax.loglog(function_parameters.frequencies, source_spectrum, color='g')
        if self.plot_parameters.get('draw_source_spectrum_with_the_noise', True):
            source_spectrum = np.sqrt(np.square(source_spectrum) + function_parameters.noise_correction_2)
            self.ax.loglog(function_parameters.frequencies, source_spectrum, color='r')

    def plot_seismogram(self, picks, traces, stream, n_noises):
        """
        Plots seismogram with picks and taper window

        :param picks:
        :type picks:
        :param traces:
        :type traces:
        :param stream:
        :type stream:
        :param n_noises:
        :type n_noises:
        """
        # self.fig, self.sax = plt.subplots()
        if self.plot_parameters is None or self.fig is None or self.sax is None:
            return
        if self.plot_parameters.get('do_not_draw', False):
            return
        colors = {'Z': 'b', 'N': 'c', 'E': 'g'}
        global_min = 1e10
        global_max = -1e10
        if self.view_begin is None:
            self.view_begin = traces[0].meta.starttime
            self.view_end = traces[0].meta.endtime
        else:
            if self.view_begin > traces[0].meta.starttime:
                self.view_begin = traces[0].meta.starttime
            if self.view_end < traces[0].meta.endtime:
                self.view_end = traces[0].meta.endtime
        for idx in range(len(stream)):
            trace = stream[idx]
            view = self.plot_parameters.get('view', 'VEL')
            if view == 'VEL':
                self.sax.set_ylabel(f'{self.station}\nm/s')
            elif view == 'DISP':
                trace.detrend("polynomial", order=3)
                trace = trace.copy().integrate()
                trace.detrend("polynomial", order=5)
                self.sax.set_ylabel(f'{self.station}\nm')
            local_min = np.min(trace.data)
            local_max = np.max(trace.data)
            if global_min > local_min:
                global_min = local_min
            if global_max < local_max:
                global_max = local_max
            # c = trace.stats.channel
            self.sax.plot(trace.times("matplotlib"), trace.data, colors[trace.stats.channel[2]])
        for pick in picks:
            x = date2num(pick.time.datetime)
            self.sax.plot([x, x], [global_min, global_max], 'r')
            self.sax.text(x, 0.95 * global_max + 0.05 * global_min, pick.phase_hint)
        taper = get_simple_taper(traces[0].data, self.configuration) * global_max
        times = traces[0].times("matplotlib")
        self.sax.plot(times, taper, 'k:')
        if self.plot_parameters.get('draw_the_noise', False):
            self.view_begin = stream[0].meta.starttime
            begin = date2num(self.view_begin.datetime)
            times = times - times[0]
            step = times[-1] - times[0]
            for idx in range(n_noises):
                self.sax.plot(times+begin, taper, 'k:')
                begin += step
        self.sax.xaxis.set_major_locator(SecondLocator(np.arange(0, 60, self.plot_parameters.get('mark_seconds', 2))))
        self.sax.xaxis.set_minor_locator(SecondLocator())
        self.sax.xaxis.set_major_formatter(DateFormatter('%M:%S'))
        self.fig.autofmt_xdate(rotation=0, ha='left')
        plt.setp(self.sax.get_xticklabels(), visible=True)

    def show_plot(self, how_to_show):
        """
        Visualize the plot and save figure to the file.

        :param how_to_show: Condition what to show. I can be only values 'single figure', 'many figures' or
            'many figures inline'. Plot is shown if the parameter equals with the 'what to show' 'plot'
            parameter in the configuration.
        :type how_to_show: str
        """
        if self.plot_parameters is None or self.fig is None:
            return
        if self.plot_parameters.get('do_not_draw', False):
            return
        if how_to_show == self.how_to_show:
            # self.fig.tight_layout()
            # if self.how_to_show == 'single figure':
            #     self.fig.savefig('results.png')
            # else:
            #     self.fig.savefig(f'{self.station}.png')
            plt.show(block=True)

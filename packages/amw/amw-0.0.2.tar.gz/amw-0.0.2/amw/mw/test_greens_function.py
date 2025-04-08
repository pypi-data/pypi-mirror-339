"""
The plot of the source spectra
------------------------------

Program plot the source spectra including the source term and theoretical Green function

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
import sys
import json
from amw.mw.parameters import get_intermediate_response, get_far_response
from amw.mw.utils import DefaultParameters, DefaultSubParameters
import matplotlib.pyplot as plt
from amw.mw.source_models import BoatwrightSourceModel, HaskellSourceModel


def test_phase_response(phase_name, r, fault_v, rho, station_parameters, frequencies):
    travel_time = r / fault_v
    phase_parameters = DefaultSubParameters('phase_parameters', phase_name, station_parameters)
    q_0 = phase_parameters('Q_0')
    q_theta = phase_parameters('Q_theta', 0.0)
    q_corner = phase_parameters('Q_corner', -1.0)
    if q_corner > 0.0:
        eval_q = q_0 * pow(1 + frequencies / q_corner, q_theta)
    else:
        eval_q = q_0 * pow(frequencies, q_theta)
    q_cor = np.exp(-np.pi * travel_time * np.divide(frequencies, eval_q))
    kappa = phase_parameters('kappa', 0.0)
    kappa_cor = np.exp(-np.pi * kappa * frequencies)
    correction = np.multiply(q_cor, kappa_cor)
    correction *= phase_parameters('surface_correction', 1.0)
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
    radial_response = np.multiply(radial_response, correction)
    transversal_response = np.multiply(transversal_response, correction)
    return radial_response, transversal_response


def test_phases_response(r, fault_vp, rho, station_parameters, frequencies, near=False):
    omega = 2.0 * np.pi * 1j * frequencies
    radial_response, transversal_response = test_phase_response('P', r, fault_vp, rho, station_parameters,
                                                                frequencies)
    rs, ts = test_phase_response('S', r, fault_vp / np.sqrt(3), rho, station_parameters, frequencies)
    radial_response += rs
    transversal_response += ts
    if near:
        # far_radial_average_radiation = station_parameters('far_radial_average_radiation', 0.52)
        # far_transversal_average_radiation = station_parameters('far_transversal_average_radiation', 0.63)
        # resp = test_near_response(r, fault_vp, rho, omega)
        # resp = np.multiply(resp, np.exp(- np.pi * station_parameters('kappa', 0.0) * frequencies))
        # radial_response += resp * station_parameters('near_radial_average_radiation',
        #                                              9.0 * far_radial_average_radiation)
        # transversal_response += resp * station_parameters('near_transversal_average_radiation',
        #                                                   -6.0 * far_transversal_average_radiation)
        resp = test_near_response(r, fault_vp, rho, omega)
        resp = np.multiply(resp, np.exp(- np.pi * station_parameters('kappa', 0.0) * frequencies))
        radial_response += resp * station_parameters(
            'near_radial_average_radiation',
            9.0 * station_parameters('far_radial_average_radiation', 0.52))
        transversal_response += resp * station_parameters(
            'near_transversal_average_radiation',
            -6.0 * station_parameters('far_transversal_average_radiation', 0.63))

        resp = np.multiply(resp, np.exp(- np.pi * station_parameters('kappa', 0.0) * frequencies))
        radial_response += resp * station_parameters(
            'near_radial_average_radiation',
            9.0 * station_parameters('far_radial_average_radiation', 0.52))
        transversal_response += resp * station_parameters(
            'near_transversal_average_radiation',
            -6.0 * station_parameters('far_transversal_average_radiation', 0.63))

    return radial_response, transversal_response


def test_near_response(r, fault_vp, rho, omega):
    travel_time_p = r / fault_vp
    travel_time_s = np.sqrt(3) * travel_time_p
    print("Travel times for r={}: Tp={}s, Ts={}s, dT={:.2f}, min frequency {:.2f}".
          format(r,
                 travel_time_p,
                 travel_time_s,
                 travel_time_s - travel_time_p,
                 1.0 / (travel_time_s - travel_time_p)))

    element_p = np.multiply(omega * travel_time_p - 1.0, np.exp(-omega * travel_time_p))
    element_s = np.multiply(omega * travel_time_s - 1.0, np.exp(-omega * travel_time_s))
    near_response = element_p - element_s
    near_response = np.divide(near_response, 4.0 * np.pi * rho * r ** 4 * omega)
    near_response = np.divide(near_response, omega)
    return near_response


def test1_greens_function(ax, phase_name, configuration, source_freq_model, frequencies):
    station_parameters = DefaultParameters('station_parameters', 'NN.SSS', configuration)
    m = len(frequencies) // 4
    if phase_name == 'P':
        fault_v = 5000.0
    else:
        fault_v = 5000.0 / np.sqrt(3.0)
    distances = [500.0, 2000.0, 5000.0, 10000.0]
    rho = 2700.0
    for r in distances:
        station_parameters.this_parameter['consider_intermediate_field'] = False
        resp_r, resp_t = test_phase_response(phase_name, r, fault_v, rho, station_parameters, frequencies)
        response = np.sqrt(np.square(np.absolute(resp_r)) + np.square(np.absolute(resp_t)))
        plot_response = np.multiply(response, source_freq_model)
        ax.loglog(frequencies, plot_response, 'k:')
        station_parameters.this_parameter['consider_intermediate_field'] = True
        resp_r, resp_t = test_phase_response(phase_name, r, fault_v, rho, station_parameters, frequencies)
        response = np.sqrt(np.square(np.absolute(resp_r)) + np.square(np.absolute(resp_t)))
        plot_response = np.multiply(response, source_freq_model)
        ax.loglog(frequencies, plot_response, 'k--')
        ax.text(frequencies[m], plot_response[m] * 1.2, "r={:.1f}km".format(r / 1000.0))


def test2_greens_function(ax, _, configuration, source_freq_model, frequencies):
    m = len(frequencies) * 10 // 25
    station_parameters = DefaultParameters('station_parameters', 'NN.SSS', configuration)
    fault_v = 5000.0
    distances = [500.0, 2000.0, 10000.0]
    rho = 2700.0
    for r in distances:
        station_parameters.this_parameter['consider_intermediate_field'] = True
        resp_r, resp_t = test_phases_response(r, fault_v, rho, station_parameters, frequencies, True)
        response = np.sqrt(np.square(np.absolute(resp_r)) + np.square(np.absolute(resp_t)))
        plot_response = np.multiply(response, source_freq_model)
        ax.loglog(frequencies, plot_response, 'k')
        ax.text(frequencies[m], plot_response[m] * 1.2, "r={:.1f}km".format(r / 1000.0))

        resp_r, resp_t = test_phases_response(r, fault_v, rho, station_parameters, frequencies)
        response = np.sqrt(np.square(np.absolute(resp_r)) + np.square(np.absolute(resp_t)))
        plot_response = np.multiply(response, source_freq_model)
        ax.loglog(frequencies, plot_response, 'k--')

        station_parameters.this_parameter['consider_intermediate_field'] = False
        resp_r, resp_t = test_phases_response(r, fault_v, rho, station_parameters, frequencies)
        response = np.sqrt(np.square(np.absolute(resp_r)) + np.square(np.absolute(resp_t)))
        plot_response = np.multiply(response, source_freq_model)
        ax.loglog(frequencies, plot_response, 'k:')


def plot_green6(test_greens_function, tit, idx, phase_name, configuration, source_function, frequencies):
    ax = plt.subplot(2, 3, idx)
    test_greens_function(ax, phase_name, configuration, source_function, frequencies)
    if idx > 3:
        plt.xlabel('Frequency [Hz]', labelpad=0)
    if idx % 3 == 1:
        plt.ylabel("Disp. spec. [ms]")
    plt.title(tit, loc='left')
    plt.ylim(bottom=9.0e-6, top=2.7e-2)
    plt.xlim(left=frequencies[0], right=frequencies[-1])
    # plt.show(block=True)


def plot_green3(test_greens_function, tit, idx, phase_name, configuration, source_function, frequencies):
    ax = plt.subplot(3, 1, idx)
    test_greens_function(ax, phase_name, configuration, source_function, frequencies)
    if idx == 3:
        plt.xlabel('Frequency [Hz]', labelpad=0)
    else:
        plt.xticks([])
    plt.ylabel("Disp. spec. [ms]")
    plt.title(tit, loc='left')
    plt.ylim(bottom=9.0e-6, top=2.7e-2)
    plt.xlim(left=frequencies[0], right=frequencies[-1])


def main():
    if len(sys.argv) < 3:
        print('call: python test_greens_function.py what <config_json>')
        sys.exit()
    what = sys.argv[1]
    with open(sys.argv[2], "r") as f:
        configuration = json.load(f)
    # CurrentCatalog = read_events(sys.argv[2])
    view_range = configuration.get('ViewRange', [-0.3, 1.3, 100])
    frequencies = np.power(10.0, np.linspace(view_range[0], view_range[1], num=view_range[2]))
    mw = 3.9
    m_0 = 10.0 ** ((mw + 6.07) * 3.0 / 2.0)
    f_0 = 3.3
    if what == 'standard':
        # Without source model
        source_freq_model = np.divide(m_0, 2.0 * np.pi * frequencies)
        plot_green6(test1_greens_function, 'a)', 1, 'P', configuration, source_freq_model, frequencies)
        plot_green6(test1_greens_function, 'b)', 2, 'S', configuration, source_freq_model, frequencies)
        plot_green6(test2_greens_function, 'c)', 3, '', configuration, source_freq_model, frequencies)
        # Brune source model
        source_model = BoatwrightSourceModel(frequencies)
        source_freq_model = source_model(m_0, f_0)
        plot_green6(test1_greens_function, 'd)', 4, 'P', configuration, source_freq_model, frequencies)
        plot_green6(test1_greens_function, 'e)', 5, 'S', configuration, source_freq_model, frequencies)
        plot_green6(test2_greens_function, 'f)', 6, '', configuration, source_freq_model, frequencies)
    elif what == 'PS3':
        # Without source model
        source_freq_model = np.divide(m_0, 2.0 * np.pi * frequencies)
        plot_green3(test2_greens_function, 'a) Knopoff and Gillbert source model', 1, '', configuration,
                    source_freq_model, frequencies)
        # Haskell source model
        source_model = HaskellSourceModel(frequencies)
        source_freq_model = source_model(m_0, f_0)
        plot_green3(test2_greens_function, 'b) Haskell source model', 2, '', configuration, source_freq_model,
                    frequencies)
        # Brune source model
        source_model = BoatwrightSourceModel(frequencies)
        source_freq_model = source_model(m_0, f_0)
        plot_green3(test2_greens_function, 'c) Brune source model', 3, '', configuration, source_freq_model,
                    frequencies)

    plt.show(block=True)


if __name__ == '__main__':
    main()

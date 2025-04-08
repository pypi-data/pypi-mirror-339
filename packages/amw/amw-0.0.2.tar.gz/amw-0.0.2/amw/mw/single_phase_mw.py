"""
Single phase spectral magnitude estimation
------------------------------------------

..
    :copyright:
        Jan Wiszniowski (jwisz@igf.edu.pl)
    :license:
        GNU Lesser General Public License, Version 3
        (https://www.gnu.org/copyleft/lesser.html)
    :version 0.0.1:
        2024-11-07

"""

from amw.mw.estimation import estimate_mw
from amw.mw.utils import get_theoretical_s, get_theoretical_p, SpectralMwException


def estimate_single_phase_mw(signal, pick_name, picks, origin, station_inventory, configuration):
    """
    Estimates spectral moment magnitude on the single phase P or S

    :param signal: The signal is the 3D seismic displacement stream, which must cover both the P wave, the S wave,
        and the noise before the P onset.
    :type signal: ObsPy.Stream
    :param pick_name: The name of the pick 'P' or 'S'
    :type pick_name: str
    :param picks: Two picks P and S are recommended. At least one wave_name must be given.
        If the P or S wave_name is missing,
        the function tries to determine it based on the earthquake time at the focus and the remaining wave_name time.
    :type picks: list(ObsPy.Pick)
    :param origin:
        The event origin.
    :type origin: ObsPy.Origin
    :param station_inventory:
        The inventory of the station that the signal was picked on
    :type station_inventory: ObsPy.Inventory
    :param configuration: The configuration container of all parameters dictionary required for the program to work.
    :type configuration: dict
    :param inventory: The inventory of all stations and channels
    :type inventory:  ObsPy.Inventory

    :return:
        mw : Estimated moment magnitude
        f0 : Source function corner frequency
        m0 : Scalar moment
        time_window : The assessed time window of P and S waves
    :rtype: tuple
    """
    if not picks:
        return None, None, None, None
    elif len(picks) == 1:
        new_picks = list()
        pick = picks[0]
        phase_name = pick.phase_hint[0:1]
        if pick_name != phase_name:
            raise SpectralMwException("Not set the '{}' wave_name".format(pick_name))
        if phase_name == 'P':  # Counting theoretical S wave
            new_picks.append(pick)
            new_picks.append(get_theoretical_s(pick, origin))
        elif phase_name == 'S':  # Counting theoretical P wave
            new_picks.append(get_theoretical_p(pick, origin, offset=-0.2))
            new_picks.append(pick)
        else:
            raise SpectralMwException('None S nor P wave_name')
        picks = new_picks
    if picks[0] is None:
        if pick_name != 'S':
            raise SpectralMwException("Not set the '{}' wave_name".format(pick_name))
        picks[0] = get_theoretical_p(picks[1], origin, offset=-0.2)
    if picks[1] is None:
        if pick_name != 'P':
            raise SpectralMwException("Not set the '{}' wave_name".format(pick_name))
        picks[1] = get_theoretical_s(picks[0], origin)
    if picks[0].phase_hint[0:1] != 'P':
        raise SpectralMwException("first phase '{}' is not P".format(picks[0].pick.phase_hint))
    if picks[1].phase_hint[0:1] != 'S':
        raise SpectralMwException("second phase '{}' is not S".format(picks[1].pick.phase_hint))

    if pick_name == 'P':
        mw, f0, m0, time_window, r = estimate_mw(signal, picks[0].time, picks[0:1], origin,
                                                 station_inventory, configuration)
    else:
        mw, f0, m0, time_window, r = estimate_mw(signal, picks[0].time, picks[1:2], origin,
                                                 station_inventory, configuration)
    return mw, f0, m0, time_window, r

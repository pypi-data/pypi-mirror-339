"""
Cumulated P and S phases spectral magnitude estimation
------------------------------------------------------

..
    :copyright:
        Jan Wiszniowski (jwisz@igf.edu.pl)
    :license:
        GNU Lesser General Public License, Version 3
        (https://www.gnu.org/copyleft/lesser.html)
    :version: 0.0.1
        2024-11-07

"""


from amw.mw.utils import get_theoretical_s, get_theoretical_p, SpectralMwException
from amw.mw.estimation import estimate_mw


def estimate_double_phase_mw(signal, picks, origin, station_inventory, configuration):
    """
    Estimates the moment magnitude on the signal covering both phases P and S together.

    :param signal:
        The signal is the 3D seismic displacement stream, which must cover both the P wave, the S wave,
        and the noise before the P onset.
    :type signal: ObsPy Stream
    :param picks:
        The list of two picks: P and S. The P wave_name is first the S wave_name is second.
        If the wave_name is missing there should be None value. At list one wave_name is required,
        but two picks P and S are recommended. At least one wave_name must be given. If the P or S wave_name is missing,
        the function tries to determine it based on the earthquake time at the focus and the remaining wave_name time.
    :type picks: list(ObsPy.Pick)
    :param origin:
        The event origin.
    :type origin: ObsPy Origin
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

    Uses functions :
        get_theoretical_s
        get_theoretical_p
        estimate_mw
    """
    # Checking phases
    if not picks:
        return None, None, None, None
    elif len(picks) == 1:
        new_picks = list()
        pick = picks[0]
        phase_name = pick.phase_hint[0:1]
        if phase_name == 'P':  # Counting theoretical S wave
            new_picks.append(pick)
            new_picks.append(get_theoretical_s(pick, origin))
        elif phase_name == 'S':  # Counting theoretical P wave
            new_picks.append(get_theoretical_p(pick, origin))
            new_picks.append(pick)
        else:
            raise SpectralMwException('None S nor P wave_name')
        picks = new_picks
    if picks[0] is None:
        picks[0] = get_theoretical_p(picks[1], origin)
    if picks[1] is None:
        picks[1] = get_theoretical_s(picks[0], origin)
    if picks[0].phase_hint[0:1] != 'P':
        raise SpectralMwException("first phase '{}' is not P".format(picks[0].pick.phase_hint))
    if picks[1].phase_hint[0:1] != 'S':
        raise SpectralMwException("second phase '{}' is not S".format(picks[1].pick.phase_hint))
    mw, f0, m0, time_window, r = estimate_mw(signal, picks[0].time, picks, origin, station_inventory, configuration)
    return mw, f0, m0, time_window, r

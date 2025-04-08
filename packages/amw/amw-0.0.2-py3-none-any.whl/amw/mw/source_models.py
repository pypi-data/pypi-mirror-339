"""
Seismic source models in frequency domain
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


class BoatwrightSourceModel(object):
    r"""
    The Boatwright (1978; 1980) seismic source model is:

    .. math::

        S\left(f|M_0,f_0\right)=
        {\frac{1}{2\pi f}M_0\left[{1+\left(\frac{f}{f_0}\right)}^{n\gamma}\right]}^\frac{-1}{\gamma},

    where :math:`M_0` is a scalar moment and :math:`f_0` is a cornel frequency. Constant values :math:`\gamma`
    and :math:`n` controls the sharpness of the corners of the spectrum. For :math:`\gamma = 1` and :math:`n = 2`,
    it is Brune (1970; 1971) source model:

    .. math::

        S\left(f|M_0,f_0\right)={\frac{1}{2\pi f}M_0\left[{1+\left(\frac{f}{f_0}\right)}^2\right]}^{-1}

    :param frequencies: The frequencies values, for w spectral function values will be computed
    :type frequencies: numpy array
    :param gamma:
    :param n:

    Default parameters gamma=1 and n=2 are for Brunea source model

    References:

    * Boatwright, J. (1978). Detailed spectral analysis of two small New York State earthquakes,
      Bull. Seism. Soc. Am. 68 (4), 1117–1131. https://doi.org/10.1785/BSSA0680041117
    * Boatwright, J. (1980). A spectral theory for circular seismic sources; simple estimates of source dimension,
      dynamic stress drop, and radiated seismic energy,
      Bull. Seism. Soc. Am. 70 (1), 1–27. https://doi.org/10.1785/BSSA0700010001
    * Brune, J. N. (1970). Tectonic stress and the spectra of seismic shear waves from earthquakes,
      J. Geophys. Res. 75, 4997-5009. https://doi.org/10.1029/JB075i026p04997
    * Brune, J.N. (1971) Correction [to "Tectonic Stress and the Spectra of Seismic Shear Waves from Earthquakes"],
      J. Geophys. Res. 76, 5002. http://dx.doi.org/10.1029/JB076i020p05002

    """
    def __init__(self, frequencies, gamma=1.0, n=2.0):
        """
        Default parameters gamma=1 and n=2 are for Brune source model
        """
        self.f = frequencies
        self.gamma = gamma
        self.n = n
        self.omega = 2.0 * np.pi * self.f

    def __call__(self, *args, **kwargs):
        """
        Return the frequency values of the source model for source model parameters

        Call example
        ------------
        from amw.mw.source_models import BoatwrightSourceModel
        source_model = BoatwrightSourceModel(np.arange(0.1, 20.0, 0.1))
        result = source_model(1.0e14, 1.5)

        :param args: Two source model parameters: moment scale and corner frequency
        :param kwargs:

        :return:

        """
        m0 = args[0]
        f0 = args[1]
        return np.divide(m0 * (1 + (self.f / f0) ** (self.n * self.gamma)) ** (-1.0 / self.gamma), self.omega)


class BruneSourceModel(BoatwrightSourceModel):
    r"""
    Brune (1970; 1971) seismic source model is:

    .. math::

        S\left(f|M_0,f_0\right)={\frac{1}{2\pi f}M_0\left[{1+\left(\frac{f}{f_0}\right)}^2\right]}^{-1},

    where :math:`M_0` is a scalar moment and :math:`f_0` is a corner frequency.

    :param frequencies: The frequencies values, for w spectral function values will be computed
    :type frequencies: numpy array

    """
    def __init__(self, frequencies):
        BoatwrightSourceModel.__init__(self, frequencies, gamma=1.0, n=2.0)


class HaskellSourceModel(object):
    r"""
     Haskell (1964) seismic source model is:

    .. math::

        S\left(f|M_0,f_0\right)=\frac{1}{2\pi f}M_0\text{sinc}\frac{f}{f0},

    where :math:`M_0` is a scalar moment and :math:`f_0` is a corner frequency.

    :param frequencies: The frequencies values, for w spectral function values will be computed
    :type frequencies: numpy array

    """
    def __init__(self, frequencies, gamma=1.0, n=2.0):
        self.f = frequencies
        self.omega = 2.0 * np.pi * self.f

    def __call__(self, *args, **kwargs):
        """
        Return the frequency values of the source model for source model parameters

        Call example
        ------------
        from amw.mw.source_models import HaskellSourceModel
        source_model = HaskellSourceModel(np.arange(0.1, 20.0, 0.1))
        result = source_model(1.0e14, 1.5)

        :param args: Two or three source model parameters: moment scale, first corner frequency,
            and second corner frequency
        :param kwargs:

        :return:

        """
        m0 = args[0]
        omega0_2 = 2.0 * np.pi * args[1]
        if len(args) > 2:
            f1 = args[1]
            raise "Two corner frequency Haskell has been not implemented yet"
        else:
            return np.abs(np.divide(m0 * np.sinc(self.f/omega0_2), self.omega))

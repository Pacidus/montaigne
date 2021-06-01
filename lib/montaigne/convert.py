from .consts import e, epsilon_0, kb, pi, Na

########################
# SI units -> Si units #
########################


def bjerrum(epsilon_r, T):
    """
    float * float -> float
    Hypothesis : T > 0 and (T, epsilon_r) in SI_units
    Return the value of the bjerrum length given
    the relative permitivity epsilon_r and the temperature of the medium.
    """
    return e * e / (4 * pi * epsilon_0 * epsilon_r * kb * T)


def debye(C_inf, bjerrum_length):
    """
    float * float -> float
    Hypothesis : C_inf and bjerrum_length >= 0 and in SI_units
    Return the value of the debye length given
    the density C_inf and the bjerrum length bjerrum_length
    """
    return 1 / (8 * pi * C_inf * bjerrum_length) ** 0.5


##############################
# SI units -> Lattices units #
##############################


def potential(V, T):
    """
    float * float -> float
    Hypothesis : T < 0 and (T, V) in SI_units
    Return the potential in lattices units
    """
    return V * e / (kb * T)

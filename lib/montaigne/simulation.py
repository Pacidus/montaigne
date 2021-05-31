"""This is the simulation module

This module create a class that runs simultaion through laboetie
"""

__all__ = ["simulation"]
__version__ = "0.0.0"
__author__ = "Yohan Duarte : pacidus@gmail.com"


import numpy as np
import tarfile as tar
import tempfile as tp
from subprocess import run, DEVNULL
from secrets import token_urlsafe
from .misc import lbin, phin
from .parsers import write_infile, read_infile, ph2lb

##############
# Main class #
##############


class simulation:
    """Class simulation,
    Use to run a simulation through laboethie.
    Save the results into a tar file.
    """

    def __init__(self, laboethie_folder_path, save_path, name_sim=None):
        """Initialisation :
	str -> simulation
	Hypothesis : laboethie_folder_path is a valid path
	    and laboetie executable is in it.
        Construct the simulation object.
	"""

        # Initialise all the paths we need
        self.Lpath = laboethie_folder_path
        self.epath = f"{self.Lpath}/laboetie"
        self.opath = f"{self.Lpath}/output"
        self.lbpath = f"./lb.in"
        self.spath = save_path

        if name_sim is None:
            # If we dont have name for the result file
            # we ensure non overlapping by a random name
            # 3 bytes token encoded in base 64 (4 char long)
            # 3 bytes -> 256**3 -> 16777216 differents names
            # if the number of file < 1e3 then P(overlapping) < 6e-5
            # therefore we dont need to check if the file already exist
            self.nsim = token_urlsafe(3)
            self.token = True
        else:
            self.nsim = name_sim
            self.token = False

        self.lbin = lbin
        self.phin = phin

    def gen_lbin(self):
        """ gen_lbin
	None -> None
	Hypothesis : self.lbin as valid entries for laboetie
        generate the lb.in file given the lbin dictionary
        """

        write_infile(self.lbin, self.lbpath)

    def phy2lat(self):
        """phy2lat
	None -> None
	Hypothesis : ø
        convert physical units into lattices units
        """

        self.lbin = ph2lb(self.phin)

    def run(self, quiet=False):
        """run
        None -> None
        Hypothesis : lbin is correct
        run the simulation given the lbin input
        """

        self.gen_lbin()

        if quiet:
            run(self.epath, stdout=DEVNULL)
        else:
            run(self.epath)

"""This is the simulation module

This module create a class that runs simultaion through laboetie
"""

__all__ = ["simulation"]
__author__ = "Yohan Duarte : pacidus@gmail.com"


import numpy as np
import tarfile as tar
import tempfile as tp

from secrets import token_urlsafe
from subprocess import run, DEVNULL

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
        self.opath = f"./output"
        self.lbpath = f"./lb.in"
        self.spath = save_path
        self.nrun = 0
        if name_sim is None:
            # If we dont have name for the result file
            # we ensure non overlapping by a random name
            # 3 bytes token encoded in base 64 (4 char long)
            # 3 bytes -> 256**3 -> 16777216 differents names
            # if the number of file < 1e3 then P(overlapping) < 6e-5
            # therefore we dont need to check if the file already exist
            self.nsim = f"Sim_{token_urlsafe(3)}"
        else:
            self.nsim = name_sim

        self.tar = tar.open(f"{self.spath}/{self.nsim}.tar.gz", "w:gz")
        self.lbin = lbin
        self.phin = phin

    def __del__(self):
        """Destroy
        ensure to destroy propely simulation
        """
        self.tar.close()

    def gen_lbin(self):
        """gen_lbin
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

    def save_sim(self, name=None):
        """save_sim
        (str) -> None
        Hypothesis : name is a valid folder name
        save the sim into the tar simulation set
        """

        # Add the output repertory and name it raw_output in the archive
        self.tar.add(self.opath, arcname=f"sim_{self.nrun}/raw_output")

        # Create a temporary file
        # the use is to modify and save new data files
        with tp.NamedTemporaryFile() as outfile:

            # Write a "clean" version of the input file
            write_infile(self.lbin, outfile.name)
            addnamedtemp(outfile, self.tar, f"{self.opath}/inputs")

            # Write a "clean" version of the phi file
            phi = np.loadtxt(f"{labout}/phi.dat")
            np.savetxt(
                outfile,
                phi,
                header="Electrostatic potential \nz [in nodes]    V [beta e phi]",
            )
            addnamedtemp(outfile, self.tar, f"{self.opath}/data/phi.dat")

            # Write a "clean" version of the charges distributions
            Chations = np.loadtxt(f"{labout}/pnp_avg_phi_cp_cm_vs_z.dat")
            np.savetxt(
                outfile,
                Chations,
                header="Mean values of V, C+, C- given z \nz [in nodes]    V, C+, C-",
            )
            addnamedtemp(outfile, self.tar, f"{self.opath}/data/mean_charges.dat")

            self.nrun += 1


#################
# Def functions #
#################


def addnamedtemp(ntemp, tarfile, name):
    """addnamedtemp
    NamedTemporaryFile * tar.open -> None
    Hypothesis : ø
    add the temporary named file in the tarfile
    """
    # Only needed here to simulate closing & reopening file
    ntemp.file.seek(0)

    # Save the clean input file
    tf.add(outfile.name, arcname=name)

from __future__ import print_function, division

import numpy as np

# Import sile objects
from ..sile import add_sile, Sile_fh_open
from .sile import *
from sisl.unit.siesta import unit_convert


__all__ = ['fcSileSiesta']


class fcSileSiesta(SileSiesta):
    """ Force constants Siesta file object """

    @Sile_fh_open
    def read_force(self, displacement=None, na=None):
        """ Reads all displacement forces by multiplying with the displacement value

        Since the force constant file does not contain the non-displaced configuration
        this will only return forces on the displaced configurations minus the forces from
        the non-displaced configuration.

        Parameters
        ----------
        displacement : float, optional
           the used displacement in the calculation, since Siesta 4.1-b4 this value
           is written in the FC file and hence not required.
           If prior Siesta versions are used and this is not supplied the 0.04 Bohr displacement
           will be assumed.
        na : int, optional
           number of atoms (for returning correct number of atoms), since Siesta 4.1-b4 this value
           is written in the FC file and hence not required.
           If prior Siesta versions are used then the file is expected to only contain 1-atom displacement.

        Returns
        -------
        forces : numpy.ndarray with 4 dimensions containing all the forces. The 2nd dimensions contains
                 -x/+x/-y/+y/-z/+z displacements.
        """
        if displacement is None:
            line = self.readline().split()
            self.fh.seek(0)
            try:
                displacement = float(line[-1])
            except:
                displacement = 0.04 * unit_convert('Bohr', 'Ang')

        return - self.read_force_constant(na) * displacement

    @Sile_fh_open
    def read_force_constant(self, na=None):
        """ Reads the force-constant stored in the FC file

        Parameters
        ----------
        na : int, optional
           number of atoms in the unit-cell

        Returns
        -------
        force constants : numpy.ndarray with 4 dimensions containing all the forces. The 2nd dimensions contains
                          -x/+x/-y/+y/-z/+z displacements.
        """
        # Force constants matrix
        line = self.readline().split()
        if na is None:
            try:
                na = int(line[-2])
            except:
                na = None

        fc = list()
        while True:
            line = self.readline()
            if line == '':
                # empty line or nothing
                break
            fc.append(list(map(float, line.split())))

        # Units are already eV / Ang ** 2
        fc = np.array(fc)
        # Slice to correct size
        if na is None:
            na = fc.size // 6 // 3
        fc.shape = (-1, 6, na, 3)
        return fc

add_sile('FC', fcSileSiesta, case=False, gzip=True)
add_sile('FCC', fcSileSiesta, case=False, gzip=True)

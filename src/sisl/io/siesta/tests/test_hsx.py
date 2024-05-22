# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from __future__ import annotations

import os.path as osp
import re
import warnings

import numpy as np
import pytest

import sisl

pytestmark = [pytest.mark.io, pytest.mark.siesta]


def si_pdos_kgrid_geom(with_orbs=True):
    if with_orbs:
        return sisl.geom.diamond(5.43, sisl.Atom("Si", R=np.arange(13) + 1))
    return sisl.geom.diamond(5.43, sisl.Atom("Si"))


def test_si_pdos_kgrid_hsx_H(sisl_files, sisl_tmp):
    si = sisl.get_sile(sisl_files("siesta", "Si_pdos_k", "Si_pdos.HSX"))
    si.read_hamiltonian(geometry=si_pdos_kgrid_geom())


def test_si_pdos_kgrid_hsx_H(sisl_files, sisl_tmp):
    si = sisl.get_sile(sisl_files("siesta", "Si_pdos_k", "Si_pdos.fdf"))
    si.read_hamiltonian(order="HSX")


def test_si_pdos_kgrid_hsx_H_no_geometry(sisl_files, sisl_tmp):
    si = sisl.get_sile(sisl_files("siesta", "Si_pdos_k", "Si_pdos.HSX"))
    H0 = si.read_hamiltonian()
    H1 = si.read_hamiltonian(geometry=si_pdos_kgrid_geom())
    assert H0._csr.spsame(H1._csr)


def test_si_pdos_kgrid_hsx_H_fix_orbitals(sisl_files, sisl_tmp):
    si = sisl.get_sile(sisl_files("siesta", "Si_pdos_k", "Si_pdos.HSX"))
    si.read_hamiltonian(geometry=si_pdos_kgrid_geom(False))


def test_si_pdos_kgrid_hsx_overlap(sisl_files, sisl_tmp):
    si = sisl.get_sile(sisl_files("siesta", "Si_pdos_k", "Si_pdos.HSX"))
    HS = si.read_hamiltonian(geometry=si_pdos_kgrid_geom())
    S = si.read_overlap(geometry=si_pdos_kgrid_geom(False))

    assert HS._csr.spsame(S._csr)
    assert np.allclose(HS._csr._D[:, HS.S_idx], S._csr._D[:, 0])


def test_h2o_dipole_hsx_no_geometry(sisl_files, sisl_tmp):
    HSX = sisl.get_sile(sisl_files("siesta", "H2O_dipole", "h2o_dipole.HSX"))
    geometry = sisl.get_sile(
        sisl_files("siesta", "H2O_dipole", "h2o_dipole.fdf")
    ).read_geometry()
    # manually define this.
    geometry.set_nsc(a=5, b=1, c=3)
    HS = HSX.read_hamiltonian()
    S = HSX.read_overlap(geometry=geometry)

    assert HS._csr.spsame(S._csr)
    assert np.allclose(HS._csr._D[:, HS.S_idx], S._csr._D[:, 0])


def test_h2o_dipole_hsx(sisl_files, sisl_tmp):
    HSX = sisl.get_sile(sisl_files("siesta", "H2O_dipole", "h2o_dipole.HSX"))
    geometry = sisl.get_sile(
        sisl_files("siesta", "H2O_dipole", "h2o_dipole.fdf")
    ).read_geometry()
    geometry.set_nsc(a=5, b=1, c=3)
    # reading from hsx just requires atoms + coordinates + nsc
    HS = HSX.read_hamiltonian(geometry=geometry)
    S = HSX.read_overlap(geometry=geometry)

    assert HS._csr.spsame(S._csr)
    assert np.allclose(HS._csr._D[:, HS.S_idx], S._csr._D[:, 0])


def test_h2o_dipole_hsx_hs_no_geometry(sisl_files, sisl_tmp):
    HSX = sisl.get_sile(sisl_files("siesta", "H2O_dipole", "h2o_dipole.HSX"))
    HS = HSX.read_hamiltonian()
    S = HSX.read_overlap()


def test_h2o_dipole_hsx_no_ef(sisl_files, sisl_tmp):
    HSX = sisl.get_sile(sisl_files("siesta", "H2O_dipole", "h2o_dipole.HSX"))
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        Ef = HSX.read_fermi_level()


def test_si_pdos_kgrid_hsx_versions(sisl_files, sisl_tmp):
    HSX0 = sisl.get_sile(sisl_files("siesta", "ancient", "si_pdos_kgrid.0.HSX"))
    assert HSX0.version == 0
    HSX1 = sisl.get_sile(sisl_files("siesta", "ancient", "si_pdos_kgrid.1.HSX"))
    assert HSX1.version == 1

    HS0 = HSX0.read_hamiltonian()
    HS1 = HSX1.read_hamiltonian()
    Ef = HSX1.read_fermi_level()
    # HSX0 does not shift, whereas HSX1 does shift
    HS1.shift(Ef)
    assert HS0._csr.spsame(HS1._csr)
    # assert np.allclose(HS0._csr._D, HS1._csr._D)


def test_si_pdos_kgrid_hsx_versions_s(sisl_files, sisl_tmp):
    HSX0 = sisl.get_sile(sisl_files("siesta", "ancient", "si_pdos_kgrid.0.HSX"))
    assert HSX0.version == 0
    HSX1 = sisl.get_sile(sisl_files("siesta", "ancient", "si_pdos_kgrid.1.HSX"))
    assert HSX1.version == 1

    HS0 = HSX0.read_hamiltonian()
    S0 = HSX0.read_overlap()
    HS1 = HSX1.read_hamiltonian()
    S1 = HSX1.read_overlap()
    assert HS0._csr.spsame(S1._csr)
    assert S0._csr.spsame(HS1._csr)

    assert np.allclose(HS0._csr._D[:, HS0.S_idx], S0._csr._D[:, 0])
    assert np.allclose(HS1._csr._D[:, HS1.S_idx], S1._csr._D[:, 0])


def test_si_pdos_kgrid_hsx_1_same_tshs(sisl_files, sisl_tmp):
    HSX = sisl.get_sile(sisl_files("siesta", "Si_pdos_k", "Si_pdos.HSX"))
    TSHS = sisl.get_sile(sisl_files("siesta", "Si_pdos_k", "Si_pdos.TSHS"))

    HSX = HSX.read_hamiltonian()
    TSHS = TSHS.read_hamiltonian()

    gx = HSX.geometry
    gt = TSHS.geometry
    assert np.allclose(gx.lattice.cell, gt.lattice.cell)
    assert np.allclose(gx.xyz, gt.xyz)
    assert np.allclose(gx.nsc, gt.nsc)

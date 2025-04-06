import macromol_dataframe as mmdf
import macromol_voxelize as mmvox
import numpy as np
import parametrize_from_file as pff
import pytest

from visible_residues import sample_visible_residues, Sphere
from polars.testing import assert_frame_equal
from pathlib import Path

CIF_DIR = Path(__file__).parent / 'resources'

def grid(params):
    return mmvox.Grid(
            length_voxels=1,
            resolution_A=float(params['length_A']),
            center_A=np.array(eval(params['center_A'])),
    )

def bounding_sphere(params):
    return Sphere(
            center_A=np.array(eval(params['center_A'])),
            radius_A=float(params['radius_A']),
    )


@pytest.mark.parametrize('n', [0, 1, 2])
@pff.parametrize(
        schema=pff.cast(
            grid=grid,
            sphere=bounding_sphere,
            expected=eval,
        ),
)
def test_sample_visible_residues(n, grid, sphere, expected):
    # I deliberately constructed this amino acid structure so that the global 
    # and residue-local coordinate frames are the same, to make it easy to 
    # reason about the expected results.

    atoms = mmdf.read_asymmetric_unit(CIF_DIR / 'axis_aligned_residue.cif')
    atoms = mmdf.assign_residue_ids(atoms)

    visible = sample_visible_residues(
            rng=np.random.default_rng(0),
            atoms=atoms,
            grid=grid,
            n=n,
            bounding_sphere=sphere,
    )
    assert len(visible) == min(expected, n)

def test_sample_visible_residues_4rek_G49():
    # This is a residue with two completely separate backbone conformations.  
    # The A conformation has 69% occupancy, so it should always be used, 
    # regardless of the actual order of the atoms in the input file.  We test 
    # by comparing to a file with only the A conformation.

    def sample_visible(alt_ids):
        atoms = mmdf.read_asymmetric_unit(CIF_DIR / f'4rek_G49_{alt_ids}.cif')
        atoms = mmdf.assign_residue_ids(atoms, maintain_order=True)

        # We're not trying to exclude any atoms in this test, so the grid just 
        # needs to fit everything.
        grid = mmvox.Grid(
                length_voxels=15,
                resolution_A=1.0,
                center_A=np.array([0, -5, 30]),
        )

        return sample_visible_residues(
                rng=np.random.default_rng(0),
                atoms=atoms,
                grid=grid,
                n=1,
        )

    visible_A = sample_visible('A')
    visible_AB = sample_visible('AB')
    visible_BA = sample_visible('BA')

    assert len(visible_A) == 1
    assert len(visible_AB) == 1
    assert len(visible_BA) == 1

    assert_frame_equal(visible_A, visible_AB)
    assert_frame_equal(visible_A, visible_BA)

def test_sample_visible_residues_4rek_M154():
    # This is a residue with three Cα conformations, but only one N/C 
    # conformation.  The A conformation has 62% occupancy, so it should always 
    # be used, regardless of the actual order of the atoms in the input file.  
    # We test by comparing to a file with only the A conformation.

    def sample_visible(alt_ids):
        atoms = mmdf.read_asymmetric_unit(CIF_DIR / f'4rek_M154_{alt_ids}.cif')
        atoms = mmdf.assign_residue_ids(atoms, maintain_order=True)

        # We're not trying to exclude any atoms in this test, so the grid just 
        # needs to fit everything.
        grid = mmvox.Grid(
                length_voxels=15,
                resolution_A=1.0,
                center_A=np.array([25, -15, 20]),
        )

        return sample_visible_residues(
                rng=np.random.default_rng(0),
                atoms=atoms,
                grid=grid,
                n=1,
        )

    visible_A = sample_visible('A')
    visible_ABC = sample_visible('ABC')
    visible_CBA = sample_visible('CBA')

    assert len(visible_A) == 1
    assert len(visible_ABC) == 1
    assert len(visible_CBA) == 1

    assert_frame_equal(visible_A.drop('alt_ids'), visible_ABC.drop('alt_ids'))
    assert_frame_equal(visible_A.drop('alt_ids'), visible_CBA.drop('alt_ids'))
    assert_frame_equal(visible_ABC, visible_CBA)

@pytest.mark.parametrize('n', [0, 1, 2, 3, 4, 5])
def test_sample_visible_residues_1lz1(n):
    # The purpose of this test is to make sure that `find_visible_residues` 
    # produces qualitatively reasonable results on a real protein structure.  

    atoms = mmdf.read_asymmetric_unit(CIF_DIR / '1lz1.cif')
    atoms = mmdf.assign_residue_ids(atoms, maintain_order=True)

    grid = mmvox.Grid(length_voxels=15, resolution_A=1.0)

    visible = sample_visible_residues(
            rng=np.random.default_rng(0),
            atoms=atoms,
            grid=grid,
            n=n,
    )
    visible = visible.join(
            atoms.group_by('residue_id', 'seq_id').agg(),
            on='residue_id',
    )

    # These expected sequence ids are based on a manual inspection, see 
    # `resources/1lz1_notes.xlsx` for details.
    assert len(visible) == min(n, 3)
    assert set(visible['seq_id']) <= {35, 57, 96}

@pytest.mark.parametrize('n', [0, 1])
def test_sample_visible_residues_1bna(n):
    # This structure doesn't contain any amino acid residues, but that 
    # shouldn't cause any problems.

    atoms = mmdf.read_asymmetric_unit(CIF_DIR / '1bna.cif')
    atoms = mmdf.assign_residue_ids(atoms, maintain_order=True)

    grid = mmvox.Grid(length_voxels=15, resolution_A=1.0)

    visible = sample_visible_residues(
            rng=np.random.default_rng(0),
            atoms=atoms,
            grid=grid,
            n=n,
    )
    assert len(visible) == 0


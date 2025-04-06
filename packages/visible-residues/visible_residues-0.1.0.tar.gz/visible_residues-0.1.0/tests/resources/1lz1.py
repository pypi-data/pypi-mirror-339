import macromol_voxelize as mmvox
import macromol_dataframe as mmdf
import numpy as np

atoms = mmdf.read_asymmetric_unit('1lz1.cif')
atoms = mmvox.set_atom_radius_A(atoms, 0.5)
atoms = mmvox.set_atom_channels_by_element(atoms, [['C'], ['N'], ['O'], ['S']])

img_params = mmvox.ImageParams(
        channels=4,
        grid=mmvox.Grid(
            length_voxels=15,
            resolution_A=1,
        ),
)

img, img_atoms = mmvox.image_from_atoms(atoms, img_params)
np.save('1lz1_15A.npy', img)



import polars as pl

from macromol_dataframe.pymol import set_ascii_dataframe_format
from pymol import cmd, cgo

set_ascii_dataframe_format()

def show_bounding_spheres_cgo(path, radius=4):
    df = pl.read_parquet(path)
    print(df)

    cmd.set('transparency_mode', 1)
    cmd.delete('bounding_spheres')

    #spheres = ['ALPHA', 0.5]
    spheres = []

    for row in df.iter_rows(named=True):
        spheres += [cgo.SPHERE, row['x'], row['y'], row['z'], float(radius)]

    cmd.load_cgo(spheres, 'bounding_spheres')

cmd.extend('show_bounding_spheres_cgo', show_bounding_spheres_cgo)
cmd.auto_arg[0]['show_bounding_spheres_cgo'] = cmd.auto_arg[1]['load']

def show_bounding_spheres_pseudoatom(path):
    df = pl.read_parquet(path)
    print(df)

    cmd.delete('bound')

    for row in df.iter_rows(named=True):
        cmd.pseudoatom(
                'bound',
                resi=row['seq_id'],
                chain=row['chain_id'],
                segi=row['chain_id'],
                pos=[row['x'], row['y'], row['z']],
        )

cmd.extend('show_bounding_spheres_pseudoatom', show_bounding_spheres_pseudoatom)
cmd.auto_arg[0]['show_bounding_spheres_pseudoatom'] = cmd.auto_arg[1]['load']

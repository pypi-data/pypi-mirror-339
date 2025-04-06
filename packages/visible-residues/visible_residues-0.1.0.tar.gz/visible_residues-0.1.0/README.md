Visible Residues
================

[![Last release](https://img.shields.io/pypi/v/visible_residues.svg)](https://pypi.python.org/pypi/visible_residues)
[![Python version](https://img.shields.io/pypi/pyversions/visible_residues.svg)](https://pypi.python.org/pypi/visible_residues)
[![Documentation](https://img.shields.io/readthedocs/visible_residues.svg)](https://visible-residues.readthedocs.io/en/latest/)
[![Test status](https://img.shields.io/github/actions/workflow/status/kalekundert/visible_residues/test.yml?branch=master)](https://github.com/kalekundert/visible_residues/actions)
[![Test coverage](https://img.shields.io/codecov/c/github/kalekundert/visible_residues)](https://app.codecov.io/github/kalekundert/visible_residues)
[![Last commit](https://img.shields.io/github/last-commit/kalekundert/visible_residues?logo=github)](https://github.com/kalekundert/visible_residues)

This is an extension module implementing one performance-critical function used 
to create a machine learning dataset of 3D images of macromolecules with 
labeled amino acid identities.  Specifically, the function accepts a dataframe 
of atoms in the image, then samples a fixed number of residues whose sidechains 
are likely to be mostly within the image.  To avoid biasing the samples based 
on the specific sidechains involved (e.g. glycine has a smaller sidechain than 
arginine, so it might be sampled more often if the actual sidechain was 
considered), this "within the image" determination is based entirely on 
backbone coordinates.

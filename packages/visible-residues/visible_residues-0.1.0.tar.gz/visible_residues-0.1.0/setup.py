from setuptools import setup
from pybind11.setup_helpers import Pybind11Extension

setup(
        ext_modules=[
            Pybind11Extension(
                name='visible_residues._inner_loop',
                sources=[
                    'src/_inner_loop.cc',
                ],
                include_dirs=[
                    'src/vendored/eigen',
                ],
                cxx_std=14,
            ),
        ],
)

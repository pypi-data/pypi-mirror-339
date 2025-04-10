from setuptools import setup, Extension
import os

# Set compiler to g++
os.environ['CC'] = 'g++'

this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

# Define the extensions
extensions = [
    Extension(
        name="gpr_calc.kernels._dot_kernel",
        sources=["gpr_calc/kernels/dot_kernel.cpp"],  # Path to your C++ source files
        include_dirs=["gpr_calc/kernels"],  # Include path for header files
        libraries=[],  # List any external libraries here if necessary
        extra_compile_args=['-O2'],  # Any specific compiler options you may need
    ),
    Extension(
        name="gpr_calc.kernels._rbf_kernel",
        sources=["gpr_calc/kernels/rbf_kernel.cpp"],  # Path to your C++ source files
        include_dirs=["gpr_calc/kernels"],  # Include path for header files
        libraries=[],  # List any external libraries here if necessary
        extra_compile_args=['-O2'],  # Any specific compiler options you may need
    ),
]

setup(
    name="gpr_calc",
    version="0.0.6",
    description="GPR",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=[
        "gpr_calc",
        "gpr_calc.kernels",
    ],

    package_data={
        "gpr_calc.kernels": ["*.cpp", "*.h", "*.so", "*.py"]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "cffi>=1.0.0",
        "mpi4py>=3.0.3",
        "ase>=3.23.0",
        "pyxtal>=1.0.5",
    ],
    python_requires=">=3.9.1",
    license="MIT",
    ext_modules=extensions,  # Add compiled extensions to the setup
    cffi_modules=[
        "gpr_calc/kernels/libdot_builder.py:ffibuilder",
        "gpr_calc/kernels/librbf_builder.py:ffibuilder"
    ],
)

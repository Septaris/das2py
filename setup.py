import os
import os.path
import sys

import numpy
from setuptools import Extension, setup

das2c_lib_dir = os.getenv("DAS2C_LIBDIR")
das2c_inc_dir = os.getenv("DAS2C_INCDIR")

ext_library_inc = os.getenv("LIBRARY_INC", None) 
ext_library_lib = os.getenv("LIBRARY_LIB", None) 
	
lDefs = []

if das2c_lib_dir: lib_dirs = [das2c_lib_dir]
else: lib_dirs = []

if ext_library_lib:
	lib_dirs.append(ext_library_lib)

if das2c_inc_dir: lib_incs = [das2c_inc_dir, numpy.get_include()]
else: lib_incs = [numpy.get_include()]

if ext_library_inc:
	lib_incs.append(ext_library_inc)

lib_src = ["src/_das2.c"]

if sys.platform.lower().startswith('sunos'):
	ext = Extension(
		"_das2", sources=lib_src, include_dirs=lib_incs, define_macros=lDefs
		,library_dirs=lib_dirs, libraries=["das2.3","fftw3", "expat", 
		                                   "ssl", "crypto", "z"]
		,extra_compile_args=["-xc99"]
	)
elif sys.platform == 'win32':
	print("setup.py: Using Headers from %s"%lib_incs)
	print("setup.py: Using Libs from %s"%lib_dirs)
	ext = Extension(
		"_das2", sources=lib_src, include_dirs=lib_incs, define_macros=lDefs
		,library_dirs=lib_dirs, 
        libraries=[
            "libdas2.3", "fftw3", "expat", "libssl", "libcrypto",
            "zlib", "pthreadVC3", "ws2_32", "gdi32", "advapi32", "crypt32", "user32"
		]
        ,extra_objects=['%s/libdas2.3.lib'%das2c_lib_dir]
	)

else:
	ext = Extension(
		"_das2", sources=lib_src, include_dirs=lib_incs, define_macros=lDefs
		,library_dirs=lib_dirs
        ,libraries=["fftw3", "expat", "ssl", "crypto", "z"]
		,extra_compile_args=['-std=c99', '-ggdb', '-O0']
        ,extra_objects=['%s/libdas2.3.a'%das2c_lib_dir]
	)


setup(description="Das2 extensions for python",
	name="das2py",
	version="2.3.2",
	ext_modules=[ ext ],
	packages=['das2'],
	author="Chris Piker",
	author_email="chris-piker@uiowa.edu",
	url="https://das2.org/das2py"
)

FROM hripko/vcpkg:vs19

# Use powershell by default
SHELL ["powershell.exe", "-ExecutionPolicy", "Bypass", "-Command"]

# install das2C/das2py dependencies
RUN vcpkg install openssl fftw3 zlib expat pthreads --triplet x64-windows-static

# clone the das2C repository
RUN git clone https://github.com/das-developers/das2C.git

# setup en vars for the build
ENV N_ARCH="/"
ENV DAS2C="C:/das2C"
ENV LIBRARY_INC="C:/vcpkg/installed/x64-windows-static/include"
ENV LIBRARY_LIB="C:/vcpkg/installed/x64-windows-static/lib"
ENV LIBRARY_PREFIX="C:/opt"
ENV VC_VARS_PATH="C:/Program Files (x86)/Microsoft Visual Studio/2019/BuildTools/VC/Auxiliary/Build/vcvars64.bat"

# Which python version to use
ENV PYVER=3.6.8
ENV PYTHON_VERSION=python${PYVER}

# add the invoke script used to setup the path for nmake.exe, cl.exe, etc. (x64) 
# TODO: add building tools directle to the path to avoid the setup before each nmake  
ADD docker/windows/invoke_environment.ps1 scripts/invoke_environment.ps1
WORKDIR $DAS2C
RUN . C:/scripts/invoke_environment.ps1; \
 invoke_environment $env:VC_VARS_PATH ; \
 nmake.exe /nologo /f makefiles\Windows.mak build


# Where to find the das2C static library for the python build
ENV DAS2C_INCDIR=$DAS2C
ENV DAS2C_LIBDIR=$DAS2C/build.windows

# Where you want to install the files
ENV INST_HOST_LIB="C:/opt/lib/${PYTHON_VERSION}"
ENV INST_EXT_LIB="C:/opt/lib/${PYTHON_VERSION}"

# install the specified version of python
RUN choco install -y python --version $env:PYVER
RUN python -m pip install -U pip
RUN python -m pip install -U setuptools numpy matplotLib wheel

# add the das2py files to the container
WORKDIR C:/
ADD . das2py 

WORKDIR C:/das2py

# Build and test
RUN . C:/scripts/invoke_environment.ps1; \
 invoke_environment $env:VC_VARS_PATH ; \
 nmake.exe /nologo /f makefiles/Windows.mak build

# RUN . C:/scripts/invoke_environment.ps1; \
#  invoke_environment $env:VC_VARS_PATH ; \
#  nmake.exe /nologo /f makefiles/Windows.mak run_test


# the wheel is generated here: C:/das2py/dist/das2py-2.3.2-cp36-cp36m-win_amd64.whl
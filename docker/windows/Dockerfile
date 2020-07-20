FROM babouh/das2c:windows

# Which python version to use (3.6.8 by default)
ARG PYVER=3.6.8
ENV PYTHON_VERSION=python${PYVER}

# Where to find the das2C static library for the python build
ENV DAS2C_INCDIR=$DAS2C
ENV DAS2C_LIBDIR=$DAS2C/build.windows

# install the specified version of python
RUN choco install -y python --version $env:PYVER
RUN python -m pip install -U pip
RUN python -m pip install -U setuptools numpy matplotLib wheel

# add the das2py files to the container
WORKDIR C:/
ADD . das2py 

WORKDIR C:/das2py

# build 
RUN . C:/scripts/invoke_environment.ps1; \
 invoke_environment $env:VC_VARS_PATH ; \
 nmake.exe /nologo /f makefiles/Windows.mak build

# the wheel is generated here: C:/das2py/dist/das2py-2.3.2-cp36-cp36m-win_amd64.whl
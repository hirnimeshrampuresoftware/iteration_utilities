#!/bin/bash
set -e -x

# Compile wheels
if [ `uname -m` == "i686" ]; then
   /opt/python/cp35-cp35m/bin/pip install pip
   /opt/python/cp35-cp35m/bin/pip install setuptools wheel
   /opt/python/cp35-cp35m/bin/pip wheel /io/ -w wheelhouse/
fi

/opt/python/cp36-cp36m/bin/pip install pip
/opt/python/cp36-cp36m/bin/pip install setuptools wheel
/opt/python/cp36-cp36m/bin/pip wheel /io/ -w wheelhouse/

/opt/python/cp37-cp37m/bin/pip install pip
/opt/python/cp37-cp37m/bin/pip install setuptools wheel
/opt/python/cp37-cp37m/bin/pip wheel /io/ -w wheelhouse/

/opt/python/cp38-cp38/bin/pip install pip
/opt/python/cp38-cp38/bin/pip install setuptools wheel
/opt/python/cp38-cp38/bin/pip wheel /io/ -w wheelhouse/

/opt/python/cp39-cp39/bin/pip install pip
/opt/python/cp39-cp39/bin/pip install setuptools wheel
/opt/python/cp39-cp39/bin/pip wheel /io/ -w wheelhouse/

# Bundle external shared libraries into the wheels
for whl in wheelhouse/*.whl; do
    auditwheel repair "$whl" --plat $PLAT -w /io/wheelhouse/
done

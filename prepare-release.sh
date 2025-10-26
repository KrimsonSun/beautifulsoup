# A script to automatically create and test source and wheel
# distributions of Beautiful Soup.

# Recommend you run these steps one at a time rather than just running
# the script.

# If you screwed up on the test server and have to create a "a" or "b"
# release the second time, add the '--pre' argument to pip install to
# find the 'prerelease'.

# At some point I'll become confident enough with hatch and tox
# that it won't be necessary to do so many install and test steps.

# First, change the version number in
#  CHANGELOG
#  bs4/__init__.py
#  doc/index.rst

pyenv activate bs4-test
hatch clean
tox run-parallel

# Build sdist and wheel.
hatch build

# Test the sdist locally.
rm -rf ../py3-install-test-virtualenv
pyenv virtualenv 3.12.2 py3-install-test-virtualenv
pyenv activate py3-install-test-virtualenv
pip install dist/beautifulsoup4-*.tar.gz pytest lxml html5lib soupsieve
python -m pytest ~/.pyenv/versions/3.12.2/envs/py3-install-test-virtualenv/lib/python3.12/site-packages/bs4/tests
echo "EXPECT HTML ON LINE BELOW"
(cd .. && python --version && python -c "from bs4 import _s, __version__; print(__version__, _s('<a>foo', 'lxml'))")
# That should print something like:
# Python 3.12.2
# [new version number] <a>foo</a>


# Test the wheel locally.
pip uninstall beautifulsoup4
pip install dist/beautifulsoup4-*.whl
echo "EXPECT HTML ON LINE BELOW"
(cd .. && python --version && python -c "from bs4 import _s, __version__; print(__version__, _s('<a>foo', 'lxml'))")

pyenv deactivate
pyenv virtualenv-delete py3-install-test-virtualenv

# Upload to test pypi
pyenv activate bs4-test
hatch publish -r test

# Test install from test pypi.
rm -rf ../py3-install-test-virtualenv
virtualenv -p /usr/bin/python3 ../py3-install-test-virtualenv
source ../py3-install-test-virtualenv/bin/activate
pip install pytest lxml html5lib

# First, install from source and run the tests.
pip install -i https://testpypi.python.org/pypi beautifulsoup4 --extra-index-url=https://pypi.python.org/pypi --no-binary beautifulsoup4
python -m pytest ../py3-install-test-virtualenv/lib/python3.11/site-packages/bs4/tests/
echo "EXPECT HTML ON LINE BELOW"
(cd .. && which python && python -c "from bs4 import _s, __version__; print(__version__, _s('<a>foo', 'lxml'))")
# That should print something like:
# /home/.../py3-install-test-virtualenv/bin/python
# [new version number] <a>foo</a>

# Next, install the wheel and just test functionality.
pip uninstall beautifulsoup4
pip install -i https://testpypi.python.org/pypi beautifulsoup4 --extra-index-url=https://pypi.python.org/pypi
echo "EXPECT HTML ON LINE BELOW"
(cd .. && which python && python -c "from bs4 import _s, __version__; print(__version__, _s('<a>foo', 'lxml'))")
# That should print something like:
# /home/.../py3-install-test-virtualenv/bin/python
# [new version number] <a>foo</a>

deactivate
rm -rf ../py3-install-test-virtualenv

# Upload to production pypi
hatch publish

# Test install from production pypi

# First, from the source distibution
rm -rf ../py3-install-test-virtualenv
virtualenv -p /usr/bin/python3 ../py3-install-test-virtualenv
source ../py3-install-test-virtualenv/bin/activate
pip install pytest lxml html5lib beautifulsoup4 --no-binary beautifulsoup4
python -m pytest ../py3-install-test-virtualenv/lib/python3.11/site-packages/bs4/tests/
echo "EXPECT HTML ON LINE BELOW"
(cd .. && which python && python -c "from bs4 import _s, __version__; print(__version__, _s('<a>foo', 'html.parser'))")
# That should print something like:
# /home/.../py3-install-test-virtualenv/bin/python
# [new version number] <a>foo</a>

# Next, from the wheel
pip uninstall beautifulsoup4
pip install beautifulsoup4
echo "EXPECT HTML ON LINE BELOW"
(cd .. && which python && python -c "from bs4 import _s, __version__; print(__version__, _s('<a>foo', 'html.parser'))")
# That should print something like:
# /home/.../py3-install-test-virtualenv/bin/python
# [new version number] <a>foo</a>

# Cleanup
deactivate
rm -rf ../py3-install-test-virtualenv

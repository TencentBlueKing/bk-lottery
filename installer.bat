ECHO Begin to install Python...
start /wait .\package\python-3.6.8-amd64.exe /QB
ECHO.

set PATH=%PATH%;C:\Program Files\Python36;C:\Program Files\Python36\Scripts;

ECHO Begin to install dependence...
pip install .\package\MarkupSafe-0.23-cp27-none-win32.whl
pip install .\package\Mako-1.0.3.tar.gz
pip install .\package\xlrd-0.9.4-py3-none-any.whl
pip install .\package\xlwt-1.0.0-py2.py3-none-any.whl
pip install ./package/blueapps-4.5.0-py2.py3-none-any.whl
pip install -r requirements.txt
ECHO.
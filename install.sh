echo "安装依赖包..."
cd "$(dirname "$0")"
pip install ./package/blueapps-4.5.0-py2.py3-none-any.whl
pip install -r requirements.txt
echo "安装完成"
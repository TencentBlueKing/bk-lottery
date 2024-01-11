echo "启动抽奖程序..."
cd "$(dirname "$0")"
echo "更新/创建数据库"
python manage.py makemigrations
python manage.py migrate
python manage.py init
echo "启动服务"
python  manage.py runserver 8080 &

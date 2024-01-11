set PATH=%PATH%;C:\Program Files\Python36\;C:\Program Files\Python36\Scripts;C:\Program Files\Git\bin;
python manage.py makemigrations
python manage.py migrate
python manage.py init
python manage.py runserver 80
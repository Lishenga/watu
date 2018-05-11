web: gunicorn gettingstarted.wsgi --log-file -
web: python manage.py clearcache && gunicorn watu_v2.wsgi -b 0.0.0.0:$PORT -w 5 --preload




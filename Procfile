web: daphne ClassFlyComm.asgi:application --port $PORT --bind 0.0.0.0
celeryd: celery -A ClassFlyComm.celery worker -E -B --loglevel=INFO
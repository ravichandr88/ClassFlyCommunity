web: daphne ClassFlyComm.asgi:application --port $PORT --bind 0.0.0.0
worker:  celery -A ClassFlyComm worker --pool=solo -l info

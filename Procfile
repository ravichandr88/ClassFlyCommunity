web: daphne ClassFlyComm.asgi:application --port $PORT --bind 0.0.0.0
worker: REMAP_SIGTERM=SIGQUIT celery worker --app ClassFlyComm.celery.app --loglevel info

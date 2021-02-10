web: daphne ClassFlyComm.asgi:application --log-file - 
worker: REMAP_SIGTERM=SIGQUIT celery worker --app ClassFlyComm.celery.app --loglevel info






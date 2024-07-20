#!/bin/bash

cd src/helpers/background

celery -A worker.celery worker --loglevel=info -P solo & celery -A worker.celery beat --loglevel=info
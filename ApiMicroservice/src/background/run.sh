#!/bin/bash

cd src/background

celery -A worker.celery worker --loglevel=info -P solo & celery -A worker.celery beat --loglevel=info
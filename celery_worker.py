#!/usr/bin/env python
# run command: celery worker -A celery_worker.celery --loglevel=info
import os
from app.app import create_app
from app.extensions import celery

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
app.app_context().push()
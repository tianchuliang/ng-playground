#!/bin/bash
gunicorn --workers 4 --bind 0.0.0.0:8000 wsgi:app --log-level=debug --timeout=90
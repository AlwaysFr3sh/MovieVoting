#!/usr/bin/env bash
gunicorn --threads 50 app:app

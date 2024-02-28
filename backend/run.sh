#!/usr/bin/env bash
gunicorn --threads 50 server:app

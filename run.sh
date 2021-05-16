#!/bin/bash

exec 2>&1

exec /usr/bin/python3.8 /var/local/scripts/nginx_metrics/metrics.py

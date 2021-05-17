#!/bin/bash

exec 2>&1

exec /usr/bin/python3.8 /var/nginx_metrics/code/metrics.py

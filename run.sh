#!/bin/bash

exec 2>&1

exec /usr/bin/python3.8 /opt/nginx_plus_metrics_fetcher/code/metrics.py

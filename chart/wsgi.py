"""
WSGI config for chart project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os
# ↓ awake用
import threading
import requests
import time
# ↑ awake用
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chart.settings')

application = get_wsgi_application()


def awake():
    while True:
        try:
            print("Start Awaking")
            requests.get("https://graph-covid-19.herokuapp.com/")
            print("End")
        except Exception as e_awake:
            print("e_awake", e_awake)
        time.sleep(1500)


t = threading.Thread(target=awake)
t.start()

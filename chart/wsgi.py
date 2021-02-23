"""
WSGI config for chart project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chart.settings')

application = get_wsgi_application()

import threading
import requests
# ↓ awake用
import time
# ↑ awake用
# ↓ checkup用
from datetime import datetime, timezone

import sys
sys.path.append('../')
from graph.models import Source
from graph.views_def import csv_str, updated
# ↑ checkup用


def awake():
    while True:
        print('Start Awake')
        try: requests.get("https://graph-covid-19.herokuapp.com/")
        except Exception as e_awake: print("e_awake", e_awake)
        print('End Awake')
        time.sleep(1500)


def update_source(source):
    while True:
        wait_time = 72000  # 更新できたとき 20時間後に再実行
        res = ''
        try: res = requests.head(source.url)
        except Exception as e_res: print('e_res', e_res)
        if res:
            if res.status_code == 200 and \
                    res.headers['Content-Type'] == 'text/csv':
                source_updated = source.updated_at
                last_modified = datetime.strptime(
                    res.headers['Last-Modified'],
                    '%a, %d %b %Y %H:%M:%S GMT'
                    ).astimezone(timezone.utc)
                if source_updated < last_modified:
                    print('Start Update', source)
                    csv_data = requests.get(source.url).content.decode('utf-8')
                    done = False
                    while not done:
                        try:
                            csv_str(source, csv_data)
                            updated(source.pk, last_modified)
                            done = True
                        except Exception: time.sleep(5)
                    print('End Update', source)
                else:
                    wait_time = 3600  # 更新がないとき 1時間後に再実行
                    print('No Update', source, 'Retry after 1 hour')
            else: print('e_res_status', res.status_code, source)
        time.sleep(wait_time)


def checkup():
    for source in Source.objects.all():
        t_update = threading.Thread(
            target=update_source, kwargs={'source': source})
        t_update.start()
        time.sleep(0.5)


t_awake = threading.Thread(target=awake)
t_awake.start()

t_checkup = threading.Thread(target=checkup)
t_checkup.start()

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

# ↓ awake, checkup用
import threading
import requests
# ↓ awake用
import time
# ↓ checkup用
from datetime import datetime, timezone
import sys
sys.path.append('../')
from graph.models import Source
from graph.views_def import csv_str, updated, up_image
from process.models import Process
from process.views_def import up_image as up_image_p
from process.views_def import updated as updated_p


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
                            time.sleep(1)
                            updated(source.pk, last_modified)
                            time.sleep(1)
                            up_image(source)
                            done = True
                        except Exception: time.sleep(7)
                    print('End Update', source)
                else:
                    wait_time = 3600  # 更新がないとき 1時間後に再実行
                    print('No Update', source, 'Retry after 1 hour')
            else: print('e_res_status', res.status_code, source)
        time.sleep(wait_time)


def update_process(process):
    while True:
        wait_time = 72000  # 更新できたとき 20時間後に再実行
        process_up = process.updated_at
        source1_up = process.data1_col.source.updated_at
        source2_up = process.data2_col.source.updated_at

        if process_up < source1_up or \
                process_up < source2_up:
            print('Start Update-P', process)
            done = False
            while not done:
                try:
                    updated_p(process.pk, max(source1_up, source2_up))
                    time.sleep(1)
                    up_image_p(process)
                    done = True
                except Exception: time.sleep(7)
            print('End Update-P', process)
        else:
            wait_time = 3600  # 更新がないとき 1時間後に再実行
            print('No Update-P', process, 'Retry after 1 hour')
        time.sleep(wait_time)


def checkup():
    for source in Source.objects.all():
        t_update = threading.Thread(
            target=update_source, kwargs={'source': source})
        t_update.start()
        time.sleep(1)

    for process in Process.objects.all():
        t_update_p = threading.Thread(
            target=update_process, kwargs={'process': process})
        t_update_p.start()
        time.sleep(1)


t_awake = threading.Thread(target=awake)
t_awake.start()

checkup()
'''
t_checkup = threading.Thread(target=checkup)
t_checkup.start()
'''

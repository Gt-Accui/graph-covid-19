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


def awake():
    while True:
        print('Start Awake')
        try: requests.get("https://graph-covid-19.herokuapp.com/")
        except Exception as e_awake: print("e_awake", e_awake)
        print('End Awake')
        time.sleep(1500)


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


def update_source(source):
    print('Start Update', source)
    res = ''
    try: res = requests.head(source.url)
    except Exception as e_res: print('e_res', source, e_res)
    if res:
        if res.status_code == 200 and \
                res.headers['Content-Type'] == 'text/csv':
            source_updated = source.updated_at
            last_modified = datetime.strptime(
                res.headers['Last-Modified'],
                '%a, %d %b %Y %H:%M:%S GMT'
                ).astimezone(timezone.utc)
            if source_updated < last_modified:
                try:
                    csv_data = requests.get(source.url).content.decode('utf-8')
                except Exception as e_csv_decode_utf8:
                    print('e_csv_decode_utf8', e_csv_decode_utf8)
                    csv_data = requests.get(source.url).content.decode('shift_jis')
                done = False
                trial = 0
                while not done:
                    try:
                        csv_str(source, csv_data)
                        updated(source.pk, last_modified)
                        up_image(source)
                        done = True
                    except Exception as e_s:
                        if trial >= 5:
                            print(f'source {source} Faild Exit')
                            done = True
                        else:
                            trial += 1
                            print(f'source {source} trial{trial} Faild\n{e_s}')
                            time.sleep(1)
                print('End Update', source)
            else: print('No Update', source)
        else: print('e_res_status', res.status_code, source)


def update_process(process):
    print('Start Update-P', process)
    process_up = process.updated_at
    source1_up = process.data1_col.source.updated_at
    source2_up = process.data2_col.source.updated_at

    if process_up < source1_up or \
            process_up < source2_up:
        done = False
        trial = 0
        while not done:
            try:
                updated_p(process.pk, max(source1_up, source2_up))
                up_image_p(process)
                done = True
            except Exception as e_p:
                if trial >= 5:
                    print(f'process {process} Faild Exit')
                    done = True
                else:
                    trial += 1
                    print(f'process {process} trial{trial} Faild \n{e_p}')
                    time.sleep(1)
        print('End Update-P', process)
    else: print('No Update', process)


def checkup():
    wait_time = 3600  # 1時間間隔で再実行
    while True:
        print('Start Checkup')
        for source in Source.objects.all():
            update_source(source)

        for process in Process.objects.all():
            update_process(process)
        print('End Checkup')
        time.sleep(wait_time)


t_awake = threading.Thread(target=awake)
t_awake.start()

t_checkup = threading.Thread(target=checkup)
t_checkup.start()

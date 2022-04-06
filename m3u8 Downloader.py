# =======================================================
# m3u8 Downloader
# Copyright (c) 2022 chaziming
# All rights reserved.
#
# ����Դ�������� Apache License 2.0 Э��
# =======================================================

import requests
import re
from Crypto.Cipher import AES
from multiprocessing.dummy import Pool
from urllib.parse import urljoin
import os


__version__ = 'v0.1.0'
__author__ = 'chaziming'


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/100.0.4896.60 Safari/537.36 Edg/100.0.1185.29 '
}
session = requests.Session()
ts_url = []


title = 'm3u8 Downloader' + ' '*5
author = 'chaziming'
version = 'v0.1.0'
dividing_line = '-' * 40 + '\n'
fix_bugs = '�޸�bug������\n'
optimization = '˵�������汾Ϊ�˳���ĵ�һ�汾������һЩȱ�㣬�����������Ż������غõ���Ƶ�ڵ��Ե���Ƶ�ļ�����\n' \
                '�ص㣺1.��������m3u8��������ӵ�з�ֹ�������Զ������Ĺ���\n' \
                '2.���̣߳��ٶȷǳ���\n' \
                '3.bug����\n' \
                'ȱ�㣺����gui����\n'
print('\033[1;34m' + dividing_line + title, version, 'by', author)
print('���棺\n' + fix_bugs + optimization + dividing_line + '\033[0m')

while True:
    try:
        m3u8_url = input('������m3u8��ַ��')
        print('��ʼ��ȡm3u8����')
        m = 1
        while True:
            try:
                response = session.get(m3u8_url, headers=headers, timeout=3)
                if response.status_code == 200:
                    break
            except requests.exceptions.ReadTimeout:
                print(f'\033[1;31m���ӳ�ʱ�����ڰ����Զ����������� \033[1;36m{m}\033[1;31m��������\033[0m ')
                m += 1
        content = response.text
        print('�ɹ���ȡm3u8�ļ�����')
    except requests.exceptions.RequestException:
        print("�������m3u8��ַ�����������ܾ����ӣ�����������")
        continue
    if "#EXTM3U" not in content:
        print("�ⲻ��һ��m3u8����Ƶ���ӣ�����������")
        continue
    else:
        break


def process_m3u8():
    global ts_url
    ts_list = re.findall('EXTINF:.*,\n(.*)\n#', content)
    for i in ts_list:
        each_url = urljoin(m3u8_url, i)
        ts_url.append(each_url)
    quantity = len(ts_url)
    print('�����ص���ƵƬ���ܹ���', quantity)
    return


def encrypted_download(url):
    key_url = re.sub('hls(/.*?.m3u8)', 'hls/key.key', m3u8_url)
    i = 1
    while True:
        try:
            key = session.get(url=key_url, headers=headers, timeout=3).text.encode('utf-8')
            break
        except requests.exceptions.ReadTimeout:
            print(f'��ȡ��Կ��ʱ�����ڰ������»�ȡ����{i}�γ��ԣ�')
            i += 1

    cryptor = AES.new(key, AES.MODE_CBC, key)
    a = 1 + ts_url.index(url)
    i = 1
    while True:
        try:
            res = session.get(url=url, headers=headers, timeout=3)
            break
        except requests.exceptions.ReadTimeout:
            print(f'��ȡ��{a}����ƵƬ�γ�ʱ�����ڰ������»�ȡ����{i}�γ��ԣ�')
            i += 1
    cont = cryptor.decrypt(res.content)
    with open(os.path.join(r'C:\Users\Administrator\Videos', '%05d.ts' % a), 'wb') as f:
        f.write(cont)


def normal_download(url):
    a = 1 + ts_url.index(url)
    i = 1
    while True:
        try:
            res = session.get(url=url, headers=headers, timeout=3)
            break
        except requests.exceptions.ReadTimeout:
            print(f'��ȡ��{a}����ƵƬ�γ�ʱ�����ڰ������»�ȡ����{i}�γ��ԣ�')
            i += 1
    with open(os.path.join(r'C:\Users\Administrator\Videos', '%05d.ts' % a), 'wb') as f:
        f.write(res.content)


def check(s):
    print('���ڰ�������Ƿ�����©����ƵƬ��')
    for a in range(len(ts_url)):
        a += 1
        if os.path.isfile(r'C:\Users\Administrator\Videos\%05d.ts' % a):
            pass
        else:
            print(f'��⵽����{a}����ƵƬ������©�����ڰ������»�ȡ')

            url = ts_url[a - 1]
            i = 1
            while True:
                try:
                    res = session.get(url=url, headers=headers, timeout=3)
                    break
                except requests.exceptions.ReadTimeout:
                    print(f'��ȡ��{a}����ƵƬ�γ�ʱ�����ڰ������»�ȡ����{i}�γ��ԣ�')
                    i += 1
            with open(os.path.join(r'C:\Users\Administrator\Videos', '%05d.ts' % a), 'wb') as f:
                if s == 1:
                    key_url = re.sub('hls(/.*?.m3u8)', 'hls/key.key', m3u8_url)
                    while True:
                        try:
                            key = session.get(url=key_url, headers=headers, timeout=3).text.encode('utf-8')
                            break
                        except requests.exceptions.ReadTimeout:
                            pass
                    cryptor = AES.new(key, AES.MODE_CBC, key)
                    cont = cryptor.decrypt(res.content)
                    f.write(cont)
                else:
                    f.write(res.content)
    print('�����ϣ���ʼ�ϳ�')


def run():
    process_m3u8()
    pool = Pool(10)
    if "EXT-X-KEY" not in content:
        pool.map(normal_download, ts_url)
        check(0)
    else:
        pool.map(encrypted_download, ts_url)
        check(1)


if __name__ == "__main__":
    run()

# =======================================================
# Bilibili Downloader
# Copyright (c) 2022 chaziming
# All rights reserved.
#
# ����Դ�������� Apache License 2.0 Э��
# =======================================================

"""
˵��.һ.�������ŵ㣺1.��������m3u8��������ӵ�з�ֹ�������Զ����������̹߳��ܣ��ٶȷǳ���
2.������ǿ����ʹ��������ʱ�ص��ٴ򿪣�ֻ������������ͬ��m3u8��ַ�Ϳ��Խ����ϴεĽ��ȼ���
ȱ�㣺1.����gui����
��.������Ϣ/��������������·�announcement()����
"""

__version__ = 'v0.2.0'
__author__ = 'chaziming'

import requests
import re
from Crypto.Cipher import AES
from multiprocessing.dummy import Pool
from urllib.parse import urljoin
import os
from subprocess import Popen
import time
import tkinter as tk
from tkinter import filedialog


class M3U8_Downloader:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/100.0.4896.60 Safari/537.36 Edg/100.0.1185.29 '
    }
    session = requests.Session()

    def __init__(self):
        self.ts_url = []
        self.content = None
        self.m3u8_url = None
        self.cryptor = None
        self.quantity = None
        self.path = None
        self.name = None
        self.announcement()
        self.get_url()
        self.process_m3u8()
        if "EXT-X-KEY" in self.content:
            self.get_key()
        self.get_path()
        self.get_name()
        self.run()
        self.combine()

    @staticmethod
    def announcement():
        title = 'm3u8 Downloader' + ' ' * 5
        author = 'chaziming'
        version = 'v0.2.0'
        dividing_line = '-' * 40 + '\n'
        feature = '�������ص㣺�ŵ㣺1.��������m3u8��������ӵ�з�ֹ\n' \
                  '�������Զ����������̹߳��ܣ��ٶȷǳ���\n' \
                  '2.������ǿ����ʹ��������ʱ�ص��ٴ򿪣�ֻ��������\n' \
                  '����ͬ��m3u8��ַ�Ϳ��Խ����ϴεĽ��ȼ���\n' \
                  'ȱ�㣺1.����gui����\n'
        fix_bugs = '�޸�bug������\n'
        optimization = '�Ż���1.�������Զ���·������\n' \
                       '2.�������Զ����߳�������\n' \
                       '3.�Ż��˵ײ��߼���ʹ���и���˳��\n' \
                       '4.�������Զ�������ʱ�䣬��ֹ������������Ƶ������\n'
        spread = 'more: \nhttps://github.com/chaziming/Video-Downloader\n'
        print('\033[1;34m' + dividing_line + title, version, 'by', author)
        print(feature + '���棺\n' + fix_bugs + optimization + spread + dividing_line + '\033[0m')

    def get_url(self):
        while True:
            try:
                m3u8_url = input('������m3u8��ַ��')
                print('��ʼ��ȡm3u8����')
                m = 1
                while True:
                    try:
                        response = self.session.get(m3u8_url, headers=self.headers, timeout=10)
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
                self.m3u8_url = m3u8_url
                self.content = content
                break

    def process_m3u8(self):
        ts_list = re.findall('EXTINF:.*,\n(.*)\n#', self.content)
        for i in ts_list:
            each_url = urljoin(self.m3u8_url, i)
            self.ts_url.append(each_url)
        self.quantity = len(self.ts_url)
        print('�����ص���ƵƬ���ܹ���', self.quantity)
        return

    def get_path(self):
        print('���ڵ����Ĵ�����ѡ����Ƶλ��')
        time.sleep(2)
        root = tk.Tk()
        root.withdraw()
        folder_path = filedialog.askdirectory()
        self.path = folder_path

    def get_name(self):
        name = input('����д�������ص��ļ������ɿգ�Ĭ��Ϊ��ǰʱ�����')
        if name == '':
            name = round(time.time())
        self.name = name
        os.makedirs(self.path + f'/{self.name}', exist_ok=True)

    def get_key(self):
        key_url = re.sub('hls(/.*?.m3u8)', 'hls/key.key', self.m3u8_url)
        i = 1
        while True:
            try:
                key = self.session.get(url=key_url, headers=self.headers, timeout=3).text.encode('utf-8')
                break
            except requests.exceptions.ReadTimeout:
                print(f'��ȡ��Կ��ʱ�����ڰ������»�ȡ����{i}�γ��ԣ�')
                i += 1
        self.cryptor = AES.new(key, AES.MODE_CBC, key)

    def encrypted_download(self, url):
        a = 1 + self.ts_url.index(url)
        i = 1
        while True:
            try:
                res = self.session.get(url=url, headers=self.headers, timeout=5)
                break
            except requests.exceptions.ReadTimeout:
                print(f'��ȡ��{a}����ƵƬ�γ�ʱ�����ڰ������»�ȡ����{i}�γ��ԣ�')
                i += 1
        cont = self.cryptor.decrypt(res.content)
        if os.path.isfile(self.path + f'/{self.name}/' + '%05d.ts' % a):
            pass
        with open(self.path + f'/{self.name}/%05d.ts' % a, 'wb') as f:
            f.write(cont)

    def normal_download(self, url):
        a = 1 + self.ts_url.index(url)
        i = 1
        while True:
            try:
                res = self.session.get(url=url, headers=self.headers, timeout=5)
                break
            except requests.exceptions.ReadTimeout:
                print(f'��ȡ��{a}����ƵƬ�γ�ʱ�����ڰ������»�ȡ����{i}�γ��ԣ�')
                i += 1
        if os.path.isfile(self.path + f'/{self.name}/' + '%05d.ts' % a):
            pass
        else:
            with open(self.path + f'/{self.name}/%05d.ts' % a, 'wb') as f:
                f.write(res.content)

    def encrypted_check(self):
        print('���ڰ�������Ƿ�����©����ƵƬ��')
        for a in range(len(self.ts_url)):
            a += 1
            if os.path.isfile(self.path + f'/{self.name}/' + '%05d.ts' % a):
                pass
            else:
                print(f'��⵽����{a}����ƵƬ������©�����ڰ������»�ȡ')
                url = self.ts_url[a - 1]
                i = 1
                while True:
                    try:
                        res = self.session.get(url=url, headers=self.headers, timeout=5)
                        break
                    except requests.exceptions.ReadTimeout:
                        print(f'��ȡ��{a}����ƵƬ�γ�ʱ�����ڰ������»�ȡ����{i}�γ��ԣ�')
                        i += 1
                with open(self.path + f'/{self.name}/%05d.ts' % a, 'wb') as f:
                    cont = self.cryptor.decrypt(res.content)
                    f.write(cont)
        print('�����ϣ���ʼ�ϲ�')

    def normal_check(self):
        print('���ڰ�������Ƿ�����©����ƵƬ��')
        for a in range(len(self.ts_url)):
            a += 1
            if os.path.isfile(self.path + f'/{self.name}/' + '%05d.ts' % a):
                pass
            else:
                print(f'��⵽����{a}����ƵƬ������©�����ڰ������»�ȡ')
                url = self.ts_url[a - 1]
                i = 1
                while True:
                    try:
                        res = self.session.get(url=url, headers=self.headers, timeout=5)
                        break
                    except requests.exceptions.ReadTimeout:
                        print(f'��ȡ��{a}����ƵƬ�γ�ʱ�����ڰ������»�ȡ����{i}�γ��ԣ�')
                        i += 1
                with open(self.path + f'/{self.name}/%05d.ts' % a, 'wb') as f:
                    f.write(res.content)
        print('�����ϣ���ʼ�ϲ�')

    def run(self):
        threads = input('�������߳������ɿգ�Ĭ��10����')
        if threads:
            pool = Pool(int(threads))
        else:
            pool = Pool(10)
        if "EXT-X-KEY" not in self.content:
            pool.map(self.normal_download, self.ts_url)
            self.normal_check()
        else:
            pool.map(self.encrypted_download, self.ts_url)
            self.encrypted_check()

    def combine(self):
        command = 'copy /b ' + self.path + f'/{self.name}/' + '*.ts ' + self.path + f'/{self.name}/{self.name}'\
                  + '.mp4 '
        Popen(command, shell=True)
        print('�ϲ���ϣ������')
        while True:
            if os.path.isfile(self.path + f'/{self.name}/{self.name}' + '.mp4'):
                time.sleep(30)
                for a in range(self.quantity):
                    a += 1
                    os.remove(self.path + f'/{self.name}/%05d.ts' % a)
                break
        print('�ɹ�ɾ��������ƵƬ��')


if __name__ == "__main__":
    m3u8_downloader = M3U8_Downloader()

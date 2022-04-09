# =======================================================
# Normal Downloader
# Copyright (c) 2022 chaziming
# All rights reserved.
#
# ����Դ�������� Apache License 2.0 Э��
# =======================================================

"""
˵����һ����������������֪�����ġ�ֱ�ӵ���Ƶ��ַ��������Ƶû���κεĲ�֣����ܡ�
��.�������ŵ㣺1.���Ի�������չʾ
ȱ�㣺1.����gui����
��.������Ϣ/��������������·�announcement()����
"""

__version__ = 'v0.1.0'
__author__ = 'chaziming'

import sys
from datetime import timedelta
import os
from time import time
from requests import Session
from requests.exceptions import RequestException

session = Session()

def announcement():
    title = 'Normal Downloader' + ' '*3
    author = 'chaziming'
    version = 'v0.1.0'
    dividing_line = '-' * 40 + '\n'
    explanation = '��������������֪�����ġ�ֱ�ӵ���Ƶ��ַ��������Ƶû���κεĲ�֣�����'
    fix_bugs = '����'
    optimization = '�Ż�������\n'
    spread = 'more see: https://github.com/chaziming/Video-Downloader\n'
    print('\033[1;34m' + dividing_line + title, version, 'by', author)
    print('˵����' + explanation)
    print('���棺\n' + fix_bugs + optimization + spread + dividing_line + '\033[0m')
    return


def get_html(url):
    head = {
        "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/98.0.4758.102 Safari/537.36 Edg/98.0.1108.56'
    }
    try:
        response = session.get(url=url, headers=head)
        if response.status_code == 200:
            return response.text
    except RequestException:
        print("����ʧ��")
        quit()


def file_download(video_url):
    headers = {
        "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/98.0.4758.102 Safari/537.36 Edg/98.0.1108.56'}
    chunk_size = 1024 * 1024
    headers['Range'] = 'bytes=' + '0' + '-'
    video_res = session.get(url=video_url, stream=True, headers=headers)
    video_size = int(video_res.headers['content-length'])
    t = time()
    speed = 0.0
    size = 0
    print('��ʼ������Ƶ')
    with open(os.path.join(r'C:\Users\Administrator\Videos', 'ԭʼʱ��.mp4'), 'ab') as f:
        for data in video_res.iter_content(chunk_size=chunk_size):  # ÿ��ֻ��ȡһ��chunk_size��С
            f.write(data)  # ÿ��ֻд��data��С
            tt = time() - t
            t = time()
            size = len(data) + size
            # 'r'ÿ�����´ӿ�ʼ�����end = ""�ǲ�����
            percentage = int(size / video_size * 40)
            if speed < 5.0:
                color = '\033[1;31m'
            else:
                color = '\033[1;32m'
            if speed == 0.0 or round((video_size - size) / chunk_size / speed) > 1800:
                eta = '\033[1;31m' + ' >30min'
            else:
                eta = '\033[1;34m' + ' eta ' + str(timedelta(seconds=round((video_size - size) / chunk_size / speed)))
            print('\r\t' + "\033[1;35m" + percentage * '��' + '\033[0m' + (40 - percentage) * '��' + '\033[1;35m',
                  str(round(size / chunk_size, 1)) + '/' + str(round(video_size / chunk_size, 1)), "MB" + color,
                  str(speed), 'MB/s' + eta, flush=True,
                  end='')
            sys.stdout.flush()
            last_speed = speed
            speed = round(float(chunk_size / 1024 / 1024) / tt, 1)

        if last_speed < 5.0:
            color = '\033[1;31m'
        else:
            color = '\033[1;32m'
        print('\r\t''\033[1;32m' + 40 * '��' + '\033[1;32m',
              str(round(size / chunk_size, 1)) + '/' + str(round(video_size / chunk_size, 1)), "MB" + color,
              str(speed), 'MB/s' + '\033[1;34m', 'eta', '0:00:00' + '\033[0m', flush=True)


def main():
    announcement()
    url = input('�����������ġ�ֱ�ӵ���Ƶ��ַ��')
    file_download(url)


if __name__ == "__main__":
    main()
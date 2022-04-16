# -*- coding: UTF-8 -*-
"""
    File Name:          interface_test.py
    Author:             LIN Guocheng
    Version:            1.0.0
    Description:        持续访问接口网址并记录返回值
"""

import time
import urllib.request
import datetime

URL = "http://101.43.164.112:8000/state"

if __name__ == "__main__":
    while True:
        time.sleep(0.5)
        response = urllib.request.urlopen(URL)
        result = response.read()
        print(datetime.datetime.now(), "-", result)

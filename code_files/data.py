import re
import os
from code_files.conf import max_retries


import sys
sys.tracebacklimit = 0

import requests


def check_internet_connectivity():
    url = "http://www.speedtest.net"
    timeout = 5
    try:
        request = requests.get(url, timeout=timeout)
        print("Connected to the Internet")
        return True
    except (requests.ConnectionError, requests.Timeout) as exception:
        print("No internet connection.")
        return False


def get_test_value_set(cycle):
    test_value = []
    i = 0
    while 0 < cycle:
        print("Attempting Speed Test...")
        try:
            ifconfig = os.popen('speedtest')
            ifconfig_out = ifconfig.read()

            Downloads = (re.findall(r'\s*\d+\b.\d+\b\s', ifconfig_out))[2]
            Upload = (re.findall(r'\s*\d+\b.\d+\b\s', ifconfig_out))[3]
            latency = (re.findall(r'\s*\d+\b.\d+\b\s', ifconfig_out))[1]

            test_value.append({"latency": latency, "download_speed": Downloads, "upload_speed": Upload})
            print(test_value)
            cycle = cycle - 1
        except:
            i = i + 1
            print("exception occurred")
        if i >= max_retries:
            print("Max Retries Exhaused. Check your connection")
            return False
    return test_value


def get_test_value_sets(n):
    test_value = []
    for i in range(0, n):
        test_value.append(get_test_value_set())
    print("final test value")
    print(test_value)
    return test_value


def get_mock_data():
    return [
        {'latency': '31.787', 'download_speed': '5.26', 'upload_speed': '2.20'},
        {'latency': '32.787', 'download_speed': '8.26', 'upload_speed': '4.20'},
        {'latency': ' 31.871 ', 'download_speed': ' 9.21 ', 'upload_speed': ' 4.30 '},
        {'latency': ' 28.787 ', 'download_speed': ' 9.16 ', 'upload_speed': ' 4.20 '},
        {'latency': ' 31.783 ', 'download_speed': ' 9.86 ', 'upload_speed': ' 3.90 '}
    ]

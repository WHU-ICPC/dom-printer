#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import time
import argparse
import requests
from base64 import b64decode


parser = argparse.ArgumentParser()
parser.add_argument('server', type=str, help='服务端地址')
parser.add_argument('user', type=str, help='用户名')
parser.add_argument('passwd', type=str, help='密码')
parser.add_argument('--saveExt', type=str, help='保存文件的扩展名, 默认.txt', default='.txt')
parser.add_argument('--rmPrintFile', type=bool, help='是否在打印完后删除对应文件', default=False)
args = parser.parse_args()

SERVER_URL = args.server
USERNAME = args.user
PASSWORD = args.passwd
SAVE_EXT = args.saveExt
RM_PRINT = args.rmPrintFile


# 获取文件的 URL
SERVER_GET_FILE_URL = f"{SERVER_URL}/api/print"
# 标记文件的 URL, 最后拼接 SERVER_GET_FILE_URL + nonce
SERVER_MARK_FILE_URL = f"{SERVER_URL}/api/print/"

while True:
    try:
        response = requests.get(SERVER_GET_FILE_URL, auth=(USERNAME, PASSWORD))
        if response.status_code == 404:
            print("---没有可打印的文件 (服务端返回404) ---")
            break
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            print('等待30s')
            time.sleep(30)
        if response.status_code == 200:
            file_data = response.json()
            nonce = file_data["id"]
            info = b64decode(file_data["info"])
            data = b64decode(file_data["data"])

            filename = nonce + SAVE_EXT

            with open(filename, "wb") as f:
                f.write(info + data)

            # 标记文件
            response = requests.delete(SERVER_MARK_FILE_URL + nonce, auth=(USERNAME, PASSWORD))
            if response.status_code == 200:
                # 调用系统打印机打印
                print(f"打印文件 {filename}")
                # 在此处添加调用系统打印机的代码
                os.startfile(filename, "print")
                if RM_PRINT:
                    os.remove(filename)
            else:
                print(f"确认文件 {nonce} 失败!")
                os.remove(filename)

    except Exception as e:
        print(f"Error: {e}")
        print('等待30s')
        time.sleep(30)

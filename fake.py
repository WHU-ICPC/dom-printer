#!/usr/bin/python
# -*- coding: UTF-8 -*-
import random
import string

from faker import Faker

if __name__ == '__main__':
    genNum = int(input('生成数量: '))
    fake = Faker(locale='zh_CN')
    for i in range(genNum):
        nonce = ''.join(random.sample(string.ascii_letters, 5))
        info = f"filename: {nonce}\ndescription: \n{fake.text()}"
        data = fake.text()
        print(f"nonce: {nonce}\n")
        with open(f"simulation/server/new/{nonce}.txt", 'w', encoding='utf-8') as f:
            f.write(info)
        with open(f"simulation/server/new/{nonce}.dat", 'w', encoding='utf-8') as f:
            f.write(data)

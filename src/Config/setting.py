#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os

import yaml


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
filename = os.path.join(BASE_DIR, 'Config/mode.yaml')


def load_info():
    with open(filename, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


if __name__ == '__main__':
    res = load_info()
    print([i for i in res])

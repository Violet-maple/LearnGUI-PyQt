#!/usr/bin/python3
# -*- coding: utf-8 -*-
import yaml


def load_info():
    with open("./mode.yaml", 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


if __name__ == '__main__':
    res = load_info()
    print([i for i in res])

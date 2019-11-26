#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
from logging import handlers


def load_info():
    return {
        "forward": {"imgPath": None},
        "sellsy": {"imgPath": None},
        "film": {"imgPath": None},
        "home": {"imgPath": None},
        "download": {"imgPath": None},
        "heart": {"imgPath": None},
        "comment": {"imgPath": None},
        "star": {"imgPath": None},
        "question": {"imgPath": None},
        "music": {"imgPath": None},
        "pause": {"imgPath": None},
        "backward": {"imgPath": None},
    }


def load_log_config(model_name):
    logging.basicConfig(level=logging.DEBUG,
                        filename=f'./Log/Model-{model_name}.log',
                        filemode='a',
                        format='%(asctime)s - [line:%(lineno)d]: %(message)s'
                        )


if __name__ == '__main__':
    res = load_info()
    print([i for i in res])

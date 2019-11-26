#!/usr/bin/python3
# -*- coding: utf-8 -*-

import random

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def save_img():
    fig = plt.figure(figsize=(10, 6))
    x = [f"now_{i}" for i in range(100)]
    data = [random.randint(10, 100) for _ in range(100)]
    # random.shuffle(x)
    y = [i for i in range(0, 100, 10)]
    
    plt.plot(x, data)
    plt.xticks(x, x, rotation=90)
    plt.tick_params(labelsize=4)
    fig.savefig('foo.png')

    writer = pd.ExcelWriter('savepicture.xlsx', engine='xlsxwriter')
    sheet = writer.book.add_worksheet('test')
    sheet.insert_image(0, 0, 'foo.png')
    sheet.insert_image(30, 0, 'foo.png')
    writer.save()

    # plt.show()


def main():
    save_img()


if __name__ == '__main__':
    main()

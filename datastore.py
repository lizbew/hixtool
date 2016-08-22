# coding: utf-8

import os
import json
import codecs

DATA_PATH = os.path.join(os.path.dirname(__file__), 'data')


def get_data_with_kind(k):
    if not k:
        raise Exception('Data kind is required')
    fpath = os.path.join(DATA_PATH, u'{}.json'.format(k))
    if not os.path.exists(fpath):
        return None
    data = json.load(codecs.open(fpath, 'r', encoding='utf-8'))
    return data


def save_data_with_kind(k, data):
    if not k:
        raise Exception('Data kind is required')
    fpath = os.path.join(DATA_PATH, u'{}.json'.format(k))
    json.dump(data, codecs.open(fpath, 'w', encoding='utf-8'))
    
#!/usr/bin/env python3

import os
import subprocess as sp
import json
import sys

def load(filename):
    return json.loads(open(filename).read())

def process(src_words):
    return_words = {}
    for x in words:
        word = x
        pinin = words[word]
        pinin = pinin.replace("（語音）", '').replace('\n', '')
        if '(' in word or '(' in pinin or '音' in pinin:
            continue
        pinin = pinin.split('\u3000')
        if len(word) != len(pinin):
            continue
        for i, single_pinin in enumerate(pinin):
            if 'ˊ' not in single_pinin and 'ˇ' not in single_pinin and 'ˋ' not in single_pinin and '˙' not in single_pinin:
                pinin[i] = pinin[i] + "-"
        return_words[word] = ' '.join(pinin)
    return return_words

def save(filename, words):
    with open(filename, 'w') as f:
        f.write(json.dumps(words))


    
try:
    os.makedirs('./dict')
except:
    pass

for root, dirnames, filenames in os.walk("./src_dict"):
    for filename in filenames:
        words = load('./src_dict/%s'%(filename))
        words = process(words)
        save('./dict/%s'%(filename), words)


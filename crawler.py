#!/usr/bin/env python3
import requests
import requests.utils
from bs4 import BeautifulSoup
import random
import time
import re
import sys
import json

sleep_time = 0.1

base_url = "http://dict.revised.moe.edu.tw/"

### sometime it will be redirected to index
### so continuously try until get the correct page
def get(url):
    print(base_url+url)
    while True:
        time.sleep(sleep_time)
        r = requests.get(base_url+url)
        if len(r.text) > 1491:
            return r.text
        print(".", end="")
        sys.stdout.flush()

### before we start to load their data
### we must go to index page to get the token
### otherwise we can do nothing
def get_token():
    r = requests.get(base_url+"/cgi-bin/cbdic/gsweb.cgi/?&o=dcbdic&")
    return re.search('ccd=(.*)&o', r.text).group(1)


### set the result size that
### make each query have at most 100 response
### maybe you can set psize to what you want(i did not try other number)
def set_psize(token):
    url = "cgi-bin/cbdic/gsweb.cgi"
    data = {
        "o": "e0",
        "sec": "sec1",
        "selectmode": "mode1",
        "qs0": "",
        "nogobrwtyp": "1",
        "field_1_value": "ㄅ",
        "brwtyp": "pin",
        "field_2_value": "ㄅㄚ",
        "brwsimpfmt": "10",
        "active": "",
        "field_2": "p,in2",
        "sf": "1",
        "field_1": "pin1",
        "brwsortby": "wqyx",
        "psize": "100",
        "ccd": token,
    }
    while True:
        time.sleep(sleep_time)
        r = requests.post(base_url+url, data=data)
        if len(r.text) > 1491:
            return r.text
        print(".", end="")
        sys.stdout.flush()

### get the url for level 1 list ㄅㄆㄇㄈ ...
def get_lv1_list():
    ### because the token we can use only 30 minutes
    ### so each time we should reset the token
    token = get_token()
    url = "/cgi-bin/cbdic/gsweb.cgi?ccd=%s&o=e0&&sec=sec1&brwsimpfmt=10&brwtyp=pin&field_1=pin1&field_1_value=XXX&field_2=pin2&brwsortby=wqyx&active=zybrw"%(token)
    res = get(url)
    soup = BeautifulSoup(res, "html5lib")
    lv1 = soup.find_all('span', {"class": "pin_bst_lv1"})
    set_psize(token)
    return [x.a['href'] for x in lv1]

### get the url for level 2 list "ㄅㄚ" "ㄅㄚˊ" ...
def get_lv2_list(url):
    res = get(url)
    soup = BeautifulSoup(res, "html5lib")
    lv2 = soup.find_all('span', {"class": "pin_bst_lv2"})
    return [x.a['href'] for x in lv2]


### get the level 3 list for words 
def get_lv3_list(url):
    re = {}
    while True:
        res = get(url)
        soup = BeautifulSoup(res, "html5lib")
        try:
            lv3 = soup.find('table', {"class": "fmt1table"}).find_all("tr")[1:]
        except:
            return re
        for x in lv3:
            try:
                x = x.find_all("td")
                word = x[1].a.string
                pinin = x[2].text
                re[word] = pinin
            except Exception as e:
                print(e)
        preview = soup.find('div', {'class': 'preview'}).find_all('a')
        if len(preview) > 2 and preview[-2]['title'] == "下一頁":
            print(preview[-2])
            url = preview[-2]['href']
        else:
            return re

if __name__ == "__main__":
    lv1_list = get_lv1_list()
    lv1_size = len(lv1_list)
    for lv1_id in range(lv1_size):
        lv1_list = get_lv1_list()
        lv1_url = lv1_list[lv1_id]
        lv2_list = get_lv2_list(lv1_url)
        for lv2_id, lv2_url in enumerate(lv2_list):
            lv3_list = get_lv3_list(lv2_url)
            file_name = "./src_dict/%s_%s.dict"%(lv1_id, lv2_id)
            with open(file_name, 'w') as f:
                f.write(json.dumps(lv3_list))


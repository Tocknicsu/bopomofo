# 中文轉注音

./crawler.py: 下載教育部辭典，並存放置 ./src_dict

./trans.py: 將下載回來的字典整理，並存放置 ./dict

./loader.py: 讀取字典檔

./main.py: 主程式

程式執行後，會先 load ./dict/ 下的字典，並且 load 當前目錄下的 extension.dict (如果有的話)。

如要新增新字或者校正，可以寫進 ./extesion.dict 中

./test.py 測試執行速度


## 使用算法
使用 greedy 算法，盡可能的匹配長詞。


## 執行狀況如下
```
# python3 main.py
>>> 早安
ㄗㄠˇㄢ-
>>> 今天天氣真好
ㄐㄧㄣ-ㄊㄧㄢ-ㄊㄧㄢ-ㄑㄧˋㄓㄣ-ㄏㄠˇ

# python3 test.py
import time: 0.29819822311401367
read file: 8.130073547363281e-05
634
trans time 634 words for 10000 times: 2.793743133544922
```

其中 test.file 選自 雅量

## 技術支援
- 目前僅支援 python3
- 如果沒有要使用 crawler.py 則無任何相依性
- 如要使用 crawler.py 請執行
```
pip3 install -r requirements.txt
```

## TODO

- [ ] 改用 [結巴](https://github.com/fxsjy/jieba) 分詞，並搭配 [萌典開放API](https://www.moedict.tw/uni/%E6%B7%B7) 提高準確度。

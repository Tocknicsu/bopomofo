import time

now = time.time()
def tick(text=""):
    global now
    newnow = time.time()
    diff = newnow - now
    now = newnow
    if text:
        print("%s: %s"%(text, diff))
    return diff


import main as pinin
tick("import time")

text = open("test.file").read()
tick("read file")

print(len(text))
times = 10000

for i in range(times):
    res = pinin.trans_sentense(text)

tick("trans time %s words for %s times"%(len(text), times))

print(res)

# -*- encoding: utf-8 -*-
from __future__ import print_function, unicode_literals
import json
import requests
import xlwt


wbk = xlwt.Workbook()
sheet = wbk.add_sheet('sheet 1')
KEYWORDS_URL = 'http://api.bosonnlp.com/keywords/analysis'


count  = 0
timer = 1
wordlist_Number = {}


filename = raw_input("please enter file name: ")
try:
    hand = open(filename)
except:
    print("wrong file name")


params = {'top_k': 100}
str = None
a = " ".encode('utf-8')
for line in hand:
    line = line.strip()
    if len(line) > 0:
        timer = timer + 1
        if str == None: str = line
        else: str = str + a + line
    if timer >= 50:
        data = json.dumps(str)
        headers = {'X-Token': 'YOUR TOKEN'}
        resp = requests.post(KEYWORDS_URL, headers=headers, params=params, data=data.encode('utf-8'))
        timer = 1

        str = None
        for weight, word in resp.json():
            print(weight, word)
            wordlist_Number[word] = wordlist_Number.get(word, 0) + weight


l= list()
for key, val in wordlist_Number.items():
    l.append((val,key))
l.sort(reverse=True)


#print(wordlist_Number)

for x,y in l[:500]:
    #print(i,wordlist_Number[i],wordlist_Category[i])
    sheet.write(count, 0, x)
    sheet.write(count, 1, y)
    count = count + 1

wbk.save('chaoy_keywordscloud.xls')
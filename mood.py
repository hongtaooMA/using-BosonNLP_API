# -*- encoding: utf-8 -*-
from __future__ import print_function, unicode_literals
import json
import requests
import xlwt


wbk = xlwt.Workbook()
sheet = wbk.add_sheet('sheet 1')
NER_URL = 'http://api.bosonnlp.com/ner/analysis'


count  = 0
timer = 1
wordlist_Number = {}
wordlist_Category = {}

filename = raw_input("please enter file name: ")
try:
    hand = open(filename)
except:
    print("wrong file name")

s = []
str = None
a = " ".encode('utf-8')
for line in hand:
    line = line.strip()
    if len(line) > 0:
        timer = timer + 1
        if str == None: str = line
        else: str = str + a + line
    if timer >= 50:
        s.append(str)
        data = json.dumps(s)
        headers = {'X-Token': 'YOUR TOKEN'}
        resp = requests.post(NER_URL, headers=headers, data=data.encode('utf-8'))
        timer = 1
        s = []
        str = None
        for item in resp.json():
            print(resp.json())
            for entity in item['entity']:
                print(''.join(item['word'][entity[0]:entity[1]]), entity[2])
                str1 = (''.join(item['word'][entity[0]:entity[1]]))
                str2 = entity[2]
                wordlist_Number[str1] = wordlist_Number.get(str, 0) + 1
                wordlist_Category[str1] = str2





#print(wordlist_Number)

for i in wordlist_Number:
    #print(i,wordlist_Number[i],wordlist_Category[i])
    sheet.write(count, 0, i)
    sheet.write(count, 1, wordlist_Number[i])
    sheet.write(count, 2, wordlist_Category[i])
    count = count + 1

wbk.save('xiden_keywords.xls')

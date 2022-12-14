# -*- coding: utf-8 -*-
"""
Spyder Editor
Python 資料分析應用課程 - C008
台灣股票分析
"""
def convertDate(date):  #轉捔民國日期為西元:108/01/01->20190101
    str1 = str(date)
    yearstr = str1[:3]  #取出民國年
    realyear = str(int(yearstr) + 1911)  #轉為西元年
    realdate = realyear + str1[4:6] + str1[7:9]  #組合日期
    return realdate

import requests
import json, csv
import pandas as pd
import os
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = "mingliu"  #設定中文字型
plt.rcParams["axes.unicode_minus"] = False 

pd.options.mode.chained_assignment = None  #取消顯示pandas資料重設警告

filepath = 'stockmonth01.csv'

if not os.path.isfile(filepath):  #如果檔案不存在就建立檔案
    url_twse = 'https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date=20220501&stockNo=2317&_=1652568553440'
    res = requests.get(url_twse)  #回傳為json資料
    jdata = json.loads(res.text)  #json解析
    
    outputfile = open(filepath, 'w', newline='', encoding='utf-8-sig')  #開啟儲存檔案
    outputwriter = csv.writer(outputfile)  #以csv格式寫入檔案
    outputwriter.writerow(jdata['fields'])
    for dataline in (jdata['data']):  #寫入資料
        outputwriter.writerow(dataline)
    outputfile.close()  #關閉檔案

pdstock = pd.read_csv(filepath, encoding='utf-8')  #以pandas讀取檔案
for i in range(len(pdstock['日期'])):  #轉換日期式為西元年格
    pdstock['日期'][i] = convertDate(pdstock['日期'][i])
pdstock['日期'] = pd.to_datetime(pdstock['日期'])  #轉換日期欄位為日期格式
pdstock.plot(kind='line', figsize=(12, 6), x='日期', y=['收盤價', '最低價', '最高價'])  #繪製統計圖
 

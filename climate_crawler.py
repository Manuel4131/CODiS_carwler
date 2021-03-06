#!/usr/bin/env python
# encoding: utf-8

# 修改自 https://gist.github.com/wy36101299/e3b32c674d9e86ba581f

import requests
import pandas as pd
from time import sleep
from bs4 import BeautifulSoup
import csv
import os

#PATH = '/home/yan/sync/project/Weather Station/CODiS/'

PATH = './data/'

#To create the directory if it doesn't exist
if not os.path.exists(PATH):
    os.mkdir(PATH)

# 產生data List , data List為兩年份
def date():
    month31=[1,3,5,7,8,10,12]
    month30=[4,6,9,11]
    year2=['2016','2017']
    nday31=range(1,32)
    nday30=range(1,31)
    nday28=range(1,29)
    day10=['01','02','03','04','05','06','07','08','09']
    month12=day10+['10','11','12']
    nday31 = map(str,nday31[9:])
    nday30 = map(str,nday30[9:])
    nday28 = map(str,nday28[9:])
    day31 = day10 + list(nday31)
    day30 = day10 + list(nday30)
    day28 = day10 + list(nday28)
    output=[]
    s=""
    for year in year2:
        for month,strmonth in zip(range(1,13),month12):
            if month in month31:
                for day in day31:
                    s = year+'-'+strmonth+'-'+day
                    output.append(s)
            elif month in month30:
                for day in day30:
                    s = year+'-'+strmonth+'-'+day
                    output.append(s)
            else:
                for day in day28:
                    s = year+'-02-'+day
                    output.append(s)
    return output


# 爬取主函式
def crawler(url,name):
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text)

    form =[]
    # title
    second_tr = soup.find(class_="second_tr")
    titles = soup.find_all("th")
    titles = titles[9:]
    strtitle=[]
    for title in titles:
        title = title.contents
        title=title[0]+title[2]+title[4]
        strtitle.append(title)

    # parameter
    soup = soup.tbody
    tmps = soup.find_all("tr")
    tmps = tmps[2:]
    for tmp in tmps:
        tmp = tmp.find_all("td")
        parameter =[]
        for strtmp in tmp:
            strtmp = strtmp.string
            parameter .append(strtmp)
        form.append(parameter)

    form = pd.DataFrame(form, columns=strtitle)
    form.to_csv(PATH + name + ".txt", encoding ="utf-8")
    sleep(0.5)


if __name__ == "__main__":
    download = date()
    hostUrl = "http://e-service.cwb.gov.tw/HistoryDataQuery/DayDataController.do?"
    fixedParameter = "command=viewMain"
    csvFile = open('TaiwanWeatherSatation.csv')

    for date in download:
        # 此為宜蘭站的觀測資料
        #url="http://e-service.cwb.gov.tw/HistoryDataQuery/DayDataController.do?command=viewMain&station=467080&stname=%25E5%25AE%259C%25E8%2598%25AD&datepicker="+date
    
        print(date)
        try:
            crawler(url,date)
            print(url)

        except:
            # 若是爬取失敗把該日期寫入error.txt
            with open (PATH + "error.txt",'a') as f:
                f.write(date+'\n')
            csvFile.close()

    csvFile.close()

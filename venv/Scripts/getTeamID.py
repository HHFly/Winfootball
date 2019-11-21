import time
import math
from os import system
from datetime import datetime
import requests
import json
import urllib.request
import gzip
import re
import threading
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
def getTime(arr):
    # 获取当前时间
    # 字符类型的时间
    month=int(arr[1])+1
    if month>12:
        month=1
    tss1 = arr[0]+"-"+str(month)+"-"+arr[2]+" "+arr[3]+":"+arr[4]+":"+arr[5]

    # 转为时间数组
    timeArray = time.strptime(tss1, "%Y-%m-%d %H:%M:%S")
    timeStamp = int(time.mktime(timeArray))

    now_datetime = datetime.utcfromtimestamp(time.time())  # utcfromtimestamp函数根据时间戳创建一个datetime对象,utc为格林威治时间，也可改为fromtimestamp()获取按本地时间比较
    old_datetime = datetime.utcfromtimestamp(time.mktime(timeArray))
    diffseconds = (now_datetime - old_datetime).total_seconds()

    return  math.floor(diffseconds / 60)

def find_all_index(arr,item):
    return [i for i,a in enumerate(arr) if a==item]

def goalSreach(id):
# 打开chrome浏览器（需提前安装好chromedriver）
    option = webdriver.ChromeOptions()
    option.add_argument('headless')  # 静默模式
# 静默打开chrome浏览器
    browser = webdriver.Chrome(options=option)

# browser = webdriver.PhantomJS()
    browser.get("http://live.win007.com/detail/"+id+"sb.htm")

# 需要等一下，直到页面加载完成
    wait = WebDriverWait(browser, 3)
# wait.until(EC.presence_of_element_located((By.CLASS_NAME, "grid")))

    soup = BeautifulSoup(browser.page_source, "lxml")
# 表头和表数据
    goal=[]
    goaldata=[]
    for data in soup.select(".content"):
    # print (data.get_text())
      title = [c.text for c in data.findAll("th")]
      if "本场技术统计" in title:
        data_colhead = data.findAll("td")
        row_dat = [r.text for r in data_colhead]
        index = find_all_index(row_dat, "红牌")
        if index:
            print("红牌比赛不符合")
            return goal
        index=find_all_index(row_dat ,"射正")
        if index:
            sum = int(row_dat[index[0]-1])+int(row_dat[index[0]+1])
            if sum >=5:
                print("射正数符合，值为" + str(sum)+"  主队射正次数"+row_dat[index[0]-1]+"  客队射正次数"+row_dat[index[0]+1])
                goaldata.append(row_dat[index[0]-1])
                goaldata.append(row_dat[index[0]+1])
            else:
                print("射正数不符合，值为" + str(sum) + "  主队射正次数" + row_dat[index[0] - 1] + "  客队射正次数" + row_dat[index[0] + 1])
                return goal
      if "技统数据" in title:
        data_colhead = data.findAll("td")
        row_dat = [r.text for r in data_colhead]
        index = find_all_index(row_dat, "进球")
        if (index):
            print("主队近3场/近10场:  "+row_dat[index[0] - 1]+"客队近3场/近10场:  "+row_dat[index[0] + 1])
      if  "进失球概率（近30场）" in title or "进失球概率近30场近50场" in title :
        data_colhead = data.findAll("td")
        row_dat = [r.text for r in data_colhead]
        index=find_all_index(row_dat ,"76~90")
        if(index):
            oneAtack =float(row_dat[index[0] - 2].replace("%",""))
            oneLose = float(row_dat[index[0] - 1].replace("%",""))
            twoAtack =float(row_dat[index[0] + 1].replace("%",""))
            twoLose =float(row_dat[index[0] + 2].replace("%",""))
            oneGoal = float(row_dat[index[0] - 2].replace("%","")) + float(row_dat[index[0] + 2].replace("%",""))
            twoGoal = float(row_dat[index[0] - 1].replace("%","")) + float(row_dat[index[0] + 1].replace("%",""))
            if oneAtack >=40:
                print("主队数据量太少不准确")
                # return goal
            if oneAtack == 0:
                print("主队数据量太少不准确")
                # return goal
            if oneLose >=40:
                print("主队数据量太少不准确")
                # return goal
            if oneLose  ==0:
                print("主队数据量太少不准确")
                # return goal
            if twoAtack >= 40:
                print("客队数据量太少不准确")
                # return goal
            if twoAtack ==0:
                print("客队数据量太少不准确")
                # return goal
            if twoLose >=40:
                print("客队数据量太少不准确")
                # return goal
            if twoLose == 0:
                print("客队数据量太少不准确")
                # return goal
            if oneGoal >=50 :
                print("主队进球率符合，值为" + str(oneGoal))
                print("客队进球率，值为" + str(twoGoal))
                goaldata.append(oneGoal)
                goaldata.append(twoGoal)
                return goaldata
            else:
                print("主队进球率不符合，值为" + str(oneGoal))
                if twoGoal>=50:
                    print("客队进球率符合，值为" + str(twoGoal))
                    goaldata.append(oneGoal)
                    goaldata.append(twoGoal)
                    return goaldata
                else:
                    print("客队队进球率不符合，值为" + str(twoGoal))
                    return goal

# data_rows = grid_data.findAll("tr")
    browser.close()
def thread(data):
    A = data.split("^")
    print("===============" + A[2] + ":   " + A[5] + " vs  " + A[8] + "==================")
    id = A[0].split("\"")[1]
    goal = goalSreach(id)
    if goal:
        print("===============" + A[2] + ": 必中！！！！  " + A[5] + " vs  " + A[8] + "==================")
# 打开chrome浏览器（需提前安装好chromedriver）
# browser = webdriver.Chrome()
# # browser = webdriver.PhantomJS()
# print("正在打开网页...")
# browser.get("http://live.win007.com")
# print("等待网页响应...")
# # 需要等一下，直到页面加载完成
# wait = WebDriverWait(browser, 5)
# wait.until(EC.presence_of_element_located((By.CLASS_NAME, "grid")))
# try:
#     browser.refresh()  #刷新页面
#     print('刷新页面')
# except Exception as e:
#     print('test fail')

print("正在获取网页数据...")
send_headers = {
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Cookie":"Cookie: UM_distinctid=16e67924ce177b-00a9de5d3564f6-6a131775-15f900-16e67924ce2281; detailCookie=0^1^1; Bet007live_hiddenID=_; bfWin007FirstMatchTime=2019,10,18,08,00,00; win007BfCookie=2^0^1^1^1^1^1^0^0^3^0^0^1^2^1^1^0^0^1^0; FS007Filter=1^0^_67_4_114_93_170_242_250_391_423_1061_1122_1366_566_210_467_592_41_448_747_1077_1170_1227_1666_1964_1669_1461_1462_1539_1599_1457_1609_1817_1830_1543_1635_1708_1840_1409_2074_1411_1682_2045_1456_1593_1394_",
    "Host":"live.win007.com",
    "Referer":"http://live.win007.com/",
    "Accept-Encoding":"gzip, deflate",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36",
    "Connection": "keep-alive",
    "Accept-Language": "zh-CN,zh;q=0.9"
    }
header="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
ticks = time.time()
new_ticks = str(ticks).split('.')
url = "http://live.win007.com/vbsxml/bfdata.js?r=007"+new_ticks[0]+"000"
request = urllib.request.Request(url)
request.add_header("User-Agent",header)
request.add_header("Accept","text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8")
request.add_header("Cookie","UM_distinctid=16e67924ce177b-00a9de5d3564f6-6a131775-15f900-16e67924ce2281; detailCookie=0^1^1; bfWin007FirstMatchTime=2019,10,19,09,00,00; win007BfCookie=2^0^1^1^1^1^1^0^0^3^0^0^1^2^1^1^0^0^1^0; Bet007live_hiddenID=_; FS007Filter=1^0^_67_648_90_114_93_54_1366_298_297_336_566_177_428_215_210_358_303_391_504_514_745_423_41_342_120_994_1085_1085_1114_1138_1170_1216_1568_1666_1964_1634_1668_1735_1956_1576_1697_1517_1558_1817_1973_1597_1550_1635_1982_1671_1775_1704_1411_2045_2066_1547_1816_2014_1476_1593_1389_1396_")
request.add_header("Host","live.win007.com")
request.add_header("Referer","http://live.win007.com/")
request.add_header("Accept-Encoding","gzip,deflate")
response = urllib.request.urlopen(request)
DData = gzip.decompress(response.read()).decode('gb2312','ignore').split(";")
Data = [str for str in DData if ('A[' in str) and ("split" in str)]
winGoalData=[]
#获取符合条件的比赛
for data in Data:
    try:
        A=data.split("^")
        state = int(A[13])
        if(state <=0):
            continue
        else:
            match_score = A[14] + "-" + A[15];
        game_id =A[0]
        if(A[13]=="1"):#上半场
            t= A[12].split(",")
            goTime = getTime(t)
            if goTime > 45:
                goTime = "45+"
            if goTime < 1:
                goTime = "1"
            strState = goTime
        elif(A[13]=="2"):#中场休息
            strState = goTime
        elif(A[13] == "3"):#下半场
            t= A[12].split(",")
            goTime=getTime(t)+46
            #选出大于65分钟的比赛进行预测
            if goTime > 65 and goTime<80:
                winGoalData.append(data)
            if goTime>90:
                goTime="90+"
            if goTime<46:
                goTime= "46"
            strState = goTime
        elif(A[13] == "3"):#加时赛
            strState = goTime
        elif(A[13] == "4"):#点球
            strState = goTime
    except Exception :
        # print(data)
        continue
#获取比赛数据判断是否符合
if winGoalData:
    for data in winGoalData:
        # threading.Thread(target=thread(data)).start()
        thread(data)
        # if goal:
        #     print(data[2] + ":   " + data[5] + " vs  " + data[8])
else:
    print("没有符合条件的比赛")
system("pause")




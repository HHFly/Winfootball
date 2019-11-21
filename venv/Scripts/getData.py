import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def find_all_index(arr,item):
    return [i for i,a in enumerate(arr) if a==item]

def goalSreach(id):
# 打开chrome浏览器（需提前安装好chromedriver）
    option = webdriver.ChromeOptions()
    # option.add_argument('headless')  # 静默模式
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

goalSreach("1751676")
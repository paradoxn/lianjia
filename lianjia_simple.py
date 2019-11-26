import bs4
import requests
import time  # 引入time，计算下载时间
import json



def open_url(url):  ##使用随机代理访问网页，若代理失效，使用其他代理。
    hd = {}
    hd['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36'
    r = requests.get(url, headers=hd, timeout=30)
    return r

def get_map(address):  # 从百度地图api根据地址获取经纬度
    url='http://api.map.baidu.com/geocoder/v2///?address={}&output=json&ak=dASz7ubuSpHidP1oQWKuAK3q'.format(address)
    html = requests.get(url)
    content = json.loads(html.text)
    if content['status'] == 0:
        location = content['result']['location']
        return location['lng'],location['lat']
    else:
        return None,None

def get_info(detail_url): #detail_url指每个房子的详情链接
    soup1 = bs4.BeautifulSoup(open_url(detail_url).text, 'lxml')
    title = soup1.find_all('h1', class_='main')[0].text.split()
    content = soup1.find_all("div", class_="content")[2].find_all('li')
    try:
        c0 = content[0].contents[1].strip()#get_text() #房屋户型
        c1 = content[1].contents[1].strip() #所在楼层
        c2 = content[2].contents[1].strip() #建筑面积
        c3 = content[3].contents[1].strip() #户型结构
        c4 = content[4].contents[1].strip() #套内面积
        c5 = content[5].contents[1].strip() #建筑类型
        c6 = content[6].contents[1].strip() #房屋朝向
        c7 = content[7].contents[1].strip() #建筑结构
        c8 = content[8].contents[1].strip() #装修情况
        c9 = content[9].contents[1].strip() #梯户比例
        c10 = content[10].contents[1].strip() #配备电梯
        c11 = content[11].contents[1].strip() #产权年限
    except Exception as E:
        print(E)
        c9 = None
        c10 = None
        c11 = None

    trans = soup1.find_all("div", class_="content")[3].find_all('li')
    t0 = trans[0].find_all('span')[1].get_text()#.strip() #挂牌时间
    t1 = trans[1].find_all('span')[1].get_text() #交易权属
    t2 = trans[2].find_all('span')[1].get_text() #上次交易
    t3 = trans[3].find_all('span')[1].get_text() #房屋用途
    t4 = trans[4].find_all('span')[1].get_text() #房屋年限
    t5 = trans[5].find_all('span')[1].get_text() #产权所属
    t6 = trans[6].find_all('span')[1].get_text().strip() #抵押信息
    t7 = trans[7].find_all('span')[1].get_text().strip() #房本备件
    try:
        t8 = trans[8].find_all('span')[1].get_text().strip() #房协编码
    except:
        t8 = None

    houseinfo = soup1.find('div',class_='houseInfo').find_all('div')
    room1 = houseinfo[1].get_text() #房间数
    room2 = houseinfo[2].get_text() #楼层情况
    type1 = houseinfo[4].get_text() #朝向
    type2 = houseinfo[5].get_text() #装修
    area1 = houseinfo[7].get_text() #平方米
    area2 = houseinfo[8].get_text() #建筑年代/类型

    region = soup1.find_all("span", class_="info")[0].text.split()[0]  #所在区域

    id = "".join(list(filter(str.isdigit,detail_url)))
    houseseerecord_url='https://sz.lianjia.com/ershoufang/houseseerecord?id={}'.format(id)# 带看次数
    totalcount=json.loads(open_url(houseseerecord_url).text)['data']['totalCnt']  #近30日带看人数

    total_price = soup1.find_all('div', class_='price')[0].find('span',class_='total').get_text() #总价格
    per_price = soup1.find_all('div', class_='price')[0].find('span', class_='unitPriceValue').get_text().replace('元/平米','') #每平方价格

    communityName = soup1.find('div',class_='communityName').find('a').get_text() #小区名字
    address = ""
    info = soup1.find_all("span", class_="info")[0].text.split()
    for i in info:
        address = address + str(i)
    address = "深圳市" + address+ communityName
    lng,lat = get_map(address)  #得到经纬度

    aa = []
    try:
        detail = soup1.find('div',id="infoList").find_all('div',class_='col')

        for i in detail:
            aa.append(i.get_text())
    except:
        aa= ['None']
    print(id,c0,c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,c11,t0,t1,t2,t3,t4,t5,t6,t7,t8,room1,room2,type1,type2,area1,area2,region,int(totalcount),float(total_price),float(per_price),communityName,lng,lat,str(aa),str(title),detail_url)
    global count
    count += 1
    print('\r' + "已经下载：" + int(count / all_count * 100) * "█" + "【" + str(
        round(float(count / all_count) * 100, 2)) + "%" + "】", end='')


if __name__ == "__main__":
    start = time.time()
    f = open('szlianjia.txt')
    a = f.readlines()
    all_count = len(a)
    count = 0
    for i in a:
        detail_url = i.replace('\n','')
        get_info(detail_url)
        time.sleep(0.5)

    end = time.time()
    print("总耗时:" + str(end - start) + "秒")


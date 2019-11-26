import bs4
import requests
import time  # 引入time，计算下载时间

def open_url(url):
    hd = {}
    hd['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36'
    r = requests.get(url, headers=hd, timeout=30)
    return r

if __name__ == "__main__":
    regions = ['luohuqu', 'futianqu', 'nanshanqu', 'yantianqu', 'baoanqu', 'longgangqu', 'longhuaqu', 'guangmingqu',
               'pingshanqu', 'dapengxinqu']  ##深圳市区域拼音
    start = time.time()
    whvj = []
    for region in regions:
        count = 1
        size = 0
        q = 100
        host = 'https://sz.lianjia.com/ershoufang/{}/pg'.format(region)
        while count <= q:
            url = host + str(count)
            r = open_url(url)
            soup = bs4.BeautifulSoup(r.text, 'html.parser')
            count = count + 1

            targets = soup.find_all('a', class_="img")[:29]
            for each in targets:
                detail_url = each['href']
                # get_info(detail_url)
                #whvj.append(each['href'])
                with open('szlianjia.txt', 'a', encoding='utf-8') as f:
                    f.write(each['href'] + "\n")

            print('\r' + region + "已经下载：" + int((count-1) / q * 100) * "█" + "【" + str(round(float((count-1) / q) * 100, 2)) + "%" + "】", end=url)

    response = requests.get(url, stream=True)  # stream参数设置成True时，它不会立即开始下载，当你使用iter_content或iter_lines遍历内容或访问内容属性时才开始下载
    end = time.time()
    print("总耗时:" + str(end - start) + "秒")
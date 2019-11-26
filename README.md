# lianjia
各文件介绍:

1.get_lianjia.py  该脚本为获取深圳链家所有区域(南山/罗湖等)的二手房网址.可得到szlianjia.txt文件.

2.lianjia_simple.py 该脚本是获取szlianjia.txt里所有网址的房屋详细信息.并打印出来(单线程爬虫,不使用代理ip)

3.lianjia.py 该脚本是获取szlianjia.txt里所有网址的房屋详细信息并写入本地的mysql数据库.(多线程爬虫,同时使用代理ip)

4.metro.xlsx 是深圳地区所有地铁站的坐标.

5.lianjia_secondhand.csv 是已爬好的约2万条房产数据情况.


6.jupyter数据分析过程.ipynb 是使用jupyter notebook的数据分析全过程.

7.数据分析详情.html 数据分析全过程的html格式.

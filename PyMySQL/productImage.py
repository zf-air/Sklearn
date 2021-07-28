# -*- coding = utf-8 -*-
# @Time : 2021/7/19 9:47
# @Author : zxh
# @File : paqufangjia.py
# @Software : PyCharm
import requests
import parsel
import csv
import pymysql
from pyecharts import options as opts
from pyecharts.charts import Bar

chengqu=[]
chengqu_h=[]
junjia=[]


def main():
    citysum = 0
    ccity = input('请输入城市:')
    user_in_city,colour,limit=query(ccity, chengqu, chengqu_h)
    print(chengqu)
    print(chengqu_h)
    print(user_in_city)
    print(colour)
    print(limit)
    print("正在爬取数据，请稍等。。。")
    for i in range(0, limit):
        user_in_area = chengqu[i]
        #a=getInformation(user_in_city, user_in_area)
        junjia.append(getInformation(user_in_city, user_in_area))
        citysum=citysum+int(junjia[i])
    cityavr=citysum/limit
    cityavr=round(cityavr)
    cityavr=str(cityavr)
    print("获取完成！-------------------------------")
    for i in range(0,limit):
        print(chengqu_h[i]+"均价为:"+junjia[i]+"元每平米")
    print(ccity+"市均价为："+cityavr+"元每平米")
    print("统计完成！-------------------------------")


    #更新数据库
    for i in range(0, limit):
        updatechengqu(chengqu[i],junjia[i])
    updatecity(ccity,cityavr)
    print("数据库更新完毕！")


    productImage(ccity,limit,chengqu_h,colour)
    print("生成统计图成功！-------------------------------")


def query(ccity,chengqu,chengqu_h):
    print("正在从数据库中查询，请稍等：")
    db = pymysql.connect(host="localhost", user="root", password="zhangfan789..", database="homeless", charset="utf8mb4")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM chengqu WHERE c_city = '%s'" % ccity)
    results = cursor.fetchall()

    for row in results:
        chengqu.append(row[1])
        chengqu_h.append(row[3])

    user_in_city = row[0]
    db.close()

    db = pymysql.connect(host="localhost", user="root", password="zhangfan789..", database="homeless", charset="utf8mb4")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM color WHERE city_cname = '%s'" % ccity)
    r = cursor.fetchall()

    for row in r:
        colour = row[1]
        limit = row[2]
    db.close()
    return user_in_city,colour,limit


def updatechengqu(chengqu,junjia):#更新城区均价
    db = pymysql.connect(host="localhost", user="root", password="zhangfan789..", database="homeless", charset="utf8mb4")
    cursor = db.cursor()
    cursor.execute("UPDATE chengqu SET junjia = '%s' WHERE p_qu='%s'"%(junjia,chengqu))
    db.commit()
    db.close()


def updatecity(cityname,shijunjia):# 更新市均价
    db = pymysql.connect(host="localhost", user="root", password="zhangfan789..", database="homeless", charset="utf8mb4")
    cursor = db.cursor()
    cursor.execute("UPDATE color SET shijunjia = '%s' WHERE city_cname='%s'" % (shijunjia, cityname))
    db.commit()
    db.close()




def getInformation(user_in_city,user_in_area):
    sum = 0
    count = 0
    url = 'http://' + user_in_city + '.lianjia.com/ershoufang/pg{}rs' + user_in_area + '/'
    for a in range(1, 4):
        url1 = url.format(a)
        #print(f'\n=========正在抓取第{a}页的数据===============')
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; X64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36'}
        response = requests.get(url=url1, headers=headers)
        # 模拟向浏览器发出请求
        html_data = response.text
        # 字符串
        # print(html_data)

        # 数据解析
        # css数据选择器提取HTML数据,转换数据类型
        selector = parsel.Selector(html_data)
        # 抓取所有的li,返回的是列表
        lis = selector.css('.clear.LOGCLICKDATA')

        for li in lis:
            title = li.css('.title a::text').get()  # 提取标题
            address = li.css('.positionInfo a::text').getall()  # 可能有两个a标签
            address = '_ '.join(address)  # 连接两个a标签
            introduce = li.css('.houseInfo ::text').get()
            star = li.css('.followInfo ::text').get()
            tags = li.css('.tag span ::text').getall()
            tags = ','.join(tags)
            totalPrice = li.css('.priceInfo .totalPrice span::text').get() + '万'
            unitPrice = li.css('.unitPrice span::text').get()

            unitPrice_int = int(unitPrice.replace("单价", "").replace("元/平米", ""))
            count += 1
            sum = sum + unitPrice_int
            #print(title, address, introduce, tags, totalPrice, unitPrice, sep='******')

            with open('链家5.csv', mode='a', encoding='utf-8', newline='') as f:
                csv_write = csv.writer(f)
                csv_write.writerow([title, address, introduce, tags, totalPrice, unitPrice])

    avr=round(sum/count)#取整后保存平均值
    avr=str(avr)
    print(avr)
    return avr


def productImage(cityname,limit,chengqu_h,colors):
    from pyecharts import options as opts
    from pyecharts.charts import Bar
    l1 = chengqu_h[0:limit]
    #l1 = ['二七区', '惠济区', '中原区', '高新区', '金水区', '经开区', '郑东新区', '管城回族区', '航空港区', '上街区']
    l2 = junjia[0:limit]
    bar = (
        Bar()
            .add_xaxis(l1)
            .add_yaxis(cityname+"各区:", l2, category_gap=20, color=colors)
            .set_global_opts(
            legend_opts=opts.LegendOpts(
                textstyle_opts=opts.TextStyleOpts(
                    font_size=14,
                    font_family='Times New Roman',
                ),
            ),
            xaxis_opts=opts.AxisOpts(
                name="城区",
                name_rotate=0,
                name_textstyle_opts=opts.TextStyleOpts(
                    font_family='Times New Roman',
                    font_size=16,
                ),
                axislabel_opts=opts.LabelOpts(
                    rotate=25,
                    font_size=16,
                    font_weight=200,
                    font_family='Microsoft YaHei',
                ),

            ),
            yaxis_opts=opts.AxisOpts(
                name="平均单价/元每平米",
                name_rotate=0,
                name_textstyle_opts=opts.TextStyleOpts(
                    font_family='Times New Roman',
                    font_size=14,
                ),
                axislabel_opts=opts.LabelOpts(
                    rotate=0,
                    font_size=16,
                    font_family='Times New Roman',
                ),

            ),

            title_opts=opts.TitleOpts(title=cityname+"城区房产均价（近一个月数据）",
                                      subtitle="",
                                      title_textstyle_opts=opts.TextStyleOpts(
                                          color=colors,
                                          font_size=12,
                                          font_family='Times New Roman',
                                          font_weight='bold',

                                      ),

                                      ),

        )
    )
    bar.render('PyMySQL/' + cityname + '.html')


if __name__ == "__main__":
    main()

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import re
import time
import pypinyin

# 加载爬虫所需要的一些python包
import requests
from lxml import etree
from tqdm import tqdm  # 进度条
import pandas as pd

# 我们需要抓取的结果，如房源、面积、价格、区域以及租房方式
city_name = 'nj'

house_list, money_list, location_list,house_info_list = [], [], [], []
rent_year_list, floor_list, advantage_list = [], [], []


#抓取城市各个区的名称
def get_city_part(city_name):

    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
    cookies = {'Cookie':'lianjia_uuid=1f89edf0-b4ab-46fa-abf1-0648a2de4332; UM_distinctid=165bcdf950212f-0bdda8e5337159-737356c-1fa400-165bcdf95030; _smt_uid=5b94b42b.53f5d53b; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22165bcdfcb21c4-0ac1926bfd9e6a-737356c-2073600-165bcdfcb237c4%22%2C%22%24device_id%22%3A%22165bcdfcb21c4-0ac1926bfd9e6a-737356c-2073600-165bcdfcb237c4%22%2C%22props%22%3A%7B%7D%7D; Qs_lvt_200116=1536472162; select_city=320100; ke_uuid=7121c302229b4177e98f6e27295328f1; _ga=GA1.2.1344147602.1536472168; _gid=GA1.2.2097624835.1536472168; www_zufangzi_server=0ca0f641b9b44a3586617f59ad4d8f06; Qs_pv_200116=1565007462557283300%2C512333916070716900; lianjia_ssid=26cfa475-6d59-4e69-9a1c-0d63f8f9538a; CNZZDATA1273627291=1742325173-1536468423-https%253A%252F%252Fnj.ke.com%252F%7C1536479224; lianjia_token=2.004e85d55536574e7e5f28fc64a5ea6016'}
    res = requests.get(url = city_url, cookies = cookies, headers = headers)
    if res.status_code == 200:
        print('房源网页抓取成功！')
    else:
        print('房源网页抓取失败！')
    res.encoding = 'utf-8'
    x = etree.HTML(res.text)
    city_part_list = x.xpath('//ul[@data-target="area"]/li[position() != 1]/a/text()')

    def hp(word): # 汉字转拼音

        city_list = []
        for every_city in word:
            s = ''
            for i in pypinyin.pinyin(every_city, style=pypinyin.NORMAL):
                s += "".join(i)
            city_list.append(s)
        return city_list
    return hp(city_part_list)


def get_house_basic_info(basic_info_url): #抓取每间房源网页链接里的房屋基本信息
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
    cookies = {'Cookie':'lianjia_uuid=1f89edf0-b4ab-46fa-abf1-0648a2de4332; UM_distinctid=165bcdf950212f-0bdda8e5337159-737356c-1fa400-165bcdf95030; _smt_uid=5b94b42b.53f5d53b; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22165bcdfcb21c4-0ac1926bfd9e6a-737356c-2073600-165bcdfcb237c4%22%2C%22%24device_id%22%3A%22165bcdfcb21c4-0ac1926bfd9e6a-737356c-2073600-165bcdfcb237c4%22%2C%22props%22%3A%7B%7D%7D; Qs_lvt_200116=1536472162; select_city=320100; ke_uuid=7121c302229b4177e98f6e27295328f1; _ga=GA1.2.1344147602.1536472168; _gid=GA1.2.2097624835.1536472168; www_zufangzi_server=0ca0f641b9b44a3586617f59ad4d8f06; Qs_pv_200116=1565007462557283300%2C512333916070716900; lianjia_ssid=26cfa475-6d59-4e69-9a1c-0d63f8f9538a; CNZZDATA1273627291=1742325173-1536468423-https%253A%252F%252Fnj.ke.com%252F%7C1536479224; lianjia_token=2.004e85d55536574e7e5f28fc64a5ea6016'}
    res = requests.get(url=basic_info_url, cookies=cookies, headers=headers)
    x = etree.HTML(res.text)
    rent_year = x.xpath('//div[@class="content__article__info"]/ul/li[5]/text()')[0] #租用时限
    floor = x.xpath('//div[@class="content__article__info"]/ul/li[8]/text()')[0] #楼层高度
    advantage = "|".join(x.xpath('//p[@class="content__aside--tags"]/i/text()')) # 优势特点
    return rent_year, floor, advantage



def get_house(city_part): #抓取租金，房源位置，发布信息等
    city_part_url = 'https://'+city_name+'.zu.ke.com/zufang/'+city_part+'/'+n_type
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
    cookies = {'Cookie':'lianjia_uuid=1f89edf0-b4ab-46fa-abf1-0648a2de4332; UM_distinctid=165bcdf950212f-0bdda8e5337159-737356c-1fa400-165bcdf95030; _smt_uid=5b94b42b.53f5d53b; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22165bcdfcb21c4-0ac1926bfd9e6a-737356c-2073600-165bcdfcb237c4%22%2C%22%24device_id%22%3A%22165bcdfcb21c4-0ac1926bfd9e6a-737356c-2073600-165bcdfcb237c4%22%2C%22props%22%3A%7B%7D%7D; Qs_lvt_200116=1536472162; select_city=320100; ke_uuid=7121c302229b4177e98f6e27295328f1; _ga=GA1.2.1344147602.1536472168; _gid=GA1.2.2097624835.1536472168; www_zufangzi_server=0ca0f641b9b44a3586617f59ad4d8f06; Qs_pv_200116=1565007462557283300%2C512333916070716900; lianjia_ssid=26cfa475-6d59-4e69-9a1c-0d63f8f9538a; CNZZDATA1273627291=1742325173-1536468423-https%253A%252F%252Fnj.ke.com%252F%7C1536479224; lianjia_token=2.004e85d55536574e7e5f28fc64a5ea6016'}
    res = requests.get(url=city_part_url, cookies=cookies, headers=headers)
    res.encoding = 'utf-8'
    if res.status_code == 200:
        print('{}房源已爬取成功！'.format(city_part))
    else:
        print('{}房源爬取失败！'.format(city_part))
    x = etree.HTML(res.text)
    city_part_number = x.xpath('//div[@class="content__pg"]/@data-totalpage')
    print('{}一共有{}页房源信息！'.format(city_part, city_part_number[0]))
    for i in tqdm(range(0,int(city_part_number[0]))): #按页数爬取租房信息
        new_part_url = 'https://'+city_name+'.zu.ke.com/zufang/'+city_part+'/pg'+'%d' % i+'/'+n_type
        new_res = requests.get(url=new_part_url, cookies=cookies, headers=headers)
        new_res.encoding = 'utf-8'
        if new_res.status_code == 200:
            print('{}第{}页房源已爬取成功！'.format(city_part,i+1))
        else:
            print('{}第{}页房源爬取失败！'.format(city_part,i+1))
        y = etree.HTML(new_res.text)
        global house_list,money_list, location_list, house_info_list, rent_year_list, floor_list, advantage_list #将house_list定义为全局变量
        n = len(y.xpath('//div[@class="content__list"]/div'))
        for n in range(1,n+1):
            pre_house_list = y.xpath('//div[@class="content__list"]/div[{}]/div[@class="content__list--item--main"]/p[@class="content__list--item--title twoline"]/a[@target="_blank"]/text()'.format(n))
            house_list.append(pre_house_list[0].strip())
            money_list.append(y.xpath('//div[@class="content__list"]/div[{}]/div[@class="content__list--item--main"]/span/em/text()'.format(n))[0])
            house_loc = y.xpath('//div[@class="content__list"]/div[{}]/div[@class="content__list--item--main"]/p[@class="content__list--item--des"]/a/text()'.format(n))
            location_list.append("".join(house_loc))
            house_info_pre = y.xpath('//div[@class="content__list"]/div[{}]/div[@class="content__list--item--main"]/p[@class="content__list--item--des"]/text()'.format(n))
            house_info_list.append("".join([m.strip() for m in house_info_pre]))
            basic_info_url = 'https://'+city_name+'.zu.ke.com/'+y.xpath('//div[@class="content__list"]/div[{}]/a[@class="link"]/@href'.format(n))[0]

            rental_company = y.xpath('//div[@class="content__list"]/div[{}]/div[@class="content__list--item--main"]/p[@class="content__list--item--brand oneline"]/text()'.format(n))[0].strip()
            if rental_company != '链家':
                rent_year, floor, advantage = '', '', ''
            else:
                rent_year, floor, advantage = get_house_basic_info(basic_info_url)#调用房屋基本信息函数，获取租用年份，房屋层数，优势等信息

            rent_year_list.append(rent_year)
            floor_list.append(floor)
            advantage_list.append(advantage)
            time.sleep(0.1) #


def main(city_name):
    global city_url
    city_urls = ['rt200600000001/', 'rt200600000002/'] #整租，合租
    global n_type
    for number,n_type in enumerate(city_urls):
        city_url = 'https://' + city_name + '.zu.ke.com/zufang/'+n_type
        for i in get_city_part(city_name):
            if (i == 'gaochun' and n_type == 'rt200600000001/') or (i in ('lishui','gaochun') and n_type == 'rt200600000002/'):
                continue
            get_house(i)

        all_house = {'house':house_list, 'money':money_list, 'location': location_list,'house_info':house_info_list, 'rent_year':rent_year_list, 'floor':floor_list, 'advantage':advantage_list}
        data = pd.DataFrame(all_house)
        data.to_csv(city_name+'%d' % number+'_house_infos.csv',columns=['house','money','location','house_info','rent_year','floor','advantage'])
        print(city_url+'所有租房信息已爬取完毕!')




if __name__ == '__main__':
    main(city_name)


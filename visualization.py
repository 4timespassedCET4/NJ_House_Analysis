#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 加载分析过程中一些必要的包

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
import seaborn as sn
import pyecharts

# 数据清洗
house = pd.read_csv('C:/Users/ASUS/Desktop/nj1_house_infos.csv',encoding='gbk')

def info_area_clean(s): #定义清洗面积的函数，通过正则表达式以m为分隔符提取面积
    temp = s.split('㎡')[0]
    if temp[0] == '-':
        return int(temp[1:])
    elif re.search(r'\d+-\d+',temp) != None:
        num1, num2 = temp.split('-')
        return (int(num1)+int(num2))/2
    else:
        return int(temp)

house['area'] = house.house_info.apply(info_area_clean)

def info_toward_clean(s): #提取房屋信息中的方位
    result = ''
    for i in s:
        if i in ['东','南','西','北']:
            result += i
    return (result)

house['toward'] = house.house_info.apply(info_toward_clean)

house['apartment'] = house.house_info.apply(lambda x: x[-6:]) #提取租房的户型

def money_clean(s): #清洗租金，租金中大部分都是一个数字，但有的是类似于1500-1700这种，我们采用其平均价位来代替其价格
    if '-' in s:
        num1, num2 = s.split('-')
        return (int(num2) + int(num1)) / 2
    else:
        return int(s)

house['money'] = house.money.apply(money_clean)

house = house.drop('house_info',axis=1) #删除House_info这一列
house.loc[house['location'].isna(),'location'] = house.loc[house['location'].isna()].house.apply(lambda x : x.split()[1]) #location公寓的有缺失位置进行处理

#可视化分析
#房屋户型分布数量前十柱形图
z = house.apartment.value_counts()[:10].sort_values()
bar = pyecharts.Bar("房屋户型分布前十","南京·NanJing")
bar.add(z,z.index,y_axis = list(z.values),is_convert= True,is_label_show =True,label_pos = 'inside',label_color = ["#996666"])
bar.render("南京租房房屋户型分析.html")

#各行政区房屋租赁数量分布及占比
part = house.part.value_counts().sort_values()
part_bar = pyecharts.Bar("各行政区房屋租赁数量分布及占比","南京·NanJing")
part_bar.add(part,part.index,part.values,is_label_show = True,label_color = ['#999999'],is_convert = True,label_pos = "inside")

pie_part = pyecharts.Pie(title_pos = "40%")
pie_part.add(part,part.index,part.values,is_label_show = True,legend_pos = '90%',legend_orient="vertical",center = [65,50])

grid = pyecharts.Grid(page_title="各行政区房屋租赁数量分布及占比",width=1200)
grid.add(part_bar,grid_right = "60%")
grid.add(pie_part,grid_left = "50%")
grid.render("南京租房数量分析.html")

#了解一下不同地区租房平均情况
single_price = round(house.loc[house.house_type == 'single'].money.groupby(house.loc[house.house_type == 'single']['part']).mean(),0)
all_price = round(house.loc[house.house_type == 'all'].money.groupby(house.loc[house.house_type == 'all']['part']).mean(),0)
line = pyecharts.Line("各行政区租房价格·¥","南京·NanJing")
line.add("整租",all_price.index,all_price.values,is_label_show = True)
line.add("合租",single_price.index,single_price.values,is_label_show = True)
line.render("南京租房房价分析.html")

#房屋不同朝向数量
toward = house.toward.value_counts()[:8]
bar = pyecharts.Bar("房屋不同朝向数量","南京·NanJing")
bar.add(toward,toward.index,toward.values,label_color = ['#996666'],is_label_show = True)
bar.render("南京租房朝向分析.html")

#租房面积分布
sn.set_style("whitegrid")
plt.figure(figsize=(12,8))
sn.distplot(house.area[house.area < 200])
plt.title("The Distribution of House Area")
plt.xlabel('House Area')
plt.show()
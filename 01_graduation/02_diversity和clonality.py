#在jupyter lab里用pyecharts画图要加上这两句
from pyecharts.globals import CurrentConfig, NotebookType
CurrentConfig.NOTEBOOK_TYPE = NotebookType.JUPYTER_LAB

from pyecharts import options as opts
from pyecharts.globals import ThemeType
import pandas as pd
from pyecharts.charts import Bar,Grid,Line

import math
import numpy as np

#unique克隆越多，diversity越高，所需数据只要AASeq和cloneFraction两列
df = pd.read_csv('PRJNA330606.tsv',sep ='\t',header=0)
df = df[['AASeq','cloneFraction']]

#对AAseq进行去重，合并cloneFraction
df1 = df.groupby(['AASeq']).agg({'cloneFraction':sum}).reset_index()
#len()返回dataframe行数
N = len(df1)
SUM = sum(df1['cloneFraction'])

#如果用R的vegan包，不需要对cloneFraction进行归一化处理（内部会自行归一化），但自己写的代码需要保证cloneFraction相加为1
#对dataframe某一列进行相同的操作，用df.map(lambda x: fx)
df1['cloneFraction'] = df1['cloneFraction'].map(lambda x: x/SUM, na_action='ignore')

#自定义diversity函数
def diversity(ll):  #由于输入的α是不连续的数值，因此记得将输出值和输入值的形式写成列表
    result = []  #空列表
    for j in ll:  #对于不同的输入值，用if进行判断
        if j==1:
            s = 0
            for i in range(N):
                s = s + df1.iloc[i,1] * math.log(df1.iloc[i,1])
            d = -1*s
        elif j==2:
            s = 0
            for i in range(N):
                s = s + pow(df1.iloc[i,1],2)
            d = -1*math.log(s)
        elif j==math.inf:
            d = -1*math.log(max(df1['cloneFraction'].values.tolist()))       
        else:
            s = 0
            for i in range(N):
                s = s + pow(df1.iloc[i,1],j)
            d = math.log(s)/(1-j)
        result.append(d)  #最后输出形式为列表
    return(result) 

#因为定义函数时输入为列表，那么0,0.25,0.5,1,2,4,8,16,32,64,math.inf使用函数时就不用循环了，而是直接以列表形式作为输入
#多个自变量组成列表进行函数运算
ss = diversity([0,0.25,0.5,1,2,4,8,16,32,64,math.inf])

#横纵坐标要求输入形式为列表，且横坐标里的元素是str形式
#pyecharts画图的时候一定要弄清楚输入的数据类型，直接看x，y输出的内容是否符合要求
x = [0,0.25,0.5,1,2,4,8,16,32,64,math.inf]
αx = [str(i) for i in x]

line=(
    Line()
    .set_global_opts(
        title_opts=opts.TitleOpts(title="多样性", pos_left="center"),
        tooltip_opts=opts.TooltipOpts(is_show=False),
        xaxis_opts=opts.AxisOpts(type_="category",name = 'α'),
        yaxis_opts=opts.AxisOpts(
            type_="value",
            name = 'diversity',
            axistick_opts=opts.AxisTickOpts(is_show=True),
            splitline_opts=opts.SplitLineOpts(is_show=True),
        )
    )
    .add_xaxis(xaxis_data=αx)
    .add_yaxis(
        series_name="",
        y_axis=ss,
        label_opts=opts.LabelOpts(is_show=False)
    )
)
line.load_javascript()

line.render_notebook()

#clonolity
def clonality(df):
    s = df.map(lambda x: x*math.log(x), na_action='ignore').sum()
    c = -1*s/math.log(N)
    #直接用Pielou‘s index求出来的和我们预期的趋势相反，因此要用1-Pielou‘s index
    return(1-c)
result_clonality = clonality(df1['cloneFraction'])  

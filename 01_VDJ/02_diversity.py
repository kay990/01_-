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

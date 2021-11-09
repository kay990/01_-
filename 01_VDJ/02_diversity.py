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


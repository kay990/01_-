#在jupyter lab中用pyecharts画图需要加上这两句
from pyecharts.globals import CurrentConfig, NotebookType
CurrentConfig.NOTEBOOK_TYPE = NotebookType.JUPYTER_LAB

from pyecharts.charts import Grid
import random
import numpy as np
from pyecharts import options as opts
import pandas as pd
from collections import Counter
from pyecharts.charts import HeatMap

#导入TCR数据，包括 AASeq	cloneFraction	Vregion	Dregion	Jregion	RunId 等信息
df = pd.read_csv('PRJNA330606.tsv', sep='\t', header=0)

#按VJ分组（groupby）-去重（将重复VJ的clonefraction相加，agg）-将分好的组再合并起来（reset_index）
hm_data = df.groupby(['Vregion', 'Jregion']).agg({'cloneFraction':sum}).reset_index()

#上一步去过重，但是是对于VJ联合而言的，对于V或者J单个而言还是有重复的，单列去重用Counter（字符串/列表/数组输入，输出字典）
#字典形式变成dataframe用pd.DataFrame.from_dict，
V = pd.DataFrame.from_dict(Counter(hm_data.Vregion.values), orient = 'index', columns = ['values']).index.tolist()
J = pd.DataFrame.from_dict(Counter(hm_data.Jregion.values), orient = 'index', columns = ['values']).index.tolist()

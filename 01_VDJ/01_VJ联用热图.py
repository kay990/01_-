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


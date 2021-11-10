from pyecharts.globals import CurrentConfig, NotebookType
CurrentConfig.NOTEBOOK_TYPE = NotebookType.JUPYTER_LAB

from pyecharts import options as opts
from pyecharts.globals import ThemeType
import pandas as pd
from pyecharts.charts import Bar,Grid

import matplotlib.pyplot as plt
import numpy as np
from collections import Counter

df = pd.read_csv('PRJNA330606.tsv', sep='\t', header=0)

#序列长度分布
a = pd.DataFrame(df.AASeq)
array = np.empty([len(a.index), 1], dtype = int)
for i in range(len(a.index)):
    array[i, 0] = len(a.iloc[i, 0])
length = pd.DataFrame(array)
length.columns = ['len']
dict_data = Counter(length.len.values)
bar_data = pd.DataFrame.from_dict(dict_data, orient = 'index', columns = ['values'])
bar_data1 = bar_data.reset_index()
bar_data1.columns = ['length', 'times']
bar_data1 = bar_data1.sort_values(by = 'length')
bar_data2 = bar_data1[(bar_data1['length'] >= 8)&(bar_data1['length'] <= 20)]

bar_AAseq=(
    Bar()
    .add_xaxis(bar_data2.length.tolist())
    .add_yaxis('', bar_data2.times.tolist())
    .set_global_opts(title_opts = opts.TitleOpts(title = 'Length Distribution', pos_left = '40%'),
                    xaxis_opts = opts.AxisOpts(name = 'AAseq-Length', name_location = 'middle', 
                                               name_textstyle_opts = opts.TextStyleOpts(font_size = 16),
                                              name_gap = 30),
                    yaxis_opts = opts.AxisOpts(name = 'Counts', name_location = 'middle', 
                                               name_textstyle_opts = opts.TextStyleOpts(font_size = 16),
                                              name_gap = 50))
)
bar_AAseq.load_javascript()

bar_AAseq.render_notebook()

#Jregion distribution
J = pd.DataFrame(df.Jregion)
Jg = Counter(J.Jregion.values)
bar_J = pd.DataFrame.from_dict(Jg, orient = 'index', columns = ['values']).reset_index()
#改列名
bar_J.columns = ['Jregion', 'Counts']
#按照重复大小排序
bar_J1 = bar_J.sort_values(by = 'Counts', ascending = False)
#只保留counts>300的J基因
bar_J1 = bar_J1[bar_J1['Counts']>0]

bar_Jregion = (
    Bar(init_opts=opts.InitOpts(width = "1900px", height = '400px'))
    #柱状图输入数据类型是列表
    .add_xaxis(bar_J1.Jregion.tolist())
    .add_yaxis('', bar_J1.Counts.tolist(), label_opts = opts.LabelOpts(is_show = False))
    .set_global_opts(title_opts = opts.TitleOpts(title = 'Jregion Distribution', pos_left = '40%'),
                    xaxis_opts = opts.AxisOpts(name = 'Jregion', name_location = 'middle', 
                                               name_textstyle_opts = opts.TextStyleOpts(font_size = 16),
                                              name_gap = 40, axislabel_opts = {'rotate': 30}),
                    yaxis_opts = opts.AxisOpts(name = 'Counts', name_location = 'middle', 
                                               name_textstyle_opts = opts.TextStyleOpts(font_size = 16),
                                              name_gap = 50))
)
bar_Jregion.load_javascript()

bar_Jregion.render_notebook()

#Vregion distribution
v = pd.DataFrame(df.Vregion)
vg = Counter(v.Vregion.values)
bar_v = pd.DataFrame.from_dict(vg, orient = 'index', columns = ['values'])
bar_v = bar_v.reset_index()
bar_v.columns = ['Vregion', 'Counts']
bar_v1 = bar_v.sort_values(by = 'Counts', ascending = False)
bar_v1 = bar_v1[bar_v1['Counts']>3000]

bar_Vregion = (
    Bar(init_opts=opts.InitOpts(width = "1900px", height = '400px'))
    .add_xaxis(bar_v1.Vregion.tolist())
    .add_yaxis('', bar_v1.Counts.tolist(), label_opts = opts.LabelOpts(is_show = False))
    .set_global_opts(title_opts = opts.TitleOpts(title = 'Vregion Distribution', pos_left = '40%'),
                    xaxis_opts = opts.AxisOpts(name = 'Vregion', name_location = 'middle', 
                                               name_textstyle_opts = opts.TextStyleOpts(font_size = 16),
                                              name_gap = 40, axislabel_opts = {'rotate': 30}),
                    yaxis_opts = opts.AxisOpts(name = 'Counts', name_location = 'middle', 
                                               name_textstyle_opts = opts.TextStyleOpts(font_size = 16),
                                              name_gap = 50))
)
bar_Vregion.load_javascript()

bar_Vregion.render_notebook()

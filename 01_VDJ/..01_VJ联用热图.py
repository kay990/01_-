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
#字典形式变成dataframe用pd.DataFrame.from_dict，‘index’和‘values’是固定的，.index（取索引名，也就是行名）.tolist（变成列表）
V = pd.DataFrame.from_dict(Counter(hm_data.Vregion.values), orient = 'index', columns = ['values']).index.tolist()
J = pd.DataFrame.from_dict(Counter(hm_data.Jregion.values), orient = 'index', columns = ['values']).index.tolist()

#创建全零dataframe，行列是unique的VJ
zero_df = pd.DataFrame(np.zeros([len(V), len(J)], dtype = int))
zero_df.index = V
zero_df.columns = J

#将原dataframe里合并后的clonefraction放入以V,J为行列名的dataframe里
#df.loc[]参数是标签，df.iloc[]参数是索引(从0开始)
for column in J:
    for row in V:
        if(len(hm_data[(hm_data.Vregion==row)&(hm_data.Jregion==column)])==1):
            zero_df.loc[row, column] = hm_data[(hm_data.Vregion==row)&(hm_data.Jregion==column)].iloc[0,2]     

#np.tile（n,A）,沿着x轴（列）n遍重复A
j = np.tile(np.array(range(len(V))),len(J))

#创建0000...111...222...333...444这样的数组
i = np.zeros((0,),dtype = int)
for x in range(len(J)):
    for y in range(len(V)):
        i = np.append(i, x)  

#将合并的clonefraction按照热图画图顺序变成列
data = np.zeros((0,),dtype = int)
for x in np.nditer(zero_df, order='F'):
    data = np.append(data, x)

    
#热图输入的格式为[0，0，x1,0,1,x2....0,n,xn,1,0,x,1,1,x,1,2,x.....]
'''
先变成三列的数组，然后.tolist()  索引都是从0开始
0 0 x
0 1 x
0 2 x
...
1 0 x
1 1 x
1 2 x
...
n 0 x

'''
heatmap_data = np.concatenate([i ,j, data]).reshape((len(i),3),order = 'F')
heatmap_data = heatmap_data.tolist()

#画热图
heatmap = (
    #设置图的大小
    HeatMap(init_opts=opts.InitOpts(width = "2000px",height = '3000px'))
     #x轴是J
    .add_xaxis(J)
    .add_yaxis(
        #系列名称，即一组数据（如一个x对应3个y，就有三个系列）
        '',
        #y轴数据是V
        V,
        #热图里面的数据
        heatmap_data,
        label_opts = opts.LabelOpts(is_show = False, position = 'inside')
    )
    #热图里面小块之间的连接线长度和宽度
    .set_series_opts(itemStyle={'borderColor': 'white', 'borderWidth':2}) 
    .set_global_opts(
                    #工具栏，比如放大，保存
                    toolbox_opts=opts.ToolboxOpts(),
                    #标题栏，名称，左右位置，上下位置，字体大小
                    title_opts = opts.TitleOpts(title = 'V-J Usage', pos_left = 1400,pos_top = 280,
                                               title_textstyle_opts=opts.TextStyleOpts(font_size=100)),
                    #x轴名称，左右上下位置，字体大小         
                    xaxis_opts = opts.AxisOpts(name = 'Jregion', name_location = 'middle', 
                                               name_textstyle_opts = opts.TextStyleOpts(font_size = 100),
                                               #x轴的每个数据字体大小和倾斜角度
                                              name_gap = 180, axislabel_opts = opts.LabelOpts(font_size = 38,rotate = 90),
                                              ),
                    yaxis_opts = opts.AxisOpts(name = 'Vregion', name_location = 'middle', 
                                               name_textstyle_opts = opts.TextStyleOpts(font_size = 100),
                                              name_gap = 500, axislabel_opts = opts.LabelOpts(font_size = 38),          
                                              ),
                    #视觉映射配置，取值范围（max），颜色过渡，上下左右位置，高度宽度
                    visualmap_opts = opts.VisualMapOpts(max_=1, range_color=["#F3C79E", '#EA5819','#F45942','#241A19'],
                                                        pos_right = '8%', pos_top = 'middle',item_height = 3500, item_width = 200
                                                       )
                    )
)
#设置画布大小和图在画布上的分布
grid = (
    Grid(init_opts = opts.InitOpts(width = "3400px",height = '4400px'))
    .add(heatmap,grid_opts = opts.GridOpts(is_show = False,pos_bottom = '10%', pos_top = '10%', pos_left = '20%', pos_right = '20%'))
)
#jupyter里用pyecharts画图必须加上xx.load_javascript()和xx.render_notebook()，并且放在不同的框框里
grid.load_javascript()

grid.render_notebook()

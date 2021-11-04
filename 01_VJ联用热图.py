#在jupyter lab中用pyecharts需要加上
from pyecharts.globals import CurrentConfig, NotebookType
CurrentConfig.NOTEBOOK_TYPE = NotebookType.JUPYTER_LAB

from pyecharts.charts import Grid
import random
import numpy as np
from pyecharts import options as opts
import pandas as pd
from collections import Counter
from pyecharts.charts import HeatMap


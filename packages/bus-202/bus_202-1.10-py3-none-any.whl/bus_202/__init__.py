import pandas as pd
from pathlib import Path
from .data_visualization.trim import trim
from .data_visualization.boxplot import boxplot
from .data_visualization.histogram import histogram
from .data_visualization.scatter import scatter
from .data import (
    midterm, financials, exec_comp, a1_df, a3_df, gapfinder, 
    sweet_things, sweet_things_simple, new_ceo, restate,
    group_1_1, group_1_2, group_1_3, group_1_4, group_1_5, group_1_6,
    group_2_1, group_2_2, group_2_3, group_2_4, group_2_5, group_2_6,
    group_3_1, group_3_2, group_3_3, group_3_4, group_3_5, group_3_6)
from .stats.ci import ci
from .stats.reg import reg

# Add this line to expose the functions at package level
__all__ = [
    'trim', 'boxplot', 'histogram', 'ci', 
    'midterm', 'financials', 'exec_comp', 
    'a1_df', 'a3_df', 'gapfinder', 'sweet_things',
    'sweet_things_simple', 'reg', 'scatter',
    'group_1_1', 'group_1_2', 'group_1_3', 'group_1_4', 'group_1_5', 'group_1_6',
    'group_2_1', 'group_2_2', 'group_2_3', 'group_2_4', 'group_2_5', 'group_2_6',
    'group_3_1', 'group_3_2', 'group_3_3', 'group_3_4', 'group_3_5', 'group_3_6']

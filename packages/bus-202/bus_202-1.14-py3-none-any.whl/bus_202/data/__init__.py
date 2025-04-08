import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).parent

class DataFrames:
    _midterm = None
    _financials = None
    _exec_comp = None
    _a1_df = None
    _a3_df = None
    _gapfinder = None
    _sweet_things = None
    _sweet_things_simple = None
    _new_ceo = None
    _restate = None
    _group_1_1 = None
    _group_1_2 = None
    _group_1_3 = None
    _group_1_4 = None
    _group_1_5 = None
    _group_1_6 = None
    _group_2_1 = None
    _group_2_2 = None
    _group_2_3 = None
    _group_2_4 = None
    _group_2_5 = None
    _group_2_6 = None
    _group_3_1 = None
    _group_3_2 = None
    _group_3_3 = None
    _group_3_4 = None
    _group_3_5 = None
    _group_3_6 = None
    
    @property
    def gapfinder(self):
        if self._gapfinder is None:
            self._gapfinder = pd.read_excel(DATA_DIR / 'gapfinder.xlsx')
        return self._gapfinder
    
    @property
    def midterm(self):
        if self._midterm is None:
            self._midterm = pd.read_excel(DATA_DIR / 'midterm.xlsx')
        return self._midterm
    
    @property
    def financials(self):
        if self._financials is None:
            self._financials = pd.read_excel(DATA_DIR / 'financials.xlsx')
        return self._financials
    
    @property
    def exec_comp(self):
        if self._exec_comp is None:
            self._exec_comp = pd.read_excel(DATA_DIR / 'exec_comp.xlsx')
        return self._exec_comp
    
    @property
    def a1_df(self):
        if self._a1_df is None:
            self._a1_df = pd.read_excel(DATA_DIR / 'a1_df.xlsx')
        return self._a1_df
    
    @property
    def a3_df(self):
        if self._a3_df is None:
            self._a3_df = pd.read_excel(DATA_DIR / 'a3_df.xlsx')
        return self._a3_df
    
    @property
    def sweet_things(self):
        if self._sweet_things is None:
            self._sweet_things = pd.read_excel(DATA_DIR / 'sweet_things.xlsx')
        return self._sweet_things
    
    @property
    def sweet_things_simple(self):
        if self._sweet_things_simple is None:
            self._sweet_things_simple = pd.read_excel(DATA_DIR / 'sweet_things_simple.xlsx')
        return self._sweet_things_simple
    
    @property
    def new_ceo(self):
        if self._new_ceo is None:
            self._new_ceo = pd.read_excel(DATA_DIR / 'new_ceo.xlsx')
        return self._new_ceo
    
    @property
    def restate(self):
        if self._restate is None:
            self._restate = pd.read_excel(DATA_DIR / 'restate.xlsx')
        return self._restate
    
    @property
    def group_1_1(self):
        if self._group_1_1 is None:
            self._group_1_1 = pd.read_excel(DATA_DIR / 'group_1_1.xlsx')
        return self._group_1_1
    
    @property
    def group_1_2(self):
        if self._group_1_2 is None:
            self._group_1_2 = pd.read_excel(DATA_DIR / 'group_1_2.xlsx')
        return self._group_1_2
    
    @property
    def group_1_3(self):
        if self._group_1_3 is None:
            self._group_1_3 = pd.read_excel(DATA_DIR / 'group_1_3.xlsx')
        return self._group_1_3
    
    @property
    def group_1_4(self):
        if self._group_1_4 is None:
            self._group_1_4 = pd.read_excel(DATA_DIR / 'group_1_4.xlsx')
        return self._group_1_4
    
    @property
    def group_1_5(self):
        if self._group_1_5 is None:
            self._group_1_5 = pd.read_excel(DATA_DIR / 'group_1_5.xlsx')
        return self._group_1_5
    
    @property
    def group_1_6(self):
        if self._group_1_6 is None:
            self._group_1_6 = pd.read_excel(DATA_DIR / 'group_1_6.xlsx')
        return self._group_1_6
    
    @property
    def group_2_1(self):
        if self._group_2_1 is None:
            self._group_2_1 = pd.read_excel(DATA_DIR / 'group_2_1.xlsx')
        return self._group_2_1
    
    @property
    def group_2_2(self):
        if self._group_2_2 is None:
            self._group_2_2 = pd.read_excel(DATA_DIR / 'group_2_2.xlsx')
        return self._group_2_2
    
    @property
    def group_2_3(self):
        if self._group_2_3 is None:
            self._group_2_3 = pd.read_excel(DATA_DIR / 'group_2_3.xlsx')
        return self._group_2_3
    
    @property
    def group_2_4(self):
        if self._group_2_4 is None:
            self._group_2_4 = pd.read_excel(DATA_DIR / 'group_2_4.xlsx')
        return self._group_2_4
    
    @property
    def group_2_5(self):
        if self._group_2_5 is None:
            self._group_2_5 = pd.read_excel(DATA_DIR / 'group_2_5.xlsx')
        return self._group_2_5
    
    @property
    def group_2_6(self):
        if self._group_2_6 is None:
            self._group_2_6 = pd.read_excel(DATA_DIR / 'group_2_6.xlsx')
        return self._group_2_6
    
    @property
    def group_3_1(self):
        if self._group_3_1 is None:
            self._group_3_1 = pd.read_excel(DATA_DIR / 'group_3_1.xlsx')
        return self._group_3_1
    
    @property
    def group_3_2(self):
        if self._group_3_2 is None:
            self._group_3_2 = pd.read_excel(DATA_DIR / 'group_3_2.xlsx')
        return self._group_3_2
    
    @property
    def group_3_3(self):
        if self._group_3_3 is None:
            self._group_3_3 = pd.read_excel(DATA_DIR / 'group_3_3.xlsx')
        return self._group_3_3
    
    @property
    def group_3_4(self):
        if self._group_3_4 is None:
            self._group_3_4 = pd.read_excel(DATA_DIR / 'group_3_4.xlsx')
        return self._group_3_4
    
    @property
    def group_3_5(self):
        if self._group_3_5 is None:
            self._group_3_5 = pd.read_excel(DATA_DIR / 'group_3_5.xlsx')
        return self._group_3_5
    
    @property
    def group_3_6(self):
        if self._group_3_6 is None:
            self._group_3_6 = pd.read_excel(DATA_DIR / 'group_3_6.xlsx')
        return self._group_3_6

# Create a single instance
_data = DataFrames()

# Define module-level functions that return the data
def midterm():
    return _data.midterm

def financials():
    return _data.financials

def exec_comp():
    return _data.exec_comp

def a1_df():
    return _data.a1_df

def a3_df():
    return _data.a3_df

def gapfinder():
    return _data.gapfinder

def sweet_things():
    return _data.sweet_things

def sweet_things_simple():
    return _data.sweet_things_simple

def new_ceo():
    return _data.new_ceo

def restate():
    return _data.restate

def group_1_1():
    return _data.group_1_1

def group_1_2():
    return _data.group_1_2

def group_1_3():
    return _data.group_1_3

def group_1_4():
    return _data.group_1_4

def group_1_5():
    return _data.group_1_5

def group_1_6():
    return _data.group_1_6

def group_2_1():
    return _data.group_2_1

def group_2_2():
    return _data.group_2_2

def group_2_3():
    return _data.group_2_3

def group_2_4():
    return _data.group_2_4

def group_2_5():
    return _data.group_2_5

def group_2_6():
    return _data.group_2_6

def group_3_1():
    return _data.group_3_1

def group_3_2():
    return _data.group_3_2

def group_3_3():
    return _data.group_3_3

def group_3_4():
    return _data.group_3_4

def group_3_5():
    return _data.group_3_5

def group_3_6():
    return _data.group_3_6

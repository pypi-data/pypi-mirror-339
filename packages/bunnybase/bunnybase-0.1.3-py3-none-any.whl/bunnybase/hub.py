from . import data
from .utils import hub_to_dataframe, dataframe_to_data, series_to_data, image_to_data
import numpy as np
import pandas as pd
class DataList:
    def __init__(self, datalist: list[data.Data]):
        self._datalist = datalist
        self._len = len(datalist)
    def filter(self, *args, **kwargs):
        elements = []
        
        for e in self._datalist:
            if e.has_properties(**kwargs):
                elements.append(e)
            elif e.has_property_values(*args):
                elements.append(e)
        return DataList(elements)
    def __repr__(self):
        return repr(self._datalist)
    def __getitem__(self, item: tuple[str]|str):
        if isinstance(item, tuple):
            return self.filter(*item)
        elif isinstance(item, str):
            return self.filter(*item)
        else:
            return self._datalist[item]
    def __len__(self) -> int:
        return self._len
    def __iter__(self):
        self.n = 0
        return self
    def __next__(self):
        self.n += 1
        if self.n == self._len:
            raise StopIteration()
        return self._datalist[self.n]
    
    
    
    
class Hub:
    def __init__(self):
        self.data : dict[str, list[data.Data]] = {}
    def __lshift__(self, data: data.Data|   DataList|list|tuple|set):
        if isinstance(data, pd.Series):
            data = series_to_data(data, 'None')
        if isinstance(data, pd.DataFrame):
            data = dataframe_to_data(data)
        elif isinstance(data, (DataList, list, tuple, set)):
            for i in data:
                category = i.category.lower()
                if self.data.get(category) is None:
                    self.data[category] = []
                self.data[category].append(i)
        else:
            category = data.category.lower()
            if self.data.get(category) is None:
                self.data[category] = []
            self.data[category].append(data)
            
        
    def __getitem__(self, item: tuple[str]|str) -> DataList:
        if isinstance(item, tuple):
            return DataList([d for k, v in self.data.items() if k in item for d in v])
        elif isinstance(item, str):
            return DataList([d for d in self.data[item]])
        
    def filter(self, *args, **kwargs) -> DataList:
        _elements = []
        elements = []
        if len(args) != 0:
            _elements = self.data[args[0]]
        else:
            for i in list(self.data.keys()):
                _elements.extend(self.data[i])
        for e in _elements:
            if e.has_properties(**kwargs):
                elements.append(e)
        return DataList(elements)
    def to_dataframe(self):
        return hub_to_dataframe(self)
    def optimise(self):
        for k, v in self.data.items():
            s = set()
            for i in v:
                s.add(i)
            self.data[k] = list(s)
        
    def __repr__(self):
        return "<object Hub>"



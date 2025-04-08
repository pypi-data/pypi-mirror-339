from .data import Data
import numpy as np
import pandas as pd
from .utils import dataframe_to_data, series_to_data
from .datalist import DataList
    
    
    
class Hub:
    def __init__(self):
        self.data : dict[str, list[Data]] = {}
    def __lshift__(self, data: Data|   DataList|list|tuple|set):
        if isinstance(data, (int, float)):
            data = Data('number', num=data)
        elif isinstance(data, str):
            data = Data('string', str=data, len=len(data))
        elif isinstance(data, pd.Series):
            data = series_to_data(data, 'None')
        elif isinstance(data, pd.DataFrame):
            data = dataframe_to_data(data)
        if isinstance(data, (DataList, list, tuple, set)):
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
    def to_dataframe(self) -> pd.DataFrame:
        data = self.data
        categories = list(data.keys())
        h = dict[str, dict[tuple[str|int], list]]()
        for category in categories:
            for idx, ds in enumerate(data[category]):
                for k, v in ds.properties.items():
                    if h.get(k) == None:
                        h[k] = {(category, idx): v}
                    else:
                        h[k].update({(category, idx): v})
        
        df = pd.DataFrame(h)
        return df
    def optimise(self):
        for k, v in self.data.items():
            s = set()
            for i in v:
                s.add(i)
            self.data[k] = list(s)
        
    def __repr__(self):
        return "<object Hub>"



from .data import Data

class DataList:
    def __init__(self, datalist: list[Data]):
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
    def groupby(self, *, property:str=None, value:str=None):
        group = []
        if not property is None:
            for i in self._datalist:
                group.append(i.has_properties({
                    property: "*"
                }))
        elif not value is None:
            for i in self._datalist:
                group.append(i.has_property_values(value))
        return DataList(group)
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
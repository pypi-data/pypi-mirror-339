from . import data

class Hub:
    def __init__(self):
        self.data : dict[str, list[data.Data]] = {}
    def __lshift__(self, data: data.Data):
        category = data.category.lower()
        if self.data.get(category) is None:
            self.data[category] = []
        self.data[category].append(data)
    def filter(self, *args, **kwargs) -> list[data.Data]:
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
        return elements
        
        
    def __repr__(self):
        return "<object Hub>"







class Data:
    def __init__(self, category: str, **kwargs):
        """Generates an data object

        Args:
            category (str): the name of the data classification for example: person
            `**kwargs` (Any): add some properties to the data object
        """
        self.category = category
        self.properties = kwargs
    def __repr__(self):
        str_properties = ""
        for k, v in self.properties.items():
            str_properties+=f"{k}={repr(v)},"
        return f"Data('{self.category}', {str_properties})"
    def has_properties(self, **kwargs):
        for k, v in kwargs.items():
            _ = self.properties.get(k)
            if _ is None:
                return False
            if v != '*':
                if _ != v:
                    return False
            
        return True
            
    
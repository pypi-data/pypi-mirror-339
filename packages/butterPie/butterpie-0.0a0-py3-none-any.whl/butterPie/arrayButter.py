class ButterArray(list):
    def __init__(self, *args):
        super().__init__(*args)

    def spread_jam(self, x: int):
        for i in range(0, len(self), 1):
            self[i] = self[i]*x

    def add_jam(self, x: int):
        for i in range(0, len(self), 1):
            self[i] = self[i]+x

    def Separate_jam_and_butter(self):
        type_map = {}

        for i in self:
            if isinstance(i, (list, tuple, set, dict)):
                raise ValueError("It isn't 1D Array.")
            t = type(i)
            if not t in type_map:
                type_map[t] = []
            type_map[t].append(i)
        
        return list(type_map.values())
    
    def knead_dough(self):
        def _flatten(lis):
            result = []
            for item in lis:
                if isinstance(item, list):
                    result.extend(_flatten(item))
                else:
                    result.append(item)
            return result
        return _flatten(self)

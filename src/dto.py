class CrudDTO:
    @property
    def fields(self):
        return ', '.join(self.dict(exclude_none=True).keys())
    
    @property
    def values_enum(self):
        fields_count = len(list(self.dict(exclude_none=True).keys()))
        return ', '.join('$' + str(i) for i in range(1, fields_count + 1))
    
    @property
    def values_list(self):
        return list(self.dict(exclude_none=True).values())

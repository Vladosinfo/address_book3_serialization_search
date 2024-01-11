from classes.field import Field
class Name(Field):
    def __init__(self, value):
        self._value = None
        self.value = value
        super().__init__(self._value)

    @property
    def value(self):
        return self.value
    
    @Field.value.setter
    def value(self, value):
        self._value = value.title()
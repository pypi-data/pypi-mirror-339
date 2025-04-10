from .update import *
from .update import upload
from .operators.matical import space,select
from .type import _AllSimpleTypes as SimpleType

__all__=["select", "space", "dint", "istr"
        "ALL", "NEW", "WILL", 
        "get_update", "get_version_update_time", "get_news_update_time", "get_new", "get_all", "get_will", 
        "get_pre_update", "get_pre_version_update_time", "get_pre_news_update_time", "get_pre_news_update_time", "get_pre_new", "get_pre_all"]

class dint(int):
    def __new__(cls, value:int):
        instance = super().__new__(cls,value)
        instance.use_dec = value
        return instance

    def __iter__(self):
        return iter([dint(i) for i in str(self)])

    def __getattr__(self, index):
        return dint(str(self)[index])
    
    def __len__(self):
        return len(str(self))

    def __lshift__(self, value):
        if self.use_dec:
            return dint(self * (10 ** value))
        else:
            return super().__lshift__(value)
    
    def __rshift__(self, value:int):
        if self.use_dec:
            o = str(self)[:-value]
            return select(dint(0), dint(o), o != "")
        else:
            return super().__rshift__(value )
    
    def __or__(self, value):
        if self.use_dec:
            o = ""
            str_v = [str(self), str(value)]

            if len(str_v[0]) > len(str_v[1]):
                o += str_v[0][:len(str_v[0]) - len(str_v[1])]
                str_v[0] = str_v[0][len(str_v[0]) - len(str_v[1]):]
            elif len(str_v[1]) > len(str_v[0]):
                o += str_v[1][:len(str_v[1]) - len(str_v[0])]
                str_v[1] = str_v[1][len(str_v[1]) - len(str_v[0]):]
            
            for index in range(len(str_v[0])):
                o += select(str_v[0][index],str_v[1][index], str_v[0][index] != str_v[1][index])
            return dint(o)
        else:
            return super().__or__(value)

    def __and__(self, value):
        if self.use_dec:
            o = ""
            str_v = [str(self), str(value)]

            if len(str_v[0]) > len(str_v[1]):
                o += str_v[0][:len(str_v[0]) - len(str_v[1])]
                str_v[0] = str_v[0][len(str_v[0]) - len(str_v[1]):]
            elif len(str_v[1]) > len(str_v[0]):
                o += str_v[1][:len(str_v[1]) - len(str_v[0])]
                str_v[1] = str_v[1][len(str_v[1]) - len(str_v[0]):]
            
            for index in range(len(str_v[0])):
                o += select(str_v[0][index], str_v[1][index], space(str_v[0][index],str_v[1][index]) <= 0)
            return dint(o)
        else:
            return super().__and__(value)
    
    def __invert__(self):
        if self.use_dec:
            o = ""
            for index in self:
                o += str(select(index + 5, index - 5, index >=5))
            return dint(o)
        else:
            return super().__invert__()
    
    def __xor__(self, value):
        if self.use_doc:
            o = ""
            str_v = [str(self), str(value)]

            if len(str_v[0]) > len(str_v[1]):
                o += str_v[0][:len(str_v[0]) - len(str_v[1])]
                str_v[0] = str_v[0][len(str_v[0]) - len(str_v[1]):]
            elif len(str_v[1]) > len(str_v[0]):
                o += str_v[1][:len(str_v[1]) - len(str_v[0])]
                str_v[1] = str_v[1][len(str_v[1]) - len(str_v[0]):]
            
            for index in range(len(str_v[0])):
                o += select(str_v[1][index], str_v[0][index], space(str_v[0][index],str_v[1][index]) <= 0)

            return dint(o)
        else:
            return super().__xor__(value)

class istr(str):
    def __new__(cls, string:str):
        instance = super().__new__(cls,string)
        instance.str = string
        return instance
    
    @property
    def all_char_unicode(self) -> list[int]:
        '''Get some string unicode.'''
        return [ord(char) for char in self.str]

    def __add__(self, value):
        if isinstance(value, int):
            self.str += chr(value)
        elif isinstance(value,str):
            self.str += value
        else:
            raise TypeError(f'unsupported operand type(s) for +: istr and {type(value)}')
        return istr(self.str)

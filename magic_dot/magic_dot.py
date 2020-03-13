"""Main module."""
"""powerdot: The lazy coders answer to lack of PEP 505"""

class MagicDot():
    def __init__(self, __data, write=False, spanList=False):
        self.__data = data
    
    def __getattr__(self, name):
        if hasattr(self.__data, name):
           self.__data = getattr(self.data,name)
           return self

        try:
            self.__data = self.data[name]
            return self

        except KeyError:
            pass
    
        # if spanList:
        #     try:
        #         iterator = iter(theElement)
        #     except TypeError:
        #         pass
        #     else:
 
        self.__data = None
        return self

    def __getitem__(self, key):
        try:
            self.__data = self.data[key]
            return self
        except KeyError:
            pass

        if hasattr(self.__data, key):
           self.__data = getattr(self.data, key)
           return self
    
        # if spanList:
        #     try:
        #         iterator = iter(theElement)
        #     except TypeError:
        #         pass
        #     else:
 
        self.__data = None
        return self

    def extract(self):
        return self.__data

    def __invert__(self):
        """Convenience operator extract __data.
        This:
          x = ~MagicDot(__data).a.b.c
        Is equivalent to this:
          x = MagicDot(__data).a.b.c.extract()
        """
        pass  

class Foo(object):
    _instance = None
    def __init__(self,name):
        self.name = name

    @classmethod
    def instance(cls,*args,**kwargs):
        if hasattr(cls,'_instance'):
            obj = cls(*args,**kwargs)
            setattr(cls,'_instance',obj)

        return getattr(cls,'_instance',None)


obj1 = Foo.instance(11)
obj2 = Foo.instance(22)

print(obj1,obj2)
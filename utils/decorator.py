class cached_property(property):
    def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        property.__init__(self, fget, fset, fdel, doc)

        self.func = fget
        self.func_name = fget.__name__

    def __get__(self, instance, type=None):
        if instance is None:
            return self

        value = instance._cached.get(self.func_name, None)
        if value is None:
            value = self.func(instance)
            instance._cached[self.func_name] = value
        return value

    def __set__(self, instance, value):
        instance._cached[self.func_name] = value
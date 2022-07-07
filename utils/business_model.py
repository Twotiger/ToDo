class Model(object):
    __slots__ = ("_db", "_cached")

    def __init__(self, db_model=None):
        self._cached = {}
        if db_model:
            self._init_(db_model)

    def _init_from_dic(self, dic):
        self._db = dic
        for slot in self.__slots__:
            setattr(self, slot, dic.get(slot))

    def _init_(self, model, slots=None):
        self._db = model
        if not slots:
            slots = self.__slots__

        for slot in slots:
            value = getattr(model, slot, None)
            if value is not None:
                setattr(self, slot, value)

class Service(object):
    def __init__(self, attr=None):
        self.parent = attr

    @classmethod
    def get(cls, attr):
        return cls(attr)
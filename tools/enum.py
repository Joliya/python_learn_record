"""
@file: enum.py
@time: 2023/11/7 14:10
@desc:
"""


class _EnumMeta(type):
    def __init__(cls, name, bases, attr_dict):
        super(_EnumMeta, cls).__init__(name, bases, attr_dict)

        enum_items = []
        value_set = set()
        verbose_set = set()
        for _name, _instance in list(attr_dict.items()):
            if isinstance(_instance, EnumItem):
                assert _instance.value not in value_set, "value必须唯一"
                assert _instance.verbose not in verbose_set, "verbose必须唯一"
                value_set.add(_instance.value)
                verbose_set.add(_instance.verbose)
                _instance.name = _name
                enum_items.append(_instance)

        enum_items.sort(key=lambda x: x.count)

        choices = []
        values_to_items = {}
        for _instance in enum_items:
            choices.append((_instance.value, _instance.verbose))
            values_to_items[_instance.value] = _instance

        if choices:
            cls.choices = choices
            cls.values_to_items = values_to_items

    def __iter__(cls):
        return iter(cls.choices)

    def __contains__(cls, v):
        return v in cls.values_to_items


class EnumItem(object):
    __count = 0
    __slots__ = ("name", "value", "verbose", "count")

    def __init__(self, value, verbose):
        self.value = value
        self.verbose = verbose
        self.name = ""
        self.count = EnumItem.__count
        EnumItem.__count += 1

    def __get__(self, instance, owner):
        return self.value

    def __str__(self):
        return "%s: %s" % (self.name, self.value)

    def __repr__(self):
        return "<%s>" % self.__str__()


class EnumBase(object, metaclass=_EnumMeta):
    """
    An Enum base class for more readable enumerations
    Example:
    >>> class TestEnum(EnumBase):
    ...     A = EnumItem('a', 'first')
    ...     B = EnumItem('b', 'second')
    ...
    ...
    >>> TestEnum.A
    'a'
    >>> TestEnum.values()
    ['a', 'b']
    >>> list(TestEnum)
    [('a', 'first'), ('b', 'second')]
    >>> TestEnum.verbose(TestEnum.A)
    'first'
    >>> TestEnum.verbose_safe('c', default='未知')
    '未知'
    """

    @classmethod
    def get_key_by_value(cls, v):
        item = cls.values_to_items[v]
        return item.name

    @classmethod
    def verbose(cls, v):
        item = cls.values_to_items[v]
        return item.verbose

    @classmethod
    def verbose_safe(cls, v, default=None):
        try:
            return cls.verbose(v)
        except KeyError:
            return default

    @classmethod
    def values(cls):
        return [_info[0] for _info in cls.choices]

    @classmethod
    def get_value_by_verbose(cls, v):
        for value, verbose in cls.choices:
            if verbose == v:
                return value
        raise KeyError('没有找到对应的verbose')

    def __iter__(self):
        return iter(self.choices)

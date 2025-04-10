from ._error import IntError
from typing import final
from .Subclass import notSubclass

@notSubclass
@final
class Int_:
    def __init__(self, integer: int) -> None:
        """
        Create immutable int type
        :param integer: an integer
        """

        self.__check_type(integer)

        self.__integer = integer

    def __str__(self):
        return str(self.__integer)

    def __int__(self):
        return self.__integer

    def __bool__(self):
        return True if self.__integer == 1 else False

    def __repr__(self):
        return f"Int({self.__integer!r})"

    def __eq__(self, other):
        return self.__integer == other

    def __and__(self, other):
        return self.__integer & other

    def __iand__(self, other):
        self.__integer &= other
        return self

    def __or__(self, other):
        return self.__integer | other

    def __ior__(self, other):
        self.__integer |= other
        return self

    def __add__(self, other):
        self.__check_type(other)
        self.__integer += other
        return self

    def __iadd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        self.__check_type(other)
        self.__integer -= other
        return self

    def __isub__(self, other):
        return self.__sub__(other)

    def __mul__(self, other):
        self.__integer *= other
        return self

    def __imul__(self, other):
        return self.__mul__(other)
    def __truediv__(self, other):
        self.__integer = self.__integer // other
        return self

    def __itruediv__(self, other):
        return self.__truediv__(other)

    def __mod__(self, other):
        self.__integer %= other
        return self

    def __imod__(self, other):
        return self.__mod__(other)

    def __pow__(self, power, modulo=None):
        self.__check_type(power)
        self.__integer **= power
        return self

    def __ipow__(self, other):
        return self.__pow__(other)

    def __check_type(self, value):
        if not isinstance(value, (int, Int_)):
            raise IntError(value)

    @property
    def int_(self) -> int:
        """
        Return actual value
        :return: int
        """
        return self.__integer

    @int_.setter
    def int_(self, new_value):
        """
        Set a new value
        :param new_value: an integer
        :return: None
        """
        self.__check_type(new_value)
        self.__integer = new_value

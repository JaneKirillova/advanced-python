import numbers

import numpy as np


class MixinWriteToFile:
    def write_to_file(self, file_name):
        with open(file_name, "w") as file:
            file.write(self.__str__())


class MixinRepresentation:
    def __str__(self):
        result = "["
        for row in self.data:
            result += str(row) + '\n'
        return result[:-1] + "]"


class MixinGetSet:
    def __init__(self, data):
        self.check(data)
        self.data = np.asarray(data)

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._data = data

    @staticmethod
    def check(data):
        if not all(len(row) == len(data[0]) for row in data):
            raise ValueError('Incorrect matrix shape')


class MixinMatrix(np.lib.mixins.NDArrayOperatorsMixin, MixinRepresentation, MixinWriteToFile, MixinGetSet):

    _HANDLED_TYPES = (np.ndarray, numbers.Number)

    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        out = kwargs.get('out', ())
        for x in inputs + out:
            # Only support operations with instances of _HANDLED_TYPES.
            # Use ArrayLike instead of type(self) for isinstance to
            # allow subclasses that don't override __array_ufunc__ to
            # handle ArrayLike objects.
            if not isinstance(x, self._HANDLED_TYPES + (MixinMatrix,)):
                return NotImplemented

        # Defer to the implementation of the ufunc on unwrapped values.
        inputs = tuple(x.data if isinstance(x, MixinMatrix) else x
                       for x in inputs)
        if out:
            kwargs['out'] = tuple(
                x.data if isinstance(x, MixinMatrix) else x
                for x in out)
        result = getattr(ufunc, method)(*inputs, **kwargs)

        if type(result) is tuple:
            # multiple return values
            return tuple(type(self)(x) for x in result)
        elif method == 'at':
            # no return value
            return None
        else:
            # one return value
            return type(self)(result)
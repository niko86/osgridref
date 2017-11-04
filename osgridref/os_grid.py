import math

class OSGridRef(object):

    """

    >>> OSGridRef.grid_100km(403123, 439567)
    'SE'
    >>> OSGridRef.grid_10km(403123, 439567)
    'SE 03'
    >>> OSGridRef.grid_5km(403123, 439567)
    'SE 03 NW'
    >>> OSGridRef.grid_1km(403123, 439567)
    'SE 03 39'
    >>> OSGridRef.grid_500m(403123, 439567)
    'SE 03 39 NW'
    >>> OSGridRef.grid_100m(403123, 439567)
    'SE 031 395'
    >>> OSGridRef.grid_10m(403123, 439567)
    'SE 0312 3956'
    >>> OSGridRef.grid_1m(403123, 439567)
    'SE 03123 39567'

    >>> OSGridRef.grid_100km(450676, 529983)
    'NZ'
    >>> OSGridRef.grid_10km(450676, 529983)
    'NZ 52'
    >>> OSGridRef.grid_5km(450676, 529983)
    'NZ 52 NW'
    >>> OSGridRef.grid_1km(450676, 529983)
    'NZ 50 29'
    >>> OSGridRef.grid_500m(450676, 529983)
    'NZ 50 29 NE'
    >>> OSGridRef.grid_100m(450676, 529983)
    'NZ 506 299'
    >>> OSGridRef.grid_10m(450676, 529983)
    'NZ 5067 2998'
    >>> OSGridRef.grid_1m(450676, 529983)
    'NZ 50676 29983'

    """

    def __init__(self, easting: int, northing: int):
        self.easting = easting
        self.northing = northing

    def _primary_pair(self):
        grid_chars = 'ABCDEFGHJKLMNOPQRSTUVWXYZ'
        e = math.floor(self.easting / 100000)
        n = math.floor(self.northing / 100000)
        e_letter = int((19 - n) - (19 - n) % 5 + math.floor((e + 10) / 5))
        n_letter = int((19 - n) * 5 % 25 + e % 5)
        return grid_chars[e_letter] + grid_chars[n_letter]

    def _grid_string(self, pair: int = 1):  # default is 1 pair
        str_e = str(self.easting)
        str_n = str(self.northing)
        return str_e[1:pair + 1], str_n[1:pair + 1]  # skips the unneeded first number

    def _secondary_pair(self, sec_pair: int = 2):  # sec_pair values either 2 or 4
        if sec_pair == 2:
            str_e, str_n = self._grid_string(pair=2)  # gets a number string 2 pairs in length
        else:
            str_e, str_n = self._grid_string(pair=3)

        e, n = str_e[-1:], str_n[-1:]

        if int(n) >= 5:
            n = 'N'
        else:
            n = 'S'
        if int(e) >= 5:
            e = 'E'
        else:
            e = 'W'

        return n + e

    @staticmethod
    def _string_maker(cls, easting: int, northing: int, pair: int = 1, sec_pair: int = None):
        instance = cls(easting, northing)
        primary_pair = instance._primary_pair()
        str_e, str_n = instance._grid_string(pair=pair)
        if sec_pair:
            secondary_pair = instance._secondary_pair(sec_pair=sec_pair)
            return (primary_pair, str_e, str_n, secondary_pair)
        else:
            return (primary_pair, str_e, str_n)

    @classmethod
    def grid_100km(cls, easting: int, northing: int):
        instance = cls(easting, northing)
        return instance._primary_pair()

    @classmethod
    def grid_10km(cls, easting: int, northing: int):
        pri, e, n = cls._string_maker(cls, easting, northing, pair=1)
        return f'{pri} {e}{n}'

    @classmethod
    def grid_5km(cls, easting: int, northing: int):
        pri, e, n, sec = cls._string_maker(cls, easting, northing, pair=1, sec_pair=2)
        return f'{pri} {e}{n} {sec}'

    @classmethod
    def grid_1km(cls, easting: int, northing: int):
        pri, e, n = cls._string_maker(cls, easting, northing, pair=2)
        return f'{pri} {e} {n}'

    @classmethod
    def grid_500m(cls, easting: int, northing: int):
        pri, e, n, sec = cls._string_maker(cls, easting, northing, pair=2, sec_pair=4)
        return f'{pri} {e} {n} {sec}'

    @classmethod
    def grid_100m(cls, easting: int, northing: int):
        pri, e, n = cls._string_maker(cls, easting, northing, pair=3)
        return f'{pri} {e} {n}'

    @classmethod
    def grid_10m(cls, easting: int, northing: int):
        pri, e, n = cls._string_maker(cls, easting, northing, pair=4)
        return f'{pri} {e} {n}'

    @classmethod
    def grid_1m(cls, easting: int, northing: int):
        pri, e, n = cls._string_maker(cls, easting, northing, pair=5)
        return f'{pri} {e} {n}'


if __name__ == "__main__":
    pass
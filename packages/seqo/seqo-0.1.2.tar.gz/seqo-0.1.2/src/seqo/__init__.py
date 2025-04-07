import string

__version__ = '0.1.2'

from functools import lru_cache

__all__ = ['SequentialString']


class SequentialString:
    _default_charset = string.printable

    def __init__(self, charset: str = ""):
        if charset:
            seen = set()
            uniques = []
            for char in charset:
                if charset in seen:
                    continue
                else:
                    seen.add(char)
                    uniques.append(char)

            self.charset = uniques
        else:
            self.charset = string.printable

    def get(self, n: int):
        max_index = len(self.charset)
        indexes = []

        while n >= max_index:
            current_index = n % max_index
            indexes.append(current_index)
            n = n // max_index - 1

        indexes.append(n)

        index_to_chars = [self.charset[i] for i in indexes]
        word = ''.join(index_to_chars[::-1])
        return word

    def index_of(self, s: str):
        rev = s[::-1]
        individual_weights = [self._char_index(c) + (1 if i != 0 else 0) for i, c in enumerate(rev)]
        positional_weights = [len(self.charset) ** w for w in range(len(rev))]
        total_weights = [p * i for p, i in zip(positional_weights, individual_weights)]
        return sum(total_weights)

    @lru_cache
    def _char_index(self, char: str):
        return self.charset.index(char)

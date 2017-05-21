# -*- coding: utf-8 -*-
#どっかからとってきたサンプルコード

import doctest

def twice(n):
    """ 引数を 2 倍して返す関数
    >>> twice(8)
    16
    >>> twice(1850923)
    3701846
    """
    return n * 2

if __name__ == "__main__":
    doctest.testmod()

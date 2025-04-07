from collections.abc import Iterable, Iterator
from functools import partial, reduce

import dill
from joblib import Parallel, delayed
from more_itertools import flatten, take
from toolz import groupby as groupfrom


def isiterable(element):
    return isinstance(element, Iterable)


def isiterator(element):
    return isinstance(element, Iterator)


def identity(x):
    return x


def argmap(f, *args, **kwargs):
    return map(partial(f, *args[:-1], **kwargs), args[-1])


def give(func, *args, **kwargs):
    yield from func(*args, **kwargs)


def collect(n, func, *args, **kwargs):
    return list(take(n, give(func, *args, **kwargs)))


def pipe(x, *funcs):
    return reduce(lambda x, func: func(x), funcs, x)


def pmap(*args, jobs=1, m=map, generator=False, **kwargs):
    *funcs, iterator = args
    return Parallel(
        jobs,
        return_as='generator' if generator else 'list',
        **kwargs
    )(
        m(
            delayed(
                lambda x: reduce(
                    lambda y, func: func(y),
                    funcs,
                    x
                )
            ),
            iterator
        )
    )


def imap(*args):
    f, *g, d = args
    f = f if f else identity
    g = g[0] if any(g) else identity
    d = d.items() if isinstance(d, dict) else d
    yield from ((f(k), g(v)) for k, v in d)


def dmap(*args):
    return dict(imap(*args))


def istarmap(f, d):
    yield from (f(k, *v) for k, v in d.items())


def dstarmap(f, d):
    return dict(istarmap(f, d))


def ifilter(*args):
    f, *g, d = args
    f = f if f else lambda x: True
    g = g[0] if any(g) else lambda x: True
    d = d.items() if isinstance(d, dict) else d
    yield from ((k, v) for k, v in d if f(k) and g(v))


def dfilter(*args):
    return dict(ifilter(*args))


def ireversed(d):
    yield from ((v, k) for k, v in (d.items() if isinstance(d, dict) else d))


def dreversed(d):
    return dict(ireversed(d))


def iagg(*D):
    f, D = (D[0], D[1:]) if callable(D[0]) else (tuple, D)
    D = list(map(dict, D))
    yield from (
        (k, f(d[k] for d in D if k in d))
        for k in set(flatten(D))
    )


def dagg(*D):
    return iagg(*D)


def keys(d):
    return list(d.keys())


def values(d):
    return list(d.values())


def items(d):
    return list(d.items())


def save(obj, dst):
    with open(dst, 'wb') as f:
        dill.dump(obj, f)
    return obj


def load(src):
    with open(src, 'rb') as f:
        return dill.load(f)

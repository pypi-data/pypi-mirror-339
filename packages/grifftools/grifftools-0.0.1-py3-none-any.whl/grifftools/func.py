import os
import sys
from functools import reduce

import dill
from joblib import Parallel, delayed


def csv(dicts, dst, sep=','):
    if isinstance(dicts, dict):
        dicts = [dicts]
    if not os.path.exists(dst):
        with open(dst, 'w') as f:
            print(sep.join(map(str, dicts[0].keys())), sep=sep, file=f)
    with open(dst, 'a') as f:
        for dict_ in dicts:
            print(sep.join(map(str, dict_.values())), sep=sep, file=f)
    return cat(dst)


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
                    x,
                )
            ),
            iterator
        )
    )


def save(obj, dst):
    with open(dst, 'wb') as f:
        dill.dump(obj, f)
    return obj


def load(src):
    with open(src, 'rb') as f:
        return dill.load(f)

import operator
import re
from inspect import isfunction
from typing import Any


def assert_comparison(case, expected, actual, tolerance):
    case.assertIsNotNone(actual)
    if isinstance(actual, float) and isinstance(expected, float):
        case.assertAlmostEqual(actual, expected, delta=tolerance)
    elif isinstance(actual, int) and isinstance(expected, int):
        case.assertEqual(expected, actual
                         )
def find(obj:Any, path:str):
    attrs = path.split('.')
    for attr in attrs:
        m = re.match(r'(\w+)\[(\d+)]', attr)
        if m is not None:
            obj = operator.getitem(getattr(obj, m.group(1)),int(m.group(2)))
        else:
            if callable(obj):
                obj = obj()
            if isinstance(obj, dict):
                obj = obj[attr]
            else:
                obj = getattr(obj, attr)

    return obj
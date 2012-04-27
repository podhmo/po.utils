## todo rename
import types
import unittest

def maybe_access(target, k, default=None):
    if k.startswith(":"):
        return getattr(target, k[1:], default)
    elif hasattr(target, "get"):
        return target.get(k, default)
    else:
        try:
            return target[k]
        except (IndexError, KeyError):
            return default

class MaybeChain(object):
    def __init__(self, value, default=None):
        self.value = value
        self.default = default

    def __getattr__(self, k, default=None):
        default = default or self.default
        if self.value == default:
            return self
        else:
            value = getattr(self.value, k, default)
            return self.__class__(value, default=default)

## dummy object
## 

def as_eigen_method(obj, fn, name=None):
    if name is None:
        name = fn.__name__
    method = types.MethodType(fn, obj, obj.__class__)
    setattr(obj, name, method)
    
class DummyObject(object):
    def __init__(self, **kwargs):
        for k, v in kwargs.iteritems():
            setattr(self, k, v)

a = DummyObject(b="c")


print MaybeChain(a).none.value
print MaybeChain(a).none.none.value
print MaybeChain(a).b.value

def foo(self, x):
    return self.b + x
as_eigen_method(a, foo)
print a.foo("foo")

class MaybeUtilsTests(unittest.TestCase):
    def test_maybe_access_empty(self):
        params = {}
        self.assertIsNone(maybe_access(params, "k"))
        self.assertEquals(maybe_access(params, "k", ":default"), ":default")

    def test_maybe_access_by_getitems(self):
        params = {"k" : "v"}
        self.assertEquals(maybe_access(params, "k"), "v")
        self.assertIsNone(maybe_access(params, ":k"))

    def test_maybe_access_by_getattr(self):
        class params(object):
            k = "v"
        self.assertEquals(maybe_access(params, ":k"), "v")
        self.assertRaises(TypeError, lambda : maybe_access(params, "k"))

# class MaybeChainUnitTests(unittest.TestCase):
#     def test_it(self):

if __name__ == "__main__":
    unittest.main()

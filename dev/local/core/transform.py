#AUTOGENERATED! DO NOT EDIT! File to edit: dev/01c_transform.ipynb (unless otherwise specified).

__all__ = ['ArrayBase', 'ArrayImageBase', 'ArrayImage', 'ArrayImageBW', 'ArrayMask', 'Transform', 'InplaceTransform',
           'TupleTransform', 'ItemTransform', 'get_func', 'Func', 'Sig', 'compose_tfms', 'mk_transform', 'gather_attrs',
           'gather_attr_names', 'Pipeline']

#Cell
from .imports import *
from .foundation import *
from .utils import *
from .dispatch import *
from ..test import *
from ..notebook.showdoc import show_doc

#Cell
class ArrayBase(ndarray):
    def __new__(cls, x, *args, **kwargs):
        if isinstance(x,tuple): super().__new__(cls, x, *args, **kwargs)
        if args or kwargs: raise RuntimeError('Unknown array init args')
        if not isinstance(x,ndarray): x = array(x)
        return x.view(cls)

#Cell
class ArrayImageBase(ArrayBase):
    _show_args = {'cmap':'viridis'}
    def show(self, ctx=None, **kwargs):
        return show_image(self, ctx=ctx, **{**self._show_args, **kwargs})

#Cell
class ArrayImage(ArrayImageBase): pass

#Cell
class ArrayImageBW(ArrayImage): _show_args = {'cmap':'Greys'}

#Cell
class ArrayMask(ArrayImageBase): _show_args = {'alpha':0.5, 'cmap':'tab20'}

#Cell
_tfm_methods = 'encodes','decodes','setups'

class _TfmDict(dict):
    def __setitem__(self,k,v):
        if k not in _tfm_methods or not callable(v): return super().__setitem__(k,v)
        if k not in self: super().__setitem__(k,TypeDispatch())
        self[k].add(v)

#Cell
class _TfmMeta(type):
    def __new__(cls, name, bases, dict):
        res = super().__new__(cls, name, bases, dict)
        res.__signature__ = inspect.signature(res.__init__)
        return res

    def __call__(cls, *args, **kwargs):
        f = args[0] if args else None
        n = getattr(f,'__name__',None)
        for nm in _tfm_methods:
            if not hasattr(cls,nm): setattr(cls, nm, TypeDispatch())
        if callable(f) and n in _tfm_methods:
            getattr(cls,n).add(f)
            return f
        return super().__call__(*args, **kwargs)

    @classmethod
    def __prepare__(cls, name, bases): return _TfmDict()

#Cell
class Transform(metaclass=_TfmMeta):
    "Delegates (`__call__`,`decode`,`setup`) to (`encodes`,`decodes`,`setups`) if `split_idx` matches"
    split_idx,init_enc,as_item_force,as_item,order = None,False,None,True,0
    def __init__(self, enc=None, dec=None, split_idx=None, as_item=False):
        self.split_idx,self.as_item = ifnone(split_idx, self.split_idx),as_item
        self.init_enc = enc or dec
        if not self.init_enc: return

        # Passing enc/dec, so need to remove (base) class level enc/dec
        del(self.__class__.encodes,self.__class__.decodes,self.__class__.setups)
        self.encodes,self.decodes,self.setups = TypeDispatch(),TypeDispatch(),TypeDispatch()
        if enc:
            self.encodes.add(enc)
            self.order = getattr(self.encodes,'order',self.order)
        if dec: self.decodes.add(dec)

    @property
    def use_as_item(self): return ifnone(self.as_item_force, self.as_item)
    def __call__(self, x, **kwargs): return self._call('encodes', x, **kwargs)
    def decode  (self, x, **kwargs): return self._call('decodes', x, **kwargs)
    def setup(self, items=None): return self.setups(items)
    def __repr__(self): return f'{self.__class__.__name__}: {self.use_as_item} {self.encodes} {self.decodes}'

    def _call(self, fn, x, split_idx=None, **kwargs):
        if split_idx!=self.split_idx and self.split_idx is not None: return x
        f = getattr(self, fn)
        if self.use_as_item or not is_listy(x): return self._do_call(f, x, **kwargs)
        g = (self._do_call(f, x_, **kwargs) for x_ in x)
        res = type(x)(g)
        return retain_type(res, x)

    def _do_call(self, f, x, **kwargs):
        return x if f is None else retain_type(f(x, **kwargs), x, f.returns_none(x))

add_docs(Transform, decode="Delegate to `decodes` to undo transform", setup="Delegate to `setups` to set up transform")

#Cell
class InplaceTransform(Transform):
    "A `Transform` that modifies in-place and just returns whatever it's passed"
    def _call(self, fn, x, split_idx=None, **kwargs):
        super()._call(fn,x,split_idx,**kwargs)
        return x

#Cell
class TupleTransform(Transform):
    "`Transform` that always treats `as_item` as `False`"
    as_item_force=False

#Cell
class ItemTransform (Transform):
    "`Transform` that always treats `as_item` as `True`"
    as_item_force=True

#Cell
def get_func(t, name, *args, **kwargs):
    "Get the `t.name` (potentially partial-ized with `args` and `kwargs`) or `noop` if not defined"
    f = getattr(t, name, noop)
    return f if not (args or kwargs) else partial(f, *args, **kwargs)

#Cell
class Func():
    "Basic wrapper around a `name` with `args` and `kwargs` to call on a given type"
    def __init__(self, name, *args, **kwargs): self.name,self.args,self.kwargs = name,args,kwargs
    def __repr__(self): return f'sig: {self.name}({self.args}, {self.kwargs})'
    def _get(self, t): return get_func(t, self.name, *self.args, **self.kwargs)
    def __call__(self,t): return mapped(self._get, t)

#Cell
class _Sig():
    def __getattr__(self,k):
        def _inner(*args, **kwargs): return Func(k, *args, **kwargs)
        return _inner

Sig = _Sig()

#Cell
def compose_tfms(x, tfms, is_enc=True, reverse=False, **kwargs):
    "Apply all `func_nm` attribute of `tfms` on `x`, maybe in `reverse` order"
    if reverse: tfms = reversed(tfms)
    for f in tfms:
        if not is_enc: f = f.decode
        x = f(x, **kwargs)
    return x

#Cell
def mk_transform(f, as_item=True):
    "Convert function `f` to `Transform` if it isn't already one"
    f = instantiate(f)
    return f if isinstance(f,Transform) else Transform(f, as_item=as_item)

#Cell
def gather_attrs(o, k, nm):
    "Used in __getattr__ to collect all attrs `k` from `self.{nm}`"
    if k.startswith('_') or k==nm: raise AttributeError(k)
    att = getattr(o,nm)
    res = [t for t in att.attrgot(k) if t is not None]
    if not res: raise AttributeError(k)
    return res[0] if len(res)==1 else L(res)

#Cell
def gather_attr_names(o, nm):
    "Used in __dir__ to collect all attrs `k` from `self.{nm}`"
    return L(getattr(o,nm)).map(dir).concat().unique()

#Cell
class Pipeline:
    "A pipeline of composed (for encode/decode) transforms, setup with types"
    def __init__(self, funcs=None, as_item=False, split_idx=None):
        self.split_idx,self.default = split_idx,None
        if isinstance(funcs, Pipeline): self.fs = funcs.fs
        else:
            if isinstance(funcs, Transform): funcs = [funcs]
            self.fs = L(ifnone(funcs,[noop])).map(mk_transform).sorted(key='order')
        for f in self.fs:
            name = camel2snake(type(f).__name__)
            a = getattr(self,name,None)
            if a is not None: f = L(a)+f
            setattr(self, name, f)
        self.set_as_item(as_item)

    def set_as_item(self, as_item):
        self.as_item = as_item
        for f in self.fs: f.as_item = as_item

    def setup(self, items=None):
        tfms = self.fs[:]
        self.fs.clear()
        for t in tfms: self.add(t,items)

    def add(self,t, items=None):
        t.setup(items)
        self.fs.append(t)

    def __call__(self, o): return compose_tfms(o, tfms=self.fs, split_idx=self.split_idx)
    def __repr__(self): return f"Pipeline: {self.fs}"
    def __getitem__(self,i): return self.fs[i]
    def __setstate__(self,data): self.__dict__.update(data)
    def __getattr__(self,k): return gather_attrs(self, k, 'fs')
    def __dir__(self): return super().__dir__() + gather_attr_names(self, 'fs')

    def decode  (self, o, full=True):
        if full: return compose_tfms(o, tfms=self.fs, is_enc=False, reverse=True, split_idx=self.split_idx)
        #Not full means we decode up to the point the item knows how to show itself.
        for f in reversed(self.fs):
            if self._is_showable(o): return o
            o = f.decode(o, split_idx=self.split_idx)
        return o

    def show(self, o, ctx=None, **kwargs):
        o = self.decode(o, full=False)
        o1 = [o] if self.as_item or not is_listy(o) else o
        for o_ in o1:
            if hasattr(o_, 'show'): ctx = o_.show(ctx=ctx, **kwargs)
        return ctx

    def _is_showable(self, o):
        return all(hasattr(o_, 'show') for o_ in o) if is_listy(o) else hasattr(o, 'show')
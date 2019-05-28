#AUTOGENERATED! DO NOT EDIT! File to edit: dev/02_data_pipeline.ipynb (unless otherwise specified).

__all__ = ['Transform', 'Pipeline', 'make_tfm', 'TfmdList', 'TfmOver']

from ..imports import *
from ..test import *
from ..core import *
from ..notebook.showdoc import show_doc

@docs
class Transform():
    "A function that `encodes` if `filt` matches, and optionally `decodes`, with an optional `setup`"
    order,filt = 0,None

    def __init__(self, encodes=None, mask=None, is_tuple=None, **kwargs):
        self._done_init = True
        if encodes is not None: self.encodes=encodes
        self.mask,self.is_tuple = mask,is_tuple
        for k,v in kwargs.items(): setattr(self, k, v)

    @classmethod
    def create(cls, f, filt=None):
        "classmethod: Turn `f` into a `Transform` unless it already is one"
        return f if isinstance(f,Transform) else cls(f)

    def setup(self, items=None):
        if getattr(self,'_is_setup',False): return
        self._is_setup = True
        self.setups(items)

    def _apply(self,f,b, **kwargs):
        assert getattr(self,'_done_init',False), f"{self.__class__}: `super().__init__` not called"
        mask = [i==0 for i in range_of(b)] if self.mask is None and self.is_tuple else self.mask
        return tuple(f(o, **kwargs) if p else o for o,p in zip(b,mask)) if self.is_tuple else f(b, **kwargs)

    def _filt_match(self, filt): return self.filt is None or self.filt==filt
    def __call__(self, b, filt=None, **kwargs):
        return self._apply(self.encodes, b, **kwargs) if self._filt_match(filt) else b
    def decode  (self, b, filt=None, **kwargs):
        return self._apply(self.decodes, b, **kwargs) if self._filt_match(filt) else b

    def __getitem__(self, x): return self(x)
    def decodes(self, o, *args, **kwargs): return o
    def setups(self, items): pass
    def __repr__(self): return str(self.encodes) if self.__class__==Transform else str(self.__class__)
    def show(self, o, filt=None, **kwargs): return self.shows(self.decode(o, filt=filt), **kwargs)
    def set_tupled(self, tf=True): self.is_tuple = ifnone(self.is_tuple,tf)

    _docs=dict(__call__="Call `self.encodes` unless `filt` is passed and it doesn't match `self.filt`",
              decode="Call `self.decodes` unless `filt` is passed and it doesn't match `self.filt`",
              decodes="Override to implement custom decoding",
              show="Call `shows` with decoded `o`",
              set_tupled="Set `is_tuple` to `tf` if it was `None` (used internally by `TfmOver`)",
              setup="Override `setups` for setup behavior",
              setups="Override to implement custom setup behavior"
              )

def _set_tupled(tfms, m=True):
    for t in tfms: getattr(t,'set_tupled',noop)(m)

@newchk
class Pipeline(Transform):
    "A pipeline of composed (for encode/decode) transforms, setup one at a time"
    def __init__(self, tfms=None):
        self.tfms,self._tfms = [],L(tfms).mapped(Transform.create)

    def setups(self, items=None):
        "Transform setup"
        self.add(self._tfms, items)
        self._tfms = None

    def add(self, tfms, items=None):
        "Call `setup` on all `tfms` and append them to this pipeline"
        for t in sorted(L(tfms), key=lambda o: getattr(o, 'order', 0)):
            self.tfms.append(t)
            if hasattr(t, 'setup'): t.setup(items)

    def composed(self, x, rev=False, fname='__call__', **kwargs):
        "Compose `{fname}` of all `self.tfms` (reversed if `rev`) on `x`"
        tfms = reversed(self.tfms) if rev else self.tfms
        for f in tfms: x = opt_call(f, fname, x, **kwargs)
        return x

    def __call__(self, x, **kwargs): return self.composed(x, **kwargs)
    def __getitem__(self, x): return self(x)
    def decode(self, x, **kwargs): return self.composed(x, rev=True, fname='decode', **kwargs)
    def decode_at(self, idx): return self.decode(self[idx])
    def show_at(self, idx): return self.show(self[idx])
    def __repr__(self): return str(self.tfms)
    def delete(self, idx): del(self.tfms[idx])
    def remove(self, tfm): self.tfms.remove(tfm)

    def show(self, o, *args, **kwargs):
        "Find last transform that supports `shows` and call it"
        for t in reversed(self.tfms):
            if hasattr(t, 'shows'): return t.show(o, *args, **kwargs)
            o = getattr(t, 'decode', noop)(o)

    def set_tupled(self, m=True): _set_tupled(self._tfms, m)

def make_tfm(tfm):
    "Create a `Pipeline` (if `tfm` is listy) or a `Transform` otherwise"
    return Pipeline(tfm) if is_listy(tfm) else Transform.create(tfm)

@docs
class TfmdList(GetAttr):
    "A transform applied to a collection of `items`"
    _xtra = 'decode __call__ show'.split()

    def __init__(self, items, tfm, do_setup=True):
        self.items = L(items)
        self.default = self.tfm = make_tfm(tfm)
        if do_setup: self.setup()

    def __getitem__(self, i):
        "Transformed item(s) at `i`"
        its = self.items[i]
        return its.mapped(self.tfm) if is_iter(i) else self.tfm(its)

    def decode_batch(self, b, **kwargs):
        "Decode `b`, a list of lists of pipeline outputs (i.e. output of a `DataLoader`)"
        transp = L(zip(*L(b)))
        return transp.mapped(partial(self.decode, **kwargs)).zipped()

    def setup(self): getattr(self.tfm,'setup',noop)(self)
    def subset(self, idxs): return self.__class__(self.items[idxs], self.tfm, do_setup=False)
    def decode_at(self, idx): return self.decode(self[idx])
    def show_at(self, idx): return self.show(self[idx])
    def __eq__(self, b): return all_equal(self, b)
    def __len__(self): return len(self.items)
    def __iter__(self): return (self[i] for i in range_of(self))
    def __repr__(self): return f"{self.__class__.__name__}: {self.items}\ntfms - {self.tfm}"

    _docs = dict(setup="Transform setup with self",
                 decode_at="Decoded item at `idx`",
                 show_at="Show item at `idx`",
                 subset="New `TfmdList` that only includes items at `idxs`")

class TfmOver(Transform):
    "Create tuple containing each of `tfms` applied to each of `o`"
    def __init__(self, tfms=None):
        super().__init__()
        if tfms is None: tfms = [None]
        self.activ,self.tfms = None,L(tfms).mapped(Pipeline)

    def __call__(self, o, *args, **kwargs):
        "List of output of each of `tfms` on `o`"
        if self.activ is not None: return self.tfms[self.activ](o[self.activ], *args, **kwargs)
        return [t(p, *args, **kwargs) for p,t in zip(o,self.tfms)]

    def decode(self, o, **kwargs):
        return [t.decode(p, **kwargs) for p,t in zip(o,self.tfms)]

    def show(self, o, ctx=None, **kwargs):
        "Show result of `show` from each of `tfms`"
        for p,t in zip(o,self.tfms): ctx = t.show(p, ctx=ctx, **kwargs)
        return ctx

    def __repr__(self): return f'TfmOver({self.tfms})'
    def shows(self): pass # needed for `Pipeline` method search for `show`

    def setups(self, o=None):
        "Setup each of `tfms` independently"
        for i,tfm in enumerate(self.tfms):
            self.activ = i
            tfm.setup(o)
        self.activ=None

    @classmethod
    def piped(cls, tfms=None, final_tfms=None):
        "`Pipeline` that duplicates input, then maps `TfmOver` over `tfms`, optionally followed by any `final_tfms`"
        tfms = L(ifnone(tfms,[None]))
        final_tfms = L(final_tfms)
        _set_tupled(final_tfms)
        init_tfm = partial(tuplify,match=tfms)
        return Pipeline([init_tfm,cls(tfms)] + final_tfms)

    xt,yt = add_props(lambda i,x:x.tfms[i])
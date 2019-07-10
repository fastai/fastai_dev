import io,operator,sys,os,re,os,mimetypes,csv,itertools,json,shutil,glob,pickle,tarfile,collections
import hashlib,itertools,types,random,inspect,functools,random,time,math,copy,bz2,types,typing,numbers

from contextlib import redirect_stdout,contextmanager
from typing import Iterable,Iterator,Generator,Callable,Sequence,List,Tuple,Union,Optional
from types import SimpleNamespace
from pathlib import Path
from collections import OrderedDict,defaultdict,Counter,namedtuple
from enum import Enum,IntEnum
from warnings import warn
from functools import partial,reduce
from textwrap import TextWrapper
from operator import itemgetter,attrgetter

# External modules
import torch,matplotlib.pyplot as plt,numpy as np,pandas as pd,scipy
import requests,yaml
from typeguard import typechecked
from fastprogress import progress_bar,master_bar

from torch import as_tensor,Tensor,ByteTensor,LongTensor,FloatTensor,HalfTensor,DoubleTensor
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader,SequentialSampler,RandomSampler
from numpy import array,ndarray
from IPython.core.debugger import set_trace

NoneType = type(None)

Tensor.ndim = property(lambda x: x.dim())

def is_iter(o):
    "Test whether `o` can be used in a `for` loop"
    #Rank 0 tensors in PyTorch are not really iterable
    return isinstance(o, (Iterable,Generator)) and getattr(o,'ndim',1)

def all_equal(a,b):
    "Compares whether `a` and `b` are the same length and have the same contents"
    if not is_iter(b): return False
    return all(equals(a_,b_) for a_,b_ in itertools.zip_longest(a,b))

def equals(a,b):
    "Compares `a` and `b` for equality; supports sublists, tensors and arrays too"
    cmp = (torch.equal    if isinstance(a, Tensor  ) and a.dim() else
           np.array_equal if isinstance(a, ndarray ) else
           operator.eq    if isinstance(a, str     ) else
           all_equal      if is_iter(a) else
           operator.eq)
    return cmp(a,b)


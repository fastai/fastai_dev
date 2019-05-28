#AUTOGENERATED! DO NOT EDIT! File to edit: dev/06_vision_core.ipynb (unless otherwise specified).

__all__ = ['Image', 'Imagify', 'ImageConverter', 'image_resize', 'ImageResizer', 'image2byte', 'unpermute_image',
           'ImageToByteTensor']

from ..imports import *
from ..test import *
from ..core import *
from ..data.pipeline import *
from ..data.core import *
from ..data.external import *

from PIL import Image

class Imagify(Transform):
    "Open an `Image` from path `fn`, show with `cmap` and `alpha`"
    def __init__(self, func=Image.open, **kwargs):
        super().__init__()
        self.func,self.kw = func,kwargs

    def encodes(self, fn): return Image.open(fn)
    def shows(self, im, ctx=None, figsize=None):
        return show_image(im, ax=ctx, figsize=figsize, **self.kw)

class ImageConverter(Transform):
    "Convert `img` to `mode`"
    def __init__(self, mode='RGB', mask=None, is_tuple=None):
        super().__init__(mask=mask, is_tuple=is_tuple)
        self.mode = mode

    def encodes(self, o): return o.convert(self.mode)

def image_resize(img, size, resample=Image.BILINEAR):
    "Resize image to `size` using `resample"
    return img.resize(size, resample=resample)
image_resize.order=10

class ImageResizer(Transform):
    "Resize image to `size` using `resample"
    def __init__(self, size, resample=Image.BILINEAR, mask=None, is_tuple=None):
        super().__init__(mask=mask, is_tuple=is_tuple)
        if not is_listy(size): size=(size,size)
        self.size,self.resample = size,resample

    def encodes(self, o): return image_resize(o, size=self.size, resample=self.resample)

def image2byte(img):
    "Transform image to byte tensor in `c*h*w` dim order."
    res = torch.ByteTensor(torch.ByteStorage.from_buffer(img.tobytes()))
    w,h = img.size
    return res.view(h,w,-1).permute(2,0,1)

def unpermute_image(img):
    "Convert `c*h*w` dim order to `h*w*c` (or just `h*w` if 1 channel)"
    return img[0] if img.shape[0] == 1 else img.permute(1,2,0)

class ImageToByteTensor(Transform):
    "Transform image to byte tensor in `c*h*w` dim order."
    order=15
    def encodes(self, o): return image2byte(o)
    def decodes(self, o): return unpermute_image(o)
from exp.nb_11 import *
from fastai.datasets import *

bs = 64
lr = 4e-3
pct_start = 0.5
size = 128
mixup = 0.2

lr *= bs/256
pcts = [pct_start,1-pct_start]
sched_lr  = combine_scheds(pcts, cos_1cycle_anneal(lr/10., lr, 0))
sched_mom = combine_scheds(pcts, cos_1cycle_anneal(0.95, 0.85, 0.95))
tfms = [make_rgb, PilTiltRandomCrop(size, 160, magnitude=0.2), PilRandomFlip(), np_to_float]

url = URLs.IMAGENETTE_160 if size<140 else URLs.IMAGENETTE_320 if size<240 else URLs.IMAGENETTE
path = untar_data(url)
il = ImageList.from_files(path, tfms=tfms)
sd = SplitData.split_by_func(il, partial(grandparent_splitter, valid_name='val'))
ll = label_by_func(sd, parent_labeler)
ll.valid.x.tfms = [make_rgb, CenterCrop(size), to_byte_tensor, to_float_tensor]
train_dl,valid_dl = get_dls(ll.train,ll.valid,bs, num_workers=4)
data = DataBunch(train_dl, valid_dl, 3, 10)

cbfs = [partial(AvgStatsCallback,accuracy), CudaCallback, ProgressCallback,
        partial(BatchTransformXCallback, norm_imagenette)]
if sched_lr : cbfs.append(partial(ParamScheduler, 'lr' , sched_lr))
if sched_mom: cbfs.append(partial(ParamScheduler, 'mom', sched_mom))
if mixup    : cbfs.append(partial(MixUp, alpha=mixup))

loss_func = LabelSmoothingCrossEntropy()
arch = partial(xresnet18, num_classes=10)
stats = [AverageGrad(dampening=True), AverageSqrGrad(), StepCount()]
opt_func = partial(StatefulOptimizer, steppers=AdamStep(), stats=stats,
               mom=0.9, mom_sqr=0.99, eps=1e-7)

learn = Learner(arch(), data, loss_func, lr=lr, cb_funcs=cbfs, opt_func=opt_func)
learn.fit(5)


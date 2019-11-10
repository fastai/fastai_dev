#AUTOGENERATED! DO NOT EDIT! File to edit: dev/14_callback_schedule.ipynb (unless otherwise specified).

__all__ = ['annealer', 'SchedLin', 'SchedCos', 'SchedNo', 'SchedExp', 'SchedPoly', 'combine_scheds', 'combined_cos',
           'ParamScheduler', 'LRFinder']

#Cell
from ..test import *
from ..basics import *

#Cell
def annealer(f):
    "Decorator to make `f` return itself partially applied."
    @functools.wraps(f)
    def _inner(start, end): return partial(f, start, end)
    return _inner

#Cell
@annealer
def SchedLin(start, end, pos): return start + pos*(end-start)
@annealer
def SchedCos(start, end, pos): return start + (1 + math.cos(math.pi*(1-pos))) * (end-start) / 2
@annealer
def SchedNo (start, end, pos): return start
@annealer
def SchedExp(start, end, pos): return start * (end/start) ** pos

SchedLin.__doc__ = "Linear schedule function from `start` to `end`"
SchedCos.__doc__ = "Cosine schedule function from `start` to `end`"
SchedNo .__doc__ = "Constant schedule function with `start` value"
SchedExp.__doc__ = "Exponential schedule function from `start` to `end`"

#Cell
def SchedPoly(start, end, power):
    "Polynomial schedule (of `power`) function from `start` to `end`"
    def _inner(pos): return start + (end - start) * pos ** power
    return _inner

#Cell
def combine_scheds(pcts, scheds):
    "Combine `scheds` according to `pcts` in one function"
    assert sum(pcts) == 1.
    pcts = tensor([0] + L(pcts))
    assert torch.all(pcts >= 0)
    pcts = torch.cumsum(pcts, 0)
    def _inner(pos):
        if pos == 1.: return scheds[-1](1.)
        idx = (pos >= pcts).nonzero().max()
        actual_pos = (pos-pcts[idx]) / (pcts[idx+1]-pcts[idx])
        return scheds[idx](actual_pos)
    return _inner

#Cell
def combined_cos(pct, start, middle, end):
    "Return a combined scheduler with cosine annealing from `start` to `middle` then `middle` to `end`"
    #if isinstance(start, Iterable):
    #    return [combine_scheds([pct,1-pct], [SchedCos(s, m), SchedCos(m, e)])
    #            for s,m,e in zip(start,middle,end)]
    return combine_scheds([pct,1-pct], [SchedCos(start, middle), SchedCos(middle, end)])

#Cell
@docs
class ParamScheduler(Callback):
    "Schedule hyper-parameters according to `scheds`"
    run_after=TrainEvalCallback

    def __init__(self, scheds): self.scheds = scheds
    def begin_fit(self): self.hps = {p:[] for p in self.scheds.keys()}

    def _update_val(self, pct):
        for n,f in self.scheds.items(): self.opt.set_hyper(n, f(pct))

    def begin_batch(self):
        if not self.training: return
        self._update_val(self.pct_train)

    def after_batch(self):
        if self.training:
            for p in self.scheds.keys(): self.hps[p].append(self.opt.hypers[-1][p])

    def after_fit(self):
        if hasattr(self.learn, 'recorder'): self.recorder.hps = self.hps

    _docs = {"begin_fit": "Initialize container for hyper-parameters",
             "begin_batch": "Set the proper hyper-parameters in the optimizer",
             "after_batch": "Record hyper-parameters of this batch",
             "after_fit": "Save the hyper-parameters in the recorder if there is one"}

#Cell
@patch
def fit_one_cycle(self:Learner, n_epoch, lr_max=None, div=25., div_final=1e5, pct_start=0.25, wd=defaults.wd,
                  moms=(0.95,0.85,0.95), cbs=None, reset_opt=False):
    "Fit `self.model` for `n_epoch` using the 1cycle policy."
    if self.opt is None: self.create_opt()
    self.opt.set_hyper('lr', self.lr if lr_max is None else lr_max)
    lr_max = np.array([h['lr'] for h in self.opt.hypers])
    scheds = {'lr': combined_cos(pct_start, lr_max/div, lr_max, lr_max/div_final),
              'mom': combined_cos(pct_start, *moms)}
    self.fit(n_epoch, cbs=ParamScheduler(scheds)+L(cbs), reset_opt=reset_opt, wd=wd)

#Cell
@patch
def plot_sched(self:Recorder, figsize=None):
    rows,cols = (len(self.hps)+1)//2, min(2, len(self.hps))
    figsize = figsize or (6*cols,4*rows)
    _, axs = plt.subplots(rows, cols, figsize=figsize)
    axs = axs.flatten() if len(self.hps) > 1 else L(axs)
    for p,ax in zip(self.hps.keys(), axs):
        ax.plot(self.hps[p])
        ax.set_ylabel(p)

#Cell
@patch
def fit_flat_cos(self:Learner, n_epoch, lr=None, div_final=1e5, pct_start=0.75, wd=defaults.wd,
                 cbs=None, reset_opt=False):
    "Fit `self.model` for `n_epoch` at flat `lr` before a cosine annealing."
    if self.opt is None: self.create_opt()
    self.opt.set_hyper('lr', self.lr if lr is None else lr)
    lr = np.array([h['lr'] for h in self.opt.hypers])
    scheds = {'lr': combined_cos(pct_start, lr, lr, lr/div_final)}
    self.fit(n_epoch, cbs=ParamScheduler(scheds)+L(cbs), reset_opt=reset_opt, wd=wd)

#Cell
@patch
def fit_sgdr(self:Learner, n_cycles, cycle_len, lr_max=None, cycle_mult=2, cbs=None, reset_opt=False, wd=defaults.wd):
    "Fit `self.model` for `n_cycles` of `cycle_len` using SGDR."
    if self.opt is None: self.create_opt()
    self.opt.set_hyper('lr', self.lr if lr_max is None else lr_max)
    lr_max = np.array([h['lr'] for h in self.opt.hypers])
    n_epoch = cycle_len * (cycle_mult**n_cycles-1)//(cycle_mult-1)
    pcts = [cycle_len * cycle_mult**i / n_epoch for i in range(n_cycles)]
    scheds = [SchedCos(lr_max, 0) for _ in range(n_cycles)]
    scheds = {'lr': combine_scheds(pcts, scheds)}
    self.fit(n_epoch, cbs=ParamScheduler(scheds)+L(cbs), reset_opt=reset_opt, wd=wd)

#Cell
@docs
class LRFinder(ParamScheduler):
    "Training with exponentially growing learning rate"
    run_after=Recorder

    def __init__(self, start_lr=1e-7, end_lr=10, num_it=100, stop_div=True):
        if is_listy(start_lr):
            self.scheds = {'lr': [SchedExp(s, e) for (s,e) in zip(start_lr,end_lr)]}
        else: self.scheds = {'lr': SchedExp(start_lr, end_lr)}
        self.num_it,self.stop_div = num_it,stop_div

    def begin_fit(self):
        super().begin_fit()
        self.learn.save('_tmp')
        self.best_loss = float('inf')

    def begin_batch(self):
        self._update_val(self.train_iter/self.num_it)

    def after_batch(self):
        super().after_batch()
        if self.smooth_loss < self.best_loss: self.best_loss = self.smooth_loss
        if self.smooth_loss > 4*self.best_loss and self.stop_div: raise CancelFitException()
        if self.train_iter >= self.num_it: raise CancelFitException()

    def begin_validate(self): raise CancelValidException()

    def after_fit(self):
        self.learn.load('_tmp')
        os.remove(self.path/self.model_dir/'_tmp.pth')

    _docs = {"begin_fit": "Initialize container for hyper-parameters and save the model",
             "begin_batch": "Set the proper hyper-parameters in the optimizer",
             "after_batch": "Record hyper-parameters of this batch and potentially stop training",
             "after_fit": "Save the hyper-parameters in the recorder if there is one and load the original model",
             "begin_validate": "Skip the validation part of training"}

#Cell
@patch
def plot_lr_find(self:Recorder, skip_end=5):
    "Plot the result of an LR Finder test (won't work if you didn't do `learn.lr_find()` before)"
    lrs    = self.lrs    if skip_end==0 else self.lrs   [:-skip_end]
    losses = self.losses if skip_end==0 else self.losses[:-skip_end]
    fig, ax = plt.subplots(1,1)
    ax.plot(lrs, losses)
    ax.set_ylabel("Loss")
    ax.set_xlabel("Learning Rate")
    ax.set_xscale('log')

#Cell
@patch
def lr_find(self:Learner, start_lr=1e-7, end_lr=10, num_it=100, stop_div=True, show_plot=True):
    "Launch a mock training to find a good learning rate"
    try: n_epoch = num_it//len(self.dbunch.train_dl) + 1
    except TypeError: n_epoch = 1
    cb=LRFinder(start_lr=start_lr, end_lr=end_lr, num_it=num_it, stop_div=stop_div)
    with self.no_logging(): self.fit(n_epoch, cbs=cb)
    if show_plot: self.recorder.plot_lr_find()
import matplotlib.pyplot as plt
import numpy as np

from treesimulator import save_forest, DIST_TO_START
from treesimulator.generator import generate
from treesimulator.mtbd_models import BirthDeathModel

# 1. BD, BD-CT(1) and BD-CT(1)-Skyline
## BD model
bd_model = BirthDeathModel(p=0.5, la=0.5, psi=0.25)
[bd_tree], (_, _, T), _ = generate([bd_model], min_tips=200, max_tips=500)
ext_ds, int_ds = [_.dist for _ in bd_tree], [_.dist for _ in bd_tree.traverse() if not _.is_leaf()]
ext_ts, int_ts = [getattr(_, DIST_TO_START) for _ in bd_tree], [getattr(_, DIST_TO_START) for _ in bd_tree.traverse() if not _.is_leaf()]
fig, ax = plt.subplots()
sort_indices_ext = np.argsort(ext_ts)
ext_ts, ext_ds = np.array(ext_ts)[sort_indices_ext], np.array(ext_ds)[sort_indices_ext]
sort_indices_int = np.argsort(int_ts)
int_ts, int_ds = np.array(int_ts)[sort_indices_int], np.array(int_ds)[sort_indices_int]


ax.plot(ext_ts, ext_ds, marker='o', label='external', color='b', linestyle='None', alpha=0.5)

slope, intercept = np.polyfit(ext_ts, ext_ds, 1)
fit_func = np.poly1d((slope, intercept))
plt.plot(ext_ts, fit_func(ext_ts), color='b', label='Fitted external line')


ax.plot(int_ts, int_ds, marker='s', label='internal', color='g', linestyle='None', alpha=0.5)

slope, intercept = np.polyfit(int_ts, int_ds, 1)
fit_func = np.poly1d((slope, intercept))
plt.plot(int_ts, fit_func(int_ts), color='g', label='Fitted internal line')


save_forest([bd_tree], 'BD_tree.nwk')
## BD-Skyline models
bd_model_2 = BirthDeathModel(p=0.5, la=0.5, psi=0.125)
[bdsky_tree], _, _ = generate([bd_model, bd_model_2], skyline_times=[2 * T / 3],
                                     min_tips=200, max_tips=500)
save_forest([bdsky_tree], 'BDSKY_tree.nwk')
ext_ds, int_ds = [_.dist for _ in bdsky_tree], [_.dist for _ in bdsky_tree.traverse() if not _.is_leaf()]
ext_ts, int_ts = [getattr(_, DIST_TO_START) for _ in bdsky_tree], [getattr(_, DIST_TO_START) for _ in bdsky_tree.traverse() if not _.is_leaf()]

sort_indices_ext = np.argsort(ext_ts)
ext_ts, ext_ds = np.array(ext_ts)[sort_indices_ext], np.array(ext_ds)[sort_indices_ext]
sort_indices_int = np.argsort(int_ts)
int_ts, int_ds = np.array(int_ts)[sort_indices_int], np.array(int_ds)[sort_indices_int]

ax.plot(ext_ts, ext_ds, marker='d', label='external-sky', color='r', linestyle='None', alpha=0.5)

slope, intercept = np.polyfit(ext_ts, ext_ds, 1)
fit_func = np.poly1d((slope, intercept))
plt.plot(ext_ts, fit_func(ext_ts), color='r', label='Fitted external-sky line')

ax.plot(int_ts, int_ds, marker='*', label='internal-sky', color='m', linestyle='None', alpha=0.5)

slope, intercept = np.polyfit(int_ts, int_ds, 1)
fit_func = np.poly1d((slope, intercept))
plt.plot(int_ts, fit_func(int_ts), color='m', label='Fitted internal-sky line')


plt.show()
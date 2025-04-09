import os
from typing import List, Tuple, Literal as Lit
import joblib
import numpy as np
import scipy.stats as sp_stats
import pandas as pd

from numpy import nan, inf
from numpy import exp, log



# ======================================================== #
# ======================== System ======================== #
# ======================================================== #
HEADERS = { 'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36', 'X-Requested-With':'XMLHttpRequest' }


def _pickle(CASES:Lit['COMPUTE','RELOAD','LOAD'], Lambda, dirs=[], name='', ext='.pkl', *a,**b):

    path    = os.path.join(*dirs, name + ext)
    EXISTS  = os.path.exists(path)

    def _calc():    return Lambda(*a,**b)
    def _read():    return joblib.load(path)
    def _save(X):   joblib.dump(X, path);  return X

    if (CASES == 'COMPUTE'):    return _calc()
    if (CASES == 'RELOAD'):     return _save(_calc())
    if (CASES == 'LOAD'):
        if     EXISTS:          return _read()
        if not EXISTS:          return _save(_calc())


def _parquet(CASES:Lit['COMPUTE','RELOAD','LOAD'], Lambda, dirs=[], name='', ext='.parquet', *a,**b):

    path    = os.path.join(*dirs, name + ext)
    EXISTS  = os.path.exists(path)

    def _calc():    return Lambda(*a,**b)
    def _read():    return pd.read_parquet(path)
    def _save(Df):  Df.to_parquet(path, index=False);  return Df

    if (CASES == 'COMPUTE'):    return _calc()
    if (CASES == 'RELOAD'):     return _save(_calc())
    if (CASES == 'LOAD'):
        if     EXISTS:          return _read()
        if not EXISTS:          return _save(_calc())



# ================================================================ #
# ======================== Text Functions ======================== #
# ================================================================ #
def _between(txt:str, A:str, Z:str):
    return txt.split(A)[1].split(Z)[0]


def _replaces(txt:str, args:List[Tuple[str, str]]):
    
    for (old, new) in args:
        txt = txt.replace(old, new)

    return txt



# ================================================================== #
# ======================== Math Functions 1 ======================== #
# ================================================================== #
def _step(X, stp=nan): 
    if isinstance(X, int) and (X < 0) or (1 < X):
            return X[::stp]
    else:   return X

def _round(x, R=nan):
    if isinstance(x, int) and (x >= 0):
            return np.round(x, R)
    else:   return x



def _sum(x):        return np.nansum(x)
def _prod(x):       return np.nanprod(x)

def _cumsum(x):     return np.nancumsum(x)
def _cumprod(x):    return np.nancumprod(x)

def _mean(x):       return np.nanmean(x)
def _std(x):        return np.nanstd(x)

def _gmean(x):      return exp(np.nanmean(log(x)))
def _gstd(x):       return exp(np.nanstd(log(x)))

def _med(x):        return np.nanmedian(x)
def _mad(x):        return sp_stats.median_abs_deviation(x, nan_policy='omit')

def _max(x):        return np.nanmax(x)
def _min(x):        return np.nanmin(x)

def _Q3(x):         return np.nanpercentile(x, 75)
def _Q1(x):         return np.nanpercentile(x, 25)



def _pct(x, Lambda): return Lambda(1+x/100)*100-100

def _pct_gmean(x):   return _pct(x, _gmean)
def _pct_gstd(x):    return _pct(x, _gstd)



def _range(Max, Min):               return (Max - Min)
def _IQR(Q3, Q1):                   return (Q3 - Q1)

def _minmax(Val, Min, Range):       return (Val - Min) / Range *100
def _robust(val, med, IQR):         return (val - med) / IQR   *100

def _zscore(val, avg, dev):         return (val - avg) / dev
def _pscore(val, series):           return sp_stats.percentileofscore(series, val, 'mean', 'omit')

def _log1p_zscore(val, avg, dev):   return (log(1+val/100) - log(1+avg/100)) / log(1+dev/100)



# ================================================================== #
# ======================== Math Functions 2 ======================== #
# ================================================================== #
def _groupby(Df, By=''):
    if By:  return Df.groupby(By, sort=0, group_keys=0, dropna=0)
    else:   return Df

def _roll(Df, Col, Lambda, win, wmin, By='', stp=nan, R=nan):
    return _round(_groupby(_step(Df, stp), By)[Col].rolling(win, wmin).apply(Lambda).reset_index(0,drop=1), R)



def _roll_mean      (Df, Col, win, wmin, By='', stp=nan, R=nan):   return _roll(Df, Col, _mean,      win, wmin, By, stp, R)
def _roll_std       (Df, Col, win, wmin, By='', stp=nan, R=nan):   return _roll(Df, Col, _std,       win, wmin, By, stp, R)

def _roll_gmean     (Df, Col, win, wmin, By='', stp=nan, R=nan):   return _roll(Df, Col, _gmean,     win, wmin, By, stp, R)
def _roll_gstd      (Df, Col, win, wmin, By='', stp=nan, R=nan):   return _roll(Df, Col, _gstd,      win, wmin, By, stp, R)

def _roll_pct_gmean (Df, Col, win, wmin, By='', stp=nan, R=nan):   return _roll(Df, Col, _pct_gmean, win, wmin, By, stp, R)
def _roll_pct_gstd  (Df, Col, win, wmin, By='', stp=nan, R=nan):   return _roll(Df, Col, _pct_gstd,  win, wmin, By, stp, R)

def _roll_med       (Df, Col, win, wmin, By='', stp=nan, R=nan):   return _roll(Df, Col, _med,       win, wmin, By, stp, R)
def _roll_mad       (Df, Col, win, wmin, By='', stp=nan, R=nan):   return _roll(Df, Col, _mad,       win, wmin, By, stp, R)

def _roll_max       (Df, Col, win, wmin, By='', stp=nan, R=nan):   return _roll(Df, Col, _max,       win, wmin, By, stp, R)
def _roll_min       (Df, Col, win, wmin, By='', stp=nan, R=nan):   return _roll(Df, Col, _min,       win, wmin, By, stp, R)

def _roll_Q3        (Df, Col, win, wmin, By='', stp=nan, R=nan):   return _roll(Df, Col, _Q3,        win, wmin, By, stp, R)
def _roll_Q1        (Df, Col, win, wmin, By='', stp=nan, R=nan):   return _roll(Df, Col, _Q1,        win, wmin, By, stp, R)

def _roll_range     (Df, Col, win, wmin, By='', stp=nan, R=nan):   return _round(_range(Max=_roll_max(Df, Col, win, wmin, By, stp), Min=_roll_min(Df, Col, win, wmin, By, stp)), R)
def _roll_iqr       (Df, Col, win, wmin, By='', stp=nan, R=nan):   return _round(  _IQR( Q3= _roll_Q3(Df, Col, win, wmin, By, stp),  Q1= _roll_Q1(Df, Col, win, wmin, By, stp)), R)



def _roll_minmax     (Df, Col, win, wmin, By='', stp=nan, R=nan):  return _round(      _minmax(Val=Df[Col],  Min=      _roll_min(Df, Col, win, wmin, By, stp),  Range= _roll_range(Df, Col, win, wmin, By, stp)), R)
def _roll_robust     (Df, Col, win, wmin, By='', stp=nan, R=nan):  return _round(      _robust(val=Df[Col],  med=      _roll_med(Df, Col, win, wmin, By, stp),  IQR=     _roll_iqr(Df, Col, win, wmin, By, stp)), R)
def _roll_zscore     (Df, Col, win, wmin, By='', stp=nan, R=nan):  return _round(      _zscore(val=Df[Col],  avg=     _roll_mean(Df, Col, win, wmin, By, stp),  dev=     _roll_std(Df, Col, win, wmin, By, stp)), R)
def _roll_pct_gscore (Df, Col, win, wmin, By='', stp=nan, R=nan):  return _round(_log1p_zscore(val=Df[Col],  avg=_roll_pct_gmean(Df, Col, win, wmin, By, stp),  dev=_roll_pct_gstd(Df, Col, win, wmin, By, stp)), R)

def _roll_pscore     (Df, Col, win, wmin, By='', stp=nan, R=nan):  return _roll(Df, Col, lambda X: _pscore(val=X.tail(1), series=X), win, wmin, By, stp, R)
#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 


import sys
import traceback

from runtime.Worker import worker

MainWorker = worker()

_PLCObjectSingleton = None


def GetPLCObjectSingleton():
    assert _PLCObjectSingleton is not None
    return _PLCObjectSingleton


def LogMessageAndException(msg, exp=None):
    if exp is None:
        exp = sys.exc_info()
    if _PLCObjectSingleton is not None:
        _PLCObjectSingleton.LogMessage(0, msg + '\n'.join(traceback.format_exception(*exp)))
    print(msg)
    traceback.print_exception(*exp)


def CreatePLCObjectSingleton(*args, **kwargs):
    global _PLCObjectSingleton
    from runtime.PLCObject import PLCObject  # noqa # pylint: disable=wrong-import-position
    _PLCObjectSingleton = PLCObject(*args, **kwargs)


def default_evaluator(tocall, *args, **kwargs):
    try:
        res = (tocall(*args, **kwargs), None)
    except Exception:
        res = (None, sys.exc_info())
    return res

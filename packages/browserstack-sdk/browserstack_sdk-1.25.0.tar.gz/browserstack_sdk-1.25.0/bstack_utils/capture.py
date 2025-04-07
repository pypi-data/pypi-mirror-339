# coding: UTF-8
import sys
bstack11111ll_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack111_opy_ = 7
def bstack11l1l11_opy_ (bstack11lll_opy_):
    global bstack1l11l11_opy_
    bstack1l1l1_opy_ = ord (bstack11lll_opy_ [-1])
    bstack1l111ll_opy_ = bstack11lll_opy_ [:-1]
    bstack11l_opy_ = bstack1l1l1_opy_ % len (bstack1l111ll_opy_)
    bstack11l111l_opy_ = bstack1l111ll_opy_ [:bstack11l_opy_] + bstack1l111ll_opy_ [bstack11l_opy_:]
    if bstack11111ll_opy_:
        bstack1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1l1l11_opy_ + bstack1l1l1_opy_) % bstack111_opy_) for bstack1l1l11_opy_, char in enumerate (bstack11l111l_opy_)])
    else:
        bstack1l_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1l1l11_opy_ + bstack1l1l1_opy_) % bstack111_opy_) for bstack1l1l11_opy_, char in enumerate (bstack11l111l_opy_)])
    return eval (bstack1l_opy_)
import builtins
import logging
class bstack11l11111ll_opy_:
    def __init__(self, handler):
        self._1l111111l1l_opy_ = builtins.print
        self.handler = handler
        self._started = False
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self._1l111111lll_opy_ = {
            level: getattr(self.logger, level)
            for level in [bstack11l1l11_opy_ (u"ࠧࡪࡰࡩࡳࠬᗋ"), bstack11l1l11_opy_ (u"ࠨࡦࡨࡦࡺ࡭ࠧᗌ"), bstack11l1l11_opy_ (u"ࠩࡺࡥࡷࡴࡩ࡯ࡩࠪᗍ"), bstack11l1l11_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩᗎ")]
        }
    def start(self):
        if self._started:
            return
        self._started = True
        builtins.print = self._1l111111l11_opy_
        self._1l11111l11l_opy_()
    def _1l111111l11_opy_(self, *args, **kwargs):
        self._1l111111l1l_opy_(*args, **kwargs)
        message = bstack11l1l11_opy_ (u"ࠫࠥ࠭ᗏ").join(map(str, args)) + bstack11l1l11_opy_ (u"ࠬࡢ࡮ࠨᗐ")
        self._log_message(bstack11l1l11_opy_ (u"࠭ࡉࡏࡈࡒࠫᗑ"), message)
    def _log_message(self, level, msg, *args, **kwargs):
        if self.handler:
            self.handler({bstack11l1l11_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ᗒ"): level, bstack11l1l11_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᗓ"): msg})
    def _1l11111l11l_opy_(self):
        for level, bstack1l111111ll1_opy_ in self._1l111111lll_opy_.items():
            setattr(logging, level, self._1l11111l111_opy_(level, bstack1l111111ll1_opy_))
    def _1l11111l111_opy_(self, level, bstack1l111111ll1_opy_):
        def wrapper(msg, *args, **kwargs):
            bstack1l111111ll1_opy_(msg, *args, **kwargs)
            self._log_message(level.upper(), msg)
        return wrapper
    def reset(self):
        if not self._started:
            return
        self._started = False
        builtins.print = self._1l111111l1l_opy_
        for level, bstack1l111111ll1_opy_ in self._1l111111lll_opy_.items():
            setattr(logging, level, bstack1l111111ll1_opy_)
# coding: UTF-8
import sys
bstack11l1ll1_opy_ = sys.version_info [0] == 2
bstack1111l11_opy_ = 2048
bstack1l11111_opy_ = 7
def bstack1ll1l1_opy_ (bstack1l1ll1_opy_):
    global bstack1l111ll_opy_
    bstack1lll1ll_opy_ = ord (bstack1l1ll1_opy_ [-1])
    bstack111llll_opy_ = bstack1l1ll1_opy_ [:-1]
    bstack1l1l11l_opy_ = bstack1lll1ll_opy_ % len (bstack111llll_opy_)
    bstack1l1l1l_opy_ = bstack111llll_opy_ [:bstack1l1l11l_opy_] + bstack111llll_opy_ [bstack1l1l11l_opy_:]
    if bstack11l1ll1_opy_:
        bstack11ll111_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l11_opy_ - (bstackl_opy_ + bstack1lll1ll_opy_) % bstack1l11111_opy_) for bstackl_opy_, char in enumerate (bstack1l1l1l_opy_)])
    else:
        bstack11ll111_opy_ = str () .join ([chr (ord (char) - bstack1111l11_opy_ - (bstackl_opy_ + bstack1lll1ll_opy_) % bstack1l11111_opy_) for bstackl_opy_, char in enumerate (bstack1l1l1l_opy_)])
    return eval (bstack11ll111_opy_)
import builtins
import logging
class bstack11l111l1l1_opy_:
    def __init__(self, handler):
        self._11lll11l1l1_opy_ = builtins.print
        self.handler = handler
        self._started = False
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self._11lll11ll1l_opy_ = {
            level: getattr(self.logger, level)
            for level in [bstack1ll1l1_opy_ (u"ࠪ࡭ࡳ࡬࡯ࠨᙚ"), bstack1ll1l1_opy_ (u"ࠫࡩ࡫ࡢࡶࡩࠪᙛ"), bstack1ll1l1_opy_ (u"ࠬࡽࡡࡳࡰ࡬ࡲ࡬࠭ᙜ"), bstack1ll1l1_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬᙝ")]
        }
    def start(self):
        if self._started:
            return
        self._started = True
        builtins.print = self._11lll11l1ll_opy_
        self._11lll11llll_opy_()
    def _11lll11l1ll_opy_(self, *args, **kwargs):
        self._11lll11l1l1_opy_(*args, **kwargs)
        message = bstack1ll1l1_opy_ (u"ࠧࠡࠩᙞ").join(map(str, args)) + bstack1ll1l1_opy_ (u"ࠨ࡞ࡱࠫᙟ")
        self._log_message(bstack1ll1l1_opy_ (u"ࠩࡌࡒࡋࡕࠧᙠ"), message)
    def _log_message(self, level, msg, *args, **kwargs):
        if self.handler:
            self.handler({bstack1ll1l1_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩᙡ"): level, bstack1ll1l1_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᙢ"): msg})
    def _11lll11llll_opy_(self):
        for level, bstack11lll11lll1_opy_ in self._11lll11ll1l_opy_.items():
            setattr(logging, level, self._11lll11ll11_opy_(level, bstack11lll11lll1_opy_))
    def _11lll11ll11_opy_(self, level, bstack11lll11lll1_opy_):
        def wrapper(msg, *args, **kwargs):
            bstack11lll11lll1_opy_(msg, *args, **kwargs)
            self._log_message(level.upper(), msg)
        return wrapper
    def reset(self):
        if not self._started:
            return
        self._started = False
        builtins.print = self._11lll11l1l1_opy_
        for level, bstack11lll11lll1_opy_ in self._11lll11ll1l_opy_.items():
            setattr(logging, level, bstack11lll11lll1_opy_)
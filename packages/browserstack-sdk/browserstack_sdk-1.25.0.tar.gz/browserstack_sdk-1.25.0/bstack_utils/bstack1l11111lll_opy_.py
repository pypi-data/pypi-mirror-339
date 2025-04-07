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
from collections import deque
from bstack_utils.constants import *
class bstack11lll1lll1_opy_:
    def __init__(self):
        self._111lllllll1_opy_ = deque()
        self._11l1111l1l1_opy_ = {}
        self._11l111111l1_opy_ = False
    def bstack11l1111111l_opy_(self, test_name, bstack11l1111l111_opy_):
        bstack11l111111ll_opy_ = self._11l1111l1l1_opy_.get(test_name, {})
        return bstack11l111111ll_opy_.get(bstack11l1111l111_opy_, 0)
    def bstack11l11111l11_opy_(self, test_name, bstack11l1111l111_opy_):
        bstack11l11111lll_opy_ = self.bstack11l1111111l_opy_(test_name, bstack11l1111l111_opy_)
        self.bstack11l1111l11l_opy_(test_name, bstack11l1111l111_opy_)
        return bstack11l11111lll_opy_
    def bstack11l1111l11l_opy_(self, test_name, bstack11l1111l111_opy_):
        if test_name not in self._11l1111l1l1_opy_:
            self._11l1111l1l1_opy_[test_name] = {}
        bstack11l111111ll_opy_ = self._11l1111l1l1_opy_[test_name]
        bstack11l11111lll_opy_ = bstack11l111111ll_opy_.get(bstack11l1111l111_opy_, 0)
        bstack11l111111ll_opy_[bstack11l1111l111_opy_] = bstack11l11111lll_opy_ + 1
    def bstack11ll111l11_opy_(self, bstack11l11111ll1_opy_, bstack11l11111l1l_opy_):
        bstack111llllllll_opy_ = self.bstack11l11111l11_opy_(bstack11l11111ll1_opy_, bstack11l11111l1l_opy_)
        event_name = bstack11lllll1111_opy_[bstack11l11111l1l_opy_]
        bstack1l1lll1l11l_opy_ = bstack11l1l11_opy_ (u"ࠢࡼࡿ࠰ࡿࢂ࠳ࡻࡾࠤᱛ").format(bstack11l11111ll1_opy_, event_name, bstack111llllllll_opy_)
        self._111lllllll1_opy_.append(bstack1l1lll1l11l_opy_)
    def bstack1l111l1111_opy_(self):
        return len(self._111lllllll1_opy_) == 0
    def bstack11lll1111l_opy_(self):
        bstack11l11111111_opy_ = self._111lllllll1_opy_.popleft()
        return bstack11l11111111_opy_
    def capturing(self):
        return self._11l111111l1_opy_
    def bstack11llllll1l_opy_(self):
        self._11l111111l1_opy_ = True
    def bstack11l1llll1_opy_(self):
        self._11l111111l1_opy_ = False
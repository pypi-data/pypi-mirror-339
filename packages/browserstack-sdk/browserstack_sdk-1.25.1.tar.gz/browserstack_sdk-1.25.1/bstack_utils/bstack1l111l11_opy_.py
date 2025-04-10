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
from collections import deque
from bstack_utils.constants import *
class bstack1llllllll1_opy_:
    def __init__(self):
        self._111ll1l111l_opy_ = deque()
        self._111ll111ll1_opy_ = {}
        self._111ll11ll11_opy_ = False
    def bstack111ll11llll_opy_(self, test_name, bstack111ll1l1111_opy_):
        bstack111ll11lll1_opy_ = self._111ll111ll1_opy_.get(test_name, {})
        return bstack111ll11lll1_opy_.get(bstack111ll1l1111_opy_, 0)
    def bstack111ll11l11l_opy_(self, test_name, bstack111ll1l1111_opy_):
        bstack111ll11l1ll_opy_ = self.bstack111ll11llll_opy_(test_name, bstack111ll1l1111_opy_)
        self.bstack111ll111lll_opy_(test_name, bstack111ll1l1111_opy_)
        return bstack111ll11l1ll_opy_
    def bstack111ll111lll_opy_(self, test_name, bstack111ll1l1111_opy_):
        if test_name not in self._111ll111ll1_opy_:
            self._111ll111ll1_opy_[test_name] = {}
        bstack111ll11lll1_opy_ = self._111ll111ll1_opy_[test_name]
        bstack111ll11l1ll_opy_ = bstack111ll11lll1_opy_.get(bstack111ll1l1111_opy_, 0)
        bstack111ll11lll1_opy_[bstack111ll1l1111_opy_] = bstack111ll11l1ll_opy_ + 1
    def bstack1l11l11lll_opy_(self, bstack111ll11ll1l_opy_, bstack111ll111l1l_opy_):
        bstack111ll11l1l1_opy_ = self.bstack111ll11l11l_opy_(bstack111ll11ll1l_opy_, bstack111ll111l1l_opy_)
        event_name = bstack11ll1l1llll_opy_[bstack111ll111l1l_opy_]
        bstack1l1ll1l1lll_opy_ = bstack1ll1l1_opy_ (u"ࠥࡿࢂ࠳ࡻࡾ࠯ࡾࢁࠧᳪ").format(bstack111ll11ll1l_opy_, event_name, bstack111ll11l1l1_opy_)
        self._111ll1l111l_opy_.append(bstack1l1ll1l1lll_opy_)
    def bstack1l1l11ll11_opy_(self):
        return len(self._111ll1l111l_opy_) == 0
    def bstack1ll1l11ll1_opy_(self):
        bstack111ll11l111_opy_ = self._111ll1l111l_opy_.popleft()
        return bstack111ll11l111_opy_
    def capturing(self):
        return self._111ll11ll11_opy_
    def bstack111l11ll1_opy_(self):
        self._111ll11ll11_opy_ = True
    def bstack111l1l11_opy_(self):
        self._111ll11ll11_opy_ = False
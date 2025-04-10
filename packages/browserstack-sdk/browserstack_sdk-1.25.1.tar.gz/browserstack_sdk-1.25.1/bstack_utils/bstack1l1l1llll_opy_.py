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
class bstack11ll1l1l_opy_:
    def __init__(self, handler):
        self._111l11l11l1_opy_ = None
        self.handler = handler
        self._111l11l11ll_opy_ = self.bstack111l11l1l11_opy_()
        self.patch()
    def patch(self):
        self._111l11l11l1_opy_ = self._111l11l11ll_opy_.execute
        self._111l11l11ll_opy_.execute = self.bstack111l11l1l1l_opy_()
    def bstack111l11l1l1l_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack1ll1l1_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫ࠢᵳ"), driver_command, None, this, args)
            response = self._111l11l11l1_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack1ll1l1_opy_ (u"ࠣࡣࡩࡸࡪࡸࠢᵴ"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._111l11l11ll_opy_.execute = self._111l11l11l1_opy_
    @staticmethod
    def bstack111l11l1l11_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver
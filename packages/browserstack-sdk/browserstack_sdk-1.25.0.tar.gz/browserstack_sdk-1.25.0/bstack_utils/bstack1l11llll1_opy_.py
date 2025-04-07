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
class bstack1ll111l1l_opy_:
    def __init__(self, handler):
        self._111ll11ll11_opy_ = None
        self.handler = handler
        self._111ll11lll1_opy_ = self.bstack111ll11ll1l_opy_()
        self.patch()
    def patch(self):
        self._111ll11ll11_opy_ = self._111ll11lll1_opy_.execute
        self._111ll11lll1_opy_.execute = self.bstack111ll11l1ll_opy_()
    def bstack111ll11l1ll_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack11l1l11_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨ᳤ࠦ"), driver_command, None, this, args)
            response = self._111ll11ll11_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack11l1l11_opy_ (u"ࠧࡧࡦࡵࡧࡵ᳥ࠦ"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._111ll11lll1_opy_.execute = self._111ll11ll11_opy_
    @staticmethod
    def bstack111ll11ll1l_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver
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
import multiprocessing
import os
import json
from time import sleep
import bstack_utils.accessibility as bstack1l1l1l1ll1_opy_
from browserstack_sdk.bstack11l1lll1ll_opy_ import *
from bstack_utils.config import Config
from bstack_utils.messages import bstack1ll11lllll_opy_
class bstack11ll111l_opy_:
    def __init__(self, args, logger, bstack111l1111l1_opy_, bstack111l11l111_opy_):
        self.args = args
        self.logger = logger
        self.bstack111l1111l1_opy_ = bstack111l1111l1_opy_
        self.bstack111l11l111_opy_ = bstack111l11l111_opy_
        self._prepareconfig = None
        self.Config = None
        self.runner = None
        self.bstack1l11l1l111_opy_ = []
        self.bstack111l111l11_opy_ = None
        self.bstack1l111l1l1l_opy_ = []
        self.bstack111l11111l_opy_ = self.bstack1111l111_opy_()
        self.bstack11l1lllll1_opy_ = -1
    def bstack11llll111l_opy_(self, bstack1111lll1ll_opy_):
        self.parse_args()
        self.bstack111l111lll_opy_()
        self.bstack1111llllll_opy_(bstack1111lll1ll_opy_)
    @staticmethod
    def version():
        import pytest
        return pytest.__version__
    @staticmethod
    def bstack1111lllll1_opy_():
        import importlib
        if getattr(importlib, bstack11l1l11_opy_ (u"ࠧࡧ࡫ࡱࡨࡤࡲ࡯ࡢࡦࡨࡶࠬ࿣"), False):
            bstack1111llll1l_opy_ = importlib.find_loader(bstack11l1l11_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡵࡨࡰࡪࡴࡩࡶ࡯ࠪ࿤"))
        else:
            bstack1111llll1l_opy_ = importlib.util.find_spec(bstack11l1l11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡡࡶࡩࡱ࡫࡮ࡪࡷࡰࠫ࿥"))
    def bstack1111lll1l1_opy_(self, arg):
        if arg in self.args:
            i = self.args.index(arg)
            self.args.pop(i + 1)
            self.args.pop(i)
    def parse_args(self):
        self.bstack11l1lllll1_opy_ = -1
        if self.bstack111l11l111_opy_ and bstack11l1l11_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ࿦") in self.bstack111l1111l1_opy_:
            self.bstack11l1lllll1_opy_ = int(self.bstack111l1111l1_opy_[bstack11l1l11_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫ࿧")])
        try:
            bstack111l111l1l_opy_ = [bstack11l1l11_opy_ (u"ࠬ࠳࠭ࡥࡴ࡬ࡺࡪࡸࠧ࿨"), bstack11l1l11_opy_ (u"࠭࠭࠮ࡲ࡯ࡹ࡬࡯࡮ࡴࠩ࿩"), bstack11l1l11_opy_ (u"ࠧ࠮ࡲࠪ࿪")]
            if self.bstack11l1lllll1_opy_ >= 0:
                bstack111l111l1l_opy_.extend([bstack11l1l11_opy_ (u"ࠨ࠯࠰ࡲࡺࡳࡰࡳࡱࡦࡩࡸࡹࡥࡴࠩ࿫"), bstack11l1l11_opy_ (u"ࠩ࠰ࡲࠬ࿬")])
            for arg in bstack111l111l1l_opy_:
                self.bstack1111lll1l1_opy_(arg)
        except Exception as exc:
            self.logger.error(str(exc))
    def get_args(self):
        return self.args
    def bstack111l111lll_opy_(self):
        bstack111l111l11_opy_ = [os.path.normpath(item) for item in self.args]
        self.bstack111l111l11_opy_ = bstack111l111l11_opy_
        return bstack111l111l11_opy_
    def bstack1ll111l111_opy_(self):
        try:
            from _pytest.config import _prepareconfig
            from _pytest.config import Config
            from _pytest import runner
            self.bstack1111lllll1_opy_()
            self._prepareconfig = _prepareconfig
            self.Config = Config
            self.runner = runner
        except Exception as e:
            self.logger.warn(e, bstack1ll11lllll_opy_)
    def bstack1111llllll_opy_(self, bstack1111lll1ll_opy_):
        bstack111ll1lll_opy_ = Config.bstack111l1l1l_opy_()
        if bstack1111lll1ll_opy_:
            self.bstack111l111l11_opy_.append(bstack11l1l11_opy_ (u"ࠪ࠱࠲ࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ࿭"))
            self.bstack111l111l11_opy_.append(bstack11l1l11_opy_ (u"࡙ࠫࡸࡵࡦࠩ࿮"))
        if bstack111ll1lll_opy_.bstack111l1111ll_opy_():
            self.bstack111l111l11_opy_.append(bstack11l1l11_opy_ (u"ࠬ࠳࠭ࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫ࿯"))
            self.bstack111l111l11_opy_.append(bstack11l1l11_opy_ (u"࠭ࡔࡳࡷࡨࠫ࿰"))
        self.bstack111l111l11_opy_.append(bstack11l1l11_opy_ (u"ࠧ࠮ࡲࠪ࿱"))
        self.bstack111l111l11_opy_.append(bstack11l1l11_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡰ࡭ࡷࡪ࡭ࡳ࠭࿲"))
        self.bstack111l111l11_opy_.append(bstack11l1l11_opy_ (u"ࠩ࠰࠱ࡩࡸࡩࡷࡧࡵࠫ࿳"))
        self.bstack111l111l11_opy_.append(bstack11l1l11_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪ࿴"))
        if self.bstack11l1lllll1_opy_ > 1:
            self.bstack111l111l11_opy_.append(bstack11l1l11_opy_ (u"ࠫ࠲ࡴࠧ࿵"))
            self.bstack111l111l11_opy_.append(str(self.bstack11l1lllll1_opy_))
    def bstack111l11l11l_opy_(self):
        bstack1l111l1l1l_opy_ = []
        for spec in self.bstack1l11l1l111_opy_:
            bstack1l1l11lll1_opy_ = [spec]
            bstack1l1l11lll1_opy_ += self.bstack111l111l11_opy_
            bstack1l111l1l1l_opy_.append(bstack1l1l11lll1_opy_)
        self.bstack1l111l1l1l_opy_ = bstack1l111l1l1l_opy_
        return bstack1l111l1l1l_opy_
    def bstack1111l111_opy_(self):
        try:
            from pytest_bdd import reporting
            self.bstack111l11111l_opy_ = True
            return True
        except Exception as e:
            self.bstack111l11111l_opy_ = False
        return self.bstack111l11111l_opy_
    def bstack1l1ll1l1_opy_(self, bstack111l111111_opy_, bstack11llll111l_opy_):
        bstack11llll111l_opy_[bstack11l1l11_opy_ (u"ࠬࡉࡏࡏࡈࡌࡋࠬ࿶")] = self.bstack111l1111l1_opy_
        multiprocessing.set_start_method(bstack11l1l11_opy_ (u"࠭ࡳࡱࡣࡺࡲࠬ࿷"))
        bstack1ll1ll1lll_opy_ = []
        manager = multiprocessing.Manager()
        bstack111l11l1ll_opy_ = manager.list()
        if bstack11l1l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ࿸") in self.bstack111l1111l1_opy_:
            for index, platform in enumerate(self.bstack111l1111l1_opy_[bstack11l1l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ࿹")]):
                bstack1ll1ll1lll_opy_.append(multiprocessing.Process(name=str(index),
                                                            target=bstack111l111111_opy_,
                                                            args=(self.bstack111l111l11_opy_, bstack11llll111l_opy_, bstack111l11l1ll_opy_)))
            bstack111l11l1l1_opy_ = len(self.bstack111l1111l1_opy_[bstack11l1l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ࿺")])
        else:
            bstack1ll1ll1lll_opy_.append(multiprocessing.Process(name=str(0),
                                                        target=bstack111l111111_opy_,
                                                        args=(self.bstack111l111l11_opy_, bstack11llll111l_opy_, bstack111l11l1ll_opy_)))
            bstack111l11l1l1_opy_ = 1
        i = 0
        for t in bstack1ll1ll1lll_opy_:
            os.environ[bstack11l1l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪ࿻")] = str(i)
            if bstack11l1l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ࿼") in self.bstack111l1111l1_opy_:
                os.environ[bstack11l1l11_opy_ (u"ࠬࡉࡕࡓࡔࡈࡒ࡙ࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡆࡄࡘࡆ࠭࿽")] = json.dumps(self.bstack111l1111l1_opy_[bstack11l1l11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ࿾")][i % bstack111l11l1l1_opy_])
            i += 1
            t.start()
        for t in bstack1ll1ll1lll_opy_:
            t.join()
        return list(bstack111l11l1ll_opy_)
    @staticmethod
    def bstack1lllllll1_opy_(driver, bstack1111llll11_opy_, logger, item=None, wait=False):
        item = item or getattr(threading.current_thread(), bstack11l1l11_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡵࡧࡰࠫ࿿"), None)
        if item and getattr(item, bstack11l1l11_opy_ (u"ࠨࡡࡤ࠵࠶ࡿ࡟ࡵࡧࡶࡸࡤࡩࡡࡴࡧࠪက"), None) and not getattr(item, bstack11l1l11_opy_ (u"ࠩࡢࡥ࠶࠷ࡹࡠࡵࡷࡳࡵࡥࡤࡰࡰࡨࠫခ"), False):
            logger.info(
                bstack11l1l11_opy_ (u"ࠥࡅࡺࡺ࡯࡮ࡣࡷࡩࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥࠡࡧࡻࡩࡨࡻࡴࡪࡱࡱࠤ࡭ࡧࡳࠡࡧࡱࡨࡪࡪ࠮ࠡࡒࡵࡳࡨ࡫ࡳࡴ࡫ࡱ࡫ࠥ࡬࡯ࡳࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡷࡩࡸࡺࡩ࡯ࡩࠣ࡭ࡸࠦࡵ࡯ࡦࡨࡶࡼࡧࡹ࠯ࠤဂ"))
            bstack111l111ll1_opy_ = item.cls.__name__ if not item.cls is None else None
            bstack1l1l1l1ll1_opy_.bstack1ll11111l_opy_(driver, item.name, item.path)
            item._a11y_stop_done = True
            if wait:
                sleep(2)
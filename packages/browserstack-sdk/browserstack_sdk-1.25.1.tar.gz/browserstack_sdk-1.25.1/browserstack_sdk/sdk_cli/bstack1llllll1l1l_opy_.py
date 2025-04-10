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
from typing import Dict, List, Any, Callable, Tuple, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1lllll1l1ll_opy_ import bstack1lll1llll11_opy_
from browserstack_sdk.sdk_cli.bstack111111l1ll_opy_ import (
    bstack11111ll1l1_opy_,
    bstack1111l1l1l1_opy_,
    bstack1llllllllll_opy_,
)
from bstack_utils.helper import  bstack11111l111_opy_
from browserstack_sdk.sdk_cli.bstack1lll1ll11ll_opy_ import bstack1lll1ll1lll_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1lllllll1ll_opy_, bstack1lll1l1l1l1_opy_, bstack1lll1l11l1l_opy_, bstack1llll1l1lll_opy_
from typing import Tuple, Any
import threading
from bstack_utils.bstack1l111l11_opy_ import bstack1llllllll1_opy_
from browserstack_sdk.sdk_cli.bstack1lll11111ll_opy_ import bstack1lll1l1l11l_opy_
from bstack_utils.percy import bstack1l1l11l1l_opy_
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.constants import *
import re
class bstack1ll1llll1l1_opy_(bstack1lll1llll11_opy_):
    def __init__(self, bstack1l1lll11111_opy_: Dict[str, str]):
        super().__init__()
        self.bstack1l1lll11111_opy_ = bstack1l1lll11111_opy_
        self.percy = bstack1l1l11l1l_opy_()
        self.bstack1llll11l11_opy_ = bstack1llllllll1_opy_()
        self.bstack1l1ll1lllll_opy_()
        bstack1lll1ll1lll_opy_.bstack1ll1l11l1l1_opy_((bstack11111ll1l1_opy_.bstack111111l11l_opy_, bstack1111l1l1l1_opy_.PRE), self.bstack1l1ll1l1ll1_opy_)
        TestFramework.bstack1ll1l11l1l1_opy_((bstack1lllllll1ll_opy_.TEST, bstack1lll1l11l1l_opy_.POST), self.bstack1ll1ll1llll_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1lll1111l_opy_(self, instance: bstack1llllllllll_opy_, driver: object):
        bstack1ll111l1ll1_opy_ = TestFramework.bstack11111l1lll_opy_(instance.context)
        for t in bstack1ll111l1ll1_opy_:
            bstack1ll111l1l11_opy_ = TestFramework.bstack11111lllll_opy_(t, bstack1lll1l1l11l_opy_.bstack1l1lll1l1l1_opy_, [])
            if any(instance is d[1] for d in bstack1ll111l1l11_opy_) or instance == driver:
                return t
    def bstack1l1ll1l1ll1_opy_(
        self,
        f: bstack1lll1ll1lll_opy_,
        driver: object,
        exec: Tuple[bstack1llllllllll_opy_, str],
        bstack1111l1l11l_opy_: Tuple[bstack11111ll1l1_opy_, bstack1111l1l1l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if not bstack1lll1ll1lll_opy_.bstack1ll1l1llll1_opy_(method_name):
                return
            platform_index = f.bstack11111lllll_opy_(instance, bstack1lll1ll1lll_opy_.bstack1ll11llll1l_opy_, 0)
            bstack1l1lll1l11l_opy_ = self.bstack1l1lll1111l_opy_(instance, driver)
            bstack1l1ll1l1lll_opy_ = TestFramework.bstack11111lllll_opy_(bstack1l1lll1l11l_opy_, TestFramework.bstack1l1ll1lll1l_opy_, None)
            if not bstack1l1ll1l1lll_opy_:
                self.logger.debug(bstack1ll1l1_opy_ (u"ࠦࡴࡴ࡟ࡱࡴࡨࡣࡪࡾࡥࡤࡷࡷࡩ࠿ࠦࡲࡦࡶࡸࡶࡳ࡯࡮ࡨࠢࡤࡷࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡩࡴࠢࡱࡳࡹࠦࡹࡦࡶࠣࡷࡹࡧࡲࡵࡧࡧࠦሬ"))
                return
            driver_command = f.bstack1ll1l1ll111_opy_(*args)
            for command in bstack1l1lll11ll_opy_:
                if command == driver_command:
                    self.bstack1111llll1_opy_(driver, platform_index)
            bstack11l1ll1111_opy_ = self.percy.bstack11l11111_opy_()
            if driver_command in bstack11111ll1l_opy_[bstack11l1ll1111_opy_]:
                self.bstack1llll11l11_opy_.bstack1l11l11lll_opy_(bstack1l1ll1l1lll_opy_, driver_command)
        except Exception as e:
            self.logger.error(bstack1ll1l1_opy_ (u"ࠧࡵ࡮ࡠࡲࡵࡩࡤ࡫ࡸࡦࡥࡸࡸࡪࡀࠠࡦࡴࡵࡳࡷࠨር"), e)
    def bstack1ll1ll1llll_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1l1l1l1_opy_,
        bstack1111l1l11l_opy_: Tuple[bstack1lllllll1ll_opy_, bstack1lll1l11l1l_opy_],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack1l111l1111_opy_ import bstack1lll111l11l_opy_
        bstack1ll111l1l11_opy_ = f.bstack11111lllll_opy_(instance, bstack1lll1l1l11l_opy_.bstack1l1lll1l1l1_opy_, [])
        if not bstack1ll111l1l11_opy_:
            self.logger.debug(bstack1ll1l1_opy_ (u"ࠨ࡯࡯ࡡࡤࡪࡹ࡫ࡲࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࠣࡨࡷ࡯ࡶࡦࡴࡶࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣሮ") + str(kwargs) + bstack1ll1l1_opy_ (u"ࠢࠣሯ"))
            return
        if len(bstack1ll111l1l11_opy_) > 1:
            self.logger.debug(bstack1ll1l1_opy_ (u"ࠣࡱࡱࡣࡦ࡬ࡴࡦࡴࡢࡸࡪࡹࡴ࠻ࠢࡾࡰࡪࡴࠨࡥࡴ࡬ࡺࡪࡸ࡟ࡪࡰࡶࡸࡦࡴࡣࡦࡵࠬࢁࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥሰ") + str(kwargs) + bstack1ll1l1_opy_ (u"ࠤࠥሱ"))
        bstack1l1ll1l1l1l_opy_, bstack1l1ll1llll1_opy_ = bstack1ll111l1l11_opy_[0]
        driver = bstack1l1ll1l1l1l_opy_()
        if not driver:
            self.logger.debug(bstack1ll1l1_opy_ (u"ࠥࡳࡳࡥࡡࡧࡶࡨࡶࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࠠࡥࡴ࡬ࡺࡪࡸࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦሲ") + str(kwargs) + bstack1ll1l1_opy_ (u"ࠦࠧሳ"))
            return
        bstack1l1ll1ll11l_opy_ = {
            TestFramework.bstack1ll1ll1l1l1_opy_: bstack1ll1l1_opy_ (u"ࠧࡺࡥࡴࡶࠣࡲࡦࡳࡥࠣሴ"),
            TestFramework.bstack1ll1ll1ll11_opy_: bstack1ll1l1_opy_ (u"ࠨࡴࡦࡵࡷࠤࡺࡻࡩࡥࠤስ"),
            TestFramework.bstack1l1ll1lll1l_opy_: bstack1ll1l1_opy_ (u"ࠢࡵࡧࡶࡸࠥࡸࡥࡳࡷࡱࠤࡳࡧ࡭ࡦࠤሶ")
        }
        bstack1l1ll1ll1ll_opy_ = { key: f.bstack11111lllll_opy_(instance, key) for key in bstack1l1ll1ll11l_opy_ }
        bstack1l1ll1ll1l1_opy_ = [key for key, value in bstack1l1ll1ll1ll_opy_.items() if not value]
        if bstack1l1ll1ll1l1_opy_:
            for key in bstack1l1ll1ll1l1_opy_:
                self.logger.debug(bstack1ll1l1_opy_ (u"ࠣࡱࡱࡣࡦ࡬ࡴࡦࡴࡢࡸࡪࡹࡴ࠻ࠢࡰ࡭ࡸࡹࡩ࡯ࡩࠣࠦሷ") + str(key) + bstack1ll1l1_opy_ (u"ࠤࠥሸ"))
            return
        platform_index = f.bstack11111lllll_opy_(instance, bstack1lll1ll1lll_opy_.bstack1ll11llll1l_opy_, 0)
        if self.bstack1l1lll11111_opy_.percy_capture_mode == bstack1ll1l1_opy_ (u"ࠥࡸࡪࡹࡴࡤࡣࡶࡩࠧሹ"):
            bstack11ll1l1ll_opy_ = bstack1l1ll1ll1ll_opy_.get(TestFramework.bstack1l1ll1lll1l_opy_) + bstack1ll1l1_opy_ (u"ࠦ࠲ࡺࡥࡴࡶࡦࡥࡸ࡫ࠢሺ")
            bstack1ll1l1l111l_opy_ = bstack1lll111l11l_opy_.bstack1ll1ll111ll_opy_(EVENTS.bstack1l1ll1ll111_opy_.value)
            PercySDK.screenshot(
                driver,
                bstack11ll1l1ll_opy_,
                bstack11l1ll11l_opy_=bstack1l1ll1ll1ll_opy_[TestFramework.bstack1ll1ll1l1l1_opy_],
                bstack1l1ll11lll_opy_=bstack1l1ll1ll1ll_opy_[TestFramework.bstack1ll1ll1ll11_opy_],
                bstack1ll11111l_opy_=platform_index
            )
            bstack1lll111l11l_opy_.end(EVENTS.bstack1l1ll1ll111_opy_.value, bstack1ll1l1l111l_opy_+bstack1ll1l1_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧሻ"), bstack1ll1l1l111l_opy_+bstack1ll1l1_opy_ (u"ࠨ࠺ࡦࡰࡧࠦሼ"), True, None, None, None, None, test_name=bstack11ll1l1ll_opy_)
    def bstack1111llll1_opy_(self, driver, platform_index):
        if self.bstack1llll11l11_opy_.bstack1l1l11ll11_opy_() is True or self.bstack1llll11l11_opy_.capturing() is True:
            return
        self.bstack1llll11l11_opy_.bstack111l11ll1_opy_()
        while not self.bstack1llll11l11_opy_.bstack1l1l11ll11_opy_():
            bstack1l1ll1l1lll_opy_ = self.bstack1llll11l11_opy_.bstack1ll1l11ll1_opy_()
            self.bstack1l11ll11l1_opy_(driver, bstack1l1ll1l1lll_opy_, platform_index)
        self.bstack1llll11l11_opy_.bstack111l1l11_opy_()
    def bstack1l11ll11l1_opy_(self, driver, bstack1lll11lll1_opy_, platform_index, test=None):
        from bstack_utils.bstack1l111l1111_opy_ import bstack1lll111l11l_opy_
        bstack1ll1l1l111l_opy_ = bstack1lll111l11l_opy_.bstack1ll1ll111ll_opy_(EVENTS.bstack1llll1l11_opy_.value)
        if test != None:
            bstack11l1ll11l_opy_ = getattr(test, bstack1ll1l1_opy_ (u"ࠧ࡯ࡣࡰࡩࠬሽ"), None)
            bstack1l1ll11lll_opy_ = getattr(test, bstack1ll1l1_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ሾ"), None)
            PercySDK.screenshot(driver, bstack1lll11lll1_opy_, bstack11l1ll11l_opy_=bstack11l1ll11l_opy_, bstack1l1ll11lll_opy_=bstack1l1ll11lll_opy_, bstack1ll11111l_opy_=platform_index)
        else:
            PercySDK.screenshot(driver, bstack1lll11lll1_opy_)
        bstack1lll111l11l_opy_.end(EVENTS.bstack1llll1l11_opy_.value, bstack1ll1l1l111l_opy_+bstack1ll1l1_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤሿ"), bstack1ll1l1l111l_opy_+bstack1ll1l1_opy_ (u"ࠥ࠾ࡪࡴࡤࠣቀ"), True, None, None, None, None, test_name=bstack1lll11lll1_opy_)
    def bstack1l1ll1lllll_opy_(self):
        os.environ[bstack1ll1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡊࡘࡃ࡚ࠩቁ")] = str(self.bstack1l1lll11111_opy_.success)
        os.environ[bstack1ll1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡋࡒࡄ࡛ࡢࡇࡆࡖࡔࡖࡔࡈࡣࡒࡕࡄࡆࠩቂ")] = str(self.bstack1l1lll11111_opy_.percy_capture_mode)
        self.percy.bstack1l1ll1lll11_opy_(self.bstack1l1lll11111_opy_.is_percy_auto_enabled)
        self.percy.bstack1l1ll1l1l11_opy_(self.bstack1l1lll11111_opy_.percy_build_id)
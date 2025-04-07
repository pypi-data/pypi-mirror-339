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
from typing import Dict, List, Any, Callable, Tuple, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1lll11llll1_opy_ import bstack1lllll1l111_opy_
from browserstack_sdk.sdk_cli.bstack1111l11lll_opy_ import (
    bstack1111l1ll1l_opy_,
    bstack111111111l_opy_,
    bstack11111l11ll_opy_,
)
from bstack_utils.helper import  bstack1llllllll1_opy_
from browserstack_sdk.sdk_cli.bstack1lllll1ll11_opy_ import bstack1lll1l11ll1_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1llllll1lll_opy_, bstack1lllllll111_opy_, bstack1lll111lll1_opy_, bstack1lll11ll111_opy_
from typing import Tuple, Any
import threading
from bstack_utils.bstack1l11111lll_opy_ import bstack11lll1lll1_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l1llll_opy_ import bstack1lll1lll11l_opy_
from bstack_utils.percy import bstack111l11l1l_opy_
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.constants import *
import re
class bstack1lll1l11l11_opy_(bstack1lllll1l111_opy_):
    def __init__(self, bstack1l1lll111ll_opy_: Dict[str, str]):
        super().__init__()
        self.bstack1l1lll111ll_opy_ = bstack1l1lll111ll_opy_
        self.percy = bstack111l11l1l_opy_()
        self.bstack1l111llll_opy_ = bstack11lll1lll1_opy_()
        self.bstack1l1lll11l11_opy_()
        bstack1lll1l11ll1_opy_.bstack1ll1l11l11l_opy_((bstack1111l1ll1l_opy_.bstack111111l111_opy_, bstack111111111l_opy_.PRE), self.bstack1l1lll1l1l1_opy_)
        TestFramework.bstack1ll1l11l11l_opy_((bstack1llllll1lll_opy_.TEST, bstack1lll111lll1_opy_.POST), self.bstack1ll1lll1l1l_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1ll11l111l1_opy_(self, instance: bstack11111l11ll_opy_, driver: object):
        bstack1ll1111ll11_opy_ = TestFramework.bstack1111l1l1ll_opy_(instance.context)
        for t in bstack1ll1111ll11_opy_:
            bstack1ll1111l11l_opy_ = TestFramework.bstack11111l1l1l_opy_(t, bstack1lll1lll11l_opy_.bstack1ll111lll11_opy_, [])
            if any(instance is d[1] for d in bstack1ll1111l11l_opy_) or instance == driver:
                return t
    def bstack1l1lll1l1l1_opy_(
        self,
        f: bstack1lll1l11ll1_opy_,
        driver: object,
        exec: Tuple[bstack11111l11ll_opy_, str],
        bstack1111l1ll11_opy_: Tuple[bstack1111l1ll1l_opy_, bstack111111111l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if not bstack1lll1l11ll1_opy_.bstack1ll1ll11l1l_opy_(method_name):
                return
            platform_index = f.bstack11111l1l1l_opy_(instance, bstack1lll1l11ll1_opy_.bstack1ll1l11llll_opy_, 0)
            bstack1ll11l11l1l_opy_ = self.bstack1ll11l111l1_opy_(instance, driver)
            bstack1l1lll1l11l_opy_ = TestFramework.bstack11111l1l1l_opy_(bstack1ll11l11l1l_opy_, TestFramework.bstack1l1lll11lll_opy_, None)
            if not bstack1l1lll1l11l_opy_:
                self.logger.debug(bstack11l1l11_opy_ (u"ࠢࡰࡰࡢࡴࡷ࡫࡟ࡦࡺࡨࡧࡺࡺࡥ࠻ࠢࡵࡩࡹࡻࡲ࡯࡫ࡱ࡫ࠥࡧࡳࠡࡵࡨࡷࡸ࡯࡯࡯ࠢ࡬ࡷࠥࡴ࡯ࡵࠢࡼࡩࡹࠦࡳࡵࡣࡵࡸࡪࡪࠢሓ"))
                return
            driver_command = f.bstack1ll1ll1l111_opy_(*args)
            for command in bstack11ll111l1l_opy_:
                if command == driver_command:
                    self.bstack1111111l_opy_(driver, platform_index)
            bstack11llll1lll_opy_ = self.percy.bstack11lllll1_opy_()
            if driver_command in bstack1lllll111l_opy_[bstack11llll1lll_opy_]:
                self.bstack1l111llll_opy_.bstack11ll111l11_opy_(bstack1l1lll1l11l_opy_, driver_command)
        except Exception as e:
            self.logger.error(bstack11l1l11_opy_ (u"ࠣࡱࡱࡣࡵࡸࡥࡠࡧࡻࡩࡨࡻࡴࡦ࠼ࠣࡩࡷࡸ࡯ࡳࠤሔ"), e)
    def bstack1ll1lll1l1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1lllllll111_opy_,
        bstack1111l1ll11_opy_: Tuple[bstack1llllll1lll_opy_, bstack1lll111lll1_opy_],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack1l1ll1l11l_opy_ import bstack1lll1llll1l_opy_
        bstack1ll1111l11l_opy_ = f.bstack11111l1l1l_opy_(instance, bstack1lll1lll11l_opy_.bstack1ll111lll11_opy_, [])
        if not bstack1ll1111l11l_opy_:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠤࡲࡲࡤࡧࡦࡵࡧࡵࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࠦࡤࡳ࡫ࡹࡩࡷࡹࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦሕ") + str(kwargs) + bstack11l1l11_opy_ (u"ࠥࠦሖ"))
            return
        if len(bstack1ll1111l11l_opy_) > 1:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠦࡴࡴ࡟ࡢࡨࡷࡩࡷࡥࡴࡦࡵࡷ࠾ࠥࢁ࡬ࡦࡰࠫࡨࡷ࡯ࡶࡦࡴࡢ࡭ࡳࡹࡴࡢࡰࡦࡩࡸ࠯ࡽࠡࡦࡵ࡭ࡻ࡫ࡲࡴࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨሗ") + str(kwargs) + bstack11l1l11_opy_ (u"ࠧࠨመ"))
        bstack1l1lll1l1ll_opy_, bstack1l1lll11l1l_opy_ = bstack1ll1111l11l_opy_[0]
        driver = bstack1l1lll1l1ll_opy_()
        if not driver:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠨ࡯࡯ࡡࡤࡪࡹ࡫ࡲࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࠣࡨࡷ࡯ࡶࡦࡴࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢሙ") + str(kwargs) + bstack11l1l11_opy_ (u"ࠢࠣሚ"))
            return
        bstack1l1lll1l111_opy_ = {
            TestFramework.bstack1ll1l11l111_opy_: bstack11l1l11_opy_ (u"ࠣࡶࡨࡷࡹࠦ࡮ࡢ࡯ࡨࠦማ"),
            TestFramework.bstack1ll1lll11l1_opy_: bstack11l1l11_opy_ (u"ࠤࡷࡩࡸࡺࠠࡶࡷ࡬ࡨࠧሜ"),
            TestFramework.bstack1l1lll11lll_opy_: bstack11l1l11_opy_ (u"ࠥࡸࡪࡹࡴࠡࡴࡨࡶࡺࡴࠠ࡯ࡣࡰࡩࠧም")
        }
        bstack1l1lll11ll1_opy_ = { key: f.bstack11111l1l1l_opy_(instance, key) for key in bstack1l1lll1l111_opy_ }
        bstack1l1lll1ll1l_opy_ = [key for key, value in bstack1l1lll11ll1_opy_.items() if not value]
        if bstack1l1lll1ll1l_opy_:
            for key in bstack1l1lll1ll1l_opy_:
                self.logger.debug(bstack11l1l11_opy_ (u"ࠦࡴࡴ࡟ࡢࡨࡷࡩࡷࡥࡴࡦࡵࡷ࠾ࠥࡳࡩࡴࡵ࡬ࡲ࡬ࠦࠢሞ") + str(key) + bstack11l1l11_opy_ (u"ࠧࠨሟ"))
            return
        platform_index = f.bstack11111l1l1l_opy_(instance, bstack1lll1l11ll1_opy_.bstack1ll1l11llll_opy_, 0)
        if self.bstack1l1lll111ll_opy_.percy_capture_mode == bstack11l1l11_opy_ (u"ࠨࡴࡦࡵࡷࡧࡦࡹࡥࠣሠ"):
            bstack1l1l1llll1_opy_ = bstack1l1lll11ll1_opy_.get(TestFramework.bstack1l1lll11lll_opy_) + bstack11l1l11_opy_ (u"ࠢ࠮ࡶࡨࡷࡹࡩࡡࡴࡧࠥሡ")
            bstack1ll1ll1l1l1_opy_ = bstack1lll1llll1l_opy_.bstack1ll1ll1lll1_opy_(EVENTS.bstack1l1lll1llll_opy_.value)
            PercySDK.screenshot(
                driver,
                bstack1l1l1llll1_opy_,
                bstack1ll11l111l_opy_=bstack1l1lll11ll1_opy_[TestFramework.bstack1ll1l11l111_opy_],
                bstack1ll111l1ll_opy_=bstack1l1lll11ll1_opy_[TestFramework.bstack1ll1lll11l1_opy_],
                bstack11l11111l_opy_=platform_index
            )
            bstack1lll1llll1l_opy_.end(EVENTS.bstack1l1lll1llll_opy_.value, bstack1ll1ll1l1l1_opy_+bstack11l1l11_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣሢ"), bstack1ll1ll1l1l1_opy_+bstack11l1l11_opy_ (u"ࠤ࠽ࡩࡳࡪࠢሣ"), True, None, None, None, None, test_name=bstack1l1l1llll1_opy_)
    def bstack1111111l_opy_(self, driver, platform_index):
        if self.bstack1l111llll_opy_.bstack1l111l1111_opy_() is True or self.bstack1l111llll_opy_.capturing() is True:
            return
        self.bstack1l111llll_opy_.bstack11llllll1l_opy_()
        while not self.bstack1l111llll_opy_.bstack1l111l1111_opy_():
            bstack1l1lll1l11l_opy_ = self.bstack1l111llll_opy_.bstack11lll1111l_opy_()
            self.bstack1lllll1lll_opy_(driver, bstack1l1lll1l11l_opy_, platform_index)
        self.bstack1l111llll_opy_.bstack11l1llll1_opy_()
    def bstack1lllll1lll_opy_(self, driver, bstack11l11ll1l1_opy_, platform_index, test=None):
        from bstack_utils.bstack1l1ll1l11l_opy_ import bstack1lll1llll1l_opy_
        bstack1ll1ll1l1l1_opy_ = bstack1lll1llll1l_opy_.bstack1ll1ll1lll1_opy_(EVENTS.bstack1ll1l1ll1l_opy_.value)
        if test != None:
            bstack1ll11l111l_opy_ = getattr(test, bstack11l1l11_opy_ (u"ࠪࡲࡦࡳࡥࠨሤ"), None)
            bstack1ll111l1ll_opy_ = getattr(test, bstack11l1l11_opy_ (u"ࠫࡺࡻࡩࡥࠩሥ"), None)
            PercySDK.screenshot(driver, bstack11l11ll1l1_opy_, bstack1ll11l111l_opy_=bstack1ll11l111l_opy_, bstack1ll111l1ll_opy_=bstack1ll111l1ll_opy_, bstack11l11111l_opy_=platform_index)
        else:
            PercySDK.screenshot(driver, bstack11l11ll1l1_opy_)
        bstack1lll1llll1l_opy_.end(EVENTS.bstack1ll1l1ll1l_opy_.value, bstack1ll1ll1l1l1_opy_+bstack11l1l11_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧሦ"), bstack1ll1ll1l1l1_opy_+bstack11l1l11_opy_ (u"ࠨ࠺ࡦࡰࡧࠦሧ"), True, None, None, None, None, test_name=bstack11l11ll1l1_opy_)
    def bstack1l1lll11l11_opy_(self):
        os.environ[bstack11l1l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡆࡔࡆ࡝ࠬረ")] = str(self.bstack1l1lll111ll_opy_.success)
        os.environ[bstack11l1l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡇࡕࡇ࡞ࡥࡃࡂࡒࡗ࡙ࡗࡋ࡟ࡎࡑࡇࡉࠬሩ")] = str(self.bstack1l1lll111ll_opy_.percy_capture_mode)
        self.percy.bstack1l1lll1lll1_opy_(self.bstack1l1lll111ll_opy_.is_percy_auto_enabled)
        self.percy.bstack1l1lll1ll11_opy_(self.bstack1l1lll111ll_opy_.percy_build_id)
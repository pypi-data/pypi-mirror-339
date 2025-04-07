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
import json
import time
import os
import threading
import asyncio
from browserstack_sdk.sdk_cli.bstack1111l11lll_opy_ import (
    bstack1111l1ll1l_opy_,
    bstack111111111l_opy_,
    bstack11111l11ll_opy_,
    bstack11111l1111_opy_,
)
from typing import Tuple, Dict, Any, List, Union
from bstack_utils.helper import bstack1ll1111l1ll_opy_, bstack1lll1ll11l_opy_
from browserstack_sdk.sdk_cli.bstack1lllll1ll11_opy_ import bstack1lll1l11ll1_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1llllll1lll_opy_, bstack1lll111lll1_opy_, bstack1lllllll111_opy_
from browserstack_sdk.sdk_cli.bstack1llll1111l1_opy_ import bstack1llllll11ll_opy_
from browserstack_sdk.sdk_cli.bstack1ll11ll111l_opy_ import bstack1ll11l1llll_opy_
from typing import Tuple, List, Any
from bstack_utils.bstack11lll1l1_opy_ import bstack11ll11111_opy_, bstack1l1l1l11l1_opy_, bstack1llll1lll1_opy_
from browserstack_sdk import sdk_pb2 as structs
class bstack1lllll1llll_opy_(bstack1ll11l1llll_opy_):
    bstack1l1ll11lll1_opy_ = bstack11l1l11_opy_ (u"ࠧࡺࡥࡴࡶࡢࡨࡷ࡯ࡶࡦࡴࡶࠦ቉")
    bstack1ll111lll11_opy_ = bstack11l1l11_opy_ (u"ࠨࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡷࡪࡹࡳࡪࡱࡱࡷࠧቊ")
    bstack1l1ll111111_opy_ = bstack11l1l11_opy_ (u"ࠢ࡯ࡱࡱࡣࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡴࠤቋ")
    bstack1l1ll11llll_opy_ = bstack11l1l11_opy_ (u"ࠣࡶࡨࡷࡹࡥࡳࡦࡵࡶ࡭ࡴࡴࡳࠣቌ")
    bstack1l1ll11ll1l_opy_ = bstack11l1l11_opy_ (u"ࠤࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡩ࡯ࡵࡷࡥࡳࡩࡥࡠࡴࡨࡪࡸࠨቍ")
    bstack1ll11111l1l_opy_ = bstack11l1l11_opy_ (u"ࠥࡧࡧࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡥࡵࡩࡦࡺࡥࡥࠤ቎")
    bstack1l1ll11l11l_opy_ = bstack11l1l11_opy_ (u"ࠦࡨࡨࡴࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡱࡥࡲ࡫ࠢ቏")
    bstack1l1ll111l1l_opy_ = bstack11l1l11_opy_ (u"ࠧࡩࡢࡵࡡࡶࡩࡸࡹࡩࡰࡰࡢࡷࡹࡧࡴࡶࡵࠥቐ")
    def __init__(self):
        super().__init__(bstack1ll11ll11l1_opy_=self.bstack1l1ll11lll1_opy_, frameworks=[bstack1lll1l11ll1_opy_.NAME])
        if not self.is_enabled():
            return
        TestFramework.bstack1ll1l11l11l_opy_((bstack1llllll1lll_opy_.BEFORE_EACH, bstack1lll111lll1_opy_.POST), self.bstack1l1ll111l11_opy_)
        if bstack1lll1ll11l_opy_():
            TestFramework.bstack1ll1l11l11l_opy_((bstack1llllll1lll_opy_.TEST, bstack1lll111lll1_opy_.POST), self.bstack1ll1l1ll11l_opy_)
        else:
            TestFramework.bstack1ll1l11l11l_opy_((bstack1llllll1lll_opy_.TEST, bstack1lll111lll1_opy_.PRE), self.bstack1ll1l1ll11l_opy_)
        TestFramework.bstack1ll1l11l11l_opy_((bstack1llllll1lll_opy_.TEST, bstack1lll111lll1_opy_.POST), self.bstack1ll1lll1l1l_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1ll111l11_opy_(
        self,
        f: TestFramework,
        instance: bstack1lllllll111_opy_,
        bstack1111l1ll11_opy_: Tuple[bstack1llllll1lll_opy_, bstack1lll111lll1_opy_],
        *args,
        **kwargs,
    ):
        bstack1l1ll11l1ll_opy_ = self.bstack1l1ll111ll1_opy_(instance.context)
        if not bstack1l1ll11l1ll_opy_:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠨࡳࡦࡶࡢࡥࡨࡺࡩࡷࡧࡢࡴࡦ࡭ࡥ࠻ࠢࡱࡳࠥࡶࡡࡨࡧࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࠦቑ") + str(bstack1111l1ll11_opy_) + bstack11l1l11_opy_ (u"ࠢࠣቒ"))
            return
        f.bstack1111111l1l_opy_(instance, bstack1lllll1llll_opy_.bstack1ll111lll11_opy_, bstack1l1ll11l1ll_opy_)
    def bstack1l1ll111ll1_opy_(self, context: bstack11111l1111_opy_, bstack1l1ll111lll_opy_= True):
        if bstack1l1ll111lll_opy_:
            bstack1l1ll11l1ll_opy_ = self.bstack1ll11ll11ll_opy_(context, reverse=True)
        else:
            bstack1l1ll11l1ll_opy_ = self.bstack1ll11l1ll11_opy_(context, reverse=True)
        return [f for f in bstack1l1ll11l1ll_opy_ if f[1].state != bstack1111l1ll1l_opy_.QUIT]
    def bstack1ll1l1ll11l_opy_(
        self,
        f: TestFramework,
        instance: bstack1lllllll111_opy_,
        bstack1111l1ll11_opy_: Tuple[bstack1llllll1lll_opy_, bstack1lll111lll1_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1ll111l11_opy_(f, instance, bstack1111l1ll11_opy_, *args, **kwargs)
        if not bstack1ll1111l1ll_opy_:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࡺࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦቓ") + str(kwargs) + bstack11l1l11_opy_ (u"ࠤࠥቔ"))
            return
        bstack1l1ll11l1ll_opy_ = f.bstack11111l1l1l_opy_(instance, bstack1lllll1llll_opy_.bstack1ll111lll11_opy_, [])
        if not bstack1l1ll11l1ll_opy_:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࡴ࡯ࠡࡦࡵ࡭ࡻ࡫ࡲࡴࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨቕ") + str(kwargs) + bstack11l1l11_opy_ (u"ࠦࠧቖ"))
            return
        if len(bstack1l1ll11l1ll_opy_) > 1:
            self.logger.debug(
                bstack1lll1l111l1_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠࡼ࡮ࡨࡲ࠭ࡶࡡࡨࡧࡢ࡭ࡳࡹࡴࡢࡰࡦࡩࡸ࠯ࡽࠡࡦࡵ࡭ࡻ࡫ࡲࡴࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࢁ࡫ࡸࡣࡵ࡫ࡸࢃࠢ቗"))
        bstack1l1l1llllll_opy_, bstack1l1lll11l1l_opy_ = bstack1l1ll11l1ll_opy_[0]
        page = bstack1l1l1llllll_opy_()
        if not page:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࠤࡵࡧࡧࡦࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨቘ") + str(kwargs) + bstack11l1l11_opy_ (u"ࠢࠣ቙"))
            return
        bstack11ll11ll11_opy_ = getattr(args[0], bstack11l1l11_opy_ (u"ࠣࡰࡲࡨࡪ࡯ࡤࠣቚ"), None)
        try:
            page.evaluate(bstack11l1l11_opy_ (u"ࠤࡢࠤࡂࡄࠠࡼࡿࠥቛ"),
                        bstack11l1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢ࡯ࡣࡰࡩࠧࡀࠧቜ") + json.dumps(
                            bstack11ll11ll11_opy_) + bstack11l1l11_opy_ (u"ࠦࢂࢃࠢቝ"))
        except Exception as e:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠧ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫ࠠࡼࡿࠥ቞"), e)
    def bstack1ll1lll1l1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1lllllll111_opy_,
        bstack1111l1ll11_opy_: Tuple[bstack1llllll1lll_opy_, bstack1lll111lll1_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1ll111l11_opy_(f, instance, bstack1111l1ll11_opy_, *args, **kwargs)
        if not bstack1ll1111l1ll_opy_:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࡸࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤ቟") + str(kwargs) + bstack11l1l11_opy_ (u"ࠢࠣበ"))
            return
        bstack1l1ll11l1ll_opy_ = f.bstack11111l1l1l_opy_(instance, bstack1lllll1llll_opy_.bstack1ll111lll11_opy_, [])
        if not bstack1l1ll11l1ll_opy_:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࠦࡤࡳ࡫ࡹࡩࡷࡹࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦቡ") + str(kwargs) + bstack11l1l11_opy_ (u"ࠤࠥቢ"))
            return
        if len(bstack1l1ll11l1ll_opy_) > 1:
            self.logger.debug(
                bstack1lll1l111l1_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࢁ࡬ࡦࡰࠫࡴࡦ࡭ࡥࡠ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡶ࠭ࢂࠦࡤࡳ࡫ࡹࡩࡷࡹࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࡿࡰࡽࡡࡳࡩࡶࢁࠧባ"))
        bstack1l1l1llllll_opy_, bstack1l1lll11l1l_opy_ = bstack1l1ll11l1ll_opy_[0]
        page = bstack1l1l1llllll_opy_()
        if not page:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࠢࡳࡥ࡬࡫ࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦቤ") + str(kwargs) + bstack11l1l11_opy_ (u"ࠧࠨብ"))
            return
        status = f.bstack11111l1l1l_opy_(instance, TestFramework.bstack1l1ll1111ll_opy_, None)
        if not status:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠨ࡮ࡰࠢࡶࡸࡦࡺࡵࡴࠢࡩࡳࡷࠦࡴࡦࡵࡷ࠰ࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࠤቦ") + str(bstack1111l1ll11_opy_) + bstack11l1l11_opy_ (u"ࠢࠣቧ"))
            return
        bstack1l1ll1111l1_opy_ = {bstack11l1l11_opy_ (u"ࠣࡵࡷࡥࡹࡻࡳࠣቨ"): status.lower()}
        bstack1l1ll11l1l1_opy_ = f.bstack11111l1l1l_opy_(instance, TestFramework.bstack1l1l1lllll1_opy_, None)
        if status.lower() == bstack11l1l11_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩቩ") and bstack1l1ll11l1l1_opy_ is not None:
            bstack1l1ll1111l1_opy_[bstack11l1l11_opy_ (u"ࠪࡶࡪࡧࡳࡰࡰࠪቪ")] = bstack1l1ll11l1l1_opy_[0][bstack11l1l11_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧቫ")][0] if isinstance(bstack1l1ll11l1l1_opy_, list) else str(bstack1l1ll11l1l1_opy_)
        try:
              page.evaluate(
                    bstack11l1l11_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨቬ"),
                    bstack11l1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࠫቭ")
                    + json.dumps(bstack1l1ll1111l1_opy_)
                    + bstack11l1l11_opy_ (u"ࠢࡾࠤቮ")
                )
        except Exception as e:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠣࡧࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡹࡴࡢࡶࡸࡷࠥࢁࡽࠣቯ"), e)
    def bstack1ll111ll11l_opy_(
        self,
        instance: bstack1lllllll111_opy_,
        f: TestFramework,
        bstack1111l1ll11_opy_: Tuple[bstack1llllll1lll_opy_, bstack1lll111lll1_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1ll111l11_opy_(f, instance, bstack1111l1ll11_opy_, *args, **kwargs)
        if not bstack1ll1111l1ll_opy_:
            self.logger.debug(
                bstack1lll1l111l1_opy_ (u"ࠤࡰࡥࡷࡱ࡟ࡰ࠳࠴ࡽࡤࡹࡹ࡯ࡥ࠽ࠤࡳࡵࡴࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮࠭ࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࡽ࡮ࡻࡦࡸࡧࡴࡿࠥተ"))
            return
        bstack1l1ll11l1ll_opy_ = f.bstack11111l1l1l_opy_(instance, bstack1lllll1llll_opy_.bstack1ll111lll11_opy_, [])
        if not bstack1l1ll11l1ll_opy_:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࡴ࡯ࠡࡦࡵ࡭ࡻ࡫ࡲࡴࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨቱ") + str(kwargs) + bstack11l1l11_opy_ (u"ࠦࠧቲ"))
            return
        if len(bstack1l1ll11l1ll_opy_) > 1:
            self.logger.debug(
                bstack1lll1l111l1_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠࡼ࡮ࡨࡲ࠭ࡶࡡࡨࡧࡢ࡭ࡳࡹࡴࡢࡰࡦࡩࡸ࠯ࡽࠡࡦࡵ࡭ࡻ࡫ࡲࡴࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࢁ࡫ࡸࡣࡵ࡫ࡸࢃࠢታ"))
        bstack1l1l1llllll_opy_, bstack1l1lll11l1l_opy_ = bstack1l1ll11l1ll_opy_[0]
        page = bstack1l1l1llllll_opy_()
        if not page:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠨ࡭ࡢࡴ࡮ࡣࡴ࠷࠱ࡺࡡࡶࡽࡳࡩ࠺ࠡࡰࡲࠤࡵࡧࡧࡦࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨቴ") + str(kwargs) + bstack11l1l11_opy_ (u"ࠢࠣት"))
            return
        timestamp = int(time.time() * 1000)
        data = bstack11l1l11_opy_ (u"ࠣࡑࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࡔࡻࡱࡧ࠿ࠨቶ") + str(timestamp)
        try:
            page.evaluate(
                bstack11l1l11_opy_ (u"ࠤࡢࠤࡂࡄࠠࡼࡿࠥቷ"),
                bstack11l1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡽࠨቸ").format(
                    json.dumps(
                        {
                            bstack11l1l11_opy_ (u"ࠦࡦࡩࡴࡪࡱࡱࠦቹ"): bstack11l1l11_opy_ (u"ࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢቺ"),
                            bstack11l1l11_opy_ (u"ࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤቻ"): {
                                bstack11l1l11_opy_ (u"ࠢࡵࡻࡳࡩࠧቼ"): bstack11l1l11_opy_ (u"ࠣࡃࡱࡲࡴࡺࡡࡵ࡫ࡲࡲࠧች"),
                                bstack11l1l11_opy_ (u"ࠤࡧࡥࡹࡧࠢቾ"): data,
                                bstack11l1l11_opy_ (u"ࠥࡰࡪࡼࡥ࡭ࠤቿ"): bstack11l1l11_opy_ (u"ࠦࡩ࡫ࡢࡶࡩࠥኀ")
                            }
                        }
                    )
                )
            )
        except Exception as e:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠧ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡱ࠴࠵ࡾࠦࡡ࡯ࡰࡲࡸࡦࡺࡩࡰࡰࠣࡱࡦࡸ࡫ࡪࡰࡪࠤࢀࢃࠢኁ"), e)
    def bstack1l1lllll11l_opy_(
        self,
        instance: bstack1lllllll111_opy_,
        f: TestFramework,
        bstack1111l1ll11_opy_: Tuple[bstack1llllll1lll_opy_, bstack1lll111lll1_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1ll111l11_opy_(f, instance, bstack1111l1ll11_opy_, *args, **kwargs)
        if f.bstack11111l1l1l_opy_(instance, bstack1lllll1llll_opy_.bstack1ll11111l1l_opy_, False):
            return
        self.bstack1ll1l1111l1_opy_()
        req = structs.TestSessionEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack11111l1l1l_opy_(instance, TestFramework.bstack1ll1l11llll_opy_)
        req.test_framework_name = TestFramework.bstack11111l1l1l_opy_(instance, TestFramework.bstack1ll1l1llll1_opy_)
        req.test_framework_version = TestFramework.bstack11111l1l1l_opy_(instance, TestFramework.bstack1ll11111l11_opy_)
        req.test_framework_state = bstack1111l1ll11_opy_[0].name
        req.test_hook_state = bstack1111l1ll11_opy_[1].name
        req.test_uuid = TestFramework.bstack11111l1l1l_opy_(instance, TestFramework.bstack1ll1lll11l1_opy_)
        for bstack1l1ll11111l_opy_ in bstack1llllll11ll_opy_.bstack1111111111_opy_.values():
            session = req.automation_sessions.add()
            session.provider = (
                bstack11l1l11_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠧኂ")
                if bstack1ll1111l1ll_opy_
                else bstack11l1l11_opy_ (u"ࠢࡶࡰ࡮ࡲࡴࡽ࡮ࡠࡩࡵ࡭ࡩࠨኃ")
            )
            session.ref = bstack1l1ll11111l_opy_.ref()
            session.hub_url = bstack1llllll11ll_opy_.bstack11111l1l1l_opy_(bstack1l1ll11111l_opy_, bstack1llllll11ll_opy_.bstack1l1ll1llll1_opy_, bstack11l1l11_opy_ (u"ࠣࠤኄ"))
            session.framework_name = bstack1l1ll11111l_opy_.framework_name
            session.framework_version = bstack1l1ll11111l_opy_.framework_version
            session.framework_session_id = bstack1llllll11ll_opy_.bstack11111l1l1l_opy_(bstack1l1ll11111l_opy_, bstack1llllll11ll_opy_.bstack1l1lll1111l_opy_, bstack11l1l11_opy_ (u"ࠤࠥኅ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        return req
    def bstack1ll1ll1ll11_opy_(
        self,
        f: TestFramework,
        instance: bstack1lllllll111_opy_,
        bstack1111l1ll11_opy_: Tuple[bstack1llllll1lll_opy_, bstack1lll111lll1_opy_],
        *args,
        **kwargs
    ):
        bstack1l1ll11l1ll_opy_ = f.bstack11111l1l1l_opy_(instance, bstack1lllll1llll_opy_.bstack1ll111lll11_opy_, [])
        if not bstack1l1ll11l1ll_opy_:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡩࡸࡩࡷࡧࡵ࠾ࠥࡴ࡯ࠡࡲࡤ࡫ࡪࡹࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦኆ") + str(kwargs) + bstack11l1l11_opy_ (u"ࠦࠧኇ"))
            return
        if len(bstack1l1ll11l1ll_opy_) > 1:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠧ࡭ࡥࡵࡡࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡤࡳ࡫ࡹࡩࡷࡀࠠࡼ࡮ࡨࡲ࠭ࡶࡡࡨࡧࡢ࡭ࡳࡹࡴࡢࡰࡦࡩࡸ࠯ࡽࠡࡦࡵ࡭ࡻ࡫ࡲࡴࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨኈ") + str(kwargs) + bstack11l1l11_opy_ (u"ࠨࠢ኉"))
        bstack1l1l1llllll_opy_, bstack1l1lll11l1l_opy_ = bstack1l1ll11l1ll_opy_[0]
        page = bstack1l1l1llllll_opy_()
        if not page:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠢࡨࡧࡷࡣࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡦࡵ࡭ࡻ࡫ࡲ࠻ࠢࡱࡳࠥࡶࡡࡨࡧࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢኊ") + str(kwargs) + bstack11l1l11_opy_ (u"ࠣࠤኋ"))
            return
        return page
    def bstack1ll1l1ll1ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1lllllll111_opy_,
        bstack1111l1ll11_opy_: Tuple[bstack1llllll1lll_opy_, bstack1lll111lll1_opy_],
        *args,
        **kwargs
    ):
        caps = {}
        bstack1l1ll11ll11_opy_ = {}
        for bstack1l1ll11111l_opy_ in bstack1llllll11ll_opy_.bstack1111111111_opy_.values():
            caps = bstack1llllll11ll_opy_.bstack11111l1l1l_opy_(bstack1l1ll11111l_opy_, bstack1llllll11ll_opy_.bstack1l1ll1l1lll_opy_, bstack11l1l11_opy_ (u"ࠤࠥኌ"))
        bstack1l1ll11ll11_opy_[bstack11l1l11_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠣኍ")] = caps.get(bstack11l1l11_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࠧ኎"), bstack11l1l11_opy_ (u"ࠧࠨ኏"))
        bstack1l1ll11ll11_opy_[bstack11l1l11_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩࠧነ")] = caps.get(bstack11l1l11_opy_ (u"ࠢࡰࡵࠥኑ"), bstack11l1l11_opy_ (u"ࠣࠤኒ"))
        bstack1l1ll11ll11_opy_[bstack11l1l11_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠦና")] = caps.get(bstack11l1l11_opy_ (u"ࠥࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴࠢኔ"), bstack11l1l11_opy_ (u"ࠦࠧን"))
        bstack1l1ll11ll11_opy_[bstack11l1l11_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳࠨኖ")] = caps.get(bstack11l1l11_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠣኗ"), bstack11l1l11_opy_ (u"ࠢࠣኘ"))
        return bstack1l1ll11ll11_opy_
    def bstack1ll1l1l1l1l_opy_(self, page: object, bstack1ll1ll1111l_opy_, args={}):
        try:
            bstack1l1ll11l111_opy_ = bstack11l1l11_opy_ (u"ࠣࠤࠥࠬ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠦࠨ࠯࠰࠱ࡦࡸࡺࡡࡤ࡭ࡖࡨࡰࡇࡲࡨࡵࠬࠤࢀࢁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡵࡩࡹࡻࡲ࡯ࠢࡱࡩࡼࠦࡐࡳࡱࡰ࡭ࡸ࡫ࠨࠩࡴࡨࡷࡴࡲࡶࡦ࠮ࠣࡶࡪࡰࡥࡤࡶࠬࠤࡂࡄࠠࡼࡽࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡥࡷࡹࡧࡣ࡬ࡕࡧ࡯ࡆࡸࡧࡴ࠰ࡳࡹࡸ࡮ࠨࡳࡧࡶࡳࡱࡼࡥࠪ࠽ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡾࡪࡳࡥࡢࡰࡦࡼࢁࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡾࡿࠬ࠿ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࢁࢂ࠯ࠨࡼࡣࡵ࡫ࡤࡰࡳࡰࡰࢀ࠭ࠧࠨࠢኙ")
            bstack1ll1ll1111l_opy_ = bstack1ll1ll1111l_opy_.replace(bstack11l1l11_opy_ (u"ࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧኚ"), bstack11l1l11_opy_ (u"ࠥࡦࡸࡺࡡࡤ࡭ࡖࡨࡰࡇࡲࡨࡵࠥኛ"))
            script = bstack1l1ll11l111_opy_.format(fn_body=bstack1ll1ll1111l_opy_, arg_json=json.dumps(args))
            return page.evaluate(script)
        except Exception as e:
            self.logger.error(bstack11l1l11_opy_ (u"ࠦࡦ࠷࠱ࡺࡡࡶࡧࡷ࡯ࡰࡵࡡࡨࡼࡪࡩࡵࡵࡧ࠽ࠤࡊࡸࡲࡰࡴࠣࡩࡽ࡫ࡣࡶࡶ࡬ࡲ࡬ࠦࡴࡩࡧࠣࡥ࠶࠷ࡹࠡࡵࡦࡶ࡮ࡶࡴ࠭ࠢࠥኜ") + str(e) + bstack11l1l11_opy_ (u"ࠧࠨኝ"))
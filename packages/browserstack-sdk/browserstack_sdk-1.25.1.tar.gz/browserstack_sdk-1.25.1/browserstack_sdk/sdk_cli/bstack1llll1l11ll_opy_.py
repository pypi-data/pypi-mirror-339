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
import json
import time
import os
import threading
import asyncio
from browserstack_sdk.sdk_cli.bstack111111l1ll_opy_ import (
    bstack11111ll1l1_opy_,
    bstack1111l1l1l1_opy_,
    bstack1llllllllll_opy_,
    bstack111111l1l1_opy_,
)
from typing import Tuple, Dict, Any, List, Union
from bstack_utils.helper import bstack1l1llll11ll_opy_, bstack111111111_opy_
from browserstack_sdk.sdk_cli.bstack1lll1ll11ll_opy_ import bstack1lll1ll1lll_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1lllllll1ll_opy_, bstack1lll1l11l1l_opy_, bstack1lll1l1l1l1_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l1l111_opy_ import bstack1llll1l1111_opy_
from browserstack_sdk.sdk_cli.bstack1ll11l1l1ll_opy_ import bstack1ll11l1lll1_opy_
from typing import Tuple, List, Any
from bstack_utils.bstack1l1lllll_opy_ import bstack11ll1ll111_opy_, bstack111l1l1l_opy_, bstack11lllll11l_opy_
from browserstack_sdk import sdk_pb2 as structs
class bstack1llll1l1l11_opy_(bstack1ll11l1lll1_opy_):
    bstack1l1l1ll1l1l_opy_ = bstack1ll1l1_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡥࡴ࡬ࡺࡪࡸࡳࠣቢ")
    bstack1l1lll1l1l1_opy_ = bstack1ll1l1_opy_ (u"ࠥࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡴࠤባ")
    bstack1l1l1ll111l_opy_ = bstack1ll1l1_opy_ (u"ࠦࡳࡵ࡮ࡠࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡸࠨቤ")
    bstack1l1l1lllll1_opy_ = bstack1ll1l1_opy_ (u"ࠧࡺࡥࡴࡶࡢࡷࡪࡹࡳࡪࡱࡱࡷࠧብ")
    bstack1l1l1llllll_opy_ = bstack1ll1l1_opy_ (u"ࠨࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢ࡭ࡳࡹࡴࡢࡰࡦࡩࡤࡸࡥࡧࡵࠥቦ")
    bstack1ll111llll1_opy_ = bstack1ll1l1_opy_ (u"ࠢࡤࡤࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤࡩࡲࡦࡣࡷࡩࡩࠨቧ")
    bstack1l1l1lll1ll_opy_ = bstack1ll1l1_opy_ (u"ࠣࡥࡥࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࡥ࡮ࡢ࡯ࡨࠦቨ")
    bstack1l1l1ll1l11_opy_ = bstack1ll1l1_opy_ (u"ࠤࡦࡦࡹࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡴࡶࡤࡸࡺࡹࠢቩ")
    def __init__(self):
        super().__init__(bstack1ll11l1ll11_opy_=self.bstack1l1l1ll1l1l_opy_, frameworks=[bstack1lll1ll1lll_opy_.NAME])
        if not self.is_enabled():
            return
        TestFramework.bstack1ll1l11l1l1_opy_((bstack1lllllll1ll_opy_.BEFORE_EACH, bstack1lll1l11l1l_opy_.POST), self.bstack1l1ll111111_opy_)
        if bstack111111111_opy_():
            TestFramework.bstack1ll1l11l1l1_opy_((bstack1lllllll1ll_opy_.TEST, bstack1lll1l11l1l_opy_.POST), self.bstack1ll1l1111ll_opy_)
        else:
            TestFramework.bstack1ll1l11l1l1_opy_((bstack1lllllll1ll_opy_.TEST, bstack1lll1l11l1l_opy_.PRE), self.bstack1ll1l1111ll_opy_)
        TestFramework.bstack1ll1l11l1l1_opy_((bstack1lllllll1ll_opy_.TEST, bstack1lll1l11l1l_opy_.POST), self.bstack1ll1ll1llll_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1ll111111_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1l1l1l1_opy_,
        bstack1111l1l11l_opy_: Tuple[bstack1lllllll1ll_opy_, bstack1lll1l11l1l_opy_],
        *args,
        **kwargs,
    ):
        bstack1l1l1llll1l_opy_ = self.bstack1l1l1lll1l1_opy_(instance.context)
        if not bstack1l1l1llll1l_opy_:
            self.logger.debug(bstack1ll1l1_opy_ (u"ࠥࡷࡪࡺ࡟ࡢࡥࡷ࡭ࡻ࡫࡟ࡱࡣࡪࡩ࠿ࠦ࡮ࡰࠢࡳࡥ࡬࡫ࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࠣቪ") + str(bstack1111l1l11l_opy_) + bstack1ll1l1_opy_ (u"ࠦࠧቫ"))
            return
        f.bstack1111111111_opy_(instance, bstack1llll1l1l11_opy_.bstack1l1lll1l1l1_opy_, bstack1l1l1llll1l_opy_)
    def bstack1l1l1lll1l1_opy_(self, context: bstack111111l1l1_opy_, bstack1l1l1ll1lll_opy_= True):
        if bstack1l1l1ll1lll_opy_:
            bstack1l1l1llll1l_opy_ = self.bstack1ll11l1ll1l_opy_(context, reverse=True)
        else:
            bstack1l1l1llll1l_opy_ = self.bstack1ll11l11ll1_opy_(context, reverse=True)
        return [f for f in bstack1l1l1llll1l_opy_ if f[1].state != bstack11111ll1l1_opy_.QUIT]
    def bstack1ll1l1111ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1l1l1l1_opy_,
        bstack1111l1l11l_opy_: Tuple[bstack1lllllll1ll_opy_, bstack1lll1l11l1l_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1ll111111_opy_(f, instance, bstack1111l1l11l_opy_, *args, **kwargs)
        if not bstack1l1llll11ll_opy_:
            self.logger.debug(bstack1ll1l1_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࡷࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣቬ") + str(kwargs) + bstack1ll1l1_opy_ (u"ࠨࠢቭ"))
            return
        bstack1l1l1llll1l_opy_ = f.bstack11111lllll_opy_(instance, bstack1llll1l1l11_opy_.bstack1l1lll1l1l1_opy_, [])
        if not bstack1l1l1llll1l_opy_:
            self.logger.debug(bstack1ll1l1_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥቮ") + str(kwargs) + bstack1ll1l1_opy_ (u"ࠣࠤቯ"))
            return
        if len(bstack1l1l1llll1l_opy_) > 1:
            self.logger.debug(
                bstack1lllll1ll11_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࢀࡲࡥ࡯ࠪࡳࡥ࡬࡫࡟ࡪࡰࡶࡸࡦࡴࡣࡦࡵࠬࢁࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࡾ࡯ࡼࡧࡲࡨࡵࢀࠦተ"))
        bstack1l1l1lll11l_opy_, bstack1l1ll1llll1_opy_ = bstack1l1l1llll1l_opy_[0]
        page = bstack1l1l1lll11l_opy_()
        if not page:
            self.logger.debug(bstack1ll1l1_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࡴ࡯ࠡࡲࡤ࡫ࡪࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥቱ") + str(kwargs) + bstack1ll1l1_opy_ (u"ࠦࠧቲ"))
            return
        bstack1l1l111l1_opy_ = getattr(args[0], bstack1ll1l1_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࠧታ"), None)
        try:
            page.evaluate(bstack1ll1l1_opy_ (u"ࠨ࡟ࠡ࠿ࡁࠤࢀࢃࠢቴ"),
                        bstack1ll1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡳࡧ࡭ࡦࠤ࠽ࠫት") + json.dumps(
                            bstack1l1l111l1_opy_) + bstack1ll1l1_opy_ (u"ࠣࡿࢀࠦቶ"))
        except Exception as e:
            self.logger.debug(bstack1ll1l1_opy_ (u"ࠤࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨࠤࢀࢃࠢቷ"), e)
    def bstack1ll1ll1llll_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1l1l1l1_opy_,
        bstack1111l1l11l_opy_: Tuple[bstack1lllllll1ll_opy_, bstack1lll1l11l1l_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1ll111111_opy_(f, instance, bstack1111l1l11l_opy_, *args, **kwargs)
        if not bstack1l1llll11ll_opy_:
            self.logger.debug(bstack1ll1l1_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࡴ࡯ࡵࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨቸ") + str(kwargs) + bstack1ll1l1_opy_ (u"ࠦࠧቹ"))
            return
        bstack1l1l1llll1l_opy_ = f.bstack11111lllll_opy_(instance, bstack1llll1l1l11_opy_.bstack1l1lll1l1l1_opy_, [])
        if not bstack1l1l1llll1l_opy_:
            self.logger.debug(bstack1ll1l1_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࠣࡨࡷ࡯ࡶࡦࡴࡶࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣቺ") + str(kwargs) + bstack1ll1l1_opy_ (u"ࠨࠢቻ"))
            return
        if len(bstack1l1l1llll1l_opy_) > 1:
            self.logger.debug(
                bstack1lllll1ll11_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡾࡰࡪࡴࠨࡱࡣࡪࡩࡤ࡯࡮ࡴࡶࡤࡲࡨ࡫ࡳࠪࡿࠣࡨࡷ࡯ࡶࡦࡴࡶࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࡼ࡭ࡺࡥࡷ࡭ࡳࡾࠤቼ"))
        bstack1l1l1lll11l_opy_, bstack1l1ll1llll1_opy_ = bstack1l1l1llll1l_opy_[0]
        page = bstack1l1l1lll11l_opy_()
        if not page:
            self.logger.debug(bstack1ll1l1_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࠦࡰࡢࡩࡨࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣች") + str(kwargs) + bstack1ll1l1_opy_ (u"ࠤࠥቾ"))
            return
        status = f.bstack11111lllll_opy_(instance, TestFramework.bstack1l1l1lll111_opy_, None)
        if not status:
            self.logger.debug(bstack1ll1l1_opy_ (u"ࠥࡲࡴࠦࡳࡵࡣࡷࡹࡸࠦࡦࡰࡴࠣࡸࡪࡹࡴ࠭ࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࠨቿ") + str(bstack1111l1l11l_opy_) + bstack1ll1l1_opy_ (u"ࠦࠧኀ"))
            return
        bstack1l1l1llll11_opy_ = {bstack1ll1l1_opy_ (u"ࠧࡹࡴࡢࡶࡸࡷࠧኁ"): status.lower()}
        bstack1l1l1l1llll_opy_ = f.bstack11111lllll_opy_(instance, TestFramework.bstack1l1l1ll1111_opy_, None)
        if status.lower() == bstack1ll1l1_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ኂ") and bstack1l1l1l1llll_opy_ is not None:
            bstack1l1l1llll11_opy_[bstack1ll1l1_opy_ (u"ࠧࡳࡧࡤࡷࡴࡴࠧኃ")] = bstack1l1l1l1llll_opy_[0][bstack1ll1l1_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫኄ")][0] if isinstance(bstack1l1l1l1llll_opy_, list) else str(bstack1l1l1l1llll_opy_)
        try:
              page.evaluate(
                    bstack1ll1l1_opy_ (u"ࠤࡢࠤࡂࡄࠠࡼࡿࠥኅ"),
                    bstack1ll1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࠨኆ")
                    + json.dumps(bstack1l1l1llll11_opy_)
                    + bstack1ll1l1_opy_ (u"ࠦࢂࠨኇ")
                )
        except Exception as e:
            self.logger.debug(bstack1ll1l1_opy_ (u"ࠧ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡶࡸࡦࡺࡵࡴࠢࡾࢁࠧኈ"), e)
    def bstack1l1lll1l111_opy_(
        self,
        instance: bstack1lll1l1l1l1_opy_,
        f: TestFramework,
        bstack1111l1l11l_opy_: Tuple[bstack1lllllll1ll_opy_, bstack1lll1l11l1l_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1ll111111_opy_(f, instance, bstack1111l1l11l_opy_, *args, **kwargs)
        if not bstack1l1llll11ll_opy_:
            self.logger.debug(
                bstack1lllll1ll11_opy_ (u"ࠨ࡭ࡢࡴ࡮ࡣࡴ࠷࠱ࡺࡡࡶࡽࡳࡩ࠺ࠡࡰࡲࡸࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠱ࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࢁ࡫ࡸࡣࡵ࡫ࡸࢃࠢ኉"))
            return
        bstack1l1l1llll1l_opy_ = f.bstack11111lllll_opy_(instance, bstack1llll1l1l11_opy_.bstack1l1lll1l1l1_opy_, [])
        if not bstack1l1l1llll1l_opy_:
            self.logger.debug(bstack1ll1l1_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥኊ") + str(kwargs) + bstack1ll1l1_opy_ (u"ࠣࠤኋ"))
            return
        if len(bstack1l1l1llll1l_opy_) > 1:
            self.logger.debug(
                bstack1lllll1ll11_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࢀࡲࡥ࡯ࠪࡳࡥ࡬࡫࡟ࡪࡰࡶࡸࡦࡴࡣࡦࡵࠬࢁࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࡾ࡯ࡼࡧࡲࡨࡵࢀࠦኌ"))
        bstack1l1l1lll11l_opy_, bstack1l1ll1llll1_opy_ = bstack1l1l1llll1l_opy_[0]
        page = bstack1l1l1lll11l_opy_()
        if not page:
            self.logger.debug(bstack1ll1l1_opy_ (u"ࠥࡱࡦࡸ࡫ࡠࡱ࠴࠵ࡾࡥࡳࡺࡰࡦ࠾ࠥࡴ࡯ࠡࡲࡤ࡫ࡪࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥኍ") + str(kwargs) + bstack1ll1l1_opy_ (u"ࠦࠧ኎"))
            return
        timestamp = int(time.time() * 1000)
        data = bstack1ll1l1_opy_ (u"ࠧࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࡘࡿ࡮ࡤ࠼ࠥ኏") + str(timestamp)
        try:
            page.evaluate(
                bstack1ll1l1_opy_ (u"ࠨ࡟ࠡ࠿ࡁࠤࢀࢃࠢነ"),
                bstack1ll1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠬኑ").format(
                    json.dumps(
                        {
                            bstack1ll1l1_opy_ (u"ࠣࡣࡦࡸ࡮ࡵ࡮ࠣኒ"): bstack1ll1l1_opy_ (u"ࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦና"),
                            bstack1ll1l1_opy_ (u"ࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨኔ"): {
                                bstack1ll1l1_opy_ (u"ࠦࡹࡿࡰࡦࠤን"): bstack1ll1l1_opy_ (u"ࠧࡇ࡮࡯ࡱࡷࡥࡹ࡯࡯࡯ࠤኖ"),
                                bstack1ll1l1_opy_ (u"ࠨࡤࡢࡶࡤࠦኗ"): data,
                                bstack1ll1l1_opy_ (u"ࠢ࡭ࡧࡹࡩࡱࠨኘ"): bstack1ll1l1_opy_ (u"ࠣࡦࡨࡦࡺ࡭ࠢኙ")
                            }
                        }
                    )
                )
            )
        except Exception as e:
            self.logger.debug(bstack1ll1l1_opy_ (u"ࠤࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡵ࠱࠲ࡻࠣࡥࡳࡴ࡯ࡵࡣࡷ࡭ࡴࡴࠠ࡮ࡣࡵ࡯࡮ࡴࡧࠡࡽࢀࠦኚ"), e)
    def bstack1ll11l11l11_opy_(
        self,
        instance: bstack1lll1l1l1l1_opy_,
        f: TestFramework,
        bstack1111l1l11l_opy_: Tuple[bstack1lllllll1ll_opy_, bstack1lll1l11l1l_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1ll111111_opy_(f, instance, bstack1111l1l11l_opy_, *args, **kwargs)
        if f.bstack11111lllll_opy_(instance, bstack1llll1l1l11_opy_.bstack1ll111llll1_opy_, False):
            return
        self.bstack1ll1l11ll11_opy_()
        req = structs.TestSessionEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack11111lllll_opy_(instance, TestFramework.bstack1ll11llll1l_opy_)
        req.test_framework_name = TestFramework.bstack11111lllll_opy_(instance, TestFramework.bstack1ll1ll1l1ll_opy_)
        req.test_framework_version = TestFramework.bstack11111lllll_opy_(instance, TestFramework.bstack1ll111l1lll_opy_)
        req.test_framework_state = bstack1111l1l11l_opy_[0].name
        req.test_hook_state = bstack1111l1l11l_opy_[1].name
        req.test_uuid = TestFramework.bstack11111lllll_opy_(instance, TestFramework.bstack1ll1ll1ll11_opy_)
        for bstack1l1l1ll11ll_opy_ in bstack1llll1l1111_opy_.bstack1llllllll1l_opy_.values():
            session = req.automation_sessions.add()
            session.provider = (
                bstack1ll1l1_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠤኛ")
                if bstack1l1llll11ll_opy_
                else bstack1ll1l1_opy_ (u"ࠦࡺࡴ࡫࡯ࡱࡺࡲࡤ࡭ࡲࡪࡦࠥኜ")
            )
            session.ref = bstack1l1l1ll11ll_opy_.ref()
            session.hub_url = bstack1llll1l1111_opy_.bstack11111lllll_opy_(bstack1l1l1ll11ll_opy_, bstack1llll1l1111_opy_.bstack1l1ll1l11ll_opy_, bstack1ll1l1_opy_ (u"ࠧࠨኝ"))
            session.framework_name = bstack1l1l1ll11ll_opy_.framework_name
            session.framework_version = bstack1l1l1ll11ll_opy_.framework_version
            session.framework_session_id = bstack1llll1l1111_opy_.bstack11111lllll_opy_(bstack1l1l1ll11ll_opy_, bstack1llll1l1111_opy_.bstack1l1ll111l1l_opy_, bstack1ll1l1_opy_ (u"ࠨࠢኞ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        return req
    def bstack1ll1lll111l_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1l1l1l1_opy_,
        bstack1111l1l11l_opy_: Tuple[bstack1lllllll1ll_opy_, bstack1lll1l11l1l_opy_],
        *args,
        **kwargs
    ):
        bstack1l1l1llll1l_opy_ = f.bstack11111lllll_opy_(instance, bstack1llll1l1l11_opy_.bstack1l1lll1l1l1_opy_, [])
        if not bstack1l1l1llll1l_opy_:
            self.logger.debug(bstack1ll1l1_opy_ (u"ࠢࡨࡧࡷࡣࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡦࡵ࡭ࡻ࡫ࡲ࠻ࠢࡱࡳࠥࡶࡡࡨࡧࡶࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣኟ") + str(kwargs) + bstack1ll1l1_opy_ (u"ࠣࠤአ"))
            return
        if len(bstack1l1l1llll1l_opy_) > 1:
            self.logger.debug(bstack1ll1l1_opy_ (u"ࠤࡪࡩࡹࡥࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡨࡷ࡯ࡶࡦࡴ࠽ࠤࢀࡲࡥ࡯ࠪࡳࡥ࡬࡫࡟ࡪࡰࡶࡸࡦࡴࡣࡦࡵࠬࢁࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥኡ") + str(kwargs) + bstack1ll1l1_opy_ (u"ࠥࠦኢ"))
        bstack1l1l1lll11l_opy_, bstack1l1ll1llll1_opy_ = bstack1l1l1llll1l_opy_[0]
        page = bstack1l1l1lll11l_opy_()
        if not page:
            self.logger.debug(bstack1ll1l1_opy_ (u"ࠦ࡬࡫ࡴࡠࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡪࡲࡪࡸࡨࡶ࠿ࠦ࡮ࡰࠢࡳࡥ࡬࡫ࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦኣ") + str(kwargs) + bstack1ll1l1_opy_ (u"ࠧࠨኤ"))
            return
        return page
    def bstack1ll1ll11111_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1l1l1l1_opy_,
        bstack1111l1l11l_opy_: Tuple[bstack1lllllll1ll_opy_, bstack1lll1l11l1l_opy_],
        *args,
        **kwargs
    ):
        caps = {}
        bstack1l1l1ll11l1_opy_ = {}
        for bstack1l1l1ll11ll_opy_ in bstack1llll1l1111_opy_.bstack1llllllll1l_opy_.values():
            caps = bstack1llll1l1111_opy_.bstack11111lllll_opy_(bstack1l1l1ll11ll_opy_, bstack1llll1l1111_opy_.bstack1l1ll111l11_opy_, bstack1ll1l1_opy_ (u"ࠨࠢእ"))
        bstack1l1l1ll11l1_opy_[bstack1ll1l1_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠧኦ")] = caps.get(bstack1ll1l1_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࠤኧ"), bstack1ll1l1_opy_ (u"ࠤࠥከ"))
        bstack1l1l1ll11l1_opy_[bstack1ll1l1_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠤኩ")] = caps.get(bstack1ll1l1_opy_ (u"ࠦࡴࡹࠢኪ"), bstack1ll1l1_opy_ (u"ࠧࠨካ"))
        bstack1l1l1ll11l1_opy_[bstack1ll1l1_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠣኬ")] = caps.get(bstack1ll1l1_opy_ (u"ࠢࡰࡵࡢࡺࡪࡸࡳࡪࡱࡱࠦክ"), bstack1ll1l1_opy_ (u"ࠣࠤኮ"))
        bstack1l1l1ll11l1_opy_[bstack1ll1l1_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠥኯ")] = caps.get(bstack1ll1l1_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠧኰ"), bstack1ll1l1_opy_ (u"ࠦࠧ኱"))
        return bstack1l1l1ll11l1_opy_
    def bstack1ll1l111l11_opy_(self, page: object, bstack1ll1ll11l11_opy_, args={}):
        try:
            bstack1l1l1ll1ll1_opy_ = bstack1ll1l1_opy_ (u"ࠧࠨࠢࠩࡨࡸࡲࡨࡺࡩࡰࡰࠣࠬ࠳࠴࠮ࡣࡵࡷࡥࡨࡱࡓࡥ࡭ࡄࡶ࡬ࡹࠩࠡࡽࡾࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡲࡦࡶࡸࡶࡳࠦ࡮ࡦࡹࠣࡔࡷࡵ࡭ࡪࡵࡨࠬ࠭ࡸࡥࡴࡱ࡯ࡺࡪ࠲ࠠࡳࡧ࡭ࡩࡨࡺࠩࠡ࠿ࡁࠤࢀࢁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡢࡴࡶࡤࡧࡰ࡙ࡤ࡬ࡃࡵ࡫ࡸ࠴ࡰࡶࡵ࡫ࠬࡷ࡫ࡳࡰ࡮ࡹࡩ࠮ࡁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡻࡧࡰࡢࡦࡴࡪࡹࡾࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࢂࢃࠩ࠼ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡾࡿࠬࠬࢀࡧࡲࡨࡡ࡭ࡷࡴࡴࡽࠪࠤࠥࠦኲ")
            bstack1ll1ll11l11_opy_ = bstack1ll1ll11l11_opy_.replace(bstack1ll1l1_opy_ (u"ࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤኳ"), bstack1ll1l1_opy_ (u"ࠢࡣࡵࡷࡥࡨࡱࡓࡥ࡭ࡄࡶ࡬ࡹࠢኴ"))
            script = bstack1l1l1ll1ll1_opy_.format(fn_body=bstack1ll1ll11l11_opy_, arg_json=json.dumps(args))
            return page.evaluate(script)
        except Exception as e:
            self.logger.error(bstack1ll1l1_opy_ (u"ࠣࡣ࠴࠵ࡾࡥࡳࡤࡴ࡬ࡴࡹࡥࡥࡹࡧࡦࡹࡹ࡫࠺ࠡࡇࡵࡶࡴࡸࠠࡦࡺࡨࡧࡺࡺࡩ࡯ࡩࠣࡸ࡭࡫ࠠࡢ࠳࠴ࡽࠥࡹࡣࡳ࡫ࡳࡸ࠱ࠦࠢኵ") + str(e) + bstack1ll1l1_opy_ (u"ࠤࠥ኶"))
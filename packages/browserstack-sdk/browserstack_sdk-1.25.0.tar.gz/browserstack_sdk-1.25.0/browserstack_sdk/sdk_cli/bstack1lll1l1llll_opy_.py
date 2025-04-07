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
from datetime import datetime, timezone
from browserstack_sdk.sdk_cli.bstack1111l11lll_opy_ import (
    bstack1111l1ll1l_opy_,
    bstack111111111l_opy_,
    bstack11111ll1l1_opy_,
    bstack11111l11ll_opy_,
    bstack11111l1111_opy_,
)
from browserstack_sdk.sdk_cli.bstack1lllll1ll11_opy_ import bstack1lll1l11ll1_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1llllll1lll_opy_, bstack1lll111lll1_opy_, bstack1lllllll111_opy_
from browserstack_sdk.sdk_cli.bstack1ll11ll111l_opy_ import bstack1ll11l1llll_opy_
from typing import Tuple, Dict, Any, List, Union
from bstack_utils.helper import bstack1ll1111l1ll_opy_
from browserstack_sdk import sdk_pb2 as structs
from bstack_utils.measure import measure
from bstack_utils.constants import *
from typing import Tuple, List, Any
class bstack1lll1lll11l_opy_(bstack1ll11l1llll_opy_):
    bstack1l1ll11lll1_opy_ = bstack11l1l11_opy_ (u"ࠣࡶࡨࡷࡹࡥࡤࡳ࡫ࡹࡩࡷࡹࠢይ")
    bstack1ll111lll11_opy_ = bstack11l1l11_opy_ (u"ࠤࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡳࡦࡵࡶ࡭ࡴࡴࡳࠣዮ")
    bstack1l1ll111111_opy_ = bstack11l1l11_opy_ (u"ࠥࡲࡴࡴ࡟ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡷࡪࡹࡳࡪࡱࡱࡷࠧዯ")
    bstack1l1ll11llll_opy_ = bstack11l1l11_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡶࡩࡸࡹࡩࡰࡰࡶࠦደ")
    bstack1l1ll11ll1l_opy_ = bstack11l1l11_opy_ (u"ࠧࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡣࡷ࡫ࡦࡴࠤዱ")
    bstack1ll11111l1l_opy_ = bstack11l1l11_opy_ (u"ࠨࡣࡣࡶࡢࡷࡪࡹࡳࡪࡱࡱࡣࡨࡸࡥࡢࡶࡨࡨࠧዲ")
    bstack1l1ll11l11l_opy_ = bstack11l1l11_opy_ (u"ࠢࡤࡤࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤࡴࡡ࡮ࡧࠥዳ")
    bstack1l1ll111l1l_opy_ = bstack11l1l11_opy_ (u"ࠣࡥࡥࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡳࡵࡣࡷࡹࡸࠨዴ")
    def __init__(self):
        super().__init__(bstack1ll11ll11l1_opy_=self.bstack1l1ll11lll1_opy_, frameworks=[bstack1lll1l11ll1_opy_.NAME])
        if not self.is_enabled():
            return
        TestFramework.bstack1ll1l11l11l_opy_((bstack1llllll1lll_opy_.BEFORE_EACH, bstack1lll111lll1_opy_.POST), self.bstack1l1l11ll1ll_opy_)
        TestFramework.bstack1ll1l11l11l_opy_((bstack1llllll1lll_opy_.TEST, bstack1lll111lll1_opy_.PRE), self.bstack1ll1l1ll11l_opy_)
        TestFramework.bstack1ll1l11l11l_opy_((bstack1llllll1lll_opy_.TEST, bstack1lll111lll1_opy_.POST), self.bstack1ll1lll1l1l_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1l11ll1ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1lllllll111_opy_,
        bstack1111l1ll11_opy_: Tuple[bstack1llllll1lll_opy_, bstack1lll111lll1_opy_],
        *args,
        **kwargs,
    ):
        bstack1ll1111l11l_opy_ = self.bstack1l1l11l1lll_opy_(instance.context)
        if not bstack1ll1111l11l_opy_:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠤࡶࡩࡹࡥࡡࡤࡶ࡬ࡺࡪࡥࡤࡳ࡫ࡹࡩࡷࡹ࠺ࠡࡰࡲࠤࡩࡸࡩࡷࡧࡵࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࠧድ") + str(bstack1111l1ll11_opy_) + bstack11l1l11_opy_ (u"ࠥࠦዶ"))
        f.bstack1111111l1l_opy_(instance, bstack1lll1lll11l_opy_.bstack1ll111lll11_opy_, bstack1ll1111l11l_opy_)
        bstack1l1l11ll1l1_opy_ = self.bstack1l1l11l1lll_opy_(instance.context, bstack1l1l11ll11l_opy_=False)
        f.bstack1111111l1l_opy_(instance, bstack1lll1lll11l_opy_.bstack1l1ll111111_opy_, bstack1l1l11ll1l1_opy_)
    def bstack1ll1l1ll11l_opy_(
        self,
        f: TestFramework,
        instance: bstack1lllllll111_opy_,
        bstack1111l1ll11_opy_: Tuple[bstack1llllll1lll_opy_, bstack1lll111lll1_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l11ll1ll_opy_(f, instance, bstack1111l1ll11_opy_, *args, **kwargs)
        if not f.bstack11111l1l1l_opy_(instance, bstack1lll1lll11l_opy_.bstack1l1ll11l11l_opy_, False):
            self.__1l1l1l11111_opy_(f,instance,bstack1111l1ll11_opy_)
    def bstack1ll1lll1l1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1lllllll111_opy_,
        bstack1111l1ll11_opy_: Tuple[bstack1llllll1lll_opy_, bstack1lll111lll1_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l11ll1ll_opy_(f, instance, bstack1111l1ll11_opy_, *args, **kwargs)
        if not f.bstack11111l1l1l_opy_(instance, bstack1lll1lll11l_opy_.bstack1l1ll11l11l_opy_, False):
            self.__1l1l1l11111_opy_(f, instance, bstack1111l1ll11_opy_)
        if not f.bstack11111l1l1l_opy_(instance, bstack1lll1lll11l_opy_.bstack1l1ll111l1l_opy_, False):
            self.__1l1l11lll1l_opy_(f, instance, bstack1111l1ll11_opy_)
    def bstack1l1l11ll111_opy_(
        self,
        f: bstack1lll1l11ll1_opy_,
        driver: object,
        exec: Tuple[bstack11111l11ll_opy_, str],
        bstack1111l1ll11_opy_: Tuple[bstack1111l1ll1l_opy_, bstack111111111l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if not f.bstack1ll1l1111ll_opy_(instance):
            return
        if f.bstack11111l1l1l_opy_(instance, bstack1lll1lll11l_opy_.bstack1l1ll111l1l_opy_, False):
            return
        driver.execute_script(
            bstack11l1l11_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠤዷ").format(
                json.dumps(
                    {
                        bstack11l1l11_opy_ (u"ࠧࡧࡣࡵ࡫ࡲࡲࠧዸ"): bstack11l1l11_opy_ (u"ࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠤዹ"),
                        bstack11l1l11_opy_ (u"ࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥዺ"): {bstack11l1l11_opy_ (u"ࠣࡵࡷࡥࡹࡻࡳࠣዻ"): result},
                    }
                )
            )
        )
        f.bstack1111111l1l_opy_(instance, bstack1lll1lll11l_opy_.bstack1l1ll111l1l_opy_, True)
    def bstack1l1l11l1lll_opy_(self, context: bstack11111l1111_opy_, bstack1l1l11ll11l_opy_= True):
        if bstack1l1l11ll11l_opy_:
            bstack1ll1111l11l_opy_ = self.bstack1ll11ll11ll_opy_(context, reverse=True)
        else:
            bstack1ll1111l11l_opy_ = self.bstack1ll11l1ll11_opy_(context, reverse=True)
        return [f for f in bstack1ll1111l11l_opy_ if f[1].state != bstack1111l1ll1l_opy_.QUIT]
    @measure(event_name=EVENTS.bstack1ll1l1l1l_opy_, stage=STAGE.bstack1l1ll1lll_opy_)
    def __1l1l11lll1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1lllllll111_opy_,
        bstack1111l1ll11_opy_: Tuple[bstack1llllll1lll_opy_, bstack1lll111lll1_opy_],
    ):
        bstack1ll1111l11l_opy_ = f.bstack11111l1l1l_opy_(instance, bstack1lll1lll11l_opy_.bstack1ll111lll11_opy_, [])
        if not bstack1ll1111l11l_opy_:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠤࡶࡩࡹࡥࡡࡤࡶ࡬ࡺࡪࡥࡤࡳ࡫ࡹࡩࡷࡹ࠺ࠡࡰࡲࠤࡩࡸࡩࡷࡧࡵࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࠧዼ") + str(bstack1111l1ll11_opy_) + bstack11l1l11_opy_ (u"ࠥࠦዽ"))
            return
        driver = bstack1ll1111l11l_opy_[0][0]()
        status = f.bstack11111l1l1l_opy_(instance, TestFramework.bstack1l1ll1111ll_opy_, None)
        if not status:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠦࡸ࡫ࡴࡠࡣࡦࡸ࡮ࡼࡥࡠࡦࡵ࡭ࡻ࡫ࡲࡴ࠼ࠣࡲࡴࠦࡳࡵࡣࡷࡹࡸࠦࡦࡰࡴࠣࡸࡪࡹࡴ࠭ࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࠨዾ") + str(bstack1111l1ll11_opy_) + bstack11l1l11_opy_ (u"ࠧࠨዿ"))
            return
        bstack1l1ll1111l1_opy_ = {bstack11l1l11_opy_ (u"ࠨࡳࡵࡣࡷࡹࡸࠨጀ"): status.lower()}
        bstack1l1ll11l1l1_opy_ = f.bstack11111l1l1l_opy_(instance, TestFramework.bstack1l1l1lllll1_opy_, None)
        if status.lower() == bstack11l1l11_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧጁ") and bstack1l1ll11l1l1_opy_ is not None:
            bstack1l1ll1111l1_opy_[bstack11l1l11_opy_ (u"ࠨࡴࡨࡥࡸࡵ࡮ࠨጂ")] = bstack1l1ll11l1l1_opy_[0][bstack11l1l11_opy_ (u"ࠩࡥࡥࡨࡱࡴࡳࡣࡦࡩࠬጃ")][0] if isinstance(bstack1l1ll11l1l1_opy_, list) else str(bstack1l1ll11l1l1_opy_)
        driver.execute_script(
            bstack11l1l11_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡽࠣጄ").format(
                json.dumps(
                    {
                        bstack11l1l11_opy_ (u"ࠦࡦࡩࡴࡪࡱࡱࠦጅ"): bstack11l1l11_opy_ (u"ࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠣጆ"),
                        bstack11l1l11_opy_ (u"ࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤጇ"): bstack1l1ll1111l1_opy_,
                    }
                )
            )
        )
        f.bstack1111111l1l_opy_(instance, bstack1lll1lll11l_opy_.bstack1l1ll111l1l_opy_, True)
    @measure(event_name=EVENTS.bstack11l1l1l1_opy_, stage=STAGE.bstack1l1ll1lll_opy_)
    def __1l1l1l11111_opy_(
        self,
        f: TestFramework,
        instance: bstack1lllllll111_opy_,
        bstack1111l1ll11_opy_: Tuple[bstack1llllll1lll_opy_, bstack1lll111lll1_opy_]
    ):
        test_name = f.bstack11111l1l1l_opy_(instance, TestFramework.bstack1l1l11llll1_opy_, None)
        if not test_name:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡰ࡭ࡸࡹࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡰࡤࡱࡪࠨገ"))
            return
        bstack1ll1111l11l_opy_ = f.bstack11111l1l1l_opy_(instance, bstack1lll1lll11l_opy_.bstack1ll111lll11_opy_, [])
        if not bstack1ll1111l11l_opy_:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠣࡵࡨࡸࡤࡧࡣࡵ࡫ࡹࡩࡤࡪࡲࡪࡸࡨࡶࡸࡀࠠ࡯ࡱࠣࡷࡹࡧࡴࡶࡵࠣࡪࡴࡸࠠࡵࡧࡶࡸ࠱ࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࠥጉ") + str(bstack1111l1ll11_opy_) + bstack11l1l11_opy_ (u"ࠤࠥጊ"))
            return
        for bstack1l1lll1l1ll_opy_, bstack1l1l11lllll_opy_ in bstack1ll1111l11l_opy_:
            if not bstack1lll1l11ll1_opy_.bstack1ll1l1111ll_opy_(bstack1l1l11lllll_opy_):
                continue
            driver = bstack1l1lll1l1ll_opy_()
            if not driver:
                continue
            driver.execute_script(
                bstack11l1l11_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡽࠣጋ").format(
                    json.dumps(
                        {
                            bstack11l1l11_opy_ (u"ࠦࡦࡩࡴࡪࡱࡱࠦጌ"): bstack11l1l11_opy_ (u"ࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨግ"),
                            bstack11l1l11_opy_ (u"ࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤጎ"): {bstack11l1l11_opy_ (u"ࠢ࡯ࡣࡰࡩࠧጏ"): test_name},
                        }
                    )
                )
            )
        f.bstack1111111l1l_opy_(instance, bstack1lll1lll11l_opy_.bstack1l1ll11l11l_opy_, True)
    def bstack1ll111ll11l_opy_(
        self,
        instance: bstack1lllllll111_opy_,
        f: TestFramework,
        bstack1111l1ll11_opy_: Tuple[bstack1llllll1lll_opy_, bstack1lll111lll1_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l11ll1ll_opy_(f, instance, bstack1111l1ll11_opy_, *args, **kwargs)
        bstack1ll1111l11l_opy_ = [d for d, _ in f.bstack11111l1l1l_opy_(instance, bstack1lll1lll11l_opy_.bstack1ll111lll11_opy_, [])]
        if not bstack1ll1111l11l_opy_:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠣࡱࡱࡣࡦ࡬ࡴࡦࡴࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࠥࡹࡥࡴࡵ࡬ࡳࡳࡹࠠࡵࡱࠣࡰ࡮ࡴ࡫ࠣጐ"))
            return
        if not bstack1ll1111l1ll_opy_():
            self.logger.debug(bstack11l1l11_opy_ (u"ࠤࡲࡲࡤࡧࡦࡵࡧࡵࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࡺࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠢ጑"))
            return
        for bstack1l1l11lll11_opy_ in bstack1ll1111l11l_opy_:
            driver = bstack1l1l11lll11_opy_()
            if not driver:
                continue
            timestamp = int(time.time() * 1000)
            data = bstack11l1l11_opy_ (u"ࠥࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࡖࡽࡳࡩ࠺ࠣጒ") + str(timestamp)
            driver.execute_script(
                bstack11l1l11_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠤጓ").format(
                    json.dumps(
                        {
                            bstack11l1l11_opy_ (u"ࠧࡧࡣࡵ࡫ࡲࡲࠧጔ"): bstack11l1l11_opy_ (u"ࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣጕ"),
                            bstack11l1l11_opy_ (u"ࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ጖"): {
                                bstack11l1l11_opy_ (u"ࠣࡶࡼࡴࡪࠨ጗"): bstack11l1l11_opy_ (u"ࠤࡄࡲࡳࡵࡴࡢࡶ࡬ࡳࡳࠨጘ"),
                                bstack11l1l11_opy_ (u"ࠥࡨࡦࡺࡡࠣጙ"): data,
                                bstack11l1l11_opy_ (u"ࠦࡱ࡫ࡶࡦ࡮ࠥጚ"): bstack11l1l11_opy_ (u"ࠧࡪࡥࡣࡷࡪࠦጛ")
                            }
                        }
                    )
                )
            )
    def bstack1l1lllll11l_opy_(
        self,
        instance: bstack1lllllll111_opy_,
        f: TestFramework,
        bstack1111l1ll11_opy_: Tuple[bstack1llllll1lll_opy_, bstack1lll111lll1_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l11ll1ll_opy_(f, instance, bstack1111l1ll11_opy_, *args, **kwargs)
        bstack1ll1111l11l_opy_ = [d for _, d in f.bstack11111l1l1l_opy_(instance, bstack1lll1lll11l_opy_.bstack1ll111lll11_opy_, [])] + [d for _, d in f.bstack11111l1l1l_opy_(instance, bstack1lll1lll11l_opy_.bstack1l1ll111111_opy_, [])]
        keys = [
            bstack1lll1lll11l_opy_.bstack1ll111lll11_opy_,
            bstack1lll1lll11l_opy_.bstack1l1ll111111_opy_,
        ]
        bstack1ll1111l11l_opy_ = [
            d for key in keys for _, d in f.bstack11111l1l1l_opy_(instance, key, [])
        ]
        if not bstack1ll1111l11l_opy_:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠨ࡯࡯ࡡࡤࡪࡹ࡫ࡲࡠࡶࡨࡷࡹࡀࠠࡶࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡪ࡮ࡴࡤࠡࡣࡱࡽࠥࡹࡥࡴࡵ࡬ࡳࡳࡹࠠࡵࡱࠣࡰ࡮ࡴ࡫ࠣጜ"))
            return
        if f.bstack11111l1l1l_opy_(instance, bstack1lll1lll11l_opy_.bstack1ll11111l1l_opy_, False):
            self.logger.debug(bstack11l1l11_opy_ (u"ࠢࡰࡰࡢࡥ࡫ࡺࡥࡳࡡࡷࡩࡸࡺ࠺ࠡࡅࡅࡘࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡣࡳࡧࡤࡸࡪࡪࠢጝ"))
            return
        self.bstack1ll1l1111l1_opy_()
        bstack1l1ll1l111_opy_ = datetime.now()
        req = structs.TestSessionEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack11111l1l1l_opy_(instance, TestFramework.bstack1ll1l11llll_opy_)
        req.test_framework_name = TestFramework.bstack11111l1l1l_opy_(instance, TestFramework.bstack1ll1l1llll1_opy_)
        req.test_framework_version = TestFramework.bstack11111l1l1l_opy_(instance, TestFramework.bstack1ll11111l11_opy_)
        req.test_framework_state = bstack1111l1ll11_opy_[0].name
        req.test_hook_state = bstack1111l1ll11_opy_[1].name
        req.test_uuid = TestFramework.bstack11111l1l1l_opy_(instance, TestFramework.bstack1ll1lll11l1_opy_)
        for driver in bstack1ll1111l11l_opy_:
            session = req.automation_sessions.add()
            session.provider = (
                bstack11l1l11_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠢጞ")
                if bstack1lll1l11ll1_opy_.bstack11111l1l1l_opy_(driver, bstack1lll1l11ll1_opy_.bstack1l1l1l1111l_opy_, False)
                else bstack11l1l11_opy_ (u"ࠤࡸࡲࡰࡴ࡯ࡸࡰࡢ࡫ࡷ࡯ࡤࠣጟ")
            )
            session.ref = driver.ref()
            session.hub_url = bstack1lll1l11ll1_opy_.bstack11111l1l1l_opy_(driver, bstack1lll1l11ll1_opy_.bstack1l1ll1llll1_opy_, bstack11l1l11_opy_ (u"ࠥࠦጠ"))
            session.framework_name = driver.framework_name
            session.framework_version = driver.framework_version
            session.framework_session_id = bstack1lll1l11ll1_opy_.bstack11111l1l1l_opy_(driver, bstack1lll1l11ll1_opy_.bstack1l1lll1111l_opy_, bstack11l1l11_opy_ (u"ࠦࠧጡ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        return req
    def bstack1ll1l1ll1ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1lllllll111_opy_,
        bstack1111l1ll11_opy_: Tuple[bstack1llllll1lll_opy_, bstack1lll111lll1_opy_],
        *args,
        **kwargs
    ):
        bstack1ll1111l11l_opy_ = f.bstack11111l1l1l_opy_(instance, bstack1lll1lll11l_opy_.bstack1ll111lll11_opy_, [])
        if not bstack1ll1111l11l_opy_:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࠣࡨࡷ࡯ࡶࡦࡴࡶࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣጢ") + str(kwargs) + bstack11l1l11_opy_ (u"ࠨࠢጣ"))
            return {}
        if len(bstack1ll1111l11l_opy_) > 1:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡾࡰࡪࡴࠨࡥࡴ࡬ࡺࡪࡸ࡟ࡪࡰࡶࡸࡦࡴࡣࡦࡵࠬࢁࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥጤ") + str(kwargs) + bstack11l1l11_opy_ (u"ࠣࠤጥ"))
            return {}
        bstack1l1lll1l1ll_opy_, bstack1l1lll11l1l_opy_ = bstack1ll1111l11l_opy_[0]
        driver = bstack1l1lll1l1ll_opy_()
        if not driver:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࠠࡥࡴ࡬ࡺࡪࡸࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦጦ") + str(kwargs) + bstack11l1l11_opy_ (u"ࠥࠦጧ"))
            return {}
        capabilities = f.bstack11111l1l1l_opy_(bstack1l1lll11l1l_opy_, bstack1lll1l11ll1_opy_.bstack1l1ll1l1lll_opy_)
        if not capabilities:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࠢࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠡࡨࡲࡹࡳࡪࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦጨ") + str(kwargs) + bstack11l1l11_opy_ (u"ࠧࠨጩ"))
            return {}
        return capabilities.get(bstack11l1l11_opy_ (u"ࠨࡡ࡭ࡹࡤࡽࡸࡓࡡࡵࡥ࡫ࠦጪ"), {})
    def bstack1ll1ll1ll11_opy_(
        self,
        f: TestFramework,
        instance: bstack1lllllll111_opy_,
        bstack1111l1ll11_opy_: Tuple[bstack1llllll1lll_opy_, bstack1lll111lll1_opy_],
        *args,
        **kwargs
    ):
        bstack1ll1111l11l_opy_ = f.bstack11111l1l1l_opy_(instance, bstack1lll1lll11l_opy_.bstack1ll111lll11_opy_, [])
        if not bstack1ll1111l11l_opy_:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠢࡨࡧࡷࡣࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡦࡵ࡭ࡻ࡫ࡲ࠻ࠢࡱࡳࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥጫ") + str(kwargs) + bstack11l1l11_opy_ (u"ࠣࠤጬ"))
            return
        if len(bstack1ll1111l11l_opy_) > 1:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠤࡪࡩࡹࡥࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡨࡷ࡯ࡶࡦࡴ࠽ࠤࢀࡲࡥ࡯ࠪࡧࡶ࡮ࡼࡥࡳࡡ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡷ࠮ࢃࠠࡥࡴ࡬ࡺࡪࡸࡳࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧጭ") + str(kwargs) + bstack11l1l11_opy_ (u"ࠥࠦጮ"))
        bstack1l1lll1l1ll_opy_, bstack1l1lll11l1l_opy_ = bstack1ll1111l11l_opy_[0]
        driver = bstack1l1lll1l1ll_opy_()
        if not driver:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠦ࡬࡫ࡴࡠࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡪࡲࡪࡸࡨࡶ࠿ࠦ࡮ࡰࠢࡧࡶ࡮ࡼࡥࡳࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨጯ") + str(kwargs) + bstack11l1l11_opy_ (u"ࠧࠨጰ"))
            return
        return driver
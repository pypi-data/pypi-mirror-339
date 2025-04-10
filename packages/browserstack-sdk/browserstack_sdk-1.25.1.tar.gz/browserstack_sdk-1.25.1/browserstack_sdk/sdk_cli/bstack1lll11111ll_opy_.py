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
from datetime import datetime, timezone
from browserstack_sdk.sdk_cli.bstack111111l1ll_opy_ import (
    bstack11111ll1l1_opy_,
    bstack1111l1l1l1_opy_,
    bstack11111lll1l_opy_,
    bstack1llllllllll_opy_,
    bstack111111l1l1_opy_,
)
from browserstack_sdk.sdk_cli.bstack1lll1ll11ll_opy_ import bstack1lll1ll1lll_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1lllllll1ll_opy_, bstack1lll1l11l1l_opy_, bstack1lll1l1l1l1_opy_
from browserstack_sdk.sdk_cli.bstack1ll11l1l1ll_opy_ import bstack1ll11l1lll1_opy_
from typing import Tuple, Dict, Any, List, Union
from bstack_utils.helper import bstack1l1llll11ll_opy_
from browserstack_sdk import sdk_pb2 as structs
from bstack_utils.measure import measure
from bstack_utils.constants import *
from typing import Tuple, List, Any
class bstack1lll1l1l11l_opy_(bstack1ll11l1lll1_opy_):
    bstack1l1l1ll1l1l_opy_ = bstack1ll1l1_opy_ (u"ࠧࡺࡥࡴࡶࡢࡨࡷ࡯ࡶࡦࡴࡶࠦጆ")
    bstack1l1lll1l1l1_opy_ = bstack1ll1l1_opy_ (u"ࠨࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡷࡪࡹࡳࡪࡱࡱࡷࠧጇ")
    bstack1l1l1ll111l_opy_ = bstack1ll1l1_opy_ (u"ࠢ࡯ࡱࡱࡣࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡴࠤገ")
    bstack1l1l1lllll1_opy_ = bstack1ll1l1_opy_ (u"ࠣࡶࡨࡷࡹࡥࡳࡦࡵࡶ࡭ࡴࡴࡳࠣጉ")
    bstack1l1l1llllll_opy_ = bstack1ll1l1_opy_ (u"ࠤࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡩ࡯ࡵࡷࡥࡳࡩࡥࡠࡴࡨࡪࡸࠨጊ")
    bstack1ll111llll1_opy_ = bstack1ll1l1_opy_ (u"ࠥࡧࡧࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡥࡵࡩࡦࡺࡥࡥࠤጋ")
    bstack1l1l1lll1ll_opy_ = bstack1ll1l1_opy_ (u"ࠦࡨࡨࡴࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡱࡥࡲ࡫ࠢጌ")
    bstack1l1l1ll1l11_opy_ = bstack1ll1l1_opy_ (u"ࠧࡩࡢࡵࡡࡶࡩࡸࡹࡩࡰࡰࡢࡷࡹࡧࡴࡶࡵࠥግ")
    def __init__(self):
        super().__init__(bstack1ll11l1ll11_opy_=self.bstack1l1l1ll1l1l_opy_, frameworks=[bstack1lll1ll1lll_opy_.NAME])
        if not self.is_enabled():
            return
        TestFramework.bstack1ll1l11l1l1_opy_((bstack1lllllll1ll_opy_.BEFORE_EACH, bstack1lll1l11l1l_opy_.POST), self.bstack1l1l111ll1l_opy_)
        TestFramework.bstack1ll1l11l1l1_opy_((bstack1lllllll1ll_opy_.TEST, bstack1lll1l11l1l_opy_.PRE), self.bstack1ll1l1111ll_opy_)
        TestFramework.bstack1ll1l11l1l1_opy_((bstack1lllllll1ll_opy_.TEST, bstack1lll1l11l1l_opy_.POST), self.bstack1ll1ll1llll_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1l111ll1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1l1l1l1_opy_,
        bstack1111l1l11l_opy_: Tuple[bstack1lllllll1ll_opy_, bstack1lll1l11l1l_opy_],
        *args,
        **kwargs,
    ):
        bstack1ll111l1l11_opy_ = self.bstack1l1l111llll_opy_(instance.context)
        if not bstack1ll111l1l11_opy_:
            self.logger.debug(bstack1ll1l1_opy_ (u"ࠨࡳࡦࡶࡢࡥࡨࡺࡩࡷࡧࡢࡨࡷ࡯ࡶࡦࡴࡶ࠾ࠥࡴ࡯ࠡࡦࡵ࡭ࡻ࡫ࡲࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࠤጎ") + str(bstack1111l1l11l_opy_) + bstack1ll1l1_opy_ (u"ࠢࠣጏ"))
        f.bstack1111111111_opy_(instance, bstack1lll1l1l11l_opy_.bstack1l1lll1l1l1_opy_, bstack1ll111l1l11_opy_)
        bstack1l1l11l11l1_opy_ = self.bstack1l1l111llll_opy_(instance.context, bstack1l1l111lll1_opy_=False)
        f.bstack1111111111_opy_(instance, bstack1lll1l1l11l_opy_.bstack1l1l1ll111l_opy_, bstack1l1l11l11l1_opy_)
    def bstack1ll1l1111ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1l1l1l1_opy_,
        bstack1111l1l11l_opy_: Tuple[bstack1lllllll1ll_opy_, bstack1lll1l11l1l_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l111ll1l_opy_(f, instance, bstack1111l1l11l_opy_, *args, **kwargs)
        if not f.bstack11111lllll_opy_(instance, bstack1lll1l1l11l_opy_.bstack1l1l1lll1ll_opy_, False):
            self.__1l1l111l111_opy_(f,instance,bstack1111l1l11l_opy_)
    def bstack1ll1ll1llll_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1l1l1l1_opy_,
        bstack1111l1l11l_opy_: Tuple[bstack1lllllll1ll_opy_, bstack1lll1l11l1l_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l111ll1l_opy_(f, instance, bstack1111l1l11l_opy_, *args, **kwargs)
        if not f.bstack11111lllll_opy_(instance, bstack1lll1l1l11l_opy_.bstack1l1l1lll1ll_opy_, False):
            self.__1l1l111l111_opy_(f, instance, bstack1111l1l11l_opy_)
        if not f.bstack11111lllll_opy_(instance, bstack1lll1l1l11l_opy_.bstack1l1l1ll1l11_opy_, False):
            self.__1l1l111l1l1_opy_(f, instance, bstack1111l1l11l_opy_)
    def bstack1l1l111l11l_opy_(
        self,
        f: bstack1lll1ll1lll_opy_,
        driver: object,
        exec: Tuple[bstack1llllllllll_opy_, str],
        bstack1111l1l11l_opy_: Tuple[bstack11111ll1l1_opy_, bstack1111l1l1l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if not f.bstack1ll1l1l1ll1_opy_(instance):
            return
        if f.bstack11111lllll_opy_(instance, bstack1lll1l1l11l_opy_.bstack1l1l1ll1l11_opy_, False):
            return
        driver.execute_script(
            bstack1ll1l1_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࢂࠨጐ").format(
                json.dumps(
                    {
                        bstack1ll1l1_opy_ (u"ࠤࡤࡧࡹ࡯࡯࡯ࠤ጑"): bstack1ll1l1_opy_ (u"ࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸࠨጒ"),
                        bstack1ll1l1_opy_ (u"ࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢጓ"): {bstack1ll1l1_opy_ (u"ࠧࡹࡴࡢࡶࡸࡷࠧጔ"): result},
                    }
                )
            )
        )
        f.bstack1111111111_opy_(instance, bstack1lll1l1l11l_opy_.bstack1l1l1ll1l11_opy_, True)
    def bstack1l1l111llll_opy_(self, context: bstack111111l1l1_opy_, bstack1l1l111lll1_opy_= True):
        if bstack1l1l111lll1_opy_:
            bstack1ll111l1l11_opy_ = self.bstack1ll11l1ll1l_opy_(context, reverse=True)
        else:
            bstack1ll111l1l11_opy_ = self.bstack1ll11l11ll1_opy_(context, reverse=True)
        return [f for f in bstack1ll111l1l11_opy_ if f[1].state != bstack11111ll1l1_opy_.QUIT]
    @measure(event_name=EVENTS.bstack1l1ll11l11_opy_, stage=STAGE.bstack1llll1l1_opy_)
    def __1l1l111l1l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1l1l1l1_opy_,
        bstack1111l1l11l_opy_: Tuple[bstack1lllllll1ll_opy_, bstack1lll1l11l1l_opy_],
    ):
        bstack1ll111l1l11_opy_ = f.bstack11111lllll_opy_(instance, bstack1lll1l1l11l_opy_.bstack1l1lll1l1l1_opy_, [])
        if not bstack1ll111l1l11_opy_:
            self.logger.debug(bstack1ll1l1_opy_ (u"ࠨࡳࡦࡶࡢࡥࡨࡺࡩࡷࡧࡢࡨࡷ࡯ࡶࡦࡴࡶ࠾ࠥࡴ࡯ࠡࡦࡵ࡭ࡻ࡫ࡲࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࠤጕ") + str(bstack1111l1l11l_opy_) + bstack1ll1l1_opy_ (u"ࠢࠣ጖"))
            return
        driver = bstack1ll111l1l11_opy_[0][0]()
        status = f.bstack11111lllll_opy_(instance, TestFramework.bstack1l1l1lll111_opy_, None)
        if not status:
            self.logger.debug(bstack1ll1l1_opy_ (u"ࠣࡵࡨࡸࡤࡧࡣࡵ࡫ࡹࡩࡤࡪࡲࡪࡸࡨࡶࡸࡀࠠ࡯ࡱࠣࡷࡹࡧࡴࡶࡵࠣࡪࡴࡸࠠࡵࡧࡶࡸ࠱ࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࠥ጗") + str(bstack1111l1l11l_opy_) + bstack1ll1l1_opy_ (u"ࠤࠥጘ"))
            return
        bstack1l1l1llll11_opy_ = {bstack1ll1l1_opy_ (u"ࠥࡷࡹࡧࡴࡶࡵࠥጙ"): status.lower()}
        bstack1l1l1l1llll_opy_ = f.bstack11111lllll_opy_(instance, TestFramework.bstack1l1l1ll1111_opy_, None)
        if status.lower() == bstack1ll1l1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫጚ") and bstack1l1l1l1llll_opy_ is not None:
            bstack1l1l1llll11_opy_[bstack1ll1l1_opy_ (u"ࠬࡸࡥࡢࡵࡲࡲࠬጛ")] = bstack1l1l1l1llll_opy_[0][bstack1ll1l1_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩጜ")][0] if isinstance(bstack1l1l1l1llll_opy_, list) else str(bstack1l1l1l1llll_opy_)
        driver.execute_script(
            bstack1ll1l1_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠧጝ").format(
                json.dumps(
                    {
                        bstack1ll1l1_opy_ (u"ࠣࡣࡦࡸ࡮ࡵ࡮ࠣጞ"): bstack1ll1l1_opy_ (u"ࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠧጟ"),
                        bstack1ll1l1_opy_ (u"ࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨጠ"): bstack1l1l1llll11_opy_,
                    }
                )
            )
        )
        f.bstack1111111111_opy_(instance, bstack1lll1l1l11l_opy_.bstack1l1l1ll1l11_opy_, True)
    @measure(event_name=EVENTS.bstack11l1l11ll_opy_, stage=STAGE.bstack1llll1l1_opy_)
    def __1l1l111l111_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1l1l1l1_opy_,
        bstack1111l1l11l_opy_: Tuple[bstack1lllllll1ll_opy_, bstack1lll1l11l1l_opy_]
    ):
        test_name = f.bstack11111lllll_opy_(instance, TestFramework.bstack1l1l111l1ll_opy_, None)
        if not test_name:
            self.logger.debug(bstack1ll1l1_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦ࡭ࡪࡵࡶ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡴࡡ࡮ࡧࠥጡ"))
            return
        bstack1ll111l1l11_opy_ = f.bstack11111lllll_opy_(instance, bstack1lll1l1l11l_opy_.bstack1l1lll1l1l1_opy_, [])
        if not bstack1ll111l1l11_opy_:
            self.logger.debug(bstack1ll1l1_opy_ (u"ࠧࡹࡥࡵࡡࡤࡧࡹ࡯ࡶࡦࡡࡧࡶ࡮ࡼࡥࡳࡵ࠽ࠤࡳࡵࠠࡴࡶࡤࡸࡺࡹࠠࡧࡱࡵࠤࡹ࡫ࡳࡵ࠮ࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࠢጢ") + str(bstack1111l1l11l_opy_) + bstack1ll1l1_opy_ (u"ࠨࠢጣ"))
            return
        for bstack1l1ll1l1l1l_opy_, bstack1l1l11l111l_opy_ in bstack1ll111l1l11_opy_:
            if not bstack1lll1ll1lll_opy_.bstack1ll1l1l1ll1_opy_(bstack1l1l11l111l_opy_):
                continue
            driver = bstack1l1ll1l1l1l_opy_()
            if not driver:
                continue
            driver.execute_script(
                bstack1ll1l1_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠧጤ").format(
                    json.dumps(
                        {
                            bstack1ll1l1_opy_ (u"ࠣࡣࡦࡸ࡮ࡵ࡮ࠣጥ"): bstack1ll1l1_opy_ (u"ࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥጦ"),
                            bstack1ll1l1_opy_ (u"ࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨጧ"): {bstack1ll1l1_opy_ (u"ࠦࡳࡧ࡭ࡦࠤጨ"): test_name},
                        }
                    )
                )
            )
        f.bstack1111111111_opy_(instance, bstack1lll1l1l11l_opy_.bstack1l1l1lll1ll_opy_, True)
    def bstack1l1lll1l111_opy_(
        self,
        instance: bstack1lll1l1l1l1_opy_,
        f: TestFramework,
        bstack1111l1l11l_opy_: Tuple[bstack1lllllll1ll_opy_, bstack1lll1l11l1l_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l111ll1l_opy_(f, instance, bstack1111l1l11l_opy_, *args, **kwargs)
        bstack1ll111l1l11_opy_ = [d for d, _ in f.bstack11111lllll_opy_(instance, bstack1lll1l1l11l_opy_.bstack1l1lll1l1l1_opy_, [])]
        if not bstack1ll111l1l11_opy_:
            self.logger.debug(bstack1ll1l1_opy_ (u"ࠧࡵ࡮ࡠࡣࡩࡸࡪࡸ࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࠢࡶࡩࡸࡹࡩࡰࡰࡶࠤࡹࡵࠠ࡭࡫ࡱ࡯ࠧጩ"))
            return
        if not bstack1l1llll11ll_opy_():
            self.logger.debug(bstack1ll1l1_opy_ (u"ࠨ࡯࡯ࡡࡤࡪࡹ࡫ࡲࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࡷࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠦጪ"))
            return
        for bstack1l1l11l1111_opy_ in bstack1ll111l1l11_opy_:
            driver = bstack1l1l11l1111_opy_()
            if not driver:
                continue
            timestamp = int(time.time() * 1000)
            data = bstack1ll1l1_opy_ (u"ࠢࡐࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࡓࡺࡰࡦ࠾ࠧጫ") + str(timestamp)
            driver.execute_script(
                bstack1ll1l1_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࢂࠨጬ").format(
                    json.dumps(
                        {
                            bstack1ll1l1_opy_ (u"ࠤࡤࡧࡹ࡯࡯࡯ࠤጭ"): bstack1ll1l1_opy_ (u"ࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧጮ"),
                            bstack1ll1l1_opy_ (u"ࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢጯ"): {
                                bstack1ll1l1_opy_ (u"ࠧࡺࡹࡱࡧࠥጰ"): bstack1ll1l1_opy_ (u"ࠨࡁ࡯ࡰࡲࡸࡦࡺࡩࡰࡰࠥጱ"),
                                bstack1ll1l1_opy_ (u"ࠢࡥࡣࡷࡥࠧጲ"): data,
                                bstack1ll1l1_opy_ (u"ࠣ࡮ࡨࡺࡪࡲࠢጳ"): bstack1ll1l1_opy_ (u"ࠤࡧࡩࡧࡻࡧࠣጴ")
                            }
                        }
                    )
                )
            )
    def bstack1ll11l11l11_opy_(
        self,
        instance: bstack1lll1l1l1l1_opy_,
        f: TestFramework,
        bstack1111l1l11l_opy_: Tuple[bstack1lllllll1ll_opy_, bstack1lll1l11l1l_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l111ll1l_opy_(f, instance, bstack1111l1l11l_opy_, *args, **kwargs)
        bstack1ll111l1l11_opy_ = [d for _, d in f.bstack11111lllll_opy_(instance, bstack1lll1l1l11l_opy_.bstack1l1lll1l1l1_opy_, [])] + [d for _, d in f.bstack11111lllll_opy_(instance, bstack1lll1l1l11l_opy_.bstack1l1l1ll111l_opy_, [])]
        keys = [
            bstack1lll1l1l11l_opy_.bstack1l1lll1l1l1_opy_,
            bstack1lll1l1l11l_opy_.bstack1l1l1ll111l_opy_,
        ]
        bstack1ll111l1l11_opy_ = [
            d for key in keys for _, d in f.bstack11111lllll_opy_(instance, key, [])
        ]
        if not bstack1ll111l1l11_opy_:
            self.logger.debug(bstack1ll1l1_opy_ (u"ࠥࡳࡳࡥࡡࡧࡶࡨࡶࡤࡺࡥࡴࡶ࠽ࠤࡺࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡧ࡫ࡱࡨࠥࡧ࡮ࡺࠢࡶࡩࡸࡹࡩࡰࡰࡶࠤࡹࡵࠠ࡭࡫ࡱ࡯ࠧጵ"))
            return
        if f.bstack11111lllll_opy_(instance, bstack1lll1l1l11l_opy_.bstack1ll111llll1_opy_, False):
            self.logger.debug(bstack1ll1l1_opy_ (u"ࠦࡴࡴ࡟ࡢࡨࡷࡩࡷࡥࡴࡦࡵࡷ࠾ࠥࡉࡂࡕࠢࡤࡰࡷ࡫ࡡࡥࡻࠣࡧࡷ࡫ࡡࡵࡧࡧࠦጶ"))
            return
        self.bstack1ll1l11ll11_opy_()
        bstack1ll11l1l1_opy_ = datetime.now()
        req = structs.TestSessionEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack11111lllll_opy_(instance, TestFramework.bstack1ll11llll1l_opy_)
        req.test_framework_name = TestFramework.bstack11111lllll_opy_(instance, TestFramework.bstack1ll1ll1l1ll_opy_)
        req.test_framework_version = TestFramework.bstack11111lllll_opy_(instance, TestFramework.bstack1ll111l1lll_opy_)
        req.test_framework_state = bstack1111l1l11l_opy_[0].name
        req.test_hook_state = bstack1111l1l11l_opy_[1].name
        req.test_uuid = TestFramework.bstack11111lllll_opy_(instance, TestFramework.bstack1ll1ll1ll11_opy_)
        for driver in bstack1ll111l1l11_opy_:
            session = req.automation_sessions.add()
            session.provider = (
                bstack1ll1l1_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠦጷ")
                if bstack1lll1ll1lll_opy_.bstack11111lllll_opy_(driver, bstack1lll1ll1lll_opy_.bstack1l1l111ll11_opy_, False)
                else bstack1ll1l1_opy_ (u"ࠨࡵ࡯࡭ࡱࡳࡼࡴ࡟ࡨࡴ࡬ࡨࠧጸ")
            )
            session.ref = driver.ref()
            session.hub_url = bstack1lll1ll1lll_opy_.bstack11111lllll_opy_(driver, bstack1lll1ll1lll_opy_.bstack1l1ll1l11ll_opy_, bstack1ll1l1_opy_ (u"ࠢࠣጹ"))
            session.framework_name = driver.framework_name
            session.framework_version = driver.framework_version
            session.framework_session_id = bstack1lll1ll1lll_opy_.bstack11111lllll_opy_(driver, bstack1lll1ll1lll_opy_.bstack1l1ll111l1l_opy_, bstack1ll1l1_opy_ (u"ࠣࠤጺ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        return req
    def bstack1ll1ll11111_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1l1l1l1_opy_,
        bstack1111l1l11l_opy_: Tuple[bstack1lllllll1ll_opy_, bstack1lll1l11l1l_opy_],
        *args,
        **kwargs
    ):
        bstack1ll111l1l11_opy_ = f.bstack11111lllll_opy_(instance, bstack1lll1l1l11l_opy_.bstack1l1lll1l1l1_opy_, [])
        if not bstack1ll111l1l11_opy_:
            self.logger.debug(bstack1ll1l1_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࠠࡥࡴ࡬ࡺࡪࡸࡳࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧጻ") + str(kwargs) + bstack1ll1l1_opy_ (u"ࠥࠦጼ"))
            return {}
        if len(bstack1ll111l1l11_opy_) > 1:
            self.logger.debug(bstack1ll1l1_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦࡻ࡭ࡧࡱࠬࡩࡸࡩࡷࡧࡵࡣ࡮ࡴࡳࡵࡣࡱࡧࡪࡹࠩࡾࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢጽ") + str(kwargs) + bstack1ll1l1_opy_ (u"ࠧࠨጾ"))
            return {}
        bstack1l1ll1l1l1l_opy_, bstack1l1ll1llll1_opy_ = bstack1ll111l1l11_opy_[0]
        driver = bstack1l1ll1l1l1l_opy_()
        if not driver:
            self.logger.debug(bstack1ll1l1_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࠤࡩࡸࡩࡷࡧࡵࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣጿ") + str(kwargs) + bstack1ll1l1_opy_ (u"ࠢࠣፀ"))
            return {}
        capabilities = f.bstack11111lllll_opy_(bstack1l1ll1llll1_opy_, bstack1lll1ll1lll_opy_.bstack1l1ll111l11_opy_)
        if not capabilities:
            self.logger.debug(bstack1ll1l1_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࠦࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠥ࡬࡯ࡶࡰࡧࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣፁ") + str(kwargs) + bstack1ll1l1_opy_ (u"ࠤࠥፂ"))
            return {}
        return capabilities.get(bstack1ll1l1_opy_ (u"ࠥࡥࡱࡽࡡࡺࡵࡐࡥࡹࡩࡨࠣፃ"), {})
    def bstack1ll1lll111l_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1l1l1l1_opy_,
        bstack1111l1l11l_opy_: Tuple[bstack1lllllll1ll_opy_, bstack1lll1l11l1l_opy_],
        *args,
        **kwargs
    ):
        bstack1ll111l1l11_opy_ = f.bstack11111lllll_opy_(instance, bstack1lll1l1l11l_opy_.bstack1l1lll1l1l1_opy_, [])
        if not bstack1ll111l1l11_opy_:
            self.logger.debug(bstack1ll1l1_opy_ (u"ࠦ࡬࡫ࡴࡠࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡪࡲࡪࡸࡨࡶ࠿ࠦ࡮ࡰࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢፄ") + str(kwargs) + bstack1ll1l1_opy_ (u"ࠧࠨፅ"))
            return
        if len(bstack1ll111l1l11_opy_) > 1:
            self.logger.debug(bstack1ll1l1_opy_ (u"ࠨࡧࡦࡶࡢࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡥࡴ࡬ࡺࡪࡸ࠺ࠡࡽ࡯ࡩࡳ࠮ࡤࡳ࡫ࡹࡩࡷࡥࡩ࡯ࡵࡷࡥࡳࡩࡥࡴࠫࢀࠤࡩࡸࡩࡷࡧࡵࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤፆ") + str(kwargs) + bstack1ll1l1_opy_ (u"ࠢࠣፇ"))
        bstack1l1ll1l1l1l_opy_, bstack1l1ll1llll1_opy_ = bstack1ll111l1l11_opy_[0]
        driver = bstack1l1ll1l1l1l_opy_()
        if not driver:
            self.logger.debug(bstack1ll1l1_opy_ (u"ࠣࡩࡨࡸࡤࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡧࡶ࡮ࡼࡥࡳ࠼ࠣࡲࡴࠦࡤࡳ࡫ࡹࡩࡷࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥፈ") + str(kwargs) + bstack1ll1l1_opy_ (u"ࠤࠥፉ"))
            return
        return driver
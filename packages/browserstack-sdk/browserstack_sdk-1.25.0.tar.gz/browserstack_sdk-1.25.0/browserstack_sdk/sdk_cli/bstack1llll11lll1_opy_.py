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
from datetime import datetime
import os
import threading
from browserstack_sdk.sdk_cli.bstack1111l11lll_opy_ import (
    bstack1111l1ll1l_opy_,
    bstack111111111l_opy_,
    bstack11111ll1l1_opy_,
    bstack11111l11ll_opy_,
)
from browserstack_sdk.sdk_cli.bstack1lllll1ll11_opy_ import bstack1lll1l11ll1_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1llllll1lll_opy_, bstack1lll111lll1_opy_, bstack1lllllll111_opy_
from typing import Tuple, Dict, Any, List, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1lll11llll1_opy_ import bstack1lllll1l111_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l1llll_opy_ import bstack1lll1lll11l_opy_
from browserstack_sdk.sdk_cli.bstack1lll1ll1l1l_opy_ import bstack1lllll1llll_opy_
from browserstack_sdk.sdk_cli.bstack1llll1111l1_opy_ import bstack1llllll11ll_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.bstack1l1ll1l11l_opy_ import bstack1lll1llll1l_opy_
import grpc
import traceback
import json
class bstack1lllll11l11_opy_(bstack1lllll1l111_opy_):
    bstack1ll1ll1l11l_opy_ = False
    bstack1ll1l111l1l_opy_ = bstack11l1l11_opy_ (u"ࠥࡷࡪࡲࡥ࡯࡫ࡸࡱ࠳ࡽࡥࡣࡦࡵ࡭ࡻ࡫ࡲࠣჷ")
    bstack1ll1l11l1ll_opy_ = bstack11l1l11_opy_ (u"ࠦࡷ࡫࡭ࡰࡶࡨ࠲ࡼ࡫ࡢࡥࡴ࡬ࡺࡪࡸࠢჸ")
    bstack1ll1ll111ll_opy_ = bstack11l1l11_opy_ (u"ࠧࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡤ࡯࡮ࡪࡶࠥჹ")
    bstack1ll1ll11111_opy_ = bstack11l1l11_opy_ (u"ࠨࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡥࡩࡴࡡࡶࡧࡦࡴ࡮ࡪࡰࡪࠦჺ")
    bstack1ll1l1l1l11_opy_ = bstack11l1l11_opy_ (u"ࠢࡥࡴ࡬ࡺࡪࡸ࡟ࡩࡣࡶࡣࡺࡸ࡬ࠣ჻")
    scripts: Dict[str, Dict[str, str]]
    commands: Dict[str, Dict[str, Dict[str, List[str]]]]
    def __init__(self, bstack1llll11ll1l_opy_, bstack1llll1l1l1l_opy_):
        super().__init__()
        self.scripts = dict()
        self.commands = dict()
        self.accessibility = False
        if not self.is_enabled():
            return
        self.bstack1ll1l1l11l1_opy_ = bstack1llll1l1l1l_opy_
        bstack1llll11ll1l_opy_.bstack1ll1l11l11l_opy_((bstack1111l1ll1l_opy_.bstack111111l111_opy_, bstack111111111l_opy_.PRE), self.bstack1ll1lll1ll1_opy_)
        TestFramework.bstack1ll1l11l11l_opy_((bstack1llllll1lll_opy_.TEST, bstack1lll111lll1_opy_.PRE), self.bstack1ll1l1ll11l_opy_)
        TestFramework.bstack1ll1l11l11l_opy_((bstack1llllll1lll_opy_.TEST, bstack1lll111lll1_opy_.POST), self.bstack1ll1lll1l1l_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1ll1l1ll11l_opy_(
        self,
        f: TestFramework,
        instance: bstack1lllllll111_opy_,
        bstack1111l1ll11_opy_: Tuple[bstack1llllll1lll_opy_, bstack1lll111lll1_opy_],
        *args,
        **kwargs,
    ):
        tags = self._1ll1ll111l1_opy_(instance, args)
        test_framework = f.bstack11111l1l1l_opy_(instance, TestFramework.bstack1ll1l1llll1_opy_)
        if bstack11l1l11_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠬჼ") in instance.bstack1ll1lll11ll_opy_:
            platform_index = f.bstack11111l1l1l_opy_(instance, TestFramework.bstack1ll1l11llll_opy_)
            self.accessibility = self.bstack1ll1l1lllll_opy_(tags, self.config[bstack11l1l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬჽ")][platform_index])
        else:
            capabilities = self.bstack1ll1l1l11l1_opy_.bstack1ll1l1ll1ll_opy_(f, instance, bstack1111l1ll11_opy_, *args, **kwargs)
            if not capabilities:
                self.logger.debug(bstack11l1l11_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࡴ࡯ࠡࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠠࡧࡱࡸࡲࡩࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥჾ") + str(kwargs) + bstack11l1l11_opy_ (u"ࠦࠧჿ"))
                return
            self.accessibility = self.bstack1ll1l1lllll_opy_(tags, capabilities)
        if self.bstack1ll1l1l11l1_opy_.pages and self.bstack1ll1l1l11l1_opy_.pages.values():
            bstack1ll1l1l1lll_opy_ = list(self.bstack1ll1l1l11l1_opy_.pages.values())
            if bstack1ll1l1l1lll_opy_ and isinstance(bstack1ll1l1l1lll_opy_[0], (list, tuple)) and bstack1ll1l1l1lll_opy_[0]:
                bstack1ll1ll11l11_opy_ = bstack1ll1l1l1lll_opy_[0][0]
                if callable(bstack1ll1ll11l11_opy_):
                    page = bstack1ll1ll11l11_opy_()
                    def bstack11l1lll11l_opy_():
                        self.get_accessibility_results(page, bstack11l1l11_opy_ (u"ࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤᄀ"))
                    def bstack1ll1ll11lll_opy_():
                        self.get_accessibility_results_summary(page, bstack11l1l11_opy_ (u"ࠨࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥᄁ"))
                    setattr(page, bstack11l1l11_opy_ (u"ࠢࡨࡧࡷࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡕࡩࡸࡻ࡬ࡵࡵࠥᄂ"), bstack11l1lll11l_opy_)
                    setattr(page, bstack11l1l11_opy_ (u"ࠣࡩࡨࡸࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡖࡪࡹࡵ࡭ࡶࡖࡹࡲࡳࡡࡳࡻࠥᄃ"), bstack1ll1ll11lll_opy_)
        self.logger.debug(bstack11l1l11_opy_ (u"ࠤࡶ࡬ࡴࡻ࡬ࡥࠢࡵࡹࡳࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡶࡢ࡮ࡸࡩࡂࠨᄄ") + str(self.accessibility) + bstack11l1l11_opy_ (u"ࠥࠦᄅ"))
    def bstack1ll1lll1ll1_opy_(
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
            bstack1l1ll1l111_opy_ = datetime.now()
            self.bstack1ll1ll11ll1_opy_(f, exec, *args, **kwargs)
            instance, method_name = exec
            instance.bstack1ll11lll_opy_(bstack11l1l11_opy_ (u"ࠦࡦ࠷࠱ࡺ࠼࡬ࡲ࡮ࡺ࡟ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡤࡱࡱࡪ࡮࡭ࠢᄆ"), datetime.now() - bstack1l1ll1l111_opy_)
            if (
                not f.bstack1ll1ll11l1l_opy_(method_name)
                or f.bstack1ll1ll1l1ll_opy_(method_name, *args)
                or f.bstack1ll1l1ll1l1_opy_(method_name, *args)
            ):
                return
            if not f.bstack11111l1l1l_opy_(instance, bstack1lllll11l11_opy_.bstack1ll1ll111ll_opy_, False):
                if not bstack1lllll11l11_opy_.bstack1ll1ll1l11l_opy_:
                    self.logger.warning(bstack11l1l11_opy_ (u"ࠧࡡࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠ࡫ࡱࡨࡪࡾ࠽ࠣᄇ") + str(f.platform_index) + bstack11l1l11_opy_ (u"ࠨ࡝ࠡࡣ࠴࠵ࡾࠦࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠥ࡮ࡡࡷࡧࠣࡲࡴࡺࠠࡣࡧࡨࡲࠥࡹࡥࡵࠢࡩࡳࡷࠦࡴࡩ࡫ࡶࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠧᄈ"))
                    bstack1lllll11l11_opy_.bstack1ll1ll1l11l_opy_ = True
                return
            bstack1ll1lll111l_opy_ = self.scripts.get(f.framework_name, {})
            if not bstack1ll1lll111l_opy_:
                platform_index = f.bstack11111l1l1l_opy_(instance, bstack1lll1l11ll1_opy_.bstack1ll1l11llll_opy_, 0)
                self.logger.debug(bstack11l1l11_opy_ (u"ࠢ࡯ࡱࠣࡥ࠶࠷ࡹࠡࡵࡦࡶ࡮ࡶࡴࡴࠢࡩࡳࡷࠦࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠ࡫ࡱࡨࡪࡾ࠽ࡼࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢ࡭ࡳࡪࡥࡹࡿࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࡁࠧᄉ") + str(f.framework_name) + bstack11l1l11_opy_ (u"ࠣࠤᄊ"))
                return
            bstack1ll1l1ll111_opy_ = f.bstack1ll1ll1l111_opy_(*args)
            if not bstack1ll1l1ll111_opy_:
                self.logger.debug(bstack11l1l11_opy_ (u"ࠤࡰ࡭ࡸࡹࡩ࡯ࡩࠣࡧࡴࡳ࡭ࡢࡰࡧࡣࡳࡧ࡭ࡦࠢࡩࡳࡷࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫࠽ࡼࡨ࠱ࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࢁࠥࡳࡥࡵࡪࡲࡨࡤࡴࡡ࡮ࡧࡀࠦᄋ") + str(method_name) + bstack11l1l11_opy_ (u"ࠥࠦᄌ"))
                return
            bstack1ll1l11ll11_opy_ = f.bstack11111l1l1l_opy_(instance, bstack1lllll11l11_opy_.bstack1ll1l1l1l11_opy_, False)
            if bstack1ll1l1ll111_opy_ == bstack11l1l11_opy_ (u"ࠦ࡬࡫ࡴࠣᄍ") and not bstack1ll1l11ll11_opy_:
                f.bstack1111111l1l_opy_(instance, bstack1lllll11l11_opy_.bstack1ll1l1l1l11_opy_, True)
            if not bstack1ll1l11ll11_opy_:
                self.logger.debug(bstack11l1l11_opy_ (u"ࠧࡴ࡯ࠡࡗࡕࡐࠥࡲ࡯ࡢࡦࡨࡨࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࡃࡻࡧ࠰ࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࢀࠤࡨࡵ࡭࡮ࡣࡱࡨࡤࡴࡡ࡮ࡧࡀࠦᄎ") + str(bstack1ll1l1ll111_opy_) + bstack11l1l11_opy_ (u"ࠨࠢᄏ"))
                return
            scripts_to_run = self.commands.get(f.framework_name, {}).get(method_name, {}).get(bstack1ll1l1ll111_opy_, [])
            if not scripts_to_run:
                self.logger.debug(bstack11l1l11_opy_ (u"ࠢ࡯ࡱࠣࡥ࠶࠷ࡹࠡࡵࡦࡶ࡮ࡶࡴࡴࠢࡩࡳࡷࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫࠽ࡼࡨ࠱ࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࢁࠥࡩ࡯࡮࡯ࡤࡲࡩࡥ࡮ࡢ࡯ࡨࡁࠧᄐ") + str(bstack1ll1l1ll111_opy_) + bstack11l1l11_opy_ (u"ࠣࠤᄑ"))
                return
            self.logger.info(bstack11l1l11_opy_ (u"ࠤࡵࡹࡳࡴࡩ࡯ࡩࠣࡿࡱ࡫࡮ࠩࡵࡦࡶ࡮ࡶࡴࡴࡡࡷࡳࡤࡸࡵ࡯ࠫࢀࠤࡸࡩࡲࡪࡲࡷࡷࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࡃࡻࡧ࠰ࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࢀࠤࡨࡵ࡭࡮ࡣࡱࡨࡤࡴࡡ࡮ࡧࡀࠦᄒ") + str(bstack1ll1l1ll111_opy_) + bstack11l1l11_opy_ (u"ࠥࠦᄓ"))
            scripts = [(s, bstack1ll1lll111l_opy_[s]) for s in scripts_to_run if s in bstack1ll1lll111l_opy_]
            for bstack1ll1l1lll11_opy_, bstack1ll1ll1111l_opy_ in scripts:
                try:
                    bstack1l1ll1l111_opy_ = datetime.now()
                    if bstack1ll1l1lll11_opy_ == bstack11l1l11_opy_ (u"ࠦࡸࡩࡡ࡯ࠤᄔ"):
                        result = self.perform_scan(driver, method=bstack1ll1l1ll111_opy_, framework_name=f.framework_name)
                    instance.bstack1ll11lll_opy_(bstack11l1l11_opy_ (u"ࠧࡧ࠱࠲ࡻ࠽ࠦᄕ") + bstack1ll1l1lll11_opy_, datetime.now() - bstack1l1ll1l111_opy_)
                    if isinstance(result, dict) and not result.get(bstack11l1l11_opy_ (u"ࠨࡳࡶࡥࡦࡩࡸࡹࠢᄖ"), True):
                        self.logger.warning(bstack11l1l11_opy_ (u"ࠢࡴ࡭࡬ࡴࠥ࡫ࡸࡦࡥࡸࡸ࡮ࡴࡧࠡࡴࡨࡱࡦ࡯࡮ࡪࡰࡪࠤࡸࡩࡲࡪࡲࡷࡷ࠿ࠦࠢᄗ") + str(result) + bstack11l1l11_opy_ (u"ࠣࠤᄘ"))
                        break
                except Exception as e:
                    self.logger.error(bstack11l1l11_opy_ (u"ࠤࡨࡶࡷࡵࡲࠡࡧࡻࡩࡨࡻࡴࡪࡰࡪࠤࡸࡩࡲࡪࡲࡷࡁࢀࡹࡣࡳ࡫ࡳࡸࡤࡴࡡ࡮ࡧࢀࠤࡪࡸࡲࡰࡴࡀࠦᄙ") + str(e) + bstack11l1l11_opy_ (u"ࠥࠦᄚ"))
        except Exception as e:
            self.logger.error(bstack11l1l11_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡦࡺࡨࡧࡺࡺࡥࠡࡧࡵࡶࡴࡸ࠽ࠣᄛ") + str(e) + bstack11l1l11_opy_ (u"ࠧࠨᄜ"))
    def bstack1ll1lll1l1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1lllllll111_opy_,
        bstack1111l1ll11_opy_: Tuple[bstack1llllll1lll_opy_, bstack1lll111lll1_opy_],
        *args,
        **kwargs,
    ):
        tags = self._1ll1ll111l1_opy_(instance, args)
        capabilities = self.bstack1ll1l1l11l1_opy_.bstack1ll1l1ll1ll_opy_(f, instance, bstack1111l1ll11_opy_, *args, **kwargs)
        self.accessibility = self.bstack1ll1l1lllll_opy_(tags, capabilities)
        if not self.accessibility:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠨ࡯࡯ࡡࡤࡪࡹ࡫ࡲࡠࡶࡨࡷࡹࡀࠠࡢ࠳࠴ࡽࠥࡴ࡯ࡵࠢࡨࡲࡦࡨ࡬ࡦࡦࠥᄝ"))
            return
        driver = self.bstack1ll1l1l11l1_opy_.bstack1ll1ll1ll11_opy_(f, instance, bstack1111l1ll11_opy_, *args, **kwargs)
        test_name = f.bstack11111l1l1l_opy_(instance, TestFramework.bstack1ll1l11l111_opy_)
        if not test_name:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠢࡰࡰࡢࡥ࡫ࡺࡥࡳࡡࡷࡩࡸࡺ࠺ࠡ࡯࡬ࡷࡸ࡯࡮ࡨࠢࡷࡩࡸࡺࠠ࡯ࡣࡰࡩࠧᄞ"))
            return
        test_uuid = f.bstack11111l1l1l_opy_(instance, TestFramework.bstack1ll1lll11l1_opy_)
        if not test_uuid:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠣࡱࡱࡣࡦ࡬ࡴࡦࡴࡢࡸࡪࡹࡴ࠻ࠢࡰ࡭ࡸࡹࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡷࡸ࡭ࡩࠨᄟ"))
            return
        if isinstance(self.bstack1ll1l1l11l1_opy_, bstack1lllll1llll_opy_):
            framework_name = bstack11l1l11_opy_ (u"ࠩࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭ᄠ")
        else:
            framework_name = bstack11l1l11_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱࠬᄡ")
        self.bstack1ll11111l_opy_(driver, test_name, framework_name, test_uuid)
    def perform_scan(self, driver: object, method: Union[None, str], framework_name: str):
        bstack1ll1ll1l1l1_opy_ = bstack1lll1llll1l_opy_.bstack1ll1ll1lll1_opy_(EVENTS.bstack1l111l1l11_opy_.value)
        if not self.accessibility:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠦࡵ࡫ࡲࡧࡱࡵࡱࡤࡹࡣࡢࡰ࠽ࠤࡦ࠷࠱ࡺࠢࡱࡳࡹࠦࡥ࡯ࡣࡥࡰࡪࡪࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥ࠾ࡽࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࢀࠤࠧᄢ"))
            return
        bstack1l1ll1l111_opy_ = datetime.now()
        bstack1ll1ll1111l_opy_ = self.scripts.get(framework_name, {}).get(bstack11l1l11_opy_ (u"ࠧࡹࡣࡢࡰࠥᄣ"), None)
        if not bstack1ll1ll1111l_opy_:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠨࡰࡦࡴࡩࡳࡷࡳ࡟ࡴࡥࡤࡲ࠿ࠦ࡭ࡪࡵࡶ࡭ࡳ࡭ࠠࠨࡵࡦࡥࡳ࠭ࠠࡴࡥࡵ࡭ࡵࡺࠠࡧࡱࡵࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࡂࠨᄤ") + str(framework_name) + bstack11l1l11_opy_ (u"ࠢࠡࠤᄥ"))
            return
        instance = bstack11111ll1l1_opy_.bstack11111ll111_opy_(driver)
        if instance:
            if not bstack11111ll1l1_opy_.bstack11111l1l1l_opy_(instance, bstack1lllll11l11_opy_.bstack1ll1ll11111_opy_, False):
                bstack11111ll1l1_opy_.bstack1111111l1l_opy_(instance, bstack1lllll11l11_opy_.bstack1ll1ll11111_opy_, True)
            else:
                self.logger.info(bstack11l1l11_opy_ (u"ࠣࡲࡨࡶ࡫ࡵࡲ࡮ࡡࡶࡧࡦࡴ࠺ࠡࡣ࡯ࡶࡪࡧࡤࡺࠢ࡬ࡲࠥࡶࡲࡰࡩࡵࡩࡸࡹࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥ࠾ࡽࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࢀࠤࡲ࡫ࡴࡩࡱࡧࡁࠧᄦ") + str(method) + bstack11l1l11_opy_ (u"ࠤࠥᄧ"))
                return
        self.logger.info(bstack11l1l11_opy_ (u"ࠥࡴࡪࡸࡦࡰࡴࡰࡣࡸࡩࡡ࡯࠼ࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࡁࢀ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࢃࠠ࡮ࡧࡷ࡬ࡴࡪ࠽ࠣᄨ") + str(method) + bstack11l1l11_opy_ (u"ࠦࠧᄩ"))
        if framework_name == bstack11l1l11_opy_ (u"ࠬࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩᄪ"):
            result = self.bstack1ll1l1l11l1_opy_.bstack1ll1l1l1l1l_opy_(driver, bstack1ll1ll1111l_opy_)
        else:
            result = driver.execute_async_script(bstack1ll1ll1111l_opy_, {bstack11l1l11_opy_ (u"ࠨ࡭ࡦࡶ࡫ࡳࡩࠨᄫ"): method if method else bstack11l1l11_opy_ (u"ࠢࠣᄬ")})
        bstack1lll1llll1l_opy_.end(EVENTS.bstack1l111l1l11_opy_.value, bstack1ll1ll1l1l1_opy_+bstack11l1l11_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣᄭ"), bstack1ll1ll1l1l1_opy_+bstack11l1l11_opy_ (u"ࠤ࠽ࡩࡳࡪࠢᄮ"), True, None, command=method)
        if instance:
            bstack11111ll1l1_opy_.bstack1111111l1l_opy_(instance, bstack1lllll11l11_opy_.bstack1ll1ll11111_opy_, False)
            instance.bstack1ll11lll_opy_(bstack11l1l11_opy_ (u"ࠥࡥ࠶࠷ࡹ࠻ࡲࡨࡶ࡫ࡵࡲ࡮ࡡࡶࡧࡦࡴࠢᄯ"), datetime.now() - bstack1l1ll1l111_opy_)
        return result
    @measure(event_name=EVENTS.bstack1ll1l1lll1_opy_, stage=STAGE.bstack1l1ll1lll_opy_)
    def get_accessibility_results(self, driver: object, framework_name):
        if not self.accessibility:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠦ࡬࡫ࡴࡠࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡠࡴࡨࡷࡺࡲࡴࡴ࠼ࠣࡥ࠶࠷ࡹࠡࡰࡲࡸࠥ࡫࡮ࡢࡤ࡯ࡩࡩࠨᄰ"))
            return
        bstack1ll1ll1111l_opy_ = self.scripts.get(framework_name, {}).get(bstack11l1l11_opy_ (u"ࠧ࡭ࡥࡵࡔࡨࡷࡺࡲࡴࡴࠤᄱ"), None)
        if not bstack1ll1ll1111l_opy_:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠨ࡭ࡪࡵࡶ࡭ࡳ࡭ࠠࠨࡩࡨࡸࡗ࡫ࡳࡶ࡮ࡷࡷࠬࠦࡳࡤࡴ࡬ࡴࡹࠦࡦࡰࡴࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࡁࠧᄲ") + str(framework_name) + bstack11l1l11_opy_ (u"ࠢࠣᄳ"))
            return
        self.perform_scan(driver, method=None, framework_name=framework_name)
        bstack1l1ll1l111_opy_ = datetime.now()
        if framework_name == bstack11l1l11_opy_ (u"ࠨࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬᄴ"):
            result = self.bstack1ll1l1l11l1_opy_.bstack1ll1l1l1l1l_opy_(driver, bstack1ll1ll1111l_opy_)
        else:
            result = driver.execute_async_script(bstack1ll1ll1111l_opy_)
        instance = bstack11111ll1l1_opy_.bstack11111ll111_opy_(driver)
        if instance:
            instance.bstack1ll11lll_opy_(bstack11l1l11_opy_ (u"ࠤࡤ࠵࠶ࡿ࠺ࡨࡧࡷࡣࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡣࡷ࡫ࡳࡶ࡮ࡷࡷࠧᄵ"), datetime.now() - bstack1l1ll1l111_opy_)
        return result
    @measure(event_name=EVENTS.bstack1lll1l11ll_opy_, stage=STAGE.bstack1l1ll1lll_opy_)
    def get_accessibility_results_summary(self, driver: object, framework_name):
        if not self.accessibility:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡳࡧࡶࡹࡱࡺࡳࡠࡵࡸࡱࡲࡧࡲࡺ࠼ࠣࡥ࠶࠷ࡹࠡࡰࡲࡸࠥ࡫࡮ࡢࡤ࡯ࡩࡩࠨᄶ"))
            return
        bstack1ll1ll1111l_opy_ = self.scripts.get(framework_name, {}).get(bstack11l1l11_opy_ (u"ࠦ࡬࡫ࡴࡓࡧࡶࡹࡱࡺࡳࡔࡷࡰࡱࡦࡸࡹࠣᄷ"), None)
        if not bstack1ll1ll1111l_opy_:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠧࡳࡩࡴࡵ࡬ࡲ࡬ࠦࠧࡨࡧࡷࡖࡪࡹࡵ࡭ࡶࡶࡗࡺࡳ࡭ࡢࡴࡼࠫࠥࡹࡣࡳ࡫ࡳࡸࠥ࡬࡯ࡳࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࡀࠦᄸ") + str(framework_name) + bstack11l1l11_opy_ (u"ࠨࠢᄹ"))
            return
        self.perform_scan(driver, method=None, framework_name=framework_name)
        bstack1l1ll1l111_opy_ = datetime.now()
        if framework_name == bstack11l1l11_opy_ (u"ࠧࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠫᄺ"):
            result = self.bstack1ll1l1l11l1_opy_.bstack1ll1l1l1l1l_opy_(driver, bstack1ll1ll1111l_opy_)
        else:
            result = driver.execute_async_script(bstack1ll1ll1111l_opy_)
        instance = bstack11111ll1l1_opy_.bstack11111ll111_opy_(driver)
        if instance:
            instance.bstack1ll11lll_opy_(bstack11l1l11_opy_ (u"ࠣࡣ࠴࠵ࡾࡀࡧࡦࡶࡢࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡢࡶࡪࡹࡵ࡭ࡶࡶࡣࡸࡻ࡭࡮ࡣࡵࡽࠧᄻ"), datetime.now() - bstack1l1ll1l111_opy_)
        return result
    @measure(event_name=EVENTS.bstack1ll1l1l1ll1_opy_, stage=STAGE.bstack1l1ll1lll_opy_)
    def bstack1ll1ll1llll_opy_(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        hub_url: str,
    ):
        self.bstack1ll1l1111l1_opy_()
        req = structs.AccessibilityConfigRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.hub_url = hub_url
        try:
            r = self.bstack1lll11lll1l_opy_.AccessibilityConfig(req)
            if not r.success:
                self.logger.debug(bstack11l1l11_opy_ (u"ࠤࡵࡩࡨ࡫ࡩࡷࡧࡧࠤ࡫ࡸ࡯࡮ࠢࡶࡩࡷࡼࡥࡳ࠼ࠣࠦᄼ") + str(r) + bstack11l1l11_opy_ (u"ࠥࠦᄽ"))
            else:
                self.bstack1ll1l11lll1_opy_(framework_name, r)
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11l1l11_opy_ (u"ࠦࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤᄾ") + str(e) + bstack11l1l11_opy_ (u"ࠧࠨᄿ"))
            traceback.print_exc()
            raise e
    def bstack1ll1l11lll1_opy_(self, framework_name: str, result: structs.AccessibilityConfigResponse) -> bool:
        if not result.success or not result.accessibility.success:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠨ࡬ࡰࡣࡧࡣࡨࡵ࡮ࡧ࡫ࡪ࠾ࠥࡧ࠱࠲ࡻࠣࡲࡴࡺࠠࡧࡱࡸࡲࡩࠨᅀ"))
            return False
        if result.accessibility.options:
            options = result.accessibility.options
            if options.scripts:
                self.scripts[framework_name] = {row.name: row.command for row in options.scripts}
            if options.commands_to_wrap and options.commands_to_wrap.commands:
                scripts_to_run = [s for s in options.commands_to_wrap.scripts_to_run]
                if not scripts_to_run:
                    return False
                bstack1ll1l1l1111_opy_ = dict()
                for command in options.commands_to_wrap.commands:
                    if command.library == self.bstack1ll1l111l1l_opy_ and command.module == self.bstack1ll1l11l1ll_opy_:
                        if command.method and not command.method in bstack1ll1l1l1111_opy_:
                            bstack1ll1l1l1111_opy_[command.method] = dict()
                        if command.name and not command.name in bstack1ll1l1l1111_opy_[command.method]:
                            bstack1ll1l1l1111_opy_[command.method][command.name] = list()
                        bstack1ll1l1l1111_opy_[command.method][command.name].extend(scripts_to_run)
                self.commands[framework_name] = bstack1ll1l1l1111_opy_
        return bool(self.commands.get(framework_name, None))
    def bstack1ll1ll11ll1_opy_(
        self,
        f: bstack1lll1l11ll1_opy_,
        exec: Tuple[bstack11111l11ll_opy_, str],
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if isinstance(self.bstack1ll1l1l11l1_opy_, bstack1lllll1llll_opy_) and method_name != bstack11l1l11_opy_ (u"ࠧࡤࡱࡱࡲࡪࡩࡴࠨᅁ"):
            return
        if bstack11111ll1l1_opy_.bstack1111111l11_opy_(instance, bstack1lllll11l11_opy_.bstack1ll1ll111ll_opy_):
            return
        if not f.bstack1ll1l1111ll_opy_(instance):
            if not bstack1lllll11l11_opy_.bstack1ll1ll1l11l_opy_:
                self.logger.warning(bstack11l1l11_opy_ (u"ࠣࡣ࠴࠵ࡾࠦࡦ࡭ࡱࡺࠤࡩ࡯ࡳࡢࡤ࡯ࡩࡩࠦࡦࡰࡴࠣࡲࡴࡴ࠭ࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡩ࡯ࡨࡵࡥࠧᅂ"))
                bstack1lllll11l11_opy_.bstack1ll1ll1l11l_opy_ = True
            return
        if f.bstack1ll1l11l1l1_opy_(method_name, *args):
            bstack1ll1l11ll1l_opy_ = False
            desired_capabilities = f.bstack1ll1ll1ll1l_opy_(instance)
            if isinstance(desired_capabilities, dict):
                hub_url = f.bstack1ll1lll1111_opy_(instance)
                platform_index = f.bstack11111l1l1l_opy_(instance, bstack1lll1l11ll1_opy_.bstack1ll1l11llll_opy_, 0)
                bstack1ll1l1l111l_opy_ = datetime.now()
                r = self.bstack1ll1ll1llll_opy_(platform_index, f.framework_name, f.framework_version, hub_url)
                instance.bstack1ll11lll_opy_(bstack11l1l11_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡤࡱࡱࡪ࡮࡭ࠢᅃ"), datetime.now() - bstack1ll1l1l111l_opy_)
                bstack1ll1l11ll1l_opy_ = r.success
            else:
                self.logger.error(bstack11l1l11_opy_ (u"ࠥࡱ࡮ࡹࡳࡪࡰࡪࠤࡩ࡫ࡳࡪࡴࡨࡨࠥࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࡁࠧᅄ") + str(desired_capabilities) + bstack11l1l11_opy_ (u"ࠦࠧᅅ"))
            f.bstack1111111l1l_opy_(instance, bstack1lllll11l11_opy_.bstack1ll1ll111ll_opy_, bstack1ll1l11ll1l_opy_)
    def bstack11lll111_opy_(self, test_tags):
        bstack1ll1ll1llll_opy_ = self.config.get(bstack11l1l11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬᅆ"))
        if not bstack1ll1ll1llll_opy_:
            return True
        try:
            include_tags = bstack1ll1ll1llll_opy_[bstack11l1l11_opy_ (u"࠭ࡩ࡯ࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫᅇ")] if bstack11l1l11_opy_ (u"ࠧࡪࡰࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬᅈ") in bstack1ll1ll1llll_opy_ and isinstance(bstack1ll1ll1llll_opy_[bstack11l1l11_opy_ (u"ࠨ࡫ࡱࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭ᅉ")], list) else []
            exclude_tags = bstack1ll1ll1llll_opy_[bstack11l1l11_opy_ (u"ࠩࡨࡼࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧᅊ")] if bstack11l1l11_opy_ (u"ࠪࡩࡽࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨᅋ") in bstack1ll1ll1llll_opy_ and isinstance(bstack1ll1ll1llll_opy_[bstack11l1l11_opy_ (u"ࠫࡪࡾࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩᅌ")], list) else []
            excluded = any(tag in exclude_tags for tag in test_tags)
            included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
            return not excluded and included
        except Exception as error:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡺࡦࡲࡩࡥࡣࡷ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧࠣࡪࡴࡸࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡣࡧࡩࡳࡷ࡫ࠠࡴࡥࡤࡲࡳ࡯࡮ࡨ࠰ࠣࡉࡷࡸ࡯ࡳࠢ࠽ࠤࠧᅍ") + str(error))
        return False
    def bstack111l1111l_opy_(self, caps):
        try:
            bstack1ll1l111lll_opy_ = caps.get(bstack11l1l11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᅎ"), {}).get(bstack11l1l11_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠫᅏ"), caps.get(bstack11l1l11_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࠨᅐ"), bstack11l1l11_opy_ (u"ࠩࠪᅑ")))
            if bstack1ll1l111lll_opy_:
                self.logger.warning(bstack11l1l11_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡸ࡫࡯ࡰࠥࡸࡵ࡯ࠢࡲࡲࡱࡿࠠࡰࡰࠣࡈࡪࡹ࡫ࡵࡱࡳࠤࡧࡸ࡯ࡸࡵࡨࡶࡸ࠴ࠢᅒ"))
                return False
            browser = caps.get(bstack11l1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩᅓ"), bstack11l1l11_opy_ (u"ࠬ࠭ᅔ")).lower()
            if browser != bstack11l1l11_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ࠭ᅕ"):
                self.logger.warning(bstack11l1l11_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡵࡹࡳࠦ࡯࡯࡮ࡼࠤࡴࡴࠠࡄࡪࡵࡳࡲ࡫ࠠࡣࡴࡲࡻࡸ࡫ࡲࡴ࠰ࠥᅖ"))
                return False
            browser_version = caps.get(bstack11l1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩᅗ"))
            if browser_version and browser_version != bstack11l1l11_opy_ (u"ࠩ࡯ࡥࡹ࡫ࡳࡵࠩᅘ") and int(browser_version.split(bstack11l1l11_opy_ (u"ࠪ࠲ࠬᅙ"))[0]) <= 98:
                self.logger.warning(bstack11l1l11_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦࡲࡶࡰࠣࡳࡳࡲࡹࠡࡱࡱࠤࡈ࡮ࡲࡰ࡯ࡨࠤࡧࡸ࡯ࡸࡵࡨࡶࠥࡼࡥࡳࡵ࡬ࡳࡳࠦࡧࡳࡧࡤࡸࡪࡸࠠࡵࡪࡤࡲࠥ࠿࠸࠯ࠤᅚ"))
                return False
            bstack1ll1lll1l11_opy_ = caps.get(bstack11l1l11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᅛ"), {}).get(bstack11l1l11_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᅜ"))
            if bstack1ll1lll1l11_opy_ and bstack11l1l11_opy_ (u"ࠧ࠮࠯࡫ࡩࡦࡪ࡬ࡦࡵࡶࠫᅝ") in bstack1ll1lll1l11_opy_.get(bstack11l1l11_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ᅞ"), []):
                self.logger.warning(bstack11l1l11_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡳࡵࡴࠡࡴࡸࡲࠥࡵ࡮ࠡ࡮ࡨ࡫ࡦࡩࡹࠡࡪࡨࡥࡩࡲࡥࡴࡵࠣࡱࡴࡪࡥ࠯ࠢࡖࡻ࡮ࡺࡣࡩࠢࡷࡳࠥࡴࡥࡸࠢ࡫ࡩࡦࡪ࡬ࡦࡵࡶࠤࡲࡵࡤࡦࠢࡲࡶࠥࡧࡶࡰ࡫ࡧࠤࡺࡹࡩ࡯ࡩࠣ࡬ࡪࡧࡤ࡭ࡧࡶࡷࠥࡳ࡯ࡥࡧ࠱ࠦᅟ"))
                return False
            return True
        except Exception as error:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡹࡥࡱ࡯ࡤࡢࡶࡨࠤࡦ࠷࠱ࡺࠢࡶࡹࡵࡶ࡯ࡳࡶࠣ࠾ࠧᅠ") + str(error))
            return False
    def bstack1ll11111l_opy_(self, driver: object, name: str, framework_name: str, test_uuid: str):
        bstack1ll1ll1l1l1_opy_ = None
        try:
            bstack1ll1l1lll1l_opy_ = {
                bstack11l1l11_opy_ (u"ࠫࡹ࡮ࡔࡦࡵࡷࡖࡺࡴࡕࡶ࡫ࡧࠫᅡ"): test_uuid,
                bstack11l1l11_opy_ (u"ࠬࡺࡨࡃࡷ࡬ࡰࡩ࡛ࡵࡪࡦࠪᅢ"): os.environ.get(bstack11l1l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫᅣ"), bstack11l1l11_opy_ (u"ࠧࠨᅤ")),
                bstack11l1l11_opy_ (u"ࠨࡶ࡫ࡎࡼࡺࡔࡰ࡭ࡨࡲࠬᅥ"): os.environ.get(bstack11l1l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭ᅦ"), bstack11l1l11_opy_ (u"ࠪࠫᅧ"))
            }
            self.logger.debug(bstack11l1l11_opy_ (u"ࠫࡕ࡫ࡲࡧࡱࡵࡱ࡮ࡴࡧࠡࡵࡦࡥࡳࠦࡢࡦࡨࡲࡶࡪࠦࡳࡢࡸ࡬ࡲ࡬ࠦࡲࡦࡵࡸࡰࡹࡹࠧᅨ") + str(bstack1ll1l1lll1l_opy_))
            self.perform_scan(driver, name, framework_name=framework_name)
            bstack1ll1ll1111l_opy_ = self.scripts.get(framework_name, {}).get(bstack11l1l11_opy_ (u"ࠧࡹࡡࡷࡧࡕࡩࡸࡻ࡬ࡵࡵࠥᅩ"), None)
            if not bstack1ll1ll1111l_opy_:
                self.logger.debug(bstack11l1l11_opy_ (u"ࠨࡰࡦࡴࡩࡳࡷࡳ࡟ࡴࡥࡤࡲ࠿ࠦ࡭ࡪࡵࡶ࡭ࡳ࡭ࠠࠨࡵࡤࡺࡪࡘࡥࡴࡷ࡯ࡸࡸ࠭ࠠࡴࡥࡵ࡭ࡵࡺࠠࡧࡱࡵࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࡂࠨᅪ") + str(framework_name) + bstack11l1l11_opy_ (u"ࠢࠡࠤᅫ"))
                return
            bstack1ll1ll1l1l1_opy_ = bstack1lll1llll1l_opy_.bstack1ll1ll1lll1_opy_(EVENTS.bstack1ll1l1l11ll_opy_.value)
            self.bstack1ll1l111ll1_opy_(driver, bstack1ll1ll1111l_opy_, bstack1ll1l1lll1l_opy_, framework_name)
            self.logger.info(bstack11l1l11_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡶࡨࡷࡹ࡯࡮ࡨࠢࡩࡳࡷࠦࡴࡩ࡫ࡶࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫ࠠࡩࡣࡶࠤࡪࡴࡤࡦࡦ࠱ࠦᅬ"))
            bstack1lll1llll1l_opy_.end(EVENTS.bstack1ll1l1l11ll_opy_.value, bstack1ll1ll1l1l1_opy_+bstack11l1l11_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᅭ"), bstack1ll1ll1l1l1_opy_+bstack11l1l11_opy_ (u"ࠥ࠾ࡪࡴࡤࠣᅮ"), True, None, command=bstack11l1l11_opy_ (u"ࠫࡸࡧࡶࡦࡔࡨࡷࡺࡲࡴࡴࠩᅯ"),test_name=name)
        except Exception as bstack1ll1l111l11_opy_:
            self.logger.error(bstack11l1l11_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡸࡥࡴࡷ࡯ࡸࡸࠦࡣࡰࡷ࡯ࡨࠥࡴ࡯ࡵࠢࡥࡩࠥࡶࡲࡰࡥࡨࡷࡸ࡫ࡤࠡࡨࡲࡶࠥࡺࡨࡦࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩ࠿ࠦࠢᅰ") + bstack11l1l11_opy_ (u"ࠨࡳࡵࡴࠫࡴࡦࡺࡨࠪࠤᅱ") + bstack11l1l11_opy_ (u"ࠢࠡࡇࡵࡶࡴࡸࠠ࠻ࠤᅲ") + str(bstack1ll1l111l11_opy_))
            bstack1lll1llll1l_opy_.end(EVENTS.bstack1ll1l1l11ll_opy_.value, bstack1ll1ll1l1l1_opy_+bstack11l1l11_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣᅳ"), bstack1ll1ll1l1l1_opy_+bstack11l1l11_opy_ (u"ࠤ࠽ࡩࡳࡪࠢᅴ"), False, bstack1ll1l111l11_opy_, command=bstack11l1l11_opy_ (u"ࠪࡷࡦࡼࡥࡓࡧࡶࡹࡱࡺࡳࠨᅵ"),test_name=name)
    def bstack1ll1l111ll1_opy_(self, driver, bstack1ll1ll1111l_opy_, bstack1ll1l1lll1l_opy_, framework_name):
        if framework_name == bstack11l1l11_opy_ (u"ࠫࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠨᅶ"):
            self.bstack1ll1l1l11l1_opy_.bstack1ll1l1l1l1l_opy_(driver, bstack1ll1ll1111l_opy_, bstack1ll1l1lll1l_opy_)
        else:
            self.logger.debug(driver.execute_async_script(bstack1ll1ll1111l_opy_, bstack1ll1l1lll1l_opy_))
    def _1ll1ll111l1_opy_(self, instance: bstack1lllllll111_opy_, args: Tuple) -> list:
        bstack11l1l11_opy_ (u"ࠧࠨࠢࡆࡺࡷࡶࡦࡩࡴࠡࡶࡤ࡫ࡸࠦࡢࡢࡵࡨࡨࠥࡵ࡮ࠡࡶ࡫ࡩࠥࡺࡥࡴࡶࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠴ࠢࠣࠤᅷ")
        if bstack11l1l11_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠪᅸ") in instance.bstack1ll1lll11ll_opy_:
            return args[2].tags if hasattr(args[2], bstack11l1l11_opy_ (u"ࠧࡵࡣࡪࡷࠬᅹ")) else []
        if hasattr(args[0], bstack11l1l11_opy_ (u"ࠨࡱࡺࡲࡤࡳࡡࡳ࡭ࡨࡶࡸ࠭ᅺ")):
            return [marker.name for marker in args[0].own_markers]
        return []
    def bstack1ll1l1lllll_opy_(self, tags, capabilities):
        return self.bstack11lll111_opy_(tags) and self.bstack111l1111l_opy_(capabilities)
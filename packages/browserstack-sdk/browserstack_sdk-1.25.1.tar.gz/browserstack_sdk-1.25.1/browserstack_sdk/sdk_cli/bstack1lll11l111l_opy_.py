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
from datetime import datetime
import os
import threading
from browserstack_sdk.sdk_cli.bstack111111l1ll_opy_ import (
    bstack11111ll1l1_opy_,
    bstack1111l1l1l1_opy_,
    bstack11111lll1l_opy_,
    bstack1llllllllll_opy_,
)
from browserstack_sdk.sdk_cli.bstack1lll1ll11ll_opy_ import bstack1lll1ll1lll_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1lllllll1ll_opy_, bstack1lll1l11l1l_opy_, bstack1lll1l1l1l1_opy_
from typing import Tuple, Dict, Any, List, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1lllll1l1ll_opy_ import bstack1lll1llll11_opy_
from browserstack_sdk.sdk_cli.bstack1lll11111ll_opy_ import bstack1lll1l1l11l_opy_
from browserstack_sdk.sdk_cli.bstack1llll1l11ll_opy_ import bstack1llll1l1l11_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l1l111_opy_ import bstack1llll1l1111_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.bstack1l111l1111_opy_ import bstack1lll111l11l_opy_
import grpc
import traceback
import json
class bstack1ll1lllll1l_opy_(bstack1lll1llll11_opy_):
    bstack1ll1l11ll1l_opy_ = False
    bstack1ll1l1l1l1l_opy_ = bstack1ll1l1_opy_ (u"ࠧࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࠮ࡸࡧࡥࡨࡷ࡯ࡶࡦࡴࠥჹ")
    bstack1ll1l1lllll_opy_ = bstack1ll1l1_opy_ (u"ࠨࡲࡦ࡯ࡲࡸࡪ࠴ࡷࡦࡤࡧࡶ࡮ࡼࡥࡳࠤჺ")
    bstack1ll11lllll1_opy_ = bstack1ll1l1_opy_ (u"ࠢࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡪࡰ࡬ࡸࠧ჻")
    bstack1ll1l11l11l_opy_ = bstack1ll1l1_opy_ (u"ࠣࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡠ࡫ࡶࡣࡸࡩࡡ࡯ࡰ࡬ࡲ࡬ࠨჼ")
    bstack1ll1ll1l11l_opy_ = bstack1ll1l1_opy_ (u"ࠤࡧࡶ࡮ࡼࡥࡳࡡ࡫ࡥࡸࡥࡵࡳ࡮ࠥჽ")
    scripts: Dict[str, Dict[str, str]]
    commands: Dict[str, Dict[str, Dict[str, List[str]]]]
    def __init__(self, bstack1lllll1l11l_opy_, bstack1lll1llllll_opy_):
        super().__init__()
        self.scripts = dict()
        self.commands = dict()
        self.accessibility = False
        if not self.is_enabled():
            return
        self.bstack1ll1l11lll1_opy_ = bstack1lll1llllll_opy_
        bstack1lllll1l11l_opy_.bstack1ll1l11l1l1_opy_((bstack11111ll1l1_opy_.bstack111111l11l_opy_, bstack1111l1l1l1_opy_.PRE), self.bstack1ll1ll111l1_opy_)
        TestFramework.bstack1ll1l11l1l1_opy_((bstack1lllllll1ll_opy_.TEST, bstack1lll1l11l1l_opy_.PRE), self.bstack1ll1l1111ll_opy_)
        TestFramework.bstack1ll1l11l1l1_opy_((bstack1lllllll1ll_opy_.TEST, bstack1lll1l11l1l_opy_.POST), self.bstack1ll1ll1llll_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1ll1l1111ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1l1l1l1_opy_,
        bstack1111l1l11l_opy_: Tuple[bstack1lllllll1ll_opy_, bstack1lll1l11l1l_opy_],
        *args,
        **kwargs,
    ):
        tags = self._1ll1l11l1ll_opy_(instance, args)
        test_framework = f.bstack11111lllll_opy_(instance, TestFramework.bstack1ll1ll1l1ll_opy_)
        if bstack1ll1l1_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠧჾ") in instance.bstack1ll1l1l1111_opy_:
            platform_index = f.bstack11111lllll_opy_(instance, TestFramework.bstack1ll11llll1l_opy_)
            self.accessibility = self.bstack1ll1ll11l1l_opy_(tags, self.config[bstack1ll1l1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧჿ")][platform_index])
        else:
            capabilities = self.bstack1ll1l11lll1_opy_.bstack1ll1ll11111_opy_(f, instance, bstack1111l1l11l_opy_, *args, **kwargs)
            if not capabilities:
                self.logger.debug(bstack1ll1l1_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࠣࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠢࡩࡳࡺࡴࡤࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧᄀ") + str(kwargs) + bstack1ll1l1_opy_ (u"ࠨࠢᄁ"))
                return
            self.accessibility = self.bstack1ll1ll11l1l_opy_(tags, capabilities)
        if self.bstack1ll1l11lll1_opy_.pages and self.bstack1ll1l11lll1_opy_.pages.values():
            bstack1ll1ll11lll_opy_ = list(self.bstack1ll1l11lll1_opy_.pages.values())
            if bstack1ll1ll11lll_opy_ and isinstance(bstack1ll1ll11lll_opy_[0], (list, tuple)) and bstack1ll1ll11lll_opy_[0]:
                bstack1ll1l1l1l11_opy_ = bstack1ll1ll11lll_opy_[0][0]
                if callable(bstack1ll1l1l1l11_opy_):
                    page = bstack1ll1l1l1l11_opy_()
                    def bstack1ll11l1ll1_opy_():
                        self.get_accessibility_results(page, bstack1ll1l1_opy_ (u"ࠢࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦᄂ"))
                    def bstack1ll1l111ll1_opy_():
                        self.get_accessibility_results_summary(page, bstack1ll1l1_opy_ (u"ࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧᄃ"))
                    setattr(page, bstack1ll1l1_opy_ (u"ࠤࡪࡩࡹࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡗ࡫ࡳࡶ࡮ࡷࡷࠧᄄ"), bstack1ll11l1ll1_opy_)
                    setattr(page, bstack1ll1l1_opy_ (u"ࠥ࡫ࡪࡺࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡘࡥࡴࡷ࡯ࡸࡘࡻ࡭࡮ࡣࡵࡽࠧᄅ"), bstack1ll1l111ll1_opy_)
        self.logger.debug(bstack1ll1l1_opy_ (u"ࠦࡸ࡮࡯ࡶ࡮ࡧࠤࡷࡻ࡮ࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡸࡤࡰࡺ࡫࠽ࠣᄆ") + str(self.accessibility) + bstack1ll1l1_opy_ (u"ࠧࠨᄇ"))
    def bstack1ll1ll111l1_opy_(
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
            bstack1ll11l1l1_opy_ = datetime.now()
            self.bstack1ll1ll1111l_opy_(f, exec, *args, **kwargs)
            instance, method_name = exec
            instance.bstack11lll1l111_opy_(bstack1ll1l1_opy_ (u"ࠨࡡ࠲࠳ࡼ࠾࡮ࡴࡩࡵࡡࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡡࡦࡳࡳ࡬ࡩࡨࠤᄈ"), datetime.now() - bstack1ll11l1l1_opy_)
            if (
                not f.bstack1ll1l1llll1_opy_(method_name)
                or f.bstack1ll1l111lll_opy_(method_name, *args)
                or f.bstack1ll1ll1l111_opy_(method_name, *args)
            ):
                return
            if not f.bstack11111lllll_opy_(instance, bstack1ll1lllll1l_opy_.bstack1ll11lllll1_opy_, False):
                if not bstack1ll1lllll1l_opy_.bstack1ll1l11ll1l_opy_:
                    self.logger.warning(bstack1ll1l1_opy_ (u"ࠢ࡜ࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢ࡭ࡳࡪࡥࡹ࠿ࠥᄉ") + str(f.platform_index) + bstack1ll1l1_opy_ (u"ࠣ࡟ࠣࡥ࠶࠷ࡹࠡࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠠࡩࡣࡹࡩࠥࡴ࡯ࡵࠢࡥࡩࡪࡴࠠࡴࡧࡷࠤ࡫ࡵࡲࠡࡶ࡫࡭ࡸࠦࡳࡦࡵࡶ࡭ࡴࡴࠢᄊ"))
                    bstack1ll1lllll1l_opy_.bstack1ll1l11ll1l_opy_ = True
                return
            bstack1ll1l1ll1ll_opy_ = self.scripts.get(f.framework_name, {})
            if not bstack1ll1l1ll1ll_opy_:
                platform_index = f.bstack11111lllll_opy_(instance, bstack1lll1ll1lll_opy_.bstack1ll11llll1l_opy_, 0)
                self.logger.debug(bstack1ll1l1_opy_ (u"ࠤࡱࡳࠥࡧ࠱࠲ࡻࠣࡷࡨࡸࡩࡱࡶࡶࠤ࡫ࡵࡲࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢ࡭ࡳࡪࡥࡹ࠿ࡾࡴࡱࡧࡴࡧࡱࡵࡱࡤ࡯࡮ࡥࡧࡻࢁࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࡃࠢᄋ") + str(f.framework_name) + bstack1ll1l1_opy_ (u"ࠥࠦᄌ"))
                return
            bstack1ll1l1l11ll_opy_ = f.bstack1ll1l1ll111_opy_(*args)
            if not bstack1ll1l1l11ll_opy_:
                self.logger.debug(bstack1ll1l1_opy_ (u"ࠦࡲ࡯ࡳࡴ࡫ࡱ࡫ࠥࡩ࡯࡮࡯ࡤࡲࡩࡥ࡮ࡢ࡯ࡨࠤ࡫ࡵࡲࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦ࠿ࡾࡪ࠳࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࢃࠠ࡮ࡧࡷ࡬ࡴࡪ࡟࡯ࡣࡰࡩࡂࠨᄍ") + str(method_name) + bstack1ll1l1_opy_ (u"ࠧࠨᄎ"))
                return
            bstack1ll1l1lll1l_opy_ = f.bstack11111lllll_opy_(instance, bstack1ll1lllll1l_opy_.bstack1ll1ll1l11l_opy_, False)
            if bstack1ll1l1l11ll_opy_ == bstack1ll1l1_opy_ (u"ࠨࡧࡦࡶࠥᄏ") and not bstack1ll1l1lll1l_opy_:
                f.bstack1111111111_opy_(instance, bstack1ll1lllll1l_opy_.bstack1ll1ll1l11l_opy_, True)
            if not bstack1ll1l1lll1l_opy_:
                self.logger.debug(bstack1ll1l1_opy_ (u"ࠢ࡯ࡱ࡙ࠣࡗࡒࠠ࡭ࡱࡤࡨࡪࡪࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥ࠾ࡽࡩ࠲࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࢂࠦࡣࡰ࡯ࡰࡥࡳࡪ࡟࡯ࡣࡰࡩࡂࠨᄐ") + str(bstack1ll1l1l11ll_opy_) + bstack1ll1l1_opy_ (u"ࠣࠤᄑ"))
                return
            scripts_to_run = self.commands.get(f.framework_name, {}).get(method_name, {}).get(bstack1ll1l1l11ll_opy_, [])
            if not scripts_to_run:
                self.logger.debug(bstack1ll1l1_opy_ (u"ࠤࡱࡳࠥࡧ࠱࠲ࡻࠣࡷࡨࡸࡩࡱࡶࡶࠤ࡫ࡵࡲࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦ࠿ࡾࡪ࠳࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࢃࠠࡤࡱࡰࡱࡦࡴࡤࡠࡰࡤࡱࡪࡃࠢᄒ") + str(bstack1ll1l1l11ll_opy_) + bstack1ll1l1_opy_ (u"ࠥࠦᄓ"))
                return
            self.logger.info(bstack1ll1l1_opy_ (u"ࠦࡷࡻ࡮࡯࡫ࡱ࡫ࠥࢁ࡬ࡦࡰࠫࡷࡨࡸࡩࡱࡶࡶࡣࡹࡵ࡟ࡳࡷࡱ࠭ࢂࠦࡳࡤࡴ࡬ࡴࡹࡹࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥ࠾ࡽࡩ࠲࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࢂࠦࡣࡰ࡯ࡰࡥࡳࡪ࡟࡯ࡣࡰࡩࡂࠨᄔ") + str(bstack1ll1l1l11ll_opy_) + bstack1ll1l1_opy_ (u"ࠧࠨᄕ"))
            scripts = [(s, bstack1ll1l1ll1ll_opy_[s]) for s in scripts_to_run if s in bstack1ll1l1ll1ll_opy_]
            for bstack1ll1l1ll11l_opy_, bstack1ll1ll11l11_opy_ in scripts:
                try:
                    bstack1ll11l1l1_opy_ = datetime.now()
                    if bstack1ll1l1ll11l_opy_ == bstack1ll1l1_opy_ (u"ࠨࡳࡤࡣࡱࠦᄖ"):
                        result = self.perform_scan(driver, method=bstack1ll1l1l11ll_opy_, framework_name=f.framework_name)
                    instance.bstack11lll1l111_opy_(bstack1ll1l1_opy_ (u"ࠢࡢ࠳࠴ࡽ࠿ࠨᄗ") + bstack1ll1l1ll11l_opy_, datetime.now() - bstack1ll11l1l1_opy_)
                    if isinstance(result, dict) and not result.get(bstack1ll1l1_opy_ (u"ࠣࡵࡸࡧࡨ࡫ࡳࡴࠤᄘ"), True):
                        self.logger.warning(bstack1ll1l1_opy_ (u"ࠤࡶ࡯࡮ࡶࠠࡦࡺࡨࡧࡺࡺࡩ࡯ࡩࠣࡶࡪࡳࡡࡪࡰ࡬ࡲ࡬ࠦࡳࡤࡴ࡬ࡴࡹࡹ࠺ࠡࠤᄙ") + str(result) + bstack1ll1l1_opy_ (u"ࠥࠦᄚ"))
                        break
                except Exception as e:
                    self.logger.error(bstack1ll1l1_opy_ (u"ࠦࡪࡸࡲࡰࡴࠣࡩࡽ࡫ࡣࡶࡶ࡬ࡲ࡬ࠦࡳࡤࡴ࡬ࡴࡹࡃࡻࡴࡥࡵ࡭ࡵࡺ࡟࡯ࡣࡰࡩࢂࠦࡥࡳࡴࡲࡶࡂࠨᄛ") + str(e) + bstack1ll1l1_opy_ (u"ࠧࠨᄜ"))
        except Exception as e:
            self.logger.error(bstack1ll1l1_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡨࡼࡪࡩࡵࡵࡧࠣࡩࡷࡸ࡯ࡳ࠿ࠥᄝ") + str(e) + bstack1ll1l1_opy_ (u"ࠢࠣᄞ"))
    def bstack1ll1ll1llll_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1l1l1l1_opy_,
        bstack1111l1l11l_opy_: Tuple[bstack1lllllll1ll_opy_, bstack1lll1l11l1l_opy_],
        *args,
        **kwargs,
    ):
        tags = self._1ll1l11l1ll_opy_(instance, args)
        capabilities = self.bstack1ll1l11lll1_opy_.bstack1ll1ll11111_opy_(f, instance, bstack1111l1l11l_opy_, *args, **kwargs)
        self.accessibility = self.bstack1ll1ll11l1l_opy_(tags, capabilities)
        if not self.accessibility:
            self.logger.debug(bstack1ll1l1_opy_ (u"ࠣࡱࡱࡣࡦ࡬ࡴࡦࡴࡢࡸࡪࡹࡴ࠻ࠢࡤ࠵࠶ࡿࠠ࡯ࡱࡷࠤࡪࡴࡡࡣ࡮ࡨࡨࠧᄟ"))
            return
        driver = self.bstack1ll1l11lll1_opy_.bstack1ll1lll111l_opy_(f, instance, bstack1111l1l11l_opy_, *args, **kwargs)
        test_name = f.bstack11111lllll_opy_(instance, TestFramework.bstack1ll1ll1l1l1_opy_)
        if not test_name:
            self.logger.debug(bstack1ll1l1_opy_ (u"ࠤࡲࡲࡤࡧࡦࡵࡧࡵࡣࡹ࡫ࡳࡵ࠼ࠣࡱ࡮ࡹࡳࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡱࡥࡲ࡫ࠢᄠ"))
            return
        test_uuid = f.bstack11111lllll_opy_(instance, TestFramework.bstack1ll1ll1ll11_opy_)
        if not test_uuid:
            self.logger.debug(bstack1ll1l1_opy_ (u"ࠥࡳࡳࡥࡡࡧࡶࡨࡶࡤࡺࡥࡴࡶ࠽ࠤࡲ࡯ࡳࡴ࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡹࡺ࡯ࡤࠣᄡ"))
            return
        if isinstance(self.bstack1ll1l11lll1_opy_, bstack1llll1l1l11_opy_):
            framework_name = bstack1ll1l1_opy_ (u"ࠫࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠨᄢ")
        else:
            framework_name = bstack1ll1l1_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠧᄣ")
        self.bstack1111l1l11_opy_(driver, test_name, framework_name, test_uuid)
    def perform_scan(self, driver: object, method: Union[None, str], framework_name: str):
        bstack1ll1l1l111l_opy_ = bstack1lll111l11l_opy_.bstack1ll1ll111ll_opy_(EVENTS.bstack1l11l11ll1_opy_.value)
        if not self.accessibility:
            self.logger.debug(bstack1ll1l1_opy_ (u"ࠨࡰࡦࡴࡩࡳࡷࡳ࡟ࡴࡥࡤࡲ࠿ࠦࡡ࠲࠳ࡼࠤࡳࡵࡴࠡࡧࡱࡥࡧࡲࡥࡥࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࡀࡿ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࢂࠦࠢᄤ"))
            return
        bstack1ll11l1l1_opy_ = datetime.now()
        bstack1ll1ll11l11_opy_ = self.scripts.get(framework_name, {}).get(bstack1ll1l1_opy_ (u"ࠢࡴࡥࡤࡲࠧᄥ"), None)
        if not bstack1ll1ll11l11_opy_:
            self.logger.debug(bstack1ll1l1_opy_ (u"ࠣࡲࡨࡶ࡫ࡵࡲ࡮ࡡࡶࡧࡦࡴ࠺ࠡ࡯࡬ࡷࡸ࡯࡮ࡨࠢࠪࡷࡨࡧ࡮ࠨࠢࡶࡧࡷ࡯ࡰࡵࠢࡩࡳࡷࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫࠽ࠣᄦ") + str(framework_name) + bstack1ll1l1_opy_ (u"ࠤࠣࠦᄧ"))
            return
        instance = bstack11111lll1l_opy_.bstack11111l1111_opy_(driver)
        if instance:
            if not bstack11111lll1l_opy_.bstack11111lllll_opy_(instance, bstack1ll1lllll1l_opy_.bstack1ll1l11l11l_opy_, False):
                bstack11111lll1l_opy_.bstack1111111111_opy_(instance, bstack1ll1lllll1l_opy_.bstack1ll1l11l11l_opy_, True)
            else:
                self.logger.info(bstack1ll1l1_opy_ (u"ࠥࡴࡪࡸࡦࡰࡴࡰࡣࡸࡩࡡ࡯࠼ࠣࡥࡱࡸࡥࡢࡦࡼࠤ࡮ࡴࠠࡱࡴࡲ࡫ࡷ࡫ࡳࡴࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࡀࡿ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࢂࠦ࡭ࡦࡶ࡫ࡳࡩࡃࠢᄨ") + str(method) + bstack1ll1l1_opy_ (u"ࠦࠧᄩ"))
                return
        self.logger.info(bstack1ll1l1_opy_ (u"ࠧࡶࡥࡳࡨࡲࡶࡲࡥࡳࡤࡣࡱ࠾ࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࡃࡻࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥࡾࠢࡰࡩࡹ࡮࡯ࡥ࠿ࠥᄪ") + str(method) + bstack1ll1l1_opy_ (u"ࠨࠢᄫ"))
        if framework_name == bstack1ll1l1_opy_ (u"ࠧࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠫᄬ"):
            result = self.bstack1ll1l11lll1_opy_.bstack1ll1l111l11_opy_(driver, bstack1ll1ll11l11_opy_)
        else:
            result = driver.execute_async_script(bstack1ll1ll11l11_opy_, {bstack1ll1l1_opy_ (u"ࠣ࡯ࡨࡸ࡭ࡵࡤࠣᄭ"): method if method else bstack1ll1l1_opy_ (u"ࠤࠥᄮ")})
        bstack1lll111l11l_opy_.end(EVENTS.bstack1l11l11ll1_opy_.value, bstack1ll1l1l111l_opy_+bstack1ll1l1_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥᄯ"), bstack1ll1l1l111l_opy_+bstack1ll1l1_opy_ (u"ࠦ࠿࡫࡮ࡥࠤᄰ"), True, None, command=method)
        if instance:
            bstack11111lll1l_opy_.bstack1111111111_opy_(instance, bstack1ll1lllll1l_opy_.bstack1ll1l11l11l_opy_, False)
            instance.bstack11lll1l111_opy_(bstack1ll1l1_opy_ (u"ࠧࡧ࠱࠲ࡻ࠽ࡴࡪࡸࡦࡰࡴࡰࡣࡸࡩࡡ࡯ࠤᄱ"), datetime.now() - bstack1ll11l1l1_opy_)
        return result
    @measure(event_name=EVENTS.bstack1111l1lll_opy_, stage=STAGE.bstack1llll1l1_opy_)
    def get_accessibility_results(self, driver: object, framework_name):
        if not self.accessibility:
            self.logger.debug(bstack1ll1l1_opy_ (u"ࠨࡧࡦࡶࡢࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡢࡶࡪࡹࡵ࡭ࡶࡶ࠾ࠥࡧ࠱࠲ࡻࠣࡲࡴࡺࠠࡦࡰࡤࡦࡱ࡫ࡤࠣᄲ"))
            return
        bstack1ll1ll11l11_opy_ = self.scripts.get(framework_name, {}).get(bstack1ll1l1_opy_ (u"ࠢࡨࡧࡷࡖࡪࡹࡵ࡭ࡶࡶࠦᄳ"), None)
        if not bstack1ll1ll11l11_opy_:
            self.logger.debug(bstack1ll1l1_opy_ (u"ࠣ࡯࡬ࡷࡸ࡯࡮ࡨࠢࠪ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࠧࠡࡵࡦࡶ࡮ࡶࡴࠡࡨࡲࡶࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࡃࠢᄴ") + str(framework_name) + bstack1ll1l1_opy_ (u"ࠤࠥᄵ"))
            return
        self.perform_scan(driver, method=None, framework_name=framework_name)
        bstack1ll11l1l1_opy_ = datetime.now()
        if framework_name == bstack1ll1l1_opy_ (u"ࠪࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠧᄶ"):
            result = self.bstack1ll1l11lll1_opy_.bstack1ll1l111l11_opy_(driver, bstack1ll1ll11l11_opy_)
        else:
            result = driver.execute_async_script(bstack1ll1ll11l11_opy_)
        instance = bstack11111lll1l_opy_.bstack11111l1111_opy_(driver)
        if instance:
            instance.bstack11lll1l111_opy_(bstack1ll1l1_opy_ (u"ࠦࡦ࠷࠱ࡺ࠼ࡪࡩࡹࡥࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡥࡲࡦࡵࡸࡰࡹࡹࠢᄷ"), datetime.now() - bstack1ll11l1l1_opy_)
        return result
    @measure(event_name=EVENTS.bstack1l1l11l1l1_opy_, stage=STAGE.bstack1llll1l1_opy_)
    def get_accessibility_results_summary(self, driver: object, framework_name):
        if not self.accessibility:
            self.logger.debug(bstack1ll1l1_opy_ (u"ࠧ࡭ࡥࡵࡡࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡡࡵࡩࡸࡻ࡬ࡵࡵࡢࡷࡺࡳ࡭ࡢࡴࡼ࠾ࠥࡧ࠱࠲ࡻࠣࡲࡴࡺࠠࡦࡰࡤࡦࡱ࡫ࡤࠣᄸ"))
            return
        bstack1ll1ll11l11_opy_ = self.scripts.get(framework_name, {}).get(bstack1ll1l1_opy_ (u"ࠨࡧࡦࡶࡕࡩࡸࡻ࡬ࡵࡵࡖࡹࡲࡳࡡࡳࡻࠥᄹ"), None)
        if not bstack1ll1ll11l11_opy_:
            self.logger.debug(bstack1ll1l1_opy_ (u"ࠢ࡮࡫ࡶࡷ࡮ࡴࡧࠡࠩࡪࡩࡹࡘࡥࡴࡷ࡯ࡸࡸ࡙ࡵ࡮࡯ࡤࡶࡾ࠭ࠠࡴࡥࡵ࡭ࡵࡺࠠࡧࡱࡵࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࡂࠨᄺ") + str(framework_name) + bstack1ll1l1_opy_ (u"ࠣࠤᄻ"))
            return
        self.perform_scan(driver, method=None, framework_name=framework_name)
        bstack1ll11l1l1_opy_ = datetime.now()
        if framework_name == bstack1ll1l1_opy_ (u"ࠩࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭ᄼ"):
            result = self.bstack1ll1l11lll1_opy_.bstack1ll1l111l11_opy_(driver, bstack1ll1ll11l11_opy_)
        else:
            result = driver.execute_async_script(bstack1ll1ll11l11_opy_)
        instance = bstack11111lll1l_opy_.bstack11111l1111_opy_(driver)
        if instance:
            instance.bstack11lll1l111_opy_(bstack1ll1l1_opy_ (u"ࠥࡥ࠶࠷ࡹ࠻ࡩࡨࡸࡤࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡤࡸࡥࡴࡷ࡯ࡸࡸࡥࡳࡶ࡯ࡰࡥࡷࡿࠢᄽ"), datetime.now() - bstack1ll11l1l1_opy_)
        return result
    @measure(event_name=EVENTS.bstack1ll1l11llll_opy_, stage=STAGE.bstack1llll1l1_opy_)
    def bstack1ll1l111111_opy_(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        hub_url: str,
    ):
        self.bstack1ll1l11ll11_opy_()
        req = structs.AccessibilityConfigRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.hub_url = hub_url
        try:
            r = self.bstack1llllll1ll1_opy_.AccessibilityConfig(req)
            if not r.success:
                self.logger.debug(bstack1ll1l1_opy_ (u"ࠦࡷ࡫ࡣࡦ࡫ࡹࡩࡩࠦࡦࡳࡱࡰࠤࡸ࡫ࡲࡷࡧࡵ࠾ࠥࠨᄾ") + str(r) + bstack1ll1l1_opy_ (u"ࠧࠨᄿ"))
            else:
                self.bstack1ll1l1l1lll_opy_(framework_name, r)
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1ll1l1_opy_ (u"ࠨࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࠦᅀ") + str(e) + bstack1ll1l1_opy_ (u"ࠢࠣᅁ"))
            traceback.print_exc()
            raise e
    def bstack1ll1l1l1lll_opy_(self, framework_name: str, result: structs.AccessibilityConfigResponse) -> bool:
        if not result.success or not result.accessibility.success:
            self.logger.debug(bstack1ll1l1_opy_ (u"ࠣ࡮ࡲࡥࡩࡥࡣࡰࡰࡩ࡭࡬ࡀࠠࡢ࠳࠴ࡽࠥࡴ࡯ࡵࠢࡩࡳࡺࡴࡤࠣᅂ"))
            return False
        if result.accessibility.options:
            options = result.accessibility.options
            if options.scripts:
                self.scripts[framework_name] = {row.name: row.command for row in options.scripts}
            if options.commands_to_wrap and options.commands_to_wrap.commands:
                scripts_to_run = [s for s in options.commands_to_wrap.scripts_to_run]
                if not scripts_to_run:
                    return False
                bstack1ll1l1111l1_opy_ = dict()
                for command in options.commands_to_wrap.commands:
                    if command.library == self.bstack1ll1l1l1l1l_opy_ and command.module == self.bstack1ll1l1lllll_opy_:
                        if command.method and not command.method in bstack1ll1l1111l1_opy_:
                            bstack1ll1l1111l1_opy_[command.method] = dict()
                        if command.name and not command.name in bstack1ll1l1111l1_opy_[command.method]:
                            bstack1ll1l1111l1_opy_[command.method][command.name] = list()
                        bstack1ll1l1111l1_opy_[command.method][command.name].extend(scripts_to_run)
                self.commands[framework_name] = bstack1ll1l1111l1_opy_
        return bool(self.commands.get(framework_name, None))
    def bstack1ll1ll1111l_opy_(
        self,
        f: bstack1lll1ll1lll_opy_,
        exec: Tuple[bstack1llllllllll_opy_, str],
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if isinstance(self.bstack1ll1l11lll1_opy_, bstack1llll1l1l11_opy_) and method_name != bstack1ll1l1_opy_ (u"ࠩࡦࡳࡳࡴࡥࡤࡶࠪᅃ"):
            return
        if bstack11111lll1l_opy_.bstack11111l1l1l_opy_(instance, bstack1ll1lllll1l_opy_.bstack1ll11lllll1_opy_):
            return
        if not f.bstack1ll1l1l1ll1_opy_(instance):
            if not bstack1ll1lllll1l_opy_.bstack1ll1l11ll1l_opy_:
                self.logger.warning(bstack1ll1l1_opy_ (u"ࠥࡥ࠶࠷ࡹࠡࡨ࡯ࡳࡼࠦࡤࡪࡵࡤࡦࡱ࡫ࡤࠡࡨࡲࡶࠥࡴ࡯࡯࠯ࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡ࡫ࡱࡪࡷࡧࠢᅄ"))
                bstack1ll1lllll1l_opy_.bstack1ll1l11ll1l_opy_ = True
            return
        if f.bstack1ll11llllll_opy_(method_name, *args):
            bstack1ll1ll1lll1_opy_ = False
            desired_capabilities = f.bstack1ll1lll1111_opy_(instance)
            if isinstance(desired_capabilities, dict):
                hub_url = f.bstack1ll1l11111l_opy_(instance)
                platform_index = f.bstack11111lllll_opy_(instance, bstack1lll1ll1lll_opy_.bstack1ll11llll1l_opy_, 0)
                bstack1ll1l1lll11_opy_ = datetime.now()
                r = self.bstack1ll1l111111_opy_(platform_index, f.framework_name, f.framework_version, hub_url)
                instance.bstack11lll1l111_opy_(bstack1ll1l1_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡡࡦࡳࡳ࡬ࡩࡨࠤᅅ"), datetime.now() - bstack1ll1l1lll11_opy_)
                bstack1ll1ll1lll1_opy_ = r.success
            else:
                self.logger.error(bstack1ll1l1_opy_ (u"ࠧࡳࡩࡴࡵ࡬ࡲ࡬ࠦࡤࡦࡵ࡬ࡶࡪࡪࠠࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࡃࠢᅆ") + str(desired_capabilities) + bstack1ll1l1_opy_ (u"ࠨࠢᅇ"))
            f.bstack1111111111_opy_(instance, bstack1ll1lllll1l_opy_.bstack1ll11lllll1_opy_, bstack1ll1ll1lll1_opy_)
    def bstack1ll11l1ll_opy_(self, test_tags):
        bstack1ll1l111111_opy_ = self.config.get(bstack1ll1l1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧᅈ"))
        if not bstack1ll1l111111_opy_:
            return True
        try:
            include_tags = bstack1ll1l111111_opy_[bstack1ll1l1_opy_ (u"ࠨ࡫ࡱࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭ᅉ")] if bstack1ll1l1_opy_ (u"ࠩ࡬ࡲࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧᅊ") in bstack1ll1l111111_opy_ and isinstance(bstack1ll1l111111_opy_[bstack1ll1l1_opy_ (u"ࠪ࡭ࡳࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨᅋ")], list) else []
            exclude_tags = bstack1ll1l111111_opy_[bstack1ll1l1_opy_ (u"ࠫࡪࡾࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩᅌ")] if bstack1ll1l1_opy_ (u"ࠬ࡫ࡸࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪᅍ") in bstack1ll1l111111_opy_ and isinstance(bstack1ll1l111111_opy_[bstack1ll1l1_opy_ (u"࠭ࡥࡹࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫᅎ")], list) else []
            excluded = any(tag in exclude_tags for tag in test_tags)
            included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
            return not excluded and included
        except Exception as error:
            self.logger.debug(bstack1ll1l1_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡼࡡ࡭࡫ࡧࡥࡹ࡯࡮ࡨࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩࠥ࡬࡯ࡳࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡥࡩ࡫ࡵࡲࡦࠢࡶࡧࡦࡴ࡮ࡪࡰࡪ࠲ࠥࡋࡲࡳࡱࡵࠤ࠿ࠦࠢᅏ") + str(error))
        return False
    def bstack1l11ll1l11_opy_(self, caps):
        try:
            bstack1ll1l1l11l1_opy_ = caps.get(bstack1ll1l1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᅐ"), {}).get(bstack1ll1l1_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪ࠭ᅑ"), caps.get(bstack1ll1l1_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࠪᅒ"), bstack1ll1l1_opy_ (u"ࠫࠬᅓ")))
            if bstack1ll1l1l11l1_opy_:
                self.logger.warning(bstack1ll1l1_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠࡳࡷࡱࠤࡴࡴ࡬ࡺࠢࡲࡲࠥࡊࡥࡴ࡭ࡷࡳࡵࠦࡢࡳࡱࡺࡷࡪࡸࡳ࠯ࠤᅔ"))
                return False
            browser = caps.get(bstack1ll1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫᅕ"), bstack1ll1l1_opy_ (u"ࠧࠨᅖ")).lower()
            if browser != bstack1ll1l1_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࠨᅗ"):
                self.logger.warning(bstack1ll1l1_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡷࡻ࡮ࠡࡱࡱࡰࡾࠦ࡯࡯ࠢࡆ࡬ࡷࡵ࡭ࡦࠢࡥࡶࡴࡽࡳࡦࡴࡶ࠲ࠧᅘ"))
                return False
            browser_version = caps.get(bstack1ll1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫᅙ"))
            if browser_version and browser_version != bstack1ll1l1_opy_ (u"ࠫࡱࡧࡴࡦࡵࡷࠫᅚ") and int(browser_version.split(bstack1ll1l1_opy_ (u"ࠬ࠴ࠧᅛ"))[0]) <= 98:
                self.logger.warning(bstack1ll1l1_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡴࡸࡲࠥࡵ࡮࡭ࡻࠣࡳࡳࠦࡃࡩࡴࡲࡱࡪࠦࡢࡳࡱࡺࡷࡪࡸࠠࡷࡧࡵࡷ࡮ࡵ࡮ࠡࡩࡵࡩࡦࡺࡥࡳࠢࡷ࡬ࡦࡴࠠ࠺࠺࠱ࠦᅜ"))
                return False
            bstack1ll1ll11ll1_opy_ = caps.get(bstack1ll1l1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᅝ"), {}).get(bstack1ll1l1_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᅞ"))
            if bstack1ll1ll11ll1_opy_ and bstack1ll1l1_opy_ (u"ࠩ࠰࠱࡭࡫ࡡࡥ࡮ࡨࡷࡸ࠭ᅟ") in bstack1ll1ll11ll1_opy_.get(bstack1ll1l1_opy_ (u"ࠪࡥࡷ࡭ࡳࠨᅠ"), []):
                self.logger.warning(bstack1ll1l1_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦ࡮ࡰࡶࠣࡶࡺࡴࠠࡰࡰࠣࡰࡪ࡭ࡡࡤࡻࠣ࡬ࡪࡧࡤ࡭ࡧࡶࡷࠥࡳ࡯ࡥࡧ࠱ࠤࡘࡽࡩࡵࡥ࡫ࠤࡹࡵࠠ࡯ࡧࡺࠤ࡭࡫ࡡࡥ࡮ࡨࡷࡸࠦ࡭ࡰࡦࡨࠤࡴࡸࠠࡢࡸࡲ࡭ࡩࠦࡵࡴ࡫ࡱ࡫ࠥ࡮ࡥࡢࡦ࡯ࡩࡸࡹࠠ࡮ࡱࡧࡩ࠳ࠨᅡ"))
                return False
            return True
        except Exception as error:
            self.logger.debug(bstack1ll1l1_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡻࡧ࡬ࡪࡦࡤࡸࡪࠦࡡ࠲࠳ࡼࠤࡸࡻࡰࡱࡱࡵࡸࠥࡀࠢᅢ") + str(error))
            return False
    def bstack1111l1l11_opy_(self, driver: object, name: str, framework_name: str, test_uuid: str):
        bstack1ll1l1l111l_opy_ = None
        try:
            bstack1ll1ll1ll1l_opy_ = {
                bstack1ll1l1_opy_ (u"࠭ࡴࡩࡖࡨࡷࡹࡘࡵ࡯ࡗࡸ࡭ࡩ࠭ᅣ"): test_uuid,
                bstack1ll1l1_opy_ (u"ࠧࡵࡪࡅࡹ࡮ࡲࡤࡖࡷ࡬ࡨࠬᅤ"): os.environ.get(bstack1ll1l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭ᅥ"), bstack1ll1l1_opy_ (u"ࠩࠪᅦ")),
                bstack1ll1l1_opy_ (u"ࠪࡸ࡭ࡐࡷࡵࡖࡲ࡯ࡪࡴࠧᅧ"): os.environ.get(bstack1ll1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨᅨ"), bstack1ll1l1_opy_ (u"ࠬ࠭ᅩ"))
            }
            self.logger.debug(bstack1ll1l1_opy_ (u"࠭ࡐࡦࡴࡩࡳࡷࡳࡩ࡯ࡩࠣࡷࡨࡧ࡮ࠡࡤࡨࡪࡴࡸࡥࠡࡵࡤࡺ࡮ࡴࡧࠡࡴࡨࡷࡺࡲࡴࡴࠩᅪ") + str(bstack1ll1ll1ll1l_opy_))
            self.perform_scan(driver, name, framework_name=framework_name)
            bstack1ll1ll11l11_opy_ = self.scripts.get(framework_name, {}).get(bstack1ll1l1_opy_ (u"ࠢࡴࡣࡹࡩࡗ࡫ࡳࡶ࡮ࡷࡷࠧᅫ"), None)
            if not bstack1ll1ll11l11_opy_:
                self.logger.debug(bstack1ll1l1_opy_ (u"ࠣࡲࡨࡶ࡫ࡵࡲ࡮ࡡࡶࡧࡦࡴ࠺ࠡ࡯࡬ࡷࡸ࡯࡮ࡨࠢࠪࡷࡦࡼࡥࡓࡧࡶࡹࡱࡺࡳࠨࠢࡶࡧࡷ࡯ࡰࡵࠢࡩࡳࡷࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫࠽ࠣᅬ") + str(framework_name) + bstack1ll1l1_opy_ (u"ࠤࠣࠦᅭ"))
                return
            bstack1ll1l1l111l_opy_ = bstack1lll111l11l_opy_.bstack1ll1ll111ll_opy_(EVENTS.bstack1ll1l1ll1l1_opy_.value)
            self.bstack1ll1l111l1l_opy_(driver, bstack1ll1ll11l11_opy_, bstack1ll1ll1ll1l_opy_, framework_name)
            self.logger.info(bstack1ll1l1_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡸࡪࡹࡴࡪࡰࡪࠤ࡫ࡵࡲࠡࡶ࡫࡭ࡸࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦࠢ࡫ࡥࡸࠦࡥ࡯ࡦࡨࡨ࠳ࠨᅮ"))
            bstack1lll111l11l_opy_.end(EVENTS.bstack1ll1l1ll1l1_opy_.value, bstack1ll1l1l111l_opy_+bstack1ll1l1_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦᅯ"), bstack1ll1l1l111l_opy_+bstack1ll1l1_opy_ (u"ࠧࡀࡥ࡯ࡦࠥᅰ"), True, None, command=bstack1ll1l1_opy_ (u"࠭ࡳࡢࡸࡨࡖࡪࡹࡵ࡭ࡶࡶࠫᅱ"),test_name=name)
        except Exception as bstack1ll1l11l111_opy_:
            self.logger.error(bstack1ll1l1_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡳࡧࡶࡹࡱࡺࡳࠡࡥࡲࡹࡱࡪࠠ࡯ࡱࡷࠤࡧ࡫ࠠࡱࡴࡲࡧࡪࡹࡳࡦࡦࠣࡪࡴࡸࠠࡵࡪࡨࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫࠺ࠡࠤᅲ") + bstack1ll1l1_opy_ (u"ࠣࡵࡷࡶ࠭ࡶࡡࡵࡪࠬࠦᅳ") + bstack1ll1l1_opy_ (u"ࠤࠣࡉࡷࡸ࡯ࡳࠢ࠽ࠦᅴ") + str(bstack1ll1l11l111_opy_))
            bstack1lll111l11l_opy_.end(EVENTS.bstack1ll1l1ll1l1_opy_.value, bstack1ll1l1l111l_opy_+bstack1ll1l1_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥᅵ"), bstack1ll1l1l111l_opy_+bstack1ll1l1_opy_ (u"ࠦ࠿࡫࡮ࡥࠤᅶ"), False, bstack1ll1l11l111_opy_, command=bstack1ll1l1_opy_ (u"ࠬࡹࡡࡷࡧࡕࡩࡸࡻ࡬ࡵࡵࠪᅷ"),test_name=name)
    def bstack1ll1l111l1l_opy_(self, driver, bstack1ll1ll11l11_opy_, bstack1ll1ll1ll1l_opy_, framework_name):
        if framework_name == bstack1ll1l1_opy_ (u"࠭ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪᅸ"):
            self.bstack1ll1l11lll1_opy_.bstack1ll1l111l11_opy_(driver, bstack1ll1ll11l11_opy_, bstack1ll1ll1ll1l_opy_)
        else:
            self.logger.debug(driver.execute_async_script(bstack1ll1ll11l11_opy_, bstack1ll1ll1ll1l_opy_))
    def _1ll1l11l1ll_opy_(self, instance: bstack1lll1l1l1l1_opy_, args: Tuple) -> list:
        bstack1ll1l1_opy_ (u"ࠢࠣࠤࡈࡼࡹࡸࡡࡤࡶࠣࡸࡦ࡭ࡳࠡࡤࡤࡷࡪࡪࠠࡰࡰࠣࡸ࡭࡫ࠠࡵࡧࡶࡸࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫࠯ࠤࠥࠦᅹ")
        if bstack1ll1l1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠬᅺ") in instance.bstack1ll1l1l1111_opy_:
            return args[2].tags if hasattr(args[2], bstack1ll1l1_opy_ (u"ࠩࡷࡥ࡬ࡹࠧᅻ")) else []
        if hasattr(args[0], bstack1ll1l1_opy_ (u"ࠪࡳࡼࡴ࡟࡮ࡣࡵ࡯ࡪࡸࡳࠨᅼ")):
            return [marker.name for marker in args[0].own_markers]
        return []
    def bstack1ll1ll11l1l_opy_(self, tags, capabilities):
        return self.bstack1ll11l1ll_opy_(tags) and self.bstack1l11ll1l11_opy_(capabilities)
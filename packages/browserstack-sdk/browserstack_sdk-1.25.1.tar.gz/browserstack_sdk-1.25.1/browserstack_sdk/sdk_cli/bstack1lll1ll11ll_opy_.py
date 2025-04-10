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
import os
import traceback
from typing import Dict, Tuple, Callable, Type, List, Any
from urllib.parse import urlparse
from browserstack_sdk.sdk_cli.bstack111111l1ll_opy_ import (
    bstack11111lll1l_opy_,
    bstack1llllllllll_opy_,
    bstack11111ll1l1_opy_,
    bstack1111l1l1l1_opy_,
)
import copy
from datetime import datetime, timezone, timedelta
from bstack_utils.bstack1l111l1111_opy_ import bstack1lll111l11l_opy_
from bstack_utils.constants import EVENTS
class bstack1lll1ll1lll_opy_(bstack11111lll1l_opy_):
    bstack1l11llllll1_opy_ = bstack1ll1l1_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝ࠨᒲ")
    NAME = bstack1ll1l1_opy_ (u"ࠢࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠤᒳ")
    bstack1l1ll1l11ll_opy_ = bstack1ll1l1_opy_ (u"ࠣࡪࡸࡦࡤࡻࡲ࡭ࠤᒴ")
    bstack1l1ll111l1l_opy_ = bstack1ll1l1_opy_ (u"ࠤࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥࠤᒵ")
    bstack1l1111lll11_opy_ = bstack1ll1l1_opy_ (u"ࠥ࡭ࡳࡶࡵࡵࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣᒶ")
    bstack1l1ll111l11_opy_ = bstack1ll1l1_opy_ (u"ࠦࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠥᒷ")
    bstack1l1l111ll11_opy_ = bstack1ll1l1_opy_ (u"ࠧ࡯ࡳࡠࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡩࡷࡥࠦᒸ")
    bstack1l111l1111l_opy_ = bstack1ll1l1_opy_ (u"ࠨࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠥᒹ")
    bstack1l1111llll1_opy_ = bstack1ll1l1_opy_ (u"ࠢࡦࡰࡧࡩࡩࡥࡡࡵࠤᒺ")
    bstack1ll11llll1l_opy_ = bstack1ll1l1_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢ࡭ࡳࡪࡥࡹࠤᒻ")
    bstack1l1l11l1l1l_opy_ = bstack1ll1l1_opy_ (u"ࠤࡱࡩࡼࡹࡥࡴࡵ࡬ࡳࡳࠨᒼ")
    bstack1l111l11l11_opy_ = bstack1ll1l1_opy_ (u"ࠥ࡫ࡪࡺࠢᒽ")
    bstack1ll1111ll1l_opy_ = bstack1ll1l1_opy_ (u"ࠦࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠣᒾ")
    bstack1l1l11111l1_opy_ = bstack1ll1l1_opy_ (u"ࠧࡽ࠳ࡤࡧࡻࡩࡨࡻࡴࡦࡵࡦࡶ࡮ࡶࡴࠣᒿ")
    bstack1l1l1111l1l_opy_ = bstack1ll1l1_opy_ (u"ࠨࡷ࠴ࡥࡨࡼࡪࡩࡵࡵࡧࡶࡧࡷ࡯ࡰࡵࡣࡶࡽࡳࡩࠢᓀ")
    bstack1l1111lllll_opy_ = bstack1ll1l1_opy_ (u"ࠢࡲࡷ࡬ࡸࠧᓁ")
    bstack1l111l111l1_opy_: Dict[str, List[Callable]] = dict()
    bstack1l1l11l1l11_opy_: str
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1lll1ll1111_opy_: Any
    bstack1l11lllllll_opy_: Dict
    def __init__(
        self,
        bstack1l1l11l1l11_opy_: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        bstack1lll1ll1111_opy_: Dict[str, Any],
        methods=[bstack1ll1l1_opy_ (u"ࠣࡡࡢ࡭ࡳ࡯ࡴࡠࡡࠥᓂ"), bstack1ll1l1_opy_ (u"ࠤࡶࡸࡦࡸࡴࡠࡵࡨࡷࡸ࡯࡯࡯ࠤᓃ"), bstack1ll1l1_opy_ (u"ࠥࡩࡽ࡫ࡣࡶࡶࡨࠦᓄ"), bstack1ll1l1_opy_ (u"ࠦࡶࡻࡩࡵࠤᓅ")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.bstack1l1l11l1l11_opy_ = bstack1l1l11l1l11_opy_
        self.platform_index = platform_index
        self.bstack11111llll1_opy_(methods)
        self.bstack1lll1ll1111_opy_ = bstack1lll1ll1111_opy_
    @staticmethod
    def session_id(target: object, strict=True):
        return bstack11111lll1l_opy_.get_data(bstack1lll1ll1lll_opy_.bstack1l1ll111l1l_opy_, target, strict)
    @staticmethod
    def hub_url(target: object, strict=True):
        return bstack11111lll1l_opy_.get_data(bstack1lll1ll1lll_opy_.bstack1l1ll1l11ll_opy_, target, strict)
    @staticmethod
    def bstack1l111l11111_opy_(target: object, strict=True):
        return bstack11111lll1l_opy_.get_data(bstack1lll1ll1lll_opy_.bstack1l1111lll11_opy_, target, strict)
    @staticmethod
    def capabilities(target: object, strict=True):
        return bstack11111lll1l_opy_.get_data(bstack1lll1ll1lll_opy_.bstack1l1ll111l11_opy_, target, strict)
    @staticmethod
    def bstack1ll1l1l1ll1_opy_(instance: bstack1llllllllll_opy_) -> bool:
        return bstack11111lll1l_opy_.bstack11111lllll_opy_(instance, bstack1lll1ll1lll_opy_.bstack1l1l111ll11_opy_, False)
    @staticmethod
    def bstack1ll1l11111l_opy_(instance: bstack1llllllllll_opy_, default_value=None):
        return bstack11111lll1l_opy_.bstack11111lllll_opy_(instance, bstack1lll1ll1lll_opy_.bstack1l1ll1l11ll_opy_, default_value)
    @staticmethod
    def bstack1ll1lll1111_opy_(instance: bstack1llllllllll_opy_, default_value=None):
        return bstack11111lll1l_opy_.bstack11111lllll_opy_(instance, bstack1lll1ll1lll_opy_.bstack1l1ll111l11_opy_, default_value)
    @staticmethod
    def bstack1ll11lll11l_opy_(hub_url: str, bstack1l111l11l1l_opy_=bstack1ll1l1_opy_ (u"ࠧ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮ࠤᓆ")):
        try:
            bstack1l1111lll1l_opy_ = str(urlparse(hub_url).netloc) if hub_url else None
            return bstack1l1111lll1l_opy_.endswith(bstack1l111l11l1l_opy_)
        except:
            pass
        return False
    @staticmethod
    def bstack1ll1l1llll1_opy_(method_name: str):
        return method_name == bstack1ll1l1_opy_ (u"ࠨࡥࡹࡧࡦࡹࡹ࡫ࠢᓇ")
    @staticmethod
    def bstack1ll11llllll_opy_(method_name: str, *args):
        return (
            bstack1lll1ll1lll_opy_.bstack1ll1l1llll1_opy_(method_name)
            and bstack1lll1ll1lll_opy_.bstack1l1l1l1l1ll_opy_(*args) == bstack1lll1ll1lll_opy_.bstack1l1l11l1l1l_opy_
        )
    @staticmethod
    def bstack1ll1l111lll_opy_(method_name: str, *args):
        if not bstack1lll1ll1lll_opy_.bstack1ll1l1llll1_opy_(method_name):
            return False
        if not bstack1lll1ll1lll_opy_.bstack1l1l11111l1_opy_ in bstack1lll1ll1lll_opy_.bstack1l1l1l1l1ll_opy_(*args):
            return False
        bstack1ll11ll1lll_opy_ = bstack1lll1ll1lll_opy_.bstack1ll11ll11l1_opy_(*args)
        return bstack1ll11ll1lll_opy_ and bstack1ll1l1_opy_ (u"ࠢࡴࡥࡵ࡭ࡵࡺࠢᓈ") in bstack1ll11ll1lll_opy_ and bstack1ll1l1_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠤᓉ") in bstack1ll11ll1lll_opy_[bstack1ll1l1_opy_ (u"ࠤࡶࡧࡷ࡯ࡰࡵࠤᓊ")]
    @staticmethod
    def bstack1ll1ll1l111_opy_(method_name: str, *args):
        if not bstack1lll1ll1lll_opy_.bstack1ll1l1llll1_opy_(method_name):
            return False
        if not bstack1lll1ll1lll_opy_.bstack1l1l11111l1_opy_ in bstack1lll1ll1lll_opy_.bstack1l1l1l1l1ll_opy_(*args):
            return False
        bstack1ll11ll1lll_opy_ = bstack1lll1ll1lll_opy_.bstack1ll11ll11l1_opy_(*args)
        return (
            bstack1ll11ll1lll_opy_
            and bstack1ll1l1_opy_ (u"ࠥࡷࡨࡸࡩࡱࡶࠥᓋ") in bstack1ll11ll1lll_opy_
            and bstack1ll1l1_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡢࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡴࡥࡵ࡭ࡵࡺࠢᓌ") in bstack1ll11ll1lll_opy_[bstack1ll1l1_opy_ (u"ࠧࡹࡣࡳ࡫ࡳࡸࠧᓍ")]
        )
    @staticmethod
    def bstack1l1l1l1l1ll_opy_(*args):
        return str(bstack1lll1ll1lll_opy_.bstack1ll1l1ll111_opy_(*args)).lower()
    @staticmethod
    def bstack1ll1l1ll111_opy_(*args):
        return args[0] if args and type(args) in [list, tuple] and isinstance(args[0], str) else None
    @staticmethod
    def bstack1ll11ll11l1_opy_(*args):
        return args[1] if len(args) > 1 and isinstance(args[1], dict) else None
    @staticmethod
    def bstack1llllll1ll_opy_(driver):
        command_executor = getattr(driver, bstack1ll1l1_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠤᓎ"), None)
        if not command_executor:
            return None
        hub_url = str(command_executor) if isinstance(command_executor, (str, bytes)) else None
        hub_url = str(command_executor._url) if not hub_url and getattr(command_executor, bstack1ll1l1_opy_ (u"ࠢࡠࡷࡵࡰࠧᓏ"), None) else None
        if not hub_url:
            client_config = getattr(command_executor, bstack1ll1l1_opy_ (u"ࠣࡡࡦࡰ࡮࡫࡮ࡵࡡࡦࡳࡳ࡬ࡩࡨࠤᓐ"), None)
            if not client_config:
                return None
            hub_url = getattr(client_config, bstack1ll1l1_opy_ (u"ࠤࡵࡩࡲࡵࡴࡦࡡࡶࡩࡷࡼࡥࡳࡡࡤࡨࡩࡸࠢᓑ"), None)
        return hub_url
    def bstack1l1l11ll111_opy_(self, instance, driver, hub_url: str):
        result = False
        if not hub_url:
            return result
        command_executor = getattr(driver, bstack1ll1l1_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡣࡪࡾࡥࡤࡷࡷࡳࡷࠨᓒ"), None)
        if command_executor:
            if isinstance(command_executor, (str, bytes)):
                setattr(driver, bstack1ll1l1_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࡤ࡫ࡸࡦࡥࡸࡸࡴࡸࠢᓓ"), hub_url)
                result = True
            elif hasattr(command_executor, bstack1ll1l1_opy_ (u"ࠧࡥࡵࡳ࡮ࠥᓔ")):
                setattr(command_executor, bstack1ll1l1_opy_ (u"ࠨ࡟ࡶࡴ࡯ࠦᓕ"), hub_url)
                result = True
        if result:
            self.bstack1l1l11l1l11_opy_ = hub_url
            bstack1lll1ll1lll_opy_.bstack1111111111_opy_(instance, bstack1lll1ll1lll_opy_.bstack1l1ll1l11ll_opy_, hub_url)
            bstack1lll1ll1lll_opy_.bstack1111111111_opy_(
                instance, bstack1lll1ll1lll_opy_.bstack1l1l111ll11_opy_, bstack1lll1ll1lll_opy_.bstack1ll11lll11l_opy_(hub_url)
            )
        return result
    @staticmethod
    def bstack1l1l111111l_opy_(bstack1111l1l11l_opy_: Tuple[bstack11111ll1l1_opy_, bstack1111l1l1l1_opy_]):
        return bstack1ll1l1_opy_ (u"ࠢ࠻ࠤᓖ").join((bstack11111ll1l1_opy_(bstack1111l1l11l_opy_[0]).name, bstack1111l1l1l1_opy_(bstack1111l1l11l_opy_[1]).name))
    @staticmethod
    def bstack1ll1l11l1l1_opy_(bstack1111l1l11l_opy_: Tuple[bstack11111ll1l1_opy_, bstack1111l1l1l1_opy_], callback: Callable):
        bstack1l1l11111ll_opy_ = bstack1lll1ll1lll_opy_.bstack1l1l111111l_opy_(bstack1111l1l11l_opy_)
        if not bstack1l1l11111ll_opy_ in bstack1lll1ll1lll_opy_.bstack1l111l111l1_opy_:
            bstack1lll1ll1lll_opy_.bstack1l111l111l1_opy_[bstack1l1l11111ll_opy_] = []
        bstack1lll1ll1lll_opy_.bstack1l111l111l1_opy_[bstack1l1l11111ll_opy_].append(callback)
    def bstack1111l11ll1_opy_(self, instance: bstack1llllllllll_opy_, method_name: str, bstack11111lll11_opy_: timedelta, *args, **kwargs):
        if not instance or method_name in (bstack1ll1l1_opy_ (u"ࠣࡵࡷࡥࡷࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠣᓗ")):
            return
        cmd = args[0] if method_name == bstack1ll1l1_opy_ (u"ࠤࡨࡼࡪࡩࡵࡵࡧࠥᓘ") and args and type(args) in [list, tuple] and isinstance(args[0], str) else None
        bstack1l111l111ll_opy_ = bstack1ll1l1_opy_ (u"ࠥ࠾ࠧᓙ").join(map(str, filter(None, [method_name, cmd])))
        instance.bstack11lll1l111_opy_(bstack1ll1l1_opy_ (u"ࠦࡩࡸࡩࡷࡧࡵ࠾ࠧᓚ") + bstack1l111l111ll_opy_, bstack11111lll11_opy_)
    def bstack11111l1ll1_opy_(
        self,
        target: object,
        exec: Tuple[bstack1llllllllll_opy_, str],
        bstack1111l1l11l_opy_: Tuple[bstack11111ll1l1_opy_, bstack1111l1l1l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable[..., Any]:
        instance, method_name = exec
        bstack111111llll_opy_, bstack1l1l1111l11_opy_ = bstack1111l1l11l_opy_
        bstack1l1l11111ll_opy_ = bstack1lll1ll1lll_opy_.bstack1l1l111111l_opy_(bstack1111l1l11l_opy_)
        self.logger.debug(bstack1ll1l1_opy_ (u"ࠧࡵ࡮ࡠࡪࡲࡳࡰࡀࠠ࡮ࡧࡷ࡬ࡴࡪ࡟࡯ࡣࡰࡩࡂࢁ࡭ࡦࡶ࡫ࡳࡩࡥ࡮ࡢ࡯ࡨࢁࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧᓛ") + str(kwargs) + bstack1ll1l1_opy_ (u"ࠨࠢᓜ"))
        if bstack111111llll_opy_ == bstack11111ll1l1_opy_.QUIT:
            if bstack1l1l1111l11_opy_ == bstack1111l1l1l1_opy_.PRE:
                bstack1ll1l1l111l_opy_ = bstack1lll111l11l_opy_.bstack1ll1ll111ll_opy_(EVENTS.bstack1ll1ll111_opy_.value)
                bstack11111lll1l_opy_.bstack1111111111_opy_(instance, EVENTS.bstack1ll1ll111_opy_.value, bstack1ll1l1l111l_opy_)
                self.logger.debug(bstack1ll1l1_opy_ (u"ࠢࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾࢁࠥࡳࡥࡵࡪࡲࡨࡤࡴࡡ࡮ࡧࡀࡿࢂࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥ࠾ࡽࢀࠤ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥ࠾ࡽࢀࠦᓝ").format(instance, method_name, bstack111111llll_opy_, bstack1l1l1111l11_opy_))
        if bstack111111llll_opy_ == bstack11111ll1l1_opy_.bstack1111l1111l_opy_:
            if bstack1l1l1111l11_opy_ == bstack1111l1l1l1_opy_.POST and not bstack1lll1ll1lll_opy_.bstack1l1ll111l1l_opy_ in instance.data:
                session_id = getattr(target, bstack1ll1l1_opy_ (u"ࠣࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࠧᓞ"), None)
                if session_id:
                    instance.data[bstack1lll1ll1lll_opy_.bstack1l1ll111l1l_opy_] = session_id
        elif (
            bstack111111llll_opy_ == bstack11111ll1l1_opy_.bstack111111l11l_opy_
            and bstack1lll1ll1lll_opy_.bstack1l1l1l1l1ll_opy_(*args) == bstack1lll1ll1lll_opy_.bstack1l1l11l1l1l_opy_
        ):
            if bstack1l1l1111l11_opy_ == bstack1111l1l1l1_opy_.PRE:
                hub_url = bstack1lll1ll1lll_opy_.bstack1llllll1ll_opy_(target)
                if hub_url:
                    instance.data.update(
                        {
                            bstack1lll1ll1lll_opy_.bstack1l1ll1l11ll_opy_: hub_url,
                            bstack1lll1ll1lll_opy_.bstack1l1l111ll11_opy_: bstack1lll1ll1lll_opy_.bstack1ll11lll11l_opy_(hub_url),
                            bstack1lll1ll1lll_opy_.bstack1ll11llll1l_opy_: int(
                                os.environ.get(bstack1ll1l1_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠤᓟ"), str(self.platform_index))
                            ),
                        }
                    )
                bstack1ll11ll1lll_opy_ = bstack1lll1ll1lll_opy_.bstack1ll11ll11l1_opy_(*args)
                bstack1l111l11111_opy_ = bstack1ll11ll1lll_opy_.get(bstack1ll1l1_opy_ (u"ࠥࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠤᓠ"), None) if bstack1ll11ll1lll_opy_ else None
                if isinstance(bstack1l111l11111_opy_, dict):
                    instance.data[bstack1lll1ll1lll_opy_.bstack1l1111lll11_opy_] = copy.deepcopy(bstack1l111l11111_opy_)
                    instance.data[bstack1lll1ll1lll_opy_.bstack1l1ll111l11_opy_] = bstack1l111l11111_opy_
            elif bstack1l1l1111l11_opy_ == bstack1111l1l1l1_opy_.POST:
                if isinstance(result, dict):
                    framework_session_id = result.get(bstack1ll1l1_opy_ (u"ࠦࡻࡧ࡬ࡶࡧࠥᓡ"), dict()).get(bstack1ll1l1_opy_ (u"ࠧࡹࡥࡴࡵ࡬ࡳࡳࡏࡤࠣᓢ"), None)
                    if framework_session_id:
                        instance.data.update(
                            {
                                bstack1lll1ll1lll_opy_.bstack1l1ll111l1l_opy_: framework_session_id,
                                bstack1lll1ll1lll_opy_.bstack1l111l1111l_opy_: datetime.now(tz=timezone.utc),
                            }
                        )
        elif (
            bstack111111llll_opy_ == bstack11111ll1l1_opy_.bstack111111l11l_opy_
            and bstack1lll1ll1lll_opy_.bstack1l1l1l1l1ll_opy_(*args) == bstack1lll1ll1lll_opy_.bstack1l1111lllll_opy_
            and bstack1l1l1111l11_opy_ == bstack1111l1l1l1_opy_.POST
        ):
            instance.data[bstack1lll1ll1lll_opy_.bstack1l1111llll1_opy_] = datetime.now(tz=timezone.utc)
        if bstack1l1l11111ll_opy_ in bstack1lll1ll1lll_opy_.bstack1l111l111l1_opy_:
            bstack1l1l1111lll_opy_ = None
            for callback in bstack1lll1ll1lll_opy_.bstack1l111l111l1_opy_[bstack1l1l11111ll_opy_]:
                try:
                    bstack1l1l1111111_opy_ = callback(self, target, exec, bstack1111l1l11l_opy_, result, *args, **kwargs)
                    if bstack1l1l1111lll_opy_ == None:
                        bstack1l1l1111lll_opy_ = bstack1l1l1111111_opy_
                except Exception as e:
                    self.logger.error(bstack1ll1l1_opy_ (u"ࠨࡥࡳࡴࡲࡶࠥ࡯࡮ࡷࡱ࡮࡭ࡳ࡭ࠠࡤࡣ࡯ࡰࡧࡧࡣ࡬࠼ࠣࠦᓣ") + str(e) + bstack1ll1l1_opy_ (u"ࠢࠣᓤ"))
                    traceback.print_exc()
            if bstack111111llll_opy_ == bstack11111ll1l1_opy_.QUIT:
                if bstack1l1l1111l11_opy_ == bstack1111l1l1l1_opy_.POST:
                    bstack1ll1l1l111l_opy_ = bstack11111lll1l_opy_.bstack11111lllll_opy_(instance, EVENTS.bstack1ll1ll111_opy_.value)
                    if bstack1ll1l1l111l_opy_!=None:
                        bstack1lll111l11l_opy_.end(EVENTS.bstack1ll1ll111_opy_.value, bstack1ll1l1l111l_opy_+bstack1ll1l1_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣᓥ"), bstack1ll1l1l111l_opy_+bstack1ll1l1_opy_ (u"ࠤ࠽ࡩࡳࡪࠢᓦ"), True, None)
            if bstack1l1l1111l11_opy_ == bstack1111l1l1l1_opy_.PRE and callable(bstack1l1l1111lll_opy_):
                return bstack1l1l1111lll_opy_
            elif bstack1l1l1111l11_opy_ == bstack1111l1l1l1_opy_.POST and bstack1l1l1111lll_opy_:
                return bstack1l1l1111lll_opy_
    def bstack111111l111_opy_(
        self, method_name, previous_state: bstack11111ll1l1_opy_, *args, **kwargs
    ) -> bstack11111ll1l1_opy_:
        if method_name == bstack1ll1l1_opy_ (u"ࠥࡣࡤ࡯࡮ࡪࡶࡢࡣࠧᓧ") or method_name == bstack1ll1l1_opy_ (u"ࠦࡸࡺࡡࡳࡶࡢࡷࡪࡹࡳࡪࡱࡱࠦᓨ"):
            return bstack11111ll1l1_opy_.bstack1111l1111l_opy_
        if method_name == bstack1ll1l1_opy_ (u"ࠧࡷࡵࡪࡶࠥᓩ"):
            return bstack11111ll1l1_opy_.QUIT
        if method_name == bstack1ll1l1_opy_ (u"ࠨࡥࡹࡧࡦࡹࡹ࡫ࠢᓪ"):
            if previous_state != bstack11111ll1l1_opy_.NONE:
                bstack1ll1l1l11ll_opy_ = bstack1lll1ll1lll_opy_.bstack1l1l1l1l1ll_opy_(*args)
                if bstack1ll1l1l11ll_opy_ == bstack1lll1ll1lll_opy_.bstack1l1l11l1l1l_opy_:
                    return bstack11111ll1l1_opy_.bstack1111l1111l_opy_
            return bstack11111ll1l1_opy_.bstack111111l11l_opy_
        return bstack11111ll1l1_opy_.NONE
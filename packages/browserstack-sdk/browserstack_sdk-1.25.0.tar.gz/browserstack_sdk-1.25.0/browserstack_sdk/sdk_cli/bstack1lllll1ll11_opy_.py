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
import os
import traceback
from typing import Dict, Tuple, Callable, Type, List, Any
from urllib.parse import urlparse
from browserstack_sdk.sdk_cli.bstack1111l11lll_opy_ import (
    bstack11111ll1l1_opy_,
    bstack11111l11ll_opy_,
    bstack1111l1ll1l_opy_,
    bstack111111111l_opy_,
)
import copy
from datetime import datetime, timezone, timedelta
from bstack_utils.bstack1l1ll1l11l_opy_ import bstack1lll1llll1l_opy_
from bstack_utils.constants import EVENTS
class bstack1lll1l11ll1_opy_(bstack11111ll1l1_opy_):
    bstack1l1l11l111l_opy_ = bstack11l1l11_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠤᑚ")
    NAME = bstack11l1l11_opy_ (u"ࠥࡷࡪࡲࡥ࡯࡫ࡸࡱࠧᑛ")
    bstack1l1ll1llll1_opy_ = bstack11l1l11_opy_ (u"ࠦ࡭ࡻࡢࡠࡷࡵࡰࠧᑜ")
    bstack1l1lll1111l_opy_ = bstack11l1l11_opy_ (u"ࠧ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࠧᑝ")
    bstack1l111llllll_opy_ = bstack11l1l11_opy_ (u"ࠨࡩ࡯ࡲࡸࡸࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦᑞ")
    bstack1l1ll1l1lll_opy_ = bstack11l1l11_opy_ (u"ࠢࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨᑟ")
    bstack1l1l1l1111l_opy_ = bstack11l1l11_opy_ (u"ࠣ࡫ࡶࡣࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢ࡬ࡺࡨࠢᑠ")
    bstack1l111lll1l1_opy_ = bstack11l1l11_opy_ (u"ࠤࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹࠨᑡ")
    bstack1l111llll11_opy_ = bstack11l1l11_opy_ (u"ࠥࡩࡳࡪࡥࡥࡡࡤࡸࠧᑢ")
    bstack1ll1l11llll_opy_ = bstack11l1l11_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࡥࡩ࡯ࡦࡨࡼࠧᑣ")
    bstack1l1l1l1l11l_opy_ = bstack11l1l11_opy_ (u"ࠧࡴࡥࡸࡵࡨࡷࡸ࡯࡯࡯ࠤᑤ")
    bstack1l11l1111ll_opy_ = bstack11l1l11_opy_ (u"ࠨࡧࡦࡶࠥᑥ")
    bstack1ll1111l111_opy_ = bstack11l1l11_opy_ (u"ࠢࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠦᑦ")
    bstack1l1l11l1l1l_opy_ = bstack11l1l11_opy_ (u"ࠣࡹ࠶ࡧࡪࡾࡥࡤࡷࡷࡩࡸࡩࡲࡪࡲࡷࠦᑧ")
    bstack1l1l111llll_opy_ = bstack11l1l11_opy_ (u"ࠤࡺ࠷ࡨ࡫ࡸࡦࡥࡸࡸࡪࡹࡣࡳ࡫ࡳࡸࡦࡹࡹ࡯ࡥࠥᑨ")
    bstack1l11l11111l_opy_ = bstack11l1l11_opy_ (u"ࠥࡵࡺ࡯ࡴࠣᑩ")
    bstack1l11l1111l1_opy_: Dict[str, List[Callable]] = dict()
    bstack1l1l1llll11_opy_: str
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1lllll1l1ll_opy_: Any
    bstack1l1l111ll1l_opy_: Dict
    def __init__(
        self,
        bstack1l1l1llll11_opy_: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        bstack1lllll1l1ll_opy_: Dict[str, Any],
        methods=[bstack11l1l11_opy_ (u"ࠦࡤࡥࡩ࡯࡫ࡷࡣࡤࠨᑪ"), bstack11l1l11_opy_ (u"ࠧࡹࡴࡢࡴࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠧᑫ"), bstack11l1l11_opy_ (u"ࠨࡥࡹࡧࡦࡹࡹ࡫ࠢᑬ"), bstack11l1l11_opy_ (u"ࠢࡲࡷ࡬ࡸࠧᑭ")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.bstack1l1l1llll11_opy_ = bstack1l1l1llll11_opy_
        self.platform_index = platform_index
        self.bstack11111l11l1_opy_(methods)
        self.bstack1lllll1l1ll_opy_ = bstack1lllll1l1ll_opy_
    @staticmethod
    def session_id(target: object, strict=True):
        return bstack11111ll1l1_opy_.get_data(bstack1lll1l11ll1_opy_.bstack1l1lll1111l_opy_, target, strict)
    @staticmethod
    def hub_url(target: object, strict=True):
        return bstack11111ll1l1_opy_.get_data(bstack1lll1l11ll1_opy_.bstack1l1ll1llll1_opy_, target, strict)
    @staticmethod
    def bstack1l111lll1ll_opy_(target: object, strict=True):
        return bstack11111ll1l1_opy_.get_data(bstack1lll1l11ll1_opy_.bstack1l111llllll_opy_, target, strict)
    @staticmethod
    def capabilities(target: object, strict=True):
        return bstack11111ll1l1_opy_.get_data(bstack1lll1l11ll1_opy_.bstack1l1ll1l1lll_opy_, target, strict)
    @staticmethod
    def bstack1ll1l1111ll_opy_(instance: bstack11111l11ll_opy_) -> bool:
        return bstack11111ll1l1_opy_.bstack11111l1l1l_opy_(instance, bstack1lll1l11ll1_opy_.bstack1l1l1l1111l_opy_, False)
    @staticmethod
    def bstack1ll1lll1111_opy_(instance: bstack11111l11ll_opy_, default_value=None):
        return bstack11111ll1l1_opy_.bstack11111l1l1l_opy_(instance, bstack1lll1l11ll1_opy_.bstack1l1ll1llll1_opy_, default_value)
    @staticmethod
    def bstack1ll1ll1ll1l_opy_(instance: bstack11111l11ll_opy_, default_value=None):
        return bstack11111ll1l1_opy_.bstack11111l1l1l_opy_(instance, bstack1lll1l11ll1_opy_.bstack1l1ll1l1lll_opy_, default_value)
    @staticmethod
    def bstack1ll11lll1ll_opy_(hub_url: str, bstack1l111lllll1_opy_=bstack11l1l11_opy_ (u"ࠣ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠧᑮ")):
        try:
            bstack1l11l111111_opy_ = str(urlparse(hub_url).netloc) if hub_url else None
            return bstack1l11l111111_opy_.endswith(bstack1l111lllll1_opy_)
        except:
            pass
        return False
    @staticmethod
    def bstack1ll1ll11l1l_opy_(method_name: str):
        return method_name == bstack11l1l11_opy_ (u"ࠤࡨࡼࡪࡩࡵࡵࡧࠥᑯ")
    @staticmethod
    def bstack1ll1l11l1l1_opy_(method_name: str, *args):
        return (
            bstack1lll1l11ll1_opy_.bstack1ll1ll11l1l_opy_(method_name)
            and bstack1lll1l11ll1_opy_.bstack1l1l1llll1l_opy_(*args) == bstack1lll1l11ll1_opy_.bstack1l1l1l1l11l_opy_
        )
    @staticmethod
    def bstack1ll1ll1l1ll_opy_(method_name: str, *args):
        if not bstack1lll1l11ll1_opy_.bstack1ll1ll11l1l_opy_(method_name):
            return False
        if not bstack1lll1l11ll1_opy_.bstack1l1l11l1l1l_opy_ in bstack1lll1l11ll1_opy_.bstack1l1l1llll1l_opy_(*args):
            return False
        bstack1ll1l11111l_opy_ = bstack1lll1l11ll1_opy_.bstack1ll11lll1l1_opy_(*args)
        return bstack1ll1l11111l_opy_ and bstack11l1l11_opy_ (u"ࠥࡷࡨࡸࡩࡱࡶࠥᑰ") in bstack1ll1l11111l_opy_ and bstack11l1l11_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶࠧᑱ") in bstack1ll1l11111l_opy_[bstack11l1l11_opy_ (u"ࠧࡹࡣࡳ࡫ࡳࡸࠧᑲ")]
    @staticmethod
    def bstack1ll1l1ll1l1_opy_(method_name: str, *args):
        if not bstack1lll1l11ll1_opy_.bstack1ll1ll11l1l_opy_(method_name):
            return False
        if not bstack1lll1l11ll1_opy_.bstack1l1l11l1l1l_opy_ in bstack1lll1l11ll1_opy_.bstack1l1l1llll1l_opy_(*args):
            return False
        bstack1ll1l11111l_opy_ = bstack1lll1l11ll1_opy_.bstack1ll11lll1l1_opy_(*args)
        return (
            bstack1ll1l11111l_opy_
            and bstack11l1l11_opy_ (u"ࠨࡳࡤࡴ࡬ࡴࡹࠨᑳ") in bstack1ll1l11111l_opy_
            and bstack11l1l11_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡥࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡷࡨࡸࡩࡱࡶࠥᑴ") in bstack1ll1l11111l_opy_[bstack11l1l11_opy_ (u"ࠣࡵࡦࡶ࡮ࡶࡴࠣᑵ")]
        )
    @staticmethod
    def bstack1l1l1llll1l_opy_(*args):
        return str(bstack1lll1l11ll1_opy_.bstack1ll1ll1l111_opy_(*args)).lower()
    @staticmethod
    def bstack1ll1ll1l111_opy_(*args):
        return args[0] if args and type(args) in [list, tuple] and isinstance(args[0], str) else None
    @staticmethod
    def bstack1ll11lll1l1_opy_(*args):
        return args[1] if len(args) > 1 and isinstance(args[1], dict) else None
    @staticmethod
    def bstack11111l1l_opy_(driver):
        command_executor = getattr(driver, bstack11l1l11_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࡢࡩࡽ࡫ࡣࡶࡶࡲࡶࠧᑶ"), None)
        if not command_executor:
            return None
        hub_url = str(command_executor) if isinstance(command_executor, (str, bytes)) else None
        hub_url = str(command_executor._url) if not hub_url and getattr(command_executor, bstack11l1l11_opy_ (u"ࠥࡣࡺࡸ࡬ࠣᑷ"), None) else None
        if not hub_url:
            client_config = getattr(command_executor, bstack11l1l11_opy_ (u"ࠦࡤࡩ࡬ࡪࡧࡱࡸࡤࡩ࡯࡯ࡨ࡬࡫ࠧᑸ"), None)
            if not client_config:
                return None
            hub_url = getattr(client_config, bstack11l1l11_opy_ (u"ࠧࡸࡥ࡮ࡱࡷࡩࡤࡹࡥࡳࡸࡨࡶࡤࡧࡤࡥࡴࠥᑹ"), None)
        return hub_url
    def bstack1l1l1l1lll1_opy_(self, instance, driver, hub_url: str):
        result = False
        if not hub_url:
            return result
        command_executor = getattr(driver, bstack11l1l11_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠤᑺ"), None)
        if command_executor:
            if isinstance(command_executor, (str, bytes)):
                setattr(driver, bstack11l1l11_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࡠࡧࡻࡩࡨࡻࡴࡰࡴࠥᑻ"), hub_url)
                result = True
            elif hasattr(command_executor, bstack11l1l11_opy_ (u"ࠣࡡࡸࡶࡱࠨᑼ")):
                setattr(command_executor, bstack11l1l11_opy_ (u"ࠤࡢࡹࡷࡲࠢᑽ"), hub_url)
                result = True
        if result:
            self.bstack1l1l1llll11_opy_ = hub_url
            bstack1lll1l11ll1_opy_.bstack1111111l1l_opy_(instance, bstack1lll1l11ll1_opy_.bstack1l1ll1llll1_opy_, hub_url)
            bstack1lll1l11ll1_opy_.bstack1111111l1l_opy_(
                instance, bstack1lll1l11ll1_opy_.bstack1l1l1l1111l_opy_, bstack1lll1l11ll1_opy_.bstack1ll11lll1ll_opy_(hub_url)
            )
        return result
    @staticmethod
    def bstack1l1l11l1l11_opy_(bstack1111l1ll11_opy_: Tuple[bstack1111l1ll1l_opy_, bstack111111111l_opy_]):
        return bstack11l1l11_opy_ (u"ࠥ࠾ࠧᑾ").join((bstack1111l1ll1l_opy_(bstack1111l1ll11_opy_[0]).name, bstack111111111l_opy_(bstack1111l1ll11_opy_[1]).name))
    @staticmethod
    def bstack1ll1l11l11l_opy_(bstack1111l1ll11_opy_: Tuple[bstack1111l1ll1l_opy_, bstack111111111l_opy_], callback: Callable):
        bstack1l1l11l1111_opy_ = bstack1lll1l11ll1_opy_.bstack1l1l11l1l11_opy_(bstack1111l1ll11_opy_)
        if not bstack1l1l11l1111_opy_ in bstack1lll1l11ll1_opy_.bstack1l11l1111l1_opy_:
            bstack1lll1l11ll1_opy_.bstack1l11l1111l1_opy_[bstack1l1l11l1111_opy_] = []
        bstack1lll1l11ll1_opy_.bstack1l11l1111l1_opy_[bstack1l1l11l1111_opy_].append(callback)
    def bstack111111llll_opy_(self, instance: bstack11111l11ll_opy_, method_name: str, bstack11111l1ll1_opy_: timedelta, *args, **kwargs):
        if not instance or method_name in (bstack11l1l11_opy_ (u"ࠦࡸࡺࡡࡳࡶࡢࡷࡪࡹࡳࡪࡱࡱࠦᑿ")):
            return
        cmd = args[0] if method_name == bstack11l1l11_opy_ (u"ࠧ࡫ࡸࡦࡥࡸࡸࡪࠨᒀ") and args and type(args) in [list, tuple] and isinstance(args[0], str) else None
        bstack1l111llll1l_opy_ = bstack11l1l11_opy_ (u"ࠨ࠺ࠣᒁ").join(map(str, filter(None, [method_name, cmd])))
        instance.bstack1ll11lll_opy_(bstack11l1l11_opy_ (u"ࠢࡥࡴ࡬ࡺࡪࡸ࠺ࠣᒂ") + bstack1l111llll1l_opy_, bstack11111l1ll1_opy_)
    def bstack1111l1111l_opy_(
        self,
        target: object,
        exec: Tuple[bstack11111l11ll_opy_, str],
        bstack1111l1ll11_opy_: Tuple[bstack1111l1ll1l_opy_, bstack111111111l_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable[..., Any]:
        instance, method_name = exec
        bstack1111l11111_opy_, bstack1l1l11l1ll1_opy_ = bstack1111l1ll11_opy_
        bstack1l1l11l1111_opy_ = bstack1lll1l11ll1_opy_.bstack1l1l11l1l11_opy_(bstack1111l1ll11_opy_)
        self.logger.debug(bstack11l1l11_opy_ (u"ࠣࡱࡱࡣ࡭ࡵ࡯࡬࠼ࠣࡱࡪࡺࡨࡰࡦࡢࡲࡦࡳࡥ࠾ࡽࡰࡩࡹ࡮࡯ࡥࡡࡱࡥࡲ࡫ࡽࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣᒃ") + str(kwargs) + bstack11l1l11_opy_ (u"ࠤࠥᒄ"))
        if bstack1111l11111_opy_ == bstack1111l1ll1l_opy_.QUIT:
            if bstack1l1l11l1ll1_opy_ == bstack111111111l_opy_.PRE:
                bstack1ll1ll1l1l1_opy_ = bstack1lll1llll1l_opy_.bstack1ll1ll1lll1_opy_(EVENTS.bstack11l1ll1l11_opy_.value)
                bstack11111ll1l1_opy_.bstack1111111l1l_opy_(instance, EVENTS.bstack11l1ll1l11_opy_.value, bstack1ll1ll1l1l1_opy_)
                self.logger.debug(bstack11l1l11_opy_ (u"ࠥ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡽࠡ࡯ࡨࡸ࡭ࡵࡤࡠࡰࡤࡱࡪࡃࡻࡾࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࡁࢀࢃࠠࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࡁࢀࢃࠢᒅ").format(instance, method_name, bstack1111l11111_opy_, bstack1l1l11l1ll1_opy_))
        if bstack1111l11111_opy_ == bstack1111l1ll1l_opy_.bstack111111ll11_opy_:
            if bstack1l1l11l1ll1_opy_ == bstack111111111l_opy_.POST and not bstack1lll1l11ll1_opy_.bstack1l1lll1111l_opy_ in instance.data:
                session_id = getattr(target, bstack11l1l11_opy_ (u"ࠦࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤࠣᒆ"), None)
                if session_id:
                    instance.data[bstack1lll1l11ll1_opy_.bstack1l1lll1111l_opy_] = session_id
        elif (
            bstack1111l11111_opy_ == bstack1111l1ll1l_opy_.bstack111111l111_opy_
            and bstack1lll1l11ll1_opy_.bstack1l1l1llll1l_opy_(*args) == bstack1lll1l11ll1_opy_.bstack1l1l1l1l11l_opy_
        ):
            if bstack1l1l11l1ll1_opy_ == bstack111111111l_opy_.PRE:
                hub_url = bstack1lll1l11ll1_opy_.bstack11111l1l_opy_(target)
                if hub_url:
                    instance.data.update(
                        {
                            bstack1lll1l11ll1_opy_.bstack1l1ll1llll1_opy_: hub_url,
                            bstack1lll1l11ll1_opy_.bstack1l1l1l1111l_opy_: bstack1lll1l11ll1_opy_.bstack1ll11lll1ll_opy_(hub_url),
                            bstack1lll1l11ll1_opy_.bstack1ll1l11llll_opy_: int(
                                os.environ.get(bstack11l1l11_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠧᒇ"), str(self.platform_index))
                            ),
                        }
                    )
                bstack1ll1l11111l_opy_ = bstack1lll1l11ll1_opy_.bstack1ll11lll1l1_opy_(*args)
                bstack1l111lll1ll_opy_ = bstack1ll1l11111l_opy_.get(bstack11l1l11_opy_ (u"ࠨࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠧᒈ"), None) if bstack1ll1l11111l_opy_ else None
                if isinstance(bstack1l111lll1ll_opy_, dict):
                    instance.data[bstack1lll1l11ll1_opy_.bstack1l111llllll_opy_] = copy.deepcopy(bstack1l111lll1ll_opy_)
                    instance.data[bstack1lll1l11ll1_opy_.bstack1l1ll1l1lll_opy_] = bstack1l111lll1ll_opy_
            elif bstack1l1l11l1ll1_opy_ == bstack111111111l_opy_.POST:
                if isinstance(result, dict):
                    framework_session_id = result.get(bstack11l1l11_opy_ (u"ࠢࡷࡣ࡯ࡹࡪࠨᒉ"), dict()).get(bstack11l1l11_opy_ (u"ࠣࡵࡨࡷࡸ࡯࡯࡯ࡋࡧࠦᒊ"), None)
                    if framework_session_id:
                        instance.data.update(
                            {
                                bstack1lll1l11ll1_opy_.bstack1l1lll1111l_opy_: framework_session_id,
                                bstack1lll1l11ll1_opy_.bstack1l111lll1l1_opy_: datetime.now(tz=timezone.utc),
                            }
                        )
        elif (
            bstack1111l11111_opy_ == bstack1111l1ll1l_opy_.bstack111111l111_opy_
            and bstack1lll1l11ll1_opy_.bstack1l1l1llll1l_opy_(*args) == bstack1lll1l11ll1_opy_.bstack1l11l11111l_opy_
            and bstack1l1l11l1ll1_opy_ == bstack111111111l_opy_.POST
        ):
            instance.data[bstack1lll1l11ll1_opy_.bstack1l111llll11_opy_] = datetime.now(tz=timezone.utc)
        if bstack1l1l11l1111_opy_ in bstack1lll1l11ll1_opy_.bstack1l11l1111l1_opy_:
            bstack1l1l111lll1_opy_ = None
            for callback in bstack1lll1l11ll1_opy_.bstack1l11l1111l1_opy_[bstack1l1l11l1111_opy_]:
                try:
                    bstack1l1l11l11ll_opy_ = callback(self, target, exec, bstack1111l1ll11_opy_, result, *args, **kwargs)
                    if bstack1l1l111lll1_opy_ == None:
                        bstack1l1l111lll1_opy_ = bstack1l1l11l11ll_opy_
                except Exception as e:
                    self.logger.error(bstack11l1l11_opy_ (u"ࠤࡨࡶࡷࡵࡲࠡ࡫ࡱࡺࡴࡱࡩ࡯ࡩࠣࡧࡦࡲ࡬ࡣࡣࡦ࡯࠿ࠦࠢᒋ") + str(e) + bstack11l1l11_opy_ (u"ࠥࠦᒌ"))
                    traceback.print_exc()
            if bstack1111l11111_opy_ == bstack1111l1ll1l_opy_.QUIT:
                if bstack1l1l11l1ll1_opy_ == bstack111111111l_opy_.POST:
                    bstack1ll1ll1l1l1_opy_ = bstack11111ll1l1_opy_.bstack11111l1l1l_opy_(instance, EVENTS.bstack11l1ll1l11_opy_.value)
                    if bstack1ll1ll1l1l1_opy_!=None:
                        bstack1lll1llll1l_opy_.end(EVENTS.bstack11l1ll1l11_opy_.value, bstack1ll1ll1l1l1_opy_+bstack11l1l11_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦᒍ"), bstack1ll1ll1l1l1_opy_+bstack11l1l11_opy_ (u"ࠧࡀࡥ࡯ࡦࠥᒎ"), True, None)
            if bstack1l1l11l1ll1_opy_ == bstack111111111l_opy_.PRE and callable(bstack1l1l111lll1_opy_):
                return bstack1l1l111lll1_opy_
            elif bstack1l1l11l1ll1_opy_ == bstack111111111l_opy_.POST and bstack1l1l111lll1_opy_:
                return bstack1l1l111lll1_opy_
    def bstack1111l111ll_opy_(
        self, method_name, previous_state: bstack1111l1ll1l_opy_, *args, **kwargs
    ) -> bstack1111l1ll1l_opy_:
        if method_name == bstack11l1l11_opy_ (u"ࠨ࡟ࡠ࡫ࡱ࡭ࡹࡥ࡟ࠣᒏ") or method_name == bstack11l1l11_opy_ (u"ࠢࡴࡶࡤࡶࡹࡥࡳࡦࡵࡶ࡭ࡴࡴࠢᒐ"):
            return bstack1111l1ll1l_opy_.bstack111111ll11_opy_
        if method_name == bstack11l1l11_opy_ (u"ࠣࡳࡸ࡭ࡹࠨᒑ"):
            return bstack1111l1ll1l_opy_.QUIT
        if method_name == bstack11l1l11_opy_ (u"ࠤࡨࡼࡪࡩࡵࡵࡧࠥᒒ"):
            if previous_state != bstack1111l1ll1l_opy_.NONE:
                bstack1ll1l1ll111_opy_ = bstack1lll1l11ll1_opy_.bstack1l1l1llll1l_opy_(*args)
                if bstack1ll1l1ll111_opy_ == bstack1lll1l11ll1_opy_.bstack1l1l1l1l11l_opy_:
                    return bstack1111l1ll1l_opy_.bstack111111ll11_opy_
            return bstack1111l1ll1l_opy_.bstack111111l111_opy_
        return bstack1111l1ll1l_opy_.NONE
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
class bstack1llllll11ll_opy_(bstack11111ll1l1_opy_):
    bstack1l1l11l111l_opy_ = bstack11l1l11_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝ࠨጱ")
    bstack1l1lll1111l_opy_ = bstack11l1l11_opy_ (u"ࠢࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪࠢጲ")
    bstack1l1ll1llll1_opy_ = bstack11l1l11_opy_ (u"ࠣࡪࡸࡦࡤࡻࡲ࡭ࠤጳ")
    bstack1l1ll1l1lll_opy_ = bstack11l1l11_opy_ (u"ࠤࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣጴ")
    bstack1l1l11l1l1l_opy_ = bstack11l1l11_opy_ (u"ࠥࡻ࠸ࡩࡥࡹࡧࡦࡹࡹ࡫ࡳࡤࡴ࡬ࡴࡹࠨጵ")
    bstack1l1l111llll_opy_ = bstack11l1l11_opy_ (u"ࠦࡼ࠹ࡣࡦࡺࡨࡧࡺࡺࡥࡴࡥࡵ࡭ࡵࡺࡡࡴࡻࡱࡧࠧጶ")
    NAME = bstack11l1l11_opy_ (u"ࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤጷ")
    bstack1l1l11l11l1_opy_: Dict[str, List[Callable]] = dict()
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1lllll1l1ll_opy_: Any
    bstack1l1l111ll1l_opy_: Dict
    def __init__(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        methods=[bstack11l1l11_opy_ (u"ࠨ࡬ࡢࡷࡱࡧ࡭ࠨጸ"), bstack11l1l11_opy_ (u"ࠢࡤࡱࡱࡲࡪࡩࡴࠣጹ"), bstack11l1l11_opy_ (u"ࠣࡰࡨࡻࡤࡶࡡࡨࡧࠥጺ"), bstack11l1l11_opy_ (u"ࠤࡦࡰࡴࡹࡥࠣጻ"), bstack11l1l11_opy_ (u"ࠥࡨ࡮ࡹࡰࡢࡶࡦ࡬ࠧጼ")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.platform_index = platform_index
        self.bstack11111l11l1_opy_(methods)
    def bstack111111llll_opy_(self, instance: bstack11111l11ll_opy_, method_name: str, bstack11111l1ll1_opy_: timedelta, *args, **kwargs):
        pass
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
        bstack1l1l11l1111_opy_ = bstack1llllll11ll_opy_.bstack1l1l11l1l11_opy_(bstack1111l1ll11_opy_)
        if bstack1l1l11l1111_opy_ in bstack1llllll11ll_opy_.bstack1l1l11l11l1_opy_:
            bstack1l1l111lll1_opy_ = None
            for callback in bstack1llllll11ll_opy_.bstack1l1l11l11l1_opy_[bstack1l1l11l1111_opy_]:
                try:
                    bstack1l1l11l11ll_opy_ = callback(self, target, exec, bstack1111l1ll11_opy_, result, *args, **kwargs)
                    if bstack1l1l111lll1_opy_ == None:
                        bstack1l1l111lll1_opy_ = bstack1l1l11l11ll_opy_
                except Exception as e:
                    self.logger.error(bstack11l1l11_opy_ (u"ࠦࡪࡸࡲࡰࡴࠣ࡭ࡳࡼ࡯࡬࡫ࡱ࡫ࠥࡩࡡ࡭࡮ࡥࡥࡨࡱ࠺ࠡࠤጽ") + str(e) + bstack11l1l11_opy_ (u"ࠧࠨጾ"))
                    traceback.print_exc()
            if bstack1l1l11l1ll1_opy_ == bstack111111111l_opy_.PRE and callable(bstack1l1l111lll1_opy_):
                return bstack1l1l111lll1_opy_
            elif bstack1l1l11l1ll1_opy_ == bstack111111111l_opy_.POST and bstack1l1l111lll1_opy_:
                return bstack1l1l111lll1_opy_
    def bstack1111l111ll_opy_(
        self, method_name, previous_state: bstack1111l1ll1l_opy_, *args, **kwargs
    ) -> bstack1111l1ll1l_opy_:
        if method_name == bstack11l1l11_opy_ (u"࠭࡬ࡢࡷࡱࡧ࡭࠭ጿ") or method_name == bstack11l1l11_opy_ (u"ࠧࡤࡱࡱࡲࡪࡩࡴࠨፀ") or method_name == bstack11l1l11_opy_ (u"ࠨࡰࡨࡻࡤࡶࡡࡨࡧࠪፁ"):
            return bstack1111l1ll1l_opy_.bstack111111ll11_opy_
        if method_name == bstack11l1l11_opy_ (u"ࠩࡧ࡭ࡸࡶࡡࡵࡥ࡫ࠫፂ"):
            return bstack1111l1ll1l_opy_.bstack11111111ll_opy_
        if method_name == bstack11l1l11_opy_ (u"ࠪࡧࡱࡵࡳࡦࠩፃ"):
            return bstack1111l1ll1l_opy_.QUIT
        return bstack1111l1ll1l_opy_.NONE
    @staticmethod
    def bstack1l1l11l1l11_opy_(bstack1111l1ll11_opy_: Tuple[bstack1111l1ll1l_opy_, bstack111111111l_opy_]):
        return bstack11l1l11_opy_ (u"ࠦ࠿ࠨፄ").join((bstack1111l1ll1l_opy_(bstack1111l1ll11_opy_[0]).name, bstack111111111l_opy_(bstack1111l1ll11_opy_[1]).name))
    @staticmethod
    def bstack1ll1l11l11l_opy_(bstack1111l1ll11_opy_: Tuple[bstack1111l1ll1l_opy_, bstack111111111l_opy_], callback: Callable):
        bstack1l1l11l1111_opy_ = bstack1llllll11ll_opy_.bstack1l1l11l1l11_opy_(bstack1111l1ll11_opy_)
        if not bstack1l1l11l1111_opy_ in bstack1llllll11ll_opy_.bstack1l1l11l11l1_opy_:
            bstack1llllll11ll_opy_.bstack1l1l11l11l1_opy_[bstack1l1l11l1111_opy_] = []
        bstack1llllll11ll_opy_.bstack1l1l11l11l1_opy_[bstack1l1l11l1111_opy_].append(callback)
    @staticmethod
    def bstack1ll1ll11l1l_opy_(method_name: str):
        return True
    @staticmethod
    def bstack1ll1l11l1l1_opy_(method_name: str, *args) -> bool:
        return True
    @staticmethod
    def bstack1ll1ll1ll1l_opy_(instance: bstack11111l11ll_opy_, default_value=None):
        return bstack11111ll1l1_opy_.bstack11111l1l1l_opy_(instance, bstack1llllll11ll_opy_.bstack1l1ll1l1lll_opy_, default_value)
    @staticmethod
    def bstack1ll1l1111ll_opy_(instance: bstack11111l11ll_opy_) -> bool:
        return True
    @staticmethod
    def bstack1ll1lll1111_opy_(instance: bstack11111l11ll_opy_, default_value=None):
        return bstack11111ll1l1_opy_.bstack11111l1l1l_opy_(instance, bstack1llllll11ll_opy_.bstack1l1ll1llll1_opy_, default_value)
    @staticmethod
    def bstack1ll1ll1l111_opy_(*args):
        return args[0] if args and type(args) in [list, tuple] and isinstance(args[0], str) else None
    @staticmethod
    def bstack1ll1ll1l1ll_opy_(method_name: str, *args):
        if not bstack1llllll11ll_opy_.bstack1ll1ll11l1l_opy_(method_name):
            return False
        if not bstack1llllll11ll_opy_.bstack1l1l11l1l1l_opy_ in bstack1llllll11ll_opy_.bstack1l1l1llll1l_opy_(*args):
            return False
        bstack1ll1l11111l_opy_ = bstack1llllll11ll_opy_.bstack1ll11lll1l1_opy_(*args)
        return bstack1ll1l11111l_opy_ and bstack11l1l11_opy_ (u"ࠧࡹࡣࡳ࡫ࡳࡸࠧፅ") in bstack1ll1l11111l_opy_ and bstack11l1l11_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸࠢፆ") in bstack1ll1l11111l_opy_[bstack11l1l11_opy_ (u"ࠢࡴࡥࡵ࡭ࡵࡺࠢፇ")]
    @staticmethod
    def bstack1ll1l1ll1l1_opy_(method_name: str, *args):
        if not bstack1llllll11ll_opy_.bstack1ll1ll11l1l_opy_(method_name):
            return False
        if not bstack1llllll11ll_opy_.bstack1l1l11l1l1l_opy_ in bstack1llllll11ll_opy_.bstack1l1l1llll1l_opy_(*args):
            return False
        bstack1ll1l11111l_opy_ = bstack1llllll11ll_opy_.bstack1ll11lll1l1_opy_(*args)
        return (
            bstack1ll1l11111l_opy_
            and bstack11l1l11_opy_ (u"ࠣࡵࡦࡶ࡮ࡶࡴࠣፈ") in bstack1ll1l11111l_opy_
            and bstack11l1l11_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡠࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡹࡣࡳ࡫ࡳࡸࠧፉ") in bstack1ll1l11111l_opy_[bstack11l1l11_opy_ (u"ࠥࡷࡨࡸࡩࡱࡶࠥፊ")]
        )
    @staticmethod
    def bstack1l1l1llll1l_opy_(*args):
        return str(bstack1llllll11ll_opy_.bstack1ll1ll1l111_opy_(*args)).lower()
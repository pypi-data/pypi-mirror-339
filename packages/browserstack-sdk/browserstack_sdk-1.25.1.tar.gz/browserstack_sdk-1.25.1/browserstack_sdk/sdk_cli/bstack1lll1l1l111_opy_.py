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
class bstack1llll1l1111_opy_(bstack11111lll1l_opy_):
    bstack1l11llllll1_opy_ = bstack1ll1l1_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠥፊ")
    bstack1l1ll111l1l_opy_ = bstack1ll1l1_opy_ (u"ࠦ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧࠦፋ")
    bstack1l1ll1l11ll_opy_ = bstack1ll1l1_opy_ (u"ࠧ࡮ࡵࡣࡡࡸࡶࡱࠨፌ")
    bstack1l1ll111l11_opy_ = bstack1ll1l1_opy_ (u"ࠨࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠧፍ")
    bstack1l1l11111l1_opy_ = bstack1ll1l1_opy_ (u"ࠢࡸ࠵ࡦࡩࡽ࡫ࡣࡶࡶࡨࡷࡨࡸࡩࡱࡶࠥፎ")
    bstack1l1l1111l1l_opy_ = bstack1ll1l1_opy_ (u"ࠣࡹ࠶ࡧࡪࡾࡥࡤࡷࡷࡩࡸࡩࡲࡪࡲࡷࡥࡸࡿ࡮ࡤࠤፏ")
    NAME = bstack1ll1l1_opy_ (u"ࠤࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨፐ")
    bstack1l1l1111ll1_opy_: Dict[str, List[Callable]] = dict()
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1lll1ll1111_opy_: Any
    bstack1l11lllllll_opy_: Dict
    def __init__(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        methods=[bstack1ll1l1_opy_ (u"ࠥࡰࡦࡻ࡮ࡤࡪࠥፑ"), bstack1ll1l1_opy_ (u"ࠦࡨࡵ࡮࡯ࡧࡦࡸࠧፒ"), bstack1ll1l1_opy_ (u"ࠧࡴࡥࡸࡡࡳࡥ࡬࡫ࠢፓ"), bstack1ll1l1_opy_ (u"ࠨࡣ࡭ࡱࡶࡩࠧፔ"), bstack1ll1l1_opy_ (u"ࠢࡥ࡫ࡶࡴࡦࡺࡣࡩࠤፕ")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.platform_index = platform_index
        self.bstack11111llll1_opy_(methods)
    def bstack1111l11ll1_opy_(self, instance: bstack1llllllllll_opy_, method_name: str, bstack11111lll11_opy_: timedelta, *args, **kwargs):
        pass
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
        bstack1l1l11111ll_opy_ = bstack1llll1l1111_opy_.bstack1l1l111111l_opy_(bstack1111l1l11l_opy_)
        if bstack1l1l11111ll_opy_ in bstack1llll1l1111_opy_.bstack1l1l1111ll1_opy_:
            bstack1l1l1111lll_opy_ = None
            for callback in bstack1llll1l1111_opy_.bstack1l1l1111ll1_opy_[bstack1l1l11111ll_opy_]:
                try:
                    bstack1l1l1111111_opy_ = callback(self, target, exec, bstack1111l1l11l_opy_, result, *args, **kwargs)
                    if bstack1l1l1111lll_opy_ == None:
                        bstack1l1l1111lll_opy_ = bstack1l1l1111111_opy_
                except Exception as e:
                    self.logger.error(bstack1ll1l1_opy_ (u"ࠣࡧࡵࡶࡴࡸࠠࡪࡰࡹࡳࡰ࡯࡮ࡨࠢࡦࡥࡱࡲࡢࡢࡥ࡮࠾ࠥࠨፖ") + str(e) + bstack1ll1l1_opy_ (u"ࠤࠥፗ"))
                    traceback.print_exc()
            if bstack1l1l1111l11_opy_ == bstack1111l1l1l1_opy_.PRE and callable(bstack1l1l1111lll_opy_):
                return bstack1l1l1111lll_opy_
            elif bstack1l1l1111l11_opy_ == bstack1111l1l1l1_opy_.POST and bstack1l1l1111lll_opy_:
                return bstack1l1l1111lll_opy_
    def bstack111111l111_opy_(
        self, method_name, previous_state: bstack11111ll1l1_opy_, *args, **kwargs
    ) -> bstack11111ll1l1_opy_:
        if method_name == bstack1ll1l1_opy_ (u"ࠪࡰࡦࡻ࡮ࡤࡪࠪፘ") or method_name == bstack1ll1l1_opy_ (u"ࠫࡨࡵ࡮࡯ࡧࡦࡸࠬፙ") or method_name == bstack1ll1l1_opy_ (u"ࠬࡴࡥࡸࡡࡳࡥ࡬࡫ࠧፚ"):
            return bstack11111ll1l1_opy_.bstack1111l1111l_opy_
        if method_name == bstack1ll1l1_opy_ (u"࠭ࡤࡪࡵࡳࡥࡹࡩࡨࠨ፛"):
            return bstack11111ll1l1_opy_.bstack11111ll11l_opy_
        if method_name == bstack1ll1l1_opy_ (u"ࠧࡤ࡮ࡲࡷࡪ࠭፜"):
            return bstack11111ll1l1_opy_.QUIT
        return bstack11111ll1l1_opy_.NONE
    @staticmethod
    def bstack1l1l111111l_opy_(bstack1111l1l11l_opy_: Tuple[bstack11111ll1l1_opy_, bstack1111l1l1l1_opy_]):
        return bstack1ll1l1_opy_ (u"ࠣ࠼ࠥ፝").join((bstack11111ll1l1_opy_(bstack1111l1l11l_opy_[0]).name, bstack1111l1l1l1_opy_(bstack1111l1l11l_opy_[1]).name))
    @staticmethod
    def bstack1ll1l11l1l1_opy_(bstack1111l1l11l_opy_: Tuple[bstack11111ll1l1_opy_, bstack1111l1l1l1_opy_], callback: Callable):
        bstack1l1l11111ll_opy_ = bstack1llll1l1111_opy_.bstack1l1l111111l_opy_(bstack1111l1l11l_opy_)
        if not bstack1l1l11111ll_opy_ in bstack1llll1l1111_opy_.bstack1l1l1111ll1_opy_:
            bstack1llll1l1111_opy_.bstack1l1l1111ll1_opy_[bstack1l1l11111ll_opy_] = []
        bstack1llll1l1111_opy_.bstack1l1l1111ll1_opy_[bstack1l1l11111ll_opy_].append(callback)
    @staticmethod
    def bstack1ll1l1llll1_opy_(method_name: str):
        return True
    @staticmethod
    def bstack1ll11llllll_opy_(method_name: str, *args) -> bool:
        return True
    @staticmethod
    def bstack1ll1lll1111_opy_(instance: bstack1llllllllll_opy_, default_value=None):
        return bstack11111lll1l_opy_.bstack11111lllll_opy_(instance, bstack1llll1l1111_opy_.bstack1l1ll111l11_opy_, default_value)
    @staticmethod
    def bstack1ll1l1l1ll1_opy_(instance: bstack1llllllllll_opy_) -> bool:
        return True
    @staticmethod
    def bstack1ll1l11111l_opy_(instance: bstack1llllllllll_opy_, default_value=None):
        return bstack11111lll1l_opy_.bstack11111lllll_opy_(instance, bstack1llll1l1111_opy_.bstack1l1ll1l11ll_opy_, default_value)
    @staticmethod
    def bstack1ll1l1ll111_opy_(*args):
        return args[0] if args and type(args) in [list, tuple] and isinstance(args[0], str) else None
    @staticmethod
    def bstack1ll1l111lll_opy_(method_name: str, *args):
        if not bstack1llll1l1111_opy_.bstack1ll1l1llll1_opy_(method_name):
            return False
        if not bstack1llll1l1111_opy_.bstack1l1l11111l1_opy_ in bstack1llll1l1111_opy_.bstack1l1l1l1l1ll_opy_(*args):
            return False
        bstack1ll11ll1lll_opy_ = bstack1llll1l1111_opy_.bstack1ll11ll11l1_opy_(*args)
        return bstack1ll11ll1lll_opy_ and bstack1ll1l1_opy_ (u"ࠤࡶࡧࡷ࡯ࡰࡵࠤ፞") in bstack1ll11ll1lll_opy_ and bstack1ll1l1_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵࠦ፟") in bstack1ll11ll1lll_opy_[bstack1ll1l1_opy_ (u"ࠦࡸࡩࡲࡪࡲࡷࠦ፠")]
    @staticmethod
    def bstack1ll1ll1l111_opy_(method_name: str, *args):
        if not bstack1llll1l1111_opy_.bstack1ll1l1llll1_opy_(method_name):
            return False
        if not bstack1llll1l1111_opy_.bstack1l1l11111l1_opy_ in bstack1llll1l1111_opy_.bstack1l1l1l1l1ll_opy_(*args):
            return False
        bstack1ll11ll1lll_opy_ = bstack1llll1l1111_opy_.bstack1ll11ll11l1_opy_(*args)
        return (
            bstack1ll11ll1lll_opy_
            and bstack1ll1l1_opy_ (u"ࠧࡹࡣࡳ࡫ࡳࡸࠧ፡") in bstack1ll11ll1lll_opy_
            and bstack1ll1l1_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡤࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡶࡧࡷ࡯ࡰࡵࠤ።") in bstack1ll11ll1lll_opy_[bstack1ll1l1_opy_ (u"ࠢࡴࡥࡵ࡭ࡵࡺࠢ፣")]
        )
    @staticmethod
    def bstack1l1l1l1l1ll_opy_(*args):
        return str(bstack1llll1l1111_opy_.bstack1ll1l1ll111_opy_(*args)).lower()
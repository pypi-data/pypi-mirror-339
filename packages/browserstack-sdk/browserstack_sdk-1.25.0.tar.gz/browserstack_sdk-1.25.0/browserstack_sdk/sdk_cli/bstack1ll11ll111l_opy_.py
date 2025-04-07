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
from browserstack_sdk.sdk_cli.bstack1lll11llll1_opy_ import bstack1lllll1l111_opy_
from browserstack_sdk.sdk_cli.bstack1111l11lll_opy_ import (
    bstack1111l1ll1l_opy_,
    bstack111111111l_opy_,
    bstack11111ll1l1_opy_,
    bstack11111l11ll_opy_,
)
from browserstack_sdk.sdk_cli.bstack1lllll1ll11_opy_ import bstack1lll1l11ll1_opy_
from browserstack_sdk.sdk_cli.bstack1llll1111l1_opy_ import bstack1llllll11ll_opy_
from browserstack_sdk.sdk_cli.bstack11111111l1_opy_ import bstack11111l1111_opy_
from typing import Tuple, Dict, Any, List, Callable
from browserstack_sdk.sdk_cli.bstack1lll11llll1_opy_ import bstack1lllll1l111_opy_
import weakref
class bstack1ll11l1llll_opy_(bstack1lllll1l111_opy_):
    bstack1ll11ll11l1_opy_: str
    frameworks: List[str]
    drivers: Dict[str, Tuple[Callable, bstack11111l11ll_opy_]]
    pages: Dict[str, Tuple[Callable, bstack11111l11ll_opy_]]
    def __init__(self, bstack1ll11ll11l1_opy_: str, frameworks: List[str]):
        super().__init__()
        self.drivers = dict()
        self.pages = dict()
        self.bstack1ll11l1l1l1_opy_ = dict()
        self.bstack1ll11ll11l1_opy_ = bstack1ll11ll11l1_opy_
        self.frameworks = frameworks
        bstack1llllll11ll_opy_.bstack1ll1l11l11l_opy_((bstack1111l1ll1l_opy_.bstack111111ll11_opy_, bstack111111111l_opy_.POST), self.__1ll11ll1ll1_opy_)
        if any(bstack1lll1l11ll1_opy_.NAME in f.lower().strip() for f in frameworks):
            bstack1lll1l11ll1_opy_.bstack1ll1l11l11l_opy_(
                (bstack1111l1ll1l_opy_.bstack111111l111_opy_, bstack111111111l_opy_.PRE), self.__1ll11ll1111_opy_
            )
            bstack1lll1l11ll1_opy_.bstack1ll1l11l11l_opy_(
                (bstack1111l1ll1l_opy_.QUIT, bstack111111111l_opy_.POST), self.__1ll11l1lll1_opy_
            )
    def __1ll11ll1ll1_opy_(
        self,
        f: bstack1llllll11ll_opy_,
        bstack1ll11ll1l1l_opy_: object,
        exec: Tuple[bstack11111l11ll_opy_, str],
        bstack1111l1ll11_opy_: Tuple[bstack1111l1ll1l_opy_, bstack111111111l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if method_name != bstack11l1l11_opy_ (u"ࠦࡳ࡫ࡷࡠࡲࡤ࡫ࡪࠨᆠ"):
                return
            contexts = bstack1ll11ll1l1l_opy_.browser.contexts
            if contexts:
                for context in contexts:
                    if context.pages:
                        for page in context.pages:
                            if bstack11l1l11_opy_ (u"ࠧࡧࡢࡰࡷࡷ࠾ࡧࡲࡡ࡯࡭ࠥᆡ") in page.url:
                                self.logger.debug(bstack11l1l11_opy_ (u"ࠨࡓࡵࡱࡵ࡭ࡳ࡭ࠠࡵࡪࡨࠤࡳ࡫ࡷࠡࡲࡤ࡫ࡪࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࠣᆢ"))
                                self.pages[instance.ref()] = weakref.ref(page), instance
                                bstack11111ll1l1_opy_.bstack1111111l1l_opy_(instance, self.bstack1ll11ll11l1_opy_, True)
                                self.logger.debug(bstack11l1l11_opy_ (u"ࠢࡠࡡࡲࡲࡤࡶࡡࡨࡧࡢ࡭ࡳ࡯ࡴ࠻ࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࠧᆣ") + str(instance.ref()) + bstack11l1l11_opy_ (u"ࠣࠤᆤ"))
        except Exception as e:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡵࡷࡳࡷ࡯࡮ࡨࠢࡱࡩࡼࠦࡰࡢࡩࡨࠤ࠿ࠨᆥ"),e)
    def __1ll11ll1111_opy_(
        self,
        f: bstack1lll1l11ll1_opy_,
        driver: object,
        exec: Tuple[bstack11111l11ll_opy_, str],
        bstack1111l1ll11_opy_: Tuple[bstack1111l1ll1l_opy_, bstack111111111l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if instance.ref() in self.drivers or bstack11111ll1l1_opy_.bstack11111l1l1l_opy_(instance, self.bstack1ll11ll11l1_opy_, False):
            return
        if not f.bstack1ll11lll1ll_opy_(f.hub_url(driver)):
            self.bstack1ll11l1l1l1_opy_[instance.ref()] = weakref.ref(driver), instance
            bstack11111ll1l1_opy_.bstack1111111l1l_opy_(instance, self.bstack1ll11ll11l1_opy_, True)
            self.logger.debug(bstack11l1l11_opy_ (u"ࠥࡣࡤࡵ࡮ࡠࡵࡨࡰࡪࡴࡩࡶ࡯ࡢ࡭ࡳ࡯ࡴ࠻ࠢࡱࡳࡳࡥࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤࡪࡲࡪࡸࡨࡶࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࠣᆦ") + str(instance.ref()) + bstack11l1l11_opy_ (u"ࠦࠧᆧ"))
            return
        self.drivers[instance.ref()] = weakref.ref(driver), instance
        bstack11111ll1l1_opy_.bstack1111111l1l_opy_(instance, self.bstack1ll11ll11l1_opy_, True)
        self.logger.debug(bstack11l1l11_opy_ (u"ࠧࡥ࡟ࡰࡰࡢࡷࡪࡲࡥ࡯࡫ࡸࡱࡤ࡯࡮ࡪࡶ࠽ࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࠢᆨ") + str(instance.ref()) + bstack11l1l11_opy_ (u"ࠨࠢᆩ"))
    def __1ll11l1lll1_opy_(
        self,
        f: bstack1lll1l11ll1_opy_,
        driver: object,
        exec: Tuple[bstack11111l11ll_opy_, str],
        bstack1111l1ll11_opy_: Tuple[bstack1111l1ll1l_opy_, bstack111111111l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if not instance.ref() in self.drivers:
            return
        self.bstack1ll11l1l1ll_opy_(instance)
        self.logger.debug(bstack11l1l11_opy_ (u"ࠢࡠࡡࡲࡲࡤࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࡟ࡲࡷ࡬ࡸ࠿ࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࠤᆪ") + str(instance.ref()) + bstack11l1l11_opy_ (u"ࠣࠤᆫ"))
    def bstack1ll11ll11ll_opy_(self, context: bstack11111l1111_opy_, reverse=True) -> List[Tuple[Callable, bstack11111l11ll_opy_]]:
        matches = []
        if self.pages:
            for data in self.pages.values():
                if data[1].bstack1ll11l1ll1l_opy_(context):
                    matches.append(data)
        if self.drivers:
            for data in self.drivers.values():
                if (
                    bstack1lll1l11ll1_opy_.bstack1ll1l1111ll_opy_(data[1])
                    and data[1].bstack1ll11l1ll1l_opy_(context)
                    and getattr(data[0](), bstack11l1l11_opy_ (u"ࠤࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩࠨᆬ"), False)
                ):
                    matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack11111l1l11_opy_, reverse=reverse)
    def bstack1ll11l1ll11_opy_(self, context: bstack11111l1111_opy_, reverse=True) -> List[Tuple[Callable, bstack11111l11ll_opy_]]:
        matches = []
        for data in self.bstack1ll11l1l1l1_opy_.values():
            if (
                data[1].bstack1ll11l1ll1l_opy_(context)
                and getattr(data[0](), bstack11l1l11_opy_ (u"ࠥࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪࠢᆭ"), False)
            ):
                matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack11111l1l11_opy_, reverse=reverse)
    def bstack1ll11ll1l11_opy_(self, instance: bstack11111l11ll_opy_) -> bool:
        return instance and instance.ref() in self.drivers
    def bstack1ll11l1l1ll_opy_(self, instance: bstack11111l11ll_opy_) -> bool:
        if self.bstack1ll11ll1l11_opy_(instance):
            self.drivers.pop(instance.ref())
            bstack11111ll1l1_opy_.bstack1111111l1l_opy_(instance, self.bstack1ll11ll11l1_opy_, False)
            return True
        return False
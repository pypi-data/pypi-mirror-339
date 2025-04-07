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
import threading
from bstack_utils.helper import bstack1ll11l1l1_opy_
from bstack_utils.constants import bstack11llll1llll_opy_, EVENTS, STAGE
from bstack_utils.bstack111ll1l11_opy_ import get_logger
logger = get_logger(__name__)
class bstack11l11l11_opy_:
    bstack111ll1lll1l_opy_ = None
    @classmethod
    def bstack11l11lllll_opy_(cls):
        if cls.on() and os.getenv(bstack11l1l11_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉࠨẓ")):
            logger.info(
                bstack11l1l11_opy_ (u"࡙ࠩ࡭ࡸ࡯ࡴࠡࡪࡷࡸࡵࡹ࠺࠰࠱ࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡨࡵࡪ࡮ࡧࡷ࠴ࢁࡽࠡࡶࡲࠤࡻ࡯ࡥࡸࠢࡥࡹ࡮ࡲࡤࠡࡴࡨࡴࡴࡸࡴ࠭ࠢ࡬ࡲࡸ࡯ࡧࡩࡶࡶ࠰ࠥࡧ࡮ࡥࠢࡰࡥࡳࡿࠠ࡮ࡱࡵࡩࠥࡪࡥࡣࡷࡪ࡫࡮ࡴࡧࠡ࡫ࡱࡪࡴࡸ࡭ࡢࡶ࡬ࡳࡳࠦࡡ࡭࡮ࠣࡥࡹࠦ࡯࡯ࡧࠣࡴࡱࡧࡣࡦࠣ࡟ࡲࠬẔ").format(os.getenv(bstack11l1l11_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠣẕ"))))
    @classmethod
    def on(cls):
        if os.environ.get(bstack11l1l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨẖ"), None) is None or os.environ[bstack11l1l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩẗ")] == bstack11l1l11_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦẘ"):
            return False
        return True
    @classmethod
    def bstack111l11ll111_opy_(cls, bs_config, framework=bstack11l1l11_opy_ (u"ࠢࠣẙ")):
        bstack1l1111111ll_opy_ = False
        for fw in bstack11llll1llll_opy_:
            if fw in framework:
                bstack1l1111111ll_opy_ = True
        return bstack1ll11l1l1_opy_(bs_config.get(bstack11l1l11_opy_ (u"ࠨࡶࡨࡷࡹࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬẚ"), bstack1l1111111ll_opy_))
    @classmethod
    def bstack111l111lll1_opy_(cls, framework):
        return framework in bstack11llll1llll_opy_
    @classmethod
    def bstack111l11llll1_opy_(cls, bs_config, framework):
        return cls.bstack111l11ll111_opy_(bs_config, framework) is True and cls.bstack111l111lll1_opy_(framework)
    @staticmethod
    def current_hook_uuid():
        return getattr(threading.current_thread(), bstack11l1l11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭ẛ"), None)
    @staticmethod
    def bstack11l111lll1_opy_():
        if getattr(threading.current_thread(), bstack11l1l11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧẜ"), None):
            return {
                bstack11l1l11_opy_ (u"ࠫࡹࡿࡰࡦࠩẝ"): bstack11l1l11_opy_ (u"ࠬࡺࡥࡴࡶࠪẞ"),
                bstack11l1l11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ẟ"): getattr(threading.current_thread(), bstack11l1l11_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫẠ"), None)
            }
        if getattr(threading.current_thread(), bstack11l1l11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬạ"), None):
            return {
                bstack11l1l11_opy_ (u"ࠩࡷࡽࡵ࡫ࠧẢ"): bstack11l1l11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨả"),
                bstack11l1l11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫẤ"): getattr(threading.current_thread(), bstack11l1l11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩấ"), None)
            }
        return None
    @staticmethod
    def bstack111l111l1l1_opy_(func):
        def wrap(*args, **kwargs):
            if bstack11l11l11_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack111l1l111l_opy_(test, hook_name=None):
        bstack111l111l1ll_opy_ = test.parent
        if hook_name in [bstack11l1l11_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡩ࡬ࡢࡵࡶࠫẦ"), bstack11l1l11_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡦࡰࡦࡹࡳࠨầ"), bstack11l1l11_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡱࡧࡹࡱ࡫ࠧẨ"), bstack11l1l11_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲࡵࡤࡶ࡮ࡨࠫẩ")]:
            bstack111l111l1ll_opy_ = test
        scope = []
        while bstack111l111l1ll_opy_ is not None:
            scope.append(bstack111l111l1ll_opy_.name)
            bstack111l111l1ll_opy_ = bstack111l111l1ll_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack111l111ll1l_opy_(hook_type):
        if hook_type == bstack11l1l11_opy_ (u"ࠥࡆࡊࡌࡏࡓࡇࡢࡉࡆࡉࡈࠣẪ"):
            return bstack11l1l11_opy_ (u"ࠦࡘ࡫ࡴࡶࡲࠣ࡬ࡴࡵ࡫ࠣẫ")
        elif hook_type == bstack11l1l11_opy_ (u"ࠧࡇࡆࡕࡇࡕࡣࡊࡇࡃࡉࠤẬ"):
            return bstack11l1l11_opy_ (u"ࠨࡔࡦࡣࡵࡨࡴࡽ࡮ࠡࡪࡲࡳࡰࠨậ")
    @staticmethod
    def bstack111l111ll11_opy_(bstack1l11l1l111_opy_):
        try:
            if not bstack11l11l11_opy_.on():
                return bstack1l11l1l111_opy_
            if os.environ.get(bstack11l1l11_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡒࡆࡔࡘࡒࠧẮ"), None) == bstack11l1l11_opy_ (u"ࠣࡶࡵࡹࡪࠨắ"):
                tests = os.environ.get(bstack11l1l11_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡔࡈࡖ࡚ࡔ࡟ࡕࡇࡖࡘࡘࠨẰ"), None)
                if tests is None or tests == bstack11l1l11_opy_ (u"ࠥࡲࡺࡲ࡬ࠣằ"):
                    return bstack1l11l1l111_opy_
                bstack1l11l1l111_opy_ = tests.split(bstack11l1l11_opy_ (u"ࠫ࠱࠭Ẳ"))
                return bstack1l11l1l111_opy_
        except Exception as exc:
            logger.debug(bstack11l1l11_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡷ࡫ࡲࡶࡰࠣ࡬ࡦࡴࡤ࡭ࡧࡵ࠾ࠥࠨẳ") + str(str(exc)) + bstack11l1l11_opy_ (u"ࠨࠢẴ"))
        return bstack1l11l1l111_opy_
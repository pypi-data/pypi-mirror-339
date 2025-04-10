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
import threading
from bstack_utils.helper import bstack11l11l1ll_opy_
from bstack_utils.constants import bstack11ll1l11ll1_opy_, EVENTS, STAGE
from bstack_utils.bstack1l1ll1111l_opy_ import get_logger
logger = get_logger(__name__)
class bstack11l1ll1ll_opy_:
    bstack111l11lllll_opy_ = None
    @classmethod
    def bstack1lll1ll1_opy_(cls):
        if cls.on() and os.getenv(bstack1ll1l1_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠤἢ")):
            logger.info(
                bstack1ll1l1_opy_ (u"ࠬ࡜ࡩࡴ࡫ࡷࠤ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡤࡸ࡭ࡱࡪࡳ࠰ࡽࢀࠤࡹࡵࠠࡷ࡫ࡨࡻࠥࡨࡵࡪ࡮ࡧࠤࡷ࡫ࡰࡰࡴࡷ࠰ࠥ࡯࡮ࡴ࡫ࡪ࡬ࡹࡹࠬࠡࡣࡱࡨࠥࡳࡡ࡯ࡻࠣࡱࡴࡸࡥࠡࡦࡨࡦࡺ࡭ࡧࡪࡰࡪࠤ࡮ࡴࡦࡰࡴࡰࡥࡹ࡯࡯࡯ࠢࡤࡰࡱࠦࡡࡵࠢࡲࡲࡪࠦࡰ࡭ࡣࡦࡩࠦࡢ࡮ࠨἣ").format(os.getenv(bstack1ll1l1_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠦἤ"))))
    @classmethod
    def on(cls):
        if os.environ.get(bstack1ll1l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫἥ"), None) is None or os.environ[bstack1ll1l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬἦ")] == bstack1ll1l1_opy_ (u"ࠤࡱࡹࡱࡲࠢἧ"):
            return False
        return True
    @classmethod
    def bstack1111l1lll1l_opy_(cls, bs_config, framework=bstack1ll1l1_opy_ (u"ࠥࠦἨ")):
        bstack11lll11l11l_opy_ = False
        for fw in bstack11ll1l11ll1_opy_:
            if fw in framework:
                bstack11lll11l11l_opy_ = True
        return bstack11l11l1ll_opy_(bs_config.get(bstack1ll1l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡑࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨἩ"), bstack11lll11l11l_opy_))
    @classmethod
    def bstack1111l1l1l1l_opy_(cls, framework):
        return framework in bstack11ll1l11ll1_opy_
    @classmethod
    def bstack1111ll111ll_opy_(cls, bs_config, framework):
        return cls.bstack1111l1lll1l_opy_(bs_config, framework) is True and cls.bstack1111l1l1l1l_opy_(framework)
    @staticmethod
    def current_hook_uuid():
        return getattr(threading.current_thread(), bstack1ll1l1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩἪ"), None)
    @staticmethod
    def bstack11l111ll11_opy_():
        if getattr(threading.current_thread(), bstack1ll1l1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪἫ"), None):
            return {
                bstack1ll1l1_opy_ (u"ࠧࡵࡻࡳࡩࠬἬ"): bstack1ll1l1_opy_ (u"ࠨࡶࡨࡷࡹ࠭Ἥ"),
                bstack1ll1l1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩἮ"): getattr(threading.current_thread(), bstack1ll1l1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧἯ"), None)
            }
        if getattr(threading.current_thread(), bstack1ll1l1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨἰ"), None):
            return {
                bstack1ll1l1_opy_ (u"ࠬࡺࡹࡱࡧࠪἱ"): bstack1ll1l1_opy_ (u"࠭ࡨࡰࡱ࡮ࠫἲ"),
                bstack1ll1l1_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧἳ"): getattr(threading.current_thread(), bstack1ll1l1_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬἴ"), None)
            }
        return None
    @staticmethod
    def bstack1111l1l111l_opy_(func):
        def wrap(*args, **kwargs):
            if bstack11l1ll1ll_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack111l1l1l1l_opy_(test, hook_name=None):
        bstack1111l1l11l1_opy_ = test.parent
        if hook_name in [bstack1ll1l1_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠࡥ࡯ࡥࡸࡹࠧἵ"), bstack1ll1l1_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡩ࡬ࡢࡵࡶࠫἶ"), bstack1ll1l1_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡴࡪࡵ࡭ࡧࠪἷ"), bstack1ll1l1_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡱࡧࡹࡱ࡫ࠧἸ")]:
            bstack1111l1l11l1_opy_ = test
        scope = []
        while bstack1111l1l11l1_opy_ is not None:
            scope.append(bstack1111l1l11l1_opy_.name)
            bstack1111l1l11l1_opy_ = bstack1111l1l11l1_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack1111l1l11ll_opy_(hook_type):
        if hook_type == bstack1ll1l1_opy_ (u"ࠨࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠦἹ"):
            return bstack1ll1l1_opy_ (u"ࠢࡔࡧࡷࡹࡵࠦࡨࡰࡱ࡮ࠦἺ")
        elif hook_type == bstack1ll1l1_opy_ (u"ࠣࡃࡉࡘࡊࡘ࡟ࡆࡃࡆࡌࠧἻ"):
            return bstack1ll1l1_opy_ (u"ࠤࡗࡩࡦࡸࡤࡰࡹࡱࠤ࡭ࡵ࡯࡬ࠤἼ")
    @staticmethod
    def bstack1111l1l1l11_opy_(bstack1lllllll1l_opy_):
        try:
            if not bstack11l1ll1ll_opy_.on():
                return bstack1lllllll1l_opy_
            if os.environ.get(bstack1ll1l1_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡕࡉࡗ࡛ࡎࠣἽ"), None) == bstack1ll1l1_opy_ (u"ࠦࡹࡸࡵࡦࠤἾ"):
                tests = os.environ.get(bstack1ll1l1_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡗࡋࡒࡖࡐࡢࡘࡊ࡙ࡔࡔࠤἿ"), None)
                if tests is None or tests == bstack1ll1l1_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦὀ"):
                    return bstack1lllllll1l_opy_
                bstack1lllllll1l_opy_ = tests.split(bstack1ll1l1_opy_ (u"ࠧ࠭ࠩὁ"))
                return bstack1lllllll1l_opy_
        except Exception as exc:
            logger.debug(bstack1ll1l1_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡳࡧࡵࡹࡳࠦࡨࡢࡰࡧࡰࡪࡸ࠺ࠡࠤὂ") + str(str(exc)) + bstack1ll1l1_opy_ (u"ࠤࠥὃ"))
        return bstack1lllllll1l_opy_
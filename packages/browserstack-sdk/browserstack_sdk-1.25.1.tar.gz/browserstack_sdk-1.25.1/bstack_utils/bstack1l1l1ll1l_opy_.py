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
from browserstack_sdk.bstack1ll11l1l1l_opy_ import bstack1111l111_opy_
from browserstack_sdk.bstack111l11l1l1_opy_ import RobotHandler
def bstack1l111ll1l1_opy_(framework):
    if framework.lower() == bstack1ll1l1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨᦒ"):
        return bstack1111l111_opy_.version()
    elif framework.lower() == bstack1ll1l1_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨᦓ"):
        return RobotHandler.version()
    elif framework.lower() == bstack1ll1l1_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪᦔ"):
        import behave
        return behave.__version__
    else:
        return bstack1ll1l1_opy_ (u"ࠫࡺࡴ࡫࡯ࡱࡺࡲࠬᦕ")
def bstack1l11lllll1_opy_():
    import importlib.metadata
    framework_name = []
    framework_version = []
    try:
        from selenium import webdriver
        framework_name.append(bstack1ll1l1_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠧᦖ"))
        framework_version.append(importlib.metadata.version(bstack1ll1l1_opy_ (u"ࠨࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠣᦗ")))
    except:
        pass
    try:
        import playwright
        framework_name.append(bstack1ll1l1_opy_ (u"ࠧࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠫᦘ"))
        framework_version.append(importlib.metadata.version(bstack1ll1l1_opy_ (u"ࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧᦙ")))
    except:
        pass
    return {
        bstack1ll1l1_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᦚ"): bstack1ll1l1_opy_ (u"ࠪࡣࠬᦛ").join(framework_name),
        bstack1ll1l1_opy_ (u"ࠫࡻ࡫ࡲࡴ࡫ࡲࡲࠬᦜ"): bstack1ll1l1_opy_ (u"ࠬࡥࠧᦝ").join(framework_version)
    }
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
from browserstack_sdk.bstack11l1llll11_opy_ import bstack11ll111l_opy_
from browserstack_sdk.bstack111lll111l_opy_ import RobotHandler
def bstack1l1ll1l1l1_opy_(framework):
    if framework.lower() == bstack11l1l11_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬᤃ"):
        return bstack11ll111l_opy_.version()
    elif framework.lower() == bstack11l1l11_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬᤄ"):
        return RobotHandler.version()
    elif framework.lower() == bstack11l1l11_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧᤅ"):
        import behave
        return behave.__version__
    else:
        return bstack11l1l11_opy_ (u"ࠨࡷࡱ࡯ࡳࡵࡷ࡯ࠩᤆ")
def bstack11l1lll1_opy_():
    import importlib.metadata
    framework_name = []
    framework_version = []
    try:
        from selenium import webdriver
        framework_name.append(bstack11l1l11_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰࠫᤇ"))
        framework_version.append(importlib.metadata.version(bstack11l1l11_opy_ (u"ࠥࡷࡪࡲࡥ࡯࡫ࡸࡱࠧᤈ")))
    except:
        pass
    try:
        import playwright
        framework_name.append(bstack11l1l11_opy_ (u"ࠫࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠨᤉ"))
        framework_version.append(importlib.metadata.version(bstack11l1l11_opy_ (u"ࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤᤊ")))
    except:
        pass
    return {
        bstack11l1l11_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᤋ"): bstack11l1l11_opy_ (u"ࠧࡠࠩᤌ").join(framework_name),
        bstack11l1l11_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯ࠩᤍ"): bstack11l1l11_opy_ (u"ࠩࡢࠫᤎ").join(framework_version)
    }
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
import re
from bstack_utils.bstack1l1lllll_opy_ import bstack111l1l11lll_opy_
def bstack111l1ll11ll_opy_(fixture_name):
    if fixture_name.startswith(bstack1ll1l1_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡸ࡫ࡴࡶࡲࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᴪ")):
        return bstack1ll1l1_opy_ (u"ࠬࡹࡥࡵࡷࡳ࠱࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭ᴫ")
    elif fixture_name.startswith(bstack1ll1l1_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡳࡦࡶࡸࡴࡤࡳ࡯ࡥࡷ࡯ࡩࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᴬ")):
        return bstack1ll1l1_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠳࡭ࡰࡦࡸࡰࡪ࠭ᴭ")
    elif fixture_name.startswith(bstack1ll1l1_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᴮ")):
        return bstack1ll1l1_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱ࠱࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭ᴯ")
    elif fixture_name.startswith(bstack1ll1l1_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡸࡪࡧࡲࡥࡱࡺࡲࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᴰ")):
        return bstack1ll1l1_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠳࡭ࡰࡦࡸࡰࡪ࠭ᴱ")
def bstack111l1l1ll1l_opy_(fixture_name):
    return bool(re.match(bstack1ll1l1_opy_ (u"ࠬࡤ࡟ࡹࡷࡱ࡭ࡹࡥࠨࡴࡧࡷࡹࡵࢂࡴࡦࡣࡵࡨࡴࡽ࡮ࠪࡡࠫࡪࡺࡴࡣࡵ࡫ࡲࡲࢁࡳ࡯ࡥࡷ࡯ࡩ࠮ࡥࡦࡪࡺࡷࡹࡷ࡫࡟࠯ࠬࠪᴲ"), fixture_name))
def bstack111l1l1l1l1_opy_(fixture_name):
    return bool(re.match(bstack1ll1l1_opy_ (u"࠭࡞ࡠࡺࡸࡲ࡮ࡺ࡟ࠩࡵࡨࡸࡺࡶࡼࡵࡧࡤࡶࡩࡵࡷ࡯ࠫࡢࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨࡣ࠳࠰ࠧᴳ"), fixture_name))
def bstack111l1l1llll_opy_(fixture_name):
    return bool(re.match(bstack1ll1l1_opy_ (u"ࠧ࡟ࡡࡻࡹࡳ࡯ࡴࡠࠪࡶࡩࡹࡻࡰࡽࡶࡨࡥࡷࡪ࡯ࡸࡰࠬࡣࡨࡲࡡࡴࡵࡢࡪ࡮ࡾࡴࡶࡴࡨࡣ࠳࠰ࠧᴴ"), fixture_name))
def bstack111l1l11ll1_opy_(fixture_name):
    if fixture_name.startswith(bstack1ll1l1_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡵࡨࡸࡺࡶ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᴵ")):
        return bstack1ll1l1_opy_ (u"ࠩࡶࡩࡹࡻࡰ࠮ࡨࡸࡲࡨࡺࡩࡰࡰࠪᴶ"), bstack1ll1l1_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡉࡆࡉࡈࠨᴷ")
    elif fixture_name.startswith(bstack1ll1l1_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡸ࡫ࡴࡶࡲࡢࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᴸ")):
        return bstack1ll1l1_opy_ (u"ࠬࡹࡥࡵࡷࡳ࠱ࡲࡵࡤࡶ࡮ࡨࠫᴹ"), bstack1ll1l1_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡁࡍࡎࠪᴺ")
    elif fixture_name.startswith(bstack1ll1l1_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᴻ")):
        return bstack1ll1l1_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰ࠰ࡪࡺࡴࡣࡵ࡫ࡲࡲࠬᴼ"), bstack1ll1l1_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡇࡄࡇࡍ࠭ᴽ")
    elif fixture_name.startswith(bstack1ll1l1_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳ࡯ࡥࡷ࡯ࡩࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᴾ")):
        return bstack1ll1l1_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠳࡭ࡰࡦࡸࡰࡪ࠭ᴿ"), bstack1ll1l1_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡆࡒࡌࠨᵀ")
    return None, None
def bstack111l1ll1111_opy_(hook_name):
    if hook_name in [bstack1ll1l1_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬᵁ"), bstack1ll1l1_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩᵂ")]:
        return hook_name.capitalize()
    return hook_name
def bstack111l1l1lll1_opy_(hook_name):
    if hook_name in [bstack1ll1l1_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩᵃ"), bstack1ll1l1_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠ࡯ࡨࡸ࡭ࡵࡤࠨᵄ")]:
        return bstack1ll1l1_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡉࡆࡉࡈࠨᵅ")
    elif hook_name in [bstack1ll1l1_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡴࡪࡵ࡭ࡧࠪᵆ"), bstack1ll1l1_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡨࡲࡡࡴࡵࠪᵇ")]:
        return bstack1ll1l1_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡁࡍࡎࠪᵈ")
    elif hook_name in [bstack1ll1l1_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡩࡹࡳࡩࡴࡪࡱࡱࠫᵉ"), bstack1ll1l1_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡪࡺࡨࡰࡦࠪᵊ")]:
        return bstack1ll1l1_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡇࡄࡇࡍ࠭ᵋ")
    elif hook_name in [bstack1ll1l1_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳ࡯ࡥࡷ࡯ࡩࠬᵌ"), bstack1ll1l1_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡣ࡭ࡣࡶࡷࠬᵍ")]:
        return bstack1ll1l1_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡆࡒࡌࠨᵎ")
    return hook_name
def bstack111l1l1ll11_opy_(node, scenario):
    if hasattr(node, bstack1ll1l1_opy_ (u"࠭ࡣࡢ࡮࡯ࡷࡵ࡫ࡣࠨᵏ")):
        parts = node.nodeid.rsplit(bstack1ll1l1_opy_ (u"ࠢ࡜ࠤᵐ"))
        params = parts[-1]
        return bstack1ll1l1_opy_ (u"ࠣࡽࢀࠤࡠࢁࡽࠣᵑ").format(scenario.name, params)
    return scenario.name
def bstack111l1l1l1ll_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack1ll1l1_opy_ (u"ࠩࡦࡥࡱࡲࡳࡱࡧࡦࠫᵒ")):
            examples = list(node.callspec.params[bstack1ll1l1_opy_ (u"ࠪࡣࡵࡿࡴࡦࡵࡷࡣࡧࡪࡤࡠࡧࡻࡥࡲࡶ࡬ࡦࠩᵓ")].values())
        return examples
    except:
        return []
def bstack111l1ll11l1_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack111l1ll111l_opy_(report):
    try:
        status = bstack1ll1l1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᵔ")
        if report.passed or (report.failed and hasattr(report, bstack1ll1l1_opy_ (u"ࠧࡽࡡࡴࡺࡩࡥ࡮ࡲࠢᵕ"))):
            status = bstack1ll1l1_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ᵖ")
        elif report.skipped:
            status = bstack1ll1l1_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨᵗ")
        bstack111l1l11lll_opy_(status)
    except:
        pass
def bstack1ll1llll1l_opy_(status):
    try:
        bstack111l1l1l111_opy_ = bstack1ll1l1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᵘ")
        if status == bstack1ll1l1_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩᵙ"):
            bstack111l1l1l111_opy_ = bstack1ll1l1_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪᵚ")
        elif status == bstack1ll1l1_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬᵛ"):
            bstack111l1l1l111_opy_ = bstack1ll1l1_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭ᵜ")
        bstack111l1l11lll_opy_(bstack111l1l1l111_opy_)
    except:
        pass
def bstack111l1l1l11l_opy_(item=None, report=None, summary=None, extra=None):
    return
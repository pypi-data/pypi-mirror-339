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
import re
from bstack_utils.bstack11lll1l1_opy_ import bstack111lll11ll1_opy_
def bstack111ll1lllll_opy_(fixture_name):
    if fixture_name.startswith(bstack11l1l11_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡵࡨࡸࡺࡶ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᲛ")):
        return bstack11l1l11_opy_ (u"ࠩࡶࡩࡹࡻࡰ࠮ࡨࡸࡲࡨࡺࡩࡰࡰࠪᲜ")
    elif fixture_name.startswith(bstack11l1l11_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡷࡪࡺࡵࡱࡡࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᲝ")):
        return bstack11l1l11_opy_ (u"ࠫࡸ࡫ࡴࡶࡲ࠰ࡱࡴࡪࡵ࡭ࡧࠪᲞ")
    elif fixture_name.startswith(bstack11l1l11_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᲟ")):
        return bstack11l1l11_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮࠮ࡨࡸࡲࡨࡺࡩࡰࡰࠪᲠ")
    elif fixture_name.startswith(bstack11l1l11_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᲡ")):
        return bstack11l1l11_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰ࠰ࡱࡴࡪࡵ࡭ࡧࠪᲢ")
def bstack111lll1111l_opy_(fixture_name):
    return bool(re.match(bstack11l1l11_opy_ (u"ࠩࡡࡣࡽࡻ࡮ࡪࡶࡢࠬࡸ࡫ࡴࡶࡲࡿࡸࡪࡧࡲࡥࡱࡺࡲ࠮ࡥࠨࡧࡷࡱࡧࡹ࡯࡯࡯ࡾࡰࡳࡩࡻ࡬ࡦࠫࡢࡪ࡮ࡾࡴࡶࡴࡨࡣ࠳࠰ࠧᲣ"), fixture_name))
def bstack111lll11lll_opy_(fixture_name):
    return bool(re.match(bstack11l1l11_opy_ (u"ࠪࡢࡤࡾࡵ࡯࡫ࡷࡣ࠭ࡹࡥࡵࡷࡳࢀࡹ࡫ࡡࡳࡦࡲࡻࡳ࠯࡟࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠ࠰࠭ࠫᲤ"), fixture_name))
def bstack111lll1l1ll_opy_(fixture_name):
    return bool(re.match(bstack11l1l11_opy_ (u"ࠫࡣࡥࡸࡶࡰ࡬ࡸࡤ࠮ࡳࡦࡶࡸࡴࢁࡺࡥࡢࡴࡧࡳࡼࡴࠩࡠࡥ࡯ࡥࡸࡹ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠ࠰࠭ࠫᲥ"), fixture_name))
def bstack111lll111l1_opy_(fixture_name):
    if fixture_name.startswith(bstack11l1l11_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡹࡥࡵࡷࡳࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᲦ")):
        return bstack11l1l11_opy_ (u"࠭ࡳࡦࡶࡸࡴ࠲࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧᲧ"), bstack11l1l11_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠬᲨ")
    elif fixture_name.startswith(bstack11l1l11_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡵࡨࡸࡺࡶ࡟࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᲩ")):
        return bstack11l1l11_opy_ (u"ࠩࡶࡩࡹࡻࡰ࠮࡯ࡲࡨࡺࡲࡥࠨᲪ"), bstack11l1l11_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡅࡑࡒࠧᲫ")
    elif fixture_name.startswith(bstack11l1l11_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᲬ")):
        return bstack11l1l11_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࠭ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩᲭ"), bstack11l1l11_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠪᲮ")
    elif fixture_name.startswith(bstack11l1l11_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᲯ")):
        return bstack11l1l11_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰ࠰ࡱࡴࡪࡵ࡭ࡧࠪᲰ"), bstack11l1l11_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡃࡏࡐࠬᲱ")
    return None, None
def bstack111lll1l111_opy_(hook_name):
    if hook_name in [bstack11l1l11_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩᲲ"), bstack11l1l11_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭Ჳ")]:
        return hook_name.capitalize()
    return hook_name
def bstack111lll111ll_opy_(hook_name):
    if hook_name in [bstack11l1l11_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭Ჴ"), bstack11l1l11_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳࡥࡵࡪࡲࡨࠬᲵ")]:
        return bstack11l1l11_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠬᲶ")
    elif hook_name in [bstack11l1l11_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡱࡧࡹࡱ࡫ࠧᲷ"), bstack11l1l11_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠࡥ࡯ࡥࡸࡹࠧᲸ")]:
        return bstack11l1l11_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡅࡑࡒࠧᲹ")
    elif hook_name in [bstack11l1l11_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨᲺ"), bstack11l1l11_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡧࡷ࡬ࡴࡪࠧ᲻")]:
        return bstack11l1l11_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠪ᲼")
    elif hook_name in [bstack11l1l11_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡳࡩࡻ࡬ࡦࠩᲽ"), bstack11l1l11_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡧࡱࡧࡳࡴࠩᲾ")]:
        return bstack11l1l11_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡃࡏࡐࠬᲿ")
    return hook_name
def bstack111lll11l11_opy_(node, scenario):
    if hasattr(node, bstack11l1l11_opy_ (u"ࠪࡧࡦࡲ࡬ࡴࡲࡨࡧࠬ᳀")):
        parts = node.nodeid.rsplit(bstack11l1l11_opy_ (u"ࠦࡠࠨ᳁"))
        params = parts[-1]
        return bstack11l1l11_opy_ (u"ࠧࢁࡽࠡ࡝ࡾࢁࠧ᳂").format(scenario.name, params)
    return scenario.name
def bstack111lll1l1l1_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack11l1l11_opy_ (u"࠭ࡣࡢ࡮࡯ࡷࡵ࡫ࡣࠨ᳃")):
            examples = list(node.callspec.params[bstack11l1l11_opy_ (u"ࠧࡠࡲࡼࡸࡪࡹࡴࡠࡤࡧࡨࡤ࡫ࡸࡢ࡯ࡳࡰࡪ࠭᳄")].values())
        return examples
    except:
        return []
def bstack111lll1l11l_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack111lll11l1l_opy_(report):
    try:
        status = bstack11l1l11_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ᳅")
        if report.passed or (report.failed and hasattr(report, bstack11l1l11_opy_ (u"ࠤࡺࡥࡸࡾࡦࡢ࡫࡯ࠦ᳆"))):
            status = bstack11l1l11_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪ᳇")
        elif report.skipped:
            status = bstack11l1l11_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬ᳈")
        bstack111lll11ll1_opy_(status)
    except:
        pass
def bstack111l1l1l1_opy_(status):
    try:
        bstack111lll11111_opy_ = bstack11l1l11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ᳉")
        if status == bstack11l1l11_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭᳊"):
            bstack111lll11111_opy_ = bstack11l1l11_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧ᳋")
        elif status == bstack11l1l11_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩ᳌"):
            bstack111lll11111_opy_ = bstack11l1l11_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪ᳍")
        bstack111lll11ll1_opy_(bstack111lll11111_opy_)
    except:
        pass
def bstack111lll1ll11_opy_(item=None, report=None, summary=None, extra=None):
    return
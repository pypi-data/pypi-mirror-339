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
import json
import os
import threading
from bstack_utils.config import Config
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack11l1ll111ll_opy_, bstack1ll1l111_opy_, bstack11111l111_opy_, bstack11l11l111_opy_, \
    bstack11ll111111l_opy_
from bstack_utils.measure import measure
def bstack1ll1l111l1_opy_(bstack111l11l1111_opy_):
    for driver in bstack111l11l1111_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack1l1ll11l11_opy_, stage=STAGE.bstack1llll1l1_opy_)
def bstack111l1l1l_opy_(driver, status, reason=bstack1ll1l1_opy_ (u"ࠩࠪᵵ")):
    bstack11ll11ll_opy_ = Config.bstack1l11l1l1ll_opy_()
    if bstack11ll11ll_opy_.bstack111l111lll_opy_():
        return
    bstack1l1l11111_opy_ = bstack11ll1ll111_opy_(bstack1ll1l1_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭ᵶ"), bstack1ll1l1_opy_ (u"ࠫࠬᵷ"), status, reason, bstack1ll1l1_opy_ (u"ࠬ࠭ᵸ"), bstack1ll1l1_opy_ (u"࠭ࠧᵹ"))
    driver.execute_script(bstack1l1l11111_opy_)
@measure(event_name=EVENTS.bstack1l1ll11l11_opy_, stage=STAGE.bstack1llll1l1_opy_)
def bstack11lllll11l_opy_(page, status, reason=bstack1ll1l1_opy_ (u"ࠧࠨᵺ")):
    try:
        if page is None:
            return
        bstack11ll11ll_opy_ = Config.bstack1l11l1l1ll_opy_()
        if bstack11ll11ll_opy_.bstack111l111lll_opy_():
            return
        bstack1l1l11111_opy_ = bstack11ll1ll111_opy_(bstack1ll1l1_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫᵻ"), bstack1ll1l1_opy_ (u"ࠩࠪᵼ"), status, reason, bstack1ll1l1_opy_ (u"ࠪࠫᵽ"), bstack1ll1l1_opy_ (u"ࠫࠬᵾ"))
        page.evaluate(bstack1ll1l1_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨᵿ"), bstack1l1l11111_opy_)
    except Exception as e:
        print(bstack1ll1l1_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡴࡶࡤࡸࡺࡹࠠࡧࡱࡵࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡽࢀࠦᶀ"), e)
def bstack11ll1ll111_opy_(type, name, status, reason, bstack11ll111111_opy_, bstack1l111ll1l_opy_):
    bstack11l11ll1ll_opy_ = {
        bstack1ll1l1_opy_ (u"ࠧࡢࡥࡷ࡭ࡴࡴࠧᶁ"): type,
        bstack1ll1l1_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫᶂ"): {}
    }
    if type == bstack1ll1l1_opy_ (u"ࠩࡤࡲࡳࡵࡴࡢࡶࡨࠫᶃ"):
        bstack11l11ll1ll_opy_[bstack1ll1l1_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ᶄ")][bstack1ll1l1_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪᶅ")] = bstack11ll111111_opy_
        bstack11l11ll1ll_opy_[bstack1ll1l1_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨᶆ")][bstack1ll1l1_opy_ (u"࠭ࡤࡢࡶࡤࠫᶇ")] = json.dumps(str(bstack1l111ll1l_opy_))
    if type == bstack1ll1l1_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨᶈ"):
        bstack11l11ll1ll_opy_[bstack1ll1l1_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫᶉ")][bstack1ll1l1_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᶊ")] = name
    if type == bstack1ll1l1_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭ᶋ"):
        bstack11l11ll1ll_opy_[bstack1ll1l1_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧᶌ")][bstack1ll1l1_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬᶍ")] = status
        if status == bstack1ll1l1_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᶎ") and str(reason) != bstack1ll1l1_opy_ (u"ࠢࠣᶏ"):
            bstack11l11ll1ll_opy_[bstack1ll1l1_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫᶐ")][bstack1ll1l1_opy_ (u"ࠩࡵࡩࡦࡹ࡯࡯ࠩᶑ")] = json.dumps(str(reason))
    bstack11ll1111l1_opy_ = bstack1ll1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡽࠨᶒ").format(json.dumps(bstack11l11ll1ll_opy_))
    return bstack11ll1111l1_opy_
def bstack111ll111l_opy_(url, config, logger, bstack111111l1l_opy_=False):
    hostname = bstack1ll1l111_opy_(url)
    is_private = bstack11l11l111_opy_(hostname)
    try:
        if is_private or bstack111111l1l_opy_:
            file_path = bstack11l1ll111ll_opy_(bstack1ll1l1_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫᶓ"), bstack1ll1l1_opy_ (u"ࠬ࠴ࡢࡴࡶࡤࡧࡰ࠳ࡣࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠫᶔ"), logger)
            if os.environ.get(bstack1ll1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡄࡃࡏࡣࡓࡕࡔࡠࡕࡈࡘࡤࡋࡒࡓࡑࡕࠫᶕ")) and eval(
                    os.environ.get(bstack1ll1l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࡤࡔࡏࡕࡡࡖࡉ࡙ࡥࡅࡓࡔࡒࡖࠬᶖ"))):
                return
            if (bstack1ll1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬᶗ") in config and not config[bstack1ll1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ᶘ")]):
                os.environ[bstack1ll1l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡏࡓࡈࡇࡌࡠࡐࡒࡘࡤ࡙ࡅࡕࡡࡈࡖࡗࡕࡒࠨᶙ")] = str(True)
                bstack111l111llll_opy_ = {bstack1ll1l1_opy_ (u"ࠫ࡭ࡵࡳࡵࡰࡤࡱࡪ࠭ᶚ"): hostname}
                bstack11ll111111l_opy_(bstack1ll1l1_opy_ (u"ࠬ࠴ࡢࡴࡶࡤࡧࡰ࠳ࡣࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠫᶛ"), bstack1ll1l1_opy_ (u"࠭࡮ࡶࡦࡪࡩࡤࡲ࡯ࡤࡣ࡯ࠫᶜ"), bstack111l111llll_opy_, logger)
    except Exception as e:
        pass
def bstack1l111ll1_opy_(caps, bstack111l11l111l_opy_):
    if bstack1ll1l1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᶝ") in caps:
        caps[bstack1ll1l1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᶞ")][bstack1ll1l1_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࠨᶟ")] = True
        if bstack111l11l111l_opy_:
            caps[bstack1ll1l1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᶠ")][bstack1ll1l1_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ᶡ")] = bstack111l11l111l_opy_
    else:
        caps[bstack1ll1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡱࡵࡣࡢ࡮ࠪᶢ")] = True
        if bstack111l11l111l_opy_:
            caps[bstack1ll1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧᶣ")] = bstack111l11l111l_opy_
def bstack111l1l11lll_opy_(bstack111lll11l1_opy_):
    bstack111l111lll1_opy_ = bstack11111l111_opy_(threading.current_thread(), bstack1ll1l1_opy_ (u"ࠧࡵࡧࡶࡸࡘࡺࡡࡵࡷࡶࠫᶤ"), bstack1ll1l1_opy_ (u"ࠨࠩᶥ"))
    if bstack111l111lll1_opy_ == bstack1ll1l1_opy_ (u"ࠩࠪᶦ") or bstack111l111lll1_opy_ == bstack1ll1l1_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫᶧ"):
        threading.current_thread().testStatus = bstack111lll11l1_opy_
    else:
        if bstack111lll11l1_opy_ == bstack1ll1l1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᶨ"):
            threading.current_thread().testStatus = bstack111lll11l1_opy_
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
import json
import os
import threading
from bstack_utils.config import Config
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack11lll1l11l1_opy_, bstack11l1ll1l1l_opy_, bstack1llllllll1_opy_, bstack111111l1_opy_, \
    bstack11ll1l11111_opy_
from bstack_utils.measure import measure
def bstack1l111ll1l_opy_(bstack111ll11l1l1_opy_):
    for driver in bstack111ll11l1l1_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack1ll1l1l1l_opy_, stage=STAGE.bstack1l1ll1lll_opy_)
def bstack1l1l1l11l1_opy_(driver, status, reason=bstack11l1l11_opy_ (u"᳦࠭ࠧ")):
    bstack111ll1lll_opy_ = Config.bstack111l1l1l_opy_()
    if bstack111ll1lll_opy_.bstack111l1111ll_opy_():
        return
    bstack1l11lll111_opy_ = bstack11ll11111_opy_(bstack11l1l11_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵ᳧ࠪ"), bstack11l1l11_opy_ (u"ࠨ᳨ࠩ"), status, reason, bstack11l1l11_opy_ (u"ࠩࠪᳩ"), bstack11l1l11_opy_ (u"ࠪࠫᳪ"))
    driver.execute_script(bstack1l11lll111_opy_)
@measure(event_name=EVENTS.bstack1ll1l1l1l_opy_, stage=STAGE.bstack1l1ll1lll_opy_)
def bstack1llll1lll1_opy_(page, status, reason=bstack11l1l11_opy_ (u"ࠫࠬᳫ")):
    try:
        if page is None:
            return
        bstack111ll1lll_opy_ = Config.bstack111l1l1l_opy_()
        if bstack111ll1lll_opy_.bstack111l1111ll_opy_():
            return
        bstack1l11lll111_opy_ = bstack11ll11111_opy_(bstack11l1l11_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠨᳬ"), bstack11l1l11_opy_ (u"᳭࠭ࠧ"), status, reason, bstack11l1l11_opy_ (u"ࠧࠨᳮ"), bstack11l1l11_opy_ (u"ࠨࠩᳯ"))
        page.evaluate(bstack11l1l11_opy_ (u"ࠤࡢࠤࡂࡄࠠࡼࡿࠥᳰ"), bstack1l11lll111_opy_)
    except Exception as e:
        print(bstack11l1l11_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡷࡪࡹࡳࡪࡱࡱࠤࡸࡺࡡࡵࡷࡶࠤ࡫ࡵࡲࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࢁࡽࠣᳱ"), e)
def bstack11ll11111_opy_(type, name, status, reason, bstack1ll111l1l1_opy_, bstack1l111lllll_opy_):
    bstack1l1ll11ll1_opy_ = {
        bstack11l1l11_opy_ (u"ࠫࡦࡩࡴࡪࡱࡱࠫᳲ"): type,
        bstack11l1l11_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨᳳ"): {}
    }
    if type == bstack11l1l11_opy_ (u"࠭ࡡ࡯ࡰࡲࡸࡦࡺࡥࠨ᳴"):
        bstack1l1ll11ll1_opy_[bstack11l1l11_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪᳵ")][bstack11l1l11_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧᳶ")] = bstack1ll111l1l1_opy_
        bstack1l1ll11ll1_opy_[bstack11l1l11_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬ᳷")][bstack11l1l11_opy_ (u"ࠪࡨࡦࡺࡡࠨ᳸")] = json.dumps(str(bstack1l111lllll_opy_))
    if type == bstack11l1l11_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ᳹"):
        bstack1l1ll11ll1_opy_[bstack11l1l11_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨᳺ")][bstack11l1l11_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ᳻")] = name
    if type == bstack11l1l11_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠪ᳼"):
        bstack1l1ll11ll1_opy_[bstack11l1l11_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫ᳽")][bstack11l1l11_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ᳾")] = status
        if status == bstack11l1l11_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ᳿") and str(reason) != bstack11l1l11_opy_ (u"ࠦࠧᴀ"):
            bstack1l1ll11ll1_opy_[bstack11l1l11_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨᴁ")][bstack11l1l11_opy_ (u"࠭ࡲࡦࡣࡶࡳࡳ࠭ᴂ")] = json.dumps(str(reason))
    bstack11ll111ll_opy_ = bstack11l1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠬᴃ").format(json.dumps(bstack1l1ll11ll1_opy_))
    return bstack11ll111ll_opy_
def bstack1l1ll1ll_opy_(url, config, logger, bstack1ll11l1l_opy_=False):
    hostname = bstack11l1ll1l1l_opy_(url)
    is_private = bstack111111l1_opy_(hostname)
    try:
        if is_private or bstack1ll11l1l_opy_:
            file_path = bstack11lll1l11l1_opy_(bstack11l1l11_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨᴄ"), bstack11l1l11_opy_ (u"ࠩ࠱ࡦࡸࡺࡡࡤ࡭࠰ࡧࡴࡴࡦࡪࡩ࠱࡮ࡸࡵ࡮ࠨᴅ"), logger)
            if os.environ.get(bstack11l1l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡏࡓࡈࡇࡌࡠࡐࡒࡘࡤ࡙ࡅࡕࡡࡈࡖࡗࡕࡒࠨᴆ")) and eval(
                    os.environ.get(bstack11l1l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࡡࡑࡓ࡙ࡥࡓࡆࡖࡢࡉࡗࡘࡏࡓࠩᴇ"))):
                return
            if (bstack11l1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩᴈ") in config and not config[bstack11l1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪᴉ")]):
                os.environ[bstack11l1l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࡤࡔࡏࡕࡡࡖࡉ࡙ࡥࡅࡓࡔࡒࡖࠬᴊ")] = str(True)
                bstack111ll11l11l_opy_ = {bstack11l1l11_opy_ (u"ࠨࡪࡲࡷࡹࡴࡡ࡮ࡧࠪᴋ"): hostname}
                bstack11ll1l11111_opy_(bstack11l1l11_opy_ (u"ࠩ࠱ࡦࡸࡺࡡࡤ࡭࠰ࡧࡴࡴࡦࡪࡩ࠱࡮ࡸࡵ࡮ࠨᴌ"), bstack11l1l11_opy_ (u"ࠪࡲࡺࡪࡧࡦࡡ࡯ࡳࡨࡧ࡬ࠨᴍ"), bstack111ll11l11l_opy_, logger)
    except Exception as e:
        pass
def bstack1ll11l1l1l_opy_(caps, bstack111ll11l111_opy_):
    if bstack11l1l11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᴎ") in caps:
        caps[bstack11l1l11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᴏ")][bstack11l1l11_opy_ (u"࠭࡬ࡰࡥࡤࡰࠬᴐ")] = True
        if bstack111ll11l111_opy_:
            caps[bstack11l1l11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᴑ")][bstack11l1l11_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪᴒ")] = bstack111ll11l111_opy_
    else:
        caps[bstack11l1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡮ࡲࡧࡦࡲࠧᴓ")] = True
        if bstack111ll11l111_opy_:
            caps[bstack11l1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫᴔ")] = bstack111ll11l111_opy_
def bstack111lll11ll1_opy_(bstack111l11ll11_opy_):
    bstack111ll111lll_opy_ = bstack1llllllll1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡕࡷࡥࡹࡻࡳࠨᴕ"), bstack11l1l11_opy_ (u"ࠬ࠭ᴖ"))
    if bstack111ll111lll_opy_ == bstack11l1l11_opy_ (u"࠭ࠧᴗ") or bstack111ll111lll_opy_ == bstack11l1l11_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨᴘ"):
        threading.current_thread().testStatus = bstack111l11ll11_opy_
    else:
        if bstack111l11ll11_opy_ == bstack11l1l11_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᴙ"):
            threading.current_thread().testStatus = bstack111l11ll11_opy_
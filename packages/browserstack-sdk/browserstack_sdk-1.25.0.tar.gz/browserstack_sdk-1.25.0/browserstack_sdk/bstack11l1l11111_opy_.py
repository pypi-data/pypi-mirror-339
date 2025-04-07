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
import json
import logging
logger = logging.getLogger(__name__)
class BrowserStackSdk:
    def get_current_platform():
        bstack1llll1l11_opy_ = {}
        bstack11l11l1lll_opy_ = os.environ.get(bstack11l1l11_opy_ (u"࠭ࡃࡖࡔࡕࡉࡓ࡚࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡇࡅ࡙ࡇࠧຠ"), bstack11l1l11_opy_ (u"ࠧࠨມ"))
        if not bstack11l11l1lll_opy_:
            return bstack1llll1l11_opy_
        try:
            bstack11l11l1ll1_opy_ = json.loads(bstack11l11l1lll_opy_)
            if bstack11l1l11_opy_ (u"ࠣࡱࡶࠦຢ") in bstack11l11l1ll1_opy_:
                bstack1llll1l11_opy_[bstack11l1l11_opy_ (u"ࠤࡲࡷࠧຣ")] = bstack11l11l1ll1_opy_[bstack11l1l11_opy_ (u"ࠥࡳࡸࠨ຤")]
            if bstack11l1l11_opy_ (u"ࠦࡴࡹ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠣລ") in bstack11l11l1ll1_opy_ or bstack11l1l11_opy_ (u"ࠧࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠣ຦") in bstack11l11l1ll1_opy_:
                bstack1llll1l11_opy_[bstack11l1l11_opy_ (u"ࠨ࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠤວ")] = bstack11l11l1ll1_opy_.get(bstack11l1l11_opy_ (u"ࠢࡰࡵࡢࡺࡪࡸࡳࡪࡱࡱࠦຨ"), bstack11l11l1ll1_opy_.get(bstack11l1l11_opy_ (u"ࠣࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠦຩ")))
            if bstack11l1l11_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࠥສ") in bstack11l11l1ll1_opy_ or bstack11l1l11_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠣຫ") in bstack11l11l1ll1_opy_:
                bstack1llll1l11_opy_[bstack11l1l11_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠤຬ")] = bstack11l11l1ll1_opy_.get(bstack11l1l11_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࠨອ"), bstack11l11l1ll1_opy_.get(bstack11l1l11_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠦຮ")))
            if bstack11l1l11_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠤຯ") in bstack11l11l1ll1_opy_ or bstack11l1l11_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠤະ") in bstack11l11l1ll1_opy_:
                bstack1llll1l11_opy_[bstack11l1l11_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠥັ")] = bstack11l11l1ll1_opy_.get(bstack11l1l11_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠧາ"), bstack11l11l1ll1_opy_.get(bstack11l1l11_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠧຳ")))
            if bstack11l1l11_opy_ (u"ࠧࡪࡥࡷ࡫ࡦࡩࠧິ") in bstack11l11l1ll1_opy_ or bstack11l1l11_opy_ (u"ࠨࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠥີ") in bstack11l11l1ll1_opy_:
                bstack1llll1l11_opy_[bstack11l1l11_opy_ (u"ࠢࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠦຶ")] = bstack11l11l1ll1_opy_.get(bstack11l1l11_opy_ (u"ࠣࡦࡨࡺ࡮ࡩࡥࠣື"), bstack11l11l1ll1_opy_.get(bstack11l1l11_opy_ (u"ࠤࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪࠨຸ")))
            if bstack11l1l11_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱູࠧ") in bstack11l11l1ll1_opy_ or bstack11l1l11_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧ຺ࠥ") in bstack11l11l1ll1_opy_:
                bstack1llll1l11_opy_[bstack11l1l11_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡎࡢ࡯ࡨࠦົ")] = bstack11l11l1ll1_opy_.get(bstack11l1l11_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠣຼ"), bstack11l11l1ll1_opy_.get(bstack11l1l11_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪࠨຽ")))
            if bstack11l1l11_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢࡺࡪࡸࡳࡪࡱࡱࠦ຾") in bstack11l11l1ll1_opy_ or bstack11l1l11_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠦ຿") in bstack11l11l1ll1_opy_:
                bstack1llll1l11_opy_[bstack11l1l11_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠧເ")] = bstack11l11l1ll1_opy_.get(bstack11l1l11_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࡥࡶࡦࡴࡶ࡭ࡴࡴࠢແ"), bstack11l11l1ll1_opy_.get(bstack11l1l11_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠢໂ")))
            if bstack11l1l11_opy_ (u"ࠨࡣࡶࡵࡷࡳࡲ࡜ࡡࡳ࡫ࡤࡦࡱ࡫ࡳࠣໃ") in bstack11l11l1ll1_opy_:
                bstack1llll1l11_opy_[bstack11l1l11_opy_ (u"ࠢࡤࡷࡶࡸࡴࡳࡖࡢࡴ࡬ࡥࡧࡲࡥࡴࠤໄ")] = bstack11l11l1ll1_opy_[bstack11l1l11_opy_ (u"ࠣࡥࡸࡷࡹࡵ࡭ࡗࡣࡵ࡭ࡦࡨ࡬ࡦࡵࠥ໅")]
        except Exception as error:
            logger.error(bstack11l1l11_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤ࡬࡫ࡴࡵ࡫ࡱ࡫ࠥࡩࡵࡳࡴࡨࡲࡹࠦࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠡࡦࡤࡸࡦࡀࠠࠣໆ") +  str(error))
        return bstack1llll1l11_opy_
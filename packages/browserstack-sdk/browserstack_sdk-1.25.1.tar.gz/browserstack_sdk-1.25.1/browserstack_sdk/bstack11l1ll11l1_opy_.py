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
import json
import logging
logger = logging.getLogger(__name__)
class BrowserStackSdk:
    def get_current_platform():
        bstack11ll11l111_opy_ = {}
        bstack11l11l11ll_opy_ = os.environ.get(bstack1ll1l1_opy_ (u"ࠨࡅࡘࡖࡗࡋࡎࡕࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡉࡇࡔࡂࠩຢ"), bstack1ll1l1_opy_ (u"ࠩࠪຣ"))
        if not bstack11l11l11ll_opy_:
            return bstack11ll11l111_opy_
        try:
            bstack11l11l1l11_opy_ = json.loads(bstack11l11l11ll_opy_)
            if bstack1ll1l1_opy_ (u"ࠥࡳࡸࠨ຤") in bstack11l11l1l11_opy_:
                bstack11ll11l111_opy_[bstack1ll1l1_opy_ (u"ࠦࡴࡹࠢລ")] = bstack11l11l1l11_opy_[bstack1ll1l1_opy_ (u"ࠧࡵࡳࠣ຦")]
            if bstack1ll1l1_opy_ (u"ࠨ࡯ࡴࡡࡹࡩࡷࡹࡩࡰࡰࠥວ") in bstack11l11l1l11_opy_ or bstack1ll1l1_opy_ (u"ࠢࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠥຨ") in bstack11l11l1l11_opy_:
                bstack11ll11l111_opy_[bstack1ll1l1_opy_ (u"ࠣࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠦຩ")] = bstack11l11l1l11_opy_.get(bstack1ll1l1_opy_ (u"ࠤࡲࡷࡤࡼࡥࡳࡵ࡬ࡳࡳࠨສ"), bstack11l11l1l11_opy_.get(bstack1ll1l1_opy_ (u"ࠥࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳࠨຫ")))
            if bstack1ll1l1_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࠧຬ") in bstack11l11l1l11_opy_ or bstack1ll1l1_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠥອ") in bstack11l11l1l11_opy_:
                bstack11ll11l111_opy_[bstack1ll1l1_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠦຮ")] = bstack11l11l1l11_opy_.get(bstack1ll1l1_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࠣຯ"), bstack11l11l1l11_opy_.get(bstack1ll1l1_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪࠨະ")))
            if bstack1ll1l1_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠦັ") in bstack11l11l1l11_opy_ or bstack1ll1l1_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠦາ") in bstack11l11l1l11_opy_:
                bstack11ll11l111_opy_[bstack1ll1l1_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠧຳ")] = bstack11l11l1l11_opy_.get(bstack1ll1l1_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠢິ"), bstack11l11l1l11_opy_.get(bstack1ll1l1_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠢີ")))
            if bstack1ll1l1_opy_ (u"ࠢࡥࡧࡹ࡭ࡨ࡫ࠢຶ") in bstack11l11l1l11_opy_ or bstack1ll1l1_opy_ (u"ࠣࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠧື") in bstack11l11l1l11_opy_:
                bstack11ll11l111_opy_[bstack1ll1l1_opy_ (u"ࠤࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪࠨຸ")] = bstack11l11l1l11_opy_.get(bstack1ll1l1_opy_ (u"ࠥࡨࡪࡼࡩࡤࡧູࠥ"), bstack11l11l1l11_opy_.get(bstack1ll1l1_opy_ (u"ࠦࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥ຺ࠣ")))
            if bstack1ll1l1_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࠢົ") in bstack11l11l1l11_opy_ or bstack1ll1l1_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩࠧຼ") in bstack11l11l1l11_opy_:
                bstack11ll11l111_opy_[bstack1ll1l1_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪࠨຽ")] = bstack11l11l1l11_opy_.get(bstack1ll1l1_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠥ຾"), bstack11l11l1l11_opy_.get(bstack1ll1l1_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠣ຿")))
            if bstack1ll1l1_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡤࡼࡥࡳࡵ࡬ࡳࡳࠨເ") in bstack11l11l1l11_opy_ or bstack1ll1l1_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳࠨແ") in bstack11l11l1l11_opy_:
                bstack11ll11l111_opy_[bstack1ll1l1_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠢໂ")] = bstack11l11l1l11_opy_.get(bstack1ll1l1_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠࡸࡨࡶࡸ࡯࡯࡯ࠤໃ"), bstack11l11l1l11_opy_.get(bstack1ll1l1_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠤໄ")))
            if bstack1ll1l1_opy_ (u"ࠣࡥࡸࡷࡹࡵ࡭ࡗࡣࡵ࡭ࡦࡨ࡬ࡦࡵࠥ໅") in bstack11l11l1l11_opy_:
                bstack11ll11l111_opy_[bstack1ll1l1_opy_ (u"ࠤࡦࡹࡸࡺ࡯࡮ࡘࡤࡶ࡮ࡧࡢ࡭ࡧࡶࠦໆ")] = bstack11l11l1l11_opy_[bstack1ll1l1_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯࡙ࡥࡷ࡯ࡡࡣ࡮ࡨࡷࠧ໇")]
        except Exception as error:
            logger.error(bstack1ll1l1_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡤࡷࡵࡶࡪࡴࡴࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠣࡨࡦࡺࡡ࠻່ࠢࠥ") +  str(error))
        return bstack11ll11l111_opy_
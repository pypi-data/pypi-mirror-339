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
import requests
from urllib.parse import urljoin, urlencode
from datetime import datetime
import os
import logging
import json
logger = logging.getLogger(__name__)
class bstack11lll1l11ll_opy_:
    @staticmethod
    def results(builder,params=None):
        bstack111l11ll111_opy_ = urljoin(builder, bstack1ll1l1_opy_ (u"ࠫ࡮ࡹࡳࡶࡧࡶࠫᵢ"))
        if params:
            bstack111l11ll111_opy_ += bstack1ll1l1_opy_ (u"ࠧࡅࡻࡾࠤᵣ").format(urlencode({bstack1ll1l1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᵤ"): params.get(bstack1ll1l1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᵥ"))}))
        return bstack11lll1l11ll_opy_.bstack111l11ll1l1_opy_(bstack111l11ll111_opy_)
    @staticmethod
    def bstack11lll1l11l1_opy_(builder,params=None):
        bstack111l11ll111_opy_ = urljoin(builder, bstack1ll1l1_opy_ (u"ࠨ࡫ࡶࡷࡺ࡫ࡳ࠮ࡵࡸࡱࡲࡧࡲࡺࠩᵦ"))
        if params:
            bstack111l11ll111_opy_ += bstack1ll1l1_opy_ (u"ࠤࡂࡿࢂࠨᵧ").format(urlencode({bstack1ll1l1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᵨ"): params.get(bstack1ll1l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᵩ"))}))
        return bstack11lll1l11ll_opy_.bstack111l11ll1l1_opy_(bstack111l11ll111_opy_)
    @staticmethod
    def bstack111l11ll1l1_opy_(bstack111l11ll11l_opy_):
        bstack111l11l1ll1_opy_ = os.environ.get(bstack1ll1l1_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪᵪ"), os.environ.get(bstack1ll1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪᵫ"), bstack1ll1l1_opy_ (u"ࠧࠨᵬ")))
        headers = {bstack1ll1l1_opy_ (u"ࠨࡃࡸࡸ࡭ࡵࡲࡪࡼࡤࡸ࡮ࡵ࡮ࠨᵭ"): bstack1ll1l1_opy_ (u"ࠩࡅࡩࡦࡸࡥࡳࠢࡾࢁࠬᵮ").format(bstack111l11l1ll1_opy_)}
        response = requests.get(bstack111l11ll11l_opy_, headers=headers)
        bstack111l11l1lll_opy_ = {}
        try:
            bstack111l11l1lll_opy_ = response.json()
        except Exception as e:
            logger.debug(bstack1ll1l1_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡰࡢࡴࡶࡩࠥࡐࡓࡐࡐࠣࡶࡪࡹࡰࡰࡰࡶࡩ࠿ࠦࡻࡾࠤᵯ").format(e))
            pass
        if bstack111l11l1lll_opy_ is not None:
            bstack111l11l1lll_opy_[bstack1ll1l1_opy_ (u"ࠫࡳ࡫ࡸࡵࡡࡳࡳࡱࡲ࡟ࡵ࡫ࡰࡩࠬᵰ")] = response.headers.get(bstack1ll1l1_opy_ (u"ࠬࡴࡥࡹࡶࡢࡴࡴࡲ࡬ࡠࡶ࡬ࡱࡪ࠭ᵱ"), str(int(datetime.now().timestamp() * 1000)))
            bstack111l11l1lll_opy_[bstack1ll1l1_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ᵲ")] = response.status_code
        return bstack111l11l1lll_opy_
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
import requests
from urllib.parse import urljoin, urlencode
from datetime import datetime
import os
import logging
import json
logger = logging.getLogger(__name__)
class bstack1l11111ll1l_opy_:
    @staticmethod
    def results(builder,params=None):
        bstack111ll1l11l1_opy_ = urljoin(builder, bstack11l1l11_opy_ (u"ࠨ࡫ࡶࡷࡺ࡫ࡳࠨ᳓"))
        if params:
            bstack111ll1l11l1_opy_ += bstack11l1l11_opy_ (u"ࠤࡂࡿࢂࠨ᳔").format(urlencode({bstack11l1l11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦ᳕ࠪ"): params.get(bstack11l1l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧ᳖ࠫ"))}))
        return bstack1l11111ll1l_opy_.bstack111ll11llll_opy_(bstack111ll1l11l1_opy_)
    @staticmethod
    def bstack1l11111l1ll_opy_(builder,params=None):
        bstack111ll1l11l1_opy_ = urljoin(builder, bstack11l1l11_opy_ (u"ࠬ࡯ࡳࡴࡷࡨࡷ࠲ࡹࡵ࡮࡯ࡤࡶࡾ᳗࠭"))
        if params:
            bstack111ll1l11l1_opy_ += bstack11l1l11_opy_ (u"ࠨ࠿ࡼࡿ᳘ࠥ").format(urlencode({bstack11l1l11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪ᳙ࠧ"): params.get(bstack11l1l11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ᳚"))}))
        return bstack1l11111ll1l_opy_.bstack111ll11llll_opy_(bstack111ll1l11l1_opy_)
    @staticmethod
    def bstack111ll11llll_opy_(bstack111ll1l111l_opy_):
        bstack111ll1l11ll_opy_ = os.environ.get(bstack11l1l11_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧ᳛"), os.environ.get(bstack11l1l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚᳜ࠧ"), bstack11l1l11_opy_ (u"᳝ࠫࠬ")))
        headers = {bstack11l1l11_opy_ (u"ࠬࡇࡵࡵࡪࡲࡶ࡮ࢀࡡࡵ࡫ࡲࡲ᳞ࠬ"): bstack11l1l11_opy_ (u"࠭ࡂࡦࡣࡵࡩࡷࠦࡻࡾ᳟ࠩ").format(bstack111ll1l11ll_opy_)}
        response = requests.get(bstack111ll1l111l_opy_, headers=headers)
        bstack111ll1l1111_opy_ = {}
        try:
            bstack111ll1l1111_opy_ = response.json()
        except Exception as e:
            logger.debug(bstack11l1l11_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡴࡦࡸࡳࡦࠢࡍࡗࡔࡔࠠࡳࡧࡶࡴࡴࡴࡳࡦ࠼ࠣࡿࢂࠨ᳠").format(e))
            pass
        if bstack111ll1l1111_opy_ is not None:
            bstack111ll1l1111_opy_[bstack11l1l11_opy_ (u"ࠨࡰࡨࡼࡹࡥࡰࡰ࡮࡯ࡣࡹ࡯࡭ࡦࠩ᳡")] = response.headers.get(bstack11l1l11_opy_ (u"ࠩࡱࡩࡽࡺ࡟ࡱࡱ࡯ࡰࡤࡺࡩ࡮ࡧ᳢ࠪ"), str(int(datetime.now().timestamp() * 1000)))
            bstack111ll1l1111_opy_[bstack11l1l11_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵ᳣ࠪ")] = response.status_code
        return bstack111ll1l1111_opy_
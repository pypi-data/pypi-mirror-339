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
import logging
import os
import datetime
import threading
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack11lllll11l1_opy_, bstack11lllll1l1l_opy_, bstack11l1lll1ll_opy_, bstack111ll11ll1_opy_, bstack11l1l11l11l_opy_, bstack11l1ll1111l_opy_, bstack11ll11lllll_opy_, bstack11l1ll11ll_opy_, bstack11111l111_opy_
from bstack_utils.measure import measure
from bstack_utils.bstack111l11lllll_opy_ import bstack111l1l1111l_opy_
import bstack_utils.bstack1ll11llll_opy_ as bstack1llll11l_opy_
from bstack_utils.bstack111llll1l1_opy_ import bstack11l1ll1ll_opy_
import bstack_utils.accessibility as bstack1l11llll_opy_
from bstack_utils.bstack1ll1l11l1l_opy_ import bstack1ll1l11l1l_opy_
from bstack_utils.bstack11l111l1ll_opy_ import bstack111lll1ll1_opy_
bstack1111lll1ll1_opy_ = bstack1ll1l1_opy_ (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡣࡰ࡮࡯ࡩࡨࡺ࡯ࡳ࠯ࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠬᷨ")
logger = logging.getLogger(__name__)
class bstack1l1lll1lll_opy_:
    bstack111l11lllll_opy_ = None
    bs_config = None
    bstack11lll11111_opy_ = None
    @classmethod
    @bstack111ll11ll1_opy_(class_method=True)
    @measure(event_name=EVENTS.bstack11ll1l111ll_opy_, stage=STAGE.bstack1llll1l1_opy_)
    def launch(cls, bs_config, bstack11lll11111_opy_):
        cls.bs_config = bs_config
        cls.bstack11lll11111_opy_ = bstack11lll11111_opy_
        try:
            cls.bstack1111lll1l1l_opy_()
            bstack11llll11lll_opy_ = bstack11lllll11l1_opy_(bs_config)
            bstack11llll1l1l1_opy_ = bstack11lllll1l1l_opy_(bs_config)
            data = bstack1llll11l_opy_.bstack1111lll1111_opy_(bs_config, bstack11lll11111_opy_)
            config = {
                bstack1ll1l1_opy_ (u"࠭ࡡࡶࡶ࡫ࠫᷩ"): (bstack11llll11lll_opy_, bstack11llll1l1l1_opy_),
                bstack1ll1l1_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡳࠨᷪ"): cls.default_headers()
            }
            response = bstack11l1lll1ll_opy_(bstack1ll1l1_opy_ (u"ࠨࡒࡒࡗ࡙࠭ᷫ"), cls.request_url(bstack1ll1l1_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠳࠱ࡥࡹ࡮ࡲࡤࡴࠩᷬ")), data, config)
            if response.status_code != 200:
                bstack1lllll111ll_opy_ = response.json()
                if bstack1lllll111ll_opy_[bstack1ll1l1_opy_ (u"ࠪࡷࡺࡩࡣࡦࡵࡶࠫᷭ")] == False:
                    cls.bstack1111ll11lll_opy_(bstack1lllll111ll_opy_)
                    return
                cls.bstack1111llll11l_opy_(bstack1lllll111ll_opy_[bstack1ll1l1_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫᷮ")])
                cls.bstack1111ll1ll11_opy_(bstack1lllll111ll_opy_[bstack1ll1l1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᷯ")])
                return None
            bstack1111lll11l1_opy_ = cls.bstack1111lll111l_opy_(response)
            return bstack1111lll11l1_opy_
        except Exception as error:
            logger.error(bstack1ll1l1_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡥࡵࡩࡦࡺࡩ࡯ࡩࠣࡦࡺ࡯࡬ࡥࠢࡩࡳࡷࠦࡔࡦࡵࡷࡌࡺࡨ࠺ࠡࡽࢀࠦᷰ").format(str(error)))
            return None
    @classmethod
    @bstack111ll11ll1_opy_(class_method=True)
    def stop(cls, bstack1111lll11ll_opy_=None):
        if not bstack11l1ll1ll_opy_.on() and not bstack1l11llll_opy_.on():
            return
        if os.environ.get(bstack1ll1l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫᷱ")) == bstack1ll1l1_opy_ (u"ࠣࡰࡸࡰࡱࠨᷲ") or os.environ.get(bstack1ll1l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧᷳ")) == bstack1ll1l1_opy_ (u"ࠥࡲࡺࡲ࡬ࠣᷴ"):
            logger.error(bstack1ll1l1_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡷࡹࡵࡰࠡࡤࡸ࡭ࡱࡪࠠࡳࡧࡴࡹࡪࡹࡴࠡࡶࡲࠤ࡙࡫ࡳࡵࡊࡸࡦ࠿ࠦࡍࡪࡵࡶ࡭ࡳ࡭ࠠࡢࡷࡷ࡬ࡪࡴࡴࡪࡥࡤࡸ࡮ࡵ࡮ࠡࡶࡲ࡯ࡪࡴࠧ᷵"))
            return {
                bstack1ll1l1_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬ᷶"): bstack1ll1l1_opy_ (u"࠭ࡥࡳࡴࡲࡶ᷷ࠬ"),
                bstack1ll1l1_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ᷸"): bstack1ll1l1_opy_ (u"ࠨࡖࡲ࡯ࡪࡴ࠯ࡣࡷ࡬ࡰࡩࡏࡄࠡ࡫ࡶࠤࡺࡴࡤࡦࡨ࡬ࡲࡪࡪࠬࠡࡤࡸ࡭ࡱࡪࠠࡤࡴࡨࡥࡹ࡯࡯࡯ࠢࡰ࡭࡬࡮ࡴࠡࡪࡤࡺࡪࠦࡦࡢ࡫࡯ࡩࡩ᷹࠭")
            }
        try:
            cls.bstack111l11lllll_opy_.shutdown()
            data = {
                bstack1ll1l1_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺ᷺ࠧ"): bstack11l1ll11ll_opy_()
            }
            if not bstack1111lll11ll_opy_ is None:
                data[bstack1ll1l1_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡳࡥࡵࡣࡧࡥࡹࡧࠧ᷻")] = [{
                    bstack1ll1l1_opy_ (u"ࠫࡷ࡫ࡡࡴࡱࡱࠫ᷼"): bstack1ll1l1_opy_ (u"ࠬࡻࡳࡦࡴࡢ࡯࡮ࡲ࡬ࡦࡦ᷽ࠪ"),
                    bstack1ll1l1_opy_ (u"࠭ࡳࡪࡩࡱࡥࡱ࠭᷾"): bstack1111lll11ll_opy_
                }]
            config = {
                bstack1ll1l1_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡳࠨ᷿"): cls.default_headers()
            }
            bstack11ll111l1ll_opy_ = bstack1ll1l1_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠱࠰ࡤࡸ࡭ࡱࡪࡳ࠰ࡽࢀ࠳ࡸࡺ࡯ࡱࠩḀ").format(os.environ[bstack1ll1l1_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠢḁ")])
            bstack1111ll1l1ll_opy_ = cls.request_url(bstack11ll111l1ll_opy_)
            response = bstack11l1lll1ll_opy_(bstack1ll1l1_opy_ (u"ࠪࡔ࡚࡚ࠧḂ"), bstack1111ll1l1ll_opy_, data, config)
            if not response.ok:
                raise Exception(bstack1ll1l1_opy_ (u"ࠦࡘࡺ࡯ࡱࠢࡵࡩࡶࡻࡥࡴࡶࠣࡲࡴࡺࠠࡰ࡭ࠥḃ"))
        except Exception as error:
            logger.error(bstack1ll1l1_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡸࡺ࡯ࡱࠢࡥࡹ࡮ࡲࡤࠡࡴࡨࡵࡺ࡫ࡳࡵࠢࡷࡳ࡚ࠥࡥࡴࡶࡋࡹࡧࡀ࠺ࠡࠤḄ") + str(error))
            return {
                bstack1ll1l1_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ḅ"): bstack1ll1l1_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭Ḇ"),
                bstack1ll1l1_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩḇ"): str(error)
            }
    @classmethod
    @bstack111ll11ll1_opy_(class_method=True)
    def bstack1111lll111l_opy_(cls, response):
        bstack1lllll111ll_opy_ = response.json() if not isinstance(response, dict) else response
        bstack1111lll11l1_opy_ = {}
        if bstack1lllll111ll_opy_.get(bstack1ll1l1_opy_ (u"ࠩ࡭ࡻࡹ࠭Ḉ")) is None:
            os.environ[bstack1ll1l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧḉ")] = bstack1ll1l1_opy_ (u"ࠫࡳࡻ࡬࡭ࠩḊ")
        else:
            os.environ[bstack1ll1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩḋ")] = bstack1lllll111ll_opy_.get(bstack1ll1l1_opy_ (u"࠭ࡪࡸࡶࠪḌ"), bstack1ll1l1_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬḍ"))
        os.environ[bstack1ll1l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭Ḏ")] = bstack1lllll111ll_opy_.get(bstack1ll1l1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫḏ"), bstack1ll1l1_opy_ (u"ࠪࡲࡺࡲ࡬ࠨḐ"))
        logger.info(bstack1ll1l1_opy_ (u"࡙ࠫ࡫ࡳࡵࡪࡸࡦࠥࡹࡴࡢࡴࡷࡩࡩࠦࡷࡪࡶ࡫ࠤ࡮ࡪ࠺ࠡࠩḑ") + os.getenv(bstack1ll1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪḒ")));
        if bstack11l1ll1ll_opy_.bstack1111ll111ll_opy_(cls.bs_config, cls.bstack11lll11111_opy_.get(bstack1ll1l1_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡸࡷࡪࡪࠧḓ"), bstack1ll1l1_opy_ (u"ࠧࠨḔ"))) is True:
            bstack111l11l1ll1_opy_, build_hashed_id, bstack1111ll11l11_opy_ = cls.bstack1111ll1l11l_opy_(bstack1lllll111ll_opy_)
            if bstack111l11l1ll1_opy_ != None and build_hashed_id != None:
                bstack1111lll11l1_opy_[bstack1ll1l1_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨḕ")] = {
                    bstack1ll1l1_opy_ (u"ࠩ࡭ࡻࡹࡥࡴࡰ࡭ࡨࡲࠬḖ"): bstack111l11l1ll1_opy_,
                    bstack1ll1l1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬḗ"): build_hashed_id,
                    bstack1ll1l1_opy_ (u"ࠫࡦࡲ࡬ࡰࡹࡢࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡳࠨḘ"): bstack1111ll11l11_opy_
                }
            else:
                bstack1111lll11l1_opy_[bstack1ll1l1_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬḙ")] = {}
        else:
            bstack1111lll11l1_opy_[bstack1ll1l1_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭Ḛ")] = {}
        if bstack1l11llll_opy_.bstack1l1l1111l_opy_(cls.bs_config) is True:
            bstack1111ll1l111_opy_, build_hashed_id = cls.bstack1111lll1lll_opy_(bstack1lllll111ll_opy_)
            if bstack1111ll1l111_opy_ != None and build_hashed_id != None:
                bstack1111lll11l1_opy_[bstack1ll1l1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧḛ")] = {
                    bstack1ll1l1_opy_ (u"ࠨࡣࡸࡸ࡭ࡥࡴࡰ࡭ࡨࡲࠬḜ"): bstack1111ll1l111_opy_,
                    bstack1ll1l1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫḝ"): build_hashed_id,
                }
            else:
                bstack1111lll11l1_opy_[bstack1ll1l1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪḞ")] = {}
        else:
            bstack1111lll11l1_opy_[bstack1ll1l1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫḟ")] = {}
        if bstack1111lll11l1_opy_[bstack1ll1l1_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬḠ")].get(bstack1ll1l1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨḡ")) != None or bstack1111lll11l1_opy_[bstack1ll1l1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧḢ")].get(bstack1ll1l1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪḣ")) != None:
            cls.bstack1111ll11l1l_opy_(bstack1lllll111ll_opy_.get(bstack1ll1l1_opy_ (u"ࠩ࡭ࡻࡹ࠭Ḥ")), bstack1lllll111ll_opy_.get(bstack1ll1l1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬḥ")))
        return bstack1111lll11l1_opy_
    @classmethod
    def bstack1111ll1l11l_opy_(cls, bstack1lllll111ll_opy_):
        if bstack1lllll111ll_opy_.get(bstack1ll1l1_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫḦ")) == None:
            cls.bstack1111llll11l_opy_()
            return [None, None, None]
        if bstack1lllll111ll_opy_[bstack1ll1l1_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬḧ")][bstack1ll1l1_opy_ (u"࠭ࡳࡶࡥࡦࡩࡸࡹࠧḨ")] != True:
            cls.bstack1111llll11l_opy_(bstack1lllll111ll_opy_[bstack1ll1l1_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧḩ")])
            return [None, None, None]
        logger.debug(bstack1ll1l1_opy_ (u"ࠨࡖࡨࡷࡹࠦࡏࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾࠦࡂࡶ࡫࡯ࡨࠥࡩࡲࡦࡣࡷ࡭ࡴࡴࠠࡔࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࠥࠬḪ"))
        os.environ[bstack1ll1l1_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡂࡖࡋࡏࡈࡤࡉࡏࡎࡒࡏࡉ࡙ࡋࡄࠨḫ")] = bstack1ll1l1_opy_ (u"ࠪࡸࡷࡻࡥࠨḬ")
        if bstack1lllll111ll_opy_.get(bstack1ll1l1_opy_ (u"ࠫ࡯ࡽࡴࠨḭ")):
            os.environ[bstack1ll1l1_opy_ (u"ࠬࡉࡒࡆࡆࡈࡒ࡙ࡏࡁࡍࡕࡢࡊࡔࡘ࡟ࡄࡔࡄࡗࡍࡥࡒࡆࡒࡒࡖ࡙ࡏࡎࡈࠩḮ")] = json.dumps({
                bstack1ll1l1_opy_ (u"࠭ࡵࡴࡧࡵࡲࡦࡳࡥࠨḯ"): bstack11lllll11l1_opy_(cls.bs_config),
                bstack1ll1l1_opy_ (u"ࠧࡱࡣࡶࡷࡼࡵࡲࡥࠩḰ"): bstack11lllll1l1l_opy_(cls.bs_config)
            })
        if bstack1lllll111ll_opy_.get(bstack1ll1l1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪḱ")):
            os.environ[bstack1ll1l1_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡂࡖࡋࡏࡈࡤࡎࡁࡔࡊࡈࡈࡤࡏࡄࠨḲ")] = bstack1lllll111ll_opy_[bstack1ll1l1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬḳ")]
        if bstack1lllll111ll_opy_[bstack1ll1l1_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫḴ")].get(bstack1ll1l1_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭ḵ"), {}).get(bstack1ll1l1_opy_ (u"࠭ࡡ࡭࡮ࡲࡻࡤࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡵࠪḶ")):
            os.environ[bstack1ll1l1_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡆࡒࡌࡐ࡙ࡢࡗࡈࡘࡅࡆࡐࡖࡌࡔ࡚ࡓࠨḷ")] = str(bstack1lllll111ll_opy_[bstack1ll1l1_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨḸ")][bstack1ll1l1_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵࠪḹ")][bstack1ll1l1_opy_ (u"ࠪࡥࡱࡲ࡯ࡸࡡࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࡹࠧḺ")])
        else:
            os.environ[bstack1ll1l1_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡃࡏࡐࡔ࡝࡟ࡔࡅࡕࡉࡊࡔࡓࡉࡑࡗࡗࠬḻ")] = bstack1ll1l1_opy_ (u"ࠧࡴࡵ࡭࡮ࠥḼ")
        return [bstack1lllll111ll_opy_[bstack1ll1l1_opy_ (u"࠭ࡪࡸࡶࠪḽ")], bstack1lllll111ll_opy_[bstack1ll1l1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩḾ")], os.environ[bstack1ll1l1_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡇࡌࡍࡑ࡚ࡣࡘࡉࡒࡆࡇࡑࡗࡍࡕࡔࡔࠩḿ")]]
    @classmethod
    def bstack1111lll1lll_opy_(cls, bstack1lllll111ll_opy_):
        if bstack1lllll111ll_opy_.get(bstack1ll1l1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩṀ")) == None:
            cls.bstack1111ll1ll11_opy_()
            return [None, None]
        if bstack1lllll111ll_opy_[bstack1ll1l1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪṁ")][bstack1ll1l1_opy_ (u"ࠫࡸࡻࡣࡤࡧࡶࡷࠬṂ")] != True:
            cls.bstack1111ll1ll11_opy_(bstack1lllll111ll_opy_[bstack1ll1l1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬṃ")])
            return [None, None]
        if bstack1lllll111ll_opy_[bstack1ll1l1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭Ṅ")].get(bstack1ll1l1_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࠨṅ")):
            logger.debug(bstack1ll1l1_opy_ (u"ࠨࡖࡨࡷࡹࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡂࡶ࡫࡯ࡨࠥࡩࡲࡦࡣࡷ࡭ࡴࡴࠠࡔࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࠥࠬṆ"))
            parsed = json.loads(os.getenv(bstack1ll1l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪṇ"), bstack1ll1l1_opy_ (u"ࠪࡿࢂ࠭Ṉ")))
            capabilities = bstack1llll11l_opy_.bstack1111ll1111l_opy_(bstack1lllll111ll_opy_[bstack1ll1l1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫṉ")][bstack1ll1l1_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭Ṋ")][bstack1ll1l1_opy_ (u"࠭ࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬṋ")], bstack1ll1l1_opy_ (u"ࠧ࡯ࡣࡰࡩࠬṌ"), bstack1ll1l1_opy_ (u"ࠨࡸࡤࡰࡺ࡫ࠧṍ"))
            bstack1111ll1l111_opy_ = capabilities[bstack1ll1l1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡖࡲ࡯ࡪࡴࠧṎ")]
            os.environ[bstack1ll1l1_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨṏ")] = bstack1111ll1l111_opy_
            if bstack1ll1l1_opy_ (u"ࠦࡦࡻࡴࡰ࡯ࡤࡸࡪࠨṐ") in bstack1lllll111ll_opy_ and bstack1lllll111ll_opy_.get(bstack1ll1l1_opy_ (u"ࠧࡧࡰࡱࡡࡤࡹࡹࡵ࡭ࡢࡶࡨࠦṑ")) is None:
                parsed[bstack1ll1l1_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧṒ")] = capabilities[bstack1ll1l1_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨṓ")]
            os.environ[bstack1ll1l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩṔ")] = json.dumps(parsed)
            scripts = bstack1llll11l_opy_.bstack1111ll1111l_opy_(bstack1lllll111ll_opy_[bstack1ll1l1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩṕ")][bstack1ll1l1_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡶࠫṖ")][bstack1ll1l1_opy_ (u"ࠫࡸࡩࡲࡪࡲࡷࡷࠬṗ")], bstack1ll1l1_opy_ (u"ࠬࡴࡡ࡮ࡧࠪṘ"), bstack1ll1l1_opy_ (u"࠭ࡣࡰ࡯ࡰࡥࡳࡪࠧṙ"))
            bstack1ll1l11l1l_opy_.bstack11llllll1_opy_(scripts)
            commands = bstack1lllll111ll_opy_[bstack1ll1l1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧṚ")][bstack1ll1l1_opy_ (u"ࠨࡱࡳࡸ࡮ࡵ࡮ࡴࠩṛ")][bstack1ll1l1_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࡶࡘࡴ࡝ࡲࡢࡲࠪṜ")].get(bstack1ll1l1_opy_ (u"ࠪࡧࡴࡳ࡭ࡢࡰࡧࡷࠬṝ"))
            bstack1ll1l11l1l_opy_.bstack11llll1llll_opy_(commands)
            bstack1ll1l11l1l_opy_.store()
        return [bstack1111ll1l111_opy_, bstack1lllll111ll_opy_[bstack1ll1l1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭Ṟ")]]
    @classmethod
    def bstack1111llll11l_opy_(cls, response=None):
        os.environ[bstack1ll1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪṟ")] = bstack1ll1l1_opy_ (u"࠭࡮ࡶ࡮࡯ࠫṠ")
        os.environ[bstack1ll1l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫṡ")] = bstack1ll1l1_opy_ (u"ࠨࡰࡸࡰࡱ࠭Ṣ")
        os.environ[bstack1ll1l1_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡂࡖࡋࡏࡈࡤࡉࡏࡎࡒࡏࡉ࡙ࡋࡄࠨṣ")] = bstack1ll1l1_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩṤ")
        os.environ[bstack1ll1l1_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡄࡘࡍࡑࡊ࡟ࡉࡃࡖࡌࡊࡊ࡟ࡊࡆࠪṥ")] = bstack1ll1l1_opy_ (u"ࠧࡴࡵ࡭࡮ࠥṦ")
        os.environ[bstack1ll1l1_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡅࡑࡒࡏࡘࡡࡖࡇࡗࡋࡅࡏࡕࡋࡓ࡙࡙ࠧṧ")] = bstack1ll1l1_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧṨ")
        cls.bstack1111ll11lll_opy_(response, bstack1ll1l1_opy_ (u"ࠣࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠣṩ"))
        return [None, None, None]
    @classmethod
    def bstack1111ll1ll11_opy_(cls, response=None):
        os.environ[bstack1ll1l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧṪ")] = bstack1ll1l1_opy_ (u"ࠪࡲࡺࡲ࡬ࠨṫ")
        os.environ[bstack1ll1l1_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩṬ")] = bstack1ll1l1_opy_ (u"ࠬࡴࡵ࡭࡮ࠪṭ")
        os.environ[bstack1ll1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪṮ")] = bstack1ll1l1_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬṯ")
        cls.bstack1111ll11lll_opy_(response, bstack1ll1l1_opy_ (u"ࠣࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠣṰ"))
        return [None, None, None]
    @classmethod
    def bstack1111ll11l1l_opy_(cls, jwt, build_hashed_id):
        os.environ[bstack1ll1l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭ṱ")] = jwt
        os.environ[bstack1ll1l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨṲ")] = build_hashed_id
    @classmethod
    def bstack1111ll11lll_opy_(cls, response=None, product=bstack1ll1l1_opy_ (u"ࠦࠧṳ")):
        if response == None:
            logger.error(product + bstack1ll1l1_opy_ (u"ࠧࠦࡂࡶ࡫࡯ࡨࠥࡩࡲࡦࡣࡷ࡭ࡴࡴࠠࡧࡣ࡬ࡰࡪࡪࠢṴ"))
        for error in response[bstack1ll1l1_opy_ (u"࠭ࡥࡳࡴࡲࡶࡸ࠭ṵ")]:
            bstack11l1l1llll1_opy_ = error[bstack1ll1l1_opy_ (u"ࠧ࡬ࡧࡼࠫṶ")]
            error_message = error[bstack1ll1l1_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩṷ")]
            if error_message:
                if bstack11l1l1llll1_opy_ == bstack1ll1l1_opy_ (u"ࠤࡈࡖࡗࡕࡒࡠࡃࡆࡇࡊ࡙ࡓࡠࡆࡈࡒࡎࡋࡄࠣṸ"):
                    logger.info(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstack1ll1l1_opy_ (u"ࠥࡈࡦࡺࡡࠡࡷࡳࡰࡴࡧࡤࠡࡶࡲࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࠦṹ") + product + bstack1ll1l1_opy_ (u"ࠦࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡪࡵࡦࠢࡷࡳࠥࡹ࡯࡮ࡧࠣࡩࡷࡸ࡯ࡳࠤṺ"))
    @classmethod
    def bstack1111lll1l1l_opy_(cls):
        if cls.bstack111l11lllll_opy_ is not None:
            return
        cls.bstack111l11lllll_opy_ = bstack111l1l1111l_opy_(cls.bstack1111ll1llll_opy_)
        cls.bstack111l11lllll_opy_.start()
    @classmethod
    def bstack111ll11l11_opy_(cls):
        if cls.bstack111l11lllll_opy_ is None:
            return
        cls.bstack111l11lllll_opy_.shutdown()
    @classmethod
    @bstack111ll11ll1_opy_(class_method=True)
    def bstack1111ll1llll_opy_(cls, bstack111lll111l_opy_, event_url=bstack1ll1l1_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠵࠴ࡨࡡࡵࡥ࡫ࠫṻ")):
        config = {
            bstack1ll1l1_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡹࠧṼ"): cls.default_headers()
        }
        logger.debug(bstack1ll1l1_opy_ (u"ࠢࡱࡱࡶࡸࡤࡪࡡࡵࡣ࠽ࠤࡘ࡫࡮ࡥ࡫ࡱ࡫ࠥࡪࡡࡵࡣࠣࡸࡴࠦࡴࡦࡵࡷ࡬ࡺࡨࠠࡧࡱࡵࠤࡪࡼࡥ࡯ࡶࡶࠤࢀࢃࠢṽ").format(bstack1ll1l1_opy_ (u"ࠨ࠮ࠣࠫṾ").join([event[bstack1ll1l1_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭ṿ")] for event in bstack111lll111l_opy_])))
        response = bstack11l1lll1ll_opy_(bstack1ll1l1_opy_ (u"ࠪࡔࡔ࡙ࡔࠨẀ"), cls.request_url(event_url), bstack111lll111l_opy_, config)
        bstack11llll1ll1l_opy_ = response.json()
    @classmethod
    def bstack1l111l1ll_opy_(cls, bstack111lll111l_opy_, event_url=bstack1ll1l1_opy_ (u"ࠫࡦࡶࡩ࠰ࡸ࠴࠳ࡧࡧࡴࡤࡪࠪẁ")):
        logger.debug(bstack1ll1l1_opy_ (u"ࠧࡹࡥ࡯ࡦࡢࡨࡦࡺࡡ࠻ࠢࡄࡸࡹ࡫࡭ࡱࡶ࡬ࡲ࡬ࠦࡴࡰࠢࡤࡨࡩࠦࡤࡢࡶࡤࠤࡹࡵࠠࡣࡣࡷࡧ࡭ࠦࡷࡪࡶ࡫ࠤࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥ࠻ࠢࡾࢁࠧẂ").format(bstack111lll111l_opy_[bstack1ll1l1_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪẃ")]))
        if not bstack1llll11l_opy_.bstack1111lll1l11_opy_(bstack111lll111l_opy_[bstack1ll1l1_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫẄ")]):
            logger.debug(bstack1ll1l1_opy_ (u"ࠣࡵࡨࡲࡩࡥࡤࡢࡶࡤ࠾ࠥࡔ࡯ࡵࠢࡤࡨࡩ࡯࡮ࡨࠢࡧࡥࡹࡧࠠࡸ࡫ࡷ࡬ࠥ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦ࠼ࠣࡿࢂࠨẅ").format(bstack111lll111l_opy_[bstack1ll1l1_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭Ẇ")]))
            return
        bstack1l11lll111_opy_ = bstack1llll11l_opy_.bstack1111llll1l1_opy_(bstack111lll111l_opy_[bstack1ll1l1_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧẇ")], bstack111lll111l_opy_.get(bstack1ll1l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳ࠭Ẉ")))
        if bstack1l11lll111_opy_ != None:
            if bstack111lll111l_opy_.get(bstack1ll1l1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴࠧẉ")) != None:
                bstack111lll111l_opy_[bstack1ll1l1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࠨẊ")][bstack1ll1l1_opy_ (u"ࠧࡱࡴࡲࡨࡺࡩࡴࡠ࡯ࡤࡴࠬẋ")] = bstack1l11lll111_opy_
            else:
                bstack111lll111l_opy_[bstack1ll1l1_opy_ (u"ࠨࡲࡵࡳࡩࡻࡣࡵࡡࡰࡥࡵ࠭Ẍ")] = bstack1l11lll111_opy_
        if event_url == bstack1ll1l1_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠲࠱ࡥࡥࡹࡩࡨࠨẍ"):
            cls.bstack1111lll1l1l_opy_()
            logger.debug(bstack1ll1l1_opy_ (u"ࠥࡷࡪࡴࡤࡠࡦࡤࡸࡦࡀࠠࡂࡦࡧ࡭ࡳ࡭ࠠࡥࡣࡷࡥࠥࡺ࡯ࠡࡤࡤࡸࡨ࡮ࠠࡸ࡫ࡷ࡬ࠥ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦ࠼ࠣࡿࢂࠨẎ").format(bstack111lll111l_opy_[bstack1ll1l1_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨẏ")]))
            cls.bstack111l11lllll_opy_.add(bstack111lll111l_opy_)
        elif event_url == bstack1ll1l1_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠵࠴ࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡵࠪẐ"):
            cls.bstack1111ll1llll_opy_([bstack111lll111l_opy_], event_url)
    @classmethod
    @bstack111ll11ll1_opy_(class_method=True)
    def bstack1l111lll1_opy_(cls, logs):
        bstack1111ll11ll1_opy_ = []
        for log in logs:
            bstack1111llll111_opy_ = {
                bstack1ll1l1_opy_ (u"࠭࡫ࡪࡰࡧࠫẑ"): bstack1ll1l1_opy_ (u"ࠧࡕࡇࡖࡘࡤࡒࡏࡈࠩẒ"),
                bstack1ll1l1_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧẓ"): log[bstack1ll1l1_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨẔ")],
                bstack1ll1l1_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ẕ"): log[bstack1ll1l1_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧẖ")],
                bstack1ll1l1_opy_ (u"ࠬ࡮ࡴࡵࡲࡢࡶࡪࡹࡰࡰࡰࡶࡩࠬẗ"): {},
                bstack1ll1l1_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧẘ"): log[bstack1ll1l1_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨẙ")],
            }
            if bstack1ll1l1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨẚ") in log:
                bstack1111llll111_opy_[bstack1ll1l1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩẛ")] = log[bstack1ll1l1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪẜ")]
            elif bstack1ll1l1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫẝ") in log:
                bstack1111llll111_opy_[bstack1ll1l1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬẞ")] = log[bstack1ll1l1_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ẟ")]
            bstack1111ll11ll1_opy_.append(bstack1111llll111_opy_)
        cls.bstack1l111l1ll_opy_({
            bstack1ll1l1_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫẠ"): bstack1ll1l1_opy_ (u"ࠨࡎࡲ࡫ࡈࡸࡥࡢࡶࡨࡨࠬạ"),
            bstack1ll1l1_opy_ (u"ࠩ࡯ࡳ࡬ࡹࠧẢ"): bstack1111ll11ll1_opy_
        })
    @classmethod
    @bstack111ll11ll1_opy_(class_method=True)
    def bstack1111llll1ll_opy_(cls, steps):
        bstack1111ll1l1l1_opy_ = []
        for step in steps:
            bstack1111ll1lll1_opy_ = {
                bstack1ll1l1_opy_ (u"ࠪ࡯࡮ࡴࡤࠨả"): bstack1ll1l1_opy_ (u"࡙ࠫࡋࡓࡕࡡࡖࡘࡊࡖࠧẤ"),
                bstack1ll1l1_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫấ"): step[bstack1ll1l1_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬẦ")],
                bstack1ll1l1_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪầ"): step[bstack1ll1l1_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫẨ")],
                bstack1ll1l1_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪẩ"): step[bstack1ll1l1_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫẪ")],
                bstack1ll1l1_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳ࠭ẫ"): step[bstack1ll1l1_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴࠧẬ")]
            }
            if bstack1ll1l1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ậ") in step:
                bstack1111ll1lll1_opy_[bstack1ll1l1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧẮ")] = step[bstack1ll1l1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨắ")]
            elif bstack1ll1l1_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩẰ") in step:
                bstack1111ll1lll1_opy_[bstack1ll1l1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪằ")] = step[bstack1ll1l1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫẲ")]
            bstack1111ll1l1l1_opy_.append(bstack1111ll1lll1_opy_)
        cls.bstack1l111l1ll_opy_({
            bstack1ll1l1_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩẳ"): bstack1ll1l1_opy_ (u"࠭ࡌࡰࡩࡆࡶࡪࡧࡴࡦࡦࠪẴ"),
            bstack1ll1l1_opy_ (u"ࠧ࡭ࡱࡪࡷࠬẵ"): bstack1111ll1l1l1_opy_
        })
    @classmethod
    @bstack111ll11ll1_opy_(class_method=True)
    @measure(event_name=EVENTS.bstack111lll11_opy_, stage=STAGE.bstack1llll1l1_opy_)
    def bstack1ll1111l11_opy_(cls, screenshot):
        cls.bstack1l111l1ll_opy_({
            bstack1ll1l1_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬẶ"): bstack1ll1l1_opy_ (u"ࠩࡏࡳ࡬ࡉࡲࡦࡣࡷࡩࡩ࠭ặ"),
            bstack1ll1l1_opy_ (u"ࠪࡰࡴ࡭ࡳࠨẸ"): [{
                bstack1ll1l1_opy_ (u"ࠫࡰ࡯࡮ࡥࠩẹ"): bstack1ll1l1_opy_ (u"࡚ࠬࡅࡔࡖࡢࡗࡈࡘࡅࡆࡐࡖࡌࡔ࡚ࠧẺ"),
                bstack1ll1l1_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩẻ"): datetime.datetime.utcnow().isoformat() + bstack1ll1l1_opy_ (u"࡛ࠧࠩẼ"),
                bstack1ll1l1_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩẽ"): screenshot[bstack1ll1l1_opy_ (u"ࠩ࡬ࡱࡦ࡭ࡥࠨẾ")],
                bstack1ll1l1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪế"): screenshot[bstack1ll1l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫỀ")]
            }]
        }, event_url=bstack1ll1l1_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠵࠴ࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡵࠪề"))
    @classmethod
    @bstack111ll11ll1_opy_(class_method=True)
    def bstack11ll11lll_opy_(cls, driver):
        current_test_uuid = cls.current_test_uuid()
        if not current_test_uuid:
            return
        cls.bstack1l111l1ll_opy_({
            bstack1ll1l1_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪỂ"): bstack1ll1l1_opy_ (u"ࠧࡄࡄࡗࡗࡪࡹࡳࡪࡱࡱࡇࡷ࡫ࡡࡵࡧࡧࠫể"),
            bstack1ll1l1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࠪỄ"): {
                bstack1ll1l1_opy_ (u"ࠤࡸࡹ࡮ࡪࠢễ"): cls.current_test_uuid(),
                bstack1ll1l1_opy_ (u"ࠥ࡭ࡳࡺࡥࡨࡴࡤࡸ࡮ࡵ࡮ࡴࠤỆ"): cls.bstack11l111ll1l_opy_(driver)
            }
        })
    @classmethod
    def bstack11l11l11l1_opy_(cls, event: str, bstack111lll111l_opy_: bstack111lll1ll1_opy_):
        bstack111ll1l1ll_opy_ = {
            bstack1ll1l1_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨệ"): event,
            bstack111lll111l_opy_.bstack111l11llll_opy_(): bstack111lll111l_opy_.bstack111ll11l1l_opy_(event)
        }
        cls.bstack1l111l1ll_opy_(bstack111ll1l1ll_opy_)
        result = getattr(bstack111lll111l_opy_, bstack1ll1l1_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬỈ"), None)
        if event == bstack1ll1l1_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧỉ"):
            threading.current_thread().bstackTestMeta = {bstack1ll1l1_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧỊ"): bstack1ll1l1_opy_ (u"ࠨࡲࡨࡲࡩ࡯࡮ࡨࠩị")}
        elif event == bstack1ll1l1_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫỌ"):
            threading.current_thread().bstackTestMeta = {bstack1ll1l1_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪọ"): getattr(result, bstack1ll1l1_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫỎ"), bstack1ll1l1_opy_ (u"ࠬ࠭ỏ"))}
    @classmethod
    def on(cls):
        if (os.environ.get(bstack1ll1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪỐ"), None) is None or os.environ[bstack1ll1l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫố")] == bstack1ll1l1_opy_ (u"ࠣࡰࡸࡰࡱࠨỒ")) and (os.environ.get(bstack1ll1l1_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧồ"), None) is None or os.environ[bstack1ll1l1_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨỔ")] == bstack1ll1l1_opy_ (u"ࠦࡳࡻ࡬࡭ࠤổ")):
            return False
        return True
    @staticmethod
    def bstack1111ll1ll1l_opy_(func):
        def wrap(*args, **kwargs):
            if bstack1l1lll1lll_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def default_headers():
        headers = {
            bstack1ll1l1_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠫỖ"): bstack1ll1l1_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩỗ"),
            bstack1ll1l1_opy_ (u"࡙ࠧ࠯ࡅࡗ࡙ࡇࡃࡌ࠯ࡗࡉࡘ࡚ࡏࡑࡕࠪỘ"): bstack1ll1l1_opy_ (u"ࠨࡶࡵࡹࡪ࠭ộ")
        }
        if os.environ.get(bstack1ll1l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭Ớ"), None):
            headers[bstack1ll1l1_opy_ (u"ࠪࡅࡺࡺࡨࡰࡴ࡬ࡾࡦࡺࡩࡰࡰࠪớ")] = bstack1ll1l1_opy_ (u"ࠫࡇ࡫ࡡࡳࡧࡵࠤࢀࢃࠧỜ").format(os.environ[bstack1ll1l1_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠤờ")])
        return headers
    @staticmethod
    def request_url(url):
        return bstack1ll1l1_opy_ (u"࠭ࡻࡾ࠱ࡾࢁࠬỞ").format(bstack1111lll1ll1_opy_, url)
    @staticmethod
    def current_test_uuid():
        return getattr(threading.current_thread(), bstack1ll1l1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫở"), None)
    @staticmethod
    def bstack11l111ll1l_opy_(driver):
        return {
            bstack11l1l11l11l_opy_(): bstack11l1ll1111l_opy_(driver)
        }
    @staticmethod
    def bstack1111ll111l1_opy_(exception_info, report):
        return [{bstack1ll1l1_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫỠ"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack1111ll1l11_opy_(typename):
        if bstack1ll1l1_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࠧỡ") in typename:
            return bstack1ll1l1_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࡋࡲࡳࡱࡵࠦỢ")
        return bstack1ll1l1_opy_ (u"࡚ࠦࡴࡨࡢࡰࡧࡰࡪࡪࡅࡳࡴࡲࡶࠧợ")
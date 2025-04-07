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
import logging
import os
import datetime
import threading
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack1l111l11l11_opy_, bstack1l1111l1l1l_opy_, bstack111ll11ll_opy_, bstack111ll1l1l1_opy_, bstack11ll1lll1ll_opy_, bstack11ll1l1111l_opy_, bstack11lll1l1ll1_opy_, bstack1ll11ll11_opy_, bstack1llllllll1_opy_
from bstack_utils.measure import measure
from bstack_utils.bstack111ll1lll1l_opy_ import bstack111ll1ll111_opy_
import bstack_utils.bstack1ll1l11ll_opy_ as bstack11l1111l1_opy_
from bstack_utils.bstack11l111ll1l_opy_ import bstack11l11l11_opy_
import bstack_utils.accessibility as bstack1l1l1l1ll1_opy_
from bstack_utils.bstack11ll1lll1l_opy_ import bstack11ll1lll1l_opy_
from bstack_utils.bstack111lllll1l_opy_ import bstack111ll1l111_opy_
bstack111l1ll11ll_opy_ = bstack11l1l11_opy_ (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡧࡴࡲ࡬ࡦࡥࡷࡳࡷ࠳࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮ࠩᵙ")
logger = logging.getLogger(__name__)
class bstack11lll111l1_opy_:
    bstack111ll1lll1l_opy_ = None
    bs_config = None
    bstack1l11ll1l1_opy_ = None
    @classmethod
    @bstack111ll1l1l1_opy_(class_method=True)
    @measure(event_name=EVENTS.bstack11llll1l111_opy_, stage=STAGE.bstack1l1ll1lll_opy_)
    def launch(cls, bs_config, bstack1l11ll1l1_opy_):
        cls.bs_config = bs_config
        cls.bstack1l11ll1l1_opy_ = bstack1l11ll1l1_opy_
        try:
            cls.bstack111l11lllll_opy_()
            bstack1l111l11111_opy_ = bstack1l111l11l11_opy_(bs_config)
            bstack1l1111llll1_opy_ = bstack1l1111l1l1l_opy_(bs_config)
            data = bstack11l1111l1_opy_.bstack111l1ll1111_opy_(bs_config, bstack1l11ll1l1_opy_)
            config = {
                bstack11l1l11_opy_ (u"ࠪࡥࡺࡺࡨࠨᵚ"): (bstack1l111l11111_opy_, bstack1l1111llll1_opy_),
                bstack11l1l11_opy_ (u"ࠫ࡭࡫ࡡࡥࡧࡵࡷࠬᵛ"): cls.default_headers()
            }
            response = bstack111ll11ll_opy_(bstack11l1l11_opy_ (u"ࠬࡖࡏࡔࡖࠪᵜ"), cls.request_url(bstack11l1l11_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠷࠵ࡢࡶ࡫࡯ࡨࡸ࠭ᵝ")), data, config)
            if response.status_code != 200:
                bstack1lllllll11l_opy_ = response.json()
                if bstack1lllllll11l_opy_[bstack11l1l11_opy_ (u"ࠧࡴࡷࡦࡧࡪࡹࡳࠨᵞ")] == False:
                    cls.bstack111l1l1l1ll_opy_(bstack1lllllll11l_opy_)
                    return
                cls.bstack111l1l1ll1l_opy_(bstack1lllllll11l_opy_[bstack11l1l11_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨᵟ")])
                cls.bstack111l1l1l111_opy_(bstack1lllllll11l_opy_[bstack11l1l11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᵠ")])
                return None
            bstack111l1l1l1l1_opy_ = cls.bstack111l1l111l1_opy_(response)
            return bstack111l1l1l1l1_opy_
        except Exception as error:
            logger.error(bstack11l1l11_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡩࡲࡦࡣࡷ࡭ࡳ࡭ࠠࡣࡷ࡬ࡰࡩࠦࡦࡰࡴࠣࡘࡪࡹࡴࡉࡷࡥ࠾ࠥࢁࡽࠣᵡ").format(str(error)))
            return None
    @classmethod
    @bstack111ll1l1l1_opy_(class_method=True)
    def stop(cls, bstack111l1l11l1l_opy_=None):
        if not bstack11l11l11_opy_.on() and not bstack1l1l1l1ll1_opy_.on():
            return
        if os.environ.get(bstack11l1l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨᵢ")) == bstack11l1l11_opy_ (u"ࠧࡴࡵ࡭࡮ࠥᵣ") or os.environ.get(bstack11l1l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫᵤ")) == bstack11l1l11_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧᵥ"):
            logger.error(bstack11l1l11_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡴࡶࡲࡴࠥࡨࡵࡪ࡮ࡧࠤࡷ࡫ࡱࡶࡧࡶࡸࠥࡺ࡯ࠡࡖࡨࡷࡹࡎࡵࡣ࠼ࠣࡑ࡮ࡹࡳࡪࡰࡪࠤࡦࡻࡴࡩࡧࡱࡸ࡮ࡩࡡࡵ࡫ࡲࡲࠥࡺ࡯࡬ࡧࡱࠫᵦ"))
            return {
                bstack11l1l11_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩᵧ"): bstack11l1l11_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩᵨ"),
                bstack11l1l11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᵩ"): bstack11l1l11_opy_ (u"࡚ࠬ࡯࡬ࡧࡱ࠳ࡧࡻࡩ࡭ࡦࡌࡈࠥ࡯ࡳࠡࡷࡱࡨࡪ࡬ࡩ࡯ࡧࡧ࠰ࠥࡨࡵࡪ࡮ࡧࠤࡨࡸࡥࡢࡶ࡬ࡳࡳࠦ࡭ࡪࡩ࡫ࡸࠥ࡮ࡡࡷࡧࠣࡪࡦ࡯࡬ࡦࡦࠪᵪ")
            }
        try:
            cls.bstack111ll1lll1l_opy_.shutdown()
            data = {
                bstack11l1l11_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᵫ"): bstack1ll11ll11_opy_()
            }
            if not bstack111l1l11l1l_opy_ is None:
                data[bstack11l1l11_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡰࡩࡹࡧࡤࡢࡶࡤࠫᵬ")] = [{
                    bstack11l1l11_opy_ (u"ࠨࡴࡨࡥࡸࡵ࡮ࠨᵭ"): bstack11l1l11_opy_ (u"ࠩࡸࡷࡪࡸ࡟࡬࡫࡯ࡰࡪࡪࠧᵮ"),
                    bstack11l1l11_opy_ (u"ࠪࡷ࡮࡭࡮ࡢ࡮ࠪᵯ"): bstack111l1l11l1l_opy_
                }]
            config = {
                bstack11l1l11_opy_ (u"ࠫ࡭࡫ࡡࡥࡧࡵࡷࠬᵰ"): cls.default_headers()
            }
            bstack11ll11l111l_opy_ = bstack11l1l11_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠵࠴ࡨࡵࡪ࡮ࡧࡷ࠴ࢁࡽ࠰ࡵࡷࡳࡵ࠭ᵱ").format(os.environ[bstack11l1l11_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠦᵲ")])
            bstack111l1l11lll_opy_ = cls.request_url(bstack11ll11l111l_opy_)
            response = bstack111ll11ll_opy_(bstack11l1l11_opy_ (u"ࠧࡑࡗࡗࠫᵳ"), bstack111l1l11lll_opy_, data, config)
            if not response.ok:
                raise Exception(bstack11l1l11_opy_ (u"ࠣࡕࡷࡳࡵࠦࡲࡦࡳࡸࡩࡸࡺࠠ࡯ࡱࡷࠤࡴࡱࠢᵴ"))
        except Exception as error:
            logger.error(bstack11l1l11_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡵࡷࡳࡵࠦࡢࡶ࡫࡯ࡨࠥࡸࡥࡲࡷࡨࡷࡹࠦࡴࡰࠢࡗࡩࡸࡺࡈࡶࡤ࠽࠾ࠥࠨᵵ") + str(error))
            return {
                bstack11l1l11_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪᵶ"): bstack11l1l11_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪᵷ"),
                bstack11l1l11_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᵸ"): str(error)
            }
    @classmethod
    @bstack111ll1l1l1_opy_(class_method=True)
    def bstack111l1l111l1_opy_(cls, response):
        bstack1lllllll11l_opy_ = response.json() if not isinstance(response, dict) else response
        bstack111l1l1l1l1_opy_ = {}
        if bstack1lllllll11l_opy_.get(bstack11l1l11_opy_ (u"࠭ࡪࡸࡶࠪᵹ")) is None:
            os.environ[bstack11l1l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫᵺ")] = bstack11l1l11_opy_ (u"ࠨࡰࡸࡰࡱ࠭ᵻ")
        else:
            os.environ[bstack11l1l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭ᵼ")] = bstack1lllllll11l_opy_.get(bstack11l1l11_opy_ (u"ࠪ࡮ࡼࡺࠧᵽ"), bstack11l1l11_opy_ (u"ࠫࡳࡻ࡬࡭ࠩᵾ"))
        os.environ[bstack11l1l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪᵿ")] = bstack1lllllll11l_opy_.get(bstack11l1l11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨᶀ"), bstack11l1l11_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬᶁ"))
        logger.info(bstack11l1l11_opy_ (u"ࠨࡖࡨࡷࡹ࡮ࡵࡣࠢࡶࡸࡦࡸࡴࡦࡦࠣࡻ࡮ࡺࡨࠡ࡫ࡧ࠾ࠥ࠭ᶂ") + os.getenv(bstack11l1l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧᶃ")));
        if bstack11l11l11_opy_.bstack111l11llll1_opy_(cls.bs_config, cls.bstack1l11ll1l1_opy_.get(bstack11l1l11_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡵࡴࡧࡧࠫᶄ"), bstack11l1l11_opy_ (u"ࠫࠬᶅ"))) is True:
            bstack111ll1l11ll_opy_, build_hashed_id, bstack111l1l111ll_opy_ = cls.bstack111l1l1111l_opy_(bstack1lllllll11l_opy_)
            if bstack111ll1l11ll_opy_ != None and build_hashed_id != None:
                bstack111l1l1l1l1_opy_[bstack11l1l11_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬᶆ")] = {
                    bstack11l1l11_opy_ (u"࠭ࡪࡸࡶࡢࡸࡴࡱࡥ࡯ࠩᶇ"): bstack111ll1l11ll_opy_,
                    bstack11l1l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩᶈ"): build_hashed_id,
                    bstack11l1l11_opy_ (u"ࠨࡣ࡯ࡰࡴࡽ࡟ࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࡷࠬᶉ"): bstack111l1l111ll_opy_
                }
            else:
                bstack111l1l1l1l1_opy_[bstack11l1l11_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩᶊ")] = {}
        else:
            bstack111l1l1l1l1_opy_[bstack11l1l11_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪᶋ")] = {}
        if bstack1l1l1l1ll1_opy_.bstack1l1111l1l_opy_(cls.bs_config) is True:
            bstack111l11ll1ll_opy_, build_hashed_id = cls.bstack111l1l1lll1_opy_(bstack1lllllll11l_opy_)
            if bstack111l11ll1ll_opy_ != None and build_hashed_id != None:
                bstack111l1l1l1l1_opy_[bstack11l1l11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᶌ")] = {
                    bstack11l1l11_opy_ (u"ࠬࡧࡵࡵࡪࡢࡸࡴࡱࡥ࡯ࠩᶍ"): bstack111l11ll1ll_opy_,
                    bstack11l1l11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨᶎ"): build_hashed_id,
                }
            else:
                bstack111l1l1l1l1_opy_[bstack11l1l11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᶏ")] = {}
        else:
            bstack111l1l1l1l1_opy_[bstack11l1l11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᶐ")] = {}
        if bstack111l1l1l1l1_opy_[bstack11l1l11_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩᶑ")].get(bstack11l1l11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬᶒ")) != None or bstack111l1l1l1l1_opy_[bstack11l1l11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᶓ")].get(bstack11l1l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧᶔ")) != None:
            cls.bstack111l1l11l11_opy_(bstack1lllllll11l_opy_.get(bstack11l1l11_opy_ (u"࠭ࡪࡸࡶࠪᶕ")), bstack1lllllll11l_opy_.get(bstack11l1l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩᶖ")))
        return bstack111l1l1l1l1_opy_
    @classmethod
    def bstack111l1l1111l_opy_(cls, bstack1lllllll11l_opy_):
        if bstack1lllllll11l_opy_.get(bstack11l1l11_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨᶗ")) == None:
            cls.bstack111l1l1ll1l_opy_()
            return [None, None, None]
        if bstack1lllllll11l_opy_[bstack11l1l11_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩᶘ")][bstack11l1l11_opy_ (u"ࠪࡷࡺࡩࡣࡦࡵࡶࠫᶙ")] != True:
            cls.bstack111l1l1ll1l_opy_(bstack1lllllll11l_opy_[bstack11l1l11_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫᶚ")])
            return [None, None, None]
        logger.debug(bstack11l1l11_opy_ (u"࡚ࠬࡥࡴࡶࠣࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠣࡆࡺ࡯࡬ࡥࠢࡦࡶࡪࡧࡴࡪࡱࡱࠤࡘࡻࡣࡤࡧࡶࡷ࡫ࡻ࡬ࠢࠩᶛ"))
        os.environ[bstack11l1l11_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡆ࡚ࡏࡌࡅࡡࡆࡓࡒࡖࡌࡆࡖࡈࡈࠬᶜ")] = bstack11l1l11_opy_ (u"ࠧࡵࡴࡸࡩࠬᶝ")
        if bstack1lllllll11l_opy_.get(bstack11l1l11_opy_ (u"ࠨ࡬ࡺࡸࠬᶞ")):
            os.environ[bstack11l1l11_opy_ (u"ࠩࡆࡖࡊࡊࡅࡏࡖࡌࡅࡑ࡙࡟ࡇࡑࡕࡣࡈࡘࡁࡔࡊࡢࡖࡊࡖࡏࡓࡖࡌࡒࡌ࠭ᶟ")] = json.dumps({
                bstack11l1l11_opy_ (u"ࠪࡹࡸ࡫ࡲ࡯ࡣࡰࡩࠬᶠ"): bstack1l111l11l11_opy_(cls.bs_config),
                bstack11l1l11_opy_ (u"ࠫࡵࡧࡳࡴࡹࡲࡶࡩ࠭ᶡ"): bstack1l1111l1l1l_opy_(cls.bs_config)
            })
        if bstack1lllllll11l_opy_.get(bstack11l1l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧᶢ")):
            os.environ[bstack11l1l11_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡆ࡚ࡏࡌࡅࡡࡋࡅࡘࡎࡅࡅࡡࡌࡈࠬᶣ")] = bstack1lllllll11l_opy_[bstack11l1l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩᶤ")]
        if bstack1lllllll11l_opy_[bstack11l1l11_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨᶥ")].get(bstack11l1l11_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵࠪᶦ"), {}).get(bstack11l1l11_opy_ (u"ࠪࡥࡱࡲ࡯ࡸࡡࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࡹࠧᶧ")):
            os.environ[bstack11l1l11_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡃࡏࡐࡔ࡝࡟ࡔࡅࡕࡉࡊࡔࡓࡉࡑࡗࡗࠬᶨ")] = str(bstack1lllllll11l_opy_[bstack11l1l11_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬᶩ")][bstack11l1l11_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡹࠧᶪ")][bstack11l1l11_opy_ (u"ࠧࡢ࡮࡯ࡳࡼࡥࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࡶࠫᶫ")])
        else:
            os.environ[bstack11l1l11_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡇࡌࡍࡑ࡚ࡣࡘࡉࡒࡆࡇࡑࡗࡍࡕࡔࡔࠩᶬ")] = bstack11l1l11_opy_ (u"ࠤࡱࡹࡱࡲࠢᶭ")
        return [bstack1lllllll11l_opy_[bstack11l1l11_opy_ (u"ࠪ࡮ࡼࡺࠧᶮ")], bstack1lllllll11l_opy_[bstack11l1l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ᶯ")], os.environ[bstack11l1l11_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡄࡐࡑࡕࡗࡠࡕࡆࡖࡊࡋࡎࡔࡊࡒࡘࡘ࠭ᶰ")]]
    @classmethod
    def bstack111l1l1lll1_opy_(cls, bstack1lllllll11l_opy_):
        if bstack1lllllll11l_opy_.get(bstack11l1l11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᶱ")) == None:
            cls.bstack111l1l1l111_opy_()
            return [None, None]
        if bstack1lllllll11l_opy_[bstack11l1l11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᶲ")][bstack11l1l11_opy_ (u"ࠨࡵࡸࡧࡨ࡫ࡳࡴࠩᶳ")] != True:
            cls.bstack111l1l1l111_opy_(bstack1lllllll11l_opy_[bstack11l1l11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᶴ")])
            return [None, None]
        if bstack1lllllll11l_opy_[bstack11l1l11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᶵ")].get(bstack11l1l11_opy_ (u"ࠫࡴࡶࡴࡪࡱࡱࡷࠬᶶ")):
            logger.debug(bstack11l1l11_opy_ (u"࡚ࠬࡥࡴࡶࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡆࡺ࡯࡬ࡥࠢࡦࡶࡪࡧࡴࡪࡱࡱࠤࡘࡻࡣࡤࡧࡶࡷ࡫ࡻ࡬ࠢࠩᶷ"))
            parsed = json.loads(os.getenv(bstack11l1l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧᶸ"), bstack11l1l11_opy_ (u"ࠧࡼࡿࠪᶹ")))
            capabilities = bstack11l1111l1_opy_.bstack111l1ll11l1_opy_(bstack1lllllll11l_opy_[bstack11l1l11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᶺ")][bstack11l1l11_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵࠪᶻ")][bstack11l1l11_opy_ (u"ࠪࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩᶼ")], bstack11l1l11_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᶽ"), bstack11l1l11_opy_ (u"ࠬࡼࡡ࡭ࡷࡨࠫᶾ"))
            bstack111l11ll1ll_opy_ = capabilities[bstack11l1l11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࡚࡯࡬ࡧࡱࠫᶿ")]
            os.environ[bstack11l1l11_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬ᷀")] = bstack111l11ll1ll_opy_
            if bstack11l1l11_opy_ (u"ࠣࡣࡸࡸࡴࡳࡡࡵࡧࠥ᷁") in bstack1lllllll11l_opy_ and bstack1lllllll11l_opy_.get(bstack11l1l11_opy_ (u"ࠤࡤࡴࡵࡥࡡࡶࡶࡲࡱࡦࡺࡥ᷂ࠣ")) is None:
                parsed[bstack11l1l11_opy_ (u"ࠪࡷࡨࡧ࡮࡯ࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫ᷃")] = capabilities[bstack11l1l11_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬ᷄")]
            os.environ[bstack11l1l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭᷅")] = json.dumps(parsed)
            scripts = bstack11l1111l1_opy_.bstack111l1ll11l1_opy_(bstack1lllllll11l_opy_[bstack11l1l11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭᷆")][bstack11l1l11_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࠨ᷇")][bstack11l1l11_opy_ (u"ࠨࡵࡦࡶ࡮ࡶࡴࡴࠩ᷈")], bstack11l1l11_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ᷉"), bstack11l1l11_opy_ (u"ࠪࡧࡴࡳ࡭ࡢࡰࡧ᷊ࠫ"))
            bstack11ll1lll1l_opy_.bstack1l1l1l1111_opy_(scripts)
            commands = bstack1lllllll11l_opy_[bstack11l1l11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ᷋")][bstack11l1l11_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭᷌")][bstack11l1l11_opy_ (u"࠭ࡣࡰ࡯ࡰࡥࡳࡪࡳࡕࡱ࡚ࡶࡦࡶࠧ᷍")].get(bstack11l1l11_opy_ (u"ࠧࡤࡱࡰࡱࡦࡴࡤࡴ᷎ࠩ"))
            bstack11ll1lll1l_opy_.bstack1l111ll1ll1_opy_(commands)
            bstack11ll1lll1l_opy_.store()
        return [bstack111l11ll1ll_opy_, bstack1lllllll11l_opy_[bstack11l1l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦ᷏ࠪ")]]
    @classmethod
    def bstack111l1l1ll1l_opy_(cls, response=None):
        os.environ[bstack11l1l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊ᷐ࠧ")] = bstack11l1l11_opy_ (u"ࠪࡲࡺࡲ࡬ࠨ᷑")
        os.environ[bstack11l1l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨ᷒")] = bstack11l1l11_opy_ (u"ࠬࡴࡵ࡭࡮ࠪᷓ")
        os.environ[bstack11l1l11_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡆ࡚ࡏࡌࡅࡡࡆࡓࡒࡖࡌࡆࡖࡈࡈࠬᷔ")] = bstack11l1l11_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭ᷕ")
        os.environ[bstack11l1l11_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡈࡕࡊࡎࡇࡣࡍࡇࡓࡉࡇࡇࡣࡎࡊࠧᷖ")] = bstack11l1l11_opy_ (u"ࠤࡱࡹࡱࡲࠢᷗ")
        os.environ[bstack11l1l11_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡂࡎࡏࡓ࡜ࡥࡓࡄࡔࡈࡉࡓ࡙ࡈࡐࡖࡖࠫᷘ")] = bstack11l1l11_opy_ (u"ࠦࡳࡻ࡬࡭ࠤᷙ")
        cls.bstack111l1l1l1ll_opy_(response, bstack11l1l11_opy_ (u"ࠧࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠧᷚ"))
        return [None, None, None]
    @classmethod
    def bstack111l1l1l111_opy_(cls, response=None):
        os.environ[bstack11l1l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫᷛ")] = bstack11l1l11_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬᷜ")
        os.environ[bstack11l1l11_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ᷝ")] = bstack11l1l11_opy_ (u"ࠩࡱࡹࡱࡲࠧᷞ")
        os.environ[bstack11l1l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧᷟ")] = bstack11l1l11_opy_ (u"ࠫࡳࡻ࡬࡭ࠩᷠ")
        cls.bstack111l1l1l1ll_opy_(response, bstack11l1l11_opy_ (u"ࠧࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠧᷡ"))
        return [None, None, None]
    @classmethod
    def bstack111l1l11l11_opy_(cls, jwt, build_hashed_id):
        os.environ[bstack11l1l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪᷢ")] = jwt
        os.environ[bstack11l1l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬᷣ")] = build_hashed_id
    @classmethod
    def bstack111l1l1l1ll_opy_(cls, response=None, product=bstack11l1l11_opy_ (u"ࠣࠤᷤ")):
        if response == None:
            logger.error(product + bstack11l1l11_opy_ (u"ࠤࠣࡆࡺ࡯࡬ࡥࠢࡦࡶࡪࡧࡴࡪࡱࡱࠤ࡫ࡧࡩ࡭ࡧࡧࠦᷥ"))
        for error in response[bstack11l1l11_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࡵࠪᷦ")]:
            bstack11ll11ll111_opy_ = error[bstack11l1l11_opy_ (u"ࠫࡰ࡫ࡹࠨᷧ")]
            error_message = error[bstack11l1l11_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᷨ")]
            if error_message:
                if bstack11ll11ll111_opy_ == bstack11l1l11_opy_ (u"ࠨࡅࡓࡔࡒࡖࡤࡇࡃࡄࡇࡖࡗࡤࡊࡅࡏࡋࡈࡈࠧᷩ"):
                    logger.info(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstack11l1l11_opy_ (u"ࠢࡅࡣࡷࡥࠥࡻࡰ࡭ࡱࡤࡨࠥࡺ࡯ࠡࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࠣᷪ") + product + bstack11l1l11_opy_ (u"ࠣࠢࡩࡥ࡮ࡲࡥࡥࠢࡧࡹࡪࠦࡴࡰࠢࡶࡳࡲ࡫ࠠࡦࡴࡵࡳࡷࠨᷫ"))
    @classmethod
    def bstack111l11lllll_opy_(cls):
        if cls.bstack111ll1lll1l_opy_ is not None:
            return
        cls.bstack111ll1lll1l_opy_ = bstack111ll1ll111_opy_(cls.bstack111l1ll111l_opy_)
        cls.bstack111ll1lll1l_opy_.start()
    @classmethod
    def bstack111l1l1ll1_opy_(cls):
        if cls.bstack111ll1lll1l_opy_ is None:
            return
        cls.bstack111ll1lll1l_opy_.shutdown()
    @classmethod
    @bstack111ll1l1l1_opy_(class_method=True)
    def bstack111l1ll111l_opy_(cls, bstack111ll1ll1l_opy_, event_url=bstack11l1l11_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠲࠱ࡥࡥࡹࡩࡨࠨᷬ")):
        config = {
            bstack11l1l11_opy_ (u"ࠪ࡬ࡪࡧࡤࡦࡴࡶࠫᷭ"): cls.default_headers()
        }
        logger.debug(bstack11l1l11_opy_ (u"ࠦࡵࡵࡳࡵࡡࡧࡥࡹࡧ࠺ࠡࡕࡨࡲࡩ࡯࡮ࡨࠢࡧࡥࡹࡧࠠࡵࡱࠣࡸࡪࡹࡴࡩࡷࡥࠤ࡫ࡵࡲࠡࡧࡹࡩࡳࡺࡳࠡࡽࢀࠦᷮ").format(bstack11l1l11_opy_ (u"ࠬ࠲ࠠࠨᷯ").join([event[bstack11l1l11_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪᷰ")] for event in bstack111ll1ll1l_opy_])))
        response = bstack111ll11ll_opy_(bstack11l1l11_opy_ (u"ࠧࡑࡑࡖࡘࠬᷱ"), cls.request_url(event_url), bstack111ll1ll1l_opy_, config)
        bstack1l1111l1l11_opy_ = response.json()
    @classmethod
    def bstack1ll1l1l1ll_opy_(cls, bstack111ll1ll1l_opy_, event_url=bstack11l1l11_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠱࠰ࡤࡤࡸࡨ࡮ࠧᷲ")):
        logger.debug(bstack11l1l11_opy_ (u"ࠤࡶࡩࡳࡪ࡟ࡥࡣࡷࡥ࠿ࠦࡁࡵࡶࡨࡱࡵࡺࡩ࡯ࡩࠣࡸࡴࠦࡡࡥࡦࠣࡨࡦࡺࡡࠡࡶࡲࠤࡧࡧࡴࡤࡪࠣࡻ࡮ࡺࡨࠡࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩ࠿ࠦࡻࡾࠤᷳ").format(bstack111ll1ll1l_opy_[bstack11l1l11_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧᷴ")]))
        if not bstack11l1111l1_opy_.bstack111l1l1ll11_opy_(bstack111ll1ll1l_opy_[bstack11l1l11_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨ᷵")]):
            logger.debug(bstack11l1l11_opy_ (u"ࠧࡹࡥ࡯ࡦࡢࡨࡦࡺࡡ࠻ࠢࡑࡳࡹࠦࡡࡥࡦ࡬ࡲ࡬ࠦࡤࡢࡶࡤࠤࡼ࡯ࡴࡩࠢࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪࡀࠠࡼࡿࠥ᷶").format(bstack111ll1ll1l_opy_[bstack11l1l11_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧ᷷ࠪ")]))
            return
        bstack11l1l111l_opy_ = bstack11l1111l1_opy_.bstack111l1ll1l11_opy_(bstack111ll1ll1l_opy_[bstack11l1l11_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨ᷸ࠫ")], bstack111ll1ll1l_opy_.get(bstack11l1l11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰ᷹ࠪ")))
        if bstack11l1l111l_opy_ != None:
            if bstack111ll1ll1l_opy_.get(bstack11l1l11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱ᷺ࠫ")) != None:
                bstack111ll1ll1l_opy_[bstack11l1l11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࠬ᷻")][bstack11l1l11_opy_ (u"ࠫࡵࡸ࡯ࡥࡷࡦࡸࡤࡳࡡࡱࠩ᷼")] = bstack11l1l111l_opy_
            else:
                bstack111ll1ll1l_opy_[bstack11l1l11_opy_ (u"ࠬࡶࡲࡰࡦࡸࡧࡹࡥ࡭ࡢࡲ᷽ࠪ")] = bstack11l1l111l_opy_
        if event_url == bstack11l1l11_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠶࠵ࡢࡢࡶࡦ࡬ࠬ᷾"):
            cls.bstack111l11lllll_opy_()
            logger.debug(bstack11l1l11_opy_ (u"ࠢࡴࡧࡱࡨࡤࡪࡡࡵࡣ࠽ࠤࡆࡪࡤࡪࡰࡪࠤࡩࡧࡴࡢࠢࡷࡳࠥࡨࡡࡵࡥ࡫ࠤࡼ࡯ࡴࡩࠢࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪࡀࠠࡼࡿ᷿ࠥ").format(bstack111ll1ll1l_opy_[bstack11l1l11_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬḀ")]))
            cls.bstack111ll1lll1l_opy_.add(bstack111ll1ll1l_opy_)
        elif event_url == bstack11l1l11_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠲࠱ࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࡹࠧḁ"):
            cls.bstack111l1ll111l_opy_([bstack111ll1ll1l_opy_], event_url)
    @classmethod
    @bstack111ll1l1l1_opy_(class_method=True)
    def bstack1lll1l1111_opy_(cls, logs):
        bstack111l11ll1l1_opy_ = []
        for log in logs:
            bstack111l1l1l11l_opy_ = {
                bstack11l1l11_opy_ (u"ࠪ࡯࡮ࡴࡤࠨḂ"): bstack11l1l11_opy_ (u"࡙ࠫࡋࡓࡕࡡࡏࡓࡌ࠭ḃ"),
                bstack11l1l11_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫḄ"): log[bstack11l1l11_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬḅ")],
                bstack11l1l11_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪḆ"): log[bstack11l1l11_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫḇ")],
                bstack11l1l11_opy_ (u"ࠩ࡫ࡸࡹࡶ࡟ࡳࡧࡶࡴࡴࡴࡳࡦࠩḈ"): {},
                bstack11l1l11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫḉ"): log[bstack11l1l11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬḊ")],
            }
            if bstack11l1l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬḋ") in log:
                bstack111l1l1l11l_opy_[bstack11l1l11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭Ḍ")] = log[bstack11l1l11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧḍ")]
            elif bstack11l1l11_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨḎ") in log:
                bstack111l1l1l11l_opy_[bstack11l1l11_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩḏ")] = log[bstack11l1l11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪḐ")]
            bstack111l11ll1l1_opy_.append(bstack111l1l1l11l_opy_)
        cls.bstack1ll1l1l1ll_opy_({
            bstack11l1l11_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨḑ"): bstack11l1l11_opy_ (u"ࠬࡒ࡯ࡨࡅࡵࡩࡦࡺࡥࡥࠩḒ"),
            bstack11l1l11_opy_ (u"࠭࡬ࡰࡩࡶࠫḓ"): bstack111l11ll1l1_opy_
        })
    @classmethod
    @bstack111ll1l1l1_opy_(class_method=True)
    def bstack111l1l11ll1_opy_(cls, steps):
        bstack111l11lll1l_opy_ = []
        for step in steps:
            bstack111l1l1llll_opy_ = {
                bstack11l1l11_opy_ (u"ࠧ࡬࡫ࡱࡨࠬḔ"): bstack11l1l11_opy_ (u"ࠨࡖࡈࡗ࡙ࡥࡓࡕࡇࡓࠫḕ"),
                bstack11l1l11_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨḖ"): step[bstack11l1l11_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩḗ")],
                bstack11l1l11_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧḘ"): step[bstack11l1l11_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨḙ")],
                bstack11l1l11_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧḚ"): step[bstack11l1l11_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨḛ")],
                bstack11l1l11_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࠪḜ"): step[bstack11l1l11_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࠫḝ")]
            }
            if bstack11l1l11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪḞ") in step:
                bstack111l1l1llll_opy_[bstack11l1l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫḟ")] = step[bstack11l1l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬḠ")]
            elif bstack11l1l11_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ḡ") in step:
                bstack111l1l1llll_opy_[bstack11l1l11_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧḢ")] = step[bstack11l1l11_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨḣ")]
            bstack111l11lll1l_opy_.append(bstack111l1l1llll_opy_)
        cls.bstack1ll1l1l1ll_opy_({
            bstack11l1l11_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭Ḥ"): bstack11l1l11_opy_ (u"ࠪࡐࡴ࡭ࡃࡳࡧࡤࡸࡪࡪࠧḥ"),
            bstack11l1l11_opy_ (u"ࠫࡱࡵࡧࡴࠩḦ"): bstack111l11lll1l_opy_
        })
    @classmethod
    @bstack111ll1l1l1_opy_(class_method=True)
    @measure(event_name=EVENTS.bstack1l1lllll1l_opy_, stage=STAGE.bstack1l1ll1lll_opy_)
    def bstack11ll1111ll_opy_(cls, screenshot):
        cls.bstack1ll1l1l1ll_opy_({
            bstack11l1l11_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩḧ"): bstack11l1l11_opy_ (u"࠭ࡌࡰࡩࡆࡶࡪࡧࡴࡦࡦࠪḨ"),
            bstack11l1l11_opy_ (u"ࠧ࡭ࡱࡪࡷࠬḩ"): [{
                bstack11l1l11_opy_ (u"ࠨ࡭࡬ࡲࡩ࠭Ḫ"): bstack11l1l11_opy_ (u"ࠩࡗࡉࡘ࡚࡟ࡔࡅࡕࡉࡊࡔࡓࡉࡑࡗࠫḫ"),
                bstack11l1l11_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭Ḭ"): datetime.datetime.utcnow().isoformat() + bstack11l1l11_opy_ (u"ࠫ࡟࠭ḭ"),
                bstack11l1l11_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭Ḯ"): screenshot[bstack11l1l11_opy_ (u"࠭ࡩ࡮ࡣࡪࡩࠬḯ")],
                bstack11l1l11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧḰ"): screenshot[bstack11l1l11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨḱ")]
            }]
        }, event_url=bstack11l1l11_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠲࠱ࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࡹࠧḲ"))
    @classmethod
    @bstack111ll1l1l1_opy_(class_method=True)
    def bstack11ll1111_opy_(cls, driver):
        current_test_uuid = cls.current_test_uuid()
        if not current_test_uuid:
            return
        cls.bstack1ll1l1l1ll_opy_({
            bstack11l1l11_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧḳ"): bstack11l1l11_opy_ (u"ࠫࡈࡈࡔࡔࡧࡶࡷ࡮ࡵ࡮ࡄࡴࡨࡥࡹ࡫ࡤࠨḴ"),
            bstack11l1l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴࠧḵ"): {
                bstack11l1l11_opy_ (u"ࠨࡵࡶ࡫ࡧࠦḶ"): cls.current_test_uuid(),
                bstack11l1l11_opy_ (u"ࠢࡪࡰࡷࡩ࡬ࡸࡡࡵ࡫ࡲࡲࡸࠨḷ"): cls.bstack11l11l111l_opy_(driver)
            }
        })
    @classmethod
    def bstack111lllllll_opy_(cls, event: str, bstack111ll1ll1l_opy_: bstack111ll1l111_opy_):
        bstack111ll11ll1_opy_ = {
            bstack11l1l11_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬḸ"): event,
            bstack111ll1ll1l_opy_.bstack111ll111l1_opy_(): bstack111ll1ll1l_opy_.bstack111llll1l1_opy_(event)
        }
        cls.bstack1ll1l1l1ll_opy_(bstack111ll11ll1_opy_)
        result = getattr(bstack111ll1ll1l_opy_, bstack11l1l11_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩḹ"), None)
        if event == bstack11l1l11_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫḺ"):
            threading.current_thread().bstackTestMeta = {bstack11l1l11_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫḻ"): bstack11l1l11_opy_ (u"ࠬࡶࡥ࡯ࡦ࡬ࡲ࡬࠭Ḽ")}
        elif event == bstack11l1l11_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨḽ"):
            threading.current_thread().bstackTestMeta = {bstack11l1l11_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧḾ"): getattr(result, bstack11l1l11_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨḿ"), bstack11l1l11_opy_ (u"ࠩࠪṀ"))}
    @classmethod
    def on(cls):
        if (os.environ.get(bstack11l1l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧṁ"), None) is None or os.environ[bstack11l1l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨṂ")] == bstack11l1l11_opy_ (u"ࠧࡴࡵ࡭࡮ࠥṃ")) and (os.environ.get(bstack11l1l11_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫṄ"), None) is None or os.environ[bstack11l1l11_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬṅ")] == bstack11l1l11_opy_ (u"ࠣࡰࡸࡰࡱࠨṆ")):
            return False
        return True
    @staticmethod
    def bstack111l1l11111_opy_(func):
        def wrap(*args, **kwargs):
            if bstack11lll111l1_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def default_headers():
        headers = {
            bstack11l1l11_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡘࡾࡶࡥࠨṇ"): bstack11l1l11_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭Ṉ"),
            bstack11l1l11_opy_ (u"ࠫ࡝࠳ࡂࡔࡖࡄࡇࡐ࠳ࡔࡆࡕࡗࡓࡕ࡙ࠧṉ"): bstack11l1l11_opy_ (u"ࠬࡺࡲࡶࡧࠪṊ")
        }
        if os.environ.get(bstack11l1l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪṋ"), None):
            headers[bstack11l1l11_opy_ (u"ࠧࡂࡷࡷ࡬ࡴࡸࡩࡻࡣࡷ࡭ࡴࡴࠧṌ")] = bstack11l1l11_opy_ (u"ࠨࡄࡨࡥࡷ࡫ࡲࠡࡽࢀࠫṍ").format(os.environ[bstack11l1l11_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙ࠨṎ")])
        return headers
    @staticmethod
    def request_url(url):
        return bstack11l1l11_opy_ (u"ࠪࡿࢂ࠵ࡻࡾࠩṏ").format(bstack111l1ll11ll_opy_, url)
    @staticmethod
    def current_test_uuid():
        return getattr(threading.current_thread(), bstack11l1l11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨṐ"), None)
    @staticmethod
    def bstack11l11l111l_opy_(driver):
        return {
            bstack11ll1lll1ll_opy_(): bstack11ll1l1111l_opy_(driver)
        }
    @staticmethod
    def bstack111l11lll11_opy_(exception_info, report):
        return [{bstack11l1l11_opy_ (u"ࠬࡨࡡࡤ࡭ࡷࡶࡦࡩࡥࠨṑ"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack1111ll1lll_opy_(typename):
        if bstack11l1l11_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࠤṒ") in typename:
            return bstack11l1l11_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࡈࡶࡷࡵࡲࠣṓ")
        return bstack11l1l11_opy_ (u"ࠣࡗࡱ࡬ࡦࡴࡤ࡭ࡧࡧࡉࡷࡸ࡯ࡳࠤṔ")
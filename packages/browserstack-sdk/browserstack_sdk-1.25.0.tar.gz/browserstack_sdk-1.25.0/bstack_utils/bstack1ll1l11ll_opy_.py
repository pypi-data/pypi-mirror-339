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
import datetime
import threading
from bstack_utils.helper import bstack1l111l111l1_opy_, bstack1ll1lllll1_opy_, get_host_info, bstack11lll1ll111_opy_, \
 bstack1l1l1ll11l_opy_, bstack1llllllll1_opy_, bstack111ll1l1l1_opy_, bstack11lll1l1ll1_opy_, bstack1ll11ll11_opy_
import bstack_utils.accessibility as bstack1l1l1l1ll1_opy_
from bstack_utils.bstack11l111ll1l_opy_ import bstack11l11l11_opy_
from bstack_utils.percy import bstack111l11l1l_opy_
from bstack_utils.config import Config
bstack111ll1lll_opy_ = Config.bstack111l1l1l_opy_()
logger = logging.getLogger(__name__)
percy = bstack111l11l1l_opy_()
@bstack111ll1l1l1_opy_(class_method=False)
def bstack111l1ll1111_opy_(bs_config, bstack1l11ll1l1_opy_):
  try:
    data = {
        bstack11l1l11_opy_ (u"ࠩࡩࡳࡷࡳࡡࡵࠩṕ"): bstack11l1l11_opy_ (u"ࠪ࡮ࡸࡵ࡮ࠨṖ"),
        bstack11l1l11_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡤࡴࡡ࡮ࡧࠪṗ"): bs_config.get(bstack11l1l11_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪṘ"), bstack11l1l11_opy_ (u"࠭ࠧṙ")),
        bstack11l1l11_opy_ (u"ࠧ࡯ࡣࡰࡩࠬṚ"): bs_config.get(bstack11l1l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫṛ"), os.path.basename(os.path.abspath(os.getcwd()))),
        bstack11l1l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠ࡫ࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬṜ"): bs_config.get(bstack11l1l11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬṝ")),
        bstack11l1l11_opy_ (u"ࠫࡩ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠩṞ"): bs_config.get(bstack11l1l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡈࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨṟ"), bstack11l1l11_opy_ (u"࠭ࠧṠ")),
        bstack11l1l11_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫṡ"): bstack1ll11ll11_opy_(),
        bstack11l1l11_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭Ṣ"): bstack11lll1ll111_opy_(bs_config),
        bstack11l1l11_opy_ (u"ࠩ࡫ࡳࡸࡺ࡟ࡪࡰࡩࡳࠬṣ"): get_host_info(),
        bstack11l1l11_opy_ (u"ࠪࡧ࡮ࡥࡩ࡯ࡨࡲࠫṤ"): bstack1ll1lllll1_opy_(),
        bstack11l1l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢࡶࡺࡴ࡟ࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫṥ"): os.environ.get(bstack11l1l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇ࡛ࡉࡍࡆࡢࡖ࡚ࡔ࡟ࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕࠫṦ")),
        bstack11l1l11_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩࡥࡴࡦࡵࡷࡷࡤࡸࡥࡳࡷࡱࠫṧ"): os.environ.get(bstack11l1l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡒࡆࡔࡘࡒࠬṨ"), False),
        bstack11l1l11_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯ࡡࡦࡳࡳࡺࡲࡰ࡮ࠪṩ"): bstack1l111l111l1_opy_(),
        bstack11l1l11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩṪ"): bstack111l11l1lll_opy_(),
        bstack11l1l11_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡤࡦࡶࡤ࡭ࡱࡹࠧṫ"): bstack111l11l1l1l_opy_(bstack1l11ll1l1_opy_),
        bstack11l1l11_opy_ (u"ࠫࡵࡸ࡯ࡥࡷࡦࡸࡤࡳࡡࡱࠩṬ"): bstack1ll1l111l1_opy_(bs_config, bstack1l11ll1l1_opy_.get(bstack11l1l11_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡷࡶࡩࡩ࠭ṭ"), bstack11l1l11_opy_ (u"࠭ࠧṮ"))),
        bstack11l1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩṯ"): bstack1l1l1ll11l_opy_(bs_config),
    }
    return data
  except Exception as error:
    logger.error(bstack11l1l11_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡧࡷ࡫ࡡࡵ࡫ࡱ࡫ࠥࡶࡡࡺ࡮ࡲࡥࡩࠦࡦࡰࡴࠣࡘࡪࡹࡴࡉࡷࡥ࠾ࠥࠦࡻࡾࠤṰ").format(str(error)))
    return None
def bstack111l11l1l1l_opy_(framework):
  return {
    bstack11l1l11_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡓࡧ࡭ࡦࠩṱ"): framework.get(bstack11l1l11_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࠫṲ"), bstack11l1l11_opy_ (u"ࠫࡕࡿࡴࡦࡵࡷࠫṳ")),
    bstack11l1l11_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡗࡧࡵࡷ࡮ࡵ࡮ࠨṴ"): framework.get(bstack11l1l11_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡹࡩࡷࡹࡩࡰࡰࠪṵ")),
    bstack11l1l11_opy_ (u"ࠧࡴࡦ࡮࡚ࡪࡸࡳࡪࡱࡱࠫṶ"): framework.get(bstack11l1l11_opy_ (u"ࠨࡵࡧ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ṷ")),
    bstack11l1l11_opy_ (u"ࠩ࡯ࡥࡳ࡭ࡵࡢࡩࡨࠫṸ"): bstack11l1l11_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪṹ"),
    bstack11l1l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫṺ"): framework.get(bstack11l1l11_opy_ (u"ࠬࡺࡥࡴࡶࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࠬṻ"))
  }
def bstack1ll1l111l1_opy_(bs_config, framework):
  bstack1l111l1l_opy_ = False
  bstack1l111l111l_opy_ = False
  bstack111l11l111l_opy_ = False
  if bstack11l1l11_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪṼ") in bs_config:
    bstack111l11l111l_opy_ = True
  elif bstack11l1l11_opy_ (u"ࠧࡢࡲࡳࠫṽ") in bs_config:
    bstack1l111l1l_opy_ = True
  else:
    bstack1l111l111l_opy_ = True
  bstack11l1l111l_opy_ = {
    bstack11l1l11_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨṾ"): bstack11l11l11_opy_.bstack111l11ll111_opy_(bs_config, framework),
    bstack11l1l11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩṿ"): bstack1l1l1l1ll1_opy_.bstack1l1111l1l_opy_(bs_config),
    bstack11l1l11_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩẀ"): bs_config.get(bstack11l1l11_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪẁ"), False),
    bstack11l1l11_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡫ࠧẂ"): bstack1l111l111l_opy_,
    bstack11l1l11_opy_ (u"࠭ࡡࡱࡲࡢࡥࡺࡺ࡯࡮ࡣࡷࡩࠬẃ"): bstack1l111l1l_opy_,
    bstack11l1l11_opy_ (u"ࠧࡵࡷࡵࡦࡴࡹࡣࡢ࡮ࡨࠫẄ"): bstack111l11l111l_opy_
  }
  return bstack11l1l111l_opy_
@bstack111ll1l1l1_opy_(class_method=False)
def bstack111l11l1lll_opy_():
  try:
    bstack111l11l1l11_opy_ = json.loads(os.getenv(bstack11l1l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩẅ"), bstack11l1l11_opy_ (u"ࠩࡾࢁࠬẆ")))
    return {
        bstack11l1l11_opy_ (u"ࠪࡷࡪࡺࡴࡪࡰࡪࡷࠬẇ"): bstack111l11l1l11_opy_
    }
  except Exception as error:
    logger.error(bstack11l1l11_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡣࡳࡧࡤࡸ࡮ࡴࡧࠡࡩࡨࡸࡤࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡤࡹࡥࡵࡶ࡬ࡲ࡬ࡹࠠࡧࡱࡵࠤ࡙࡫ࡳࡵࡊࡸࡦ࠿ࠦࠠࡼࡿࠥẈ").format(str(error)))
    return {}
def bstack111l1ll11l1_opy_(array, bstack111l11l11ll_opy_, bstack111l111llll_opy_):
  result = {}
  for o in array:
    key = o[bstack111l11l11ll_opy_]
    result[key] = o[bstack111l111llll_opy_]
  return result
def bstack111l1l1ll11_opy_(bstack1ll1ll1ll_opy_=bstack11l1l11_opy_ (u"ࠬ࠭ẉ")):
  bstack111l11l11l1_opy_ = bstack1l1l1l1ll1_opy_.on()
  bstack111l11l1ll1_opy_ = bstack11l11l11_opy_.on()
  bstack111l11ll11l_opy_ = percy.bstack1ll1111111_opy_()
  if bstack111l11ll11l_opy_ and not bstack111l11l1ll1_opy_ and not bstack111l11l11l1_opy_:
    return bstack1ll1ll1ll_opy_ not in [bstack11l1l11_opy_ (u"࠭ࡃࡃࡖࡖࡩࡸࡹࡩࡰࡰࡆࡶࡪࡧࡴࡦࡦࠪẊ"), bstack11l1l11_opy_ (u"ࠧࡍࡱࡪࡇࡷ࡫ࡡࡵࡧࡧࠫẋ")]
  elif bstack111l11l11l1_opy_ and not bstack111l11l1ll1_opy_:
    return bstack1ll1ll1ll_opy_ not in [bstack11l1l11_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩẌ"), bstack11l1l11_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫẍ"), bstack11l1l11_opy_ (u"ࠪࡐࡴ࡭ࡃࡳࡧࡤࡸࡪࡪࠧẎ")]
  return bstack111l11l11l1_opy_ or bstack111l11l1ll1_opy_ or bstack111l11ll11l_opy_
@bstack111ll1l1l1_opy_(class_method=False)
def bstack111l1ll1l11_opy_(bstack1ll1ll1ll_opy_, test=None):
  bstack111l11l1111_opy_ = bstack1l1l1l1ll1_opy_.on()
  if not bstack111l11l1111_opy_ or bstack1ll1ll1ll_opy_ not in [bstack11l1l11_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ẏ")] or test == None:
    return None
  return {
    bstack11l1l11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬẐ"): bstack111l11l1111_opy_ and bstack1llllllll1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬẑ"), None) == True and bstack1l1l1l1ll1_opy_.bstack11lll111_opy_(test[bstack11l1l11_opy_ (u"ࠧࡵࡣࡪࡷࠬẒ")])
  }
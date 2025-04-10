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
import datetime
import threading
from bstack_utils.helper import bstack11llll11ll1_opy_, bstack1ll111l11_opy_, get_host_info, bstack11ll111l11l_opy_, \
 bstack11l11ll1l1_opy_, bstack11111l111_opy_, bstack111ll11ll1_opy_, bstack11ll11lllll_opy_, bstack11l1ll11ll_opy_
import bstack_utils.accessibility as bstack1l11llll_opy_
from bstack_utils.bstack111llll1l1_opy_ import bstack11l1ll1ll_opy_
from bstack_utils.percy import bstack1l1l11l1l_opy_
from bstack_utils.config import Config
bstack11ll11ll_opy_ = Config.bstack1l11l1l1ll_opy_()
logger = logging.getLogger(__name__)
percy = bstack1l1l11l1l_opy_()
@bstack111ll11ll1_opy_(class_method=False)
def bstack1111lll1111_opy_(bs_config, bstack11lll11111_opy_):
  try:
    data = {
        bstack1ll1l1_opy_ (u"ࠬ࡬࡯ࡳ࡯ࡤࡸࠬỤ"): bstack1ll1l1_opy_ (u"࠭ࡪࡴࡱࡱࠫụ"),
        bstack1ll1l1_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡠࡰࡤࡱࡪ࠭Ủ"): bs_config.get(bstack1ll1l1_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭ủ"), bstack1ll1l1_opy_ (u"ࠩࠪỨ")),
        bstack1ll1l1_opy_ (u"ࠪࡲࡦࡳࡥࠨứ"): bs_config.get(bstack1ll1l1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧỪ"), os.path.basename(os.path.abspath(os.getcwd()))),
        bstack1ll1l1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨừ"): bs_config.get(bstack1ll1l1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨỬ")),
        bstack1ll1l1_opy_ (u"ࠧࡥࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠬử"): bs_config.get(bstack1ll1l1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡄࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫỮ"), bstack1ll1l1_opy_ (u"ࠩࠪữ")),
        bstack1ll1l1_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧỰ"): bstack11l1ll11ll_opy_(),
        bstack1ll1l1_opy_ (u"ࠫࡹࡧࡧࡴࠩự"): bstack11ll111l11l_opy_(bs_config),
        bstack1ll1l1_opy_ (u"ࠬ࡮࡯ࡴࡶࡢ࡭ࡳ࡬࡯ࠨỲ"): get_host_info(),
        bstack1ll1l1_opy_ (u"࠭ࡣࡪࡡ࡬ࡲ࡫ࡵࠧỳ"): bstack1ll111l11_opy_(),
        bstack1ll1l1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡲࡶࡰࡢ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧỴ"): os.environ.get(bstack1ll1l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡗࡌࡐࡉࡥࡒࡖࡐࡢࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠧỵ")),
        bstack1ll1l1_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࡡࡷࡩࡸࡺࡳࡠࡴࡨࡶࡺࡴࠧỶ"): os.environ.get(bstack1ll1l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡕࡉࡗ࡛ࡎࠨỷ"), False),
        bstack1ll1l1_opy_ (u"ࠫࡻ࡫ࡲࡴ࡫ࡲࡲࡤࡩ࡯࡯ࡶࡵࡳࡱ࠭Ỹ"): bstack11llll11ll1_opy_(),
        bstack1ll1l1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬỹ"): bstack1111l1ll1ll_opy_(),
        bstack1ll1l1_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡧࡩࡹࡧࡩ࡭ࡵࠪỺ"): bstack1111l1lllll_opy_(bstack11lll11111_opy_),
        bstack1ll1l1_opy_ (u"ࠧࡱࡴࡲࡨࡺࡩࡴࡠ࡯ࡤࡴࠬỻ"): bstack11l11ll1l_opy_(bs_config, bstack11lll11111_opy_.get(bstack1ll1l1_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡺࡹࡥࡥࠩỼ"), bstack1ll1l1_opy_ (u"ࠩࠪỽ"))),
        bstack1ll1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬỾ"): bstack11l11ll1l1_opy_(bs_config),
    }
    return data
  except Exception as error:
    logger.error(bstack1ll1l1_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡣࡳࡧࡤࡸ࡮ࡴࡧࠡࡲࡤࡽࡱࡵࡡࡥࠢࡩࡳࡷࠦࡔࡦࡵࡷࡌࡺࡨ࠺ࠡࠢࡾࢁࠧỿ").format(str(error)))
    return None
def bstack1111l1lllll_opy_(framework):
  return {
    bstack1ll1l1_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡏࡣࡰࡩࠬἀ"): framework.get(bstack1ll1l1_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫ࠧἁ"), bstack1ll1l1_opy_ (u"ࠧࡑࡻࡷࡩࡸࡺࠧἂ")),
    bstack1ll1l1_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮࡚ࡪࡸࡳࡪࡱࡱࠫἃ"): framework.get(bstack1ll1l1_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ἄ")),
    bstack1ll1l1_opy_ (u"ࠪࡷࡩࡱࡖࡦࡴࡶ࡭ࡴࡴࠧἅ"): framework.get(bstack1ll1l1_opy_ (u"ࠫࡸࡪ࡫ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩἆ")),
    bstack1ll1l1_opy_ (u"ࠬࡲࡡ࡯ࡩࡸࡥ࡬࡫ࠧἇ"): bstack1ll1l1_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭Ἀ"),
    bstack1ll1l1_opy_ (u"ࠧࡵࡧࡶࡸࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࠧἉ"): framework.get(bstack1ll1l1_opy_ (u"ࠨࡶࡨࡷࡹࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨἊ"))
  }
def bstack11l11ll1l_opy_(bs_config, framework):
  bstack1111l111l_opy_ = False
  bstack11ll111ll_opy_ = False
  bstack1111l1l1ll1_opy_ = False
  if bstack1ll1l1_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭Ἃ") in bs_config:
    bstack1111l1l1ll1_opy_ = True
  elif bstack1ll1l1_opy_ (u"ࠪࡥࡵࡶࠧἌ") in bs_config:
    bstack1111l111l_opy_ = True
  else:
    bstack11ll111ll_opy_ = True
  bstack1l11lll111_opy_ = {
    bstack1ll1l1_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫἍ"): bstack11l1ll1ll_opy_.bstack1111l1lll1l_opy_(bs_config, framework),
    bstack1ll1l1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬἎ"): bstack1l11llll_opy_.bstack1l1l1111l_opy_(bs_config),
    bstack1ll1l1_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬἏ"): bs_config.get(bstack1ll1l1_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭ἐ"), False),
    bstack1ll1l1_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵࡧࠪἑ"): bstack11ll111ll_opy_,
    bstack1ll1l1_opy_ (u"ࠩࡤࡴࡵࡥࡡࡶࡶࡲࡱࡦࡺࡥࠨἒ"): bstack1111l111l_opy_,
    bstack1ll1l1_opy_ (u"ࠪࡸࡺࡸࡢࡰࡵࡦࡥࡱ࡫ࠧἓ"): bstack1111l1l1ll1_opy_
  }
  return bstack1l11lll111_opy_
@bstack111ll11ll1_opy_(class_method=False)
def bstack1111l1ll1ll_opy_():
  try:
    bstack1111l1l1lll_opy_ = json.loads(os.getenv(bstack1ll1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬἔ"), bstack1ll1l1_opy_ (u"ࠬࢁࡽࠨἕ")))
    return {
        bstack1ll1l1_opy_ (u"࠭ࡳࡦࡶࡷ࡭ࡳ࡭ࡳࠨ἖"): bstack1111l1l1lll_opy_
    }
  except Exception as error:
    logger.error(bstack1ll1l1_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡦࡶࡪࡧࡴࡪࡰࡪࠤ࡬࡫ࡴࡠࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡠࡵࡨࡸࡹ࡯࡮ࡨࡵࠣࡪࡴࡸࠠࡕࡧࡶࡸࡍࡻࡢ࠻ࠢࠣࡿࢂࠨ἗").format(str(error)))
    return {}
def bstack1111ll1111l_opy_(array, bstack1111l1ll111_opy_, bstack1111ll11111_opy_):
  result = {}
  for o in array:
    key = o[bstack1111l1ll111_opy_]
    result[key] = o[bstack1111ll11111_opy_]
  return result
def bstack1111lll1l11_opy_(bstack1lllllll11_opy_=bstack1ll1l1_opy_ (u"ࠨࠩἘ")):
  bstack1111l1lll11_opy_ = bstack1l11llll_opy_.on()
  bstack1111l1llll1_opy_ = bstack11l1ll1ll_opy_.on()
  bstack1111l1ll11l_opy_ = percy.bstack1111l1l1_opy_()
  if bstack1111l1ll11l_opy_ and not bstack1111l1llll1_opy_ and not bstack1111l1lll11_opy_:
    return bstack1lllllll11_opy_ not in [bstack1ll1l1_opy_ (u"ࠩࡆࡆ࡙࡙ࡥࡴࡵ࡬ࡳࡳࡉࡲࡦࡣࡷࡩࡩ࠭Ἑ"), bstack1ll1l1_opy_ (u"ࠪࡐࡴ࡭ࡃࡳࡧࡤࡸࡪࡪࠧἚ")]
  elif bstack1111l1lll11_opy_ and not bstack1111l1llll1_opy_:
    return bstack1lllllll11_opy_ not in [bstack1ll1l1_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬἛ"), bstack1ll1l1_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧἜ"), bstack1ll1l1_opy_ (u"࠭ࡌࡰࡩࡆࡶࡪࡧࡴࡦࡦࠪἝ")]
  return bstack1111l1lll11_opy_ or bstack1111l1llll1_opy_ or bstack1111l1ll11l_opy_
@bstack111ll11ll1_opy_(class_method=False)
def bstack1111llll1l1_opy_(bstack1lllllll11_opy_, test=None):
  bstack1111l1ll1l1_opy_ = bstack1l11llll_opy_.on()
  if not bstack1111l1ll1l1_opy_ or bstack1lllllll11_opy_ not in [bstack1ll1l1_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩ἞")] or test == None:
    return None
  return {
    bstack1ll1l1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ἟"): bstack1111l1ll1l1_opy_ and bstack11111l111_opy_(threading.current_thread(), bstack1ll1l1_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨἠ"), None) == True and bstack1l11llll_opy_.bstack1ll11l1ll_opy_(test[bstack1ll1l1_opy_ (u"ࠪࡸࡦ࡭ࡳࠨἡ")])
  }
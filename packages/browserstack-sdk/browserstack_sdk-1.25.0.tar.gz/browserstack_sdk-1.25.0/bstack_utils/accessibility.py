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
import requests
import logging
import threading
from urllib.parse import urlparse
from bstack_utils.constants import bstack1l111l11l1l_opy_ as bstack1l111l1lll1_opy_, EVENTS
from bstack_utils.bstack11ll1lll1l_opy_ import bstack11ll1lll1l_opy_
from bstack_utils.helper import bstack1ll11ll11_opy_, bstack111l1l1l11_opy_, bstack1l1l1ll11l_opy_, bstack1l111l11l11_opy_, \
  bstack1l1111l1l1l_opy_, bstack1ll1lllll1_opy_, get_host_info, bstack1l111l111l1_opy_, bstack111ll11ll_opy_, bstack111ll1l1l1_opy_, bstack1llllllll1_opy_
from browserstack_sdk._version import __version__
from bstack_utils.bstack111ll1l11_opy_ import get_logger
from bstack_utils.bstack1l1ll1l11l_opy_ import bstack1lll1llll1l_opy_
from bstack_utils.constants import *
logger = get_logger(__name__)
bstack1l1ll1l11l_opy_ = bstack1lll1llll1l_opy_()
@bstack111ll1l1l1_opy_(class_method=False)
def _1l111l11ll1_opy_(driver, bstack1111llll11_opy_):
  response = {}
  try:
    caps = driver.capabilities
    response = {
        bstack11l1l11_opy_ (u"ࠬࡵࡳࡠࡰࡤࡱࡪ࠭ᓛ"): caps.get(bstack11l1l11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩࠬᓜ"), None),
        bstack11l1l11_opy_ (u"ࠧࡰࡵࡢࡺࡪࡸࡳࡪࡱࡱࠫᓝ"): bstack1111llll11_opy_.get(bstack11l1l11_opy_ (u"ࠨࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠫᓞ"), None),
        bstack11l1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡲࡦࡳࡥࠨᓟ"): caps.get(bstack11l1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨᓠ"), None),
        bstack11l1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ᓡ"): caps.get(bstack11l1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᓢ"), None)
    }
  except Exception as error:
    logger.debug(bstack11l1l11_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡬ࡥࡵࡥ࡫࡭ࡳ࡭ࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠢࡧࡩࡹࡧࡩ࡭ࡵࠣࡻ࡮ࡺࡨࠡࡧࡵࡶࡴࡸࠠ࠻ࠢࠪᓣ") + str(error))
  return response
def on():
    if os.environ.get(bstack11l1l11_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬᓤ"), None) is None or os.environ[bstack11l1l11_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ᓥ")] == bstack11l1l11_opy_ (u"ࠤࡱࡹࡱࡲࠢᓦ"):
        return False
    return True
def bstack1l1111l1l_opy_(config):
  return config.get(bstack11l1l11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᓧ"), False) or any([p.get(bstack11l1l11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᓨ"), False) == True for p in config.get(bstack11l1l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨᓩ"), [])])
def bstack1l1l1l1l_opy_(config, bstack1l1l1l111_opy_):
  try:
    if not bstack1l1l1ll11l_opy_(config):
      return False
    bstack1l111l1111l_opy_ = config.get(bstack11l1l11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᓪ"), False)
    if int(bstack1l1l1l111_opy_) < len(config.get(bstack11l1l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪᓫ"), [])) and config[bstack11l1l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᓬ")][bstack1l1l1l111_opy_]:
      bstack1l1111ll1l1_opy_ = config[bstack11l1l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬᓭ")][bstack1l1l1l111_opy_].get(bstack11l1l11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᓮ"), None)
    else:
      bstack1l1111ll1l1_opy_ = config.get(bstack11l1l11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᓯ"), None)
    if bstack1l1111ll1l1_opy_ != None:
      bstack1l111l1111l_opy_ = bstack1l1111ll1l1_opy_
    bstack1l1111l11ll_opy_ = os.getenv(bstack11l1l11_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪᓰ")) is not None and len(os.getenv(bstack11l1l11_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫᓱ"))) > 0 and os.getenv(bstack11l1l11_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬᓲ")) != bstack11l1l11_opy_ (u"ࠨࡰࡸࡰࡱ࠭ᓳ")
    return bstack1l111l1111l_opy_ and bstack1l1111l11ll_opy_
  except Exception as error:
    logger.debug(bstack11l1l11_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡸࡨࡶ࡮࡬ࡹࡪࡰࡪࠤࡹ࡮ࡥࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡺ࡭ࡹ࡮ࠠࡦࡴࡵࡳࡷࠦ࠺ࠡࠩᓴ") + str(error))
  return False
def bstack11lll111_opy_(test_tags):
  bstack1ll1ll1llll_opy_ = os.getenv(bstack11l1l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫᓵ"))
  if bstack1ll1ll1llll_opy_ is None:
    return True
  bstack1ll1ll1llll_opy_ = json.loads(bstack1ll1ll1llll_opy_)
  try:
    include_tags = bstack1ll1ll1llll_opy_[bstack11l1l11_opy_ (u"ࠫ࡮ࡴࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩᓶ")] if bstack11l1l11_opy_ (u"ࠬ࡯࡮ࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪᓷ") in bstack1ll1ll1llll_opy_ and isinstance(bstack1ll1ll1llll_opy_[bstack11l1l11_opy_ (u"࠭ࡩ࡯ࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫᓸ")], list) else []
    exclude_tags = bstack1ll1ll1llll_opy_[bstack11l1l11_opy_ (u"ࠧࡦࡺࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬᓹ")] if bstack11l1l11_opy_ (u"ࠨࡧࡻࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭ᓺ") in bstack1ll1ll1llll_opy_ and isinstance(bstack1ll1ll1llll_opy_[bstack11l1l11_opy_ (u"ࠩࡨࡼࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧᓻ")], list) else []
    excluded = any(tag in exclude_tags for tag in test_tags)
    included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
    return not excluded and included
  except Exception as error:
    logger.debug(bstack11l1l11_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡࡸࡤࡰ࡮ࡪࡡࡵ࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥࠡࡨࡲࡶࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡨࡥࡧࡱࡵࡩࠥࡹࡣࡢࡰࡱ࡭ࡳ࡭࠮ࠡࡇࡵࡶࡴࡸࠠ࠻ࠢࠥᓼ") + str(error))
  return False
def bstack1l111l1llll_opy_(config, bstack1l1111l1lll_opy_, bstack1l1111ll11l_opy_, bstack1l111l11lll_opy_):
  bstack1l111l11111_opy_ = bstack1l111l11l11_opy_(config)
  bstack1l1111llll1_opy_ = bstack1l1111l1l1l_opy_(config)
  if bstack1l111l11111_opy_ is None or bstack1l1111llll1_opy_ is None:
    logger.error(bstack11l1l11_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡣࡳࡧࡤࡸ࡮ࡴࡧࠡࡶࡨࡷࡹࠦࡲࡶࡰࠣࡪࡴࡸࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰ࠽ࠤࡒ࡯ࡳࡴ࡫ࡱ࡫ࠥࡧࡵࡵࡪࡨࡲࡹ࡯ࡣࡢࡶ࡬ࡳࡳࠦࡴࡰ࡭ࡨࡲࠬᓽ"))
    return [None, None]
  try:
    settings = json.loads(os.getenv(bstack11l1l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭ᓾ"), bstack11l1l11_opy_ (u"࠭ࡻࡾࠩᓿ")))
    data = {
        bstack11l1l11_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬᔀ"): config[bstack11l1l11_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭ᔁ")],
        bstack11l1l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬᔂ"): config.get(bstack11l1l11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ᔃ"), os.path.basename(os.getcwd())),
        bstack11l1l11_opy_ (u"ࠫࡸࡺࡡࡳࡶࡗ࡭ࡲ࡫ࠧᔄ"): bstack1ll11ll11_opy_(),
        bstack11l1l11_opy_ (u"ࠬࡪࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠪᔅ"): config.get(bstack11l1l11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡉ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠩᔆ"), bstack11l1l11_opy_ (u"ࠧࠨᔇ")),
        bstack11l1l11_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨᔈ"): {
            bstack11l1l11_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡓࡧ࡭ࡦࠩᔉ"): bstack1l1111l1lll_opy_,
            bstack11l1l11_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᔊ"): bstack1l1111ll11l_opy_,
            bstack11l1l11_opy_ (u"ࠫࡸࡪ࡫ࡗࡧࡵࡷ࡮ࡵ࡮ࠨᔋ"): __version__,
            bstack11l1l11_opy_ (u"ࠬࡲࡡ࡯ࡩࡸࡥ࡬࡫ࠧᔌ"): bstack11l1l11_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭ᔍ"),
            bstack11l1l11_opy_ (u"ࠧࡵࡧࡶࡸࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࠧᔎ"): bstack11l1l11_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯ࠪᔏ"),
            bstack11l1l11_opy_ (u"ࠩࡷࡩࡸࡺࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࡘࡨࡶࡸ࡯࡯࡯ࠩᔐ"): bstack1l111l11lll_opy_
        },
        bstack11l1l11_opy_ (u"ࠪࡷࡪࡺࡴࡪࡰࡪࡷࠬᔑ"): settings,
        bstack11l1l11_opy_ (u"ࠫࡻ࡫ࡲࡴ࡫ࡲࡲࡈࡵ࡮ࡵࡴࡲࡰࠬᔒ"): bstack1l111l111l1_opy_(),
        bstack11l1l11_opy_ (u"ࠬࡩࡩࡊࡰࡩࡳࠬᔓ"): bstack1ll1lllll1_opy_(),
        bstack11l1l11_opy_ (u"࠭ࡨࡰࡵࡷࡍࡳ࡬࡯ࠨᔔ"): get_host_info(),
        bstack11l1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩᔕ"): bstack1l1l1ll11l_opy_(config)
    }
    headers = {
        bstack11l1l11_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡗࡽࡵ࡫ࠧᔖ"): bstack11l1l11_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯࡫ࡵࡲࡲࠬᔗ"),
    }
    config = {
        bstack11l1l11_opy_ (u"ࠪࡥࡺࡺࡨࠨᔘ"): (bstack1l111l11111_opy_, bstack1l1111llll1_opy_),
        bstack11l1l11_opy_ (u"ࠫ࡭࡫ࡡࡥࡧࡵࡷࠬᔙ"): headers
    }
    response = bstack111ll11ll_opy_(bstack11l1l11_opy_ (u"ࠬࡖࡏࡔࡖࠪᔚ"), bstack1l111l1lll1_opy_ + bstack11l1l11_opy_ (u"࠭࠯ࡷ࠴࠲ࡸࡪࡹࡴࡠࡴࡸࡲࡸ࠭ᔛ"), data, config)
    bstack1l1111l1l11_opy_ = response.json()
    if bstack1l1111l1l11_opy_[bstack11l1l11_opy_ (u"ࠧࡴࡷࡦࡧࡪࡹࡳࠨᔜ")]:
      parsed = json.loads(os.getenv(bstack11l1l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩᔝ"), bstack11l1l11_opy_ (u"ࠩࡾࢁࠬᔞ")))
      parsed[bstack11l1l11_opy_ (u"ࠪࡷࡨࡧ࡮࡯ࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫᔟ")] = bstack1l1111l1l11_opy_[bstack11l1l11_opy_ (u"ࠫࡩࡧࡴࡢࠩᔠ")][bstack11l1l11_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᔡ")]
      os.environ[bstack11l1l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧᔢ")] = json.dumps(parsed)
      bstack11ll1lll1l_opy_.bstack1l1l1l1111_opy_(bstack1l1111l1l11_opy_[bstack11l1l11_opy_ (u"ࠧࡥࡣࡷࡥࠬᔣ")][bstack11l1l11_opy_ (u"ࠨࡵࡦࡶ࡮ࡶࡴࡴࠩᔤ")])
      bstack11ll1lll1l_opy_.bstack1l111ll1ll1_opy_(bstack1l1111l1l11_opy_[bstack11l1l11_opy_ (u"ࠩࡧࡥࡹࡧࠧᔥ")][bstack11l1l11_opy_ (u"ࠪࡧࡴࡳ࡭ࡢࡰࡧࡷࠬᔦ")])
      bstack11ll1lll1l_opy_.store()
      return bstack1l1111l1l11_opy_[bstack11l1l11_opy_ (u"ࠫࡩࡧࡴࡢࠩᔧ")][bstack11l1l11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽ࡙ࡵ࡫ࡦࡰࠪᔨ")], bstack1l1111l1l11_opy_[bstack11l1l11_opy_ (u"࠭ࡤࡢࡶࡤࠫᔩ")][bstack11l1l11_opy_ (u"ࠧࡪࡦࠪᔪ")]
    else:
      logger.error(bstack11l1l11_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡶࡺࡴ࡮ࡪࡰࡪࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࠺ࠡࠩᔫ") + bstack1l1111l1l11_opy_[bstack11l1l11_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᔬ")])
      if bstack1l1111l1l11_opy_[bstack11l1l11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᔭ")] == bstack11l1l11_opy_ (u"ࠫࡎࡴࡶࡢ࡮࡬ࡨࠥࡩ࡯࡯ࡨ࡬࡫ࡺࡸࡡࡵ࡫ࡲࡲࠥࡶࡡࡴࡵࡨࡨ࠳࠭ᔮ"):
        for bstack1l111ll1111_opy_ in bstack1l1111l1l11_opy_[bstack11l1l11_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࡷࠬᔯ")]:
          logger.error(bstack1l111ll1111_opy_[bstack11l1l11_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᔰ")])
      return None, None
  except Exception as error:
    logger.error(bstack11l1l11_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡦࡶࡪࡧࡴࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡵࡹࡳࠦࡦࡰࡴࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡀࠠࠣᔱ") +  str(error))
    return None, None
def bstack1l111l1l1ll_opy_():
  if os.getenv(bstack11l1l11_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ᔲ")) is None:
    return {
        bstack11l1l11_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩᔳ"): bstack11l1l11_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩᔴ"),
        bstack11l1l11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᔵ"): bstack11l1l11_opy_ (u"ࠬࡈࡵࡪ࡮ࡧࠤࡨࡸࡥࡢࡶ࡬ࡳࡳࠦࡨࡢࡦࠣࡪࡦ࡯࡬ࡦࡦ࠱ࠫᔶ")
    }
  data = {bstack11l1l11_opy_ (u"࠭ࡥ࡯ࡦࡗ࡭ࡲ࡫ࠧᔷ"): bstack1ll11ll11_opy_()}
  headers = {
      bstack11l1l11_opy_ (u"ࠧࡂࡷࡷ࡬ࡴࡸࡩࡻࡣࡷ࡭ࡴࡴࠧᔸ"): bstack11l1l11_opy_ (u"ࠨࡄࡨࡥࡷ࡫ࡲࠡࠩᔹ") + os.getenv(bstack11l1l11_opy_ (u"ࠤࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠢᔺ")),
      bstack11l1l11_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱࡙ࡿࡰࡦࠩᔻ"): bstack11l1l11_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧᔼ")
  }
  response = bstack111ll11ll_opy_(bstack11l1l11_opy_ (u"ࠬࡖࡕࡕࠩᔽ"), bstack1l111l1lll1_opy_ + bstack11l1l11_opy_ (u"࠭࠯ࡵࡧࡶࡸࡤࡸࡵ࡯ࡵ࠲ࡷࡹࡵࡰࠨᔾ"), data, { bstack11l1l11_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡳࠨᔿ"): headers })
  try:
    if response.status_code == 200:
      logger.info(bstack11l1l11_opy_ (u"ࠣࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤ࡙࡫ࡳࡵࠢࡕࡹࡳࠦ࡭ࡢࡴ࡮ࡩࡩࠦࡡࡴࠢࡦࡳࡲࡶ࡬ࡦࡶࡨࡨࠥࡧࡴࠡࠤᕀ") + bstack111l1l1l11_opy_().isoformat() + bstack11l1l11_opy_ (u"ࠩ࡝ࠫᕁ"))
      return {bstack11l1l11_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪᕂ"): bstack11l1l11_opy_ (u"ࠫࡸࡻࡣࡤࡧࡶࡷࠬᕃ"), bstack11l1l11_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᕄ"): bstack11l1l11_opy_ (u"࠭ࠧᕅ")}
    else:
      response.raise_for_status()
  except requests.RequestException as error:
    logger.error(bstack11l1l11_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡰࡥࡷࡱࡩ࡯ࡩࠣࡧࡴࡳࡰ࡭ࡧࡷ࡭ࡴࡴࠠࡰࡨࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡔࡦࡵࡷࠤࡗࡻ࡮࠻ࠢࠥᕆ") + str(error))
    return {
        bstack11l1l11_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨᕇ"): bstack11l1l11_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨᕈ"),
        bstack11l1l11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᕉ"): str(error)
    }
def bstack1l111l1l111_opy_(bstack1l1111l1ll1_opy_):
    return re.match(bstack11l1l11_opy_ (u"ࡶࠬࡤ࡜ࡥ࠭ࠫࡠ࠳ࡢࡤࠬࠫࡂࠨࠬᕊ"), bstack1l1111l1ll1_opy_.strip()) is not None
def bstack111l1111l_opy_(caps, options, desired_capabilities={}):
    try:
        if options:
          bstack1l1111ll1ll_opy_ = options.to_capabilities()
        elif desired_capabilities:
          bstack1l1111ll1ll_opy_ = desired_capabilities
        else:
          bstack1l1111ll1ll_opy_ = {}
        bstack1l111l111ll_opy_ = (bstack1l1111ll1ll_opy_.get(bstack11l1l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡎࡢ࡯ࡨࠫᕋ"), bstack11l1l11_opy_ (u"࠭ࠧᕌ")).lower() or caps.get(bstack11l1l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪ࠭ᕍ"), bstack11l1l11_opy_ (u"ࠨࠩᕎ")).lower())
        if bstack1l111l111ll_opy_ == bstack11l1l11_opy_ (u"ࠩ࡬ࡳࡸ࠭ᕏ"):
            return True
        if bstack1l111l111ll_opy_ == bstack11l1l11_opy_ (u"ࠪࡥࡳࡪࡲࡰ࡫ࡧࠫᕐ"):
            bstack1l111l1l1l1_opy_ = str(float(caps.get(bstack11l1l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᕑ")) or bstack1l1111ll1ll_opy_.get(bstack11l1l11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᕒ"), {}).get(bstack11l1l11_opy_ (u"࠭࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩᕓ"),bstack11l1l11_opy_ (u"ࠧࠨᕔ"))))
            if bstack1l111l111ll_opy_ == bstack11l1l11_opy_ (u"ࠨࡣࡱࡨࡷࡵࡩࡥࠩᕕ") and int(bstack1l111l1l1l1_opy_.split(bstack11l1l11_opy_ (u"ࠩ࠱ࠫᕖ"))[0]) < float(bstack1l111l1ll1l_opy_):
                logger.warning(str(bstack1l1111ll111_opy_))
                return False
            return True
        bstack1ll1l111lll_opy_ = caps.get(bstack11l1l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᕗ"), {}).get(bstack11l1l11_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨᕘ"), caps.get(bstack11l1l11_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࠬᕙ"), bstack11l1l11_opy_ (u"࠭ࠧᕚ")))
        if bstack1ll1l111lll_opy_:
            logger.warn(bstack11l1l11_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡵࡹࡳࠦ࡯࡯࡮ࡼࠤࡴࡴࠠࡅࡧࡶ࡯ࡹࡵࡰࠡࡤࡵࡳࡼࡹࡥࡳࡵ࠱ࠦᕛ"))
            return False
        browser = caps.get(bstack11l1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ᕜ"), bstack11l1l11_opy_ (u"ࠩࠪᕝ")).lower() or bstack1l1111ll1ll_opy_.get(bstack11l1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨᕞ"), bstack11l1l11_opy_ (u"ࠫࠬᕟ")).lower()
        if browser != bstack11l1l11_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࠬᕠ"):
            logger.warning(bstack11l1l11_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡴࡸࡲࠥࡵ࡮࡭ࡻࠣࡳࡳࠦࡃࡩࡴࡲࡱࡪࠦࡢࡳࡱࡺࡷࡪࡸࡳ࠯ࠤᕡ"))
            return False
        browser_version = caps.get(bstack11l1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨᕢ")) or caps.get(bstack11l1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪᕣ")) or bstack1l1111ll1ll_opy_.get(bstack11l1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᕤ")) or bstack1l1111ll1ll_opy_.get(bstack11l1l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᕥ"), {}).get(bstack11l1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬᕦ")) or bstack1l1111ll1ll_opy_.get(bstack11l1l11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᕧ"), {}).get(bstack11l1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᕨ"))
        if browser_version and browser_version != bstack11l1l11_opy_ (u"ࠧ࡭ࡣࡷࡩࡸࡺࠧᕩ") and int(browser_version.split(bstack11l1l11_opy_ (u"ࠨ࠰ࠪᕪ"))[0]) <= 98:
            logger.warning(bstack11l1l11_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡷࡻ࡮ࠡࡱࡱࡰࡾࠦ࡯࡯ࠢࡆ࡬ࡷࡵ࡭ࡦࠢࡥࡶࡴࡽࡳࡦࡴࠣࡺࡪࡸࡳࡪࡱࡱࠤ࡬ࡸࡥࡢࡶࡨࡶࠥࡺࡨࡢࡰࠣ࠽࠽࠴ࠢᕫ"))
            return False
        if not options:
            bstack1ll1lll1l11_opy_ = caps.get(bstack11l1l11_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᕬ")) or bstack1l1111ll1ll_opy_.get(bstack11l1l11_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᕭ"), {})
            if bstack11l1l11_opy_ (u"ࠬ࠳࠭ࡩࡧࡤࡨࡱ࡫ࡳࡴࠩᕮ") in bstack1ll1lll1l11_opy_.get(bstack11l1l11_opy_ (u"࠭ࡡࡳࡩࡶࠫᕯ"), []):
                logger.warn(bstack11l1l11_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡱࡳࡹࠦࡲࡶࡰࠣࡳࡳࠦ࡬ࡦࡩࡤࡧࡾࠦࡨࡦࡣࡧࡰࡪࡹࡳࠡ࡯ࡲࡨࡪ࠴ࠠࡔࡹ࡬ࡸࡨ࡮ࠠࡵࡱࠣࡲࡪࡽࠠࡩࡧࡤࡨࡱ࡫ࡳࡴࠢࡰࡳࡩ࡫ࠠࡰࡴࠣࡥࡻࡵࡩࡥࠢࡸࡷ࡮ࡴࡧࠡࡪࡨࡥࡩࡲࡥࡴࡵࠣࡱࡴࡪࡥ࠯ࠤᕰ"))
                return False
        return True
    except Exception as error:
        logger.debug(bstack11l1l11_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡷࡣ࡯࡭ࡩࡧࡴࡦࠢࡤ࠵࠶ࡿࠠࡴࡷࡳࡴࡴࡸࡴࠡ࠼ࠥᕱ") + str(error))
        return False
def set_capabilities(caps, config):
  try:
    bstack1lll1ll1l11_opy_ = config.get(bstack11l1l11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩᕲ"), {})
    bstack1lll1ll1l11_opy_[bstack11l1l11_opy_ (u"ࠪࡥࡺࡺࡨࡕࡱ࡮ࡩࡳ࠭ᕳ")] = os.getenv(bstack11l1l11_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩᕴ"))
    bstack1l1111lll1l_opy_ = json.loads(os.getenv(bstack11l1l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭ᕵ"), bstack11l1l11_opy_ (u"࠭ࡻࡾࠩᕶ"))).get(bstack11l1l11_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨᕷ"))
    caps[bstack11l1l11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᕸ")] = True
    if not config[bstack11l1l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡑࡴࡲࡨࡺࡩࡴࡎࡣࡳࠫᕹ")].get(bstack11l1l11_opy_ (u"ࠥࡥࡵࡶ࡟ࡢࡷࡷࡳࡲࡧࡴࡦࠤᕺ")):
      if bstack11l1l11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᕻ") in caps:
        caps[bstack11l1l11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᕼ")][bstack11l1l11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ᕽ")] = bstack1lll1ll1l11_opy_
        caps[bstack11l1l11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᕾ")][bstack11l1l11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨᕿ")][bstack11l1l11_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᖀ")] = bstack1l1111lll1l_opy_
      else:
        caps[bstack11l1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩᖁ")] = bstack1lll1ll1l11_opy_
        caps[bstack11l1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪᖂ")][bstack11l1l11_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᖃ")] = bstack1l1111lll1l_opy_
  except Exception as error:
    logger.debug(bstack11l1l11_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷ࠳ࠦࡅࡳࡴࡲࡶ࠿ࠦࠢᖄ") +  str(error))
def bstack1l111l11l1_opy_(driver, bstack1l1111lll11_opy_):
  try:
    setattr(driver, bstack11l1l11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡁ࠲࠳ࡼࡗ࡭ࡵࡵ࡭ࡦࡖࡧࡦࡴࠧᖅ"), True)
    session = driver.session_id
    if session:
      bstack1l111l1l11l_opy_ = True
      current_url = driver.current_url
      try:
        url = urlparse(current_url)
      except Exception as e:
        bstack1l111l1l11l_opy_ = False
      bstack1l111l1l11l_opy_ = url.scheme in [bstack11l1l11_opy_ (u"ࠣࡪࡷࡸࡵࠨᖆ"), bstack11l1l11_opy_ (u"ࠤ࡫ࡸࡹࡶࡳࠣᖇ")]
      if bstack1l111l1l11l_opy_:
        if bstack1l1111lll11_opy_:
          logger.info(bstack11l1l11_opy_ (u"ࠥࡗࡪࡺࡵࡱࠢࡩࡳࡷࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡴࡦࡵࡷ࡭ࡳ࡭ࠠࡩࡣࡶࠤࡸࡺࡡࡳࡶࡨࡨ࠳ࠦࡁࡶࡶࡲࡱࡦࡺࡥࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨࠤࡪࡾࡥࡤࡷࡷ࡭ࡴࡴࠠࡸ࡫࡯ࡰࠥࡨࡥࡨ࡫ࡱࠤࡲࡵ࡭ࡦࡰࡷࡥࡷ࡯࡬ࡺ࠰ࠥᖈ"))
      return bstack1l1111lll11_opy_
  except Exception as e:
    logger.error(bstack11l1l11_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡷࡹࡧࡲࡵ࡫ࡱ࡫ࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡶࡧࡦࡴࠠࡧࡱࡵࠤࡹ࡮ࡩࡴࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩ࠿ࠦࠢᖉ") + str(e))
    return False
def bstack1ll11111l_opy_(driver, name, path):
  try:
    bstack1ll1l1lll1l_opy_ = {
        bstack11l1l11_opy_ (u"ࠬࡺࡨࡕࡧࡶࡸࡗࡻ࡮ࡖࡷ࡬ࡨࠬᖊ"): threading.current_thread().current_test_uuid,
        bstack11l1l11_opy_ (u"࠭ࡴࡩࡄࡸ࡭ࡱࡪࡕࡶ࡫ࡧࠫᖋ"): os.environ.get(bstack11l1l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬᖌ"), bstack11l1l11_opy_ (u"ࠨࠩᖍ")),
        bstack11l1l11_opy_ (u"ࠩࡷ࡬ࡏࡽࡴࡕࡱ࡮ࡩࡳ࠭ᖎ"): os.environ.get(bstack11l1l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧᖏ"), bstack11l1l11_opy_ (u"ࠫࠬᖐ"))
    }
    bstack1ll1ll1l1l1_opy_ = bstack1l1ll1l11l_opy_.bstack1ll1ll1lll1_opy_(EVENTS.bstack1l111l1l11_opy_.value)
    logger.debug(bstack11l1l11_opy_ (u"ࠬࡖࡥࡳࡨࡲࡶࡲ࡯࡮ࡨࠢࡶࡧࡦࡴࠠࡣࡧࡩࡳࡷ࡫ࠠࡴࡣࡹ࡭ࡳ࡭ࠠࡳࡧࡶࡹࡱࡺࡳࠨᖑ"))
    try:
      if (bstack1llllllll1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"࠭ࡩࡴࡃࡳࡴࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭ᖒ"), None) and bstack1llllllll1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"ࠧࡢࡲࡳࡅ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩᖓ"), None)):
        scripts = {bstack11l1l11_opy_ (u"ࠨࡵࡦࡥࡳ࠭ᖔ"): bstack11ll1lll1l_opy_.perform_scan}
        bstack1l111ll111l_opy_ = json.loads(scripts[bstack11l1l11_opy_ (u"ࠤࡶࡧࡦࡴࠢᖕ")].replace(bstack11l1l11_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࠨᖖ"), bstack11l1l11_opy_ (u"ࠦࠧᖗ")))
        bstack1l111ll111l_opy_[bstack11l1l11_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨᖘ")][bstack11l1l11_opy_ (u"࠭࡭ࡦࡶ࡫ࡳࡩ࠭ᖙ")] = None
        scripts[bstack11l1l11_opy_ (u"ࠢࡴࡥࡤࡲࠧᖚ")] = bstack11l1l11_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࠦᖛ") + json.dumps(bstack1l111ll111l_opy_)
        bstack11ll1lll1l_opy_.bstack1l1l1l1111_opy_(scripts)
        bstack11ll1lll1l_opy_.store()
        logger.debug(driver.execute_script(bstack11ll1lll1l_opy_.perform_scan))
      else:
        logger.debug(driver.execute_async_script(bstack11ll1lll1l_opy_.perform_scan, {bstack11l1l11_opy_ (u"ࠤࡰࡩࡹ࡮࡯ࡥࠤᖜ"): name}))
      bstack1l1ll1l11l_opy_.end(EVENTS.bstack1l111l1l11_opy_.value, bstack1ll1ll1l1l1_opy_ + bstack11l1l11_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥᖝ"), bstack1ll1ll1l1l1_opy_ + bstack11l1l11_opy_ (u"ࠦ࠿࡫࡮ࡥࠤᖞ"), True, None)
    except Exception as error:
      bstack1l1ll1l11l_opy_.end(EVENTS.bstack1l111l1l11_opy_.value, bstack1ll1ll1l1l1_opy_ + bstack11l1l11_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧᖟ"), bstack1ll1ll1l1l1_opy_ + bstack11l1l11_opy_ (u"ࠨ࠺ࡦࡰࡧࠦᖠ"), False, str(error))
    bstack1ll1ll1l1l1_opy_ = bstack1l1ll1l11l_opy_.bstack1l1111lllll_opy_(EVENTS.bstack1ll1l1l11ll_opy_.value)
    bstack1l1ll1l11l_opy_.mark(bstack1ll1ll1l1l1_opy_ + bstack11l1l11_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢᖡ"))
    try:
      if (bstack1llllllll1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"ࠨ࡫ࡶࡅࡵࡶࡁ࠲࠳ࡼࡘࡪࡹࡴࠨᖢ"), None) and bstack1llllllll1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"ࠩࡤࡴࡵࡇ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫᖣ"), None)):
        scripts = {bstack11l1l11_opy_ (u"ࠪࡷࡨࡧ࡮ࠨᖤ"): bstack11ll1lll1l_opy_.perform_scan}
        bstack1l111ll111l_opy_ = json.loads(scripts[bstack11l1l11_opy_ (u"ࠦࡸࡩࡡ࡯ࠤᖥ")].replace(bstack11l1l11_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࠣᖦ"), bstack11l1l11_opy_ (u"ࠨࠢᖧ")))
        bstack1l111ll111l_opy_[bstack11l1l11_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪᖨ")][bstack11l1l11_opy_ (u"ࠨ࡯ࡨࡸ࡭ࡵࡤࠨᖩ")] = None
        scripts[bstack11l1l11_opy_ (u"ࠤࡶࡧࡦࡴࠢᖪ")] = bstack11l1l11_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࠨᖫ") + json.dumps(bstack1l111ll111l_opy_)
        bstack11ll1lll1l_opy_.bstack1l1l1l1111_opy_(scripts)
        bstack11ll1lll1l_opy_.store()
        logger.debug(driver.execute_script(bstack11ll1lll1l_opy_.perform_scan))
      else:
        logger.debug(driver.execute_async_script(bstack11ll1lll1l_opy_.bstack1l111ll11l1_opy_, bstack1ll1l1lll1l_opy_))
      bstack1l1ll1l11l_opy_.end(bstack1ll1ll1l1l1_opy_, bstack1ll1ll1l1l1_opy_ + bstack11l1l11_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦᖬ"), bstack1ll1ll1l1l1_opy_ + bstack11l1l11_opy_ (u"ࠧࡀࡥ࡯ࡦࠥᖭ"),True, None)
    except Exception as error:
      bstack1l1ll1l11l_opy_.end(bstack1ll1ll1l1l1_opy_, bstack1ll1ll1l1l1_opy_ + bstack11l1l11_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨᖮ"), bstack1ll1ll1l1l1_opy_ + bstack11l1l11_opy_ (u"ࠢ࠻ࡧࡱࡨࠧᖯ"),False, str(error))
    logger.info(bstack11l1l11_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡶࡨࡷࡹ࡯࡮ࡨࠢࡩࡳࡷࠦࡴࡩ࡫ࡶࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫ࠠࡩࡣࡶࠤࡪࡴࡤࡦࡦ࠱ࠦᖰ"))
  except Exception as bstack1ll1l111l11_opy_:
    logger.error(bstack11l1l11_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡵࡩࡸࡻ࡬ࡵࡵࠣࡧࡴࡻ࡬ࡥࠢࡱࡳࡹࠦࡢࡦࠢࡳࡶࡴࡩࡥࡴࡵࡨࡨࠥ࡬࡯ࡳࠢࡷ࡬ࡪࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦ࠼ࠣࠦᖱ") + str(path) + bstack11l1l11_opy_ (u"ࠥࠤࡊࡸࡲࡰࡴࠣ࠾ࠧᖲ") + str(bstack1ll1l111l11_opy_))
def bstack1l111l1ll11_opy_(driver):
    caps = driver.capabilities
    if caps.get(bstack11l1l11_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧࠥᖳ")) and str(caps.get(bstack11l1l11_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡎࡢ࡯ࡨࠦᖴ"))).lower() == bstack11l1l11_opy_ (u"ࠨࡡ࡯ࡦࡵࡳ࡮ࡪࠢᖵ"):
        bstack1l111l1l1l1_opy_ = caps.get(bstack11l1l11_opy_ (u"ࠢࡢࡲࡳ࡭ࡺࡳ࠺ࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠤᖶ")) or caps.get(bstack11l1l11_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠥᖷ"))
        if bstack1l111l1l1l1_opy_ and int(str(bstack1l111l1l1l1_opy_)) < bstack1l111l1ll1l_opy_:
            return False
    return True
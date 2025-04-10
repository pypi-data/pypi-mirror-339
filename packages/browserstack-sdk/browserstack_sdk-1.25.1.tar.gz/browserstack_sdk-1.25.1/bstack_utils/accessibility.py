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
import requests
import logging
import threading
from urllib.parse import urlparse
from bstack_utils.constants import bstack11lllll1lll_opy_ as bstack11llll11l11_opy_, EVENTS
from bstack_utils.bstack1ll1l11l1l_opy_ import bstack1ll1l11l1l_opy_
from bstack_utils.helper import bstack11l1ll11ll_opy_, bstack111l1l1ll1_opy_, bstack11l11ll1l1_opy_, bstack11lllll11l1_opy_, \
  bstack11lllll1l1l_opy_, bstack1ll111l11_opy_, get_host_info, bstack11llll11ll1_opy_, bstack11l1lll1ll_opy_, bstack111ll11ll1_opy_, bstack11111l111_opy_
from browserstack_sdk._version import __version__
from bstack_utils.bstack1l1ll1111l_opy_ import get_logger
from bstack_utils.bstack1l111l1111_opy_ import bstack1lll111l11l_opy_
from bstack_utils.constants import *
logger = get_logger(__name__)
bstack1l111l1111_opy_ = bstack1lll111l11l_opy_()
@bstack111ll11ll1_opy_(class_method=False)
def _11llll111ll_opy_(driver, bstack111l111ll1_opy_):
  response = {}
  try:
    caps = driver.capabilities
    response = {
        bstack1ll1l1_opy_ (u"ࠪࡳࡸࡥ࡮ࡢ࡯ࡨࠫᕐ"): caps.get(bstack1ll1l1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧࠪᕑ"), None),
        bstack1ll1l1_opy_ (u"ࠬࡵࡳࡠࡸࡨࡶࡸ࡯࡯࡯ࠩᕒ"): bstack111l111ll1_opy_.get(bstack1ll1l1_opy_ (u"࠭࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩᕓ"), None),
        bstack1ll1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡰࡤࡱࡪ࠭ᕔ"): caps.get(bstack1ll1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ᕕ"), None),
        bstack1ll1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠫᕖ"): caps.get(bstack1ll1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫᕗ"), None)
    }
  except Exception as error:
    logger.debug(bstack1ll1l1_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡪࡪࡺࡣࡩ࡫ࡱ࡫ࠥࡶ࡬ࡢࡶࡩࡳࡷࡳࠠࡥࡧࡷࡥ࡮ࡲࡳࠡࡹ࡬ࡸ࡭ࠦࡥࡳࡴࡲࡶࠥࡀࠠࠨᕘ") + str(error))
  return response
def on():
    if os.environ.get(bstack1ll1l1_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪᕙ"), None) is None or os.environ[bstack1ll1l1_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫᕚ")] == bstack1ll1l1_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧᕛ"):
        return False
    return True
def bstack1l1l1111l_opy_(config):
  return config.get(bstack1ll1l1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᕜ"), False) or any([p.get(bstack1ll1l1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᕝ"), False) == True for p in config.get(bstack1ll1l1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ᕞ"), [])])
def bstack111111ll1_opy_(config, bstack1lll1l111_opy_):
  try:
    if not bstack11l11ll1l1_opy_(config):
      return False
    bstack11llll11l1l_opy_ = config.get(bstack1ll1l1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᕟ"), False)
    if int(bstack1lll1l111_opy_) < len(config.get(bstack1ll1l1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨᕠ"), [])) and config[bstack1ll1l1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩᕡ")][bstack1lll1l111_opy_]:
      bstack11llllll11l_opy_ = config[bstack1ll1l1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪᕢ")][bstack1lll1l111_opy_].get(bstack1ll1l1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᕣ"), None)
    else:
      bstack11llllll11l_opy_ = config.get(bstack1ll1l1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᕤ"), None)
    if bstack11llllll11l_opy_ != None:
      bstack11llll11l1l_opy_ = bstack11llllll11l_opy_
    bstack11llllll111_opy_ = os.getenv(bstack1ll1l1_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨᕥ")) is not None and len(os.getenv(bstack1ll1l1_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩᕦ"))) > 0 and os.getenv(bstack1ll1l1_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪᕧ")) != bstack1ll1l1_opy_ (u"࠭࡮ࡶ࡮࡯ࠫᕨ")
    return bstack11llll11l1l_opy_ and bstack11llllll111_opy_
  except Exception as error:
    logger.debug(bstack1ll1l1_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡶࡦࡴ࡬ࡪࡾ࡯࡮ࡨࠢࡷ࡬ࡪࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡸ࡫ࡷ࡬ࠥ࡫ࡲࡳࡱࡵࠤ࠿ࠦࠧᕩ") + str(error))
  return False
def bstack1ll11l1ll_opy_(test_tags):
  bstack1ll1l111111_opy_ = os.getenv(bstack1ll1l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩᕪ"))
  if bstack1ll1l111111_opy_ is None:
    return True
  bstack1ll1l111111_opy_ = json.loads(bstack1ll1l111111_opy_)
  try:
    include_tags = bstack1ll1l111111_opy_[bstack1ll1l1_opy_ (u"ࠩ࡬ࡲࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧᕫ")] if bstack1ll1l1_opy_ (u"ࠪ࡭ࡳࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨᕬ") in bstack1ll1l111111_opy_ and isinstance(bstack1ll1l111111_opy_[bstack1ll1l1_opy_ (u"ࠫ࡮ࡴࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩᕭ")], list) else []
    exclude_tags = bstack1ll1l111111_opy_[bstack1ll1l1_opy_ (u"ࠬ࡫ࡸࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪᕮ")] if bstack1ll1l1_opy_ (u"࠭ࡥࡹࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫᕯ") in bstack1ll1l111111_opy_ and isinstance(bstack1ll1l111111_opy_[bstack1ll1l1_opy_ (u"ࠧࡦࡺࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬᕰ")], list) else []
    excluded = any(tag in exclude_tags for tag in test_tags)
    included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
    return not excluded and included
  except Exception as error:
    logger.debug(bstack1ll1l1_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦࡶࡢ࡮࡬ࡨࡦࡺࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࠦࡦࡰࡴࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡦࡪ࡬࡯ࡳࡧࠣࡷࡨࡧ࡮࡯࡫ࡱ࡫࠳ࠦࡅࡳࡴࡲࡶࠥࡀࠠࠣᕱ") + str(error))
  return False
def bstack11llllll1ll_opy_(config, bstack11lllll111l_opy_, bstack11lllll1ll1_opy_, bstack11llll1l111_opy_):
  bstack11llll11lll_opy_ = bstack11lllll11l1_opy_(config)
  bstack11llll1l1l1_opy_ = bstack11lllll1l1l_opy_(config)
  if bstack11llll11lll_opy_ is None or bstack11llll1l1l1_opy_ is None:
    logger.error(bstack1ll1l1_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡨࡸࡥࡢࡶ࡬ࡲ࡬ࠦࡴࡦࡵࡷࠤࡷࡻ࡮ࠡࡨࡲࡶࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮࠻ࠢࡐ࡭ࡸࡹࡩ࡯ࡩࠣࡥࡺࡺࡨࡦࡰࡷ࡭ࡨࡧࡴࡪࡱࡱࠤࡹࡵ࡫ࡦࡰࠪᕲ"))
    return [None, None]
  try:
    settings = json.loads(os.getenv(bstack1ll1l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫᕳ"), bstack1ll1l1_opy_ (u"ࠫࢀࢃࠧᕴ")))
    data = {
        bstack1ll1l1_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪᕵ"): config[bstack1ll1l1_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫᕶ")],
        bstack1ll1l1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪᕷ"): config.get(bstack1ll1l1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫᕸ"), os.path.basename(os.getcwd())),
        bstack1ll1l1_opy_ (u"ࠩࡶࡸࡦࡸࡴࡕ࡫ࡰࡩࠬᕹ"): bstack11l1ll11ll_opy_(),
        bstack1ll1l1_opy_ (u"ࠪࡨࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨᕺ"): config.get(bstack1ll1l1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡇࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠧᕻ"), bstack1ll1l1_opy_ (u"ࠬ࠭ᕼ")),
        bstack1ll1l1_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭ᕽ"): {
            bstack1ll1l1_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡑࡥࡲ࡫ࠧᕾ"): bstack11lllll111l_opy_,
            bstack1ll1l1_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮࡚ࡪࡸࡳࡪࡱࡱࠫᕿ"): bstack11lllll1ll1_opy_,
            bstack1ll1l1_opy_ (u"ࠩࡶࡨࡰ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᖀ"): __version__,
            bstack1ll1l1_opy_ (u"ࠪࡰࡦࡴࡧࡶࡣࡪࡩࠬᖁ"): bstack1ll1l1_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫᖂ"),
            bstack1ll1l1_opy_ (u"ࠬࡺࡥࡴࡶࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࠬᖃ"): bstack1ll1l1_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠨᖄ"),
            bstack1ll1l1_opy_ (u"ࠧࡵࡧࡶࡸࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࡖࡦࡴࡶ࡭ࡴࡴࠧᖅ"): bstack11llll1l111_opy_
        },
        bstack1ll1l1_opy_ (u"ࠨࡵࡨࡸࡹ࡯࡮ࡨࡵࠪᖆ"): settings,
        bstack1ll1l1_opy_ (u"ࠩࡹࡩࡷࡹࡩࡰࡰࡆࡳࡳࡺࡲࡰ࡮ࠪᖇ"): bstack11llll11ll1_opy_(),
        bstack1ll1l1_opy_ (u"ࠪࡧ࡮ࡏ࡮ࡧࡱࠪᖈ"): bstack1ll111l11_opy_(),
        bstack1ll1l1_opy_ (u"ࠫ࡭ࡵࡳࡵࡋࡱࡪࡴ࠭ᖉ"): get_host_info(),
        bstack1ll1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧᖊ"): bstack11l11ll1l1_opy_(config)
    }
    headers = {
        bstack1ll1l1_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡕࡻࡳࡩࠬᖋ"): bstack1ll1l1_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡳࡰࡰࠪᖌ"),
    }
    config = {
        bstack1ll1l1_opy_ (u"ࠨࡣࡸࡸ࡭࠭ᖍ"): (bstack11llll11lll_opy_, bstack11llll1l1l1_opy_),
        bstack1ll1l1_opy_ (u"ࠩ࡫ࡩࡦࡪࡥࡳࡵࠪᖎ"): headers
    }
    response = bstack11l1lll1ll_opy_(bstack1ll1l1_opy_ (u"ࠪࡔࡔ࡙ࡔࠨᖏ"), bstack11llll11l11_opy_ + bstack1ll1l1_opy_ (u"ࠫ࠴ࡼ࠲࠰ࡶࡨࡷࡹࡥࡲࡶࡰࡶࠫᖐ"), data, config)
    bstack11llll1ll1l_opy_ = response.json()
    if bstack11llll1ll1l_opy_[bstack1ll1l1_opy_ (u"ࠬࡹࡵࡤࡥࡨࡷࡸ࠭ᖑ")]:
      parsed = json.loads(os.getenv(bstack1ll1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧᖒ"), bstack1ll1l1_opy_ (u"ࠧࡼࡿࠪᖓ")))
      parsed[bstack1ll1l1_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩᖔ")] = bstack11llll1ll1l_opy_[bstack1ll1l1_opy_ (u"ࠩࡧࡥࡹࡧࠧᖕ")][bstack1ll1l1_opy_ (u"ࠪࡷࡨࡧ࡮࡯ࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫᖖ")]
      os.environ[bstack1ll1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬᖗ")] = json.dumps(parsed)
      bstack1ll1l11l1l_opy_.bstack11llllll1_opy_(bstack11llll1ll1l_opy_[bstack1ll1l1_opy_ (u"ࠬࡪࡡࡵࡣࠪᖘ")][bstack1ll1l1_opy_ (u"࠭ࡳࡤࡴ࡬ࡴࡹࡹࠧᖙ")])
      bstack1ll1l11l1l_opy_.bstack11llll1llll_opy_(bstack11llll1ll1l_opy_[bstack1ll1l1_opy_ (u"ࠧࡥࡣࡷࡥࠬᖚ")][bstack1ll1l1_opy_ (u"ࠨࡥࡲࡱࡲࡧ࡮ࡥࡵࠪᖛ")])
      bstack1ll1l11l1l_opy_.store()
      return bstack11llll1ll1l_opy_[bstack1ll1l1_opy_ (u"ࠩࡧࡥࡹࡧࠧᖜ")][bstack1ll1l1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡗࡳࡰ࡫࡮ࠨᖝ")], bstack11llll1ll1l_opy_[bstack1ll1l1_opy_ (u"ࠫࡩࡧࡴࡢࠩᖞ")][bstack1ll1l1_opy_ (u"ࠬ࡯ࡤࠨᖟ")]
    else:
      logger.error(bstack1ll1l1_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡴࡸࡲࡳ࡯࡮ࡨࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࠿ࠦࠧᖠ") + bstack11llll1ll1l_opy_[bstack1ll1l1_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᖡ")])
      if bstack11llll1ll1l_opy_[bstack1ll1l1_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᖢ")] == bstack1ll1l1_opy_ (u"ࠩࡌࡲࡻࡧ࡬ࡪࡦࠣࡧࡴࡴࡦࡪࡩࡸࡶࡦࡺࡩࡰࡰࠣࡴࡦࡹࡳࡦࡦ࠱ࠫᖣ"):
        for bstack11llll1l11l_opy_ in bstack11llll1ll1l_opy_[bstack1ll1l1_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࡵࠪᖤ")]:
          logger.error(bstack11llll1l11l_opy_[bstack1ll1l1_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᖥ")])
      return None, None
  except Exception as error:
    logger.error(bstack1ll1l1_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡤࡴࡨࡥࡹ࡯࡮ࡨࠢࡷࡩࡸࡺࠠࡳࡷࡱࠤ࡫ࡵࡲࠡࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱ࠾ࠥࠨᖦ") +  str(error))
    return None, None
def bstack11llll1111l_opy_():
  if os.getenv(bstack1ll1l1_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫᖧ")) is None:
    return {
        bstack1ll1l1_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧᖨ"): bstack1ll1l1_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧᖩ"),
        bstack1ll1l1_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᖪ"): bstack1ll1l1_opy_ (u"ࠪࡆࡺ࡯࡬ࡥࠢࡦࡶࡪࡧࡴࡪࡱࡱࠤ࡭ࡧࡤࠡࡨࡤ࡭ࡱ࡫ࡤ࠯ࠩᖫ")
    }
  data = {bstack1ll1l1_opy_ (u"ࠫࡪࡴࡤࡕ࡫ࡰࡩࠬᖬ"): bstack11l1ll11ll_opy_()}
  headers = {
      bstack1ll1l1_opy_ (u"ࠬࡇࡵࡵࡪࡲࡶ࡮ࢀࡡࡵ࡫ࡲࡲࠬᖭ"): bstack1ll1l1_opy_ (u"࠭ࡂࡦࡣࡵࡩࡷࠦࠧᖮ") + os.getenv(bstack1ll1l1_opy_ (u"ࠢࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠧᖯ")),
      bstack1ll1l1_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡗࡽࡵ࡫ࠧᖰ"): bstack1ll1l1_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯࡫ࡵࡲࡲࠬᖱ")
  }
  response = bstack11l1lll1ll_opy_(bstack1ll1l1_opy_ (u"ࠪࡔ࡚࡚ࠧᖲ"), bstack11llll11l11_opy_ + bstack1ll1l1_opy_ (u"ࠫ࠴ࡺࡥࡴࡶࡢࡶࡺࡴࡳ࠰ࡵࡷࡳࡵ࠭ᖳ"), data, { bstack1ll1l1_opy_ (u"ࠬ࡮ࡥࡢࡦࡨࡶࡸ࠭ᖴ"): headers })
  try:
    if response.status_code == 200:
      logger.info(bstack1ll1l1_opy_ (u"ࠨࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡗࡩࡸࡺࠠࡓࡷࡱࠤࡲࡧࡲ࡬ࡧࡧࠤࡦࡹࠠࡤࡱࡰࡴࡱ࡫ࡴࡦࡦࠣࡥࡹࠦࠢᖵ") + bstack111l1l1ll1_opy_().isoformat() + bstack1ll1l1_opy_ (u"࡛ࠧࠩᖶ"))
      return {bstack1ll1l1_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨᖷ"): bstack1ll1l1_opy_ (u"ࠩࡶࡹࡨࡩࡥࡴࡵࠪᖸ"), bstack1ll1l1_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᖹ"): bstack1ll1l1_opy_ (u"ࠫࠬᖺ")}
    else:
      response.raise_for_status()
  except requests.RequestException as error:
    logger.error(bstack1ll1l1_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠ࡮ࡣࡵ࡯࡮ࡴࡧࠡࡥࡲࡱࡵࡲࡥࡵ࡫ࡲࡲࠥࡵࡦࠡࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤ࡙࡫ࡳࡵࠢࡕࡹࡳࡀࠠࠣᖻ") + str(error))
    return {
        bstack1ll1l1_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ᖼ"): bstack1ll1l1_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ᖽ"),
        bstack1ll1l1_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᖾ"): str(error)
    }
def bstack11lllllll1l_opy_(bstack11llll11111_opy_):
    return re.match(bstack1ll1l1_opy_ (u"ࡴࠪࡢࡡࡪࠫࠩ࡞࠱ࡠࡩ࠱ࠩࡀࠦࠪᖿ"), bstack11llll11111_opy_.strip()) is not None
def bstack1l11ll1l11_opy_(caps, options, desired_capabilities={}):
    try:
        if options:
          bstack11lllllll11_opy_ = options.to_capabilities()
        elif desired_capabilities:
          bstack11lllllll11_opy_ = desired_capabilities
        else:
          bstack11lllllll11_opy_ = {}
        bstack11lll1lllll_opy_ = (bstack11lllllll11_opy_.get(bstack1ll1l1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠩᗀ"), bstack1ll1l1_opy_ (u"ࠫࠬᗁ")).lower() or caps.get(bstack1ll1l1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡎࡢ࡯ࡨࠫᗂ"), bstack1ll1l1_opy_ (u"࠭ࠧᗃ")).lower())
        if bstack11lll1lllll_opy_ == bstack1ll1l1_opy_ (u"ࠧࡪࡱࡶࠫᗄ"):
            return True
        if bstack11lll1lllll_opy_ == bstack1ll1l1_opy_ (u"ࠨࡣࡱࡨࡷࡵࡩࡥࠩᗅ"):
            bstack11llllll1l1_opy_ = str(float(caps.get(bstack1ll1l1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠫᗆ")) or bstack11lllllll11_opy_.get(bstack1ll1l1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᗇ"), {}).get(bstack1ll1l1_opy_ (u"ࠫࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠧᗈ"),bstack1ll1l1_opy_ (u"ࠬ࠭ᗉ"))))
            if bstack11lll1lllll_opy_ == bstack1ll1l1_opy_ (u"࠭ࡡ࡯ࡦࡵࡳ࡮ࡪࠧᗊ") and int(bstack11llllll1l1_opy_.split(bstack1ll1l1_opy_ (u"ࠧ࠯ࠩᗋ"))[0]) < float(bstack11lllll11ll_opy_):
                logger.warning(str(bstack11lllll1l11_opy_))
                return False
            return True
        bstack1ll1l1l11l1_opy_ = caps.get(bstack1ll1l1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᗌ"), {}).get(bstack1ll1l1_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪ࠭ᗍ"), caps.get(bstack1ll1l1_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࠪᗎ"), bstack1ll1l1_opy_ (u"ࠫࠬᗏ")))
        if bstack1ll1l1l11l1_opy_:
            logger.warn(bstack1ll1l1_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠࡳࡷࡱࠤࡴࡴ࡬ࡺࠢࡲࡲࠥࡊࡥࡴ࡭ࡷࡳࡵࠦࡢࡳࡱࡺࡷࡪࡸࡳ࠯ࠤᗐ"))
            return False
        browser = caps.get(bstack1ll1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫᗑ"), bstack1ll1l1_opy_ (u"ࠧࠨᗒ")).lower() or bstack11lllllll11_opy_.get(bstack1ll1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ᗓ"), bstack1ll1l1_opy_ (u"ࠩࠪᗔ")).lower()
        if browser != bstack1ll1l1_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪᗕ"):
            logger.warning(bstack1ll1l1_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦࡲࡶࡰࠣࡳࡳࡲࡹࠡࡱࡱࠤࡈ࡮ࡲࡰ࡯ࡨࠤࡧࡸ࡯ࡸࡵࡨࡶࡸ࠴ࠢᗖ"))
            return False
        browser_version = caps.get(bstack1ll1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᗗ")) or caps.get(bstack1ll1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᗘ")) or bstack11lllllll11_opy_.get(bstack1ll1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨᗙ")) or bstack11lllllll11_opy_.get(bstack1ll1l1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᗚ"), {}).get(bstack1ll1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᗛ")) or bstack11lllllll11_opy_.get(bstack1ll1l1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᗜ"), {}).get(bstack1ll1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ᗝ"))
        if browser_version and browser_version != bstack1ll1l1_opy_ (u"ࠬࡲࡡࡵࡧࡶࡸࠬᗞ") and int(browser_version.split(bstack1ll1l1_opy_ (u"࠭࠮ࠨᗟ"))[0]) <= 98:
            logger.warning(bstack1ll1l1_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡵࡹࡳࠦ࡯࡯࡮ࡼࠤࡴࡴࠠࡄࡪࡵࡳࡲ࡫ࠠࡣࡴࡲࡻࡸ࡫ࡲࠡࡸࡨࡶࡸ࡯࡯࡯ࠢࡪࡶࡪࡧࡴࡦࡴࠣࡸ࡭ࡧ࡮ࠡ࠻࠻࠲ࠧᗠ"))
            return False
        if not options:
            bstack1ll1ll11ll1_opy_ = caps.get(bstack1ll1l1_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᗡ")) or bstack11lllllll11_opy_.get(bstack1ll1l1_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᗢ"), {})
            if bstack1ll1l1_opy_ (u"ࠪ࠱࠲࡮ࡥࡢࡦ࡯ࡩࡸࡹࠧᗣ") in bstack1ll1ll11ll1_opy_.get(bstack1ll1l1_opy_ (u"ࠫࡦࡸࡧࡴࠩᗤ"), []):
                logger.warn(bstack1ll1l1_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠ࡯ࡱࡷࠤࡷࡻ࡮ࠡࡱࡱࠤࡱ࡫ࡧࡢࡥࡼࠤ࡭࡫ࡡࡥ࡮ࡨࡷࡸࠦ࡭ࡰࡦࡨ࠲࡙ࠥࡷࡪࡶࡦ࡬ࠥࡺ࡯ࠡࡰࡨࡻࠥ࡮ࡥࡢࡦ࡯ࡩࡸࡹࠠ࡮ࡱࡧࡩࠥࡵࡲࠡࡣࡹࡳ࡮ࡪࠠࡶࡵ࡬ࡲ࡬ࠦࡨࡦࡣࡧࡰࡪࡹࡳࠡ࡯ࡲࡨࡪ࠴ࠢᗥ"))
                return False
        return True
    except Exception as error:
        logger.debug(bstack1ll1l1_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡼࡡ࡭࡫ࡧࡥࡹ࡫ࠠࡢ࠳࠴ࡽࠥࡹࡵࡱࡲࡲࡶࡹࠦ࠺ࠣᗦ") + str(error))
        return False
def set_capabilities(caps, config):
  try:
    bstack1lll111ll1l_opy_ = config.get(bstack1ll1l1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧᗧ"), {})
    bstack1lll111ll1l_opy_[bstack1ll1l1_opy_ (u"ࠨࡣࡸࡸ࡭࡚࡯࡬ࡧࡱࠫᗨ")] = os.getenv(bstack1ll1l1_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧᗩ"))
    bstack11lllll1111_opy_ = json.loads(os.getenv(bstack1ll1l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫᗪ"), bstack1ll1l1_opy_ (u"ࠫࢀࢃࠧᗫ"))).get(bstack1ll1l1_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᗬ"))
    caps[bstack1ll1l1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᗭ")] = True
    if not config[bstack1ll1l1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡖࡲࡰࡦࡸࡧࡹࡓࡡࡱࠩᗮ")].get(bstack1ll1l1_opy_ (u"ࠣࡣࡳࡴࡤࡧࡵࡵࡱࡰࡥࡹ࡫ࠢᗯ")):
      if bstack1ll1l1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᗰ") in caps:
        caps[bstack1ll1l1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᗱ")][bstack1ll1l1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫᗲ")] = bstack1lll111ll1l_opy_
        caps[bstack1ll1l1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᗳ")][bstack1ll1l1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ᗴ")][bstack1ll1l1_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨᗵ")] = bstack11lllll1111_opy_
      else:
        caps[bstack1ll1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧᗶ")] = bstack1lll111ll1l_opy_
        caps[bstack1ll1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨᗷ")][bstack1ll1l1_opy_ (u"ࠪࡷࡨࡧ࡮࡯ࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫᗸ")] = bstack11lllll1111_opy_
  except Exception as error:
    logger.debug(bstack1ll1l1_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵ࠱ࠤࡊࡸࡲࡰࡴ࠽ࠤࠧᗹ") +  str(error))
def bstack11llll11_opy_(driver, bstack11lll1llll1_opy_):
  try:
    setattr(driver, bstack1ll1l1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡆ࠷࠱ࡺࡕ࡫ࡳࡺࡲࡤࡔࡥࡤࡲࠬᗺ"), True)
    session = driver.session_id
    if session:
      bstack11llll1ll11_opy_ = True
      current_url = driver.current_url
      try:
        url = urlparse(current_url)
      except Exception as e:
        bstack11llll1ll11_opy_ = False
      bstack11llll1ll11_opy_ = url.scheme in [bstack1ll1l1_opy_ (u"ࠨࡨࡵࡶࡳࠦᗻ"), bstack1ll1l1_opy_ (u"ࠢࡩࡶࡷࡴࡸࠨᗼ")]
      if bstack11llll1ll11_opy_:
        if bstack11lll1llll1_opy_:
          logger.info(bstack1ll1l1_opy_ (u"ࠣࡕࡨࡸࡺࡶࠠࡧࡱࡵࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡹ࡫ࡳࡵ࡫ࡱ࡫ࠥ࡮ࡡࡴࠢࡶࡸࡦࡸࡴࡦࡦ࠱ࠤࡆࡻࡴࡰ࡯ࡤࡸࡪࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦࠢࡨࡼࡪࡩࡵࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡦࡪ࡭ࡩ࡯ࠢࡰࡳࡲ࡫࡮ࡵࡣࡵ࡭ࡱࡿ࠮ࠣᗽ"))
      return bstack11lll1llll1_opy_
  except Exception as e:
    logger.error(bstack1ll1l1_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡵࡷࡥࡷࡺࡩ࡯ࡩࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡴࡥࡤࡲࠥ࡬࡯ࡳࠢࡷ࡬࡮ࡹࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧ࠽ࠤࠧᗾ") + str(e))
    return False
def bstack1111l1l11_opy_(driver, name, path):
  try:
    bstack1ll1ll1ll1l_opy_ = {
        bstack1ll1l1_opy_ (u"ࠪࡸ࡭࡚ࡥࡴࡶࡕࡹࡳ࡛ࡵࡪࡦࠪᗿ"): threading.current_thread().current_test_uuid,
        bstack1ll1l1_opy_ (u"ࠫࡹ࡮ࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠩᘀ"): os.environ.get(bstack1ll1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪᘁ"), bstack1ll1l1_opy_ (u"࠭ࠧᘂ")),
        bstack1ll1l1_opy_ (u"ࠧࡵࡪࡍࡻࡹ࡚࡯࡬ࡧࡱࠫᘃ"): os.environ.get(bstack1ll1l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬᘄ"), bstack1ll1l1_opy_ (u"ࠩࠪᘅ"))
    }
    bstack1ll1l1l111l_opy_ = bstack1l111l1111_opy_.bstack1ll1ll111ll_opy_(EVENTS.bstack1l11l11ll1_opy_.value)
    logger.debug(bstack1ll1l1_opy_ (u"ࠪࡔࡪࡸࡦࡰࡴࡰ࡭ࡳ࡭ࠠࡴࡥࡤࡲࠥࡨࡥࡧࡱࡵࡩࠥࡹࡡࡷ࡫ࡱ࡫ࠥࡸࡥࡴࡷ࡯ࡸࡸ࠭ᘆ"))
    try:
      if (bstack11111l111_opy_(threading.current_thread(), bstack1ll1l1_opy_ (u"ࠫ࡮ࡹࡁࡱࡲࡄ࠵࠶ࡿࡔࡦࡵࡷࠫᘇ"), None) and bstack11111l111_opy_(threading.current_thread(), bstack1ll1l1_opy_ (u"ࠬࡧࡰࡱࡃ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧᘈ"), None)):
        scripts = {bstack1ll1l1_opy_ (u"࠭ࡳࡤࡣࡱࠫᘉ"): bstack1ll1l11l1l_opy_.perform_scan}
        bstack11lll1lll1l_opy_ = json.loads(scripts[bstack1ll1l1_opy_ (u"ࠢࡴࡥࡤࡲࠧᘊ")].replace(bstack1ll1l1_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࠦᘋ"), bstack1ll1l1_opy_ (u"ࠤࠥᘌ")))
        bstack11lll1lll1l_opy_[bstack1ll1l1_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ᘍ")][bstack1ll1l1_opy_ (u"ࠫࡲ࡫ࡴࡩࡱࡧࠫᘎ")] = None
        scripts[bstack1ll1l1_opy_ (u"ࠧࡹࡣࡢࡰࠥᘏ")] = bstack1ll1l1_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࠤᘐ") + json.dumps(bstack11lll1lll1l_opy_)
        bstack1ll1l11l1l_opy_.bstack11llllll1_opy_(scripts)
        bstack1ll1l11l1l_opy_.store()
        logger.debug(driver.execute_script(bstack1ll1l11l1l_opy_.perform_scan))
      else:
        logger.debug(driver.execute_async_script(bstack1ll1l11l1l_opy_.perform_scan, {bstack1ll1l1_opy_ (u"ࠢ࡮ࡧࡷ࡬ࡴࡪࠢᘑ"): name}))
      bstack1l111l1111_opy_.end(EVENTS.bstack1l11l11ll1_opy_.value, bstack1ll1l1l111l_opy_ + bstack1ll1l1_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣᘒ"), bstack1ll1l1l111l_opy_ + bstack1ll1l1_opy_ (u"ࠤ࠽ࡩࡳࡪࠢᘓ"), True, None)
    except Exception as error:
      bstack1l111l1111_opy_.end(EVENTS.bstack1l11l11ll1_opy_.value, bstack1ll1l1l111l_opy_ + bstack1ll1l1_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥᘔ"), bstack1ll1l1l111l_opy_ + bstack1ll1l1_opy_ (u"ࠦ࠿࡫࡮ࡥࠤᘕ"), False, str(error))
    bstack1ll1l1l111l_opy_ = bstack1l111l1111_opy_.bstack11llll111l1_opy_(EVENTS.bstack1ll1l1ll1l1_opy_.value)
    bstack1l111l1111_opy_.mark(bstack1ll1l1l111l_opy_ + bstack1ll1l1_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧᘖ"))
    try:
      if (bstack11111l111_opy_(threading.current_thread(), bstack1ll1l1_opy_ (u"࠭ࡩࡴࡃࡳࡴࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭ᘗ"), None) and bstack11111l111_opy_(threading.current_thread(), bstack1ll1l1_opy_ (u"ࠧࡢࡲࡳࡅ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩᘘ"), None)):
        scripts = {bstack1ll1l1_opy_ (u"ࠨࡵࡦࡥࡳ࠭ᘙ"): bstack1ll1l11l1l_opy_.perform_scan}
        bstack11lll1lll1l_opy_ = json.loads(scripts[bstack1ll1l1_opy_ (u"ࠤࡶࡧࡦࡴࠢᘚ")].replace(bstack1ll1l1_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࠨᘛ"), bstack1ll1l1_opy_ (u"ࠦࠧᘜ")))
        bstack11lll1lll1l_opy_[bstack1ll1l1_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨᘝ")][bstack1ll1l1_opy_ (u"࠭࡭ࡦࡶ࡫ࡳࡩ࠭ᘞ")] = None
        scripts[bstack1ll1l1_opy_ (u"ࠢࡴࡥࡤࡲࠧᘟ")] = bstack1ll1l1_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࠦᘠ") + json.dumps(bstack11lll1lll1l_opy_)
        bstack1ll1l11l1l_opy_.bstack11llllll1_opy_(scripts)
        bstack1ll1l11l1l_opy_.store()
        logger.debug(driver.execute_script(bstack1ll1l11l1l_opy_.perform_scan))
      else:
        logger.debug(driver.execute_async_script(bstack1ll1l11l1l_opy_.bstack11llll1lll1_opy_, bstack1ll1ll1ll1l_opy_))
      bstack1l111l1111_opy_.end(bstack1ll1l1l111l_opy_, bstack1ll1l1l111l_opy_ + bstack1ll1l1_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᘡ"), bstack1ll1l1l111l_opy_ + bstack1ll1l1_opy_ (u"ࠥ࠾ࡪࡴࡤࠣᘢ"),True, None)
    except Exception as error:
      bstack1l111l1111_opy_.end(bstack1ll1l1l111l_opy_, bstack1ll1l1l111l_opy_ + bstack1ll1l1_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦᘣ"), bstack1ll1l1l111l_opy_ + bstack1ll1l1_opy_ (u"ࠧࡀࡥ࡯ࡦࠥᘤ"),False, str(error))
    logger.info(bstack1ll1l1_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡴࡦࡵࡷ࡭ࡳ࡭ࠠࡧࡱࡵࠤࡹ࡮ࡩࡴࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩࠥ࡮ࡡࡴࠢࡨࡲࡩ࡫ࡤ࠯ࠤᘥ"))
  except Exception as bstack1ll1l11l111_opy_:
    logger.error(bstack1ll1l1_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡳࡧࡶࡹࡱࡺࡳࠡࡥࡲࡹࡱࡪࠠ࡯ࡱࡷࠤࡧ࡫ࠠࡱࡴࡲࡧࡪࡹࡳࡦࡦࠣࡪࡴࡸࠠࡵࡪࡨࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫࠺ࠡࠤᘦ") + str(path) + bstack1ll1l1_opy_ (u"ࠣࠢࡈࡶࡷࡵࡲࠡ࠼ࠥᘧ") + str(bstack1ll1l11l111_opy_))
def bstack11llll1l1ll_opy_(driver):
    caps = driver.capabilities
    if caps.get(bstack1ll1l1_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠣᘨ")) and str(caps.get(bstack1ll1l1_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠤᘩ"))).lower() == bstack1ll1l1_opy_ (u"ࠦࡦࡴࡤࡳࡱ࡬ࡨࠧᘪ"):
        bstack11llllll1l1_opy_ = caps.get(bstack1ll1l1_opy_ (u"ࠧࡧࡰࡱ࡫ࡸࡱ࠿ࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠢᘫ")) or caps.get(bstack1ll1l1_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠣᘬ"))
        if bstack11llllll1l1_opy_ and int(str(bstack11llllll1l1_opy_)) < bstack11lllll11ll_opy_:
            return False
    return True
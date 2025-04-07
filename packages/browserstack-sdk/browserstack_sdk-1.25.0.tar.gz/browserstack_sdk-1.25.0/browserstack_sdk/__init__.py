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
import atexit
import signal
import yaml
import socket
import datetime
import string
import random
import collections.abc
import traceback
import copy
from concurrent.futures import ThreadPoolExecutor, TimeoutError
import json
from packaging import version
from browserstack.local import Local
from urllib.parse import urlparse
from dotenv import load_dotenv
from browserstack_sdk.bstack1lll111l11_opy_ import bstack111l1l111_opy_
from browserstack_sdk.bstack11l1l11111_opy_ import *
import time
import requests
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.measure import measure
def bstack1lll111111_opy_():
  global CONFIG
  headers = {
        bstack11l1l11_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩࡶ"): bstack11l1l11_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧࡷ"),
      }
  proxies = bstack1ll11lll1_opy_(CONFIG, bstack1ll111ll1_opy_)
  try:
    response = requests.get(bstack1ll111ll1_opy_, headers=headers, proxies=proxies, timeout=5)
    if response.json():
      bstack1lll1l111_opy_ = response.json()[bstack11l1l11_opy_ (u"ࠬ࡮ࡵࡣࡵࠪࡸ")]
      logger.debug(bstack11111111l_opy_.format(response.json()))
      return bstack1lll1l111_opy_
    else:
      logger.debug(bstack1ll111111_opy_.format(bstack11l1l11_opy_ (u"ࠨࡒࡦࡵࡳࡳࡳࡹࡥࠡࡌࡖࡓࡓࠦࡰࡢࡴࡶࡩࠥ࡫ࡲࡳࡱࡵࠤࠧࡹ")))
  except Exception as e:
    logger.debug(bstack1ll111111_opy_.format(e))
def bstack11l1111ll_opy_(hub_url):
  global CONFIG
  url = bstack11l1l11_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤࡺ")+  hub_url + bstack11l1l11_opy_ (u"ࠣ࠱ࡦ࡬ࡪࡩ࡫ࠣࡻ")
  headers = {
        bstack11l1l11_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨࡼ"): bstack11l1l11_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ࡽ"),
      }
  proxies = bstack1ll11lll1_opy_(CONFIG, url)
  try:
    start_time = time.perf_counter()
    requests.get(url, headers=headers, proxies=proxies, timeout=5)
    latency = time.perf_counter() - start_time
    logger.debug(bstack1l1l1l111l_opy_.format(hub_url, latency))
    return dict(hub_url=hub_url, latency=latency)
  except Exception as e:
    logger.debug(bstack1ll1lll1_opy_.format(hub_url, e))
@measure(event_name=EVENTS.bstack1l11111l_opy_, stage=STAGE.bstack1l1ll1lll_opy_)
def bstack11l1lll111_opy_():
  try:
    global bstack1111l1l1_opy_
    bstack1lll1l111_opy_ = bstack1lll111111_opy_()
    bstack1l11ll1lll_opy_ = []
    results = []
    for bstack1l11ll111l_opy_ in bstack1lll1l111_opy_:
      bstack1l11ll1lll_opy_.append(bstack1l111lll11_opy_(target=bstack11l1111ll_opy_,args=(bstack1l11ll111l_opy_,)))
    for t in bstack1l11ll1lll_opy_:
      t.start()
    for t in bstack1l11ll1lll_opy_:
      results.append(t.join())
    bstack11llll1ll1_opy_ = {}
    for item in results:
      hub_url = item[bstack11l1l11_opy_ (u"ࠫ࡭ࡻࡢࡠࡷࡵࡰࠬࡾ")]
      latency = item[bstack11l1l11_opy_ (u"ࠬࡲࡡࡵࡧࡱࡧࡾ࠭ࡿ")]
      bstack11llll1ll1_opy_[hub_url] = latency
    bstack1ll1l11l1_opy_ = min(bstack11llll1ll1_opy_, key= lambda x: bstack11llll1ll1_opy_[x])
    bstack1111l1l1_opy_ = bstack1ll1l11l1_opy_
    logger.debug(bstack11l11l1l_opy_.format(bstack1ll1l11l1_opy_))
  except Exception as e:
    logger.debug(bstack11111ll1l_opy_.format(e))
from browserstack_sdk.bstack11l1llll11_opy_ import *
from browserstack_sdk.bstack11l1lll1ll_opy_ import *
from browserstack_sdk.bstack1l1ll1l11_opy_ import *
import logging
import requests
from bstack_utils.constants import *
from bstack_utils.bstack111ll1l11_opy_ import get_logger
from bstack_utils.measure import measure
logger = get_logger(__name__)
@measure(event_name=EVENTS.bstack1lll1l111l_opy_, stage=STAGE.bstack1l1ll1lll_opy_)
def bstack1ll1ll11_opy_():
    global bstack1111l1l1_opy_
    try:
        bstack1ll1l1l11_opy_ = bstack1lll11l11l_opy_()
        bstack11llllll_opy_(bstack1ll1l1l11_opy_)
        hub_url = bstack1ll1l1l11_opy_.get(bstack11l1l11_opy_ (u"ࠨࡵࡳ࡮ࠥࢀ"), bstack11l1l11_opy_ (u"ࠢࠣࢁ"))
        if hub_url.endswith(bstack11l1l11_opy_ (u"ࠨ࠱ࡺࡨ࠴࡮ࡵࡣࠩࢂ")):
            hub_url = hub_url.rsplit(bstack11l1l11_opy_ (u"ࠩ࠲ࡻࡩ࠵ࡨࡶࡤࠪࢃ"), 1)[0]
        if hub_url.startswith(bstack11l1l11_opy_ (u"ࠪ࡬ࡹࡺࡰ࠻࠱࠲ࠫࢄ")):
            hub_url = hub_url[7:]
        elif hub_url.startswith(bstack11l1l11_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴࠭ࢅ")):
            hub_url = hub_url[8:]
        bstack1111l1l1_opy_ = hub_url
    except Exception as e:
        raise RuntimeError(e)
def bstack1lll11l11l_opy_():
    global CONFIG
    bstack11lll11111_opy_ = CONFIG.get(bstack11l1l11_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩࢆ"), {}).get(bstack11l1l11_opy_ (u"࠭ࡧࡳ࡫ࡧࡒࡦࡳࡥࠨࢇ"), bstack11l1l11_opy_ (u"ࠧࡏࡑࡢࡋࡗࡏࡄࡠࡐࡄࡑࡊࡥࡐࡂࡕࡖࡉࡉ࠭࢈"))
    if not isinstance(bstack11lll11111_opy_, str):
        raise ValueError(bstack11l1l11_opy_ (u"ࠣࡃࡗࡗࠥࡀࠠࡈࡴ࡬ࡨࠥࡴࡡ࡮ࡧࠣࡱࡺࡹࡴࠡࡤࡨࠤࡦࠦࡶࡢ࡮࡬ࡨࠥࡹࡴࡳ࡫ࡱ࡫ࠧࢉ"))
    try:
        bstack1ll1l1l11_opy_ = bstack11ll1lll11_opy_(bstack11lll11111_opy_)
        return bstack1ll1l1l11_opy_
    except Exception as e:
        logger.error(bstack11l1l11_opy_ (u"ࠤࡄࡘࡘࠦ࠺ࠡࡇࡵࡶࡴࡸࠠࡪࡰࠣ࡫ࡪࡺࡴࡪࡰࡪࠤ࡬ࡸࡩࡥࠢࡧࡩࡹࡧࡩ࡭ࡵࠣ࠾ࠥࢁࡽࠣࢊ").format(str(e)))
        return {}
def bstack11ll1lll11_opy_(bstack11lll11111_opy_):
    global CONFIG
    try:
        if not CONFIG[bstack11l1l11_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬࢋ")] or not CONFIG[bstack11l1l11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧࢌ")]:
            raise ValueError(bstack11l1l11_opy_ (u"ࠧࡓࡩࡴࡵ࡬ࡲ࡬ࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡻࡳࡦࡴࡱࡥࡲ࡫ࠠࡰࡴࠣࡥࡨࡩࡥࡴࡵࠣ࡯ࡪࡿࠢࢍ"))
        url = bstack1ll11ll1l_opy_ + bstack11lll11111_opy_
        auth = (CONFIG[bstack11l1l11_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨࢎ")], CONFIG[bstack11l1l11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪ࢏")])
        response = requests.get(url, auth=auth)
        if response.status_code == 200 and response.text:
            bstack11l1ll1l_opy_ = json.loads(response.text)
            return bstack11l1ll1l_opy_
    except ValueError as ve:
        logger.error(bstack11l1l11_opy_ (u"ࠣࡃࡗࡗࠥࡀࠠࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡩࡩࡹࡩࡨࡪࡰࡪࠤ࡬ࡸࡩࡥࠢࡧࡩࡹࡧࡩ࡭ࡵࠣ࠾ࠥࢁࡽࠣ࢐").format(str(ve)))
        raise ValueError(ve)
    except Exception as e:
        logger.error(bstack11l1l11_opy_ (u"ࠤࡄࡘࡘࠦ࠺ࠡࡇࡵࡶࡴࡸࠠࡪࡰࠣࡪࡪࡺࡣࡩ࡫ࡱ࡫ࠥ࡭ࡲࡪࡦࠣࡨࡪࡺࡡࡪ࡮ࡶࠤ࠿ࠦࡻࡾࠤ࢑").format(str(e)))
        raise RuntimeError(e)
    return {}
def bstack11llllll_opy_(bstack11l11ll11_opy_):
    global CONFIG
    if bstack11l1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ࢒") not in CONFIG or str(CONFIG[bstack11l1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ࢓")]).lower() == bstack11l1l11_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫ࢔"):
        CONFIG[bstack11l1l11_opy_ (u"࠭࡬ࡰࡥࡤࡰࠬ࢕")] = False
    elif bstack11l1l11_opy_ (u"ࠧࡪࡵࡗࡶ࡮ࡧ࡬ࡈࡴ࡬ࡨࠬ࢖") in bstack11l11ll11_opy_:
        bstack1l1l11l1ll_opy_ = CONFIG.get(bstack11l1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬࢗ"), {})
        logger.debug(bstack11l1l11_opy_ (u"ࠤࡄࡘࡘࠦ࠺ࠡࡇࡻ࡭ࡸࡺࡩ࡯ࡩࠣࡰࡴࡩࡡ࡭ࠢࡲࡴࡹ࡯࡯࡯ࡵ࠽ࠤࠪࡹࠢ࢘"), bstack1l1l11l1ll_opy_)
        bstack1l11l11l_opy_ = bstack11l11ll11_opy_.get(bstack11l1l11_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯ࡕࡩࡵ࡫ࡡࡵࡧࡵࡷ࢙ࠧ"), [])
        bstack11111lll1_opy_ = bstack11l1l11_opy_ (u"ࠦ࠱ࠨ࢚").join(bstack1l11l11l_opy_)
        logger.debug(bstack11l1l11_opy_ (u"ࠧࡇࡔࡔࠢ࠽ࠤࡈࡻࡳࡵࡱࡰࠤࡷ࡫ࡰࡦࡣࡷࡩࡷࠦࡳࡵࡴ࡬ࡲ࡬ࡀࠠࠦࡵ࢛ࠥ"), bstack11111lll1_opy_)
        bstack1llll11l_opy_ = {
            bstack11l1l11_opy_ (u"ࠨ࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠣ࢜"): bstack11l1l11_opy_ (u"ࠢࡢࡶࡶ࠱ࡷ࡫ࡰࡦࡣࡷࡩࡷࠨ࢝"),
            bstack11l1l11_opy_ (u"ࠣࡨࡲࡶࡨ࡫ࡌࡰࡥࡤࡰࠧ࢞"): bstack11l1l11_opy_ (u"ࠤࡷࡶࡺ࡫ࠢ࢟"),
            bstack11l1l11_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯࠰ࡶࡪࡶࡥࡢࡶࡨࡶࠧࢠ"): bstack11111lll1_opy_
        }
        bstack1l1l11l1ll_opy_.update(bstack1llll11l_opy_)
        logger.debug(bstack11l1l11_opy_ (u"ࠦࡆ࡚ࡓࠡ࠼࡙ࠣࡵࡪࡡࡵࡧࡧࠤࡱࡵࡣࡢ࡮ࠣࡳࡵࡺࡩࡰࡰࡶ࠾ࠥࠫࡳࠣࢡ"), bstack1l1l11l1ll_opy_)
        CONFIG[bstack11l1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩࢢ")] = bstack1l1l11l1ll_opy_
        logger.debug(bstack11l1l11_opy_ (u"ࠨࡁࡕࡕࠣ࠾ࠥࡌࡩ࡯ࡣ࡯ࠤࡈࡕࡎࡇࡋࡊ࠾ࠥࠫࡳࠣࢣ"), CONFIG)
def bstack1lll11ll_opy_():
    bstack1ll1l1l11_opy_ = bstack1lll11l11l_opy_()
    if not bstack1ll1l1l11_opy_[bstack11l1l11_opy_ (u"ࠧࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࡙ࡷࡲࠧࢤ")]:
      raise ValueError(bstack11l1l11_opy_ (u"ࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࡚ࡸ࡬ࠡ࡫ࡶࠤࡲ࡯ࡳࡴ࡫ࡱ࡫ࠥ࡬ࡲࡰ࡯ࠣ࡫ࡷ࡯ࡤࠡࡦࡨࡸࡦ࡯࡬ࡴ࠰ࠥࢥ"))
    return bstack1ll1l1l11_opy_[bstack11l1l11_opy_ (u"ࠩࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࡛ࡲ࡭ࠩࢦ")] + bstack11l1l11_opy_ (u"ࠪࡃࡨࡧࡰࡴ࠿ࠪࢧ")
@measure(event_name=EVENTS.bstack11ll11l1l1_opy_, stage=STAGE.bstack1l1ll1lll_opy_)
def bstack1l1ll11l11_opy_() -> list:
    global CONFIG
    result = []
    if CONFIG:
        auth = (CONFIG[bstack11l1l11_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ࢨ")], CONFIG[bstack11l1l11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨࢩ")])
        url = bstack1ll1111ll1_opy_
        logger.debug(bstack11l1l11_opy_ (u"ࠨࡁࡵࡶࡨࡱࡵࡺࡩ࡯ࡩࠣࡸࡴࠦࡦࡦࡶࡦ࡬ࠥࡨࡵࡪ࡮ࡧࡷࠥ࡬ࡲࡰ࡯ࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡗࡹࡷࡨ࡯ࡔࡥࡤࡰࡪࠦࡁࡑࡋࠥࢪ"))
        try:
            response = requests.get(url, auth=auth, headers={bstack11l1l11_opy_ (u"ࠢࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪࠨࢫ"): bstack11l1l11_opy_ (u"ࠣࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠦࢬ")})
            if response.status_code == 200:
                bstack1l1llll111_opy_ = json.loads(response.text)
                bstack1ll1ll1111_opy_ = bstack1l1llll111_opy_.get(bstack11l1l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡴࠩࢭ"), [])
                if bstack1ll1ll1111_opy_:
                    bstack1l1l1111ll_opy_ = bstack1ll1ll1111_opy_[0]
                    build_hashed_id = bstack1l1l1111ll_opy_.get(bstack11l1l11_opy_ (u"ࠪ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ࢮ"))
                    bstack1l1llll1ll_opy_ = bstack11l1l1l1l_opy_ + build_hashed_id
                    result.extend([build_hashed_id, bstack1l1llll1ll_opy_])
                    logger.info(bstack1l1111ll1_opy_.format(bstack1l1llll1ll_opy_))
                    bstack1llll1llll_opy_ = CONFIG[bstack11l1l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧࢯ")]
                    if bstack11l1l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࢰ") in CONFIG:
                      bstack1llll1llll_opy_ += bstack11l1l11_opy_ (u"࠭ࠠࠨࢱ") + CONFIG[bstack11l1l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩࢲ")]
                    if bstack1llll1llll_opy_ != bstack1l1l1111ll_opy_.get(bstack11l1l11_opy_ (u"ࠨࡰࡤࡱࡪ࠭ࢳ")):
                      logger.debug(bstack1l11l111_opy_.format(bstack1l1l1111ll_opy_.get(bstack11l1l11_opy_ (u"ࠩࡱࡥࡲ࡫ࠧࢴ")), bstack1llll1llll_opy_))
                    return result
                else:
                    logger.debug(bstack11l1l11_opy_ (u"ࠥࡅ࡙࡙ࠠ࠻ࠢࡑࡳࠥࡨࡵࡪ࡮ࡧࡷࠥ࡬࡯ࡶࡰࡧࠤ࡮ࡴࠠࡵࡪࡨࠤࡷ࡫ࡳࡱࡱࡱࡷࡪ࠴ࠢࢵ"))
            else:
                logger.debug(bstack11l1l11_opy_ (u"ࠦࡆ࡚ࡓࠡ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡦࡦࡶࡦ࡬ࠥࡨࡵࡪ࡮ࡧࡷ࠳ࠨࢶ"))
        except Exception as e:
            logger.error(bstack11l1l11_opy_ (u"ࠧࡇࡔࡔࠢ࠽ࠤࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡣࡷ࡬ࡰࡩࡹࠠ࠻ࠢࡾࢁࠧࢷ").format(str(e)))
    else:
        logger.debug(bstack11l1l11_opy_ (u"ࠨࡁࡕࡕࠣ࠾ࠥࡉࡏࡏࡈࡌࡋࠥ࡯ࡳࠡࡰࡲࡸࠥࡹࡥࡵ࠰࡙ࠣࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡦࡦࡶࡦ࡬ࠥࡨࡵࡪ࡮ࡧࡷ࠳ࠨࢸ"))
    return [None, None]
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.bstack11l11ll11l_opy_ import bstack11l11ll11l_opy_, bstack1llll111ll_opy_, bstack1l1ll11ll_opy_, bstack111111ll1_opy_
from bstack_utils.measure import bstack1l1ll1l11l_opy_
from bstack_utils.measure import measure
from bstack_utils.percy import *
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.bstack1l11111lll_opy_ import bstack11lll1lll1_opy_
from bstack_utils.messages import *
from bstack_utils import bstack111ll1l11_opy_
from bstack_utils.constants import *
from bstack_utils.helper import bstack1ll1l11l_opy_, bstack111ll11ll_opy_, bstack1ll11l11l_opy_, bstack1llllllll1_opy_, \
  bstack1l1l1ll11l_opy_, \
  Notset, bstack11l1l1l11l_opy_, \
  bstack1ll1l1llll_opy_, bstack11lll11l11_opy_, bstack1llll11l11_opy_, bstack1ll1lllll1_opy_, bstack1lll1ll11l_opy_, bstack1lll1l1ll1_opy_, \
  bstack1l1l111ll_opy_, \
  bstack11lll1lll_opy_, bstack1l11l1llll_opy_, bstack1l11llll_opy_, bstack1111llll1_opy_, \
  bstack1l111lll1_opy_, bstack1l1ll111ll_opy_, bstack1ll11l1l1_opy_, bstack1l1l111ll1_opy_
from bstack_utils.bstack1l1lll1111_opy_ import bstack1l1ll1l1l1_opy_, bstack11l1lll1_opy_
from bstack_utils.bstack1l11llll1_opy_ import bstack1ll111l1l_opy_
from bstack_utils.bstack11lll1l1_opy_ import bstack1l1l1l11l1_opy_, bstack1llll1lll1_opy_
from bstack_utils.bstack11ll1lll1l_opy_ import bstack11ll1lll1l_opy_
from bstack_utils.bstack1l1111ll11_opy_ import bstack1l1l111l11_opy_
from bstack_utils.proxy import bstack11llll1l_opy_, bstack1ll11lll1_opy_, bstack11ll1l1l1_opy_, bstack1l1ll1ll11_opy_
from bstack_utils.bstack1lll11lll1_opy_ import bstack111l1l1l1_opy_
import bstack_utils.bstack1ll1l11ll_opy_ as bstack11l1111l1_opy_
import bstack_utils.bstack11ll1l11l1_opy_ as bstack1lll1111l_opy_
if os.getenv(bstack11l1l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡍࡋࡢࡌࡔࡕࡋࡔࠩࢹ")):
  cli.bstack1l1l1lll1_opy_()
else:
  os.environ[bstack11l1l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡎࡌࡣࡍࡕࡏࡌࡕࠪࢺ")] = bstack11l1l11_opy_ (u"ࠩࡷࡶࡺ࡫ࠧࢻ")
bstack1l1ll1lll1_opy_ = bstack11l1l11_opy_ (u"ࠪࠤࠥ࠵ࠪࠡ࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࠥ࠰࠯࡝ࡰࠣࠤ࡮࡬ࠨࡱࡣࡪࡩࠥࡃ࠽࠾ࠢࡹࡳ࡮ࡪࠠ࠱ࠫࠣࡿࡡࡴࠠࠡࠢࡷࡶࡾࢁ࡜࡯ࠢࡦࡳࡳࡹࡴࠡࡨࡶࠤࡂࠦࡲࡦࡳࡸ࡭ࡷ࡫ࠨ࡝ࠩࡩࡷࡡ࠭ࠩ࠼࡞ࡱࠤࠥࠦࠠࠡࡨࡶ࠲ࡦࡶࡰࡦࡰࡧࡊ࡮ࡲࡥࡔࡻࡱࡧ࠭ࡨࡳࡵࡣࡦ࡯ࡤࡶࡡࡵࡪ࠯ࠤࡏ࡙ࡏࡏ࠰ࡶࡸࡷ࡯࡮ࡨ࡫ࡩࡽ࠭ࡶ࡟ࡪࡰࡧࡩࡽ࠯ࠠࠬࠢࠥ࠾ࠧࠦࠫࠡࡌࡖࡓࡓ࠴ࡳࡵࡴ࡬ࡲ࡬࡯ࡦࡺࠪࡍࡗࡔࡔ࠮ࡱࡣࡵࡷࡪ࠮ࠨࡢࡹࡤ࡭ࡹࠦ࡮ࡦࡹࡓࡥ࡬࡫࠲࠯ࡧࡹࡥࡱࡻࡡࡵࡧࠫࠦ࠭࠯ࠠ࠾ࡀࠣࡿࢂࠨࠬࠡ࡞ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥ࡫ࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡄࡦࡶࡤ࡭ࡱࡹࠢࡾ࡞ࠪ࠭࠮࠯࡛ࠣࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠦࡢ࠯ࠠࠬࠢࠥ࠰ࡡࡢ࡮ࠣࠫ࡟ࡲࠥࠦࠠࠡࡿࡦࡥࡹࡩࡨࠩࡧࡻ࠭ࢀࡢ࡮ࠡࠢࠣࠤࢂࡢ࡮ࠡࠢࢀࡠࡳࠦࠠ࠰ࠬࠣࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃࠠࠫ࠱ࠪࢼ")
bstack11l1lll1l1_opy_ = bstack11l1l11_opy_ (u"ࠫࡡࡴ࠯ࠫࠢࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࠦࠪ࠰࡞ࡱࡧࡴࡴࡳࡵࠢࡥࡷࡹࡧࡣ࡬ࡡࡳࡥࡹ࡮ࠠ࠾ࠢࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࡜ࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࠮࡭ࡧࡱ࡫ࡹ࡮ࠠ࠮ࠢ࠶ࡡࡡࡴࡣࡰࡰࡶࡸࠥࡨࡳࡵࡣࡦ࡯ࡤࡩࡡࡱࡵࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࡟ࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡰࡪࡴࡧࡵࡪࠣ࠱ࠥ࠷࡝࡝ࡰࡦࡳࡳࡹࡴࠡࡲࡢ࡭ࡳࡪࡥࡹࠢࡀࠤࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࡞ࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࠰࡯ࡩࡳ࡭ࡴࡩࠢ࠰ࠤ࠷ࡣ࡜࡯ࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼࠠ࠾ࠢࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࠯ࡵ࡯࡭ࡨ࡫ࠨ࠱࠮ࠣࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࠰࡯ࡩࡳ࡭ࡴࡩࠢ࠰ࠤ࠸࠯࡜࡯ࡥࡲࡲࡸࡺࠠࡪ࡯ࡳࡳࡷࡺ࡟ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࠸ࡤࡨࡳࡵࡣࡦ࡯ࠥࡃࠠࡳࡧࡴࡹ࡮ࡸࡥࠩࠤࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨࠩ࠼࡞ࡱ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫࠯ࡥ࡫ࡶࡴࡳࡩࡶ࡯࠱ࡰࡦࡻ࡮ࡤࡪࠣࡁࠥࡧࡳࡺࡰࡦࠤ࠭ࡲࡡࡶࡰࡦ࡬ࡔࡶࡴࡪࡱࡱࡷ࠮ࠦ࠽࠿ࠢࡾࡠࡳࡲࡥࡵࠢࡦࡥࡵࡹ࠻࡝ࡰࡷࡶࡾࠦࡻ࡝ࡰࡦࡥࡵࡹࠠ࠾ࠢࡍࡗࡔࡔ࠮ࡱࡣࡵࡷࡪ࠮ࡢࡴࡶࡤࡧࡰࡥࡣࡢࡲࡶ࠭ࡡࡴࠠࠡࡿࠣࡧࡦࡺࡣࡩࠪࡨࡼ࠮ࠦࡻ࡝ࡰࠣࠤࠥࠦࡽ࡝ࡰࠣࠤࡷ࡫ࡴࡶࡴࡱࠤࡦࡽࡡࡪࡶࠣ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫࠯ࡥ࡫ࡶࡴࡳࡩࡶ࡯࠱ࡧࡴࡴ࡮ࡦࡥࡷࠬࢀࡢ࡮ࠡࠢࠣࠤࡼࡹࡅ࡯ࡦࡳࡳ࡮ࡴࡴ࠻ࠢࡣࡻࡸࡹ࠺࠰࠱ࡦࡨࡵ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࡅࡣࡢࡲࡶࡁࠩࢁࡥ࡯ࡥࡲࡨࡪ࡛ࡒࡊࡅࡲࡱࡵࡵ࡮ࡦࡰࡷࠬࡏ࡙ࡏࡏ࠰ࡶࡸࡷ࡯࡮ࡨ࡫ࡩࡽ࠭ࡩࡡࡱࡵࠬ࠭ࢂࡦࠬ࡝ࡰࠣࠤࠥࠦ࠮࠯࠰࡯ࡥࡺࡴࡣࡩࡑࡳࡸ࡮ࡵ࡮ࡴ࡞ࡱࠤࠥࢃࠩ࡝ࡰࢀࡠࡳ࠵ࠪࠡ࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࠥ࠰࠯࡝ࡰࠪࢽ")
from ._version import __version__
bstack1ll1l11l11_opy_ = None
CONFIG = {}
bstack11lllll1l1_opy_ = {}
bstack1ll111111l_opy_ = {}
bstack1lll11111_opy_ = None
bstack1l1ll11l1l_opy_ = None
bstack11l1l1lll_opy_ = None
bstack1l1ll11111_opy_ = -1
bstack1l1lllllll_opy_ = 0
bstack1llll1ll1l_opy_ = bstack11lll1l1l_opy_
bstack1l11l11l1l_opy_ = 1
bstack111lll11_opy_ = False
bstack1lll1l11l1_opy_ = False
bstack1l11lll1l_opy_ = bstack11l1l11_opy_ (u"ࠬ࠭ࢾ")
bstack11l1ll1l1_opy_ = bstack11l1l11_opy_ (u"࠭ࠧࢿ")
bstack11ll11l11l_opy_ = False
bstack1l111ll111_opy_ = True
bstack1lll111l1_opy_ = bstack11l1l11_opy_ (u"ࠧࠨࣀ")
bstack1l11ll11l1_opy_ = []
bstack1111l1l1_opy_ = bstack11l1l11_opy_ (u"ࠨࠩࣁ")
bstack1l1l1lllll_opy_ = False
bstack1ll1llll1_opy_ = None
bstack1l1ll1llll_opy_ = None
bstack11l1l1ll_opy_ = None
bstack11l11ll111_opy_ = -1
bstack1ll11l1ll1_opy_ = os.path.join(os.path.expanduser(bstack11l1l11_opy_ (u"ࠩࢁࠫࣂ")), bstack11l1l11_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪࣃ"), bstack11l1l11_opy_ (u"ࠫ࠳ࡸ࡯ࡣࡱࡷ࠱ࡷ࡫ࡰࡰࡴࡷ࠱࡭࡫࡬ࡱࡧࡵ࠲࡯ࡹ࡯࡯ࠩࣄ"))
bstack1lll1ll111_opy_ = 0
bstack1l1l1ll1l1_opy_ = 0
bstack1l1lll111_opy_ = []
bstack11l1l1l1l1_opy_ = []
bstack1l1lll1ll_opy_ = []
bstack11l1l1l1ll_opy_ = []
bstack1111l1111_opy_ = bstack11l1l11_opy_ (u"ࠬ࠭ࣅ")
bstack11llllll1_opy_ = bstack11l1l11_opy_ (u"࠭ࠧࣆ")
bstack1l1lllll1_opy_ = False
bstack1l11l1ll11_opy_ = False
bstack1l11lll1ll_opy_ = {}
bstack1lll1l1l_opy_ = None
bstack1lllll11l1_opy_ = None
bstack1ll111ll1l_opy_ = None
bstack11l1lll1l_opy_ = None
bstack111ll11l_opy_ = None
bstack1lll1lll_opy_ = None
bstack1l1llll11_opy_ = None
bstack1lll11l1ll_opy_ = None
bstack1l1l1ll111_opy_ = None
bstack1ll111ll_opy_ = None
bstack1l111l1l1_opy_ = None
bstack1ll111l1_opy_ = None
bstack1llll1l1ll_opy_ = None
bstack1l1l1lll_opy_ = None
bstack1l1111111l_opy_ = None
bstack11llll11ll_opy_ = None
bstack1l1111ll1l_opy_ = None
bstack11l1l11l_opy_ = None
bstack11ll11lll_opy_ = None
bstack11l1l111ll_opy_ = None
bstack1111ll1l_opy_ = None
bstack1l1l11l11_opy_ = None
bstack1l11lll1l1_opy_ = None
thread_local = threading.local()
bstack1l1l1lll1l_opy_ = False
bstack1l1l111111_opy_ = bstack11l1l11_opy_ (u"ࠢࠣࣇ")
logger = bstack111ll1l11_opy_.get_logger(__name__, bstack1llll1ll1l_opy_)
bstack111ll1lll_opy_ = Config.bstack111l1l1l_opy_()
percy = bstack111l11l1l_opy_()
bstack1l111llll_opy_ = bstack11lll1lll1_opy_()
bstack11l111111_opy_ = bstack1l1ll1l11_opy_()
def bstack1l1l1l1l11_opy_():
  global CONFIG
  global bstack1l1lllll1_opy_
  global bstack111ll1lll_opy_
  bstack1llll111_opy_ = bstack1lll1lll11_opy_(CONFIG)
  if bstack1l1l1ll11l_opy_(CONFIG):
    if (bstack11l1l11_opy_ (u"ࠨࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪࣈ") in bstack1llll111_opy_ and str(bstack1llll111_opy_[bstack11l1l11_opy_ (u"ࠩࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫࣉ")]).lower() == bstack11l1l11_opy_ (u"ࠪࡸࡷࡻࡥࠨ࣊")):
      bstack1l1lllll1_opy_ = True
    bstack111ll1lll_opy_.bstack11l11l11l_opy_(bstack1llll111_opy_.get(bstack11l1l11_opy_ (u"ࠫࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠨ࣋"), False))
  else:
    bstack1l1lllll1_opy_ = True
    bstack111ll1lll_opy_.bstack11l11l11l_opy_(True)
def bstack1l1l111l_opy_():
  from appium.version import version as appium_version
  return version.parse(appium_version)
def bstack1ll1lllll_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack1ll1ll1l_opy_():
  args = sys.argv
  for i in range(len(args)):
    if bstack11l1l11_opy_ (u"ࠧ࠳࠭ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡩ࡯࡯ࡨ࡬࡫࡫࡯࡬ࡦࠤ࣌") == args[i].lower() or bstack11l1l11_opy_ (u"ࠨ࠭࠮ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡱࡪ࡮࡭ࠢ࣍") == args[i].lower():
      path = args[i + 1]
      sys.argv.remove(args[i])
      sys.argv.remove(path)
      global bstack1lll111l1_opy_
      bstack1lll111l1_opy_ += bstack11l1l11_opy_ (u"ࠧ࠮࠯ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡄࡱࡱࡪ࡮࡭ࡆࡪ࡮ࡨࠤࠬ࣎") + path
      return path
  return None
bstack1llllll1l_opy_ = re.compile(bstack11l1l11_opy_ (u"ࡳࠤ࠱࠮ࡄࡢࠤࡼࠪ࠱࠮ࡄ࠯ࡽ࠯ࠬࡂ࣏ࠦ"))
def bstack1l11llll1l_opy_(loader, node):
  value = loader.construct_scalar(node)
  for group in bstack1llllll1l_opy_.findall(value):
    if group is not None and os.environ.get(group) is not None:
      value = value.replace(bstack11l1l11_opy_ (u"ࠤࠧࡿ࣐ࠧ") + group + bstack11l1l11_opy_ (u"ࠥࢁ࣑ࠧ"), os.environ.get(group))
  return value
def bstack11l111lll_opy_():
  global bstack1l11lll1l1_opy_
  if bstack1l11lll1l1_opy_ is None:
        bstack1l11lll1l1_opy_ = bstack1ll1ll1l_opy_()
  bstack1l111lll1l_opy_ = bstack1l11lll1l1_opy_
  if bstack1l111lll1l_opy_ and os.path.exists(os.path.abspath(bstack1l111lll1l_opy_)):
    fileName = bstack1l111lll1l_opy_
  if bstack11l1l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࡢࡊࡎࡒࡅࠨ࣒") in os.environ and os.path.exists(
          os.path.abspath(os.environ[bstack11l1l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡕࡎࡇࡋࡊࡣࡋࡏࡌࡆ࣓ࠩ")])) and not bstack11l1l11_opy_ (u"࠭ࡦࡪ࡮ࡨࡒࡦࡳࡥࠨࣔ") in locals():
    fileName = os.environ[bstack11l1l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡐࡐࡉࡍࡌࡥࡆࡊࡎࡈࠫࣕ")]
  if bstack11l1l11_opy_ (u"ࠨࡨ࡬ࡰࡪࡔࡡ࡮ࡧࠪࣖ") in locals():
    bstack1lllll1l_opy_ = os.path.abspath(fileName)
  else:
    bstack1lllll1l_opy_ = bstack11l1l11_opy_ (u"ࠩࠪࣗ")
  bstack1llll11l1_opy_ = os.getcwd()
  bstack1lllll1l11_opy_ = bstack11l1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡱࡱ࠭ࣘ")
  bstack1l1l11111_opy_ = bstack11l1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡽࡦࡳ࡬ࠨࣙ")
  while (not os.path.exists(bstack1lllll1l_opy_)) and bstack1llll11l1_opy_ != bstack11l1l11_opy_ (u"ࠧࠨࣚ"):
    bstack1lllll1l_opy_ = os.path.join(bstack1llll11l1_opy_, bstack1lllll1l11_opy_)
    if not os.path.exists(bstack1lllll1l_opy_):
      bstack1lllll1l_opy_ = os.path.join(bstack1llll11l1_opy_, bstack1l1l11111_opy_)
    if bstack1llll11l1_opy_ != os.path.dirname(bstack1llll11l1_opy_):
      bstack1llll11l1_opy_ = os.path.dirname(bstack1llll11l1_opy_)
    else:
      bstack1llll11l1_opy_ = bstack11l1l11_opy_ (u"ࠨࠢࣛ")
  bstack1l11lll1l1_opy_ = bstack1lllll1l_opy_ if os.path.exists(bstack1lllll1l_opy_) else None
  return bstack1l11lll1l1_opy_
def bstack11l1l1l11_opy_():
  bstack1lllll1l_opy_ = bstack11l111lll_opy_()
  if not os.path.exists(bstack1lllll1l_opy_):
    bstack11111l1ll_opy_(
      bstack1l11ll11_opy_.format(os.getcwd()))
  try:
    with open(bstack1lllll1l_opy_, bstack11l1l11_opy_ (u"ࠧࡳࠩࣜ")) as stream:
      yaml.add_implicit_resolver(bstack11l1l11_opy_ (u"ࠣࠣࡳࡥࡹ࡮ࡥࡹࠤࣝ"), bstack1llllll1l_opy_)
      yaml.add_constructor(bstack11l1l11_opy_ (u"ࠤࠤࡴࡦࡺࡨࡦࡺࠥࣞ"), bstack1l11llll1l_opy_)
      config = yaml.load(stream, yaml.FullLoader)
      return config
  except:
    with open(bstack1lllll1l_opy_, bstack11l1l11_opy_ (u"ࠪࡶࠬࣟ")) as stream:
      try:
        config = yaml.safe_load(stream)
        return config
      except yaml.YAMLError as exc:
        bstack11111l1ll_opy_(bstack1ll1ll1ll1_opy_.format(str(exc)))
def bstack1lll1l1l11_opy_(config):
  bstack11l11llll_opy_ = bstack1l1ll1111l_opy_(config)
  for option in list(bstack11l11llll_opy_):
    if option.lower() in bstack1lllll11l_opy_ and option != bstack1lllll11l_opy_[option.lower()]:
      bstack11l11llll_opy_[bstack1lllll11l_opy_[option.lower()]] = bstack11l11llll_opy_[option]
      del bstack11l11llll_opy_[option]
  return config
def bstack11ll1l1ll_opy_():
  global bstack1ll111111l_opy_
  for key, bstack111l111l_opy_ in bstack111lll1ll_opy_.items():
    if isinstance(bstack111l111l_opy_, list):
      for var in bstack111l111l_opy_:
        if var in os.environ and os.environ[var] and str(os.environ[var]).strip():
          bstack1ll111111l_opy_[key] = os.environ[var]
          break
    elif bstack111l111l_opy_ in os.environ and os.environ[bstack111l111l_opy_] and str(os.environ[bstack111l111l_opy_]).strip():
      bstack1ll111111l_opy_[key] = os.environ[bstack111l111l_opy_]
  if bstack11l1l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࡡࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭࣠") in os.environ:
    bstack1ll111111l_opy_[bstack11l1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩ࣡")] = {}
    bstack1ll111111l_opy_[bstack11l1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪ࣢")][bstack11l1l11_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࣣࠩ")] = os.environ[bstack11l1l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡑࡆࡅࡑࡥࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠪࣤ")]
def bstack1l11l11111_opy_():
  global bstack11lllll1l1_opy_
  global bstack1lll111l1_opy_
  for idx, val in enumerate(sys.argv):
    if idx < len(sys.argv) and bstack11l1l11_opy_ (u"ࠩ࠰࠱ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬࣥ").lower() == val.lower():
      bstack11lllll1l1_opy_[bstack11l1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࣦࠧ")] = {}
      bstack11lllll1l1_opy_[bstack11l1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨࣧ")][bstack11l1l11_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࣨ")] = sys.argv[idx + 1]
      del sys.argv[idx:idx + 2]
      break
  for key, bstack11l1l1111l_opy_ in bstack1ll1llllll_opy_.items():
    if isinstance(bstack11l1l1111l_opy_, list):
      for idx, val in enumerate(sys.argv):
        for var in bstack11l1l1111l_opy_:
          if idx < len(sys.argv) and bstack11l1l11_opy_ (u"࠭࠭࠮ࣩࠩ") + var.lower() == val.lower() and not key in bstack11lllll1l1_opy_:
            bstack11lllll1l1_opy_[key] = sys.argv[idx + 1]
            bstack1lll111l1_opy_ += bstack11l1l11_opy_ (u"ࠧࠡ࠯࠰ࠫ࣪") + var + bstack11l1l11_opy_ (u"ࠨࠢࠪ࣫") + sys.argv[idx + 1]
            del sys.argv[idx:idx + 2]
            break
    else:
      for idx, val in enumerate(sys.argv):
        if idx < len(sys.argv) and bstack11l1l11_opy_ (u"ࠩ࠰࠱ࠬ࣬") + bstack11l1l1111l_opy_.lower() == val.lower() and not key in bstack11lllll1l1_opy_:
          bstack11lllll1l1_opy_[key] = sys.argv[idx + 1]
          bstack1lll111l1_opy_ += bstack11l1l11_opy_ (u"ࠪࠤ࠲࠳࣭ࠧ") + bstack11l1l1111l_opy_ + bstack11l1l11_opy_ (u"࣮ࠫࠥ࠭") + sys.argv[idx + 1]
          del sys.argv[idx:idx + 2]
def bstack1l1lll11l_opy_(config):
  bstack11ll1llll_opy_ = config.keys()
  for bstack11lll1ll11_opy_, bstack1ll1l1ll11_opy_ in bstack111111l11_opy_.items():
    if bstack1ll1l1ll11_opy_ in bstack11ll1llll_opy_:
      config[bstack11lll1ll11_opy_] = config[bstack1ll1l1ll11_opy_]
      del config[bstack1ll1l1ll11_opy_]
  for bstack11lll1ll11_opy_, bstack1ll1l1ll11_opy_ in bstack1l11l1l1l_opy_.items():
    if isinstance(bstack1ll1l1ll11_opy_, list):
      for bstack1ll1lll1l_opy_ in bstack1ll1l1ll11_opy_:
        if bstack1ll1lll1l_opy_ in bstack11ll1llll_opy_:
          config[bstack11lll1ll11_opy_] = config[bstack1ll1lll1l_opy_]
          del config[bstack1ll1lll1l_opy_]
          break
    elif bstack1ll1l1ll11_opy_ in bstack11ll1llll_opy_:
      config[bstack11lll1ll11_opy_] = config[bstack1ll1l1ll11_opy_]
      del config[bstack1ll1l1ll11_opy_]
  for bstack1ll1lll1l_opy_ in list(config):
    for bstack1lll11l11_opy_ in bstack1ll111l11l_opy_:
      if bstack1ll1lll1l_opy_.lower() == bstack1lll11l11_opy_.lower() and bstack1ll1lll1l_opy_ != bstack1lll11l11_opy_:
        config[bstack1lll11l11_opy_] = config[bstack1ll1lll1l_opy_]
        del config[bstack1ll1lll1l_opy_]
  bstack11ll1l1lll_opy_ = [{}]
  if not config.get(bstack11l1l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ࣯")):
    config[bstack11l1l11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࣰࠩ")] = [{}]
  bstack11ll1l1lll_opy_ = config[bstack11l1l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࣱࠪ")]
  for platform in bstack11ll1l1lll_opy_:
    for bstack1ll1lll1l_opy_ in list(platform):
      for bstack1lll11l11_opy_ in bstack1ll111l11l_opy_:
        if bstack1ll1lll1l_opy_.lower() == bstack1lll11l11_opy_.lower() and bstack1ll1lll1l_opy_ != bstack1lll11l11_opy_:
          platform[bstack1lll11l11_opy_] = platform[bstack1ll1lll1l_opy_]
          del platform[bstack1ll1lll1l_opy_]
  for bstack11lll1ll11_opy_, bstack1ll1l1ll11_opy_ in bstack1l11l1l1l_opy_.items():
    for platform in bstack11ll1l1lll_opy_:
      if isinstance(bstack1ll1l1ll11_opy_, list):
        for bstack1ll1lll1l_opy_ in bstack1ll1l1ll11_opy_:
          if bstack1ll1lll1l_opy_ in platform:
            platform[bstack11lll1ll11_opy_] = platform[bstack1ll1lll1l_opy_]
            del platform[bstack1ll1lll1l_opy_]
            break
      elif bstack1ll1l1ll11_opy_ in platform:
        platform[bstack11lll1ll11_opy_] = platform[bstack1ll1l1ll11_opy_]
        del platform[bstack1ll1l1ll11_opy_]
  for bstack1111111l1_opy_ in bstack1l11ll1l_opy_:
    if bstack1111111l1_opy_ in config:
      if not bstack1l11ll1l_opy_[bstack1111111l1_opy_] in config:
        config[bstack1l11ll1l_opy_[bstack1111111l1_opy_]] = {}
      config[bstack1l11ll1l_opy_[bstack1111111l1_opy_]].update(config[bstack1111111l1_opy_])
      del config[bstack1111111l1_opy_]
  for platform in bstack11ll1l1lll_opy_:
    for bstack1111111l1_opy_ in bstack1l11ll1l_opy_:
      if bstack1111111l1_opy_ in list(platform):
        if not bstack1l11ll1l_opy_[bstack1111111l1_opy_] in platform:
          platform[bstack1l11ll1l_opy_[bstack1111111l1_opy_]] = {}
        platform[bstack1l11ll1l_opy_[bstack1111111l1_opy_]].update(platform[bstack1111111l1_opy_])
        del platform[bstack1111111l1_opy_]
  config = bstack1lll1l1l11_opy_(config)
  return config
def bstack11l1l11ll1_opy_(config):
  global bstack11l1ll1l1_opy_
  bstack111llll1l_opy_ = False
  if bstack11l1l11_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࣲࠬ") in config and str(config[bstack11l1l11_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭ࣳ")]).lower() != bstack11l1l11_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩࣴ"):
    if bstack11l1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨࣵ") not in config or str(config[bstack11l1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࣶࠩ")]).lower() == bstack11l1l11_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬࣷ"):
      config[bstack11l1l11_opy_ (u"ࠧ࡭ࡱࡦࡥࡱ࠭ࣸ")] = False
    else:
      bstack1ll1l1l11_opy_ = bstack1lll11l11l_opy_()
      if bstack11l1l11_opy_ (u"ࠨ࡫ࡶࡘࡷ࡯ࡡ࡭ࡉࡵ࡭ࡩࣹ࠭") in bstack1ll1l1l11_opy_:
        if not bstack11l1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸࣺ࠭") in config:
          config[bstack11l1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧࣻ")] = {}
        config[bstack11l1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨࣼ")][bstack11l1l11_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࣽ")] = bstack11l1l11_opy_ (u"࠭ࡡࡵࡵ࠰ࡶࡪࡶࡥࡢࡶࡨࡶࠬࣾ")
        bstack111llll1l_opy_ = True
        bstack11l1ll1l1_opy_ = config[bstack11l1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫࣿ")].get(bstack11l1l11_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪऀ"))
  if bstack1l1l1ll11l_opy_(config) and bstack11l1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ँ") in config and str(config[bstack11l1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧं")]).lower() != bstack11l1l11_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪः") and not bstack111llll1l_opy_:
    if not bstack11l1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩऄ") in config:
      config[bstack11l1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪअ")] = {}
    if not config[bstack11l1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫआ")].get(bstack11l1l11_opy_ (u"ࠨࡵ࡮࡭ࡵࡈࡩ࡯ࡣࡵࡽࡎࡴࡩࡵ࡫ࡤࡰ࡮ࡹࡡࡵ࡫ࡲࡲࠬइ")) and not bstack11l1l11_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫई") in config[bstack11l1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧउ")]:
      bstack1ll11ll11_opy_ = datetime.datetime.now()
      bstack1l1l1l1l1_opy_ = bstack1ll11ll11_opy_.strftime(bstack11l1l11_opy_ (u"ࠫࠪࡪ࡟ࠦࡤࡢࠩࡍࠫࡍࠨऊ"))
      hostname = socket.gethostname()
      bstack1llll1l11l_opy_ = bstack11l1l11_opy_ (u"ࠬ࠭ऋ").join(random.choices(string.ascii_lowercase + string.digits, k=4))
      identifier = bstack11l1l11_opy_ (u"࠭ࡻࡾࡡࡾࢁࡤࢁࡽࠨऌ").format(bstack1l1l1l1l1_opy_, hostname, bstack1llll1l11l_opy_)
      config[bstack11l1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫऍ")][bstack11l1l11_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪऎ")] = identifier
    bstack11l1ll1l1_opy_ = config[bstack11l1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ए")].get(bstack11l1l11_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬऐ"))
  return config
def bstack1l1l11ll1_opy_():
  bstack111111lll_opy_ =  bstack1ll1lllll1_opy_()[bstack11l1l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠪऑ")]
  return bstack111111lll_opy_ if bstack111111lll_opy_ else -1
def bstack11ll1lll_opy_(bstack111111lll_opy_):
  global CONFIG
  if not bstack11l1l11_opy_ (u"ࠬࠪࡻࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࢃࠧऒ") in CONFIG[bstack11l1l11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨओ")]:
    return
  CONFIG[bstack11l1l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩऔ")] = CONFIG[bstack11l1l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪक")].replace(
    bstack11l1l11_opy_ (u"ࠩࠧࡿࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࢀࠫख"),
    str(bstack111111lll_opy_)
  )
def bstack1ll11l111_opy_():
  global CONFIG
  if not bstack11l1l11_opy_ (u"ࠪࠨࢀࡊࡁࡕࡇࡢࡘࡎࡓࡅࡾࠩग") in CONFIG[bstack11l1l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭घ")]:
    return
  bstack1ll11ll11_opy_ = datetime.datetime.now()
  bstack1l1l1l1l1_opy_ = bstack1ll11ll11_opy_.strftime(bstack11l1l11_opy_ (u"ࠬࠫࡤ࠮ࠧࡥ࠱ࠪࡎ࠺ࠦࡏࠪङ"))
  CONFIG[bstack11l1l11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨच")] = CONFIG[bstack11l1l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩछ")].replace(
    bstack11l1l11_opy_ (u"ࠨࠦࡾࡈࡆ࡚ࡅࡠࡖࡌࡑࡊࢃࠧज"),
    bstack1l1l1l1l1_opy_
  )
def bstack111l1l11_opy_():
  global CONFIG
  if bstack11l1l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫझ") in CONFIG and not bool(CONFIG[bstack11l1l11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬञ")]):
    del CONFIG[bstack11l1l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ट")]
    return
  if not bstack11l1l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧठ") in CONFIG:
    CONFIG[bstack11l1l11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨड")] = bstack11l1l11_opy_ (u"ࠧࠤࠦࡾࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࡿࠪढ")
  if bstack11l1l11_opy_ (u"ࠨࠦࡾࡈࡆ࡚ࡅࡠࡖࡌࡑࡊࢃࠧण") in CONFIG[bstack11l1l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫत")]:
    bstack1ll11l111_opy_()
    os.environ[bstack11l1l11_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡢࡇࡔࡓࡂࡊࡐࡈࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠧथ")] = CONFIG[bstack11l1l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭द")]
  if not bstack11l1l11_opy_ (u"ࠬࠪࡻࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࢃࠧध") in CONFIG[bstack11l1l11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨन")]:
    return
  bstack111111lll_opy_ = bstack11l1l11_opy_ (u"ࠧࠨऩ")
  bstack111ll1l1_opy_ = bstack1l1l11ll1_opy_()
  if bstack111ll1l1_opy_ != -1:
    bstack111111lll_opy_ = bstack11l1l11_opy_ (u"ࠨࡅࡌࠤࠬप") + str(bstack111ll1l1_opy_)
  if bstack111111lll_opy_ == bstack11l1l11_opy_ (u"ࠩࠪफ"):
    bstack1l1l11l11l_opy_ = bstack1l1111l111_opy_(CONFIG[bstack11l1l11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ब")])
    if bstack1l1l11l11l_opy_ != -1:
      bstack111111lll_opy_ = str(bstack1l1l11l11l_opy_)
  if bstack111111lll_opy_:
    bstack11ll1lll_opy_(bstack111111lll_opy_)
    os.environ[bstack11l1l11_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡣࡈࡕࡍࡃࡋࡑࡉࡉࡥࡂࡖࡋࡏࡈࡤࡏࡄࠨभ")] = CONFIG[bstack11l1l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧम")]
def bstack1l11l1lll1_opy_(bstack1111l1l1l_opy_, bstack11l11111_opy_, path):
  bstack1llllll1ll_opy_ = {
    bstack11l1l11_opy_ (u"࠭ࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪय"): bstack11l11111_opy_
  }
  if os.path.exists(path):
    bstack1lll1111_opy_ = json.load(open(path, bstack11l1l11_opy_ (u"ࠧࡳࡤࠪर")))
  else:
    bstack1lll1111_opy_ = {}
  bstack1lll1111_opy_[bstack1111l1l1l_opy_] = bstack1llllll1ll_opy_
  with open(path, bstack11l1l11_opy_ (u"ࠣࡹ࠮ࠦऱ")) as outfile:
    json.dump(bstack1lll1111_opy_, outfile)
def bstack1l1111l111_opy_(bstack1111l1l1l_opy_):
  bstack1111l1l1l_opy_ = str(bstack1111l1l1l_opy_)
  bstack1l11l11ll_opy_ = os.path.join(os.path.expanduser(bstack11l1l11_opy_ (u"ࠩࢁࠫल")), bstack11l1l11_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪळ"))
  try:
    if not os.path.exists(bstack1l11l11ll_opy_):
      os.makedirs(bstack1l11l11ll_opy_)
    file_path = os.path.join(os.path.expanduser(bstack11l1l11_opy_ (u"ࠫࢃ࠭ऴ")), bstack11l1l11_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬव"), bstack11l1l11_opy_ (u"࠭࠮ࡣࡷ࡬ࡰࡩ࠳࡮ࡢ࡯ࡨ࠱ࡨࡧࡣࡩࡧ࠱࡮ࡸࡵ࡮ࠨश"))
    if not os.path.isfile(file_path):
      with open(file_path, bstack11l1l11_opy_ (u"ࠧࡸࠩष")):
        pass
      with open(file_path, bstack11l1l11_opy_ (u"ࠣࡹ࠮ࠦस")) as outfile:
        json.dump({}, outfile)
    with open(file_path, bstack11l1l11_opy_ (u"ࠩࡵࠫह")) as bstack1lll11lll_opy_:
      bstack1l1l111l1l_opy_ = json.load(bstack1lll11lll_opy_)
    if bstack1111l1l1l_opy_ in bstack1l1l111l1l_opy_:
      bstack1l1llll1l_opy_ = bstack1l1l111l1l_opy_[bstack1111l1l1l_opy_][bstack11l1l11_opy_ (u"ࠪ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧऺ")]
      bstack1ll1llll_opy_ = int(bstack1l1llll1l_opy_) + 1
      bstack1l11l1lll1_opy_(bstack1111l1l1l_opy_, bstack1ll1llll_opy_, file_path)
      return bstack1ll1llll_opy_
    else:
      bstack1l11l1lll1_opy_(bstack1111l1l1l_opy_, 1, file_path)
      return 1
  except Exception as e:
    logger.warn(bstack1l111ll1_opy_.format(str(e)))
    return -1
def bstack1l1111l11_opy_(config):
  if not config[bstack11l1l11_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ऻ")] or not config[bstack11l1l11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ़")]:
    return True
  else:
    return False
def bstack111l1l1ll_opy_(config, index=0):
  global bstack11ll11l11l_opy_
  bstack11l11ll1_opy_ = {}
  caps = bstack1l1lll11ll_opy_ + bstack111l11lll_opy_
  if config.get(bstack11l1l11_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪऽ"), False):
    bstack11l11ll1_opy_[bstack11l1l11_opy_ (u"ࠧࡵࡷࡵࡦࡴࡹࡣࡢ࡮ࡨࠫा")] = True
    bstack11l11ll1_opy_[bstack11l1l11_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࡔࡶࡴࡪࡱࡱࡷࠬि")] = config.get(bstack11l1l11_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ी"), {})
  if bstack11ll11l11l_opy_:
    caps += bstack11ll11l1_opy_
  for key in config:
    if key in caps + [bstack11l1l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ु")]:
      continue
    bstack11l11ll1_opy_[key] = config[key]
  if bstack11l1l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧू") in config:
    for bstack1l111111l_opy_ in config[bstack11l1l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨृ")][index]:
      if bstack1l111111l_opy_ in caps:
        continue
      bstack11l11ll1_opy_[bstack1l111111l_opy_] = config[bstack11l1l11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩॄ")][index][bstack1l111111l_opy_]
  bstack11l11ll1_opy_[bstack11l1l11_opy_ (u"ࠧࡩࡱࡶࡸࡓࡧ࡭ࡦࠩॅ")] = socket.gethostname()
  if bstack11l1l11_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯ࠩॆ") in bstack11l11ll1_opy_:
    del (bstack11l11ll1_opy_[bstack11l1l11_opy_ (u"ࠩࡹࡩࡷࡹࡩࡰࡰࠪे")])
  return bstack11l11ll1_opy_
def bstack1lllllll11_opy_(config):
  global bstack11ll11l11l_opy_
  bstack1l1l1lll11_opy_ = {}
  caps = bstack111l11lll_opy_
  if bstack11ll11l11l_opy_:
    caps += bstack11ll11l1_opy_
  for key in caps:
    if key in config:
      bstack1l1l1lll11_opy_[key] = config[key]
  return bstack1l1l1lll11_opy_
def bstack1lll1l11l_opy_(bstack11l11ll1_opy_, bstack1l1l1lll11_opy_):
  bstack111lll11l_opy_ = {}
  for key in bstack11l11ll1_opy_.keys():
    if key in bstack111111l11_opy_:
      bstack111lll11l_opy_[bstack111111l11_opy_[key]] = bstack11l11ll1_opy_[key]
    else:
      bstack111lll11l_opy_[key] = bstack11l11ll1_opy_[key]
  for key in bstack1l1l1lll11_opy_:
    if key in bstack111111l11_opy_:
      bstack111lll11l_opy_[bstack111111l11_opy_[key]] = bstack1l1l1lll11_opy_[key]
    else:
      bstack111lll11l_opy_[key] = bstack1l1l1lll11_opy_[key]
  return bstack111lll11l_opy_
def bstack1lll111ll1_opy_(config, index=0):
  global bstack11ll11l11l_opy_
  caps = {}
  config = copy.deepcopy(config)
  bstack1llll1ll1_opy_ = bstack1ll1l11l_opy_(bstack1ll1l111_opy_, config, logger)
  bstack1l1l1lll11_opy_ = bstack1lllllll11_opy_(config)
  bstack1llllll11l_opy_ = bstack111l11lll_opy_
  bstack1llllll11l_opy_ += bstack1lll11111l_opy_
  bstack1l1l1lll11_opy_ = update(bstack1l1l1lll11_opy_, bstack1llll1ll1_opy_)
  if bstack11ll11l11l_opy_:
    bstack1llllll11l_opy_ += bstack11ll11l1_opy_
  if bstack11l1l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ै") in config:
    if bstack11l1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩॉ") in config[bstack11l1l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨॊ")][index]:
      caps[bstack11l1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫो")] = config[bstack11l1l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪौ")][index][bstack11l1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ्࠭")]
    if bstack11l1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪॎ") in config[bstack11l1l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ॏ")][index]:
      caps[bstack11l1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬॐ")] = str(config[bstack11l1l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ॑")][index][bstack11l1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴ॒ࠧ")])
    bstack1ll1l1111_opy_ = bstack1ll1l11l_opy_(bstack1ll1l111_opy_, config[bstack11l1l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ॓")][index], logger)
    bstack1llllll11l_opy_ += list(bstack1ll1l1111_opy_.keys())
    for bstack1lllll1l1_opy_ in bstack1llllll11l_opy_:
      if bstack1lllll1l1_opy_ in config[bstack11l1l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ॔")][index]:
        if bstack1lllll1l1_opy_ == bstack11l1l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠫॕ"):
          try:
            bstack1ll1l1111_opy_[bstack1lllll1l1_opy_] = str(config[bstack11l1l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ॖ")][index][bstack1lllll1l1_opy_] * 1.0)
          except:
            bstack1ll1l1111_opy_[bstack1lllll1l1_opy_] = str(config[bstack11l1l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧॗ")][index][bstack1lllll1l1_opy_])
        else:
          bstack1ll1l1111_opy_[bstack1lllll1l1_opy_] = config[bstack11l1l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨक़")][index][bstack1lllll1l1_opy_]
        del (config[bstack11l1l11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩख़")][index][bstack1lllll1l1_opy_])
    bstack1l1l1lll11_opy_ = update(bstack1l1l1lll11_opy_, bstack1ll1l1111_opy_)
  bstack11l11ll1_opy_ = bstack111l1l1ll_opy_(config, index)
  for bstack1ll1lll1l_opy_ in bstack111l11lll_opy_ + list(bstack1llll1ll1_opy_.keys()):
    if bstack1ll1lll1l_opy_ in bstack11l11ll1_opy_:
      bstack1l1l1lll11_opy_[bstack1ll1lll1l_opy_] = bstack11l11ll1_opy_[bstack1ll1lll1l_opy_]
      del (bstack11l11ll1_opy_[bstack1ll1lll1l_opy_])
  if bstack11l1l1l11l_opy_(config):
    bstack11l11ll1_opy_[bstack11l1l11_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧग़")] = True
    caps.update(bstack1l1l1lll11_opy_)
    caps[bstack11l1l11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩज़")] = bstack11l11ll1_opy_
  else:
    bstack11l11ll1_opy_[bstack11l1l11_opy_ (u"ࠩࡸࡷࡪ࡝࠳ࡄࠩड़")] = False
    caps.update(bstack1lll1l11l_opy_(bstack11l11ll1_opy_, bstack1l1l1lll11_opy_))
    if bstack11l1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨढ़") in caps:
      caps[bstack11l1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬफ़")] = caps[bstack11l1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪय़")]
      del (caps[bstack11l1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫॠ")])
    if bstack11l1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨॡ") in caps:
      caps[bstack11l1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪॢ")] = caps[bstack11l1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪॣ")]
      del (caps[bstack11l1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫ।")])
  return caps
def bstack11111l1l_opy_():
  global bstack1111l1l1_opy_
  global CONFIG
  if bstack1ll1lllll_opy_() <= version.parse(bstack11l1l11_opy_ (u"ࠫ࠸࠴࠱࠴࠰࠳ࠫ॥")):
    if bstack1111l1l1_opy_ != bstack11l1l11_opy_ (u"ࠬ࠭०"):
      return bstack11l1l11_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢ१") + bstack1111l1l1_opy_ + bstack11l1l11_opy_ (u"ࠢ࠻࠺࠳࠳ࡼࡪ࠯ࡩࡷࡥࠦ२")
    return bstack11ll1ll1l1_opy_
  if bstack1111l1l1_opy_ != bstack11l1l11_opy_ (u"ࠨࠩ३"):
    return bstack11l1l11_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࠦ४") + bstack1111l1l1_opy_ + bstack11l1l11_opy_ (u"ࠥ࠳ࡼࡪ࠯ࡩࡷࡥࠦ५")
  return bstack11ll1ll11_opy_
def bstack11l1lll11_opy_(options):
  return hasattr(options, bstack11l1l11_opy_ (u"ࠫࡸ࡫ࡴࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷࡽࠬ६"))
def update(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = update(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d
def bstack1ll11111_opy_(options, bstack1l11l11ll1_opy_):
  for bstack1l111l11ll_opy_ in bstack1l11l11ll1_opy_:
    if bstack1l111l11ll_opy_ in [bstack11l1l11_opy_ (u"ࠬࡧࡲࡨࡵࠪ७"), bstack11l1l11_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪ८")]:
      continue
    if bstack1l111l11ll_opy_ in options._experimental_options:
      options._experimental_options[bstack1l111l11ll_opy_] = update(options._experimental_options[bstack1l111l11ll_opy_],
                                                         bstack1l11l11ll1_opy_[bstack1l111l11ll_opy_])
    else:
      options.add_experimental_option(bstack1l111l11ll_opy_, bstack1l11l11ll1_opy_[bstack1l111l11ll_opy_])
  if bstack11l1l11_opy_ (u"ࠧࡢࡴࡪࡷࠬ९") in bstack1l11l11ll1_opy_:
    for arg in bstack1l11l11ll1_opy_[bstack11l1l11_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭॰")]:
      options.add_argument(arg)
    del (bstack1l11l11ll1_opy_[bstack11l1l11_opy_ (u"ࠩࡤࡶ࡬ࡹࠧॱ")])
  if bstack11l1l11_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧॲ") in bstack1l11l11ll1_opy_:
    for ext in bstack1l11l11ll1_opy_[bstack11l1l11_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨॳ")]:
      try:
        options.add_extension(ext)
      except OSError:
        options.add_encoded_extension(ext)
    del (bstack1l11l11ll1_opy_[bstack11l1l11_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩॴ")])
def bstack11l11lll11_opy_(options, bstack1llll1lll_opy_):
  if bstack11l1l11_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬॵ") in bstack1llll1lll_opy_:
    for bstack11ll1l1l1l_opy_ in bstack1llll1lll_opy_[bstack11l1l11_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭ॶ")]:
      if bstack11ll1l1l1l_opy_ in options._preferences:
        options._preferences[bstack11ll1l1l1l_opy_] = update(options._preferences[bstack11ll1l1l1l_opy_], bstack1llll1lll_opy_[bstack11l1l11_opy_ (u"ࠨࡲࡵࡩ࡫ࡹࠧॷ")][bstack11ll1l1l1l_opy_])
      else:
        options.set_preference(bstack11ll1l1l1l_opy_, bstack1llll1lll_opy_[bstack11l1l11_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨॸ")][bstack11ll1l1l1l_opy_])
  if bstack11l1l11_opy_ (u"ࠪࡥࡷ࡭ࡳࠨॹ") in bstack1llll1lll_opy_:
    for arg in bstack1llll1lll_opy_[bstack11l1l11_opy_ (u"ࠫࡦࡸࡧࡴࠩॺ")]:
      options.add_argument(arg)
def bstack1ll1ll11l_opy_(options, bstack11lllll111_opy_):
  if bstack11l1l11_opy_ (u"ࠬࡽࡥࡣࡸ࡬ࡩࡼ࠭ॻ") in bstack11lllll111_opy_:
    options.use_webview(bool(bstack11lllll111_opy_[bstack11l1l11_opy_ (u"࠭ࡷࡦࡤࡹ࡭ࡪࡽࠧॼ")]))
  bstack1ll11111_opy_(options, bstack11lllll111_opy_)
def bstack1lll11ll1_opy_(options, bstack1llll1111l_opy_):
  for bstack111llll11_opy_ in bstack1llll1111l_opy_:
    if bstack111llll11_opy_ in [bstack11l1l11_opy_ (u"ࠧࡵࡧࡦ࡬ࡳࡵ࡬ࡰࡩࡼࡔࡷ࡫ࡶࡪࡧࡺࠫॽ"), bstack11l1l11_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ॾ")]:
      continue
    options.set_capability(bstack111llll11_opy_, bstack1llll1111l_opy_[bstack111llll11_opy_])
  if bstack11l1l11_opy_ (u"ࠩࡤࡶ࡬ࡹࠧॿ") in bstack1llll1111l_opy_:
    for arg in bstack1llll1111l_opy_[bstack11l1l11_opy_ (u"ࠪࡥࡷ࡭ࡳࠨঀ")]:
      options.add_argument(arg)
  if bstack11l1l11_opy_ (u"ࠫࡹ࡫ࡣࡩࡰࡲࡰࡴ࡭ࡹࡑࡴࡨࡺ࡮࡫ࡷࠨঁ") in bstack1llll1111l_opy_:
    options.bstack1111l11l_opy_(bool(bstack1llll1111l_opy_[bstack11l1l11_opy_ (u"ࠬࡺࡥࡤࡪࡱࡳࡱࡵࡧࡺࡒࡵࡩࡻ࡯ࡥࡸࠩং")]))
def bstack11llllllll_opy_(options, bstack1ll1l11lll_opy_):
  for bstack11lll1l1ll_opy_ in bstack1ll1l11lll_opy_:
    if bstack11lll1l1ll_opy_ in [bstack11l1l11_opy_ (u"࠭ࡡࡥࡦ࡬ࡸ࡮ࡵ࡮ࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪঃ"), bstack11l1l11_opy_ (u"ࠧࡢࡴࡪࡷࠬ঄")]:
      continue
    options._options[bstack11lll1l1ll_opy_] = bstack1ll1l11lll_opy_[bstack11lll1l1ll_opy_]
  if bstack11l1l11_opy_ (u"ࠨࡣࡧࡨ࡮ࡺࡩࡰࡰࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬঅ") in bstack1ll1l11lll_opy_:
    for bstack11111111_opy_ in bstack1ll1l11lll_opy_[bstack11l1l11_opy_ (u"ࠩࡤࡨࡩ࡯ࡴࡪࡱࡱࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭আ")]:
      options.bstack1llll1l111_opy_(
        bstack11111111_opy_, bstack1ll1l11lll_opy_[bstack11l1l11_opy_ (u"ࠪࡥࡩࡪࡩࡵ࡫ࡲࡲࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧই")][bstack11111111_opy_])
  if bstack11l1l11_opy_ (u"ࠫࡦࡸࡧࡴࠩঈ") in bstack1ll1l11lll_opy_:
    for arg in bstack1ll1l11lll_opy_[bstack11l1l11_opy_ (u"ࠬࡧࡲࡨࡵࠪউ")]:
      options.add_argument(arg)
def bstack1l1ll11lll_opy_(options, caps):
  if not hasattr(options, bstack11l1l11_opy_ (u"࠭ࡋࡆ࡛ࠪঊ")):
    return
  if options.KEY == bstack11l1l11_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬঋ") and options.KEY in caps:
    bstack1ll11111_opy_(options, caps[bstack11l1l11_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ঌ")])
  elif options.KEY == bstack11l1l11_opy_ (u"ࠩࡰࡳࡿࡀࡦࡪࡴࡨࡪࡴࡾࡏࡱࡶ࡬ࡳࡳࡹࠧ঍") and options.KEY in caps:
    bstack11l11lll11_opy_(options, caps[bstack11l1l11_opy_ (u"ࠪࡱࡴࢀ࠺ࡧ࡫ࡵࡩ࡫ࡵࡸࡐࡲࡷ࡭ࡴࡴࡳࠨ঎")])
  elif options.KEY == bstack11l1l11_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬࠲ࡴࡶࡴࡪࡱࡱࡷࠬএ") and options.KEY in caps:
    bstack1lll11ll1_opy_(options, caps[bstack11l1l11_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭࠳ࡵࡰࡵ࡫ࡲࡲࡸ࠭ঐ")])
  elif options.KEY == bstack11l1l11_opy_ (u"࠭࡭ࡴ࠼ࡨࡨ࡬࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ঑") and options.KEY in caps:
    bstack1ll1ll11l_opy_(options, caps[bstack11l1l11_opy_ (u"ࠧ࡮ࡵ࠽ࡩࡩ࡭ࡥࡐࡲࡷ࡭ࡴࡴࡳࠨ঒")])
  elif options.KEY == bstack11l1l11_opy_ (u"ࠨࡵࡨ࠾࡮࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧও") and options.KEY in caps:
    bstack11llllllll_opy_(options, caps[bstack11l1l11_opy_ (u"ࠩࡶࡩ࠿࡯ࡥࡐࡲࡷ࡭ࡴࡴࡳࠨঔ")])
def bstack1l11111l11_opy_(caps):
  global bstack11ll11l11l_opy_
  if isinstance(os.environ.get(bstack11l1l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫক")), str):
    bstack11ll11l11l_opy_ = eval(os.getenv(bstack11l1l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬখ")))
  if bstack11ll11l11l_opy_:
    if bstack1l1l111l_opy_() < version.parse(bstack11l1l11_opy_ (u"ࠬ࠸࠮࠴࠰࠳ࠫগ")):
      return None
    else:
      from appium.options.common.base import AppiumOptions
      options = AppiumOptions().load_capabilities(caps)
      return options
  else:
    browser = bstack11l1l11_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ࠭ঘ")
    if bstack11l1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬঙ") in caps:
      browser = caps[bstack11l1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭চ")]
    elif bstack11l1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪছ") in caps:
      browser = caps[bstack11l1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࠫজ")]
    browser = str(browser).lower()
    if browser == bstack11l1l11_opy_ (u"ࠫ࡮ࡶࡨࡰࡰࡨࠫঝ") or browser == bstack11l1l11_opy_ (u"ࠬ࡯ࡰࡢࡦࠪঞ"):
      browser = bstack11l1l11_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮࠭ট")
    if browser == bstack11l1l11_opy_ (u"ࠧࡴࡣࡰࡷࡺࡴࡧࠨঠ"):
      browser = bstack11l1l11_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࠨড")
    if browser not in [bstack11l1l11_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࠩঢ"), bstack11l1l11_opy_ (u"ࠪࡩࡩ࡭ࡥࠨণ"), bstack11l1l11_opy_ (u"ࠫ࡮࡫ࠧত"), bstack11l1l11_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭ࠬথ"), bstack11l1l11_opy_ (u"࠭ࡦࡪࡴࡨࡪࡴࡾࠧদ")]:
      return None
    try:
      package = bstack11l1l11_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮࠰ࡺࡩࡧࡪࡲࡪࡸࡨࡶ࠳ࢁࡽ࠯ࡱࡳࡸ࡮ࡵ࡮ࡴࠩধ").format(browser)
      name = bstack11l1l11_opy_ (u"ࠨࡑࡳࡸ࡮ࡵ࡮ࡴࠩন")
      browser_options = getattr(__import__(package, fromlist=[name]), name)
      options = browser_options()
      if not bstack11l1lll11_opy_(options):
        return None
      for bstack1ll1lll1l_opy_ in caps.keys():
        options.set_capability(bstack1ll1lll1l_opy_, caps[bstack1ll1lll1l_opy_])
      bstack1l1ll11lll_opy_(options, caps)
      return options
    except Exception as e:
      logger.debug(str(e))
      return None
def bstack11l11ll1ll_opy_(options, bstack11lllll11l_opy_):
  if not bstack11l1lll11_opy_(options):
    return
  for bstack1ll1lll1l_opy_ in bstack11lllll11l_opy_.keys():
    if bstack1ll1lll1l_opy_ in bstack1lll11111l_opy_:
      continue
    if bstack1ll1lll1l_opy_ in options._caps and type(options._caps[bstack1ll1lll1l_opy_]) in [dict, list]:
      options._caps[bstack1ll1lll1l_opy_] = update(options._caps[bstack1ll1lll1l_opy_], bstack11lllll11l_opy_[bstack1ll1lll1l_opy_])
    else:
      options.set_capability(bstack1ll1lll1l_opy_, bstack11lllll11l_opy_[bstack1ll1lll1l_opy_])
  bstack1l1ll11lll_opy_(options, bstack11lllll11l_opy_)
  if bstack11l1l11_opy_ (u"ࠩࡰࡳࡿࡀࡤࡦࡤࡸ࡫࡬࡫ࡲࡂࡦࡧࡶࡪࡹࡳࠨ঩") in options._caps:
    if options._caps[bstack11l1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨপ")] and options._caps[bstack11l1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩফ")].lower() != bstack11l1l11_opy_ (u"ࠬ࡬ࡩࡳࡧࡩࡳࡽ࠭ব"):
      del options._caps[bstack11l1l11_opy_ (u"࠭࡭ࡰࡼ࠽ࡨࡪࡨࡵࡨࡩࡨࡶࡆࡪࡤࡳࡧࡶࡷࠬভ")]
def bstack1l1l1ll11_opy_(proxy_config):
  if bstack11l1l11_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫম") in proxy_config:
    proxy_config[bstack11l1l11_opy_ (u"ࠨࡵࡶࡰࡕࡸ࡯ࡹࡻࠪয")] = proxy_config[bstack11l1l11_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭র")]
    del (proxy_config[bstack11l1l11_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧ঱")])
  if bstack11l1l11_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡗࡽࡵ࡫ࠧল") in proxy_config and proxy_config[bstack11l1l11_opy_ (u"ࠬࡶࡲࡰࡺࡼࡘࡾࡶࡥࠨ঳")].lower() != bstack11l1l11_opy_ (u"࠭ࡤࡪࡴࡨࡧࡹ࠭঴"):
    proxy_config[bstack11l1l11_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡚ࡹࡱࡧࠪ঵")] = bstack11l1l11_opy_ (u"ࠨ࡯ࡤࡲࡺࡧ࡬ࠨশ")
  if bstack11l1l11_opy_ (u"ࠩࡳࡶࡴࡾࡹࡂࡷࡷࡳࡨࡵ࡮ࡧ࡫ࡪ࡙ࡷࡲࠧষ") in proxy_config:
    proxy_config[bstack11l1l11_opy_ (u"ࠪࡴࡷࡵࡸࡺࡖࡼࡴࡪ࠭স")] = bstack11l1l11_opy_ (u"ࠫࡵࡧࡣࠨহ")
  return proxy_config
def bstack1l11l1ll1l_opy_(config, proxy):
  from selenium.webdriver.common.proxy import Proxy
  if not bstack11l1l11_opy_ (u"ࠬࡶࡲࡰࡺࡼࠫ঺") in config:
    return proxy
  config[bstack11l1l11_opy_ (u"࠭ࡰࡳࡱࡻࡽࠬ঻")] = bstack1l1l1ll11_opy_(config[bstack11l1l11_opy_ (u"ࠧࡱࡴࡲࡼࡾ়࠭")])
  if proxy == None:
    proxy = Proxy(config[bstack11l1l11_opy_ (u"ࠨࡲࡵࡳࡽࡿࠧঽ")])
  return proxy
def bstack1l1ll1111_opy_(self):
  global CONFIG
  global bstack1ll111l1_opy_
  try:
    proxy = bstack11ll1l1l1_opy_(CONFIG)
    if proxy:
      if proxy.endswith(bstack11l1l11_opy_ (u"ࠩ࠱ࡴࡦࡩࠧা")):
        proxies = bstack11llll1l_opy_(proxy, bstack11111l1l_opy_())
        if len(proxies) > 0:
          protocol, bstack1l111111ll_opy_ = proxies.popitem()
          if bstack11l1l11_opy_ (u"ࠥ࠾࠴࠵ࠢি") in bstack1l111111ll_opy_:
            return bstack1l111111ll_opy_
          else:
            return bstack11l1l11_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࠧী") + bstack1l111111ll_opy_
      else:
        return proxy
  except Exception as e:
    logger.error(bstack11l1l11_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡲࡵࡳࡽࡿࠠࡶࡴ࡯ࠤ࠿ࠦࡻࡾࠤু").format(str(e)))
  return bstack1ll111l1_opy_(self)
def bstack11ll111l1_opy_():
  global CONFIG
  return bstack1l1ll1ll11_opy_(CONFIG) and bstack1lll1l1ll1_opy_() and bstack1ll1lllll_opy_() >= version.parse(bstack11lllll11_opy_)
def bstack1l11l1l1ll_opy_():
  global CONFIG
  return (bstack11l1l11_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩূ") in CONFIG or bstack11l1l11_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫৃ") in CONFIG) and bstack1l1l111ll_opy_()
def bstack1l1ll1111l_opy_(config):
  bstack11l11llll_opy_ = {}
  if bstack11l1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬৄ") in config:
    bstack11l11llll_opy_ = config[bstack11l1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭৅")]
  if bstack11l1l11_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩ৆") in config:
    bstack11l11llll_opy_ = config[bstack11l1l11_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪে")]
  proxy = bstack11ll1l1l1_opy_(config)
  if proxy:
    if proxy.endswith(bstack11l1l11_opy_ (u"ࠬ࠴ࡰࡢࡥࠪৈ")) and os.path.isfile(proxy):
      bstack11l11llll_opy_[bstack11l1l11_opy_ (u"࠭࠭ࡱࡣࡦ࠱࡫࡯࡬ࡦࠩ৉")] = proxy
    else:
      parsed_url = None
      if proxy.endswith(bstack11l1l11_opy_ (u"ࠧ࠯ࡲࡤࡧࠬ৊")):
        proxies = bstack1ll11lll1_opy_(config, bstack11111l1l_opy_())
        if len(proxies) > 0:
          protocol, bstack1l111111ll_opy_ = proxies.popitem()
          if bstack11l1l11_opy_ (u"ࠣ࠼࠲࠳ࠧো") in bstack1l111111ll_opy_:
            parsed_url = urlparse(bstack1l111111ll_opy_)
          else:
            parsed_url = urlparse(protocol + bstack11l1l11_opy_ (u"ࠤ࠽࠳࠴ࠨৌ") + bstack1l111111ll_opy_)
      else:
        parsed_url = urlparse(proxy)
      if parsed_url and parsed_url.hostname: bstack11l11llll_opy_[bstack11l1l11_opy_ (u"ࠪࡴࡷࡵࡸࡺࡊࡲࡷࡹ্࠭")] = str(parsed_url.hostname)
      if parsed_url and parsed_url.port: bstack11l11llll_opy_[bstack11l1l11_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡓࡳࡷࡺࠧৎ")] = str(parsed_url.port)
      if parsed_url and parsed_url.username: bstack11l11llll_opy_[bstack11l1l11_opy_ (u"ࠬࡶࡲࡰࡺࡼ࡙ࡸ࡫ࡲࠨ৏")] = str(parsed_url.username)
      if parsed_url and parsed_url.password: bstack11l11llll_opy_[bstack11l1l11_opy_ (u"࠭ࡰࡳࡱࡻࡽࡕࡧࡳࡴࠩ৐")] = str(parsed_url.password)
  return bstack11l11llll_opy_
def bstack1lll1lll11_opy_(config):
  if bstack11l1l11_opy_ (u"ࠧࡵࡧࡶࡸࡈࡵ࡮ࡵࡧࡻࡸࡔࡶࡴࡪࡱࡱࡷࠬ৑") in config:
    return config[bstack11l1l11_opy_ (u"ࠨࡶࡨࡷࡹࡉ࡯࡯ࡶࡨࡼࡹࡕࡰࡵ࡫ࡲࡲࡸ࠭৒")]
  return {}
def bstack1ll11l1l1l_opy_(caps):
  global bstack11l1ll1l1_opy_
  if bstack11l1l11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪ৓") in caps:
    caps[bstack11l1l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫ৔")][bstack11l1l11_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࠪ৕")] = True
    if bstack11l1ll1l1_opy_:
      caps[bstack11l1l11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭৖")][bstack11l1l11_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨৗ")] = bstack11l1ll1l1_opy_
  else:
    caps[bstack11l1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡬ࡰࡥࡤࡰࠬ৘")] = True
    if bstack11l1ll1l1_opy_:
      caps[bstack11l1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ৙")] = bstack11l1ll1l1_opy_
@measure(event_name=EVENTS.bstack1l11111ll_opy_, stage=STAGE.bstack1l1ll1lll_opy_, bstack11ll11ll11_opy_=bstack11l1l1lll_opy_)
def bstack1ll11ll11l_opy_():
  global CONFIG
  if not bstack1l1l1ll11l_opy_(CONFIG) or cli.is_enabled(CONFIG):
    return
  if bstack11l1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭৚") in CONFIG and bstack1ll11l1l1_opy_(CONFIG[bstack11l1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ৛")]):
    if (
      bstack11l1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨড়") in CONFIG
      and bstack1ll11l1l1_opy_(CONFIG[bstack11l1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩঢ়")].get(bstack11l1l11_opy_ (u"࠭ࡳ࡬࡫ࡳࡆ࡮ࡴࡡࡳࡻࡌࡲ࡮ࡺࡩࡢ࡮࡬ࡷࡦࡺࡩࡰࡰࠪ৞")))
    ):
      logger.debug(bstack11l1l11_opy_ (u"ࠢࡍࡱࡦࡥࡱࠦࡢࡪࡰࡤࡶࡾࠦ࡮ࡰࡶࠣࡷࡹࡧࡲࡵࡧࡧࠤࡦࡹࠠࡴ࡭࡬ࡴࡇ࡯࡮ࡢࡴࡼࡍࡳ࡯ࡴࡪࡣ࡯࡭ࡸࡧࡴࡪࡱࡱࠤ࡮ࡹࠠࡦࡰࡤࡦࡱ࡫ࡤࠣয়"))
      return
    bstack11l11llll_opy_ = bstack1l1ll1111l_opy_(CONFIG)
    bstack11lllllll1_opy_(CONFIG[bstack11l1l11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫৠ")], bstack11l11llll_opy_)
def bstack11lllllll1_opy_(key, bstack11l11llll_opy_):
  global bstack1ll1l11l11_opy_
  logger.info(bstack1ll1l1l1_opy_)
  try:
    bstack1ll1l11l11_opy_ = Local()
    bstack1ll1ll11l1_opy_ = {bstack11l1l11_opy_ (u"ࠩ࡮ࡩࡾ࠭ৡ"): key}
    bstack1ll1ll11l1_opy_.update(bstack11l11llll_opy_)
    logger.debug(bstack1ll11l1lll_opy_.format(str(bstack1ll1ll11l1_opy_)).replace(key, bstack11l1l11_opy_ (u"ࠪ࡟ࡗࡋࡄࡂࡅࡗࡉࡉࡣࠧৢ")))
    bstack1ll1l11l11_opy_.start(**bstack1ll1ll11l1_opy_)
    if bstack1ll1l11l11_opy_.isRunning():
      logger.info(bstack1ll111llll_opy_)
  except Exception as e:
    bstack11111l1ll_opy_(bstack1ll1ll1l11_opy_.format(str(e)))
def bstack11l1l11lll_opy_():
  global bstack1ll1l11l11_opy_
  if bstack1ll1l11l11_opy_.isRunning():
    logger.info(bstack1l1l1111l_opy_)
    bstack1ll1l11l11_opy_.stop()
  bstack1ll1l11l11_opy_ = None
def bstack111l1lll_opy_(bstack11ll1l1ll1_opy_=[]):
  global CONFIG
  bstack11llll1l1l_opy_ = []
  bstack1l11l1ll_opy_ = [bstack11l1l11_opy_ (u"ࠫࡴࡹࠧৣ"), bstack11l1l11_opy_ (u"ࠬࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠨ৤"), bstack11l1l11_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪ৥"), bstack11l1l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩ০"), bstack11l1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭১"), bstack11l1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪ২")]
  try:
    for err in bstack11ll1l1ll1_opy_:
      bstack11l1l1111_opy_ = {}
      for k in bstack1l11l1ll_opy_:
        val = CONFIG[bstack11l1l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭৩")][int(err[bstack11l1l11_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪ৪")])].get(k)
        if val:
          bstack11l1l1111_opy_[k] = val
      if(err[bstack11l1l11_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫ৫")] != bstack11l1l11_opy_ (u"࠭ࠧ৬")):
        bstack11l1l1111_opy_[bstack11l1l11_opy_ (u"ࠧࡵࡧࡶࡸࡸ࠭৭")] = {
          err[bstack11l1l11_opy_ (u"ࠨࡰࡤࡱࡪ࠭৮")]: err[bstack11l1l11_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ৯")]
        }
        bstack11llll1l1l_opy_.append(bstack11l1l1111_opy_)
  except Exception as e:
    logger.debug(bstack11l1l11_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥ࡬࡯ࡳ࡯ࡤࡸࡹ࡯࡮ࡨࠢࡧࡥࡹࡧࠠࡧࡱࡵࠤࡪࡼࡥ࡯ࡶ࠽ࠤࠬৰ") + str(e))
  finally:
    return bstack11llll1l1l_opy_
def bstack1l11ll111_opy_(file_name):
  bstack1ll1l11l1l_opy_ = []
  try:
    bstack1l1111ll_opy_ = os.path.join(tempfile.gettempdir(), file_name)
    if os.path.exists(bstack1l1111ll_opy_):
      with open(bstack1l1111ll_opy_) as f:
        bstack1llllll11_opy_ = json.load(f)
        bstack1ll1l11l1l_opy_ = bstack1llllll11_opy_
      os.remove(bstack1l1111ll_opy_)
    return bstack1ll1l11l1l_opy_
  except Exception as e:
    logger.debug(bstack11l1l11_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡦࡪࡰࡧ࡭ࡳ࡭ࠠࡦࡴࡵࡳࡷࠦ࡬ࡪࡵࡷ࠾ࠥ࠭ৱ") + str(e))
    return bstack1ll1l11l1l_opy_
def bstack1l1ll111l1_opy_():
  try:
      from bstack_utils.constants import bstack1lll111ll_opy_, EVENTS
      from bstack_utils.helper import bstack111ll11ll_opy_, get_host_info, bstack111ll1lll_opy_
      from datetime import datetime
      from filelock import FileLock
      bstack1llll111l1_opy_ = os.path.join(os.getcwd(), bstack11l1l11_opy_ (u"ࠬࡲ࡯ࡨࠩ৲"), bstack11l1l11_opy_ (u"࠭࡫ࡦࡻ࠰ࡱࡪࡺࡲࡪࡥࡶ࠲࡯ࡹ࡯࡯ࠩ৳"))
      lock = FileLock(bstack1llll111l1_opy_+bstack11l1l11_opy_ (u"ࠢ࠯࡮ࡲࡧࡰࠨ৴"))
      def bstack1ll1l1l1ll_opy_():
          try:
              with lock:
                  with open(bstack1llll111l1_opy_, bstack11l1l11_opy_ (u"ࠣࡴࠥ৵"), encoding=bstack11l1l11_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣ৶")) as file:
                      data = json.load(file)
                      config = {
                          bstack11l1l11_opy_ (u"ࠥ࡬ࡪࡧࡤࡦࡴࡶࠦ৷"): {
                              bstack11l1l11_opy_ (u"ࠦࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠥ৸"): bstack11l1l11_opy_ (u"ࠧࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠣ৹"),
                          }
                      }
                      bstack1lllllll1l_opy_ = datetime.utcnow()
                      bstack1ll11ll11_opy_ = bstack1lllllll1l_opy_.strftime(bstack11l1l11_opy_ (u"ࠨ࡚ࠥ࠯ࠨࡱ࠲ࠫࡤࡕࠧࡋ࠾ࠪࡓ࠺ࠦࡕ࠱ࠩ࡫ࠦࡕࡕࡅࠥ৺"))
                      bstack1l1l1ll1l_opy_ = os.environ.get(bstack11l1l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬ৻")) if os.environ.get(bstack11l1l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭ৼ")) else bstack111ll1lll_opy_.get_property(bstack11l1l11_opy_ (u"ࠤࡶࡨࡰࡘࡵ࡯ࡋࡧࠦ৽"))
                      payload = {
                          bstack11l1l11_opy_ (u"ࠥࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠢ৾"): bstack11l1l11_opy_ (u"ࠦࡸࡪ࡫ࡠࡧࡹࡩࡳࡺࡳࠣ৿"),
                          bstack11l1l11_opy_ (u"ࠧࡪࡡࡵࡣࠥ਀"): {
                              bstack11l1l11_opy_ (u"ࠨࡴࡦࡵࡷ࡬ࡺࡨ࡟ࡶࡷ࡬ࡨࠧਁ"): bstack1l1l1ll1l_opy_,
                              bstack11l1l11_opy_ (u"ࠢࡤࡴࡨࡥࡹ࡫ࡤࡠࡦࡤࡽࠧਂ"): bstack1ll11ll11_opy_,
                              bstack11l1l11_opy_ (u"ࠣࡧࡹࡩࡳࡺ࡟࡯ࡣࡰࡩࠧਃ"): bstack11l1l11_opy_ (u"ࠤࡖࡈࡐࡌࡥࡢࡶࡸࡶࡪࡖࡥࡳࡨࡲࡶࡲࡧ࡮ࡤࡧࠥ਄"),
                              bstack11l1l11_opy_ (u"ࠥࡩࡻ࡫࡮ࡵࡡ࡭ࡷࡴࡴࠢਅ"): {
                                  bstack11l1l11_opy_ (u"ࠦࡲ࡫ࡡࡴࡷࡵࡩࡸࠨਆ"): data,
                                  bstack11l1l11_opy_ (u"ࠧࡹࡤ࡬ࡔࡸࡲࡎࡪࠢਇ"): bstack111ll1lll_opy_.get_property(bstack11l1l11_opy_ (u"ࠨࡳࡥ࡭ࡕࡹࡳࡏࡤࠣਈ"))
                              },
                              bstack11l1l11_opy_ (u"ࠢࡶࡵࡨࡶࡤࡪࡡࡵࡣࠥਉ"): bstack111ll1lll_opy_.get_property(bstack11l1l11_opy_ (u"ࠣࡷࡶࡩࡷࡔࡡ࡮ࡧࠥਊ")),
                              bstack11l1l11_opy_ (u"ࠤ࡫ࡳࡸࡺ࡟ࡪࡰࡩࡳࠧ਋"): get_host_info()
                          }
                      }
                      response = bstack111ll11ll_opy_(bstack11l1l11_opy_ (u"ࠥࡔࡔ࡙ࡔࠣ਌"), bstack1lll111ll_opy_, payload, config)
                      if(response.status_code >= 200 and response.status_code < 300):
                          logger.debug(bstack11l1l11_opy_ (u"ࠦࡉࡧࡴࡢࠢࡶࡩࡳࡺࠠࡴࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࡰࡾࠦࡴࡰࠢࡾࢁࠥࡽࡩࡵࡪࠣࡨࡦࡺࡡࠡࡽࢀࠦ਍").format(bstack1lll111ll_opy_, payload))
                      else:
                          logger.debug(bstack11l1l11_opy_ (u"ࠧࡘࡥࡲࡷࡨࡷࡹࠦࡦࡢ࡫࡯ࡩࡩࠦࡦࡰࡴࠣࡿࢂࠦࡷࡪࡶ࡫ࠤࡩࡧࡴࡢࠢࡾࢁࠧ਎").format(bstack1lll111ll_opy_, payload))
          except Exception as e:
              logger.debug(bstack11l1l11_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡳࡪࠠ࡬ࡧࡼࠤࡲ࡫ࡴࡳ࡫ࡦࡷࠥࡪࡡࡵࡣࠣࡻ࡮ࡺࡨࠡࡧࡵࡶࡴࡸࠠࡼࡿࠥਏ").format(e))
      bstack1ll1l1l1ll_opy_()
      bstack11lll11l11_opy_(bstack1llll111l1_opy_, logger)
  except:
    pass
def bstack1l111ll1l_opy_():
  global bstack1l1l111111_opy_
  global bstack1l11ll11l1_opy_
  global bstack1l1lll111_opy_
  global bstack11l1l1l1l1_opy_
  global bstack1l1lll1ll_opy_
  global bstack11llllll1_opy_
  global CONFIG
  bstack1lllll1111_opy_ = os.environ.get(bstack11l1l11_opy_ (u"ࠧࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࡢ࡙ࡘࡋࡄࠨਐ"))
  if bstack1lllll1111_opy_ in [bstack11l1l11_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ਑"), bstack11l1l11_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨ਒")]:
    bstack11l1ll11ll_opy_()
  percy.shutdown()
  if bstack1l1l111111_opy_:
    logger.warning(bstack1ll111lll1_opy_.format(str(bstack1l1l111111_opy_)))
  else:
    try:
      bstack1lll1111_opy_ = bstack1ll1l1llll_opy_(bstack11l1l11_opy_ (u"ࠪ࠲ࡧࡹࡴࡢࡥ࡮࠱ࡨࡵ࡮ࡧ࡫ࡪ࠲࡯ࡹ࡯࡯ࠩਓ"), logger)
      if bstack1lll1111_opy_.get(bstack11l1l11_opy_ (u"ࠫࡳࡻࡤࡨࡧࡢࡰࡴࡩࡡ࡭ࠩਔ")) and bstack1lll1111_opy_.get(bstack11l1l11_opy_ (u"ࠬࡴࡵࡥࡩࡨࡣࡱࡵࡣࡢ࡮ࠪਕ")).get(bstack11l1l11_opy_ (u"࠭ࡨࡰࡵࡷࡲࡦࡳࡥࠨਖ")):
        logger.warning(bstack1ll111lll1_opy_.format(str(bstack1lll1111_opy_[bstack11l1l11_opy_ (u"ࠧ࡯ࡷࡧ࡫ࡪࡥ࡬ࡰࡥࡤࡰࠬਗ")][bstack11l1l11_opy_ (u"ࠨࡪࡲࡷࡹࡴࡡ࡮ࡧࠪਘ")])))
    except Exception as e:
      logger.error(e)
  if cli.is_running():
    bstack11l11ll11l_opy_.invoke(bstack1llll111ll_opy_.bstack1ll11111ll_opy_)
  logger.info(bstack111l1lll1_opy_)
  global bstack1ll1l11l11_opy_
  if bstack1ll1l11l11_opy_:
    bstack11l1l11lll_opy_()
  try:
    for driver in bstack1l11ll11l1_opy_:
      driver.quit()
  except Exception as e:
    pass
  logger.info(bstack11ll11l11_opy_)
  if bstack11llllll1_opy_ == bstack11l1l11_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨਙ"):
    bstack1l1lll1ll_opy_ = bstack1l11ll111_opy_(bstack11l1l11_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࡡࡨࡶࡷࡵࡲࡠ࡮࡬ࡷࡹ࠴ࡪࡴࡱࡱࠫਚ"))
  if bstack11llllll1_opy_ == bstack11l1l11_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫਛ") and len(bstack11l1l1l1l1_opy_) == 0:
    bstack11l1l1l1l1_opy_ = bstack1l11ll111_opy_(bstack11l1l11_opy_ (u"ࠬࡶࡷࡠࡲࡼࡸࡪࡹࡴࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸ࠳ࡰࡳࡰࡰࠪਜ"))
    if len(bstack11l1l1l1l1_opy_) == 0:
      bstack11l1l1l1l1_opy_ = bstack1l11ll111_opy_(bstack11l1l11_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹࡥࡰࡱࡲࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺ࠮࡫ࡵࡲࡲࠬਝ"))
  bstack111ll111_opy_ = bstack11l1l11_opy_ (u"ࠧࠨਞ")
  if len(bstack1l1lll111_opy_) > 0:
    bstack111ll111_opy_ = bstack111l1lll_opy_(bstack1l1lll111_opy_)
  elif len(bstack11l1l1l1l1_opy_) > 0:
    bstack111ll111_opy_ = bstack111l1lll_opy_(bstack11l1l1l1l1_opy_)
  elif len(bstack1l1lll1ll_opy_) > 0:
    bstack111ll111_opy_ = bstack111l1lll_opy_(bstack1l1lll1ll_opy_)
  elif len(bstack11l1l1l1ll_opy_) > 0:
    bstack111ll111_opy_ = bstack111l1lll_opy_(bstack11l1l1l1ll_opy_)
  if bool(bstack111ll111_opy_):
    bstack111l11ll_opy_(bstack111ll111_opy_)
  else:
    bstack111l11ll_opy_()
  bstack11lll11l11_opy_(bstack1ll1l11ll1_opy_, logger)
  if bstack1lllll1111_opy_ not in [bstack11l1l11_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩਟ")]:
    bstack1l1ll111l1_opy_()
  bstack111ll1l11_opy_.bstack1lll1l1111_opy_(CONFIG)
  if len(bstack1l1lll1ll_opy_) > 0:
    sys.exit(len(bstack1l1lll1ll_opy_))
def bstack1ll1l1l111_opy_(bstack1ll1l111l_opy_, frame):
  global bstack111ll1lll_opy_
  logger.error(bstack1l11l11l1_opy_)
  bstack111ll1lll_opy_.bstack11l111l1_opy_(bstack11l1l11_opy_ (u"ࠩࡶࡨࡰࡑࡩ࡭࡮ࡑࡳࠬਠ"), bstack1ll1l111l_opy_)
  if hasattr(signal, bstack11l1l11_opy_ (u"ࠪࡗ࡮࡭࡮ࡢ࡮ࡶࠫਡ")):
    bstack111ll1lll_opy_.bstack11l111l1_opy_(bstack11l1l11_opy_ (u"ࠫࡸࡪ࡫ࡌ࡫࡯ࡰࡘ࡯ࡧ࡯ࡣ࡯ࠫਢ"), signal.Signals(bstack1ll1l111l_opy_).name)
  else:
    bstack111ll1lll_opy_.bstack11l111l1_opy_(bstack11l1l11_opy_ (u"ࠬࡹࡤ࡬ࡍ࡬ࡰࡱ࡙ࡩࡨࡰࡤࡰࠬਣ"), bstack11l1l11_opy_ (u"࠭ࡓࡊࡉࡘࡒࡐࡔࡏࡘࡐࠪਤ"))
  if cli.is_running():
    bstack11l11ll11l_opy_.invoke(bstack1llll111ll_opy_.bstack1ll11111ll_opy_)
  bstack1lllll1111_opy_ = os.environ.get(bstack11l1l11_opy_ (u"ࠧࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࡢ࡙ࡘࡋࡄࠨਥ"))
  if bstack1lllll1111_opy_ == bstack11l1l11_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨਦ") and not cli.is_enabled(CONFIG):
    bstack11lll111l1_opy_.stop(bstack111ll1lll_opy_.get_property(bstack11l1l11_opy_ (u"ࠩࡶࡨࡰࡑࡩ࡭࡮ࡖ࡭࡬ࡴࡡ࡭ࠩਧ")))
  bstack1l111ll1l_opy_()
  sys.exit(1)
def bstack11111l1ll_opy_(err):
  logger.critical(bstack11lll1llll_opy_.format(str(err)))
  bstack111l11ll_opy_(bstack11lll1llll_opy_.format(str(err)), True)
  atexit.unregister(bstack1l111ll1l_opy_)
  bstack11l1ll11ll_opy_()
  sys.exit(1)
def bstack11lll1ll1l_opy_(error, message):
  logger.critical(str(error))
  logger.critical(message)
  bstack111l11ll_opy_(message, True)
  atexit.unregister(bstack1l111ll1l_opy_)
  bstack11l1ll11ll_opy_()
  sys.exit(1)
def bstack1111l11ll_opy_():
  global CONFIG
  global bstack11lllll1l1_opy_
  global bstack1ll111111l_opy_
  global bstack1l111ll111_opy_
  CONFIG = bstack11l1l1l11_opy_()
  load_dotenv(CONFIG.get(bstack11l1l11_opy_ (u"ࠪࡩࡳࡼࡆࡪ࡮ࡨࠫਨ")))
  bstack11ll1l1ll_opy_()
  bstack1l11l11111_opy_()
  CONFIG = bstack1l1lll11l_opy_(CONFIG)
  update(CONFIG, bstack1ll111111l_opy_)
  update(CONFIG, bstack11lllll1l1_opy_)
  if not cli.is_enabled(CONFIG):
    CONFIG = bstack11l1l11ll1_opy_(CONFIG)
  bstack1l111ll111_opy_ = bstack1l1l1ll11l_opy_(CONFIG)
  os.environ[bstack11l1l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠧ਩")] = bstack1l111ll111_opy_.__str__().lower()
  bstack111ll1lll_opy_.bstack11l111l1_opy_(bstack11l1l11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳ࠭ਪ"), bstack1l111ll111_opy_)
  if (bstack11l1l11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩਫ") in CONFIG and bstack11l1l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪਬ") in bstack11lllll1l1_opy_) or (
          bstack11l1l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫਭ") in CONFIG and bstack11l1l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬਮ") not in bstack1ll111111l_opy_):
    if os.getenv(bstack11l1l11_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡢࡇࡔࡓࡂࡊࡐࡈࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠧਯ")):
      CONFIG[bstack11l1l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ਰ")] = os.getenv(bstack11l1l11_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡤࡉࡏࡎࡄࡌࡒࡊࡊ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠩ਱"))
    else:
      if not CONFIG.get(bstack11l1l11_opy_ (u"ࠨࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠤਲ"), bstack11l1l11_opy_ (u"ࠢࠣਲ਼")) in bstack1l1111llll_opy_:
        bstack111l1l11_opy_()
  elif (bstack11l1l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ਴") not in CONFIG and bstack11l1l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫਵ") in CONFIG) or (
          bstack11l1l11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ਸ਼") in bstack1ll111111l_opy_ and bstack11l1l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ਷") not in bstack11lllll1l1_opy_):
    del (CONFIG[bstack11l1l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧਸ")])
  if bstack1l1111l11_opy_(CONFIG):
    bstack11111l1ll_opy_(bstack11lll11ll1_opy_)
  Config.bstack111l1l1l_opy_().bstack11l111l1_opy_(bstack11l1l11_opy_ (u"ࠨࡵࡴࡧࡵࡒࡦࡳࡥࠣਹ"), CONFIG[bstack11l1l11_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ਺")])
  bstack11l1l111l1_opy_()
  bstack11l11l1l1_opy_()
  if bstack11ll11l11l_opy_ and not CONFIG.get(bstack11l1l11_opy_ (u"ࠣࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠦ਻"), bstack11l1l11_opy_ (u"ࠤ਼ࠥ")) in bstack1l1111llll_opy_:
    CONFIG[bstack11l1l11_opy_ (u"ࠪࡥࡵࡶࠧ਽")] = bstack111lll1l_opy_(CONFIG)
    logger.info(bstack11ll1ll111_opy_.format(CONFIG[bstack11l1l11_opy_ (u"ࠫࡦࡶࡰࠨਾ")]))
  if not bstack1l111ll111_opy_:
    CONFIG[bstack11l1l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨਿ")] = [{}]
def bstack1lll11ll11_opy_(config, bstack1llll11111_opy_):
  global CONFIG
  global bstack11ll11l11l_opy_
  CONFIG = config
  bstack11ll11l11l_opy_ = bstack1llll11111_opy_
def bstack11l11l1l1_opy_():
  global CONFIG
  global bstack11ll11l11l_opy_
  if bstack11l1l11_opy_ (u"࠭ࡡࡱࡲࠪੀ") in CONFIG:
    try:
      from appium import version
    except Exception as e:
      bstack11lll1ll1l_opy_(e, bstack1l111ll1l1_opy_)
    bstack11ll11l11l_opy_ = True
    bstack111ll1lll_opy_.bstack11l111l1_opy_(bstack11l1l11_opy_ (u"ࠧࡢࡲࡳࡣࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭ੁ"), True)
def bstack111lll1l_opy_(config):
  bstack1ll1llll11_opy_ = bstack11l1l11_opy_ (u"ࠨࠩੂ")
  app = config[bstack11l1l11_opy_ (u"ࠩࡤࡴࡵ࠭੃")]
  if isinstance(app, str):
    if os.path.splitext(app)[1] in bstack11llll11l_opy_:
      if os.path.exists(app):
        bstack1ll1llll11_opy_ = bstack1ll1l1ll_opy_(config, app)
      elif bstack1lll11l1_opy_(app):
        bstack1ll1llll11_opy_ = app
      else:
        bstack11111l1ll_opy_(bstack1l1ll11l1_opy_.format(app))
    else:
      if bstack1lll11l1_opy_(app):
        bstack1ll1llll11_opy_ = app
      elif os.path.exists(app):
        bstack1ll1llll11_opy_ = bstack1ll1l1ll_opy_(app)
      else:
        bstack11111l1ll_opy_(bstack111llllll_opy_)
  else:
    if len(app) > 2:
      bstack11111l1ll_opy_(bstack1l1ll1ll1l_opy_)
    elif len(app) == 2:
      if bstack11l1l11_opy_ (u"ࠪࡴࡦࡺࡨࠨ੄") in app and bstack11l1l11_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡣ࡮ࡪࠧ੅") in app:
        if os.path.exists(app[bstack11l1l11_opy_ (u"ࠬࡶࡡࡵࡪࠪ੆")]):
          bstack1ll1llll11_opy_ = bstack1ll1l1ll_opy_(config, app[bstack11l1l11_opy_ (u"࠭ࡰࡢࡶ࡫ࠫੇ")], app[bstack11l1l11_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳ࡟ࡪࡦࠪੈ")])
        else:
          bstack11111l1ll_opy_(bstack1l1ll11l1_opy_.format(app))
      else:
        bstack11111l1ll_opy_(bstack1l1ll1ll1l_opy_)
    else:
      for key in app:
        if key in bstack1llll1111_opy_:
          if key == bstack11l1l11_opy_ (u"ࠨࡲࡤࡸ࡭࠭੉"):
            if os.path.exists(app[key]):
              bstack1ll1llll11_opy_ = bstack1ll1l1ll_opy_(config, app[key])
            else:
              bstack11111l1ll_opy_(bstack1l1ll11l1_opy_.format(app))
          else:
            bstack1ll1llll11_opy_ = app[key]
        else:
          bstack11111l1ll_opy_(bstack1lll1l1l1_opy_)
  return bstack1ll1llll11_opy_
def bstack1lll11l1_opy_(bstack1ll1llll11_opy_):
  import re
  bstack11l1111l_opy_ = re.compile(bstack11l1l11_opy_ (u"ࡴࠥࡢࡠࡧ࠭ࡻࡃ࠰࡞࠵࠳࠹࡝ࡡ࠱ࡠ࠲ࡣࠪࠥࠤ੊"))
  bstack111111111_opy_ = re.compile(bstack11l1l11_opy_ (u"ࡵࠦࡣࡡࡡ࠮ࡼࡄ࠱࡟࠶࠭࠺࡞ࡢ࠲ࡡ࠳࡝ࠫ࠱࡞ࡥ࠲ࢀࡁ࠮࡜࠳࠱࠾ࡢ࡟࠯࡞࠰ࡡ࠯ࠪࠢੋ"))
  if bstack11l1l11_opy_ (u"ࠫࡧࡹ࠺࠰࠱ࠪੌ") in bstack1ll1llll11_opy_ or re.fullmatch(bstack11l1111l_opy_, bstack1ll1llll11_opy_) or re.fullmatch(bstack111111111_opy_, bstack1ll1llll11_opy_):
    return True
  else:
    return False
@measure(event_name=EVENTS.bstack11lllll1ll_opy_, stage=STAGE.bstack1l1ll1lll_opy_, bstack11ll11ll11_opy_=bstack11l1l1lll_opy_)
def bstack1ll1l1ll_opy_(config, path, bstack111l1ll1_opy_=None):
  import requests
  from requests_toolbelt.multipart.encoder import MultipartEncoder
  import hashlib
  md5_hash = hashlib.md5(open(os.path.abspath(path), bstack11l1l11_opy_ (u"ࠬࡸࡢࠨ੍")).read()).hexdigest()
  bstack111l1ll11_opy_ = bstack1lll11l111_opy_(md5_hash)
  bstack1ll1llll11_opy_ = None
  if bstack111l1ll11_opy_:
    logger.info(bstack1ll11ll1ll_opy_.format(bstack111l1ll11_opy_, md5_hash))
    return bstack111l1ll11_opy_
  bstack1l1ll1l111_opy_ = datetime.datetime.now()
  bstack1l111l111_opy_ = MultipartEncoder(
    fields={
      bstack11l1l11_opy_ (u"࠭ࡦࡪ࡮ࡨࠫ੎"): (os.path.basename(path), open(os.path.abspath(path), bstack11l1l11_opy_ (u"ࠧࡳࡤࠪ੏")), bstack11l1l11_opy_ (u"ࠨࡶࡨࡼࡹ࠵ࡰ࡭ࡣ࡬ࡲࠬ੐")),
      bstack11l1l11_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡡ࡬ࡨࠬੑ"): bstack111l1ll1_opy_
    }
  )
  response = requests.post(bstack11llll1l11_opy_, data=bstack1l111l111_opy_,
                           headers={bstack11l1l11_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱࡙ࡿࡰࡦࠩ੒"): bstack1l111l111_opy_.content_type},
                           auth=(config[bstack11l1l11_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭੓")], config[bstack11l1l11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ੔")]))
  try:
    res = json.loads(response.text)
    bstack1ll1llll11_opy_ = res[bstack11l1l11_opy_ (u"࠭ࡡࡱࡲࡢࡹࡷࡲࠧ੕")]
    logger.info(bstack11ll11ll1_opy_.format(bstack1ll1llll11_opy_))
    bstack11llll1ll_opy_(md5_hash, bstack1ll1llll11_opy_)
    cli.bstack1ll11lll_opy_(bstack11l1l11_opy_ (u"ࠢࡩࡶࡷࡴ࠿ࡻࡰ࡭ࡱࡤࡨࡤࡧࡰࡱࠤ੖"), datetime.datetime.now() - bstack1l1ll1l111_opy_)
  except ValueError as err:
    bstack11111l1ll_opy_(bstack11ll11ll1l_opy_.format(str(err)))
  return bstack1ll1llll11_opy_
def bstack11l1l111l1_opy_(framework_name=None, args=None):
  global CONFIG
  global bstack1l11l11l1l_opy_
  bstack1llll1l11_opy_ = 1
  bstack1lll11ll1l_opy_ = 1
  if bstack11l1l11_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ੗") in CONFIG:
    bstack1lll11ll1l_opy_ = CONFIG[bstack11l1l11_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ੘")]
  else:
    bstack1lll11ll1l_opy_ = bstack1l1lll1l1l_opy_(framework_name, args) or 1
  if bstack11l1l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ਖ਼") in CONFIG:
    bstack1llll1l11_opy_ = len(CONFIG[bstack11l1l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧਗ਼")])
  bstack1l11l11l1l_opy_ = int(bstack1lll11ll1l_opy_) * int(bstack1llll1l11_opy_)
def bstack1l1lll1l1l_opy_(framework_name, args):
  if framework_name == bstack111l11ll1_opy_ and args and bstack11l1l11_opy_ (u"ࠬ࠳࠭ࡱࡴࡲࡧࡪࡹࡳࡦࡵࠪਜ਼") in args:
      bstack11l111l1l_opy_ = args.index(bstack11l1l11_opy_ (u"࠭࠭࠮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠫੜ"))
      return int(args[bstack11l111l1l_opy_ + 1]) or 1
  return 1
def bstack1lll11l111_opy_(md5_hash):
  bstack111lll1l1_opy_ = os.path.join(os.path.expanduser(bstack11l1l11_opy_ (u"ࠧࡿࠩ੝")), bstack11l1l11_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨਫ਼"), bstack11l1l11_opy_ (u"ࠩࡤࡴࡵ࡛ࡰ࡭ࡱࡤࡨࡒࡊ࠵ࡉࡣࡶ࡬࠳ࡰࡳࡰࡰࠪ੟"))
  if os.path.exists(bstack111lll1l1_opy_):
    bstack1l1lll1lll_opy_ = json.load(open(bstack111lll1l1_opy_, bstack11l1l11_opy_ (u"ࠪࡶࡧ࠭੠")))
    if md5_hash in bstack1l1lll1lll_opy_:
      bstack1111ll11_opy_ = bstack1l1lll1lll_opy_[md5_hash]
      bstack1111l111l_opy_ = datetime.datetime.now()
      bstack11lll11l1_opy_ = datetime.datetime.strptime(bstack1111ll11_opy_[bstack11l1l11_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧ੡")], bstack11l1l11_opy_ (u"ࠬࠫࡤ࠰ࠧࡰ࠳ࠪ࡟ࠠࠦࡊ࠽ࠩࡒࡀࠥࡔࠩ੢"))
      if (bstack1111l111l_opy_ - bstack11lll11l1_opy_).days > 30:
        return None
      elif version.parse(str(__version__)) > version.parse(bstack1111ll11_opy_[bstack11l1l11_opy_ (u"࠭ࡳࡥ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫ੣")]):
        return None
      return bstack1111ll11_opy_[bstack11l1l11_opy_ (u"ࠧࡪࡦࠪ੤")]
  else:
    return None
def bstack11llll1ll_opy_(md5_hash, bstack1ll1llll11_opy_):
  bstack1l11l11ll_opy_ = os.path.join(os.path.expanduser(bstack11l1l11_opy_ (u"ࠨࢀࠪ੥")), bstack11l1l11_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩ੦"))
  if not os.path.exists(bstack1l11l11ll_opy_):
    os.makedirs(bstack1l11l11ll_opy_)
  bstack111lll1l1_opy_ = os.path.join(os.path.expanduser(bstack11l1l11_opy_ (u"ࠪࢂࠬ੧")), bstack11l1l11_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫ੨"), bstack11l1l11_opy_ (u"ࠬࡧࡰࡱࡗࡳࡰࡴࡧࡤࡎࡆ࠸ࡌࡦࡹࡨ࠯࡬ࡶࡳࡳ࠭੩"))
  bstack11ll11lll1_opy_ = {
    bstack11l1l11_opy_ (u"࠭ࡩࡥࠩ੪"): bstack1ll1llll11_opy_,
    bstack11l1l11_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪ੫"): datetime.datetime.strftime(datetime.datetime.now(), bstack11l1l11_opy_ (u"ࠨࠧࡧ࠳ࠪࡳ࠯࡛ࠦࠣࠩࡍࡀࠥࡎ࠼ࠨࡗࠬ੬")),
    bstack11l1l11_opy_ (u"ࠩࡶࡨࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ੭"): str(__version__)
  }
  if os.path.exists(bstack111lll1l1_opy_):
    bstack1l1lll1lll_opy_ = json.load(open(bstack111lll1l1_opy_, bstack11l1l11_opy_ (u"ࠪࡶࡧ࠭੮")))
  else:
    bstack1l1lll1lll_opy_ = {}
  bstack1l1lll1lll_opy_[md5_hash] = bstack11ll11lll1_opy_
  with open(bstack111lll1l1_opy_, bstack11l1l11_opy_ (u"ࠦࡼ࠱ࠢ੯")) as outfile:
    json.dump(bstack1l1lll1lll_opy_, outfile)
def bstack11ll1ll1_opy_(self):
  return
def bstack1ll1llll1l_opy_(self):
  return
def bstack1l11l1l1_opy_(self):
  global bstack1llll1l1ll_opy_
  bstack1llll1l1ll_opy_(self)
def bstack1llll1l1_opy_():
  global bstack11l1l1ll_opy_
  bstack11l1l1ll_opy_ = True
@measure(event_name=EVENTS.bstack11l1ll1l11_opy_, stage=STAGE.bstack1l1ll1lll_opy_, bstack11ll11ll11_opy_=bstack11l1l1lll_opy_)
def bstack111l1l11l_opy_(self):
  global bstack1l11lll1l_opy_
  global bstack1lll11111_opy_
  global bstack1lllll11l1_opy_
  try:
    if bstack11l1l11_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬੰ") in bstack1l11lll1l_opy_ and self.session_id != None and bstack1llllllll1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"࠭ࡴࡦࡵࡷࡗࡹࡧࡴࡶࡵࠪੱ"), bstack11l1l11_opy_ (u"ࠧࠨੲ")) != bstack11l1l11_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩੳ"):
      bstack1l111l1ll_opy_ = bstack11l1l11_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩੴ") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack11l1l11_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪੵ")
      if bstack1l111l1ll_opy_ == bstack11l1l11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ੶"):
        bstack1l111lll1_opy_(logger)
      if self != None:
        bstack1l1l1l11l1_opy_(self, bstack1l111l1ll_opy_, bstack11l1l11_opy_ (u"ࠬ࠲ࠠࠨ੷").join(threading.current_thread().bstackTestErrorMessages))
    threading.current_thread().testStatus = bstack11l1l11_opy_ (u"࠭ࠧ੸")
    if bstack11l1l11_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ੹") in bstack1l11lll1l_opy_ and getattr(threading.current_thread(), bstack11l1l11_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ੺"), None):
      bstack11ll111l_opy_.bstack1lllllll1_opy_(self, bstack1l11lll1ll_opy_, logger, wait=True)
    if bstack11l1l11_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩ੻") in bstack1l11lll1l_opy_:
      if not threading.currentThread().behave_test_status:
        bstack1l1l1l11l1_opy_(self, bstack11l1l11_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥ੼"))
      bstack1lll1111l_opy_.bstack11111lll_opy_(self)
  except Exception as e:
    logger.debug(bstack11l1l11_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡰࡥࡷࡱࡩ࡯ࡩࠣࡷࡹࡧࡴࡶࡵ࠽ࠤࠧ੽") + str(e))
  bstack1lllll11l1_opy_(self)
  self.session_id = None
def bstack1llll111l_opy_(self, *args, **kwargs):
  try:
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    from bstack_utils.helper import bstack11ll1l1l_opy_
    global bstack1l11lll1l_opy_
    command_executor = kwargs.get(bstack11l1l11_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩࡥࡥࡹࡧࡦࡹࡹࡵࡲࠨ੾"), bstack11l1l11_opy_ (u"࠭ࠧ੿"))
    bstack11l1llll1l_opy_ = False
    if type(command_executor) == str and bstack11l1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠪ઀") in command_executor:
      bstack11l1llll1l_opy_ = True
    elif isinstance(command_executor, RemoteConnection) and bstack11l1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫઁ") in str(getattr(command_executor, bstack11l1l11_opy_ (u"ࠩࡢࡹࡷࡲࠧં"), bstack11l1l11_opy_ (u"ࠪࠫઃ"))):
      bstack11l1llll1l_opy_ = True
    else:
      return bstack1lll1l1l_opy_(self, *args, **kwargs)
    if bstack11l1llll1l_opy_:
      bstack11l1l111l_opy_ = bstack11l1111l1_opy_.bstack1ll1l111l1_opy_(CONFIG, bstack1l11lll1l_opy_)
      if kwargs.get(bstack11l1l11_opy_ (u"ࠫࡴࡶࡴࡪࡱࡱࡷࠬ઄")):
        kwargs[bstack11l1l11_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭અ")] = bstack11ll1l1l_opy_(kwargs[bstack11l1l11_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡹࠧઆ")], bstack1l11lll1l_opy_, bstack11l1l111l_opy_)
      elif kwargs.get(bstack11l1l11_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧઇ")):
        kwargs[bstack11l1l11_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨઈ")] = bstack11ll1l1l_opy_(kwargs[bstack11l1l11_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩઉ")], bstack1l11lll1l_opy_, bstack11l1l111l_opy_)
  except Exception as e:
    logger.error(bstack11l1l11_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬ࡪࡴࠠࡱࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤࡘࡊࡋࠡࡥࡤࡴࡸࡀࠠࡼࡿࠥઊ").format(str(e)))
  return bstack1lll1l1l_opy_(self, *args, **kwargs)
@measure(event_name=EVENTS.bstack111ll111l_opy_, stage=STAGE.bstack1l1ll1lll_opy_, bstack11ll11ll11_opy_=bstack11l1l1lll_opy_)
def bstack1llll1ll_opy_(self, command_executor=bstack11l1l11_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳࠶࠸࠷࠯࠲࠱࠴࠳࠷࠺࠵࠶࠷࠸ࠧઋ"), *args, **kwargs):
  bstack1llllll1l1_opy_ = bstack1llll111l_opy_(self, command_executor=command_executor, *args, **kwargs)
  if not bstack11l11l11_opy_.on():
    return bstack1llllll1l1_opy_
  try:
    logger.debug(bstack11l1l11_opy_ (u"ࠬࡉ࡯࡮࡯ࡤࡲࡩࠦࡅࡹࡧࡦࡹࡹࡵࡲࠡࡹ࡫ࡩࡳࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢ࡬ࡷࠥ࡬ࡡ࡭ࡵࡨࠤ࠲ࠦࡻࡾࠩઌ").format(str(command_executor)))
    logger.debug(bstack11l1l11_opy_ (u"࠭ࡈࡶࡤ࡙ࠣࡗࡒࠠࡪࡵࠣ࠱ࠥࢁࡽࠨઍ").format(str(command_executor._url)))
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    if isinstance(command_executor, RemoteConnection) and bstack11l1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠪ઎") in command_executor._url:
      bstack111ll1lll_opy_.bstack11l111l1_opy_(bstack11l1l11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࠩએ"), True)
  except:
    pass
  if (isinstance(command_executor, str) and bstack11l1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠬઐ") in command_executor):
    bstack111ll1lll_opy_.bstack11l111l1_opy_(bstack11l1l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡷࡪࡹࡳࡪࡱࡱࠫઑ"), True)
  threading.current_thread().bstackSessionDriver = self
  bstack1ll11111l1_opy_ = getattr(threading.current_thread(), bstack11l1l11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡘࡪࡹࡴࡎࡧࡷࡥࠬ઒"), None)
  if bstack11l1l11_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬઓ") in bstack1l11lll1l_opy_ or bstack11l1l11_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬઔ") in bstack1l11lll1l_opy_:
    bstack11lll111l1_opy_.bstack11ll1111_opy_(self)
  if bstack11l1l11_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧક") in bstack1l11lll1l_opy_ and bstack1ll11111l1_opy_ and bstack1ll11111l1_opy_.get(bstack11l1l11_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨખ"), bstack11l1l11_opy_ (u"ࠩࠪગ")) == bstack11l1l11_opy_ (u"ࠪࡴࡪࡴࡤࡪࡰࡪࠫઘ"):
    bstack11lll111l1_opy_.bstack11ll1111_opy_(self)
  return bstack1llllll1l1_opy_
def bstack1l111111_opy_(args):
  return bstack11l1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶࠬઙ") in str(args)
def bstack1llll11ll1_opy_(self, driver_command, *args, **kwargs):
  global bstack11l1l111ll_opy_
  global bstack1l1l1lll1l_opy_
  bstack1l11l1ll1_opy_ = bstack1llllllll1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"ࠬ࡯ࡳࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩચ"), None) and bstack1llllllll1_opy_(
          threading.current_thread(), bstack11l1l11_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬછ"), None)
  bstack11ll1ll1ll_opy_ = bstack1llllllll1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"ࠧࡪࡵࡄࡴࡵࡇ࠱࠲ࡻࡗࡩࡸࡺࠧજ"), None) and bstack1llllllll1_opy_(
          threading.current_thread(), bstack11l1l11_opy_ (u"ࠨࡣࡳࡴࡆ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪઝ"), None)
  bstack1lll1111ll_opy_ = getattr(self, bstack11l1l11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡃ࠴࠵ࡾ࡙ࡨࡰࡷ࡯ࡨࡘࡩࡡ࡯ࠩઞ"), None) != None and getattr(self, bstack11l1l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡄ࠵࠶ࡿࡓࡩࡱࡸࡰࡩ࡙ࡣࡢࡰࠪટ"), None) == True
  if not bstack1l1l1lll1l_opy_ and bstack1l111ll111_opy_ and bstack1l1l1l1ll1_opy_.bstack1l1111l1l_opy_(CONFIG) and bstack11ll1lll1l_opy_.bstack11ll111111_opy_(driver_command) and (bstack1lll1111ll_opy_ or bstack1l11l1ll1_opy_ or bstack11ll1ll1ll_opy_) and not bstack1l111111_opy_(args):
    try:
      bstack1l1l1lll1l_opy_ = True
      logger.debug(bstack11l1l11_opy_ (u"ࠫࡕ࡫ࡲࡧࡱࡵࡱ࡮ࡴࡧࠡࡵࡦࡥࡳࠦࡦࡰࡴࠣࡿࢂ࠭ઠ").format(driver_command))
      logger.debug(perform_scan(self, driver_command=driver_command))
    except Exception as err:
      logger.debug(bstack11l1l11_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡲࡨࡶ࡫ࡵࡲ࡮ࠢࡶࡧࡦࡴࠠࡼࡿࠪડ").format(str(err)))
    bstack1l1l1lll1l_opy_ = False
  response = bstack11l1l111ll_opy_(self, driver_command, *args, **kwargs)
  if (bstack11l1l11_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬઢ") in str(bstack1l11lll1l_opy_).lower() or bstack11l1l11_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧણ") in str(bstack1l11lll1l_opy_).lower()) and bstack11l11l11_opy_.on():
    try:
      if driver_command == bstack11l1l11_opy_ (u"ࠨࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠬત"):
        bstack11lll111l1_opy_.bstack11ll1111ll_opy_({
            bstack11l1l11_opy_ (u"ࠩ࡬ࡱࡦ࡭ࡥࠨથ"): response[bstack11l1l11_opy_ (u"ࠪࡺࡦࡲࡵࡦࠩદ")],
            bstack11l1l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫધ"): bstack11lll111l1_opy_.current_test_uuid() if bstack11lll111l1_opy_.current_test_uuid() else bstack11l11l11_opy_.current_hook_uuid()
        })
    except:
      pass
  return response
@measure(event_name=EVENTS.bstack1ll1lll1ll_opy_, stage=STAGE.bstack1l1ll1lll_opy_, bstack11ll11ll11_opy_=bstack11l1l1lll_opy_)
def bstack1lll111lll_opy_(self, command_executor,
             desired_capabilities=None, bstack11llll11l1_opy_=None, proxy=None,
             keep_alive=True, file_detector=None, options=None, *args, **kwargs):
  global CONFIG
  global bstack1lll11111_opy_
  global bstack1l1ll11111_opy_
  global bstack11l1l1lll_opy_
  global bstack111lll11_opy_
  global bstack1lll1l11l1_opy_
  global bstack1l11lll1l_opy_
  global bstack1lll1l1l_opy_
  global bstack1l11ll11l1_opy_
  global bstack11l11ll111_opy_
  global bstack1l11lll1ll_opy_
  CONFIG[bstack11l1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧન")] = str(bstack1l11lll1l_opy_) + str(__version__)
  bstack1l11l1111_opy_ = os.environ[bstack11l1l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫ઩")]
  bstack11l1l111l_opy_ = bstack11l1111l1_opy_.bstack1ll1l111l1_opy_(CONFIG, bstack1l11lll1l_opy_)
  CONFIG[bstack11l1l11_opy_ (u"ࠧࡵࡧࡶࡸ࡭ࡻࡢࡃࡷ࡬ࡰࡩ࡛ࡵࡪࡦࠪપ")] = bstack1l11l1111_opy_
  CONFIG[bstack11l1l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡐࡳࡱࡧࡹࡨࡺࡍࡢࡲࠪફ")] = bstack11l1l111l_opy_
  if CONFIG.get(bstack11l1l11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩબ"),bstack11l1l11_opy_ (u"ࠪࠫભ")) and bstack11l1l11_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪમ") in bstack1l11lll1l_opy_:
    CONFIG[bstack11l1l11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬય")].pop(bstack11l1l11_opy_ (u"࠭ࡩ࡯ࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫર"), None)
    CONFIG[bstack11l1l11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧ઱")].pop(bstack11l1l11_opy_ (u"ࠨࡧࡻࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭લ"), None)
  command_executor = bstack11111l1l_opy_()
  logger.debug(bstack1l11ll11ll_opy_.format(command_executor))
  proxy = bstack1l11l1ll1l_opy_(CONFIG, proxy)
  bstack1l1l1l111_opy_ = 0 if bstack1l1ll11111_opy_ < 0 else bstack1l1ll11111_opy_
  try:
    if bstack111lll11_opy_ is True:
      bstack1l1l1l111_opy_ = int(multiprocessing.current_process().name)
    elif bstack1lll1l11l1_opy_ is True:
      bstack1l1l1l111_opy_ = int(threading.current_thread().name)
  except:
    bstack1l1l1l111_opy_ = 0
  bstack11lllll11l_opy_ = bstack1lll111ll1_opy_(CONFIG, bstack1l1l1l111_opy_)
  logger.debug(bstack111l11l1_opy_.format(str(bstack11lllll11l_opy_)))
  if bstack11l1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ળ") in CONFIG and bstack1ll11l1l1_opy_(CONFIG[bstack11l1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ઴")]):
    bstack1ll11l1l1l_opy_(bstack11lllll11l_opy_)
  if bstack1l1l1l1ll1_opy_.bstack1l1l1l1l_opy_(CONFIG, bstack1l1l1l111_opy_) and bstack1l1l1l1ll1_opy_.bstack111l1111l_opy_(bstack11lllll11l_opy_, options, desired_capabilities):
    threading.current_thread().a11yPlatform = True
    if cli.accessibility is None or not cli.accessibility.is_enabled():
      bstack1l1l1l1ll1_opy_.set_capabilities(bstack11lllll11l_opy_, CONFIG)
  if desired_capabilities:
    bstack1l1lll1ll1_opy_ = bstack1l1lll11l_opy_(desired_capabilities)
    bstack1l1lll1ll1_opy_[bstack11l1l11_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫવ")] = bstack11l1l1l11l_opy_(CONFIG)
    bstack1ll1lll11l_opy_ = bstack1lll111ll1_opy_(bstack1l1lll1ll1_opy_)
    if bstack1ll1lll11l_opy_:
      bstack11lllll11l_opy_ = update(bstack1ll1lll11l_opy_, bstack11lllll11l_opy_)
    desired_capabilities = None
  if options:
    bstack11l11ll1ll_opy_(options, bstack11lllll11l_opy_)
  if not options:
    options = bstack1l11111l11_opy_(bstack11lllll11l_opy_)
  bstack1l11lll1ll_opy_ = CONFIG.get(bstack11l1l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨશ"))[bstack1l1l1l111_opy_]
  if proxy and bstack1ll1lllll_opy_() >= version.parse(bstack11l1l11_opy_ (u"࠭࠴࠯࠳࠳࠲࠵࠭ષ")):
    options.proxy(proxy)
  if options and bstack1ll1lllll_opy_() >= version.parse(bstack11l1l11_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭સ")):
    desired_capabilities = None
  if (
          not options and not desired_capabilities
  ) or (
          bstack1ll1lllll_opy_() < version.parse(bstack11l1l11_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧહ")) and not desired_capabilities
  ):
    desired_capabilities = {}
    desired_capabilities.update(bstack11lllll11l_opy_)
  logger.info(bstack11l1ll1ll_opy_)
  bstack1l1ll1l11l_opy_.end(EVENTS.bstack1l1l11l1l1_opy_.value, EVENTS.bstack1l1l11l1l1_opy_.value + bstack11l1l11_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤ઺"), EVENTS.bstack1l1l11l1l1_opy_.value + bstack11l1l11_opy_ (u"ࠥ࠾ࡪࡴࡤࠣ઻"), status=True, failure=None, test_name=bstack11l1l1lll_opy_)
  if bstack1ll1lllll_opy_() >= version.parse(bstack11l1l11_opy_ (u"ࠫ࠹࠴࠱࠱࠰࠳઼ࠫ")):
    bstack1lll1l1l_opy_(self, command_executor=command_executor,
              options=options, keep_alive=keep_alive, file_detector=file_detector, *args, **kwargs)
  elif bstack1ll1lllll_opy_() >= version.parse(bstack11l1l11_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫઽ")):
    bstack1lll1l1l_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities, options=options,
              bstack11llll11l1_opy_=bstack11llll11l1_opy_, proxy=proxy,
              keep_alive=keep_alive, file_detector=file_detector)
  elif bstack1ll1lllll_opy_() >= version.parse(bstack11l1l11_opy_ (u"࠭࠲࠯࠷࠶࠲࠵࠭ા")):
    bstack1lll1l1l_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities,
              bstack11llll11l1_opy_=bstack11llll11l1_opy_, proxy=proxy,
              keep_alive=keep_alive, file_detector=file_detector)
  else:
    bstack1lll1l1l_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities,
              bstack11llll11l1_opy_=bstack11llll11l1_opy_, proxy=proxy,
              keep_alive=keep_alive)
  if bstack1l1l1l1ll1_opy_.bstack1l1l1l1l_opy_(CONFIG, bstack1l1l1l111_opy_) and bstack1l1l1l1ll1_opy_.bstack111l1111l_opy_(self.caps, options, desired_capabilities):
    if CONFIG[bstack11l1l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡖࡲࡰࡦࡸࡧࡹࡓࡡࡱࠩિ")][bstack11l1l11_opy_ (u"ࠨࡣࡳࡴࡤࡧࡵࡵࡱࡰࡥࡹ࡫ࠧી")] == True:
      threading.current_thread().appA11yPlatform = True
      if cli.accessibility is None or not cli.accessibility.is_enabled():
        bstack1l1l1l1ll1_opy_.set_capabilities(bstack11lllll11l_opy_, CONFIG)
  try:
    bstack1l11ll1111_opy_ = bstack11l1l11_opy_ (u"ࠩࠪુ")
    if bstack1ll1lllll_opy_() >= version.parse(bstack11l1l11_opy_ (u"ࠪ࠸࠳࠶࠮࠱ࡤ࠴ࠫૂ")):
      bstack1l11ll1111_opy_ = self.caps.get(bstack11l1l11_opy_ (u"ࠦࡴࡶࡴࡪ࡯ࡤࡰࡍࡻࡢࡖࡴ࡯ࠦૃ"))
    else:
      bstack1l11ll1111_opy_ = self.capabilities.get(bstack11l1l11_opy_ (u"ࠧࡵࡰࡵ࡫ࡰࡥࡱࡎࡵࡣࡗࡵࡰࠧૄ"))
    if bstack1l11ll1111_opy_:
      bstack1l11llll_opy_(bstack1l11ll1111_opy_)
      if bstack1ll1lllll_opy_() <= version.parse(bstack11l1l11_opy_ (u"࠭࠳࠯࠳࠶࠲࠵࠭ૅ")):
        self.command_executor._url = bstack11l1l11_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࠣ૆") + bstack1111l1l1_opy_ + bstack11l1l11_opy_ (u"ࠣ࠼࠻࠴࠴ࡽࡤ࠰ࡪࡸࡦࠧે")
      else:
        self.command_executor._url = bstack11l1l11_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࠦૈ") + bstack1l11ll1111_opy_ + bstack11l1l11_opy_ (u"ࠥ࠳ࡼࡪ࠯ࡩࡷࡥࠦૉ")
      logger.debug(bstack1111llll_opy_.format(bstack1l11ll1111_opy_))
    else:
      logger.debug(bstack11ll1l1111_opy_.format(bstack11l1l11_opy_ (u"ࠦࡔࡶࡴࡪ࡯ࡤࡰࠥࡎࡵࡣࠢࡱࡳࡹࠦࡦࡰࡷࡱࡨࠧ૊")))
  except Exception as e:
    logger.debug(bstack11ll1l1111_opy_.format(e))
  if bstack11l1l11_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫો") in bstack1l11lll1l_opy_:
    bstack1l11ll1ll1_opy_(bstack1l1ll11111_opy_, bstack11l11ll111_opy_)
  bstack1lll11111_opy_ = self.session_id
  if bstack11l1l11_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ૌ") in bstack1l11lll1l_opy_ or bstack11l1l11_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫્ࠧ") in bstack1l11lll1l_opy_ or bstack11l1l11_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ૎") in bstack1l11lll1l_opy_:
    threading.current_thread().bstackSessionId = self.session_id
    threading.current_thread().bstackSessionDriver = self
    threading.current_thread().bstackTestErrorMessages = []
  bstack1ll11111l1_opy_ = getattr(threading.current_thread(), bstack11l1l11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡖࡨࡷࡹࡓࡥࡵࡣࠪ૏"), None)
  if bstack11l1l11_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪૐ") in bstack1l11lll1l_opy_ or bstack11l1l11_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪ૑") in bstack1l11lll1l_opy_:
    bstack11lll111l1_opy_.bstack11ll1111_opy_(self)
  if bstack11l1l11_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ૒") in bstack1l11lll1l_opy_ and bstack1ll11111l1_opy_ and bstack1ll11111l1_opy_.get(bstack11l1l11_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭૓"), bstack11l1l11_opy_ (u"ࠧࠨ૔")) == bstack11l1l11_opy_ (u"ࠨࡲࡨࡲࡩ࡯࡮ࡨࠩ૕"):
    bstack11lll111l1_opy_.bstack11ll1111_opy_(self)
  bstack1l11ll11l1_opy_.append(self)
  if bstack11l1l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ૖") in CONFIG and bstack11l1l11_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ૗") in CONFIG[bstack11l1l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ૘")][bstack1l1l1l111_opy_]:
    bstack11l1l1lll_opy_ = CONFIG[bstack11l1l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ૙")][bstack1l1l1l111_opy_][bstack11l1l11_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ૚")]
  logger.debug(bstack111111ll_opy_.format(bstack1lll11111_opy_))
try:
  try:
    import Browser
    from subprocess import Popen
    from browserstack_sdk.__init__ import bstack1lll11ll_opy_
    def bstack1111ll1ll_opy_(self, args, bufsize=-1, executable=None,
              stdin=None, stdout=None, stderr=None,
              preexec_fn=None, close_fds=True,
              shell=False, cwd=None, env=None, universal_newlines=None,
              startupinfo=None, creationflags=0,
              restore_signals=True, start_new_session=False,
              pass_fds=(), *, user=None, group=None, extra_groups=None,
              encoding=None, errors=None, text=None, umask=-1, pipesize=-1):
      global CONFIG
      global bstack1l1l1lllll_opy_
      if(bstack11l1l11_opy_ (u"ࠢࡪࡰࡧࡩࡽ࠴ࡪࡴࠤ૛") in args[1]):
        with open(os.path.join(os.path.expanduser(bstack11l1l11_opy_ (u"ࠨࢀࠪ૜")), bstack11l1l11_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩ૝"), bstack11l1l11_opy_ (u"ࠪ࠲ࡸ࡫ࡳࡴ࡫ࡲࡲ࡮ࡪࡳ࠯ࡶࡻࡸࠬ૞")), bstack11l1l11_opy_ (u"ࠫࡼ࠭૟")) as fp:
          fp.write(bstack11l1l11_opy_ (u"ࠧࠨૠ"))
        if(not os.path.exists(os.path.join(os.path.dirname(args[1]), bstack11l1l11_opy_ (u"ࠨࡩ࡯ࡦࡨࡼࡤࡨࡳࡵࡣࡦ࡯࠳ࡰࡳࠣૡ")))):
          with open(args[1], bstack11l1l11_opy_ (u"ࠧࡳࠩૢ")) as f:
            lines = f.readlines()
            index = next((i for i, line in enumerate(lines) if bstack11l1l11_opy_ (u"ࠨࡣࡶࡽࡳࡩࠠࡧࡷࡱࡧࡹ࡯࡯࡯ࠢࡢࡲࡪࡽࡐࡢࡩࡨࠬࡨࡵ࡮ࡵࡧࡻࡸ࠱ࠦࡰࡢࡩࡨࠤࡂࠦࡶࡰ࡫ࡧࠤ࠵࠯ࠧૣ") in line), None)
            if index is not None:
                lines.insert(index+2, bstack1l1ll1lll1_opy_)
            if bstack11l1l11_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭૤") in CONFIG and str(CONFIG[bstack11l1l11_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧ૥")]).lower() != bstack11l1l11_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪ૦"):
                bstack1l1lllll_opy_ = bstack1lll11ll_opy_()
                bstack11l1lll1l1_opy_ = bstack11l1l11_opy_ (u"ࠬ࠭ࠧࠋ࠱࠭ࠤࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽ࠡࠬ࠲ࠎࡨࡵ࡮ࡴࡶࠣࡦࡸࡺࡡࡤ࡭ࡢࡴࡦࡺࡨࠡ࠿ࠣࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࡝ࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࠯࡮ࡨࡲ࡬ࡺࡨࠡ࠯ࠣ࠷ࡢࡁࠊࡤࡱࡱࡷࡹࠦࡢࡴࡶࡤࡧࡰࡥࡣࡢࡲࡶࠤࡂࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺࡠࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡱ࡫࡮ࡨࡶ࡫ࠤ࠲ࠦ࠱࡞࠽ࠍࡧࡴࡴࡳࡵࠢࡳࡣ࡮ࡴࡤࡦࡺࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࡟ࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡰࡪࡴࡧࡵࡪࠣ࠱ࠥ࠸࡝࠼ࠌࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶࠡ࠿ࠣࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࠰ࡶࡰ࡮ࡩࡥࠩ࠲࠯ࠤࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡰࡪࡴࡧࡵࡪࠣ࠱ࠥ࠹ࠩ࠼ࠌࡦࡳࡳࡹࡴࠡ࡫ࡰࡴࡴࡸࡴࡠࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࠹ࡥࡢࡴࡶࡤࡧࡰࠦ࠽ࠡࡴࡨࡵࡺ࡯ࡲࡦࠪࠥࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢࠪ࠽ࠍ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫࠯ࡥ࡫ࡶࡴࡳࡩࡶ࡯࠱ࡰࡦࡻ࡮ࡤࡪࠣࡁࠥࡧࡳࡺࡰࡦࠤ࠭ࡲࡡࡶࡰࡦ࡬ࡔࡶࡴࡪࡱࡱࡷ࠮ࠦ࠽࠿ࠢࡾࡿࠏࠦࠠ࡭ࡧࡷࠤࡨࡧࡰࡴ࠽ࠍࠤࠥࡺࡲࡺࠢࡾࡿࠏࠦࠠࠡࠢࡦࡥࡵࡹࠠ࠾ࠢࡍࡗࡔࡔ࠮ࡱࡣࡵࡷࡪ࠮ࡢࡴࡶࡤࡧࡰࡥࡣࡢࡲࡶ࠭ࡀࠐࠠࠡࡿࢀࠤࡨࡧࡴࡤࡪࠣࠬࡪࡾࠩࠡࡽࡾࠎࠥࠦࠠࠡࡥࡲࡲࡸࡵ࡬ࡦ࠰ࡨࡶࡷࡵࡲࠩࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡶࡡࡳࡵࡨࠤࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵ࠽ࠦ࠱ࠦࡥࡹࠫ࠾ࠎࠥࠦࡽࡾࠌࠣࠤࡷ࡫ࡴࡶࡴࡱࠤࡦࡽࡡࡪࡶࠣ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫࠯ࡥ࡫ࡶࡴࡳࡩࡶ࡯࠱ࡧࡴࡴ࡮ࡦࡥࡷࠬࢀࢁࠊࠡࠢࠣࠤࡼࡹࡅ࡯ࡦࡳࡳ࡮ࡴࡴ࠻ࠢࠪࡿࡨࡪࡰࡖࡴ࡯ࢁࠬࠦࠫࠡࡧࡱࡧࡴࡪࡥࡖࡔࡌࡇࡴࡳࡰࡰࡰࡨࡲࡹ࠮ࡊࡔࡑࡑ࠲ࡸࡺࡲࡪࡰࡪ࡭࡫ࡿࠨࡤࡣࡳࡷ࠮࠯ࠬࠋࠢࠣࠤࠥ࠴࠮࠯࡮ࡤࡹࡳࡩࡨࡐࡲࡷ࡭ࡴࡴࡳࠋࠢࠣࢁࢂ࠯࠻ࠋࡿࢀ࠿ࠏ࠵ࠪࠡ࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࠥ࠰࠯ࠋࠩࠪࠫ૧").format(bstack1l1lllll_opy_=bstack1l1lllll_opy_)
            lines.insert(1, bstack11l1lll1l1_opy_)
            f.seek(0)
            with open(os.path.join(os.path.dirname(args[1]), bstack11l1l11_opy_ (u"ࠨࡩ࡯ࡦࡨࡼࡤࡨࡳࡵࡣࡦ࡯࠳ࡰࡳࠣ૨")), bstack11l1l11_opy_ (u"ࠧࡸࠩ૩")) as bstack11lll1l11l_opy_:
              bstack11lll1l11l_opy_.writelines(lines)
        CONFIG[bstack11l1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪ૪")] = str(bstack1l11lll1l_opy_) + str(__version__)
        bstack1l11l1111_opy_ = os.environ[bstack11l1l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧ૫")]
        bstack11l1l111l_opy_ = bstack11l1111l1_opy_.bstack1ll1l111l1_opy_(CONFIG, bstack1l11lll1l_opy_)
        CONFIG[bstack11l1l11_opy_ (u"ࠪࡸࡪࡹࡴࡩࡷࡥࡆࡺ࡯࡬ࡥࡗࡸ࡭ࡩ࠭૬")] = bstack1l11l1111_opy_
        CONFIG[bstack11l1l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡓࡶࡴࡪࡵࡤࡶࡐࡥࡵ࠭૭")] = bstack11l1l111l_opy_
        bstack1l1l1l111_opy_ = 0 if bstack1l1ll11111_opy_ < 0 else bstack1l1ll11111_opy_
        try:
          if bstack111lll11_opy_ is True:
            bstack1l1l1l111_opy_ = int(multiprocessing.current_process().name)
          elif bstack1lll1l11l1_opy_ is True:
            bstack1l1l1l111_opy_ = int(threading.current_thread().name)
        except:
          bstack1l1l1l111_opy_ = 0
        CONFIG[bstack11l1l11_opy_ (u"ࠧࡻࡳࡦ࡙࠶ࡇࠧ૮")] = False
        CONFIG[bstack11l1l11_opy_ (u"ࠨࡩࡴࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧ૯")] = True
        bstack11lllll11l_opy_ = bstack1lll111ll1_opy_(CONFIG, bstack1l1l1l111_opy_)
        logger.debug(bstack111l11l1_opy_.format(str(bstack11lllll11l_opy_)))
        if CONFIG.get(bstack11l1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ૰")):
          bstack1ll11l1l1l_opy_(bstack11lllll11l_opy_)
        if bstack11l1l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ૱") in CONFIG and bstack11l1l11_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ૲") in CONFIG[bstack11l1l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭૳")][bstack1l1l1l111_opy_]:
          bstack11l1l1lll_opy_ = CONFIG[bstack11l1l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ૴")][bstack1l1l1l111_opy_][bstack11l1l11_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ૵")]
        args.append(os.path.join(os.path.expanduser(bstack11l1l11_opy_ (u"࠭ࡾࠨ૶")), bstack11l1l11_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧ૷"), bstack11l1l11_opy_ (u"ࠨ࠰ࡶࡩࡸࡹࡩࡰࡰ࡬ࡨࡸ࠴ࡴࡹࡶࠪ૸")))
        args.append(str(threading.get_ident()))
        args.append(json.dumps(bstack11lllll11l_opy_))
        args[1] = os.path.join(os.path.dirname(args[1]), bstack11l1l11_opy_ (u"ࠤ࡬ࡲࡩ࡫ࡸࡠࡤࡶࡸࡦࡩ࡫࠯࡬ࡶࠦૹ"))
      bstack1l1l1lllll_opy_ = True
      return bstack1l1111111l_opy_(self, args, bufsize=bufsize, executable=executable,
                    stdin=stdin, stdout=stdout, stderr=stderr,
                    preexec_fn=preexec_fn, close_fds=close_fds,
                    shell=shell, cwd=cwd, env=env, universal_newlines=universal_newlines,
                    startupinfo=startupinfo, creationflags=creationflags,
                    restore_signals=restore_signals, start_new_session=start_new_session,
                    pass_fds=pass_fds, user=user, group=group, extra_groups=extra_groups,
                    encoding=encoding, errors=errors, text=text, umask=umask, pipesize=pipesize)
  except Exception as e:
    pass
  import playwright._impl._api_structures
  import playwright._impl._helper
  def bstack1ll11llll_opy_(self,
        executablePath = None,
        channel = None,
        args = None,
        ignoreDefaultArgs = None,
        handleSIGINT = None,
        handleSIGTERM = None,
        handleSIGHUP = None,
        timeout = None,
        env = None,
        headless = None,
        devtools = None,
        proxy = None,
        downloadsPath = None,
        slowMo = None,
        tracesDir = None,
        chromiumSandbox = None,
        firefoxUserPrefs = None
        ):
    global CONFIG
    global bstack1l1ll11111_opy_
    global bstack11l1l1lll_opy_
    global bstack111lll11_opy_
    global bstack1lll1l11l1_opy_
    global bstack1l11lll1l_opy_
    CONFIG[bstack11l1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬૺ")] = str(bstack1l11lll1l_opy_) + str(__version__)
    bstack1l11l1111_opy_ = os.environ[bstack11l1l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩૻ")]
    bstack11l1l111l_opy_ = bstack11l1111l1_opy_.bstack1ll1l111l1_opy_(CONFIG, bstack1l11lll1l_opy_)
    CONFIG[bstack11l1l11_opy_ (u"ࠬࡺࡥࡴࡶ࡫ࡹࡧࡈࡵࡪ࡮ࡧ࡙ࡺ࡯ࡤࠨૼ")] = bstack1l11l1111_opy_
    CONFIG[bstack11l1l11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡕࡸ࡯ࡥࡷࡦࡸࡒࡧࡰࠨ૽")] = bstack11l1l111l_opy_
    bstack1l1l1l111_opy_ = 0 if bstack1l1ll11111_opy_ < 0 else bstack1l1ll11111_opy_
    try:
      if bstack111lll11_opy_ is True:
        bstack1l1l1l111_opy_ = int(multiprocessing.current_process().name)
      elif bstack1lll1l11l1_opy_ is True:
        bstack1l1l1l111_opy_ = int(threading.current_thread().name)
    except:
      bstack1l1l1l111_opy_ = 0
    CONFIG[bstack11l1l11_opy_ (u"ࠢࡪࡵࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨ૾")] = True
    bstack11lllll11l_opy_ = bstack1lll111ll1_opy_(CONFIG, bstack1l1l1l111_opy_)
    logger.debug(bstack111l11l1_opy_.format(str(bstack11lllll11l_opy_)))
    if CONFIG.get(bstack11l1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬ૿")):
      bstack1ll11l1l1l_opy_(bstack11lllll11l_opy_)
    if bstack11l1l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ଀") in CONFIG and bstack11l1l11_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨଁ") in CONFIG[bstack11l1l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧଂ")][bstack1l1l1l111_opy_]:
      bstack11l1l1lll_opy_ = CONFIG[bstack11l1l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨଃ")][bstack1l1l1l111_opy_][bstack11l1l11_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ଄")]
    import urllib
    import json
    if bstack11l1l11_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫଅ") in CONFIG and str(CONFIG[bstack11l1l11_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬଆ")]).lower() != bstack11l1l11_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨଇ"):
        bstack1l1l11llll_opy_ = bstack1lll11ll_opy_()
        bstack1l1lllll_opy_ = bstack1l1l11llll_opy_ + urllib.parse.quote(json.dumps(bstack11lllll11l_opy_))
    else:
        bstack1l1lllll_opy_ = bstack11l1l11_opy_ (u"ࠪࡻࡸࡹ࠺࠰࠱ࡦࡨࡵ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࡅࡣࡢࡲࡶࡁࠬଈ") + urllib.parse.quote(json.dumps(bstack11lllll11l_opy_))
    browser = self.connect(bstack1l1lllll_opy_)
    return browser
except Exception as e:
    pass
def bstack1111l1ll1_opy_():
    global bstack1l1l1lllll_opy_
    global bstack1l11lll1l_opy_
    global CONFIG
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack11llll111_opy_
        global bstack111ll1lll_opy_
        if not bstack1l111ll111_opy_:
          global bstack1l1l11l11_opy_
          if not bstack1l1l11l11_opy_:
            from bstack_utils.helper import bstack1lll1l1l1l_opy_, bstack11lllll1l_opy_, bstack11l11lll_opy_
            bstack1l1l11l11_opy_ = bstack1lll1l1l1l_opy_()
            bstack11lllll1l_opy_(bstack1l11lll1l_opy_)
            bstack11l1l111l_opy_ = bstack11l1111l1_opy_.bstack1ll1l111l1_opy_(CONFIG, bstack1l11lll1l_opy_)
            bstack111ll1lll_opy_.bstack11l111l1_opy_(bstack11l1l11_opy_ (u"ࠦࡕࡒࡁ࡚࡙ࡕࡍࡌࡎࡔࡠࡒࡕࡓࡉ࡛ࡃࡕࡡࡐࡅࡕࠨଉ"), bstack11l1l111l_opy_)
          BrowserType.connect = bstack11llll111_opy_
          return
        BrowserType.launch = bstack1ll11llll_opy_
        bstack1l1l1lllll_opy_ = True
    except Exception as e:
        pass
    try:
      import Browser
      from subprocess import Popen
      Popen.__init__ = bstack1111ll1ll_opy_
      bstack1l1l1lllll_opy_ = True
    except Exception as e:
      pass
def bstack1l11ll1l11_opy_(context, bstack1l111lll_opy_):
  try:
    context.page.evaluate(bstack11l1l11_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨଊ"), bstack11l1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡲࡦࡳࡥࠣ࠼ࠪଋ")+ json.dumps(bstack1l111lll_opy_) + bstack11l1l11_opy_ (u"ࠢࡾࡿࠥଌ"))
  except Exception as e:
    logger.debug(bstack11l1l11_opy_ (u"ࠣࡧࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠣࡿࢂࡀࠠࡼࡿࠥ଍").format(str(e), traceback.format_exc()))
def bstack1lll111l1l_opy_(context, message, level):
  try:
    context.page.evaluate(bstack11l1l11_opy_ (u"ࠤࡢࠤࡂࡄࠠࡼࡿࠥ଎"), bstack11l1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡦࡤࡸࡦࠨ࠺ࠨଏ") + json.dumps(message) + bstack11l1l11_opy_ (u"ࠫ࠱ࠨ࡬ࡦࡸࡨࡰࠧࡀࠧଐ") + json.dumps(level) + bstack11l1l11_opy_ (u"ࠬࢃࡽࠨ଑"))
  except Exception as e:
    logger.debug(bstack11l1l11_opy_ (u"ࠨࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡤࡲࡳࡵࡴࡢࡶ࡬ࡳࡳࠦࡻࡾ࠼ࠣࡿࢂࠨ଒").format(str(e), traceback.format_exc()))
@measure(event_name=EVENTS.bstack11lll1l111_opy_, stage=STAGE.bstack1l1ll1lll_opy_, bstack11ll11ll11_opy_=bstack11l1l1lll_opy_)
def bstack11lll1ll1_opy_(self, url):
  global bstack1l1l1lll_opy_
  try:
    bstack1l1ll1ll_opy_(url)
  except Exception as err:
    logger.debug(bstack11l1ll111l_opy_.format(str(err)))
  try:
    bstack1l1l1lll_opy_(self, url)
  except Exception as e:
    try:
      bstack1111l1lll_opy_ = str(e)
      if any(err_msg in bstack1111l1lll_opy_ for err_msg in bstack1111lll11_opy_):
        bstack1l1ll1ll_opy_(url, True)
    except Exception as err:
      logger.debug(bstack11l1ll111l_opy_.format(str(err)))
    raise e
def bstack111l111ll_opy_(self):
  global bstack1l1ll1llll_opy_
  bstack1l1ll1llll_opy_ = self
  return
def bstack11111l111_opy_(self):
  global bstack1ll1llll1_opy_
  bstack1ll1llll1_opy_ = self
  return
def bstack1llll11l1l_opy_(test_name, bstack11ll1l11_opy_):
  global CONFIG
  if percy.bstack1ll1111111_opy_() == bstack11l1l11_opy_ (u"ࠢࡵࡴࡸࡩࠧଓ"):
    bstack1l1111lll1_opy_ = os.path.relpath(bstack11ll1l11_opy_, start=os.getcwd())
    suite_name, _ = os.path.splitext(bstack1l1111lll1_opy_)
    bstack11ll11ll11_opy_ = suite_name + bstack11l1l11_opy_ (u"ࠣ࠯ࠥଔ") + test_name
    threading.current_thread().percySessionName = bstack11ll11ll11_opy_
def bstack1l1l1l1l1l_opy_(self, test, *args, **kwargs):
  global bstack1ll111ll1l_opy_
  test_name = None
  bstack11ll1l11_opy_ = None
  if test:
    test_name = str(test.name)
    bstack11ll1l11_opy_ = str(test.source)
  bstack1llll11l1l_opy_(test_name, bstack11ll1l11_opy_)
  bstack1ll111ll1l_opy_(self, test, *args, **kwargs)
@measure(event_name=EVENTS.bstack1l1111111_opy_, stage=STAGE.bstack1l1ll1lll_opy_, bstack11ll11ll11_opy_=bstack11l1l1lll_opy_)
def bstack111lll111_opy_(driver, bstack11ll11ll11_opy_):
  if not bstack1l1lllll1_opy_ and bstack11ll11ll11_opy_:
      bstack1l1ll11ll1_opy_ = {
          bstack11l1l11_opy_ (u"ࠩࡤࡧࡹ࡯࡯࡯ࠩକ"): bstack11l1l11_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫଖ"),
          bstack11l1l11_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧଗ"): {
              bstack11l1l11_opy_ (u"ࠬࡴࡡ࡮ࡧࠪଘ"): bstack11ll11ll11_opy_
          }
      }
      bstack11ll111ll_opy_ = bstack11l1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠫଙ").format(json.dumps(bstack1l1ll11ll1_opy_))
      driver.execute_script(bstack11ll111ll_opy_)
  if bstack1l1ll11l1l_opy_:
      bstack11l1ll1ll1_opy_ = {
          bstack11l1l11_opy_ (u"ࠧࡢࡥࡷ࡭ࡴࡴࠧଚ"): bstack11l1l11_opy_ (u"ࠨࡣࡱࡲࡴࡺࡡࡵࡧࠪଛ"),
          bstack11l1l11_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬଜ"): {
              bstack11l1l11_opy_ (u"ࠪࡨࡦࡺࡡࠨଝ"): bstack11ll11ll11_opy_ + bstack11l1l11_opy_ (u"ࠫࠥࡶࡡࡴࡵࡨࡨࠦ࠭ଞ"),
              bstack11l1l11_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫଟ"): bstack11l1l11_opy_ (u"࠭ࡩ࡯ࡨࡲࠫଠ")
          }
      }
      if bstack1l1ll11l1l_opy_.status == bstack11l1l11_opy_ (u"ࠧࡑࡃࡖࡗࠬଡ"):
          bstack11lll1l1l1_opy_ = bstack11l1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࢂ࠭ଢ").format(json.dumps(bstack11l1ll1ll1_opy_))
          driver.execute_script(bstack11lll1l1l1_opy_)
          bstack1l1l1l11l1_opy_(driver, bstack11l1l11_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩଣ"))
      elif bstack1l1ll11l1l_opy_.status == bstack11l1l11_opy_ (u"ࠪࡊࡆࡏࡌࠨତ"):
          reason = bstack11l1l11_opy_ (u"ࠦࠧଥ")
          bstack11lllllll_opy_ = bstack11ll11ll11_opy_ + bstack11l1l11_opy_ (u"ࠬࠦࡦࡢ࡫࡯ࡩࡩ࠭ଦ")
          if bstack1l1ll11l1l_opy_.message:
              reason = str(bstack1l1ll11l1l_opy_.message)
              bstack11lllllll_opy_ = bstack11lllllll_opy_ + bstack11l1l11_opy_ (u"࠭ࠠࡸ࡫ࡷ࡬ࠥ࡫ࡲࡳࡱࡵ࠾ࠥ࠭ଧ") + reason
          bstack11l1ll1ll1_opy_[bstack11l1l11_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪନ")] = {
              bstack11l1l11_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ଩"): bstack11l1l11_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨପ"),
              bstack11l1l11_opy_ (u"ࠪࡨࡦࡺࡡࠨଫ"): bstack11lllllll_opy_
          }
          bstack11lll1l1l1_opy_ = bstack11l1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠩବ").format(json.dumps(bstack11l1ll1ll1_opy_))
          driver.execute_script(bstack11lll1l1l1_opy_)
          bstack1l1l1l11l1_opy_(driver, bstack11l1l11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬଭ"), reason)
          bstack1l1ll111ll_opy_(reason, str(bstack1l1ll11l1l_opy_), str(bstack1l1ll11111_opy_), logger)
@measure(event_name=EVENTS.bstack1l1lllll1l_opy_, stage=STAGE.bstack1l1ll1lll_opy_, bstack11ll11ll11_opy_=bstack11l1l1lll_opy_)
def bstack1l11lll11_opy_(driver, test):
  if percy.bstack1ll1111111_opy_() == bstack11l1l11_opy_ (u"ࠨࡴࡳࡷࡨࠦମ") and percy.bstack11lllll1_opy_() == bstack11l1l11_opy_ (u"ࠢࡵࡧࡶࡸࡨࡧࡳࡦࠤଯ"):
      bstack1l1l1llll1_opy_ = bstack1llllllll1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"ࠨࡲࡨࡶࡨࡿࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫର"), None)
      bstack1lllll1lll_opy_(driver, bstack1l1l1llll1_opy_, test)
  if (bstack1llllllll1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"ࠩ࡬ࡷࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭଱"), None) and
      bstack1llllllll1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩଲ"), None)) or (
      bstack1llllllll1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"ࠫ࡮ࡹࡁࡱࡲࡄ࠵࠶ࡿࡔࡦࡵࡷࠫଳ"), None) and
      bstack1llllllll1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"ࠬࡧࡰࡱࡃ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ଴"), None)):
      logger.info(bstack11l1l11_opy_ (u"ࠨࡁࡶࡶࡲࡱࡦࡺࡥࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨࠤࡪࡾࡥࡤࡷࡷ࡭ࡴࡴࠠࡩࡣࡶࠤࡪࡴࡤࡦࡦ࠱ࠤࡕࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡨࡲࡶࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡺࡥࡴࡶ࡬ࡲ࡬ࠦࡩࡴࠢࡸࡲࡩ࡫ࡲࡸࡣࡼ࠲ࠥࠨଵ"))
      bstack1l1l1l1ll1_opy_.bstack1ll11111l_opy_(driver, name=test.name, path=test.source)
def bstack11l111l11_opy_(test, bstack11ll11ll11_opy_):
    try:
      bstack1l1ll1l111_opy_ = datetime.datetime.now()
      data = {}
      if test:
        data[bstack11l1l11_opy_ (u"ࠧ࡯ࡣࡰࡩࠬଶ")] = bstack11ll11ll11_opy_
      if bstack1l1ll11l1l_opy_:
        if bstack1l1ll11l1l_opy_.status == bstack11l1l11_opy_ (u"ࠨࡒࡄࡗࡘ࠭ଷ"):
          data[bstack11l1l11_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩସ")] = bstack11l1l11_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪହ")
        elif bstack1l1ll11l1l_opy_.status == bstack11l1l11_opy_ (u"ࠫࡋࡇࡉࡍࠩ଺"):
          data[bstack11l1l11_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬ଻")] = bstack11l1l11_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ଼࠭")
          if bstack1l1ll11l1l_opy_.message:
            data[bstack11l1l11_opy_ (u"ࠧࡳࡧࡤࡷࡴࡴࠧଽ")] = str(bstack1l1ll11l1l_opy_.message)
      user = CONFIG[bstack11l1l11_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪା")]
      key = CONFIG[bstack11l1l11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬି")]
      url = bstack11l1l11_opy_ (u"ࠪ࡬ࡹࡺࡰࡴ࠼࠲࠳ࢀࢃ࠺ࡼࡿࡃࡥࡵ࡯࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡥࡺࡺ࡯࡮ࡣࡷࡩ࠴ࡹࡥࡴࡵ࡬ࡳࡳࡹ࠯ࡼࡿ࠱࡮ࡸࡵ࡮ࠨୀ").format(user, key, bstack1lll11111_opy_)
      headers = {
        bstack11l1l11_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲ࡺࡹࡱࡧࠪୁ"): bstack11l1l11_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨୂ"),
      }
      if bool(data):
        requests.put(url, json=data, headers=headers)
        cli.bstack1ll11lll_opy_(bstack11l1l11_opy_ (u"ࠨࡨࡵࡶࡳ࠾ࡺࡶࡤࡢࡶࡨࡣࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡷࡹࡧࡴࡶࡵࠥୃ"), datetime.datetime.now() - bstack1l1ll1l111_opy_)
    except Exception as e:
      logger.error(bstack1l11l111l1_opy_.format(str(e)))
def bstack1lll11l1l1_opy_(test, bstack11ll11ll11_opy_):
  global CONFIG
  global bstack1ll1llll1_opy_
  global bstack1l1ll1llll_opy_
  global bstack1lll11111_opy_
  global bstack1l1ll11l1l_opy_
  global bstack11l1l1lll_opy_
  global bstack11l1lll1l_opy_
  global bstack111ll11l_opy_
  global bstack1lll1lll_opy_
  global bstack1111ll1l_opy_
  global bstack1l11ll11l1_opy_
  global bstack1l11lll1ll_opy_
  try:
    if not bstack1lll11111_opy_:
      with open(os.path.join(os.path.expanduser(bstack11l1l11_opy_ (u"ࠧࡿࠩୄ")), bstack11l1l11_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨ୅"), bstack11l1l11_opy_ (u"ࠩ࠱ࡷࡪࡹࡳࡪࡱࡱ࡭ࡩࡹ࠮ࡵࡺࡷࠫ୆"))) as f:
        bstack11lll111l_opy_ = json.loads(bstack11l1l11_opy_ (u"ࠥࡿࠧେ") + f.read().strip() + bstack11l1l11_opy_ (u"ࠫࠧࡾࠢ࠻ࠢࠥࡽࠧ࠭ୈ") + bstack11l1l11_opy_ (u"ࠧࢃࠢ୉"))
        bstack1lll11111_opy_ = bstack11lll111l_opy_[str(threading.get_ident())]
  except:
    pass
  if bstack1l11ll11l1_opy_:
    for driver in bstack1l11ll11l1_opy_:
      if bstack1lll11111_opy_ == driver.session_id:
        if test:
          bstack1l11lll11_opy_(driver, test)
        bstack111lll111_opy_(driver, bstack11ll11ll11_opy_)
  elif bstack1lll11111_opy_:
    bstack11l111l11_opy_(test, bstack11ll11ll11_opy_)
  if bstack1ll1llll1_opy_:
    bstack111ll11l_opy_(bstack1ll1llll1_opy_)
  if bstack1l1ll1llll_opy_:
    bstack1lll1lll_opy_(bstack1l1ll1llll_opy_)
  if bstack11l1l1ll_opy_:
    bstack1111ll1l_opy_()
def bstack111ll1ll1_opy_(self, test, *args, **kwargs):
  bstack11ll11ll11_opy_ = None
  if test:
    bstack11ll11ll11_opy_ = str(test.name)
  bstack1lll11l1l1_opy_(test, bstack11ll11ll11_opy_)
  bstack11l1lll1l_opy_(self, test, *args, **kwargs)
def bstack1ll11l11_opy_(self, parent, test, skip_on_failure=None, rpa=False):
  global bstack1l1llll11_opy_
  global CONFIG
  global bstack1l11ll11l1_opy_
  global bstack1lll11111_opy_
  bstack1l1lll1l_opy_ = None
  try:
    if bstack1llllllll1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬ୊"), None) or bstack1llllllll1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"ࠧࡢࡲࡳࡅ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩୋ"), None):
      try:
        if not bstack1lll11111_opy_:
          with open(os.path.join(os.path.expanduser(bstack11l1l11_opy_ (u"ࠨࢀࠪୌ")), bstack11l1l11_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬୍ࠩ"), bstack11l1l11_opy_ (u"ࠪ࠲ࡸ࡫ࡳࡴ࡫ࡲࡲ࡮ࡪࡳ࠯ࡶࡻࡸࠬ୎"))) as f:
            bstack11lll111l_opy_ = json.loads(bstack11l1l11_opy_ (u"ࠦࢀࠨ୏") + f.read().strip() + bstack11l1l11_opy_ (u"ࠬࠨࡸࠣ࠼ࠣࠦࡾࠨࠧ୐") + bstack11l1l11_opy_ (u"ࠨࡽࠣ୑"))
            bstack1lll11111_opy_ = bstack11lll111l_opy_[str(threading.get_ident())]
      except:
        pass
      if bstack1l11ll11l1_opy_:
        for driver in bstack1l11ll11l1_opy_:
          if bstack1lll11111_opy_ == driver.session_id:
            bstack1l1lll1l_opy_ = driver
    bstack11l11llll1_opy_ = bstack1l1l1l1ll1_opy_.bstack11lll111_opy_(test.tags)
    if bstack1l1lll1l_opy_:
      threading.current_thread().isA11yTest = bstack1l1l1l1ll1_opy_.bstack1l111l11l1_opy_(bstack1l1lll1l_opy_, bstack11l11llll1_opy_)
      threading.current_thread().isAppA11yTest = bstack1l1l1l1ll1_opy_.bstack1l111l11l1_opy_(bstack1l1lll1l_opy_, bstack11l11llll1_opy_)
    else:
      threading.current_thread().isA11yTest = bstack11l11llll1_opy_
      threading.current_thread().isAppA11yTest = bstack11l11llll1_opy_
  except:
    pass
  bstack1l1llll11_opy_(self, parent, test, skip_on_failure=skip_on_failure, rpa=rpa)
  global bstack1l1ll11l1l_opy_
  try:
    bstack1l1ll11l1l_opy_ = self._test
  except:
    bstack1l1ll11l1l_opy_ = self.test
def bstack1llll11ll_opy_():
  global bstack1ll11l1ll1_opy_
  try:
    if os.path.exists(bstack1ll11l1ll1_opy_):
      os.remove(bstack1ll11l1ll1_opy_)
  except Exception as e:
    logger.debug(bstack11l1l11_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡧࡩࡱ࡫ࡴࡪࡰࡪࠤࡷࡵࡢࡰࡶࠣࡶࡪࡶ࡯ࡳࡶࠣࡪ࡮ࡲࡥ࠻ࠢࠪ୒") + str(e))
def bstack11l11l1ll_opy_():
  global bstack1ll11l1ll1_opy_
  bstack1lll1111_opy_ = {}
  try:
    if not os.path.isfile(bstack1ll11l1ll1_opy_):
      with open(bstack1ll11l1ll1_opy_, bstack11l1l11_opy_ (u"ࠨࡹࠪ୓")):
        pass
      with open(bstack1ll11l1ll1_opy_, bstack11l1l11_opy_ (u"ࠤࡺ࠯ࠧ୔")) as outfile:
        json.dump({}, outfile)
    if os.path.exists(bstack1ll11l1ll1_opy_):
      bstack1lll1111_opy_ = json.load(open(bstack1ll11l1ll1_opy_, bstack11l1l11_opy_ (u"ࠪࡶࡧ࠭୕")))
  except Exception as e:
    logger.debug(bstack11l1l11_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡲࡦࡣࡧ࡭ࡳ࡭ࠠࡳࡱࡥࡳࡹࠦࡲࡦࡲࡲࡶࡹࠦࡦࡪ࡮ࡨ࠾ࠥ࠭ୖ") + str(e))
  finally:
    return bstack1lll1111_opy_
def bstack1l11ll1ll1_opy_(platform_index, item_index):
  global bstack1ll11l1ll1_opy_
  try:
    bstack1lll1111_opy_ = bstack11l11l1ll_opy_()
    bstack1lll1111_opy_[item_index] = platform_index
    with open(bstack1ll11l1ll1_opy_, bstack11l1l11_opy_ (u"ࠧࡽࠫࠣୗ")) as outfile:
      json.dump(bstack1lll1111_opy_, outfile)
  except Exception as e:
    logger.debug(bstack11l1l11_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡹࡵ࡭ࡹ࡯࡮ࡨࠢࡷࡳࠥࡸ࡯ࡣࡱࡷࠤࡷ࡫ࡰࡰࡴࡷࠤ࡫࡯࡬ࡦ࠼ࠣࠫ୘") + str(e))
def bstack11l111ll_opy_(bstack1l1lll1l11_opy_):
  global CONFIG
  bstack11111llll_opy_ = bstack11l1l11_opy_ (u"ࠧࠨ୙")
  if not bstack11l1l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ୚") in CONFIG:
    logger.info(bstack11l1l11_opy_ (u"ࠩࡑࡳࠥࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠡࡲࡤࡷࡸ࡫ࡤࠡࡷࡱࡥࡧࡲࡥࠡࡶࡲࠤ࡬࡫࡮ࡦࡴࡤࡸࡪࠦࡲࡦࡲࡲࡶࡹࠦࡦࡰࡴࠣࡖࡴࡨ࡯ࡵࠢࡵࡹࡳ࠭୛"))
  try:
    platform = CONFIG[bstack11l1l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ଡ଼")][bstack1l1lll1l11_opy_]
    if bstack11l1l11_opy_ (u"ࠫࡴࡹࠧଢ଼") in platform:
      bstack11111llll_opy_ += str(platform[bstack11l1l11_opy_ (u"ࠬࡵࡳࠨ୞")]) + bstack11l1l11_opy_ (u"࠭ࠬࠡࠩୟ")
    if bstack11l1l11_opy_ (u"ࠧࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠪୠ") in platform:
      bstack11111llll_opy_ += str(platform[bstack11l1l11_opy_ (u"ࠨࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠫୡ")]) + bstack11l1l11_opy_ (u"ࠩ࠯ࠤࠬୢ")
    if bstack11l1l11_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧୣ") in platform:
      bstack11111llll_opy_ += str(platform[bstack11l1l11_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨ୤")]) + bstack11l1l11_opy_ (u"ࠬ࠲ࠠࠨ୥")
    if bstack11l1l11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ୦") in platform:
      bstack11111llll_opy_ += str(platform[bstack11l1l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩ୧")]) + bstack11l1l11_opy_ (u"ࠨ࠮ࠣࠫ୨")
    if bstack11l1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧ୩") in platform:
      bstack11111llll_opy_ += str(platform[bstack11l1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨ୪")]) + bstack11l1l11_opy_ (u"ࠫ࠱ࠦࠧ୫")
    if bstack11l1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭୬") in platform:
      bstack11111llll_opy_ += str(platform[bstack11l1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ୭")]) + bstack11l1l11_opy_ (u"ࠧ࠭ࠢࠪ୮")
  except Exception as e:
    logger.debug(bstack11l1l11_opy_ (u"ࠨࡕࡲࡱࡪࠦࡥࡳࡴࡲࡶࠥ࡯࡮ࠡࡩࡨࡲࡪࡸࡡࡵ࡫ࡱ࡫ࠥࡶ࡬ࡢࡶࡩࡳࡷࡳࠠࡴࡶࡵ࡭ࡳ࡭ࠠࡧࡱࡵࠤࡷ࡫ࡰࡰࡴࡷࠤ࡬࡫࡮ࡦࡴࡤࡸ࡮ࡵ࡮ࠨ୯") + str(e))
  finally:
    if bstack11111llll_opy_[len(bstack11111llll_opy_) - 2:] == bstack11l1l11_opy_ (u"ࠩ࠯ࠤࠬ୰"):
      bstack11111llll_opy_ = bstack11111llll_opy_[:-2]
    return bstack11111llll_opy_
def bstack111llll1_opy_(path, bstack11111llll_opy_):
  try:
    import xml.etree.ElementTree as ET
    bstack1l1111l1_opy_ = ET.parse(path)
    bstack1ll1111l1l_opy_ = bstack1l1111l1_opy_.getroot()
    bstack1lll1ll11_opy_ = None
    for suite in bstack1ll1111l1l_opy_.iter(bstack11l1l11_opy_ (u"ࠪࡷࡺ࡯ࡴࡦࠩୱ")):
      if bstack11l1l11_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫ୲") in suite.attrib:
        suite.attrib[bstack11l1l11_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ୳")] += bstack11l1l11_opy_ (u"࠭ࠠࠨ୴") + bstack11111llll_opy_
        bstack1lll1ll11_opy_ = suite
    bstack1lllll111_opy_ = None
    for robot in bstack1ll1111l1l_opy_.iter(bstack11l1l11_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭୵")):
      bstack1lllll111_opy_ = robot
    bstack1l1ll11l_opy_ = len(bstack1lllll111_opy_.findall(bstack11l1l11_opy_ (u"ࠨࡵࡸ࡭ࡹ࡫ࠧ୶")))
    if bstack1l1ll11l_opy_ == 1:
      bstack1lllll111_opy_.remove(bstack1lllll111_opy_.findall(bstack11l1l11_opy_ (u"ࠩࡶࡹ࡮ࡺࡥࠨ୷"))[0])
      bstack11111l1l1_opy_ = ET.Element(bstack11l1l11_opy_ (u"ࠪࡷࡺ࡯ࡴࡦࠩ୸"), attrib={bstack11l1l11_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ୹"): bstack11l1l11_opy_ (u"࡙ࠬࡵࡪࡶࡨࡷࠬ୺"), bstack11l1l11_opy_ (u"࠭ࡩࡥࠩ୻"): bstack11l1l11_opy_ (u"ࠧࡴ࠲ࠪ୼")})
      bstack1lllll111_opy_.insert(1, bstack11111l1l1_opy_)
      bstack11ll1llll1_opy_ = None
      for suite in bstack1lllll111_opy_.iter(bstack11l1l11_opy_ (u"ࠨࡵࡸ࡭ࡹ࡫ࠧ୽")):
        bstack11ll1llll1_opy_ = suite
      bstack11ll1llll1_opy_.append(bstack1lll1ll11_opy_)
      bstack1111lll1l_opy_ = None
      for status in bstack1lll1ll11_opy_.iter(bstack11l1l11_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ୾")):
        bstack1111lll1l_opy_ = status
      bstack11ll1llll1_opy_.append(bstack1111lll1l_opy_)
    bstack1l1111l1_opy_.write(path)
  except Exception as e:
    logger.debug(bstack11l1l11_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡶࡡࡳࡵ࡬ࡲ࡬ࠦࡷࡩ࡫࡯ࡩࠥ࡭ࡥ࡯ࡧࡵࡥࡹ࡯࡮ࡨࠢࡵࡳࡧࡵࡴࠡࡴࡨࡴࡴࡸࡴࠨ୿") + str(e))
def bstack1lll1l11_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name):
  global bstack11l1l11l_opy_
  global CONFIG
  if bstack11l1l11_opy_ (u"ࠦࡵࡿࡴࡩࡱࡱࡴࡦࡺࡨࠣ஀") in options:
    del options[bstack11l1l11_opy_ (u"ࠧࡶࡹࡵࡪࡲࡲࡵࡧࡴࡩࠤ஁")]
  bstack1llllll1ll_opy_ = bstack11l11l1ll_opy_()
  for bstack1llll1l1l1_opy_ in bstack1llllll1ll_opy_.keys():
    path = os.path.join(os.getcwd(), bstack11l1l11_opy_ (u"࠭ࡰࡢࡤࡲࡸࡤࡸࡥࡴࡷ࡯ࡸࡸ࠭ஂ"), str(bstack1llll1l1l1_opy_), bstack11l1l11_opy_ (u"ࠧࡰࡷࡷࡴࡺࡺ࠮ࡹ࡯࡯ࠫஃ"))
    bstack111llll1_opy_(path, bstack11l111ll_opy_(bstack1llllll1ll_opy_[bstack1llll1l1l1_opy_]))
  bstack1llll11ll_opy_()
  return bstack11l1l11l_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name)
def bstack1l111l11_opy_(self, ff_profile_dir):
  global bstack1lll11l1ll_opy_
  if not ff_profile_dir:
    return None
  return bstack1lll11l1ll_opy_(self, ff_profile_dir)
def bstack1ll111ll11_opy_(datasources, opts_for_run, outs_dir, pabot_args, suite_group):
  from pabot.pabot import QueueItem
  global CONFIG
  global bstack11l1ll1l1_opy_
  bstack1ll1l1l1l1_opy_ = []
  if bstack11l1l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ஄") in CONFIG:
    bstack1ll1l1l1l1_opy_ = CONFIG[bstack11l1l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬஅ")]
  return [
    QueueItem(
      datasources,
      outs_dir,
      opts_for_run,
      suite,
      pabot_args[bstack11l1l11_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࠦஆ")],
      pabot_args[bstack11l1l11_opy_ (u"ࠦࡻ࡫ࡲࡣࡱࡶࡩࠧஇ")],
      argfile,
      pabot_args.get(bstack11l1l11_opy_ (u"ࠧ࡮ࡩࡷࡧࠥஈ")),
      pabot_args[bstack11l1l11_opy_ (u"ࠨࡰࡳࡱࡦࡩࡸࡹࡥࡴࠤஉ")],
      platform[0],
      bstack11l1ll1l1_opy_
    )
    for suite in suite_group
    for argfile in pabot_args[bstack11l1l11_opy_ (u"ࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡨ࡬ࡰࡪࡹࠢஊ")] or [(bstack11l1l11_opy_ (u"ࠣࠤ஋"), None)]
    for platform in enumerate(bstack1ll1l1l1l1_opy_)
  ]
def bstack111l11111_opy_(self, datasources, outs_dir, options,
                        execution_item, command, verbose, argfile,
                        hive=None, processes=0, platform_index=0, bstack1lllll1ll_opy_=bstack11l1l11_opy_ (u"ࠩࠪ஌")):
  global bstack1ll111ll_opy_
  self.platform_index = platform_index
  self.bstack1lllll11ll_opy_ = bstack1lllll1ll_opy_
  bstack1ll111ll_opy_(self, datasources, outs_dir, options,
                      execution_item, command, verbose, argfile, hive, processes)
def bstack1l111ll1ll_opy_(caller_id, datasources, is_last, item, outs_dir):
  global bstack1l111l1l1_opy_
  global bstack1lll111l1_opy_
  bstack1ll11l1l11_opy_ = copy.deepcopy(item)
  if not bstack11l1l11_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬ஍") in item.options:
    bstack1ll11l1l11_opy_.options[bstack11l1l11_opy_ (u"ࠫࡻࡧࡲࡪࡣࡥࡰࡪ࠭எ")] = []
  bstack11ll11l1l_opy_ = bstack1ll11l1l11_opy_.options[bstack11l1l11_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧஏ")].copy()
  for v in bstack1ll11l1l11_opy_.options[bstack11l1l11_opy_ (u"࠭ࡶࡢࡴ࡬ࡥࡧࡲࡥࠨஐ")]:
    if bstack11l1l11_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡐࡍࡃࡗࡊࡔࡘࡍࡊࡐࡇࡉ࡝࠭஑") in v:
      bstack11ll11l1l_opy_.remove(v)
    if bstack11l1l11_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡄࡎࡌࡅࡗࡍࡓࠨஒ") in v:
      bstack11ll11l1l_opy_.remove(v)
    if bstack11l1l11_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡆࡈࡊࡑࡕࡃࡂࡎࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭ஓ") in v:
      bstack11ll11l1l_opy_.remove(v)
  bstack11ll11l1l_opy_.insert(0, bstack11l1l11_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡓࡐࡆ࡚ࡆࡐࡔࡐࡍࡓࡊࡅ࡙࠼ࡾࢁࠬஔ").format(bstack1ll11l1l11_opy_.platform_index))
  bstack11ll11l1l_opy_.insert(0, bstack11l1l11_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡈࡊࡌࡌࡐࡅࡄࡐࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒ࠻ࡽࢀࠫக").format(bstack1ll11l1l11_opy_.bstack1lllll11ll_opy_))
  bstack1ll11l1l11_opy_.options[bstack11l1l11_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧ஖")] = bstack11ll11l1l_opy_
  if bstack1lll111l1_opy_:
    bstack1ll11l1l11_opy_.options[bstack11l1l11_opy_ (u"࠭ࡶࡢࡴ࡬ࡥࡧࡲࡥࠨ஗")].insert(0, bstack11l1l11_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡃࡍࡋࡄࡖࡌ࡙࠺ࡼࡿࠪ஘").format(bstack1lll111l1_opy_))
  return bstack1l111l1l1_opy_(caller_id, datasources, is_last, bstack1ll11l1l11_opy_, outs_dir)
def bstack111ll1111_opy_(command, item_index):
  if bstack111ll1lll_opy_.get_property(bstack11l1l11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࠩங")):
    os.environ[bstack11l1l11_opy_ (u"ࠩࡆ࡙ࡗࡘࡅࡏࡖࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡊࡁࡕࡃࠪச")] = json.dumps(CONFIG[bstack11l1l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭஛")][item_index % bstack1l1lllllll_opy_])
  global bstack1lll111l1_opy_
  if bstack1lll111l1_opy_:
    command[0] = command[0].replace(bstack11l1l11_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪஜ"), bstack11l1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠱ࡸࡪ࡫ࠡࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠢ࠰࠱ࡧࡹࡴࡢࡥ࡮ࡣ࡮ࡺࡥ࡮ࡡ࡬ࡲࡩ࡫ࡸࠡࠩ஝") + str(
      item_index) + bstack11l1l11_opy_ (u"࠭ࠠࠨஞ") + bstack1lll111l1_opy_, 1)
  else:
    command[0] = command[0].replace(bstack11l1l11_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ட"),
                                    bstack11l1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠭ࡴࡦ࡮ࠤࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠥ࠳࠭ࡣࡵࡷࡥࡨࡱ࡟ࡪࡶࡨࡱࡤ࡯࡮ࡥࡧࡻࠤࠬ஠") + str(item_index), 1)
def bstack111ll1l1l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index):
  global bstack1l1l1ll111_opy_
  bstack111ll1111_opy_(command, item_index)
  return bstack1l1l1ll111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
def bstack1l11lll11l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir):
  global bstack1l1l1ll111_opy_
  bstack111ll1111_opy_(command, item_index)
  return bstack1l1l1ll111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
def bstack1ll11lll11_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout):
  global bstack1l1l1ll111_opy_
  bstack111ll1111_opy_(command, item_index)
  return bstack1l1l1ll111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
def is_driver_active(driver):
  return True if driver and driver.session_id else False
def bstack1l1l111l1_opy_(self, runner, quiet=False, capture=True):
  global bstack1l111l1lll_opy_
  bstack111l1111_opy_ = bstack1l111l1lll_opy_(self, runner, quiet=quiet, capture=capture)
  if self.exception:
    if not hasattr(runner, bstack11l1l11_opy_ (u"ࠩࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࡤࡧࡲࡳࠩ஡")):
      runner.exception_arr = []
    if not hasattr(runner, bstack11l1l11_opy_ (u"ࠪࡩࡽࡩ࡟ࡵࡴࡤࡧࡪࡨࡡࡤ࡭ࡢࡥࡷࡸࠧ஢")):
      runner.exc_traceback_arr = []
    runner.exception = self.exception
    runner.exc_traceback = self.exc_traceback
    runner.exception_arr.append(self.exception)
    runner.exc_traceback_arr.append(self.exc_traceback)
  return bstack111l1111_opy_
def bstack1lll1ll1l1_opy_(runner, hook_name, context, element, bstack11lll11l_opy_, *args):
  try:
    if runner.hooks.get(hook_name):
      bstack11l111111_opy_.bstack11111l11_opy_(hook_name, element)
    bstack11lll11l_opy_(runner, hook_name, context, *args)
    if runner.hooks.get(hook_name):
      bstack11l111111_opy_.bstack1lll1lll1l_opy_(element)
      if hook_name not in [bstack11l1l11_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࡣࡦࡲ࡬ࠨண"), bstack11l1l11_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡦࡲ࡬ࠨத")] and args and hasattr(args[0], bstack11l1l11_opy_ (u"࠭ࡥࡳࡴࡲࡶࡤࡳࡥࡴࡵࡤ࡫ࡪ࠭஥")):
        args[0].error_message = bstack11l1l11_opy_ (u"ࠧࠨ஦")
  except Exception as e:
    logger.debug(bstack11l1l11_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤ࡭ࡧ࡮ࡥ࡮ࡨࠤ࡭ࡵ࡯࡬ࡵࠣ࡭ࡳࠦࡢࡦࡪࡤࡺࡪࡀࠠࡼࡿࠪ஧").format(str(e)))
@measure(event_name=EVENTS.bstack1lll1ll1ll_opy_, stage=STAGE.bstack1l1ll1lll_opy_, hook_type=bstack11l1l11_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡃ࡯ࡰࠧந"), bstack11ll11ll11_opy_=bstack11l1l1lll_opy_)
def bstack11lll1111_opy_(runner, name, context, bstack11lll11l_opy_, *args):
    if runner.hooks.get(bstack11l1l11_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡥࡱࡲࠢன")).__name__ != bstack11l1l11_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡦࡲ࡬ࡠࡦࡨࡪࡦࡻ࡬ࡵࡡ࡫ࡳࡴࡱࠢப"):
      bstack1lll1ll1l1_opy_(runner, name, context, runner, bstack11lll11l_opy_, *args)
    try:
      threading.current_thread().bstackSessionDriver if bstack11lll11l1l_opy_(bstack11l1l11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫ஫")) else context.browser
      runner.driver_initialised = bstack11l1l11_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡡ࡭࡮ࠥ஬")
    except Exception as e:
      logger.debug(bstack11l1l11_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࠠࡥࡴ࡬ࡺࡪࡸࠠࡪࡰ࡬ࡸ࡮ࡧ࡬ࡪࡵࡨࠤࡦࡺࡴࡳ࡫ࡥࡹࡹ࡫࠺ࠡࡽࢀࠫ஭").format(str(e)))
def bstack1lll1ll1l_opy_(runner, name, context, bstack11lll11l_opy_, *args):
    bstack1lll1ll1l1_opy_(runner, name, context, context.feature, bstack11lll11l_opy_, *args)
    try:
      if not bstack1l1lllll1_opy_:
        bstack1l1lll1l_opy_ = threading.current_thread().bstackSessionDriver if bstack11lll11l1l_opy_(bstack11l1l11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧம")) else context.browser
        if is_driver_active(bstack1l1lll1l_opy_):
          if runner.driver_initialised is None: runner.driver_initialised = bstack11l1l11_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡩࡩࡦࡺࡵࡳࡧࠥய")
          bstack1l111lll_opy_ = str(runner.feature.name)
          bstack1l11ll1l11_opy_(context, bstack1l111lll_opy_)
          bstack1l1lll1l_opy_.execute_script(bstack11l1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢ࡯ࡣࡰࡩࠧࡀࠠࠨர") + json.dumps(bstack1l111lll_opy_) + bstack11l1l11_opy_ (u"ࠫࢂࢃࠧற"))
    except Exception as e:
      logger.debug(bstack11l1l11_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡨࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨࠤ࡮ࡴࠠࡣࡧࡩࡳࡷ࡫ࠠࡧࡧࡤࡸࡺࡸࡥ࠻ࠢࡾࢁࠬல").format(str(e)))
def bstack1l111l11l_opy_(runner, name, context, bstack11lll11l_opy_, *args):
    if hasattr(context, bstack11l1l11_opy_ (u"࠭ࡳࡤࡧࡱࡥࡷ࡯࡯ࠨள")):
        bstack11l111111_opy_.start_test(context)
    target = context.scenario if hasattr(context, bstack11l1l11_opy_ (u"ࠧࡴࡥࡨࡲࡦࡸࡩࡰࠩழ")) else context.feature
    bstack1lll1ll1l1_opy_(runner, name, context, target, bstack11lll11l_opy_, *args)
@measure(event_name=EVENTS.bstack1111ll111_opy_, stage=STAGE.bstack1l1ll1lll_opy_, bstack11ll11ll11_opy_=bstack11l1l1lll_opy_)
def bstack11ll1lll1_opy_(runner, name, context, bstack11lll11l_opy_, *args):
    if len(context.scenario.tags) == 0: bstack11l111111_opy_.start_test(context)
    bstack1lll1ll1l1_opy_(runner, name, context, context.scenario, bstack11lll11l_opy_, *args)
    threading.current_thread().a11y_stop = False
    bstack1lll1111l_opy_.bstack1ll1l11111_opy_(context, *args)
    try:
      bstack1l1lll1l_opy_ = bstack1llllllll1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧவ"), context.browser)
      if is_driver_active(bstack1l1lll1l_opy_):
        bstack11lll111l1_opy_.bstack11ll1111_opy_(bstack1llllllll1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨஶ"), {}))
        if runner.driver_initialised is None: runner.driver_initialised = bstack11l1l11_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠧஷ")
        if (not bstack1l1lllll1_opy_):
          scenario_name = args[0].name
          feature_name = bstack1l111lll_opy_ = str(runner.feature.name)
          bstack1l111lll_opy_ = feature_name + bstack11l1l11_opy_ (u"ࠫࠥ࠳ࠠࠨஸ") + scenario_name
          if runner.driver_initialised == bstack11l1l11_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠢஹ"):
            bstack1l11ll1l11_opy_(context, bstack1l111lll_opy_)
            bstack1l1lll1l_opy_.execute_script(bstack11l1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡲࡦࡳࡥࠣ࠼ࠣࠫ஺") + json.dumps(bstack1l111lll_opy_) + bstack11l1l11_opy_ (u"ࠧࡾࡿࠪ஻"))
    except Exception as e:
      logger.debug(bstack11l1l11_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫ࠠࡪࡰࠣࡦࡪ࡬࡯ࡳࡧࠣࡷࡨ࡫࡮ࡢࡴ࡬ࡳ࠿ࠦࡻࡾࠩ஼").format(str(e)))
@measure(event_name=EVENTS.bstack1lll1ll1ll_opy_, stage=STAGE.bstack1l1ll1lll_opy_, hook_type=bstack11l1l11_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡕࡷࡩࡵࠨ஽"), bstack11ll11ll11_opy_=bstack11l1l1lll_opy_)
def bstack1l1llll1l1_opy_(runner, name, context, bstack11lll11l_opy_, *args):
    bstack1lll1ll1l1_opy_(runner, name, context, args[0], bstack11lll11l_opy_, *args)
    try:
      bstack1l1lll1l_opy_ = threading.current_thread().bstackSessionDriver if bstack11lll11l1l_opy_(bstack11l1l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩா")) else context.browser
      if is_driver_active(bstack1l1lll1l_opy_):
        if runner.driver_initialised is None: runner.driver_initialised = bstack11l1l11_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡸࡺࡥࡱࠤி")
        bstack11l111111_opy_.bstack1l1lll11l1_opy_(args[0])
        if runner.driver_initialised == bstack11l1l11_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡹࡴࡦࡲࠥீ"):
          feature_name = bstack1l111lll_opy_ = str(runner.feature.name)
          bstack1l111lll_opy_ = feature_name + bstack11l1l11_opy_ (u"࠭ࠠ࠮ࠢࠪு") + context.scenario.name
          bstack1l1lll1l_opy_.execute_script(bstack11l1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡳࡧ࡭ࡦࠤ࠽ࠤࠬூ") + json.dumps(bstack1l111lll_opy_) + bstack11l1l11_opy_ (u"ࠨࡿࢀࠫ௃"))
    except Exception as e:
      logger.debug(bstack11l1l11_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡥࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥࠡ࡫ࡱࠤࡧ࡫ࡦࡰࡴࡨࠤࡸࡺࡥࡱ࠼ࠣࡿࢂ࠭௄").format(str(e)))
@measure(event_name=EVENTS.bstack1lll1ll1ll_opy_, stage=STAGE.bstack1l1ll1lll_opy_, hook_type=bstack11l1l11_opy_ (u"ࠥࡥ࡫ࡺࡥࡳࡕࡷࡩࡵࠨ௅"), bstack11ll11ll11_opy_=bstack11l1l1lll_opy_)
def bstack1l1l1l1lll_opy_(runner, name, context, bstack11lll11l_opy_, *args):
  bstack11l111111_opy_.bstack1111l11l1_opy_(args[0])
  try:
    bstack1lll1llll1_opy_ = args[0].status.name
    bstack1l1lll1l_opy_ = threading.current_thread().bstackSessionDriver if bstack11l1l11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪெ") in threading.current_thread().__dict__.keys() else context.browser
    if is_driver_active(bstack1l1lll1l_opy_):
      if runner.driver_initialised is None:
        runner.driver_initialised  = bstack11l1l11_opy_ (u"ࠬ࡯࡮ࡴࡶࡨࡴࠬே")
        feature_name = bstack1l111lll_opy_ = str(runner.feature.name)
        bstack1l111lll_opy_ = feature_name + bstack11l1l11_opy_ (u"࠭ࠠ࠮ࠢࠪை") + context.scenario.name
        bstack1l1lll1l_opy_.execute_script(bstack11l1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡳࡧ࡭ࡦࠤ࠽ࠤࠬ௉") + json.dumps(bstack1l111lll_opy_) + bstack11l1l11_opy_ (u"ࠨࡿࢀࠫொ"))
    if str(bstack1lll1llll1_opy_).lower() == bstack11l1l11_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩோ"):
      bstack1ll11l1111_opy_ = bstack11l1l11_opy_ (u"ࠪࠫௌ")
      bstack1l1l11ll_opy_ = bstack11l1l11_opy_ (u"்ࠫࠬ")
      bstack1l11l11l11_opy_ = bstack11l1l11_opy_ (u"ࠬ࠭௎")
      try:
        import traceback
        bstack1ll11l1111_opy_ = runner.exception.__class__.__name__
        bstack1llllll111_opy_ = traceback.format_tb(runner.exc_traceback)
        bstack1l1l11ll_opy_ = bstack11l1l11_opy_ (u"࠭ࠠࠨ௏").join(bstack1llllll111_opy_)
        bstack1l11l11l11_opy_ = bstack1llllll111_opy_[-1]
      except Exception as e:
        logger.debug(bstack1l1llll11l_opy_.format(str(e)))
      bstack1ll11l1111_opy_ += bstack1l11l11l11_opy_
      bstack1lll111l1l_opy_(context, json.dumps(str(args[0].name) + bstack11l1l11_opy_ (u"ࠢࠡ࠯ࠣࡊࡦ࡯࡬ࡦࡦࠤࡠࡳࠨௐ") + str(bstack1l1l11ll_opy_)),
                          bstack11l1l11_opy_ (u"ࠣࡧࡵࡶࡴࡸࠢ௑"))
      if runner.driver_initialised == bstack11l1l11_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡶࡸࡪࡶࠢ௒"):
        bstack1llll1lll1_opy_(getattr(context, bstack11l1l11_opy_ (u"ࠪࡴࡦ࡭ࡥࠨ௓"), None), bstack11l1l11_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦ௔"), bstack1ll11l1111_opy_)
        bstack1l1lll1l_opy_.execute_script(bstack11l1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡨࡦࡺࡡࠣ࠼ࠪ௕") + json.dumps(str(args[0].name) + bstack11l1l11_opy_ (u"ࠨࠠ࠮ࠢࡉࡥ࡮ࡲࡥࡥࠣ࡟ࡲࠧ௖") + str(bstack1l1l11ll_opy_)) + bstack11l1l11_opy_ (u"ࠧ࠭ࠢࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠤࠧ࡫ࡲࡳࡱࡵࠦࢂࢃࠧௗ"))
      if runner.driver_initialised == bstack11l1l11_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡵࡷࡩࡵࠨ௘"):
        bstack1l1l1l11l1_opy_(bstack1l1lll1l_opy_, bstack11l1l11_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ௙"), bstack11l1l11_opy_ (u"ࠥࡗࡨ࡫࡮ࡢࡴ࡬ࡳࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡽࡩࡵࡪ࠽ࠤࡡࡴࠢ௚") + str(bstack1ll11l1111_opy_))
    else:
      bstack1lll111l1l_opy_(context, bstack11l1l11_opy_ (u"ࠦࡕࡧࡳࡴࡧࡧࠥࠧ௛"), bstack11l1l11_opy_ (u"ࠧ࡯࡮ࡧࡱࠥ௜"))
      if runner.driver_initialised == bstack11l1l11_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡵࡧࡳࠦ௝"):
        bstack1llll1lll1_opy_(getattr(context, bstack11l1l11_opy_ (u"ࠧࡱࡣࡪࡩࠬ௞"), None), bstack11l1l11_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣ௟"))
      bstack1l1lll1l_opy_.execute_script(bstack11l1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡥࡣࡷࡥࠧࡀࠧ௠") + json.dumps(str(args[0].name) + bstack11l1l11_opy_ (u"ࠥࠤ࠲ࠦࡐࡢࡵࡶࡩࡩࠧࠢ௡")) + bstack11l1l11_opy_ (u"ࠫ࠱ࠦࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠡࠤ࡬ࡲ࡫ࡵࠢࡾࡿࠪ௢"))
      if runner.driver_initialised == bstack11l1l11_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡹࡴࡦࡲࠥ௣"):
        bstack1l1l1l11l1_opy_(bstack1l1lll1l_opy_, bstack11l1l11_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨ௤"))
  except Exception as e:
    logger.debug(bstack11l1l11_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡱࡦࡸ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡶࡸࡦࡺࡵࡴࠢ࡬ࡲࠥࡧࡦࡵࡧࡵࠤࡸࡺࡥࡱ࠼ࠣࡿࢂ࠭௥").format(str(e)))
  bstack1lll1ll1l1_opy_(runner, name, context, args[0], bstack11lll11l_opy_, *args)
@measure(event_name=EVENTS.bstack1ll1ll1l1l_opy_, stage=STAGE.bstack1l1ll1lll_opy_, bstack11ll11ll11_opy_=bstack11l1l1lll_opy_)
def bstack1l1llll1_opy_(runner, name, context, bstack11lll11l_opy_, *args):
  bstack11l111111_opy_.end_test(args[0])
  try:
    bstack11l11lll1l_opy_ = args[0].status.name
    bstack1l1lll1l_opy_ = bstack1llllllll1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧ௦"), context.browser)
    bstack1lll1111l_opy_.bstack11111lll_opy_(bstack1l1lll1l_opy_)
    if str(bstack11l11lll1l_opy_).lower() == bstack11l1l11_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ௧"):
      bstack1ll11l1111_opy_ = bstack11l1l11_opy_ (u"ࠪࠫ௨")
      bstack1l1l11ll_opy_ = bstack11l1l11_opy_ (u"ࠫࠬ௩")
      bstack1l11l11l11_opy_ = bstack11l1l11_opy_ (u"ࠬ࠭௪")
      try:
        import traceback
        bstack1ll11l1111_opy_ = runner.exception.__class__.__name__
        bstack1llllll111_opy_ = traceback.format_tb(runner.exc_traceback)
        bstack1l1l11ll_opy_ = bstack11l1l11_opy_ (u"࠭ࠠࠨ௫").join(bstack1llllll111_opy_)
        bstack1l11l11l11_opy_ = bstack1llllll111_opy_[-1]
      except Exception as e:
        logger.debug(bstack1l1llll11l_opy_.format(str(e)))
      bstack1ll11l1111_opy_ += bstack1l11l11l11_opy_
      bstack1lll111l1l_opy_(context, json.dumps(str(args[0].name) + bstack11l1l11_opy_ (u"ࠢࠡ࠯ࠣࡊࡦ࡯࡬ࡦࡦࠤࡠࡳࠨ௬") + str(bstack1l1l11ll_opy_)),
                          bstack11l1l11_opy_ (u"ࠣࡧࡵࡶࡴࡸࠢ௭"))
      if runner.driver_initialised == bstack11l1l11_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠦ௮") or runner.driver_initialised == bstack11l1l11_opy_ (u"ࠪ࡭ࡳࡹࡴࡦࡲࠪ௯"):
        bstack1llll1lll1_opy_(getattr(context, bstack11l1l11_opy_ (u"ࠫࡵࡧࡧࡦࠩ௰"), None), bstack11l1l11_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧ௱"), bstack1ll11l1111_opy_)
        bstack1l1lll1l_opy_.execute_script(bstack11l1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡩࡧࡴࡢࠤ࠽ࠫ௲") + json.dumps(str(args[0].name) + bstack11l1l11_opy_ (u"ࠢࠡ࠯ࠣࡊࡦ࡯࡬ࡦࡦࠤࡠࡳࠨ௳") + str(bstack1l1l11ll_opy_)) + bstack11l1l11_opy_ (u"ࠨ࠮ࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡥࡳࡴࡲࡶࠧࢃࡽࠨ௴"))
      if runner.driver_initialised == bstack11l1l11_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠦ௵") or runner.driver_initialised == bstack11l1l11_opy_ (u"ࠪ࡭ࡳࡹࡴࡦࡲࠪ௶"):
        bstack1l1l1l11l1_opy_(bstack1l1lll1l_opy_, bstack11l1l11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ௷"), bstack11l1l11_opy_ (u"࡙ࠧࡣࡦࡰࡤࡶ࡮ࡵࠠࡧࡣ࡬ࡰࡪࡪࠠࡸ࡫ࡷ࡬࠿ࠦ࡜࡯ࠤ௸") + str(bstack1ll11l1111_opy_))
    else:
      bstack1lll111l1l_opy_(context, bstack11l1l11_opy_ (u"ࠨࡐࡢࡵࡶࡩࡩࠧࠢ௹"), bstack11l1l11_opy_ (u"ࠢࡪࡰࡩࡳࠧ௺"))
      if runner.driver_initialised == bstack11l1l11_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡵࡦࡩࡳࡧࡲࡪࡱࠥ௻") or runner.driver_initialised == bstack11l1l11_opy_ (u"ࠩ࡬ࡲࡸࡺࡥࡱࠩ௼"):
        bstack1llll1lll1_opy_(getattr(context, bstack11l1l11_opy_ (u"ࠪࡴࡦ࡭ࡥࠨ௽"), None), bstack11l1l11_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦ௾"))
      bstack1l1lll1l_opy_.execute_script(bstack11l1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡨࡦࡺࡡࠣ࠼ࠪ௿") + json.dumps(str(args[0].name) + bstack11l1l11_opy_ (u"ࠨࠠ࠮ࠢࡓࡥࡸࡹࡥࡥࠣࠥఀ")) + bstack11l1l11_opy_ (u"ࠧ࠭ࠢࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠤࠧ࡯࡮ࡧࡱࠥࢁࢂ࠭ఁ"))
      if runner.driver_initialised == bstack11l1l11_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡵࡦࡩࡳࡧࡲࡪࡱࠥం") or runner.driver_initialised == bstack11l1l11_opy_ (u"ࠩ࡬ࡲࡸࡺࡥࡱࠩః"):
        bstack1l1l1l11l1_opy_(bstack1l1lll1l_opy_, bstack11l1l11_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥఄ"))
  except Exception as e:
    logger.debug(bstack11l1l11_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠ࡮ࡣࡵ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡳࡵࡣࡷࡹࡸࠦࡩ࡯ࠢࡤࡪࡹ࡫ࡲࠡࡨࡨࡥࡹࡻࡲࡦ࠼ࠣࡿࢂ࠭అ").format(str(e)))
  bstack1lll1ll1l1_opy_(runner, name, context, context.scenario, bstack11lll11l_opy_, *args)
  if len(context.scenario.tags) == 0: threading.current_thread().current_test_uuid = None
def bstack1l11lll1_opy_(runner, name, context, bstack11lll11l_opy_, *args):
    target = context.scenario if hasattr(context, bstack11l1l11_opy_ (u"ࠬࡹࡣࡦࡰࡤࡶ࡮ࡵࠧఆ")) else context.feature
    bstack1lll1ll1l1_opy_(runner, name, context, target, bstack11lll11l_opy_, *args)
    threading.current_thread().current_test_uuid = None
def bstack1l1l11l1l_opy_(runner, name, context, bstack11lll11l_opy_, *args):
    try:
      bstack1l1lll1l_opy_ = bstack1llllllll1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬఇ"), context.browser)
      bstack11lll11ll_opy_ = bstack11l1l11_opy_ (u"ࠧࠨఈ")
      if context.failed is True:
        bstack1l1l1ll1_opy_ = []
        bstack1l1l1l11l_opy_ = []
        bstack11ll11l1ll_opy_ = []
        try:
          import traceback
          for exc in runner.exception_arr:
            bstack1l1l1ll1_opy_.append(exc.__class__.__name__)
          for exc_tb in runner.exc_traceback_arr:
            bstack1llllll111_opy_ = traceback.format_tb(exc_tb)
            bstack1ll11lll1l_opy_ = bstack11l1l11_opy_ (u"ࠨࠢࠪఉ").join(bstack1llllll111_opy_)
            bstack1l1l1l11l_opy_.append(bstack1ll11lll1l_opy_)
            bstack11ll11l1ll_opy_.append(bstack1llllll111_opy_[-1])
        except Exception as e:
          logger.debug(bstack1l1llll11l_opy_.format(str(e)))
        bstack1ll11l1111_opy_ = bstack11l1l11_opy_ (u"ࠩࠪఊ")
        for i in range(len(bstack1l1l1ll1_opy_)):
          bstack1ll11l1111_opy_ += bstack1l1l1ll1_opy_[i] + bstack11ll11l1ll_opy_[i] + bstack11l1l11_opy_ (u"ࠪࡠࡳ࠭ఋ")
        bstack11lll11ll_opy_ = bstack11l1l11_opy_ (u"ࠫࠥ࠭ఌ").join(bstack1l1l1l11l_opy_)
        if runner.driver_initialised in [bstack11l1l11_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤ࡬ࡥࡢࡶࡸࡶࡪࠨ఍"), bstack11l1l11_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡡ࡭࡮ࠥఎ")]:
          bstack1lll111l1l_opy_(context, bstack11lll11ll_opy_, bstack11l1l11_opy_ (u"ࠢࡦࡴࡵࡳࡷࠨఏ"))
          bstack1llll1lll1_opy_(getattr(context, bstack11l1l11_opy_ (u"ࠨࡲࡤ࡫ࡪ࠭ఐ"), None), bstack11l1l11_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤ఑"), bstack1ll11l1111_opy_)
          bstack1l1lll1l_opy_.execute_script(bstack11l1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡦࡤࡸࡦࠨ࠺ࠨఒ") + json.dumps(bstack11lll11ll_opy_) + bstack11l1l11_opy_ (u"ࠫ࠱ࠦࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠡࠤࡨࡶࡷࡵࡲࠣࡿࢀࠫఓ"))
          bstack1l1l1l11l1_opy_(bstack1l1lll1l_opy_, bstack11l1l11_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧఔ"), bstack11l1l11_opy_ (u"ࠨࡓࡰ࡯ࡨࠤࡸࡩࡥ࡯ࡣࡵ࡭ࡴࡹࠠࡧࡣ࡬ࡰࡪࡪ࠺ࠡ࡞ࡱࠦక") + str(bstack1ll11l1111_opy_))
          bstack11ll111ll1_opy_ = bstack1111llll1_opy_(bstack11lll11ll_opy_, runner.feature.name, logger)
          if (bstack11ll111ll1_opy_ != None):
            bstack11l1l1l1ll_opy_.append(bstack11ll111ll1_opy_)
      else:
        if runner.driver_initialised in [bstack11l1l11_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡧࡧࡤࡸࡺࡸࡥࠣఖ"), bstack11l1l11_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡣ࡯ࡰࠧగ")]:
          bstack1lll111l1l_opy_(context, bstack11l1l11_opy_ (u"ࠤࡉࡩࡦࡺࡵࡳࡧ࠽ࠤࠧఘ") + str(runner.feature.name) + bstack11l1l11_opy_ (u"ࠥࠤࡵࡧࡳࡴࡧࡧࠥࠧఙ"), bstack11l1l11_opy_ (u"ࠦ࡮ࡴࡦࡰࠤచ"))
          bstack1llll1lll1_opy_(getattr(context, bstack11l1l11_opy_ (u"ࠬࡶࡡࡨࡧࠪఛ"), None), bstack11l1l11_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨజ"))
          bstack1l1lll1l_opy_.execute_script(bstack11l1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡪࡡࡵࡣࠥ࠾ࠬఝ") + json.dumps(bstack11l1l11_opy_ (u"ࠣࡈࡨࡥࡹࡻࡲࡦ࠼ࠣࠦఞ") + str(runner.feature.name) + bstack11l1l11_opy_ (u"ࠤࠣࡴࡦࡹࡳࡦࡦࠤࠦట")) + bstack11l1l11_opy_ (u"ࠪ࠰ࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣ࡫ࡱࡪࡴࠨࡽࡾࠩఠ"))
          bstack1l1l1l11l1_opy_(bstack1l1lll1l_opy_, bstack11l1l11_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫడ"))
          bstack11ll111ll1_opy_ = bstack1111llll1_opy_(bstack11lll11ll_opy_, runner.feature.name, logger)
          if (bstack11ll111ll1_opy_ != None):
            bstack11l1l1l1ll_opy_.append(bstack11ll111ll1_opy_)
    except Exception as e:
      logger.debug(bstack11l1l11_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡ࡯ࡤࡶࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡴࡶࡤࡸࡺࡹࠠࡪࡰࠣࡥ࡫ࡺࡥࡳࠢࡩࡩࡦࡺࡵࡳࡧ࠽ࠤࢀࢃࠧఢ").format(str(e)))
    bstack1lll1ll1l1_opy_(runner, name, context, context.feature, bstack11lll11l_opy_, *args)
@measure(event_name=EVENTS.bstack1lll1ll1ll_opy_, stage=STAGE.bstack1l1ll1lll_opy_, hook_type=bstack11l1l11_opy_ (u"ࠨࡡࡧࡶࡨࡶࡆࡲ࡬ࠣణ"), bstack11ll11ll11_opy_=bstack11l1l1lll_opy_)
def bstack1ll1lll1l1_opy_(runner, name, context, bstack11lll11l_opy_, *args):
    bstack1lll1ll1l1_opy_(runner, name, context, runner, bstack11lll11l_opy_, *args)
def bstack1l1lllll11_opy_(self, name, context, *args):
  if bstack1l111ll111_opy_:
    platform_index = int(threading.current_thread()._name) % bstack1l1lllllll_opy_
    bstack1ll1l1lll_opy_ = CONFIG[bstack11l1l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪత")][platform_index]
    os.environ[bstack11l1l11_opy_ (u"ࠨࡅࡘࡖࡗࡋࡎࡕࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡉࡇࡔࡂࠩథ")] = json.dumps(bstack1ll1l1lll_opy_)
  global bstack11lll11l_opy_
  if not hasattr(self, bstack11l1l11_opy_ (u"ࠩࡧࡶ࡮ࡼࡥࡳࡡ࡬ࡲ࡮ࡺࡩࡢ࡮࡬ࡷࡪࡪࠧద")):
    self.driver_initialised = None
  bstack1lll1lll1_opy_ = {
      bstack11l1l11_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࡢࡥࡱࡲࠧధ"): bstack11lll1111_opy_,
      bstack11l1l11_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࡣ࡫࡫ࡡࡵࡷࡵࡩࠬన"): bstack1lll1ll1l_opy_,
      bstack11l1l11_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࡤࡺࡡࡨࠩ఩"): bstack1l111l11l_opy_,
      bstack11l1l11_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠨప"): bstack11ll1lll1_opy_,
      bstack11l1l11_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫࡟ࡴࡶࡨࡴࠬఫ"): bstack1l1llll1l1_opy_,
      bstack11l1l11_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡴࡶࡨࡴࠬబ"): bstack1l1l1l1lll_opy_,
      bstack11l1l11_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡵࡦࡩࡳࡧࡲࡪࡱࠪభ"): bstack1l1llll1_opy_,
      bstack11l1l11_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡷࡥ࡬࠭మ"): bstack1l11lll1_opy_,
      bstack11l1l11_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡪࡪࡧࡴࡶࡴࡨࠫయ"): bstack1l1l11l1l_opy_,
      bstack11l1l11_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡦࡲ࡬ࠨర"): bstack1ll1lll1l1_opy_
  }
  handler = bstack1lll1lll1_opy_.get(name, bstack11lll11l_opy_)
  handler(self, name, context, bstack11lll11l_opy_, *args)
  if name in [bstack11l1l11_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤ࡬ࡥࡢࡶࡸࡶࡪ࠭ఱ"), bstack11l1l11_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠨల"), bstack11l1l11_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡢ࡮࡯ࠫళ")]:
    try:
      bstack1l1lll1l_opy_ = threading.current_thread().bstackSessionDriver if bstack11lll11l1l_opy_(bstack11l1l11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨఴ")) else context.browser
      bstack11lll111ll_opy_ = (
        (name == bstack11l1l11_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡤࡰࡱ࠭వ") and self.driver_initialised == bstack11l1l11_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡦࡲ࡬ࠣశ")) or
        (name == bstack11l1l11_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣ࡫࡫ࡡࡵࡷࡵࡩࠬష") and self.driver_initialised == bstack11l1l11_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡦࡦࡣࡷࡹࡷ࡫ࠢస")) or
        (name == bstack11l1l11_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠨహ") and self.driver_initialised in [bstack11l1l11_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡵࡦࡩࡳࡧࡲࡪࡱࠥ఺"), bstack11l1l11_opy_ (u"ࠤ࡬ࡲࡸࡺࡥࡱࠤ఻")]) or
        (name == bstack11l1l11_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡶࡸࡪࡶ఼ࠧ") and self.driver_initialised == bstack11l1l11_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡸࡺࡥࡱࠤఽ"))
      )
      if bstack11lll111ll_opy_:
        self.driver_initialised = None
        bstack1l1lll1l_opy_.quit()
    except Exception:
      pass
def bstack111lllll_opy_(config, startdir):
  return bstack11l1l11_opy_ (u"ࠧࡪࡲࡪࡸࡨࡶ࠿ࠦࡻ࠱ࡿࠥా").format(bstack11l1l11_opy_ (u"ࠨࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠧి"))
notset = Notset()
def bstack1l1lll11_opy_(self, name: str, default=notset, skip: bool = False):
  global bstack11llll11ll_opy_
  if str(name).lower() == bstack11l1l11_opy_ (u"ࠧࡥࡴ࡬ࡺࡪࡸࠧీ"):
    return bstack11l1l11_opy_ (u"ࠣࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠢు")
  else:
    return bstack11llll11ll_opy_(self, name, default, skip)
def bstack1ll1ll11ll_opy_(item, when):
  global bstack1l1111ll1l_opy_
  try:
    bstack1l1111ll1l_opy_(item, when)
  except Exception as e:
    pass
def bstack1ll111l11_opy_():
  return
def bstack11ll11111_opy_(type, name, status, reason, bstack1ll111l1l1_opy_, bstack1l111lllll_opy_):
  bstack1l1ll11ll1_opy_ = {
    bstack11l1l11_opy_ (u"ࠩࡤࡧࡹ࡯࡯࡯ࠩూ"): type,
    bstack11l1l11_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ృ"): {}
  }
  if type == bstack11l1l11_opy_ (u"ࠫࡦࡴ࡮ࡰࡶࡤࡸࡪ࠭ౄ"):
    bstack1l1ll11ll1_opy_[bstack11l1l11_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨ౅")][bstack11l1l11_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬె")] = bstack1ll111l1l1_opy_
    bstack1l1ll11ll1_opy_[bstack11l1l11_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪే")][bstack11l1l11_opy_ (u"ࠨࡦࡤࡸࡦ࠭ై")] = json.dumps(str(bstack1l111lllll_opy_))
  if type == bstack11l1l11_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ౉"):
    bstack1l1ll11ll1_opy_[bstack11l1l11_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ొ")][bstack11l1l11_opy_ (u"ࠫࡳࡧ࡭ࡦࠩో")] = name
  if type == bstack11l1l11_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠨౌ"):
    bstack1l1ll11ll1_opy_[bstack11l1l11_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴ్ࠩ")][bstack11l1l11_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ౎")] = status
    if status == bstack11l1l11_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ౏"):
      bstack1l1ll11ll1_opy_[bstack11l1l11_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬ౐")][bstack11l1l11_opy_ (u"ࠪࡶࡪࡧࡳࡰࡰࠪ౑")] = json.dumps(str(reason))
  bstack11ll111ll_opy_ = bstack11l1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠩ౒").format(json.dumps(bstack1l1ll11ll1_opy_))
  return bstack11ll111ll_opy_
def bstack1ll11ll1_opy_(driver_command, response):
    if driver_command == bstack11l1l11_opy_ (u"ࠬࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠩ౓"):
        bstack11lll111l1_opy_.bstack11ll1111ll_opy_({
            bstack11l1l11_opy_ (u"࠭ࡩ࡮ࡣࡪࡩࠬ౔"): response[bstack11l1l11_opy_ (u"ࠧࡷࡣ࡯ࡹࡪౕ࠭")],
            bstack11l1l11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨౖ"): bstack11lll111l1_opy_.current_test_uuid()
        })
def bstack1l1ll1ll1_opy_(item, call, rep):
  global bstack11ll11lll_opy_
  global bstack1l11ll11l1_opy_
  global bstack1l1lllll1_opy_
  name = bstack11l1l11_opy_ (u"ࠩࠪ౗")
  try:
    if rep.when == bstack11l1l11_opy_ (u"ࠪࡧࡦࡲ࡬ࠨౘ"):
      bstack1lll11111_opy_ = threading.current_thread().bstackSessionId
      try:
        if not bstack1l1lllll1_opy_:
          name = str(rep.nodeid)
          bstack1l11lll111_opy_ = bstack11ll11111_opy_(bstack11l1l11_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬౙ"), name, bstack11l1l11_opy_ (u"ࠬ࠭ౚ"), bstack11l1l11_opy_ (u"࠭ࠧ౛"), bstack11l1l11_opy_ (u"ࠧࠨ౜"), bstack11l1l11_opy_ (u"ࠨࠩౝ"))
          threading.current_thread().bstack1l11llll11_opy_ = name
          for driver in bstack1l11ll11l1_opy_:
            if bstack1lll11111_opy_ == driver.session_id:
              driver.execute_script(bstack1l11lll111_opy_)
      except Exception as e:
        logger.debug(bstack11l1l11_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠣࡪࡴࡸࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠿ࠦࡻࡾࠩ౞").format(str(e)))
      try:
        bstack111l1l1l1_opy_(rep.outcome.lower())
        if rep.outcome.lower() != bstack11l1l11_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫ౟"):
          status = bstack11l1l11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫౠ") if rep.outcome.lower() == bstack11l1l11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬౡ") else bstack11l1l11_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ౢ")
          reason = bstack11l1l11_opy_ (u"ࠧࠨౣ")
          if status == bstack11l1l11_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ౤"):
            reason = rep.longrepr.reprcrash.message
            if (not threading.current_thread().bstackTestErrorMessages):
              threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(reason)
          level = bstack11l1l11_opy_ (u"ࠩ࡬ࡲ࡫ࡵࠧ౥") if status == bstack11l1l11_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪ౦") else bstack11l1l11_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪ౧")
          data = name + bstack11l1l11_opy_ (u"ࠬࠦࡰࡢࡵࡶࡩࡩࠧࠧ౨") if status == bstack11l1l11_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭౩") else name + bstack11l1l11_opy_ (u"ࠧࠡࡨࡤ࡭ࡱ࡫ࡤࠢࠢࠪ౪") + reason
          bstack11l1l11l1l_opy_ = bstack11ll11111_opy_(bstack11l1l11_opy_ (u"ࠨࡣࡱࡲࡴࡺࡡࡵࡧࠪ౫"), bstack11l1l11_opy_ (u"ࠩࠪ౬"), bstack11l1l11_opy_ (u"ࠪࠫ౭"), bstack11l1l11_opy_ (u"ࠫࠬ౮"), level, data)
          for driver in bstack1l11ll11l1_opy_:
            if bstack1lll11111_opy_ == driver.session_id:
              driver.execute_script(bstack11l1l11l1l_opy_)
      except Exception as e:
        logger.debug(bstack11l1l11_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡦࡳࡳࡺࡥࡹࡶࠣࡪࡴࡸࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠿ࠦࡻࡾࠩ౯").format(str(e)))
  except Exception as e:
    logger.debug(bstack11l1l11_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡶࡸࡦࡺࡥࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡶࡨࡷࡹࠦࡳࡵࡣࡷࡹࡸࡀࠠࡼࡿࠪ౰").format(str(e)))
  bstack11ll11lll_opy_(item, call, rep)
def bstack1lllll1lll_opy_(driver, bstack11l11ll1l1_opy_, test=None):
  global bstack1l1ll11111_opy_
  if test != None:
    bstack1ll11l111l_opy_ = getattr(test, bstack11l1l11_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ౱"), None)
    bstack1ll111l1ll_opy_ = getattr(test, bstack11l1l11_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭౲"), None)
    PercySDK.screenshot(driver, bstack11l11ll1l1_opy_, bstack1ll11l111l_opy_=bstack1ll11l111l_opy_, bstack1ll111l1ll_opy_=bstack1ll111l1ll_opy_, bstack11l11111l_opy_=bstack1l1ll11111_opy_)
  else:
    PercySDK.screenshot(driver, bstack11l11ll1l1_opy_)
@measure(event_name=EVENTS.bstack1ll1l1ll1l_opy_, stage=STAGE.bstack1l1ll1lll_opy_, bstack11ll11ll11_opy_=bstack11l1l1lll_opy_)
def bstack1111111l_opy_(driver):
  if bstack1l111llll_opy_.bstack1l111l1111_opy_() is True or bstack1l111llll_opy_.capturing() is True:
    return
  bstack1l111llll_opy_.bstack11llllll1l_opy_()
  while not bstack1l111llll_opy_.bstack1l111l1111_opy_():
    bstack1l11l1l11_opy_ = bstack1l111llll_opy_.bstack11lll1111l_opy_()
    bstack1lllll1lll_opy_(driver, bstack1l11l1l11_opy_)
  bstack1l111llll_opy_.bstack11l1llll1_opy_()
def bstack1lll111l_opy_(sequence, driver_command, response = None, bstack1l111ll11l_opy_ = None, args = None):
    try:
      if sequence != bstack11l1l11_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࠩ౳"):
        return
      if percy.bstack1ll1111111_opy_() == bstack11l1l11_opy_ (u"ࠥࡪࡦࡲࡳࡦࠤ౴"):
        return
      bstack1l11l1l11_opy_ = bstack1llllllll1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ౵"), None)
      for command in bstack11ll111l1l_opy_:
        if command == driver_command:
          for driver in bstack1l11ll11l1_opy_:
            bstack1111111l_opy_(driver)
      bstack11llll1lll_opy_ = percy.bstack11lllll1_opy_()
      if driver_command in bstack1lllll111l_opy_[bstack11llll1lll_opy_]:
        bstack1l111llll_opy_.bstack11ll111l11_opy_(bstack1l11l1l11_opy_, driver_command)
    except Exception as e:
      pass
def bstack1l1111l11l_opy_(framework_name):
  if bstack111ll1lll_opy_.get_property(bstack11l1l11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡳ࡯ࡥࡡࡦࡥࡱࡲࡥࡥࠩ౶")):
      return
  bstack111ll1lll_opy_.bstack11l111l1_opy_(bstack11l1l11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥ࡭ࡰࡦࡢࡧࡦࡲ࡬ࡦࡦࠪ౷"), True)
  global bstack1l11lll1l_opy_
  global bstack1l1l1lllll_opy_
  global bstack1l11l1ll11_opy_
  bstack1l11lll1l_opy_ = framework_name
  logger.info(bstack11l1l1ll1l_opy_.format(bstack1l11lll1l_opy_.split(bstack11l1l11_opy_ (u"ࠧ࠮ࠩ౸"))[0]))
  bstack1l1l1l1l11_opy_()
  try:
    from selenium import webdriver
    from selenium.webdriver.common.service import Service
    from selenium.webdriver.remote.webdriver import WebDriver
    if bstack1l111ll111_opy_:
      Service.start = bstack11ll1ll1_opy_
      Service.stop = bstack1ll1llll1l_opy_
      webdriver.Remote.get = bstack11lll1ll1_opy_
      WebDriver.close = bstack1l11l1l1_opy_
      WebDriver.quit = bstack111l1l11l_opy_
      webdriver.Remote.__init__ = bstack1lll111lll_opy_
      WebDriver.getAccessibilityResults = getAccessibilityResults
      WebDriver.get_accessibility_results = getAccessibilityResults
      WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
      WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
      WebDriver.performScan = perform_scan
      WebDriver.perform_scan = perform_scan
    if not bstack1l111ll111_opy_:
        webdriver.Remote.__init__ = bstack1llll1ll_opy_
    WebDriver.execute = bstack1llll11ll1_opy_
    bstack1l1l1lllll_opy_ = True
  except Exception as e:
    pass
  try:
    if bstack1l111ll111_opy_:
      from QWeb.keywords import browser
      browser.close_browser = bstack1llll1l1_opy_
  except Exception as e:
    pass
  bstack1111l1ll1_opy_()
  if not bstack1l1l1lllll_opy_:
    bstack11lll1ll1l_opy_(bstack11l1l11_opy_ (u"ࠣࡒࡤࡧࡰࡧࡧࡦࡵࠣࡲࡴࡺࠠࡪࡰࡶࡸࡦࡲ࡬ࡦࡦࠥ౹"), bstack1l11l1111l_opy_)
  if bstack11ll111l1_opy_():
    try:
      from selenium.webdriver.remote.remote_connection import RemoteConnection
      RemoteConnection._1ll1111l11_opy_ = bstack1l1ll1111_opy_
    except Exception as e:
      logger.error(bstack111l1llll_opy_.format(str(e)))
  if bstack1l11l1l1ll_opy_():
    bstack11lll1lll_opy_(CONFIG, logger)
  if (bstack11l1l11_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ౺") in str(framework_name).lower()):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        if percy.bstack1ll1111111_opy_() == bstack11l1l11_opy_ (u"ࠥࡸࡷࡻࡥࠣ౻"):
          bstack1ll111l1l_opy_(bstack1lll111l_opy_)
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        WebDriverCreator._get_ff_profile = bstack1l111l11_opy_
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCache.close = bstack11111l111_opy_
      except Exception as e:
        logger.warn(bstack1l1l111lll_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        ApplicationCache.close = bstack111l111ll_opy_
      except Exception as e:
        logger.debug(bstack11ll11l111_opy_ + str(e))
    except Exception as e:
      bstack11lll1ll1l_opy_(e, bstack1l1l111lll_opy_)
    Output.start_test = bstack1l1l1l1l1l_opy_
    Output.end_test = bstack111ll1ll1_opy_
    TestStatus.__init__ = bstack1ll11l11_opy_
    QueueItem.__init__ = bstack111l11111_opy_
    pabot._create_items = bstack1ll111ll11_opy_
    try:
      from pabot import __version__ as bstack1l11ll1ll_opy_
      if version.parse(bstack1l11ll1ll_opy_) >= version.parse(bstack11l1l11_opy_ (u"ࠫ࠷࠴࠱࠶࠰࠳ࠫ౼")):
        pabot._run = bstack1ll11lll11_opy_
      elif version.parse(bstack1l11ll1ll_opy_) >= version.parse(bstack11l1l11_opy_ (u"ࠬ࠸࠮࠲࠵࠱࠴ࠬ౽")):
        pabot._run = bstack1l11lll11l_opy_
      else:
        pabot._run = bstack111ll1l1l_opy_
    except Exception as e:
      pabot._run = bstack111ll1l1l_opy_
    pabot._create_command_for_execution = bstack1l111ll1ll_opy_
    pabot._report_results = bstack1lll1l11_opy_
  if bstack11l1l11_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭౾") in str(framework_name).lower():
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack11lll1ll1l_opy_(e, bstack1ll1l1ll1_opy_)
    Runner.run_hook = bstack1l1lllll11_opy_
    Step.run = bstack1l1l111l1_opy_
  if bstack11l1l11_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ౿") in str(framework_name).lower():
    if not bstack1l111ll111_opy_:
      return
    try:
      from pytest_selenium import pytest_selenium
      from _pytest.config import Config
      pytest_selenium.pytest_report_header = bstack111lllll_opy_
      from pytest_selenium.drivers import browserstack
      browserstack.pytest_selenium_runtest_makereport = bstack1ll111l11_opy_
      Config.getoption = bstack1l1lll11_opy_
    except Exception as e:
      pass
    try:
      from pytest_bdd import reporting
      reporting.runtest_makereport = bstack1l1ll1ll1_opy_
    except Exception as e:
      pass
def bstack11ll1lllll_opy_():
  global CONFIG
  if bstack11l1l11_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨಀ") in CONFIG and int(CONFIG[bstack11l1l11_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩಁ")]) > 1:
    logger.warn(bstack1l1l1l11ll_opy_)
def bstack11111ll1_opy_(arg, bstack11llll111l_opy_, bstack1ll1l11l1l_opy_=None):
  global CONFIG
  global bstack1111l1l1_opy_
  global bstack11ll11l11l_opy_
  global bstack1l111ll111_opy_
  global bstack111ll1lll_opy_
  bstack1lllll1111_opy_ = bstack11l1l11_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪಂ")
  if bstack11llll111l_opy_ and isinstance(bstack11llll111l_opy_, str):
    bstack11llll111l_opy_ = eval(bstack11llll111l_opy_)
  CONFIG = bstack11llll111l_opy_[bstack11l1l11_opy_ (u"ࠫࡈࡕࡎࡇࡋࡊࠫಃ")]
  bstack1111l1l1_opy_ = bstack11llll111l_opy_[bstack11l1l11_opy_ (u"ࠬࡎࡕࡃࡡࡘࡖࡑ࠭಄")]
  bstack11ll11l11l_opy_ = bstack11llll111l_opy_[bstack11l1l11_opy_ (u"࠭ࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨಅ")]
  bstack1l111ll111_opy_ = bstack11llll111l_opy_[bstack11l1l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡖࡖࡒࡑࡆ࡚ࡉࡐࡐࠪಆ")]
  bstack111ll1lll_opy_.bstack11l111l1_opy_(bstack11l1l11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࠩಇ"), bstack1l111ll111_opy_)
  os.environ[bstack11l1l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡈࡕࡅࡒࡋࡗࡐࡔࡎࠫಈ")] = bstack1lllll1111_opy_
  os.environ[bstack11l1l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡓࡓࡌࡉࡈࠩಉ")] = json.dumps(CONFIG)
  os.environ[bstack11l1l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡌ࡚ࡈ࡟ࡖࡔࡏࠫಊ")] = bstack1111l1l1_opy_
  os.environ[bstack11l1l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭ಋ")] = str(bstack11ll11l11l_opy_)
  os.environ[bstack11l1l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖ࡙ࡕࡇࡖࡘࡤࡖࡌࡖࡉࡌࡒࠬಌ")] = str(True)
  if bstack1llll11l11_opy_(arg, [bstack11l1l11_opy_ (u"ࠧ࠮ࡰࠪ಍"), bstack11l1l11_opy_ (u"ࠨ࠯࠰ࡲࡺࡳࡰࡳࡱࡦࡩࡸࡹࡥࡴࠩಎ")]) != -1:
    os.environ[bstack11l1l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒ࡜ࡘࡊ࡙ࡔࡠࡒࡄࡖࡆࡒࡌࡆࡎࠪಏ")] = str(True)
  if len(sys.argv) <= 1:
    logger.critical(bstack1l1l11l1_opy_)
    return
  bstack1l1l1ll1ll_opy_()
  global bstack1l11l11l1l_opy_
  global bstack1l1ll11111_opy_
  global bstack11l1ll1l1_opy_
  global bstack1lll111l1_opy_
  global bstack11l1l1l1l1_opy_
  global bstack1l11l1ll11_opy_
  global bstack111lll11_opy_
  arg.append(bstack11l1l11_opy_ (u"ࠥ࠱࡜ࠨಐ"))
  arg.append(bstack11l1l11_opy_ (u"ࠦ࡮࡭࡮ࡰࡴࡨ࠾ࡒࡵࡤࡶ࡮ࡨࠤࡦࡲࡲࡦࡣࡧࡽࠥ࡯࡭ࡱࡱࡵࡸࡪࡪ࠺ࡱࡻࡷࡩࡸࡺ࠮ࡑࡻࡷࡩࡸࡺࡗࡢࡴࡱ࡭ࡳ࡭ࠢ಑"))
  arg.append(bstack11l1l11_opy_ (u"ࠧ࠳ࡗࠣಒ"))
  arg.append(bstack11l1l11_opy_ (u"ࠨࡩࡨࡰࡲࡶࡪࡀࡔࡩࡧࠣ࡬ࡴࡵ࡫ࡪ࡯ࡳࡰࠧಓ"))
  global bstack1lll1l1l_opy_
  global bstack1lllll11l1_opy_
  global bstack11l1l111ll_opy_
  global bstack1l1llll11_opy_
  global bstack1lll11l1ll_opy_
  global bstack1ll111ll_opy_
  global bstack1l111l1l1_opy_
  global bstack1llll1l1ll_opy_
  global bstack1l1l1lll_opy_
  global bstack1ll111l1_opy_
  global bstack11llll11ll_opy_
  global bstack1l1111ll1l_opy_
  global bstack11ll11lll_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack1lll1l1l_opy_ = webdriver.Remote.__init__
    bstack1lllll11l1_opy_ = WebDriver.quit
    bstack1llll1l1ll_opy_ = WebDriver.close
    bstack1l1l1lll_opy_ = WebDriver.get
    bstack11l1l111ll_opy_ = WebDriver.execute
  except Exception as e:
    pass
  if bstack1l1ll1ll11_opy_(CONFIG) and bstack1lll1l1ll1_opy_():
    if bstack1ll1lllll_opy_() < version.parse(bstack11lllll11_opy_):
      logger.error(bstack1lll1l1ll_opy_.format(bstack1ll1lllll_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        bstack1ll111l1_opy_ = RemoteConnection._1ll1111l11_opy_
      except Exception as e:
        logger.error(bstack111l1llll_opy_.format(str(e)))
  try:
    from _pytest.config import Config
    bstack11llll11ll_opy_ = Config.getoption
    from _pytest import runner
    bstack1l1111ll1l_opy_ = runner._update_current_test_var
  except Exception as e:
    logger.warn(e, bstack1ll11lllll_opy_)
  try:
    from pytest_bdd import reporting
    bstack11ll11lll_opy_ = reporting.runtest_makereport
  except Exception as e:
    logger.debug(bstack11l1l11_opy_ (u"ࠧࡑ࡮ࡨࡥࡸ࡫ࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡺ࡯ࠡࡴࡸࡲࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡷࡩࡸࡺࡳࠨಔ"))
  bstack11l1ll1l1_opy_ = CONFIG.get(bstack11l1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬಕ"), {}).get(bstack11l1l11_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫಖ"))
  bstack111lll11_opy_ = True
  if cli.is_enabled(CONFIG):
    if cli.bstack11llll1l1_opy_():
      bstack11l11ll11l_opy_.invoke(bstack1llll111ll_opy_.CONNECT, bstack111111ll1_opy_())
    platform_index = int(os.environ.get(bstack11l1l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪಗ"), bstack11l1l11_opy_ (u"ࠫ࠵࠭ಘ")))
  else:
    bstack1l1111l11l_opy_(bstack1111111ll_opy_)
  os.environ[bstack11l1l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡚࡙ࡅࡓࡐࡄࡑࡊ࠭ಙ")] = CONFIG[bstack11l1l11_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨಚ")]
  os.environ[bstack11l1l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡄࡅࡈࡗࡘࡥࡋࡆ࡛ࠪಛ")] = CONFIG[bstack11l1l11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫಜ")]
  os.environ[bstack11l1l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡘࡘࡔࡓࡁࡕࡋࡒࡒࠬಝ")] = bstack1l111ll111_opy_.__str__()
  from _pytest.config import main as bstack11l1l1lll1_opy_
  bstack1lll11l1l_opy_ = []
  try:
    bstack1ll1l111ll_opy_ = bstack11l1l1lll1_opy_(arg)
    if cli.is_enabled(CONFIG):
      cli.bstack11ll1111l1_opy_()
    if bstack11l1l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺࠧಞ") in multiprocessing.current_process().__dict__.keys():
      for bstack1l1ll1l1ll_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack1lll11l1l_opy_.append(bstack1l1ll1l1ll_opy_)
    try:
      bstack1l11111ll1_opy_ = (bstack1lll11l1l_opy_, int(bstack1ll1l111ll_opy_))
      bstack1ll1l11l1l_opy_.append(bstack1l11111ll1_opy_)
    except:
      bstack1ll1l11l1l_opy_.append((bstack1lll11l1l_opy_, bstack1ll1l111ll_opy_))
  except Exception as e:
    logger.error(traceback.format_exc())
    bstack1lll11l1l_opy_.append({bstack11l1l11_opy_ (u"ࠫࡳࡧ࡭ࡦࠩಟ"): bstack11l1l11_opy_ (u"ࠬࡖࡲࡰࡥࡨࡷࡸࠦࠧಠ") + os.environ.get(bstack11l1l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ಡ")), bstack11l1l11_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ಢ"): traceback.format_exc(), bstack11l1l11_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧಣ"): int(os.environ.get(bstack11l1l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩತ")))})
    bstack1ll1l11l1l_opy_.append((bstack1lll11l1l_opy_, 1))
def bstack11ll11llll_opy_(arg):
  global bstack1l1l1ll1l1_opy_
  bstack1l1111l11l_opy_(bstack11ll1l11l_opy_)
  os.environ[bstack11l1l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫಥ")] = str(bstack11ll11l11l_opy_)
  from behave.__main__ import main as bstack11l1ll11l1_opy_
  status_code = bstack11l1ll11l1_opy_(arg)
  if status_code != 0:
    bstack1l1l1ll1l1_opy_ = status_code
def bstack11ll1l1l11_opy_():
  logger.info(bstack1lll1llll_opy_)
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument(bstack11l1l11_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪದ"), help=bstack11l1l11_opy_ (u"ࠬࡍࡥ࡯ࡧࡵࡥࡹ࡫ࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡣࡰࡰࡩ࡭࡬࠭ಧ"))
  parser.add_argument(bstack11l1l11_opy_ (u"࠭࠭ࡶࠩನ"), bstack11l1l11_opy_ (u"ࠧ࠮࠯ࡸࡷࡪࡸ࡮ࡢ࡯ࡨࠫ಩"), help=bstack11l1l11_opy_ (u"ࠨ࡛ࡲࡹࡷࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡻࡳࡦࡴࡱࡥࡲ࡫ࠧಪ"))
  parser.add_argument(bstack11l1l11_opy_ (u"ࠩ࠰࡯ࠬಫ"), bstack11l1l11_opy_ (u"ࠪ࠱࠲ࡱࡥࡺࠩಬ"), help=bstack11l1l11_opy_ (u"ࠫ࡞ࡵࡵࡳࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡣࡦࡧࡪࡹࡳࠡ࡭ࡨࡽࠬಭ"))
  parser.add_argument(bstack11l1l11_opy_ (u"ࠬ࠳ࡦࠨಮ"), bstack11l1l11_opy_ (u"࠭࠭࠮ࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫಯ"), help=bstack11l1l11_opy_ (u"࡚ࠧࡱࡸࡶࠥࡺࡥࡴࡶࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ರ"))
  bstack1lll1111l1_opy_ = parser.parse_args()
  try:
    bstack1l11llllll_opy_ = bstack11l1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡨࡧࡱࡩࡷ࡯ࡣ࠯ࡻࡰࡰ࠳ࡹࡡ࡮ࡲ࡯ࡩࠬಱ")
    if bstack1lll1111l1_opy_.framework and bstack1lll1111l1_opy_.framework not in (bstack11l1l11_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩಲ"), bstack11l1l11_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰ࠶ࠫಳ")):
      bstack1l11llllll_opy_ = bstack11l1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠴ࡹ࡮࡮࠱ࡷࡦࡳࡰ࡭ࡧࠪ಴")
    bstack1ll1ll111_opy_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1l11llllll_opy_)
    bstack1ll11l11l1_opy_ = open(bstack1ll1ll111_opy_, bstack11l1l11_opy_ (u"ࠬࡸࠧವ"))
    bstack1l11111l1_opy_ = bstack1ll11l11l1_opy_.read()
    bstack1ll11l11l1_opy_.close()
    if bstack1lll1111l1_opy_.username:
      bstack1l11111l1_opy_ = bstack1l11111l1_opy_.replace(bstack11l1l11_opy_ (u"࡙࠭ࡐࡗࡕࡣ࡚࡙ࡅࡓࡐࡄࡑࡊ࠭ಶ"), bstack1lll1111l1_opy_.username)
    if bstack1lll1111l1_opy_.key:
      bstack1l11111l1_opy_ = bstack1l11111l1_opy_.replace(bstack11l1l11_opy_ (u"࡚ࠧࡑࡘࡖࡤࡇࡃࡄࡇࡖࡗࡤࡑࡅ࡚ࠩಷ"), bstack1lll1111l1_opy_.key)
    if bstack1lll1111l1_opy_.framework:
      bstack1l11111l1_opy_ = bstack1l11111l1_opy_.replace(bstack11l1l11_opy_ (u"ࠨ࡛ࡒ࡙ࡗࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࠩಸ"), bstack1lll1111l1_opy_.framework)
    file_name = bstack11l1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡻࡰࡰࠬಹ")
    file_path = os.path.abspath(file_name)
    bstack1111lllll_opy_ = open(file_path, bstack11l1l11_opy_ (u"ࠪࡻࠬ಺"))
    bstack1111lllll_opy_.write(bstack1l11111l1_opy_)
    bstack1111lllll_opy_.close()
    logger.info(bstack1l1l1l1ll_opy_)
    try:
      os.environ[bstack11l1l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐ࠭಻")] = bstack1lll1111l1_opy_.framework if bstack1lll1111l1_opy_.framework != None else bstack11l1l11_opy_ (u"ࠧࠨ಼")
      config = yaml.safe_load(bstack1l11111l1_opy_)
      config[bstack11l1l11_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭ಽ")] = bstack11l1l11_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴ࠭ࡴࡧࡷࡹࡵ࠭ಾ")
      bstack1ll111lll_opy_(bstack1lll1lllll_opy_, config)
    except Exception as e:
      logger.debug(bstack111lllll1_opy_.format(str(e)))
  except Exception as e:
    logger.error(bstack11ll1l11ll_opy_.format(str(e)))
def bstack1ll111lll_opy_(bstack1ll1ll1ll_opy_, config, bstack11llll1111_opy_={}):
  global bstack1l111ll111_opy_
  global bstack11llllll1_opy_
  global bstack111ll1lll_opy_
  if not config:
    return
  bstack1llll11lll_opy_ = bstack1l11l11lll_opy_ if not bstack1l111ll111_opy_ else (
    bstack1l11l1l11l_opy_ if bstack11l1l11_opy_ (u"ࠨࡣࡳࡴࠬಿ") in config else (
        bstack1lll1ll1_opy_ if config.get(bstack11l1l11_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭ೀ")) else bstack11l11l111_opy_
    )
)
  bstack1l111l1l_opy_ = False
  bstack1l111l111l_opy_ = False
  if bstack1l111ll111_opy_ is True:
      if bstack11l1l11_opy_ (u"ࠪࡥࡵࡶࠧು") in config:
          bstack1l111l1l_opy_ = True
      else:
          bstack1l111l111l_opy_ = True
  bstack11l1l111l_opy_ = bstack11l1111l1_opy_.bstack1ll1l111l1_opy_(config, bstack11llllll1_opy_)
  bstack11l1l1ll11_opy_ = bstack11l1lll1_opy_()
  data = {
    bstack11l1l11_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ೂ"): config[bstack11l1l11_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧೃ")],
    bstack11l1l11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩೄ"): config[bstack11l1l11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪ೅")],
    bstack11l1l11_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬೆ"): bstack1ll1ll1ll_opy_,
    bstack11l1l11_opy_ (u"ࠩࡧࡩࡹ࡫ࡣࡵࡧࡧࡊࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ೇ"): os.environ.get(bstack11l1l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠬೈ"), bstack11llllll1_opy_),
    bstack11l1l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭೉"): bstack1111l1111_opy_,
    bstack11l1l11_opy_ (u"ࠬࡵࡰࡵ࡫ࡰࡥࡱࡥࡨࡶࡤࡢࡹࡷࡲࠧೊ"): bstack1l11l1llll_opy_(),
    bstack11l1l11_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡶࡲࡰࡲࡨࡶࡹ࡯ࡥࡴࠩೋ"): {
      bstack11l1l11_opy_ (u"ࠧ࡭ࡣࡱ࡫ࡺࡧࡧࡦࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬೌ"): str(config[bstack11l1l11_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨ್")]) if bstack11l1l11_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩ೎") in config else bstack11l1l11_opy_ (u"ࠥࡹࡳࡱ࡮ࡰࡹࡱࠦ೏"),
      bstack11l1l11_opy_ (u"ࠫࡱࡧ࡮ࡨࡷࡤ࡫ࡪ࡜ࡥࡳࡵ࡬ࡳࡳ࠭೐"): sys.version,
      bstack11l1l11_opy_ (u"ࠬࡸࡥࡧࡧࡵࡶࡪࡸࠧ೑"): bstack1ll11ll111_opy_(os.environ.get(bstack11l1l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࠨ೒"), bstack11llllll1_opy_)),
      bstack11l1l11_opy_ (u"ࠧ࡭ࡣࡱ࡫ࡺࡧࡧࡦࠩ೓"): bstack11l1l11_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨ೔"),
      bstack11l1l11_opy_ (u"ࠩࡳࡶࡴࡪࡵࡤࡶࠪೕ"): bstack1llll11lll_opy_,
      bstack11l1l11_opy_ (u"ࠪࡴࡷࡵࡤࡶࡥࡷࡣࡲࡧࡰࠨೖ"): bstack11l1l111l_opy_,
      bstack11l1l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡪࡸࡦࡤࡻࡵࡪࡦࠪ೗"): os.environ[bstack11l1l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪ೘")],
      bstack11l1l11_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ೙"): os.environ.get(bstack11l1l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࠩ೚"), bstack11llllll1_opy_),
      bstack11l1l11_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮࡚ࡪࡸࡳࡪࡱࡱࠫ೛"): bstack1l1ll1l1l1_opy_(os.environ.get(bstack11l1l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡈࡕࡅࡒࡋࡗࡐࡔࡎࠫ೜"), bstack11llllll1_opy_)),
      bstack11l1l11_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࠩೝ"): bstack11l1l1ll11_opy_.get(bstack11l1l11_opy_ (u"ࠫࡳࡧ࡭ࡦࠩೞ")),
      bstack11l1l11_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮࡚ࡪࡸࡳࡪࡱࡱࠫ೟"): bstack11l1l1ll11_opy_.get(bstack11l1l11_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴࠧೠ")),
      bstack11l1l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪೡ"): config[bstack11l1l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫೢ")] if config[bstack11l1l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬೣ")] else bstack11l1l11_opy_ (u"ࠥࡹࡳࡱ࡮ࡰࡹࡱࠦ೤"),
      bstack11l1l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭೥"): str(config[bstack11l1l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ೦")]) if bstack11l1l11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ೧") in config else bstack11l1l11_opy_ (u"ࠢࡶࡰ࡮ࡲࡴࡽ࡮ࠣ೨"),
      bstack11l1l11_opy_ (u"ࠨࡱࡶࠫ೩"): sys.platform,
      bstack11l1l11_opy_ (u"ࠩ࡫ࡳࡸࡺ࡮ࡢ࡯ࡨࠫ೪"): socket.gethostname(),
      bstack11l1l11_opy_ (u"ࠪࡷࡩࡱࡒࡶࡰࡌࡨࠬ೫"): bstack111ll1lll_opy_.get_property(bstack11l1l11_opy_ (u"ࠫࡸࡪ࡫ࡓࡷࡱࡍࡩ࠭೬"))
    }
  }
  if not bstack111ll1lll_opy_.get_property(bstack11l1l11_opy_ (u"ࠬࡹࡤ࡬ࡍ࡬ࡰࡱ࡙ࡩࡨࡰࡤࡰࠬ೭")) is None:
    data[bstack11l1l11_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡶࡲࡰࡲࡨࡶࡹ࡯ࡥࡴࠩ೮")][bstack11l1l11_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡏࡨࡸࡦࡪࡡࡵࡣࠪ೯")] = {
      bstack11l1l11_opy_ (u"ࠨࡴࡨࡥࡸࡵ࡮ࠨ೰"): bstack11l1l11_opy_ (u"ࠩࡸࡷࡪࡸ࡟࡬࡫࡯ࡰࡪࡪࠧೱ"),
      bstack11l1l11_opy_ (u"ࠪࡷ࡮࡭࡮ࡢ࡮ࠪೲ"): bstack111ll1lll_opy_.get_property(bstack11l1l11_opy_ (u"ࠫࡸࡪ࡫ࡌ࡫࡯ࡰࡘ࡯ࡧ࡯ࡣ࡯ࠫೳ")),
      bstack11l1l11_opy_ (u"ࠬࡹࡩࡨࡰࡤࡰࡓࡻ࡭ࡣࡧࡵࠫ೴"): bstack111ll1lll_opy_.get_property(bstack11l1l11_opy_ (u"࠭ࡳࡥ࡭ࡎ࡭ࡱࡲࡎࡰࠩ೵"))
    }
  if bstack1ll1ll1ll_opy_ == bstack11l1l111_opy_:
    data[bstack11l1l11_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡰࡳࡱࡳࡩࡷࡺࡩࡦࡵࠪ೶")][bstack11l1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡃࡰࡰࡩ࡭࡬࠭೷")] = bstack1l1l111ll1_opy_(config)
    data[bstack11l1l11_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡲࡵࡳࡵ࡫ࡲࡵ࡫ࡨࡷࠬ೸")][bstack11l1l11_opy_ (u"ࠪ࡭ࡸࡖࡥࡳࡥࡼࡅࡺࡺ࡯ࡆࡰࡤࡦࡱ࡫ࡤࠨ೹")] = percy.bstack1lllll11_opy_
    data[bstack11l1l11_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡴࡷࡵࡰࡦࡴࡷ࡭ࡪࡹࠧ೺")][bstack11l1l11_opy_ (u"ࠬࡶࡥࡳࡥࡼࡆࡺ࡯࡬ࡥࡋࡧࠫ೻")] = percy.percy_build_id
  update(data[bstack11l1l11_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡶࡲࡰࡲࡨࡶࡹ࡯ࡥࡴࠩ೼")], bstack11llll1111_opy_)
  try:
    response = bstack111ll11ll_opy_(bstack11l1l11_opy_ (u"ࠧࡑࡑࡖࡘࠬ೽"), bstack1ll11l11l_opy_(bstack1l11ll11l_opy_), data, {
      bstack11l1l11_opy_ (u"ࠨࡣࡸࡸ࡭࠭೾"): (config[bstack11l1l11_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ೿")], config[bstack11l1l11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ഀ")])
    })
    if response:
      logger.debug(bstack1lll1l1lll_opy_.format(bstack1ll1ll1ll_opy_, str(response.json())))
  except Exception as e:
    logger.debug(bstack1l1lll1l1_opy_.format(str(e)))
def bstack1ll11ll111_opy_(framework):
  return bstack11l1l11_opy_ (u"ࠦࢀࢃ࠭ࡱࡻࡷ࡬ࡴࡴࡡࡨࡧࡱࡸ࠴ࢁࡽࠣഁ").format(str(framework), __version__) if framework else bstack11l1l11_opy_ (u"ࠧࡶࡹࡵࡪࡲࡲࡦ࡭ࡥ࡯ࡶ࠲ࡿࢂࠨം").format(
    __version__)
def bstack1l1l1ll1ll_opy_():
  global CONFIG
  global bstack1llll1ll1l_opy_
  if bool(CONFIG):
    return
  try:
    bstack1111l11ll_opy_()
    logger.debug(bstack11l1llll_opy_.format(str(CONFIG)))
    bstack1llll1ll1l_opy_ = bstack111ll1l11_opy_.bstack11ll1l111l_opy_(CONFIG, bstack1llll1ll1l_opy_)
    bstack1l1l1l1l11_opy_()
  except Exception as e:
    logger.error(bstack11l1l11_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡹࡻࡰ࠭ࠢࡨࡶࡷࡵࡲ࠻ࠢࠥഃ") + str(e))
    sys.exit(1)
  sys.excepthook = bstack1l1l1llll_opy_
  atexit.register(bstack1l111ll1l_opy_)
  signal.signal(signal.SIGINT, bstack1ll1l1l111_opy_)
  signal.signal(signal.SIGTERM, bstack1ll1l1l111_opy_)
def bstack1l1l1llll_opy_(exctype, value, traceback):
  global bstack1l11ll11l1_opy_
  try:
    for driver in bstack1l11ll11l1_opy_:
      bstack1l1l1l11l1_opy_(driver, bstack11l1l11_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧഄ"), bstack11l1l11_opy_ (u"ࠣࡕࡨࡷࡸ࡯࡯࡯ࠢࡩࡥ࡮ࡲࡥࡥࠢࡺ࡭ࡹ࡮࠺ࠡ࡞ࡱࠦഅ") + str(value))
  except Exception:
    pass
  logger.info(bstack1ll11llll1_opy_)
  bstack111l11ll_opy_(value, True)
  sys.__excepthook__(exctype, value, traceback)
  sys.exit(1)
def bstack111l11ll_opy_(message=bstack11l1l11_opy_ (u"ࠩࠪആ"), bstack1ll1lll11_opy_ = False):
  global CONFIG
  bstack1l11111111_opy_ = bstack11l1l11_opy_ (u"ࠪ࡫ࡱࡵࡢࡢ࡮ࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠬഇ") if bstack1ll1lll11_opy_ else bstack11l1l11_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪഈ")
  try:
    if message:
      bstack11llll1111_opy_ = {
        bstack1l11111111_opy_ : str(message)
      }
      bstack1ll111lll_opy_(bstack11l1l111_opy_, CONFIG, bstack11llll1111_opy_)
    else:
      bstack1ll111lll_opy_(bstack11l1l111_opy_, CONFIG)
  except Exception as e:
    logger.debug(bstack1ll1ll1l1_opy_.format(str(e)))
def bstack1l1111l1ll_opy_(bstack11ll1ll1l_opy_, size):
  bstack1llllllll_opy_ = []
  while len(bstack11ll1ll1l_opy_) > size:
    bstack1111ll1l1_opy_ = bstack11ll1ll1l_opy_[:size]
    bstack1llllllll_opy_.append(bstack1111ll1l1_opy_)
    bstack11ll1ll1l_opy_ = bstack11ll1ll1l_opy_[size:]
  bstack1llllllll_opy_.append(bstack11ll1ll1l_opy_)
  return bstack1llllllll_opy_
def bstack11l1l11l11_opy_(args):
  if bstack11l1l11_opy_ (u"ࠬ࠳࡭ࠨഉ") in args and bstack11l1l11_opy_ (u"࠭ࡰࡥࡤࠪഊ") in args:
    return True
  return False
@measure(event_name=EVENTS.bstack1l1l11l1l1_opy_, stage=STAGE.bstack1ll11l11ll_opy_)
def run_on_browserstack(bstack1l1l11lll_opy_=None, bstack1ll1l11l1l_opy_=None, bstack1ll1l1111l_opy_=False):
  global CONFIG
  global bstack1111l1l1_opy_
  global bstack11ll11l11l_opy_
  global bstack11llllll1_opy_
  global bstack111ll1lll_opy_
  bstack1lllll1111_opy_ = bstack11l1l11_opy_ (u"ࠧࠨഋ")
  bstack11lll11l11_opy_(bstack1ll1l11ll1_opy_, logger)
  if bstack1l1l11lll_opy_ and isinstance(bstack1l1l11lll_opy_, str):
    bstack1l1l11lll_opy_ = eval(bstack1l1l11lll_opy_)
  if bstack1l1l11lll_opy_:
    CONFIG = bstack1l1l11lll_opy_[bstack11l1l11_opy_ (u"ࠨࡅࡒࡒࡋࡏࡇࠨഌ")]
    bstack1111l1l1_opy_ = bstack1l1l11lll_opy_[bstack11l1l11_opy_ (u"ࠩࡋ࡙ࡇࡥࡕࡓࡎࠪ഍")]
    bstack11ll11l11l_opy_ = bstack1l1l11lll_opy_[bstack11l1l11_opy_ (u"ࠪࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬഎ")]
    bstack111ll1lll_opy_.bstack11l111l1_opy_(bstack11l1l11_opy_ (u"ࠫࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭ഏ"), bstack11ll11l11l_opy_)
    bstack1lllll1111_opy_ = bstack11l1l11_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬഐ")
  bstack111ll1lll_opy_.bstack11l111l1_opy_(bstack11l1l11_opy_ (u"࠭ࡳࡥ࡭ࡕࡹࡳࡏࡤࠨ഑"), uuid4().__str__())
  logger.info(bstack11l1l11_opy_ (u"ࠧࡔࡆࡎࠤࡷࡻ࡮ࠡࡵࡷࡥࡷࡺࡥࡥࠢࡺ࡭ࡹ࡮ࠠࡪࡦ࠽ࠤࠬഒ") + bstack111ll1lll_opy_.get_property(bstack11l1l11_opy_ (u"ࠨࡵࡧ࡯ࡗࡻ࡮ࡊࡦࠪഓ")));
  logger.debug(bstack11l1l11_opy_ (u"ࠩࡶࡨࡰࡘࡵ࡯ࡋࡧࡁࠬഔ") + bstack111ll1lll_opy_.get_property(bstack11l1l11_opy_ (u"ࠪࡷࡩࡱࡒࡶࡰࡌࡨࠬക")))
  if not bstack1ll1l1111l_opy_:
    if len(sys.argv) <= 1:
      logger.critical(bstack1l1l11l1_opy_)
      return
    if sys.argv[1] == bstack11l1l11_opy_ (u"ࠫ࠲࠳ࡶࡦࡴࡶ࡭ࡴࡴࠧഖ") or sys.argv[1] == bstack11l1l11_opy_ (u"ࠬ࠳ࡶࠨഗ"):
      logger.info(bstack11l1l11_opy_ (u"࠭ࡂࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡖࡹࡵࡪࡲࡲ࡙ࠥࡄࡌࠢࡹࡿࢂ࠭ഘ").format(__version__))
      return
    if sys.argv[1] == bstack11l1l11_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭ങ"):
      bstack11ll1l1l11_opy_()
      return
  args = sys.argv
  bstack1l1l1ll1ll_opy_()
  global bstack1l11l11l1l_opy_
  global bstack1l1lllllll_opy_
  global bstack111lll11_opy_
  global bstack1lll1l11l1_opy_
  global bstack1l1ll11111_opy_
  global bstack11l1ll1l1_opy_
  global bstack1lll111l1_opy_
  global bstack1l1lll111_opy_
  global bstack11l1l1l1l1_opy_
  global bstack1l11l1ll11_opy_
  global bstack1lll1ll111_opy_
  bstack1l1lllllll_opy_ = len(CONFIG.get(bstack11l1l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫച"), []))
  if not bstack1lllll1111_opy_:
    if args[1] == bstack11l1l11_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩഛ") or args[1] == bstack11l1l11_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰ࠶ࠫജ"):
      bstack1lllll1111_opy_ = bstack11l1l11_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫഝ")
      args = args[2:]
    elif args[1] == bstack11l1l11_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫഞ"):
      bstack1lllll1111_opy_ = bstack11l1l11_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬട")
      args = args[2:]
    elif args[1] == bstack11l1l11_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭ഠ"):
      bstack1lllll1111_opy_ = bstack11l1l11_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧഡ")
      args = args[2:]
    elif args[1] == bstack11l1l11_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠪഢ"):
      bstack1lllll1111_opy_ = bstack11l1l11_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫണ")
      args = args[2:]
    elif args[1] == bstack11l1l11_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫത"):
      bstack1lllll1111_opy_ = bstack11l1l11_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬഥ")
      args = args[2:]
    elif args[1] == bstack11l1l11_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭ദ"):
      bstack1lllll1111_opy_ = bstack11l1l11_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧധ")
      args = args[2:]
    else:
      if not bstack11l1l11_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫന") in CONFIG or str(CONFIG[bstack11l1l11_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬഩ")]).lower() in [bstack11l1l11_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪപ"), bstack11l1l11_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱ࠷ࠬഫ")]:
        bstack1lllll1111_opy_ = bstack11l1l11_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬബ")
        args = args[1:]
      elif str(CONFIG[bstack11l1l11_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩഭ")]).lower() == bstack11l1l11_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭മ"):
        bstack1lllll1111_opy_ = bstack11l1l11_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧയ")
        args = args[1:]
      elif str(CONFIG[bstack11l1l11_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬര")]).lower() == bstack11l1l11_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩറ"):
        bstack1lllll1111_opy_ = bstack11l1l11_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪല")
        args = args[1:]
      elif str(CONFIG[bstack11l1l11_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨള")]).lower() == bstack11l1l11_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ഴ"):
        bstack1lllll1111_opy_ = bstack11l1l11_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧവ")
        args = args[1:]
      elif str(CONFIG[bstack11l1l11_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫശ")]).lower() == bstack11l1l11_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩഷ"):
        bstack1lllll1111_opy_ = bstack11l1l11_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪസ")
        args = args[1:]
      else:
        os.environ[bstack11l1l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐ࠭ഹ")] = bstack1lllll1111_opy_
        bstack11111l1ll_opy_(bstack11l1ll11l_opy_)
  os.environ[bstack11l1l11_opy_ (u"ࠬࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࡠࡗࡖࡉࡉ࠭ഺ")] = bstack1lllll1111_opy_
  bstack11llllll1_opy_ = bstack1lllll1111_opy_
  if cli.is_enabled(CONFIG):
    try:
      bstack111111l1l_opy_ = bstack1l1111l1l1_opy_[bstack11l1l11_opy_ (u"࠭ࡐ࡚ࡖࡈࡗ࡙࠳ࡂࡅࡆ഻ࠪ")] if bstack1lllll1111_opy_ == bstack11l1l11_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ഼ࠧ") and bstack1lll1ll11l_opy_() else bstack1lllll1111_opy_
      bstack11l11ll11l_opy_.invoke(bstack1llll111ll_opy_.bstack111l1ll1l_opy_, bstack1l1ll11ll_opy_(
        sdk_version=__version__,
        path_config=bstack11l111lll_opy_(),
        path_project=os.getcwd(),
        test_framework=bstack111111l1l_opy_,
        frameworks=[bstack111111l1l_opy_],
        framework_versions={
          bstack111111l1l_opy_: bstack1l1ll1l1l1_opy_(bstack11l1l11_opy_ (u"ࠨࡔࡲࡦࡴࡺࠧഽ") if bstack1lllll1111_opy_ in [bstack11l1l11_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨാ"), bstack11l1l11_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩി"), bstack11l1l11_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬീ")] else bstack1lllll1111_opy_)
        },
        bs_config=CONFIG
      ))
      if cli.config.get(bstack11l1l11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠢു"), None):
        CONFIG[bstack11l1l11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠣൂ")] = cli.config.get(bstack11l1l11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠤൃ"), None)
    except Exception as e:
      bstack11l11ll11l_opy_.invoke(bstack1llll111ll_opy_.bstack1l1llllll_opy_, e.__traceback__, 1)
    if bstack11ll11l11l_opy_:
      CONFIG[bstack11l1l11_opy_ (u"ࠣࡣࡳࡴࠧൄ")] = cli.config[bstack11l1l11_opy_ (u"ࠤࡤࡴࡵࠨ൅")]
      logger.info(bstack11ll1ll111_opy_.format(CONFIG[bstack11l1l11_opy_ (u"ࠪࡥࡵࡶࠧെ")]))
  else:
    bstack11l11ll11l_opy_.clear()
  global bstack1l1111111l_opy_
  global bstack1l1l11l11_opy_
  if bstack1l1l11lll_opy_:
    try:
      bstack1l1ll1l111_opy_ = datetime.datetime.now()
      os.environ[bstack11l1l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐ࠭േ")] = bstack1lllll1111_opy_
      bstack1ll111lll_opy_(bstack11l1l11l1_opy_, CONFIG)
      cli.bstack1ll11lll_opy_(bstack11l1l11_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽ࡷࡩࡱ࡟ࡵࡧࡶࡸࡤࡧࡴࡵࡧࡰࡴࡹ࡫ࡤࠣൈ"), datetime.datetime.now() - bstack1l1ll1l111_opy_)
    except Exception as e:
      logger.debug(bstack1l11ll1l1l_opy_.format(str(e)))
  global bstack1lll1l1l_opy_
  global bstack1lllll11l1_opy_
  global bstack1ll111ll1l_opy_
  global bstack11l1lll1l_opy_
  global bstack1lll1lll_opy_
  global bstack111ll11l_opy_
  global bstack1l1llll11_opy_
  global bstack1lll11l1ll_opy_
  global bstack1l1l1ll111_opy_
  global bstack1ll111ll_opy_
  global bstack1l111l1l1_opy_
  global bstack1llll1l1ll_opy_
  global bstack11lll11l_opy_
  global bstack1l111l1lll_opy_
  global bstack1l1l1lll_opy_
  global bstack1ll111l1_opy_
  global bstack11llll11ll_opy_
  global bstack1l1111ll1l_opy_
  global bstack11l1l11l_opy_
  global bstack11ll11lll_opy_
  global bstack11l1l111ll_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack1lll1l1l_opy_ = webdriver.Remote.__init__
    bstack1lllll11l1_opy_ = WebDriver.quit
    bstack1llll1l1ll_opy_ = WebDriver.close
    bstack1l1l1lll_opy_ = WebDriver.get
    bstack11l1l111ll_opy_ = WebDriver.execute
  except Exception as e:
    pass
  try:
    import Browser
    from subprocess import Popen
    bstack1l1111111l_opy_ = Popen.__init__
  except Exception as e:
    pass
  try:
    from bstack_utils.helper import bstack1lll1l1l1l_opy_
    bstack1l1l11l11_opy_ = bstack1lll1l1l1l_opy_()
  except Exception as e:
    pass
  try:
    global bstack1111ll1l_opy_
    from QWeb.keywords import browser
    bstack1111ll1l_opy_ = browser.close_browser
  except Exception as e:
    pass
  if bstack1l1ll1ll11_opy_(CONFIG) and bstack1lll1l1ll1_opy_():
    if bstack1ll1lllll_opy_() < version.parse(bstack11lllll11_opy_):
      logger.error(bstack1lll1l1ll_opy_.format(bstack1ll1lllll_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        bstack1ll111l1_opy_ = RemoteConnection._1ll1111l11_opy_
      except Exception as e:
        logger.error(bstack111l1llll_opy_.format(str(e)))
  if not CONFIG.get(bstack11l1l11_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡁࡶࡶࡲࡇࡦࡶࡴࡶࡴࡨࡐࡴ࡭ࡳࠨ൉"), False) and not bstack1l1l11lll_opy_:
    logger.info(bstack1l11111l1l_opy_)
  if not cli.is_enabled(CONFIG):
    if bstack11l1l11_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫൊ") in CONFIG and str(CONFIG[bstack11l1l11_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬോ")]).lower() != bstack11l1l11_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨൌ"):
      bstack1ll1ll11_opy_()
    elif bstack1lllll1111_opy_ != bstack11l1l11_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰ്ࠪ") or (bstack1lllll1111_opy_ == bstack11l1l11_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫൎ") and not bstack1l1l11lll_opy_):
      bstack11l1lll111_opy_()
  if (bstack1lllll1111_opy_ in [bstack11l1l11_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫ൏"), bstack11l1l11_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ൐"), bstack11l1l11_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠨ൑")]):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCreator._get_ff_profile = bstack1l111l11_opy_
        bstack111ll11l_opy_ = WebDriverCache.close
      except Exception as e:
        logger.warn(bstack1l1l111lll_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        bstack1lll1lll_opy_ = ApplicationCache.close
      except Exception as e:
        logger.debug(bstack11ll11l111_opy_ + str(e))
    except Exception as e:
      bstack11lll1ll1l_opy_(e, bstack1l1l111lll_opy_)
    if bstack1lllll1111_opy_ != bstack11l1l11_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩ൒"):
      bstack1llll11ll_opy_()
    bstack1ll111ll1l_opy_ = Output.start_test
    bstack11l1lll1l_opy_ = Output.end_test
    bstack1l1llll11_opy_ = TestStatus.__init__
    bstack1l1l1ll111_opy_ = pabot._run
    bstack1ll111ll_opy_ = QueueItem.__init__
    bstack1l111l1l1_opy_ = pabot._create_command_for_execution
    bstack11l1l11l_opy_ = pabot._report_results
  if bstack1lllll1111_opy_ == bstack11l1l11_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩ൓"):
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack11lll1ll1l_opy_(e, bstack1ll1l1ll1_opy_)
    bstack11lll11l_opy_ = Runner.run_hook
    bstack1l111l1lll_opy_ = Step.run
  if bstack1lllll1111_opy_ == bstack11l1l11_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪൔ"):
    try:
      from _pytest.config import Config
      bstack11llll11ll_opy_ = Config.getoption
      from _pytest import runner
      bstack1l1111ll1l_opy_ = runner._update_current_test_var
    except Exception as e:
      logger.warn(e, bstack1ll11lllll_opy_)
    try:
      from pytest_bdd import reporting
      bstack11ll11lll_opy_ = reporting.runtest_makereport
    except Exception as e:
      logger.debug(bstack11l1l11_opy_ (u"ࠫࡕࡲࡥࡢࡵࡨࠤ࡮ࡴࡳࡵࡣ࡯ࡰࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡷࡳࠥࡸࡵ࡯ࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡴࡦࡵࡷࡷࠬൕ"))
  try:
    framework_name = bstack11l1l11_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫൖ") if bstack1lllll1111_opy_ in [bstack11l1l11_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬൗ"), bstack11l1l11_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭൘"), bstack11l1l11_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩ൙")] else bstack11ll11111l_opy_(bstack1lllll1111_opy_)
    bstack1l11ll1l1_opy_ = {
      bstack11l1l11_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࠪ൚"): bstack11l1l11_opy_ (u"ࠪࡔࡾࡺࡥࡴࡶ࠰ࡧࡺࡩࡵ࡮ࡤࡨࡶࠬ൛") if bstack1lllll1111_opy_ == bstack11l1l11_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ൜") and bstack1lll1ll11l_opy_() else framework_name,
      bstack11l1l11_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ൝"): bstack1l1ll1l1l1_opy_(framework_name),
      bstack11l1l11_opy_ (u"࠭ࡳࡥ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫ൞"): __version__,
      bstack11l1l11_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡹࡸ࡫ࡤࠨൟ"): bstack1lllll1111_opy_
    }
    if bstack1lllll1111_opy_ in bstack1l1111lll_opy_ + bstack1l11lllll1_opy_:
      if bstack1l111ll111_opy_ and bstack1l1l1l1ll1_opy_.bstack1l1111l1l_opy_(CONFIG):
        if bstack11l1l11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨൠ") in CONFIG:
          os.environ[bstack11l1l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪൡ")] = os.getenv(bstack11l1l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫൢ"), json.dumps(CONFIG[bstack11l1l11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫൣ")]))
          CONFIG[bstack11l1l11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬ൤")].pop(bstack11l1l11_opy_ (u"࠭ࡩ࡯ࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫ൥"), None)
          CONFIG[bstack11l1l11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧ൦")].pop(bstack11l1l11_opy_ (u"ࠨࡧࡻࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭൧"), None)
        bstack1l11ll1l1_opy_[bstack11l1l11_opy_ (u"ࠩࡷࡩࡸࡺࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ൨")] = {
          bstack11l1l11_opy_ (u"ࠪࡲࡦࡳࡥࠨ൩"): bstack11l1l11_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠭൪"),
          bstack11l1l11_opy_ (u"ࠬࡼࡥࡳࡵ࡬ࡳࡳ࠭൫"): str(bstack1ll1lllll_opy_())
        }
    if bstack1lllll1111_opy_ not in [bstack11l1l11_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠧ൬")] and not cli.is_running():
      bstack1ll1111lll_opy_ = bstack11lll111l1_opy_.launch(CONFIG, bstack1l11ll1l1_opy_)
  except Exception as e:
    logger.debug(bstack11ll1ll11l_opy_.format(bstack11l1l11_opy_ (u"ࠧࡕࡧࡶࡸࡍࡻࡢࠨ൭"), str(e)))
  if bstack1lllll1111_opy_ == bstack11l1l11_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨ൮"):
    bstack111lll11_opy_ = True
    if bstack1l1l11lll_opy_ and bstack1ll1l1111l_opy_:
      bstack11l1ll1l1_opy_ = CONFIG.get(bstack11l1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭൯"), {}).get(bstack11l1l11_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ൰"))
      bstack1l1111l11l_opy_(bstack11l1ll1111_opy_)
    elif bstack1l1l11lll_opy_:
      bstack11l1ll1l1_opy_ = CONFIG.get(bstack11l1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨ൱"), {}).get(bstack11l1l11_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ൲"))
      global bstack1l11ll11l1_opy_
      try:
        if bstack11l1l11l11_opy_(bstack1l1l11lll_opy_[bstack11l1l11_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩ൳")]) and multiprocessing.current_process().name == bstack11l1l11_opy_ (u"ࠧ࠱ࠩ൴"):
          bstack1l1l11lll_opy_[bstack11l1l11_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫ൵")].remove(bstack11l1l11_opy_ (u"ࠩ࠰ࡱࠬ൶"))
          bstack1l1l11lll_opy_[bstack11l1l11_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭൷")].remove(bstack11l1l11_opy_ (u"ࠫࡵࡪࡢࠨ൸"))
          bstack1l1l11lll_opy_[bstack11l1l11_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ൹")] = bstack1l1l11lll_opy_[bstack11l1l11_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩൺ")][0]
          with open(bstack1l1l11lll_opy_[bstack11l1l11_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪൻ")], bstack11l1l11_opy_ (u"ࠨࡴࠪർ")) as f:
            bstack1lllllllll_opy_ = f.read()
          bstack1l1l11ll1l_opy_ = bstack11l1l11_opy_ (u"ࠤࠥࠦ࡫ࡸ࡯࡮ࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡵࡧ࡯ࠥ࡯࡭ࡱࡱࡵࡸࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣ࡮ࡴࡩࡵ࡫ࡤࡰ࡮ࢀࡥ࠼ࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠ࡫ࡱ࡭ࡹ࡯ࡡ࡭࡫ࡽࡩ࠭ࢁࡽࠪ࠽ࠣࡪࡷࡵ࡭ࠡࡲࡧࡦࠥ࡯࡭ࡱࡱࡵࡸࠥࡖࡤࡣ࠽ࠣࡳ࡬ࡥࡤࡣࠢࡀࠤࡕࡪࡢ࠯ࡦࡲࡣࡧࡸࡥࡢ࡭࠾ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡥࡧࡩࠤࡲࡵࡤࡠࡤࡵࡩࡦࡱࠨࡴࡧ࡯ࡪ࠱ࠦࡡࡳࡩ࠯ࠤࡹ࡫࡭ࡱࡱࡵࡥࡷࡿࠠ࠾ࠢ࠳࠭࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡹࡸࡹ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡤࡶ࡬ࠦ࠽ࠡࡵࡷࡶ࠭࡯࡮ࡵࠪࡤࡶ࡬࠯ࠫ࠲࠲ࠬࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡨࡼࡨ࡫ࡰࡵࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡧࡳࠡࡧ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡵࡧࡳࡴࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡰࡩࡢࡨࡧ࠮ࡳࡦ࡮ࡩ࠰ࡦࡸࡧ࠭ࡶࡨࡱࡵࡵࡲࡢࡴࡼ࠭ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡒࡧࡦ࠳ࡪ࡯ࡠࡤࠣࡁࠥࡳ࡯ࡥࡡࡥࡶࡪࡧ࡫ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡕࡪࡢ࠯ࡦࡲࡣࡧࡸࡥࡢ࡭ࠣࡁࠥࡳ࡯ࡥࡡࡥࡶࡪࡧ࡫ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡕࡪࡢࠩࠫ࠱ࡷࡪࡺ࡟ࡵࡴࡤࡧࡪ࠮ࠩ࡝ࡰࠥࠦࠧൽ").format(str(bstack1l1l11lll_opy_))
          bstack11l111ll1_opy_ = bstack1l1l11ll1l_opy_ + bstack1lllllllll_opy_
          bstack111ll1ll_opy_ = bstack1l1l11lll_opy_[bstack11l1l11_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ൾ")] + bstack11l1l11_opy_ (u"ࠫࡤࡨࡳࡵࡣࡦ࡯ࡤࡺࡥ࡮ࡲ࠱ࡴࡾ࠭ൿ")
          with open(bstack111ll1ll_opy_, bstack11l1l11_opy_ (u"ࠬࡽࠧ඀")):
            pass
          with open(bstack111ll1ll_opy_, bstack11l1l11_opy_ (u"ࠨࡷࠬࠤඁ")) as f:
            f.write(bstack11l111ll1_opy_)
          import subprocess
          bstack1111ll11l_opy_ = subprocess.run([bstack11l1l11_opy_ (u"ࠢࡱࡻࡷ࡬ࡴࡴࠢං"), bstack111ll1ll_opy_])
          if os.path.exists(bstack111ll1ll_opy_):
            os.unlink(bstack111ll1ll_opy_)
          os._exit(bstack1111ll11l_opy_.returncode)
        else:
          if bstack11l1l11l11_opy_(bstack1l1l11lll_opy_[bstack11l1l11_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫඃ")]):
            bstack1l1l11lll_opy_[bstack11l1l11_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ඄")].remove(bstack11l1l11_opy_ (u"ࠪ࠱ࡲ࠭අ"))
            bstack1l1l11lll_opy_[bstack11l1l11_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧආ")].remove(bstack11l1l11_opy_ (u"ࠬࡶࡤࡣࠩඇ"))
            bstack1l1l11lll_opy_[bstack11l1l11_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩඈ")] = bstack1l1l11lll_opy_[bstack11l1l11_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪඉ")][0]
          bstack1l1111l11l_opy_(bstack11l1ll1111_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(bstack1l1l11lll_opy_[bstack11l1l11_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫඊ")])))
          sys.argv = sys.argv[2:]
          mod_globals = globals()
          mod_globals[bstack11l1l11_opy_ (u"ࠩࡢࡣࡳࡧ࡭ࡦࡡࡢࠫඋ")] = bstack11l1l11_opy_ (u"ࠪࡣࡤࡳࡡࡪࡰࡢࡣࠬඌ")
          mod_globals[bstack11l1l11_opy_ (u"ࠫࡤࡥࡦࡪ࡮ࡨࡣࡤ࠭ඍ")] = os.path.abspath(bstack1l1l11lll_opy_[bstack11l1l11_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨඎ")])
          exec(open(bstack1l1l11lll_opy_[bstack11l1l11_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩඏ")]).read(), mod_globals)
      except BaseException as e:
        try:
          traceback.print_exc()
          logger.error(bstack11l1l11_opy_ (u"ࠧࡄࡣࡸ࡫࡭ࡺࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰ࠽ࠤࢀࢃࠧඐ").format(str(e)))
          for driver in bstack1l11ll11l1_opy_:
            bstack1ll1l11l1l_opy_.append({
              bstack11l1l11_opy_ (u"ࠨࡰࡤࡱࡪ࠭එ"): bstack1l1l11lll_opy_[bstack11l1l11_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬඒ")],
              bstack11l1l11_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩඓ"): str(e),
              bstack11l1l11_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪඔ"): multiprocessing.current_process().name
            })
            bstack1l1l1l11l1_opy_(driver, bstack11l1l11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬඕ"), bstack11l1l11_opy_ (u"ࠨࡓࡦࡵࡶ࡭ࡴࡴࠠࡧࡣ࡬ࡰࡪࡪࠠࡸ࡫ࡷ࡬࠿ࠦ࡜࡯ࠤඖ") + str(e))
        except Exception:
          pass
      finally:
        try:
          for driver in bstack1l11ll11l1_opy_:
            driver.quit()
        except Exception as e:
          pass
    else:
      percy.init(bstack11ll11l11l_opy_, CONFIG, logger)
      bstack1ll11ll11l_opy_()
      bstack11ll1lllll_opy_()
      percy.bstack1l1l1111l1_opy_()
      bstack11llll111l_opy_ = {
        bstack11l1l11_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪ඗"): args[0],
        bstack11l1l11_opy_ (u"ࠨࡅࡒࡒࡋࡏࡇࠨ඘"): CONFIG,
        bstack11l1l11_opy_ (u"ࠩࡋ࡙ࡇࡥࡕࡓࡎࠪ඙"): bstack1111l1l1_opy_,
        bstack11l1l11_opy_ (u"ࠪࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬක"): bstack11ll11l11l_opy_
      }
      if bstack11l1l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧඛ") in CONFIG:
        bstack111l111l1_opy_ = bstack111l1l111_opy_(args, logger, CONFIG, bstack1l111ll111_opy_, bstack1l1lllllll_opy_)
        bstack1l1lll111_opy_ = bstack111l111l1_opy_.bstack1l1ll1l1_opy_(run_on_browserstack, bstack11llll111l_opy_, bstack11l1l11l11_opy_(args))
      else:
        if bstack11l1l11l11_opy_(args):
          bstack11llll111l_opy_[bstack11l1l11_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨග")] = args
          test = multiprocessing.Process(name=str(0),
                                         target=run_on_browserstack, args=(bstack11llll111l_opy_,))
          test.start()
          test.join()
        else:
          bstack1l1111l11l_opy_(bstack11l1ll1111_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(args[0])))
          mod_globals = globals()
          mod_globals[bstack11l1l11_opy_ (u"࠭࡟ࡠࡰࡤࡱࡪࡥ࡟ࠨඝ")] = bstack11l1l11_opy_ (u"ࠧࡠࡡࡰࡥ࡮ࡴ࡟ࡠࠩඞ")
          mod_globals[bstack11l1l11_opy_ (u"ࠨࡡࡢࡪ࡮ࡲࡥࡠࡡࠪඟ")] = os.path.abspath(args[0])
          sys.argv = sys.argv[2:]
          exec(open(args[0]).read(), mod_globals)
  elif bstack1lllll1111_opy_ == bstack11l1l11_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨච") or bstack1lllll1111_opy_ == bstack11l1l11_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩඡ"):
    percy.init(bstack11ll11l11l_opy_, CONFIG, logger)
    percy.bstack1l1l1111l1_opy_()
    try:
      from pabot import pabot
    except Exception as e:
      bstack11lll1ll1l_opy_(e, bstack1l1l111lll_opy_)
    bstack1ll11ll11l_opy_()
    bstack1l1111l11l_opy_(bstack111l11ll1_opy_)
    if bstack1l111ll111_opy_:
      bstack11l1l111l1_opy_(bstack111l11ll1_opy_, args)
      if bstack11l1l11_opy_ (u"ࠫ࠲࠳ࡰࡳࡱࡦࡩࡸࡹࡥࡴࠩජ") in args:
        i = args.index(bstack11l1l11_opy_ (u"ࠬ࠳࠭ࡱࡴࡲࡧࡪࡹࡳࡦࡵࠪඣ"))
        args.pop(i)
        args.pop(i)
      if bstack11l1l11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩඤ") not in CONFIG:
        CONFIG[bstack11l1l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪඥ")] = [{}]
        bstack1l1lllllll_opy_ = 1
      if bstack1l11l11l1l_opy_ == 0:
        bstack1l11l11l1l_opy_ = 1
      args.insert(0, str(bstack1l11l11l1l_opy_))
      args.insert(0, str(bstack11l1l11_opy_ (u"ࠨ࠯࠰ࡴࡷࡵࡣࡦࡵࡶࡩࡸ࠭ඦ")))
    if bstack11lll111l1_opy_.on():
      try:
        from robot.run import USAGE
        from robot.utils import ArgumentParser
        from pabot.arguments import _parse_pabot_args
        bstack1l1l1l11_opy_, pabot_args = _parse_pabot_args(args)
        opts, bstack1ll1l1l11l_opy_ = ArgumentParser(
            USAGE,
            auto_pythonpath=False,
            auto_argumentfile=True,
            env_options=bstack11l1l11_opy_ (u"ࠤࡕࡓࡇࡕࡔࡠࡑࡓࡘࡎࡕࡎࡔࠤට"),
        ).parse_args(bstack1l1l1l11_opy_)
        bstack1l1l11111l_opy_ = args.index(bstack1l1l1l11_opy_[0]) if len(bstack1l1l1l11_opy_) > 0 else len(args)
        args.insert(bstack1l1l11111l_opy_, str(bstack11l1l11_opy_ (u"ࠪ࠱࠲ࡲࡩࡴࡶࡨࡲࡪࡸࠧඨ")))
        args.insert(bstack1l1l11111l_opy_ + 1, str(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack11l1l11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡷࡵࡢࡰࡶࡢࡰ࡮ࡹࡴࡦࡰࡨࡶ࠳ࡶࡹࠨඩ"))))
        if bstack1ll11l1l1_opy_(os.environ.get(bstack11l1l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡗࡋࡒࡖࡐࠪඪ"))) and str(os.environ.get(bstack11l1l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡘࡅࡓࡗࡑࡣ࡙ࡋࡓࡕࡕࠪණ"), bstack11l1l11_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬඬ"))) != bstack11l1l11_opy_ (u"ࠨࡰࡸࡰࡱ࠭ත"):
          for bstack11l1l1ll1_opy_ in bstack1ll1l1l11l_opy_:
            args.remove(bstack11l1l1ll1_opy_)
          bstack1l11l1l1l1_opy_ = os.environ.get(bstack11l1l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡔࡈࡖ࡚ࡔ࡟ࡕࡇࡖࡘࡘ࠭ථ")).split(bstack11l1l11_opy_ (u"ࠪ࠰ࠬද"))
          for bstack1l111l1ll1_opy_ in bstack1l11l1l1l1_opy_:
            args.append(bstack1l111l1ll1_opy_)
      except Exception as e:
        logger.error(bstack11l1l11_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡤࡸࡹࡧࡣࡩ࡫ࡱ࡫ࠥࡲࡩࡴࡶࡨࡲࡪࡸࠠࡧࡱࡵࠤࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼ࠲ࠥࡋࡲࡳࡱࡵࠤ࠲ࠦࠢධ").format(e))
    pabot.main(args)
  elif bstack1lllll1111_opy_ == bstack11l1l11_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭න"):
    try:
      from robot import run_cli
    except Exception as e:
      bstack11lll1ll1l_opy_(e, bstack1l1l111lll_opy_)
    for a in args:
      if bstack11l1l11_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡖࡌࡂࡖࡉࡓࡗࡓࡉࡏࡆࡈ࡜ࠬ඲") in a:
        bstack1l1ll11111_opy_ = int(a.split(bstack11l1l11_opy_ (u"ࠧ࠻ࠩඳ"))[1])
      if bstack11l1l11_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡅࡇࡉࡐࡔࡉࡁࡍࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖࠬප") in a:
        bstack11l1ll1l1_opy_ = str(a.split(bstack11l1l11_opy_ (u"ࠩ࠽ࠫඵ"))[1])
      if bstack11l1l11_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡆࡐࡎࡇࡒࡈࡕࠪබ") in a:
        bstack1lll111l1_opy_ = str(a.split(bstack11l1l11_opy_ (u"ࠫ࠿࠭භ"))[1])
    bstack11ll111lll_opy_ = None
    if bstack11l1l11_opy_ (u"ࠬ࠳࠭ࡣࡵࡷࡥࡨࡱ࡟ࡪࡶࡨࡱࡤ࡯࡮ࡥࡧࡻࠫම") in args:
      i = args.index(bstack11l1l11_opy_ (u"࠭࠭࠮ࡤࡶࡸࡦࡩ࡫ࡠ࡫ࡷࡩࡲࡥࡩ࡯ࡦࡨࡼࠬඹ"))
      args.pop(i)
      bstack11ll111lll_opy_ = args.pop(i)
    if bstack11ll111lll_opy_ is not None:
      global bstack11l11ll111_opy_
      bstack11l11ll111_opy_ = bstack11ll111lll_opy_
    bstack1l1111l11l_opy_(bstack111l11ll1_opy_)
    run_cli(args)
    if bstack11l1l11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡦࡴࡵࡳࡷࡥ࡬ࡪࡵࡷࠫය") in multiprocessing.current_process().__dict__.keys():
      for bstack1l1ll1l1ll_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack1ll1l11l1l_opy_.append(bstack1l1ll1l1ll_opy_)
  elif bstack1lllll1111_opy_ == bstack11l1l11_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨර"):
    bstack1l11l1lll_opy_ = bstack11ll111l_opy_(args, logger, CONFIG, bstack1l111ll111_opy_)
    bstack1l11l1lll_opy_.bstack1ll111l111_opy_()
    bstack1ll11ll11l_opy_()
    bstack1lll1l11l1_opy_ = True
    bstack1l11l1ll11_opy_ = bstack1l11l1lll_opy_.bstack1111l111_opy_()
    bstack1l11l1lll_opy_.bstack11llll111l_opy_(bstack1l1lllll1_opy_)
    bstack1l11lllll_opy_ = bstack1l11l1lll_opy_.bstack1l1ll1l1_opy_(bstack11111ll1_opy_, {
      bstack11l1l11_opy_ (u"ࠩࡋ࡙ࡇࡥࡕࡓࡎࠪ඼"): bstack1111l1l1_opy_,
      bstack11l1l11_opy_ (u"ࠪࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬල"): bstack11ll11l11l_opy_,
      bstack11l1l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠧ඾"): bstack1l111ll111_opy_
    })
    try:
      bstack1lll11l1l_opy_, bstack11l1llllll_opy_ = map(list, zip(*bstack1l11lllll_opy_))
      bstack11l1l1l1l1_opy_ = bstack1lll11l1l_opy_[0]
      for status_code in bstack11l1llllll_opy_:
        if status_code != 0:
          bstack1lll1ll111_opy_ = status_code
          break
    except Exception as e:
      logger.debug(bstack11l1l11_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡤࡺࡪࠦࡥࡳࡴࡲࡶࡸࠦࡡ࡯ࡦࠣࡷࡹࡧࡴࡶࡵࠣࡧࡴࡪࡥ࠯ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡀࠠࡼࡿࠥ඿").format(str(e)))
  elif bstack1lllll1111_opy_ == bstack11l1l11_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭ව"):
    try:
      from behave.__main__ import main as bstack11l1ll11l1_opy_
      from behave.configuration import Configuration
    except Exception as e:
      bstack11lll1ll1l_opy_(e, bstack1ll1l1ll1_opy_)
    bstack1ll11ll11l_opy_()
    bstack1lll1l11l1_opy_ = True
    bstack11l1lllll1_opy_ = 1
    if bstack11l1l11_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧශ") in CONFIG:
      bstack11l1lllll1_opy_ = CONFIG[bstack11l1l11_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨෂ")]
    if bstack11l1l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬස") in CONFIG:
      bstack1ll1111l_opy_ = int(bstack11l1lllll1_opy_) * int(len(CONFIG[bstack11l1l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭හ")]))
    else:
      bstack1ll1111l_opy_ = int(bstack11l1lllll1_opy_)
    config = Configuration(args)
    bstack1ll1111l1_opy_ = config.paths
    if len(bstack1ll1111l1_opy_) == 0:
      import glob
      pattern = bstack11l1l11_opy_ (u"ࠫ࠯࠰࠯ࠫ࠰ࡩࡩࡦࡺࡵࡳࡧࠪළ")
      bstack11ll11ll_opy_ = glob.glob(pattern, recursive=True)
      args.extend(bstack11ll11ll_opy_)
      config = Configuration(args)
      bstack1ll1111l1_opy_ = config.paths
    bstack1l11l1l111_opy_ = [os.path.normpath(item) for item in bstack1ll1111l1_opy_]
    bstack11l11lll1_opy_ = [os.path.normpath(item) for item in args]
    bstack11111ll11_opy_ = [item for item in bstack11l11lll1_opy_ if item not in bstack1l11l1l111_opy_]
    import platform as pf
    if pf.system().lower() == bstack11l1l11_opy_ (u"ࠬࡽࡩ࡯ࡦࡲࡻࡸ࠭ෆ"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack1l11l1l111_opy_ = [str(PurePosixPath(PureWindowsPath(bstack1lll11llll_opy_)))
                    for bstack1lll11llll_opy_ in bstack1l11l1l111_opy_]
    bstack1l111l1l1l_opy_ = []
    for spec in bstack1l11l1l111_opy_:
      bstack1l1l11lll1_opy_ = []
      bstack1l1l11lll1_opy_ += bstack11111ll11_opy_
      bstack1l1l11lll1_opy_.append(spec)
      bstack1l111l1l1l_opy_.append(bstack1l1l11lll1_opy_)
    execution_items = []
    for bstack1l1l11lll1_opy_ in bstack1l111l1l1l_opy_:
      if bstack11l1l11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ෇") in CONFIG:
        for index, _ in enumerate(CONFIG[bstack11l1l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ෈")]):
          item = {}
          item[bstack11l1l11_opy_ (u"ࠨࡣࡵ࡫ࠬ෉")] = bstack11l1l11_opy_ (u"්ࠩࠣࠫ").join(bstack1l1l11lll1_opy_)
          item[bstack11l1l11_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩ෋")] = index
          execution_items.append(item)
      else:
        item = {}
        item[bstack11l1l11_opy_ (u"ࠫࡦࡸࡧࠨ෌")] = bstack11l1l11_opy_ (u"ࠬࠦࠧ෍").join(bstack1l1l11lll1_opy_)
        item[bstack11l1l11_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬ෎")] = 0
        execution_items.append(item)
    bstack1l1ll1l1l_opy_ = bstack1l1111l1ll_opy_(execution_items, bstack1ll1111l_opy_)
    for execution_item in bstack1l1ll1l1l_opy_:
      bstack1ll1ll1lll_opy_ = []
      for item in execution_item:
        bstack1ll1ll1lll_opy_.append(bstack1l111lll11_opy_(name=str(item[bstack11l1l11_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭ා")]),
                                             target=bstack11ll11llll_opy_,
                                             args=(item[bstack11l1l11_opy_ (u"ࠨࡣࡵ࡫ࠬැ")],)))
      for t in bstack1ll1ll1lll_opy_:
        t.start()
      for t in bstack1ll1ll1lll_opy_:
        t.join()
  else:
    bstack11111l1ll_opy_(bstack11l1ll11l_opy_)
  if not bstack1l1l11lll_opy_:
    bstack11l1ll11ll_opy_()
    if(bstack1lllll1111_opy_ in [bstack11l1l11_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩෑ"), bstack11l1l11_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪි")]):
      bstack1l1ll111l1_opy_()
  bstack111ll1l11_opy_.bstack1l1l1111_opy_()
def browserstack_initialize(bstack1l11l111ll_opy_=None):
  logger.info(bstack11l1l11_opy_ (u"ࠫࡗࡻ࡮࡯࡫ࡱ࡫࡙ࠥࡄࡌࠢࡺ࡭ࡹ࡮ࠠࡢࡴࡪࡷ࠿ࠦࠧී") + str(bstack1l11l111ll_opy_))
  run_on_browserstack(bstack1l11l111ll_opy_, None, True)
@measure(event_name=EVENTS.bstack11lll1ll_opy_, stage=STAGE.bstack1l1ll1lll_opy_, bstack11ll11ll11_opy_=bstack11l1l1lll_opy_)
def bstack11l1ll11ll_opy_():
  global CONFIG
  global bstack11llllll1_opy_
  global bstack1lll1ll111_opy_
  global bstack1l1l1ll1l1_opy_
  global bstack111ll1lll_opy_
  if cli.is_running():
    bstack11l11ll11l_opy_.invoke(bstack1llll111ll_opy_.bstack1ll11111ll_opy_)
  if bstack11llllll1_opy_ == bstack11l1l11_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬු"):
    if not cli.is_enabled(CONFIG):
      bstack11lll111l1_opy_.stop()
  else:
    bstack11lll111l1_opy_.stop()
  if not cli.is_enabled(CONFIG):
    bstack11l11l11_opy_.bstack11l11lllll_opy_()
  if bstack11l1l11_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪ෕") in CONFIG and str(CONFIG[bstack11l1l11_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫූ")]).lower() != bstack11l1l11_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧ෗"):
    bstack1l111111l1_opy_, bstack1l1llll1ll_opy_ = bstack1l1ll11l11_opy_()
  else:
    bstack1l111111l1_opy_, bstack1l1llll1ll_opy_ = get_build_link()
  bstack1l1llllll1_opy_(bstack1l111111l1_opy_)
  logger.info(bstack11l1l11_opy_ (u"ࠩࡖࡈࡐࠦࡲࡶࡰࠣࡩࡳࡪࡥࡥࠢࡩࡳࡷࠦࡩࡥ࠼ࠪෘ") + bstack111ll1lll_opy_.get_property(bstack11l1l11_opy_ (u"ࠪࡷࡩࡱࡒࡶࡰࡌࡨࠬෙ"), bstack11l1l11_opy_ (u"ࠫࠬේ")) + bstack11l1l11_opy_ (u"ࠬ࠲ࠠࡵࡧࡶࡸ࡭ࡻࡢࠡ࡫ࡧ࠾ࠥ࠭ෛ") + os.getenv(bstack11l1l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫො"), bstack11l1l11_opy_ (u"ࠧࠨෝ")))
  if bstack1l111111l1_opy_ is not None and bstack1l1l11ll1_opy_() != -1:
    sessions = bstack11ll1111l_opy_(bstack1l111111l1_opy_)
    bstack1111lll1_opy_(sessions, bstack1l1llll1ll_opy_)
  if bstack11llllll1_opy_ == bstack11l1l11_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨෞ") and bstack1lll1ll111_opy_ != 0:
    sys.exit(bstack1lll1ll111_opy_)
  if bstack11llllll1_opy_ == bstack11l1l11_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩෟ") and bstack1l1l1ll1l1_opy_ != 0:
    sys.exit(bstack1l1l1ll1l1_opy_)
def bstack1l1llllll1_opy_(new_id):
    global bstack1111l1111_opy_
    bstack1111l1111_opy_ = new_id
def bstack11ll11111l_opy_(bstack11l1l11ll_opy_):
  if bstack11l1l11ll_opy_:
    return bstack11l1l11ll_opy_.capitalize()
  else:
    return bstack11l1l11_opy_ (u"ࠪࠫ෠")
@measure(event_name=EVENTS.bstack11l1l1l1_opy_, stage=STAGE.bstack1l1ll1lll_opy_, bstack11ll11ll11_opy_=bstack11l1l1lll_opy_)
def bstack11l11ll1l_opy_(bstack11lll1l11_opy_):
  if bstack11l1l11_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ෡") in bstack11lll1l11_opy_ and bstack11lll1l11_opy_[bstack11l1l11_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ෢")] != bstack11l1l11_opy_ (u"࠭ࠧ෣"):
    return bstack11lll1l11_opy_[bstack11l1l11_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ෤")]
  else:
    bstack11ll11ll11_opy_ = bstack11l1l11_opy_ (u"ࠣࠤ෥")
    if bstack11l1l11_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࠩ෦") in bstack11lll1l11_opy_ and bstack11lll1l11_opy_[bstack11l1l11_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࠪ෧")] != None:
      bstack11ll11ll11_opy_ += bstack11lll1l11_opy_[bstack11l1l11_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࠫ෨")] + bstack11l1l11_opy_ (u"ࠧ࠲ࠠࠣ෩")
      if bstack11lll1l11_opy_[bstack11l1l11_opy_ (u"࠭࡯ࡴࠩ෪")] == bstack11l1l11_opy_ (u"ࠢࡪࡱࡶࠦ෫"):
        bstack11ll11ll11_opy_ += bstack11l1l11_opy_ (u"ࠣ࡫ࡒࡗࠥࠨ෬")
      bstack11ll11ll11_opy_ += (bstack11lll1l11_opy_[bstack11l1l11_opy_ (u"ࠩࡲࡷࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭෭")] or bstack11l1l11_opy_ (u"ࠪࠫ෮"))
      return bstack11ll11ll11_opy_
    else:
      bstack11ll11ll11_opy_ += bstack11ll11111l_opy_(bstack11lll1l11_opy_[bstack11l1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬ෯")]) + bstack11l1l11_opy_ (u"ࠧࠦࠢ෰") + (
              bstack11lll1l11_opy_[bstack11l1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ෱")] or bstack11l1l11_opy_ (u"ࠧࠨෲ")) + bstack11l1l11_opy_ (u"ࠣ࠮ࠣࠦෳ")
      if bstack11lll1l11_opy_[bstack11l1l11_opy_ (u"ࠩࡲࡷࠬ෴")] == bstack11l1l11_opy_ (u"࡛ࠥ࡮ࡴࡤࡰࡹࡶࠦ෵"):
        bstack11ll11ll11_opy_ += bstack11l1l11_opy_ (u"ࠦ࡜࡯࡮ࠡࠤ෶")
      bstack11ll11ll11_opy_ += bstack11lll1l11_opy_[bstack11l1l11_opy_ (u"ࠬࡵࡳࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ෷")] or bstack11l1l11_opy_ (u"࠭ࠧ෸")
      return bstack11ll11ll11_opy_
@measure(event_name=EVENTS.bstack1ll1l1l1l_opy_, stage=STAGE.bstack1l1ll1lll_opy_, bstack11ll11ll11_opy_=bstack11l1l1lll_opy_)
def bstack11l1l1llll_opy_(bstack1llll1l1l_opy_):
  if bstack1llll1l1l_opy_ == bstack11l1l11_opy_ (u"ࠢࡥࡱࡱࡩࠧ෹"):
    return bstack11l1l11_opy_ (u"ࠨ࠾ࡷࡨࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࠤࡸࡺࡹ࡭ࡧࡀࠦࡨࡵ࡬ࡰࡴ࠽࡫ࡷ࡫ࡥ࡯࠽ࠥࡂࡁ࡬࡯࡯ࡶࠣࡧࡴࡲ࡯ࡳ࠿ࠥ࡫ࡷ࡫ࡥ࡯ࠤࡁࡇࡴࡳࡰ࡭ࡧࡷࡩࡩࡂ࠯ࡧࡱࡱࡸࡃࡂ࠯ࡵࡦࡁࠫ෺")
  elif bstack1llll1l1l_opy_ == bstack11l1l11_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤ෻"):
    return bstack11l1l11_opy_ (u"ࠪࡀࡹࡪࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࠦࡳࡵࡻ࡯ࡩࡂࠨࡣࡰ࡮ࡲࡶ࠿ࡸࡥࡥ࠽ࠥࡂࡁ࡬࡯࡯ࡶࠣࡧࡴࡲ࡯ࡳ࠿ࠥࡶࡪࡪࠢ࠿ࡈࡤ࡭ࡱ࡫ࡤ࠽࠱ࡩࡳࡳࡺ࠾࠽࠱ࡷࡨࡃ࠭෼")
  elif bstack1llll1l1l_opy_ == bstack11l1l11_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦ෽"):
    return bstack11l1l11_opy_ (u"ࠬࡂࡴࡥࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢࠡࡵࡷࡽࡱ࡫࠽ࠣࡥࡲࡰࡴࡸ࠺ࡨࡴࡨࡩࡳࡁࠢ࠿࠾ࡩࡳࡳࡺࠠࡤࡱ࡯ࡳࡷࡃࠢࡨࡴࡨࡩࡳࠨ࠾ࡑࡣࡶࡷࡪࡪ࠼࠰ࡨࡲࡲࡹࡄ࠼࠰ࡶࡧࡂࠬ෾")
  elif bstack1llll1l1l_opy_ == bstack11l1l11_opy_ (u"ࠨࡥࡳࡴࡲࡶࠧ෿"):
    return bstack11l1l11_opy_ (u"ࠧ࠽ࡶࡧࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࠣࡷࡹࡿ࡬ࡦ࠿ࠥࡧࡴࡲ࡯ࡳ࠼ࡵࡩࡩࡁࠢ࠿࠾ࡩࡳࡳࡺࠠࡤࡱ࡯ࡳࡷࡃࠢࡳࡧࡧࠦࡃࡋࡲࡳࡱࡵࡀ࠴࡬࡯࡯ࡶࡁࡀ࠴ࡺࡤ࠿ࠩ฀")
  elif bstack1llll1l1l_opy_ == bstack11l1l11_opy_ (u"ࠣࡶ࡬ࡱࡪࡵࡵࡵࠤก"):
    return bstack11l1l11_opy_ (u"ࠩ࠿ࡸࡩࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࠥࡹࡴࡺ࡮ࡨࡁࠧࡩ࡯࡭ࡱࡵ࠾ࠨ࡫ࡥࡢ࠵࠵࠺ࡀࠨ࠾࠽ࡨࡲࡲࡹࠦࡣࡰ࡮ࡲࡶࡂࠨࠣࡦࡧࡤ࠷࠷࠼ࠢ࠿ࡖ࡬ࡱࡪࡵࡵࡵ࠾࠲ࡪࡴࡴࡴ࠿࠾࠲ࡸࡩࡄࠧข")
  elif bstack1llll1l1l_opy_ == bstack11l1l11_opy_ (u"ࠥࡶࡺࡴ࡮ࡪࡰࡪࠦฃ"):
    return bstack11l1l11_opy_ (u"ࠫࡁࡺࡤࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨࠠࡴࡶࡼࡰࡪࡃࠢࡤࡱ࡯ࡳࡷࡀࡢ࡭ࡣࡦ࡯ࡀࠨ࠾࠽ࡨࡲࡲࡹࠦࡣࡰ࡮ࡲࡶࡂࠨࡢ࡭ࡣࡦ࡯ࠧࡄࡒࡶࡰࡱ࡭ࡳ࡭࠼࠰ࡨࡲࡲࡹࡄ࠼࠰ࡶࡧࡂࠬค")
  else:
    return bstack11l1l11_opy_ (u"ࠬࡂࡴࡥࠢࡤࡰ࡮࡭࡮࠾ࠤࡦࡩࡳࡺࡥࡳࠤࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࠢࡶࡸࡾࡲࡥ࠾ࠤࡦࡳࡱࡵࡲ࠻ࡤ࡯ࡥࡨࡱ࠻ࠣࡀ࠿ࡪࡴࡴࡴࠡࡥࡲࡰࡴࡸ࠽ࠣࡤ࡯ࡥࡨࡱࠢ࠿ࠩฅ") + bstack11ll11111l_opy_(
      bstack1llll1l1l_opy_) + bstack11l1l11_opy_ (u"࠭࠼࠰ࡨࡲࡲࡹࡄ࠼࠰ࡶࡧࡂࠬฆ")
def bstack11l1ll111_opy_(session):
  return bstack11l1l11_opy_ (u"ࠧ࠽ࡶࡵࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡷࡵࡷࠣࡀ࠿ࡸࡩࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠲ࡴࡡ࡮ࡧࠥࡂࡁࡧࠠࡩࡴࡨࡪࡂࠨࡻࡾࠤࠣࡸࡦࡸࡧࡦࡶࡀࠦࡤࡨ࡬ࡢࡰ࡮ࠦࡃࢁࡽ࠽࠱ࡤࡂࡁ࠵ࡴࡥࡀࡾࢁࢀࢃ࠼ࡵࡦࠣࡥࡱ࡯ࡧ࡯࠿ࠥࡧࡪࡴࡴࡦࡴࠥࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࡁࡿࢂࡂ࠯ࡵࡦࡁࡀࡹࡪࠠࡢ࡮࡬࡫ࡳࡃࠢࡤࡧࡱࡸࡪࡸࠢࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨ࠾ࡼࡿ࠿࠳ࡹࡪ࠾࠽ࡶࡧࠤࡦࡲࡩࡨࡰࡀࠦࡨ࡫࡮ࡵࡧࡵࠦࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࡂࢀࢃ࠼࠰ࡶࡧࡂࡁࡺࡤࠡࡣ࡯࡭࡬ࡴ࠽ࠣࡥࡨࡲࡹ࡫ࡲࠣࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢ࠿ࡽࢀࡀ࠴ࡺࡤ࠿࠾࠲ࡸࡷࡄࠧง").format(
    session[bstack11l1l11_opy_ (u"ࠨࡲࡸࡦࡱ࡯ࡣࡠࡷࡵࡰࠬจ")], bstack11l11ll1l_opy_(session), bstack11l1l1llll_opy_(session[bstack11l1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡵࡷࡥࡹࡻࡳࠨฉ")]),
    bstack11l1l1llll_opy_(session[bstack11l1l11_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪช")]),
    bstack11ll11111l_opy_(session[bstack11l1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬซ")] or session[bstack11l1l11_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࠬฌ")] or bstack11l1l11_opy_ (u"࠭ࠧญ")) + bstack11l1l11_opy_ (u"ࠢࠡࠤฎ") + (session[bstack11l1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪฏ")] or bstack11l1l11_opy_ (u"ࠩࠪฐ")),
    session[bstack11l1l11_opy_ (u"ࠪࡳࡸ࠭ฑ")] + bstack11l1l11_opy_ (u"ࠦࠥࠨฒ") + session[bstack11l1l11_opy_ (u"ࠬࡵࡳࡠࡸࡨࡶࡸ࡯࡯࡯ࠩณ")], session[bstack11l1l11_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࠨด")] or bstack11l1l11_opy_ (u"ࠧࠨต"),
    session[bstack11l1l11_opy_ (u"ࠨࡥࡵࡩࡦࡺࡥࡥࡡࡤࡸࠬถ")] if session[bstack11l1l11_opy_ (u"ࠩࡦࡶࡪࡧࡴࡦࡦࡢࡥࡹ࠭ท")] else bstack11l1l11_opy_ (u"ࠪࠫธ"))
@measure(event_name=EVENTS.bstack11ll1l111_opy_, stage=STAGE.bstack1l1ll1lll_opy_, bstack11ll11ll11_opy_=bstack11l1l1lll_opy_)
def bstack1111lll1_opy_(sessions, bstack1l1llll1ll_opy_):
  try:
    bstack1lllll1l1l_opy_ = bstack11l1l11_opy_ (u"ࠦࠧน")
    if not os.path.exists(bstack1ll1lll111_opy_):
      os.mkdir(bstack1ll1lll111_opy_)
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack11l1l11_opy_ (u"ࠬࡧࡳࡴࡧࡷࡷ࠴ࡸࡥࡱࡱࡵࡸ࠳࡮ࡴ࡮࡮ࠪบ")), bstack11l1l11_opy_ (u"࠭ࡲࠨป")) as f:
      bstack1lllll1l1l_opy_ = f.read()
    bstack1lllll1l1l_opy_ = bstack1lllll1l1l_opy_.replace(bstack11l1l11_opy_ (u"ࠧࡼࠧࡕࡉࡘ࡛ࡌࡕࡕࡢࡇࡔ࡛ࡎࡕࠧࢀࠫผ"), str(len(sessions)))
    bstack1lllll1l1l_opy_ = bstack1lllll1l1l_opy_.replace(bstack11l1l11_opy_ (u"ࠨࡽࠨࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠫࡽࠨฝ"), bstack1l1llll1ll_opy_)
    bstack1lllll1l1l_opy_ = bstack1lllll1l1l_opy_.replace(bstack11l1l11_opy_ (u"ࠩࡾࠩࡇ࡛ࡉࡍࡆࡢࡒࡆࡓࡅࠦࡿࠪพ"),
                                              sessions[0].get(bstack11l1l11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡࡱࡥࡲ࡫ࠧฟ")) if sessions[0] else bstack11l1l11_opy_ (u"ࠫࠬภ"))
    with open(os.path.join(bstack1ll1lll111_opy_, bstack11l1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠱ࡷ࡫ࡰࡰࡴࡷ࠲࡭ࡺ࡭࡭ࠩม")), bstack11l1l11_opy_ (u"࠭ࡷࠨย")) as stream:
      stream.write(bstack1lllll1l1l_opy_.split(bstack11l1l11_opy_ (u"ࠧࡼࠧࡖࡉࡘ࡙ࡉࡐࡐࡖࡣࡉࡇࡔࡂࠧࢀࠫร"))[0])
      for session in sessions:
        stream.write(bstack11l1ll111_opy_(session))
      stream.write(bstack1lllll1l1l_opy_.split(bstack11l1l11_opy_ (u"ࠨࡽࠨࡗࡊ࡙ࡓࡊࡑࡑࡗࡤࡊࡁࡕࡃࠨࢁࠬฤ"))[1])
    logger.info(bstack11l1l11_opy_ (u"ࠩࡊࡩࡳ࡫ࡲࡢࡶࡨࡨࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡧࡻࡩ࡭ࡦࠣࡥࡷࡺࡩࡧࡣࡦࡸࡸࠦࡡࡵࠢࡾࢁࠬล").format(bstack1ll1lll111_opy_));
  except Exception as e:
    logger.debug(bstack11l1lllll_opy_.format(str(e)))
def bstack11ll1111l_opy_(bstack1l111111l1_opy_):
  global CONFIG
  try:
    bstack1l1ll1l111_opy_ = datetime.datetime.now()
    host = bstack11l1l11_opy_ (u"ࠪࡥࡵ࡯࠭ࡤ࡮ࡲࡹࡩ࠭ฦ") if bstack11l1l11_opy_ (u"ࠫࡦࡶࡰࠨว") in CONFIG else bstack11l1l11_opy_ (u"ࠬࡧࡰࡪࠩศ")
    user = CONFIG[bstack11l1l11_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨษ")]
    key = CONFIG[bstack11l1l11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪส")]
    bstack1l11l111l_opy_ = bstack11l1l11_opy_ (u"ࠨࡣࡳࡴ࠲ࡧࡵࡵࡱࡰࡥࡹ࡫ࠧห") if bstack11l1l11_opy_ (u"ࠩࡤࡴࡵ࠭ฬ") in CONFIG else (bstack11l1l11_opy_ (u"ࠪࡸࡺࡸࡢࡰࡵࡦࡥࡱ࡫ࠧอ") if CONFIG.get(bstack11l1l11_opy_ (u"ࠫࡹࡻࡲࡣࡱࡶࡧࡦࡲࡥࠨฮ")) else bstack11l1l11_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡫ࠧฯ"))
    url = bstack11l1l11_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡼࡿ࠽ࡿࢂࡆࡻࡾ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࢁࡽ࠰ࡤࡸ࡭ࡱࡪࡳ࠰ࡽࢀ࠳ࡸ࡫ࡳࡴ࡫ࡲࡲࡸ࠴ࡪࡴࡱࡱࠫะ").format(user, key, host, bstack1l11l111l_opy_,
                                                                                bstack1l111111l1_opy_)
    headers = {
      bstack11l1l11_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡶࡼࡴࡪ࠭ั"): bstack11l1l11_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫา"),
    }
    proxies = bstack1ll11lll1_opy_(CONFIG, url)
    response = requests.get(url, headers=headers, proxies=proxies)
    if response.json():
      cli.bstack1ll11lll_opy_(bstack11l1l11_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺ࡨࡧࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡸࡥ࡬ࡪࡵࡷࠦำ"), datetime.datetime.now() - bstack1l1ll1l111_opy_)
      return list(map(lambda session: session[bstack11l1l11_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠨิ")], response.json()))
  except Exception as e:
    logger.debug(bstack111ll11l1_opy_.format(str(e)))
@measure(event_name=EVENTS.bstack11lll11lll_opy_, stage=STAGE.bstack1l1ll1lll_opy_, bstack11ll11ll11_opy_=bstack11l1l1lll_opy_)
def get_build_link():
  global CONFIG
  global bstack1111l1111_opy_
  try:
    if bstack11l1l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧี") in CONFIG:
      bstack1l1ll1l111_opy_ = datetime.datetime.now()
      host = bstack11l1l11_opy_ (u"ࠬࡧࡰࡪ࠯ࡦࡰࡴࡻࡤࠨึ") if bstack11l1l11_opy_ (u"࠭ࡡࡱࡲࠪื") in CONFIG else bstack11l1l11_opy_ (u"ࠧࡢࡲ࡬ุࠫ")
      user = CONFIG[bstack11l1l11_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧูࠪ")]
      key = CONFIG[bstack11l1l11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽฺࠬ")]
      bstack1l11l111l_opy_ = bstack11l1l11_opy_ (u"ࠪࡥࡵࡶ࠭ࡢࡷࡷࡳࡲࡧࡴࡦࠩ฻") if bstack11l1l11_opy_ (u"ࠫࡦࡶࡰࠨ฼") in CONFIG else bstack11l1l11_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡫ࠧ฽")
      url = bstack11l1l11_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡼࡿ࠽ࡿࢂࡆࡻࡾ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࢁࡽ࠰ࡤࡸ࡭ࡱࡪࡳ࠯࡬ࡶࡳࡳ࠭฾").format(user, key, host, bstack1l11l111l_opy_)
      headers = {
        bstack11l1l11_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡶࡼࡴࡪ࠭฿"): bstack11l1l11_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫเ"),
      }
      if bstack11l1l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫแ") in CONFIG:
        params = {bstack11l1l11_opy_ (u"ࠪࡲࡦࡳࡥࠨโ"): CONFIG[bstack11l1l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧใ")], bstack11l1l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨไ"): CONFIG[bstack11l1l11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨๅ")]}
      else:
        params = {bstack11l1l11_opy_ (u"ࠧ࡯ࡣࡰࡩࠬๆ"): CONFIG[bstack11l1l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ็")]}
      proxies = bstack1ll11lll1_opy_(CONFIG, url)
      response = requests.get(url, params=params, headers=headers, proxies=proxies)
      if response.json():
        bstack11l1ll1lll_opy_ = response.json()[0][bstack11l1l11_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡢࡶ࡫࡯ࡨ่ࠬ")]
        if bstack11l1ll1lll_opy_:
          bstack1l1llll1ll_opy_ = bstack11l1ll1lll_opy_[bstack11l1l11_opy_ (u"ࠪࡴࡺࡨ࡬ࡪࡥࡢࡹࡷࡲ้ࠧ")].split(bstack11l1l11_opy_ (u"ࠫࡵࡻࡢ࡭࡫ࡦ࠱ࡧࡻࡩ࡭ࡦ๊ࠪ"))[0] + bstack11l1l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡷ࠴๋࠭") + bstack11l1ll1lll_opy_[
            bstack11l1l11_opy_ (u"࠭ࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩ์")]
          logger.info(bstack1l1111ll1_opy_.format(bstack1l1llll1ll_opy_))
          bstack1111l1111_opy_ = bstack11l1ll1lll_opy_[bstack11l1l11_opy_ (u"ࠧࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪํ")]
          bstack1llll1llll_opy_ = CONFIG[bstack11l1l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ๎")]
          if bstack11l1l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ๏") in CONFIG:
            bstack1llll1llll_opy_ += bstack11l1l11_opy_ (u"ࠪࠤࠬ๐") + CONFIG[bstack11l1l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭๑")]
          if bstack1llll1llll_opy_ != bstack11l1ll1lll_opy_[bstack11l1l11_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ๒")]:
            logger.debug(bstack1l11l111_opy_.format(bstack11l1ll1lll_opy_[bstack11l1l11_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ๓")], bstack1llll1llll_opy_))
          cli.bstack1ll11lll_opy_(bstack11l1l11_opy_ (u"ࠢࡩࡶࡷࡴ࠿࡭ࡥࡵࡡࡥࡹ࡮ࡲࡤࡠ࡮࡬ࡲࡰࠨ๔"), datetime.datetime.now() - bstack1l1ll1l111_opy_)
          return [bstack11l1ll1lll_opy_[bstack11l1l11_opy_ (u"ࠨࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫ๕")], bstack1l1llll1ll_opy_]
    else:
      logger.warn(bstack1ll1ll111l_opy_)
  except Exception as e:
    logger.debug(bstack11l1ll11_opy_.format(str(e)))
  return [None, None]
def bstack1l1ll1ll_opy_(url, bstack1ll11l1l_opy_=False):
  global CONFIG
  global bstack1l1l111111_opy_
  if not bstack1l1l111111_opy_:
    hostname = bstack11l1ll1l1l_opy_(url)
    is_private = bstack111111l1_opy_(hostname)
    if (bstack11l1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭๖") in CONFIG and not bstack1ll11l1l1_opy_(CONFIG[bstack11l1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ๗")])) and (is_private or bstack1ll11l1l_opy_):
      bstack1l1l111111_opy_ = hostname
def bstack11l1ll1l1l_opy_(url):
  return urlparse(url).hostname
def bstack111111l1_opy_(hostname):
  for bstack111l11l11_opy_ in bstack1llll1ll11_opy_:
    regex = re.compile(bstack111l11l11_opy_)
    if regex.match(hostname):
      return True
  return False
def bstack11lll11l1l_opy_(bstack11111l11l_opy_):
  return True if bstack11111l11l_opy_ in threading.current_thread().__dict__.keys() else False
@measure(event_name=EVENTS.bstack1ll1l1lll1_opy_, stage=STAGE.bstack1l1ll1lll_opy_, bstack11ll11ll11_opy_=bstack11l1l1lll_opy_)
def getAccessibilityResults(driver):
  global CONFIG
  global bstack1l1ll11111_opy_
  bstack1lllll1ll1_opy_ = not (bstack1llllllll1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"ࠫ࡮ࡹࡁ࠲࠳ࡼࡘࡪࡹࡴࠨ๘"), None) and bstack1llllllll1_opy_(
          threading.current_thread(), bstack11l1l11_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫ๙"), None))
  bstack1l1ll111l_opy_ = getattr(driver, bstack11l1l11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡇ࠱࠲ࡻࡖ࡬ࡴࡻ࡬ࡥࡕࡦࡥࡳ࠭๚"), None) != True
  bstack11ll1ll1ll_opy_ = bstack1llllllll1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"ࠧࡪࡵࡄࡴࡵࡇ࠱࠲ࡻࡗࡩࡸࡺࠧ๛"), None) and bstack1llllllll1_opy_(
          threading.current_thread(), bstack11l1l11_opy_ (u"ࠨࡣࡳࡴࡆ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ๜"), None)
  if bstack11ll1ll1ll_opy_:
    if not bstack11l1l1l111_opy_():
      logger.warning(bstack11l1l11_opy_ (u"ࠤࡑࡳࡹࠦࡡ࡯ࠢࡄࡴࡵࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡷࡪࡹࡳࡪࡱࡱ࠰ࠥࡩࡡ࡯ࡰࡲࡸࠥࡸࡥࡵࡴ࡬ࡩࡻ࡫ࠠࡂࡲࡳࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡷ࡫ࡳࡶ࡮ࡷࡷ࠳ࠨ๝"))
      return {}
    logger.debug(bstack11l1l11_opy_ (u"ࠪࡔࡪࡸࡦࡰࡴࡰ࡭ࡳ࡭ࠠࡴࡥࡤࡲࠥࡨࡥࡧࡱࡵࡩࠥ࡭ࡥࡵࡶ࡬ࡲ࡬ࠦࡲࡦࡵࡸࡰࡹࡹࠧ๞"))
    logger.debug(perform_scan(driver, driver_command=bstack11l1l11_opy_ (u"ࠫࡪࡾࡥࡤࡷࡷࡩࡘࡩࡲࡪࡲࡷࠫ๟")))
    results = bstack1ll1111ll_opy_(bstack11l1l11_opy_ (u"ࠧࡸࡥࡴࡷ࡯ࡸࡸࠨ๠"))
    if results is not None and results.get(bstack11l1l11_opy_ (u"ࠨࡩࡴࡵࡸࡩࡸࠨ๡")) is not None:
        return results[bstack11l1l11_opy_ (u"ࠢࡪࡵࡶࡹࡪࡹࠢ๢")]
    logger.error(bstack11l1l11_opy_ (u"ࠣࡐࡲࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡗ࡫ࡳࡶ࡮ࡷࡷࠥࡽࡥࡳࡧࠣࡪࡴࡻ࡮ࡥ࠰ࠥ๣"))
    return []
  if not bstack1l1l1l1ll1_opy_.bstack1l1l1l1l_opy_(CONFIG, bstack1l1ll11111_opy_) or (bstack1l1ll111l_opy_ and bstack1lllll1ll1_opy_):
    logger.warning(bstack11l1l11_opy_ (u"ࠤࡑࡳࡹࠦࡡ࡯ࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡳࡦࡵࡶ࡭ࡴࡴࠬࠡࡥࡤࡲࡳࡵࡴࠡࡴࡨࡸࡷ࡯ࡥࡷࡧࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡶࡪࡹࡵ࡭ࡶࡶ࠲ࠧ๤"))
    return {}
  try:
    logger.debug(bstack11l1l11_opy_ (u"ࠪࡔࡪࡸࡦࡰࡴࡰ࡭ࡳ࡭ࠠࡴࡥࡤࡲࠥࡨࡥࡧࡱࡵࡩࠥ࡭ࡥࡵࡶ࡬ࡲ࡬ࠦࡲࡦࡵࡸࡰࡹࡹࠧ๥"))
    logger.debug(perform_scan(driver))
    results = driver.execute_async_script(bstack11ll1lll1l_opy_.bstack11l1lll11l_opy_)
    return results
  except Exception:
    logger.error(bstack11l1l11_opy_ (u"ࠦࡓࡵࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡳࡧࡶࡹࡱࡺࡳࠡࡹࡨࡶࡪࠦࡦࡰࡷࡱࡨ࠳ࠨ๦"))
    return {}
@measure(event_name=EVENTS.bstack1lll1l11ll_opy_, stage=STAGE.bstack1l1ll1lll_opy_, bstack11ll11ll11_opy_=bstack11l1l1lll_opy_)
def getAccessibilityResultsSummary(driver):
  global CONFIG
  global bstack1l1ll11111_opy_
  bstack1lllll1ll1_opy_ = not (bstack1llllllll1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"ࠬ࡯ࡳࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩ๧"), None) and bstack1llllllll1_opy_(
          threading.current_thread(), bstack11l1l11_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬ๨"), None))
  bstack1l1ll111l_opy_ = getattr(driver, bstack11l1l11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡁ࠲࠳ࡼࡗ࡭ࡵࡵ࡭ࡦࡖࡧࡦࡴࠧ๩"), None) != True
  bstack11ll1ll1ll_opy_ = bstack1llllllll1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"ࠨ࡫ࡶࡅࡵࡶࡁ࠲࠳ࡼࡘࡪࡹࡴࠨ๪"), None) and bstack1llllllll1_opy_(
          threading.current_thread(), bstack11l1l11_opy_ (u"ࠩࡤࡴࡵࡇ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫ๫"), None)
  if bstack11ll1ll1ll_opy_:
    if not bstack11l1l1l111_opy_():
      logger.warning(bstack11l1l11_opy_ (u"ࠥࡒࡴࡺࠠࡢࡰࠣࡅࡵࡶࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠱ࠦࡣࡢࡰࡱࡳࡹࠦࡲࡦࡶࡵ࡭ࡪࡼࡥࠡࡃࡳࡴࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡸࡥࡴࡷ࡯ࡸࡸࠦࡳࡶ࡯ࡰࡥࡷࡿ࠮ࠣ๬"))
      return {}
    logger.debug(bstack11l1l11_opy_ (u"ࠫࡕ࡫ࡲࡧࡱࡵࡱ࡮ࡴࡧࠡࡵࡦࡥࡳࠦࡢࡦࡨࡲࡶࡪࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡳࡧࡶࡹࡱࡺࡳࠡࡵࡸࡱࡲࡧࡲࡺࠩ๭"))
    logger.debug(perform_scan(driver, driver_command=bstack11l1l11_opy_ (u"ࠬ࡫ࡸࡦࡥࡸࡸࡪ࡙ࡣࡳ࡫ࡳࡸࠬ๮")))
    results = bstack1ll1111ll_opy_(bstack11l1l11_opy_ (u"ࠨࡲࡦࡵࡸࡰࡹ࡙ࡵ࡮࡯ࡤࡶࡾࠨ๯"))
    if results is not None and results.get(bstack11l1l11_opy_ (u"ࠢࡴࡷࡰࡱࡦࡸࡹࠣ๰")) is not None:
        return results[bstack11l1l11_opy_ (u"ࠣࡵࡸࡱࡲࡧࡲࡺࠤ๱")]
    logger.error(bstack11l1l11_opy_ (u"ࠤࡑࡳࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡘࡥࡴࡷ࡯ࡸࡸࠦࡓࡶ࡯ࡰࡥࡷࡿࠠࡸࡣࡶࠤ࡫ࡵࡵ࡯ࡦ࠱ࠦ๲"))
    return {}
  if not bstack1l1l1l1ll1_opy_.bstack1l1l1l1l_opy_(CONFIG, bstack1l1ll11111_opy_) or (bstack1l1ll111l_opy_ and bstack1lllll1ll1_opy_):
    logger.warning(bstack11l1l11_opy_ (u"ࠥࡒࡴࡺࠠࡢࡰࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡴࡧࡶࡷ࡮ࡵ࡮࠭ࠢࡦࡥࡳࡴ࡯ࡵࠢࡵࡩࡹࡸࡩࡦࡸࡨࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡷ࡫ࡳࡶ࡮ࡷࡷࠥࡹࡵ࡮࡯ࡤࡶࡾ࠴ࠢ๳"))
    return {}
  try:
    logger.debug(bstack11l1l11_opy_ (u"ࠫࡕ࡫ࡲࡧࡱࡵࡱ࡮ࡴࡧࠡࡵࡦࡥࡳࠦࡢࡦࡨࡲࡶࡪࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡳࡧࡶࡹࡱࡺࡳࠡࡵࡸࡱࡲࡧࡲࡺࠩ๴"))
    logger.debug(perform_scan(driver))
    bstack11llll11_opy_ = driver.execute_async_script(bstack11ll1lll1l_opy_.bstack1l111ll11_opy_)
    return bstack11llll11_opy_
  except Exception:
    logger.error(bstack11l1l11_opy_ (u"ࠧࡔ࡯ࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡵࡸࡱࡲࡧࡲࡺࠢࡺࡥࡸࠦࡦࡰࡷࡱࡨ࠳ࠨ๵"))
    return {}
def bstack11l1l1l111_opy_():
  global CONFIG
  global bstack1l1ll11111_opy_
  bstack1l1ll111_opy_ = bstack1llllllll1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"࠭ࡩࡴࡃࡳࡴࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭๶"), None) and bstack1llllllll1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"ࠧࡢࡲࡳࡅ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ๷"), None)
  if not bstack1l1l1l1ll1_opy_.bstack1l1l1l1l_opy_(CONFIG, bstack1l1ll11111_opy_) or not bstack1l1ll111_opy_:
        logger.warning(bstack11l1l11_opy_ (u"ࠣࡐࡲࡸࠥࡧ࡮ࠡࡃࡳࡴࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡶࡩࡸࡹࡩࡰࡰ࠯ࠤࡨࡧ࡮࡯ࡱࡷࠤࡷ࡫ࡴࡳ࡫ࡨࡺࡪࠦࡲࡦࡵࡸࡰࡹࡹ࠮ࠣ๸"))
        return False
  return True
def bstack1ll1111ll_opy_(bstack1ll11l1ll_opy_):
    bstack1111l1ll_opy_ = bstack11lll111l1_opy_.current_test_uuid() if bstack11lll111l1_opy_.current_test_uuid() else bstack11l11l11_opy_.current_hook_uuid()
    with ThreadPoolExecutor() as executor:
        future = executor.submit(bstack1l1l111l11_opy_(bstack1111l1ll_opy_, bstack1ll11l1ll_opy_))
        try:
            return future.result(timeout=bstack1l1lll111l_opy_)
        except TimeoutError:
            logger.error(bstack11l1l11_opy_ (u"ࠤࡗ࡭ࡲ࡫࡯ࡶࡶࠣࡥ࡫ࡺࡥࡳࠢࡾࢁࡸࠦࡷࡩ࡫࡯ࡩࠥ࡬ࡥࡵࡥ࡫࡭ࡳ࡭ࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡓࡧࡶࡹࡱࡺࡳࠣ๹").format(bstack1l1lll111l_opy_))
        except Exception as ex:
            logger.debug(bstack11l1l11_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡵࡩࡹࡸࡩࡦࡸ࡬ࡲ࡬ࠦࡁࡱࡲࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡼࡿ࠱ࠤࡊࡸࡲࡰࡴࠣ࠱ࠥࢁࡽࠣ๺").format(bstack1ll11l1ll_opy_, str(ex)))
    return {}
@measure(event_name=EVENTS.bstack1l111l1l11_opy_, stage=STAGE.bstack1l1ll1lll_opy_, bstack11ll11ll11_opy_=bstack11l1l1lll_opy_)
def perform_scan(driver, *args, **kwargs):
  global CONFIG
  global bstack1l1ll11111_opy_
  bstack1lllll1ll1_opy_ = not (bstack1llllllll1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"ࠫ࡮ࡹࡁ࠲࠳ࡼࡘࡪࡹࡴࠨ๻"), None) and bstack1llllllll1_opy_(
          threading.current_thread(), bstack11l1l11_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫ๼"), None))
  bstack1l1l11ll11_opy_ = not (bstack1llllllll1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"࠭ࡩࡴࡃࡳࡴࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭๽"), None) and bstack1llllllll1_opy_(
          threading.current_thread(), bstack11l1l11_opy_ (u"ࠧࡢࡲࡳࡅ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ๾"), None))
  bstack1l1ll111l_opy_ = getattr(driver, bstack11l1l11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡂ࠳࠴ࡽࡘ࡮࡯ࡶ࡮ࡧࡗࡨࡧ࡮ࠨ๿"), None) != True
  if not bstack1l1l1l1ll1_opy_.bstack1l1l1l1l_opy_(CONFIG, bstack1l1ll11111_opy_) or (bstack1l1ll111l_opy_ and bstack1lllll1ll1_opy_ and bstack1l1l11ll11_opy_):
    logger.warning(bstack11l1l11_opy_ (u"ࠤࡑࡳࡹࠦࡡ࡯ࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡳࡦࡵࡶ࡭ࡴࡴࠬࠡࡥࡤࡲࡳࡵࡴࠡࡴࡸࡲࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡹࡣࡢࡰ࠱ࠦ຀"))
    return {}
  try:
    bstack1ll11ll1l1_opy_ = bstack11l1l11_opy_ (u"ࠪࡥࡵࡶࠧກ") in CONFIG and CONFIG.get(bstack11l1l11_opy_ (u"ࠫࡦࡶࡰࠨຂ"), bstack11l1l11_opy_ (u"ࠬ࠭຃"))
    session_id = getattr(driver, bstack11l1l11_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡪࡦࠪຄ"), None)
    if not session_id:
      logger.warning(bstack11l1l11_opy_ (u"ࠢࡏࡱࠣࡷࡪࡹࡳࡪࡱࡱࠤࡎࡊࠠࡧࡱࡸࡲࡩࠦࡦࡰࡴࠣࡨࡷ࡯ࡶࡦࡴࠥ຅"))
      return {bstack11l1l11_opy_ (u"ࠣࡧࡵࡶࡴࡸࠢຆ"): bstack11l1l11_opy_ (u"ࠤࡑࡳࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡉࡅࠢࡩࡳࡺࡴࡤࠣງ")}
    if bstack1ll11ll1l1_opy_:
      try:
        bstack1111l1l11_opy_ = {
              bstack11l1l11_opy_ (u"ࠪࡸ࡭ࡐࡷࡵࡖࡲ࡯ࡪࡴࠧຈ"): os.environ.get(bstack11l1l11_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩຉ"), os.environ.get(bstack11l1l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩຊ"), bstack11l1l11_opy_ (u"࠭ࠧ຋"))),
              bstack11l1l11_opy_ (u"ࠧࡵࡪࡗࡩࡸࡺࡒࡶࡰࡘࡹ࡮ࡪࠧຌ"): bstack11lll111l1_opy_.current_test_uuid() if bstack11lll111l1_opy_.current_test_uuid() else bstack11l11l11_opy_.current_hook_uuid(),
              bstack11l1l11_opy_ (u"ࠨࡣࡸࡸ࡭ࡎࡥࡢࡦࡨࡶࠬຍ"): os.environ.get(bstack11l1l11_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧຎ")),
              bstack11l1l11_opy_ (u"ࠪࡷࡨࡧ࡮ࡕ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪຏ"): str(int(datetime.datetime.now().timestamp() * 1000)),
              bstack11l1l11_opy_ (u"ࠫࡹ࡮ࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠩຐ"): os.environ.get(bstack11l1l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪຑ"), bstack11l1l11_opy_ (u"࠭ࠧຒ")),
              bstack11l1l11_opy_ (u"ࠧ࡮ࡧࡷ࡬ࡴࡪࠧຓ"): kwargs.get(bstack11l1l11_opy_ (u"ࠨࡦࡵ࡭ࡻ࡫ࡲࡠࡥࡲࡱࡲࡧ࡮ࡥࠩດ"), None) or bstack11l1l11_opy_ (u"ࠩࠪຕ")
          }
        if not hasattr(thread_local, bstack11l1l11_opy_ (u"ࠪࡦࡦࡹࡥࡠࡣࡳࡴࡤࡧ࠱࠲ࡻࡢࡷࡨࡸࡩࡱࡶࠪຖ")):
            scripts = {bstack11l1l11_opy_ (u"ࠫࡸࡩࡡ࡯ࠩທ"): bstack11ll1lll1l_opy_.perform_scan}
            thread_local.base_app_a11y_script = scripts
        bstack1l1l11l111_opy_ = copy.deepcopy(thread_local.base_app_a11y_script)
        bstack1l1l11l111_opy_[bstack11l1l11_opy_ (u"ࠬࡹࡣࡢࡰࠪຘ")] = bstack1l1l11l111_opy_[bstack11l1l11_opy_ (u"࠭ࡳࡤࡣࡱࠫນ")] % json.dumps(bstack1111l1l11_opy_)
        bstack11ll1lll1l_opy_.bstack1l1l1l1111_opy_(bstack1l1l11l111_opy_)
        bstack11ll1lll1l_opy_.store()
        bstack11llllll11_opy_ = driver.execute_script(bstack11ll1lll1l_opy_.perform_scan)
      except Exception as bstack1l111llll1_opy_:
        logger.info(bstack11l1l11_opy_ (u"ࠢࡂࡲࡳ࡭ࡺࡳࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡴࡥࡤࡲࠥ࡬ࡡࡪ࡮ࡨࡨ࠿ࠦࠢບ") + str(bstack1l111llll1_opy_))
        bstack11llllll11_opy_ = {bstack11l1l11_opy_ (u"ࠣࡧࡵࡶࡴࡸࠢປ"): str(bstack1l111llll1_opy_)}
    else:
      bstack11llllll11_opy_ = driver.execute_async_script(bstack11ll1lll1l_opy_.perform_scan, {bstack11l1l11_opy_ (u"ࠩࡰࡩࡹ࡮࡯ࡥࠩຜ"): kwargs.get(bstack11l1l11_opy_ (u"ࠪࡨࡷ࡯ࡶࡦࡴࡢࡧࡴࡳ࡭ࡢࡰࡧࠫຝ"), None) or bstack11l1l11_opy_ (u"ࠫࠬພ")})
    return bstack11llllll11_opy_
  except Exception as err:
    logger.error(bstack11l1l11_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡴࡸࡲࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡹࡣࡢࡰ࠱ࠤࢀࢃࠢຟ").format(str(err)))
    return {}
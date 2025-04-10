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
import re
import sys
import json
import time
import shutil
import tempfile
import requests
import subprocess
from threading import Thread
from os.path import expanduser
from bstack_utils.constants import *
from requests.auth import HTTPBasicAuth
from bstack_utils.helper import bstack1l11ll111l_opy_, bstack11l1lll1ll_opy_
from bstack_utils.measure import measure
class bstack1l1l11l1l_opy_:
  working_dir = os.getcwd()
  bstack11l11111l_opy_ = False
  config = {}
  bstack11l1l11l1l1_opy_ = bstack1ll1l1_opy_ (u"ࠬ࠭ᱧ")
  binary_path = bstack1ll1l1_opy_ (u"࠭ࠧᱨ")
  bstack111ll1l1l11_opy_ = bstack1ll1l1_opy_ (u"ࠧࠨᱩ")
  bstack1llll11l11_opy_ = False
  bstack111lll1l11l_opy_ = None
  bstack111lll11lll_opy_ = {}
  bstack111lll11l11_opy_ = 300
  bstack111ll1l1lll_opy_ = False
  logger = None
  bstack111ll1l11l1_opy_ = False
  bstack1111l1ll1_opy_ = False
  percy_build_id = None
  bstack111llll1l11_opy_ = bstack1ll1l1_opy_ (u"ࠨࠩᱪ")
  bstack11l111111ll_opy_ = {
    bstack1ll1l1_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࠩᱫ") : 1,
    bstack1ll1l1_opy_ (u"ࠪࡪ࡮ࡸࡥࡧࡱࡻࠫᱬ") : 2,
    bstack1ll1l1_opy_ (u"ࠫࡪࡪࡧࡦࠩᱭ") : 3,
    bstack1ll1l1_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭ࠬᱮ") : 4
  }
  def __init__(self) -> None: pass
  def bstack111lll1llll_opy_(self):
    bstack111llll1ll1_opy_ = bstack1ll1l1_opy_ (u"࠭ࠧᱯ")
    bstack111lll1l111_opy_ = sys.platform
    bstack111lll1l1l1_opy_ = bstack1ll1l1_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭ᱰ")
    if re.match(bstack1ll1l1_opy_ (u"ࠣࡦࡤࡶࡼ࡯࡮ࡽ࡯ࡤࡧࠥࡵࡳࠣᱱ"), bstack111lll1l111_opy_) != None:
      bstack111llll1ll1_opy_ = bstack11ll1ll1l11_opy_ + bstack1ll1l1_opy_ (u"ࠤ࠲ࡴࡪࡸࡣࡺ࠯ࡲࡷࡽ࠴ࡺࡪࡲࠥᱲ")
      self.bstack111llll1l11_opy_ = bstack1ll1l1_opy_ (u"ࠪࡱࡦࡩࠧᱳ")
    elif re.match(bstack1ll1l1_opy_ (u"ࠦࡲࡹࡷࡪࡰࡿࡱࡸࡿࡳࡽ࡯࡬ࡲ࡬ࡽࡼࡤࡻࡪࡻ࡮ࡴࡼࡣࡥࡦࡻ࡮ࡴࡼࡸ࡫ࡱࡧࡪࢂࡥ࡮ࡥࡿࡻ࡮ࡴ࠳࠳ࠤᱴ"), bstack111lll1l111_opy_) != None:
      bstack111llll1ll1_opy_ = bstack11ll1ll1l11_opy_ + bstack1ll1l1_opy_ (u"ࠧ࠵ࡰࡦࡴࡦࡽ࠲ࡽࡩ࡯࠰ࡽ࡭ࡵࠨᱵ")
      bstack111lll1l1l1_opy_ = bstack1ll1l1_opy_ (u"ࠨࡰࡦࡴࡦࡽ࠳࡫ࡸࡦࠤᱶ")
      self.bstack111llll1l11_opy_ = bstack1ll1l1_opy_ (u"ࠧࡸ࡫ࡱࠫᱷ")
    else:
      bstack111llll1ll1_opy_ = bstack11ll1ll1l11_opy_ + bstack1ll1l1_opy_ (u"ࠣ࠱ࡳࡩࡷࡩࡹ࠮࡮࡬ࡲࡺࡾ࠮ࡻ࡫ࡳࠦᱸ")
      self.bstack111llll1l11_opy_ = bstack1ll1l1_opy_ (u"ࠩ࡯࡭ࡳࡻࡸࠨᱹ")
    return bstack111llll1ll1_opy_, bstack111lll1l1l1_opy_
  def bstack11l11111ll1_opy_(self):
    try:
      bstack111lll11111_opy_ = [os.path.join(expanduser(bstack1ll1l1_opy_ (u"ࠥࢂࠧᱺ")), bstack1ll1l1_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫᱻ")), self.working_dir, tempfile.gettempdir()]
      for path in bstack111lll11111_opy_:
        if(self.bstack111lllll1l1_opy_(path)):
          return path
      raise bstack1ll1l1_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡦࡲࡻࡳࡲ࡯ࡢࡦࠣࡴࡪࡸࡣࡺࠢࡥ࡭ࡳࡧࡲࡺࠤᱼ")
    except Exception as e:
      self.logger.error(bstack1ll1l1_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡩ࡭ࡳࡪࠠࡢࡸࡤ࡭ࡱࡧࡢ࡭ࡧࠣࡴࡦࡺࡨࠡࡨࡲࡶࠥࡶࡥࡳࡥࡼࠤࡩࡵࡷ࡯࡮ࡲࡥࡩ࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࠱ࠥࢁࡽࠣᱽ").format(e))
  def bstack111lllll1l1_opy_(self, path):
    try:
      if not os.path.exists(path):
        os.makedirs(path)
      return True
    except:
      return False
  def bstack111llllllll_opy_(self, bstack111ll1ll1ll_opy_):
    return os.path.join(bstack111ll1ll1ll_opy_, self.bstack11l1l11l1l1_opy_ + bstack1ll1l1_opy_ (u"ࠢ࠯ࡧࡷࡥ࡬ࠨ᱾"))
  def bstack111llll11ll_opy_(self, bstack111ll1ll1ll_opy_, bstack111lllll111_opy_):
    if not bstack111lllll111_opy_: return
    try:
      bstack111llll1111_opy_ = self.bstack111llllllll_opy_(bstack111ll1ll1ll_opy_)
      with open(bstack111llll1111_opy_, bstack1ll1l1_opy_ (u"ࠣࡹࠥ᱿")) as f:
        f.write(bstack111lllll111_opy_)
        self.logger.debug(bstack1ll1l1_opy_ (u"ࠤࡖࡥࡻ࡫ࡤࠡࡰࡨࡻࠥࡋࡔࡢࡩࠣࡪࡴࡸࠠࡱࡧࡵࡧࡾࠨᲀ"))
    except Exception as e:
      self.logger.error(bstack1ll1l1_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡢࡸࡨࠤࡹ࡮ࡥࠡࡧࡷࡥ࡬࠲ࠠࡦࡴࡵࡳࡷࡀࠠࡼࡿࠥᲁ").format(e))
  def bstack111lll1lll1_opy_(self, bstack111ll1ll1ll_opy_):
    try:
      bstack111llll1111_opy_ = self.bstack111llllllll_opy_(bstack111ll1ll1ll_opy_)
      if os.path.exists(bstack111llll1111_opy_):
        with open(bstack111llll1111_opy_, bstack1ll1l1_opy_ (u"ࠦࡷࠨᲂ")) as f:
          bstack111lllll111_opy_ = f.read().strip()
          return bstack111lllll111_opy_ if bstack111lllll111_opy_ else None
    except Exception as e:
      self.logger.error(bstack1ll1l1_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡲ࡯ࡢࡦ࡬ࡲ࡬ࠦࡅࡕࡣࡪ࠰ࠥ࡫ࡲࡳࡱࡵ࠾ࠥࢁࡽࠣᲃ").format(e))
  def bstack11l1111l1l1_opy_(self, bstack111ll1ll1ll_opy_, bstack111llll1ll1_opy_):
    bstack111llll1l1l_opy_ = self.bstack111lll1lll1_opy_(bstack111ll1ll1ll_opy_)
    if bstack111llll1l1l_opy_:
      try:
        bstack11l1111111l_opy_ = self.bstack111ll1l1ll1_opy_(bstack111llll1l1l_opy_, bstack111llll1ll1_opy_)
        if not bstack11l1111111l_opy_:
          self.logger.debug(bstack1ll1l1_opy_ (u"ࠨࡐࡦࡴࡦࡽࠥࡨࡩ࡯ࡣࡵࡽࠥ࡯ࡳࠡࡷࡳࠤࡹࡵࠠࡥࡣࡷࡩࠥ࠮ࡅࡕࡣࡪࠤࡺࡴࡣࡩࡣࡱ࡫ࡪࡪࠩࠣᲄ"))
          return True
        self.logger.debug(bstack1ll1l1_opy_ (u"ࠢࡏࡧࡺࠤࡕ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠣࡺࡪࡸࡳࡪࡱࡱࠤࡦࡼࡡࡪ࡮ࡤࡦࡱ࡫ࠬࠡࡦࡲࡻࡳࡲ࡯ࡢࡦ࡬ࡲ࡬ࠦࡵࡱࡦࡤࡸࡪࠨᲅ"))
        return False
      except Exception as e:
        self.logger.warn(bstack1ll1l1_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡨ࡮ࡥࡤ࡭ࠣࡪࡴࡸࠠࡣ࡫ࡱࡥࡷࡿࠠࡶࡲࡧࡥࡹ࡫ࡳ࠭ࠢࡸࡷ࡮ࡴࡧࠡࡧࡻ࡭ࡸࡺࡩ࡯ࡩࠣࡦ࡮ࡴࡡࡳࡻ࠽ࠤࢀࢃࠢᲆ").format(e))
    return False
  def bstack111ll1l1ll1_opy_(self, bstack111llll1l1l_opy_, bstack111llll1ll1_opy_):
    try:
      headers = {
        bstack1ll1l1_opy_ (u"ࠤࡌࡪ࠲ࡔ࡯࡯ࡧ࠰ࡑࡦࡺࡣࡩࠤᲇ"): bstack111llll1l1l_opy_
      }
      response = bstack11l1lll1ll_opy_(bstack1ll1l1_opy_ (u"ࠪࡋࡊ࡚ࠧᲈ"), bstack111llll1ll1_opy_, {}, {bstack1ll1l1_opy_ (u"ࠦ࡭࡫ࡡࡥࡧࡵࡷࠧᲉ"): headers})
      if response.status_code == 304:
        return False
      return True
    except Exception as e:
      raise(bstack1ll1l1_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡨ࡮ࡥࡤ࡭࡬ࡲ࡬ࠦࡦࡰࡴࠣࡔࡪࡸࡣࡺࠢࡥ࡭ࡳࡧࡲࡺࠢࡸࡴࡩࡧࡴࡦࡵ࠽ࠤࢀࢃࠢᲊ").format(e))
  @measure(event_name=EVENTS.bstack11ll1ll1111_opy_, stage=STAGE.bstack1llll1l1_opy_)
  def bstack111ll1ll111_opy_(self, bstack111llll1ll1_opy_, bstack111lll1l1l1_opy_):
    try:
      bstack111lllllll1_opy_ = self.bstack11l11111ll1_opy_()
      bstack111lll111ll_opy_ = os.path.join(bstack111lllllll1_opy_, bstack1ll1l1_opy_ (u"࠭ࡰࡦࡴࡦࡽ࠳ࢀࡩࡱࠩ᲋"))
      bstack111lllll11l_opy_ = os.path.join(bstack111lllllll1_opy_, bstack111lll1l1l1_opy_)
      if self.bstack11l1111l1l1_opy_(bstack111lllllll1_opy_, bstack111llll1ll1_opy_):
        if os.path.exists(bstack111lllll11l_opy_):
          self.logger.info(bstack1ll1l1_opy_ (u"ࠢࡑࡧࡵࡧࡾࠦࡢࡪࡰࡤࡶࡾࠦࡦࡰࡷࡱࡨࠥ࡯࡮ࠡࡽࢀ࠰ࠥࡹ࡫ࡪࡲࡳ࡭ࡳ࡭ࠠࡥࡱࡺࡲࡱࡵࡡࡥࠤ᲌").format(bstack111lllll11l_opy_))
          return bstack111lllll11l_opy_
        if os.path.exists(bstack111lll111ll_opy_):
          self.logger.info(bstack1ll1l1_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡻ࡫ࡳࠤ࡫ࡵࡵ࡯ࡦࠣ࡭ࡳࠦࡻࡾ࠮ࠣࡹࡳࢀࡩࡱࡲ࡬ࡲ࡬ࠨ᲍").format(bstack111lll111ll_opy_))
          return self.bstack11l11111l11_opy_(bstack111lll111ll_opy_, bstack111lll1l1l1_opy_)
      self.logger.info(bstack1ll1l1_opy_ (u"ࠤࡇࡳࡼࡴ࡬ࡰࡣࡧ࡭ࡳ࡭ࠠࡱࡧࡵࡧࡾࠦࡢࡪࡰࡤࡶࡾࠦࡦࡳࡱࡰࠤࢀࢃࠢ᲎").format(bstack111llll1ll1_opy_))
      response = bstack11l1lll1ll_opy_(bstack1ll1l1_opy_ (u"ࠪࡋࡊ࡚ࠧ᲏"), bstack111llll1ll1_opy_, {}, {})
      if response.status_code == 200:
        bstack111lll1ll11_opy_ = response.headers.get(bstack1ll1l1_opy_ (u"ࠦࡊ࡚ࡡࡨࠤᲐ"), bstack1ll1l1_opy_ (u"ࠧࠨᲑ"))
        if bstack111lll1ll11_opy_:
          self.bstack111llll11ll_opy_(bstack111lllllll1_opy_, bstack111lll1ll11_opy_)
        with open(bstack111lll111ll_opy_, bstack1ll1l1_opy_ (u"࠭ࡷࡣࠩᲒ")) as file:
          file.write(response.content)
        self.logger.info(bstack1ll1l1_opy_ (u"ࠢࡅࡱࡺࡲࡱࡵࡡࡥࡧࡧࠤࡵ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠣࡥࡳࡪࠠࡴࡣࡹࡩࡩࠦࡡࡵࠢࡾࢁࠧᲓ").format(bstack111lll111ll_opy_))
        return self.bstack11l11111l11_opy_(bstack111lll111ll_opy_, bstack111lll1l1l1_opy_)
      else:
        raise(bstack1ll1l1_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡩࡵࡷ࡯࡮ࡲࡥࡩࠦࡴࡩࡧࠣࡪ࡮ࡲࡥ࠯ࠢࡖࡸࡦࡺࡵࡴࠢࡦࡳࡩ࡫࠺ࠡࡽࢀࠦᲔ").format(response.status_code))
    except Exception as e:
      self.logger.error(bstack1ll1l1_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠠࡱࡧࡵࡧࡾࠦࡢࡪࡰࡤࡶࡾࡀࠠࡼࡿࠥᲕ").format(e))
  def bstack111ll1lll11_opy_(self, bstack111llll1ll1_opy_, bstack111lll1l1l1_opy_):
    try:
      retry = 2
      bstack111lllll11l_opy_ = None
      bstack11l1111ll1l_opy_ = False
      while retry > 0:
        bstack111lllll11l_opy_ = self.bstack111ll1ll111_opy_(bstack111llll1ll1_opy_, bstack111lll1l1l1_opy_)
        bstack11l1111ll1l_opy_ = self.bstack111llllll11_opy_(bstack111llll1ll1_opy_, bstack111lll1l1l1_opy_, bstack111lllll11l_opy_)
        if bstack11l1111ll1l_opy_:
          break
        retry -= 1
      return bstack111lllll11l_opy_, bstack11l1111ll1l_opy_
    except Exception as e:
      self.logger.error(bstack1ll1l1_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡧࡦࡶࠣࡴࡪࡸࡣࡺࠢࡥ࡭ࡳࡧࡲࡺࠢࡳࡥࡹ࡮ࠢᲖ").format(e))
    return bstack111lllll11l_opy_, False
  def bstack111llllll11_opy_(self, bstack111llll1ll1_opy_, bstack111lll1l1l1_opy_, bstack111lllll11l_opy_, bstack11l11111l1l_opy_ = 0):
    if bstack11l11111l1l_opy_ > 1:
      return False
    if bstack111lllll11l_opy_ == None or os.path.exists(bstack111lllll11l_opy_) == False:
      self.logger.warn(bstack1ll1l1_opy_ (u"ࠦࡕ࡫ࡲࡤࡻࠣࡴࡦࡺࡨࠡࡰࡲࡸࠥ࡬࡯ࡶࡰࡧ࠰ࠥࡸࡥࡵࡴࡼ࡭ࡳ࡭ࠠࡥࡱࡺࡲࡱࡵࡡࡥࠤᲗ"))
      return False
    bstack11l11111lll_opy_ = bstack1ll1l1_opy_ (u"ࠧࡤ࠮ࠫࡂࡳࡩࡷࡩࡹ࡝࠱ࡦࡰ࡮ࠦ࡜ࡥ࠰࡟ࡨ࠰࠴࡜ࡥ࠭ࠥᲘ")
    command = bstack1ll1l1_opy_ (u"࠭ࡻࡾࠢ࠰࠱ࡻ࡫ࡲࡴ࡫ࡲࡲࠬᲙ").format(bstack111lllll11l_opy_)
    bstack111ll1l1l1l_opy_ = subprocess.check_output(command, shell=True, text=True)
    if re.match(bstack11l11111lll_opy_, bstack111ll1l1l1l_opy_) != None:
      return True
    else:
      self.logger.error(bstack1ll1l1_opy_ (u"ࠢࡑࡧࡵࡧࡾࠦࡶࡦࡴࡶ࡭ࡴࡴࠠࡤࡪࡨࡧࡰࠦࡦࡢ࡫࡯ࡩࡩࠨᲚ"))
      return False
  def bstack11l11111l11_opy_(self, bstack111lll111ll_opy_, bstack111lll1l1l1_opy_):
    try:
      working_dir = os.path.dirname(bstack111lll111ll_opy_)
      shutil.unpack_archive(bstack111lll111ll_opy_, working_dir)
      bstack111lllll11l_opy_ = os.path.join(working_dir, bstack111lll1l1l1_opy_)
      os.chmod(bstack111lllll11l_opy_, 0o755)
      return bstack111lllll11l_opy_
    except Exception as e:
      self.logger.error(bstack1ll1l1_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡺࡴࡺࡪࡲࠣࡴࡪࡸࡣࡺࠢࡥ࡭ࡳࡧࡲࡺࠤᲛ"))
  def bstack111lll11ll1_opy_(self):
    try:
      bstack111llll111l_opy_ = self.config.get(bstack1ll1l1_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨᲜ"))
      bstack111lll11ll1_opy_ = bstack111llll111l_opy_ or (bstack111llll111l_opy_ is None and self.bstack11l11111l_opy_)
      if not bstack111lll11ll1_opy_ or self.config.get(bstack1ll1l1_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭Ო"), None) not in bstack11ll1lll1l1_opy_:
        return False
      self.bstack1llll11l11_opy_ = True
      return True
    except Exception as e:
      self.logger.error(bstack1ll1l1_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡥࡧࡷࡩࡨࡺࠠࡱࡧࡵࡧࡾ࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡿࢂࠨᲞ").format(e))
  def bstack11l11111111_opy_(self):
    try:
      bstack11l11111111_opy_ = self.percy_capture_mode
      return bstack11l11111111_opy_
    except Exception as e:
      self.logger.error(bstack1ll1l1_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡦࡨࡸࡪࡩࡴࠡࡲࡨࡶࡨࡿࠠࡤࡣࡳࡸࡺࡸࡥࠡ࡯ࡲࡨࡪ࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡿࢂࠨᲟ").format(e))
  def init(self, bstack11l11111l_opy_, config, logger):
    self.bstack11l11111l_opy_ = bstack11l11111l_opy_
    self.config = config
    self.logger = logger
    if not self.bstack111lll11ll1_opy_():
      return
    self.bstack111lll11lll_opy_ = config.get(bstack1ll1l1_opy_ (u"࠭ࡰࡦࡴࡦࡽࡔࡶࡴࡪࡱࡱࡷࠬᲠ"), {})
    self.percy_capture_mode = config.get(bstack1ll1l1_opy_ (u"ࠧࡱࡧࡵࡧࡾࡉࡡࡱࡶࡸࡶࡪࡓ࡯ࡥࡧࠪᲡ"))
    try:
      bstack111llll1ll1_opy_, bstack111lll1l1l1_opy_ = self.bstack111lll1llll_opy_()
      self.bstack11l1l11l1l1_opy_ = bstack111lll1l1l1_opy_
      bstack111lllll11l_opy_, bstack11l1111ll1l_opy_ = self.bstack111ll1lll11_opy_(bstack111llll1ll1_opy_, bstack111lll1l1l1_opy_)
      if bstack11l1111ll1l_opy_:
        self.binary_path = bstack111lllll11l_opy_
        thread = Thread(target=self.bstack111ll1ll11l_opy_)
        thread.start()
      else:
        self.bstack111ll1l11l1_opy_ = True
        self.logger.error(bstack1ll1l1_opy_ (u"ࠣࡋࡱࡺࡦࡲࡩࡥࠢࡳࡩࡷࡩࡹࠡࡲࡤࡸ࡭ࠦࡦࡰࡷࡱࡨࠥ࠳ࠠࡼࡿ࠯ࠤ࡚ࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡶࡤࡶࡹࠦࡐࡦࡴࡦࡽࠧᲢ").format(bstack111lllll11l_opy_))
    except Exception as e:
      self.logger.error(bstack1ll1l1_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡴࡢࡴࡷࠤࡵ࡫ࡲࡤࡻ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡼࡿࠥᲣ").format(e))
  def bstack111lll1ll1l_opy_(self):
    try:
      logfile = os.path.join(self.working_dir, bstack1ll1l1_opy_ (u"ࠪࡰࡴ࡭ࠧᲤ"), bstack1ll1l1_opy_ (u"ࠫࡵ࡫ࡲࡤࡻ࠱ࡰࡴ࡭ࠧᲥ"))
      os.makedirs(os.path.dirname(logfile)) if not os.path.exists(os.path.dirname(logfile)) else None
      self.logger.debug(bstack1ll1l1_opy_ (u"ࠧࡖࡵࡴࡪ࡬ࡲ࡬ࠦࡰࡦࡴࡦࡽࠥࡲ࡯ࡨࡵࠣࡥࡹࠦࡻࡾࠤᲦ").format(logfile))
      self.bstack111ll1l1l11_opy_ = logfile
    except Exception as e:
      self.logger.error(bstack1ll1l1_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡩࡹࠦࡰࡦࡴࡦࡽࠥࡲ࡯ࡨࠢࡳࡥࡹ࡮ࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࢀࢃࠢᲧ").format(e))
  @measure(event_name=EVENTS.bstack11ll1lll11l_opy_, stage=STAGE.bstack1llll1l1_opy_)
  def bstack111ll1ll11l_opy_(self):
    bstack111llll11l1_opy_ = self.bstack111ll1l11ll_opy_()
    if bstack111llll11l1_opy_ == None:
      self.bstack111ll1l11l1_opy_ = True
      self.logger.error(bstack1ll1l1_opy_ (u"ࠢࡑࡧࡵࡧࡾࠦࡴࡰ࡭ࡨࡲࠥࡴ࡯ࡵࠢࡩࡳࡺࡴࡤ࠭ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡴࡢࡴࡷࠤࡵ࡫ࡲࡤࡻࠥᲨ"))
      return False
    command_args = [bstack1ll1l1_opy_ (u"ࠣࡣࡳࡴ࠿࡫ࡸࡦࡥ࠽ࡷࡹࡧࡲࡵࠤᲩ") if self.bstack11l11111l_opy_ else bstack1ll1l1_opy_ (u"ࠩࡨࡼࡪࡩ࠺ࡴࡶࡤࡶࡹ࠭Ც")]
    bstack11l11l111l1_opy_ = self.bstack11l1111l111_opy_()
    if bstack11l11l111l1_opy_ != None:
      command_args.append(bstack1ll1l1_opy_ (u"ࠥ࠱ࡨࠦࡻࡾࠤᲫ").format(bstack11l11l111l1_opy_))
    env = os.environ.copy()
    env[bstack1ll1l1_opy_ (u"ࠦࡕࡋࡒࡄ࡛ࡢࡘࡔࡑࡅࡏࠤᲬ")] = bstack111llll11l1_opy_
    env[bstack1ll1l1_opy_ (u"࡚ࠧࡈࡠࡄࡘࡍࡑࡊ࡟ࡖࡗࡌࡈࠧᲭ")] = os.environ.get(bstack1ll1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫᲮ"), bstack1ll1l1_opy_ (u"ࠧࠨᲯ"))
    bstack11l1111l1ll_opy_ = [self.binary_path]
    self.bstack111lll1ll1l_opy_()
    self.bstack111lll1l11l_opy_ = self.bstack111ll1lllll_opy_(bstack11l1111l1ll_opy_ + command_args, env)
    self.logger.debug(bstack1ll1l1_opy_ (u"ࠣࡕࡷࡥࡷࡺࡩ࡯ࡩࠣࡌࡪࡧ࡬ࡵࡪࠣࡇ࡭࡫ࡣ࡬ࠤᲰ"))
    bstack11l11111l1l_opy_ = 0
    while self.bstack111lll1l11l_opy_.poll() == None:
      bstack111ll1ll1l1_opy_ = self.bstack111lll111l1_opy_()
      if bstack111ll1ll1l1_opy_:
        self.logger.debug(bstack1ll1l1_opy_ (u"ࠤࡋࡩࡦࡲࡴࡩࠢࡆ࡬ࡪࡩ࡫ࠡࡵࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࠧᲱ"))
        self.bstack111ll1l1lll_opy_ = True
        return True
      bstack11l11111l1l_opy_ += 1
      self.logger.debug(bstack1ll1l1_opy_ (u"ࠥࡌࡪࡧ࡬ࡵࡪࠣࡇ࡭࡫ࡣ࡬ࠢࡕࡩࡹࡸࡹࠡ࠯ࠣࡿࢂࠨᲲ").format(bstack11l11111l1l_opy_))
      time.sleep(2)
    self.logger.error(bstack1ll1l1_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡶࡤࡶࡹࠦࡰࡦࡴࡦࡽ࠱ࠦࡈࡦࡣ࡯ࡸ࡭ࠦࡃࡩࡧࡦ࡯ࠥࡌࡡࡪ࡮ࡨࡨࠥࡧࡦࡵࡧࡵࠤࢀࢃࠠࡢࡶࡷࡩࡲࡶࡴࡴࠤᲳ").format(bstack11l11111l1l_opy_))
    self.bstack111ll1l11l1_opy_ = True
    return False
  def bstack111lll111l1_opy_(self, bstack11l11111l1l_opy_ = 0):
    if bstack11l11111l1l_opy_ > 10:
      return False
    try:
      bstack11l1111ll11_opy_ = os.environ.get(bstack1ll1l1_opy_ (u"ࠬࡖࡅࡓࡅ࡜ࡣࡘࡋࡒࡗࡇࡕࡣࡆࡊࡄࡓࡇࡖࡗࠬᲴ"), bstack1ll1l1_opy_ (u"࠭ࡨࡵࡶࡳ࠾࠴࠵࡬ࡰࡥࡤࡰ࡭ࡵࡳࡵ࠼࠸࠷࠸࠾ࠧᲵ"))
      bstack111ll1lll1l_opy_ = bstack11l1111ll11_opy_ + bstack11lll111111_opy_
      response = requests.get(bstack111ll1lll1l_opy_)
      data = response.json()
      self.percy_build_id = data.get(bstack1ll1l1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩ࠭Ჶ"), {}).get(bstack1ll1l1_opy_ (u"ࠨ࡫ࡧࠫᲷ"), None)
      return True
    except:
      self.logger.debug(bstack1ll1l1_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡱࡦࡧࡺࡸࡲࡦࡦࠣࡻ࡭࡯࡬ࡦࠢࡳࡶࡴࡩࡥࡴࡵ࡬ࡲ࡬ࠦࡨࡦࡣ࡯ࡸ࡭ࠦࡣࡩࡧࡦ࡯ࠥࡸࡥࡴࡲࡲࡲࡸ࡫ࠢᲸ"))
      return False
  def bstack111ll1l11ll_opy_(self):
    bstack11l1111lll1_opy_ = bstack1ll1l1_opy_ (u"ࠪࡥࡵࡶࠧᲹ") if self.bstack11l11111l_opy_ else bstack1ll1l1_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭Ჺ")
    bstack111lllll1ll_opy_ = bstack1ll1l1_opy_ (u"ࠧࡻ࡮ࡥࡧࡩ࡭ࡳ࡫ࡤࠣ᲻") if self.config.get(bstack1ll1l1_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬ᲼")) is None else True
    bstack11ll111l1ll_opy_ = bstack1ll1l1_opy_ (u"ࠢࡢࡲ࡬࠳ࡦࡶࡰࡠࡲࡨࡶࡨࡿ࠯ࡨࡧࡷࡣࡵࡸ࡯࡫ࡧࡦࡸࡤࡺ࡯࡬ࡧࡱࡃࡳࡧ࡭ࡦ࠿ࡾࢁࠫࡺࡹࡱࡧࡀࡿࢂࠬࡰࡦࡴࡦࡽࡂࢁࡽࠣᲽ").format(self.config[bstack1ll1l1_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭Ჾ")], bstack11l1111lll1_opy_, bstack111lllll1ll_opy_)
    if self.percy_capture_mode:
      bstack11ll111l1ll_opy_ += bstack1ll1l1_opy_ (u"ࠤࠩࡴࡪࡸࡣࡺࡡࡦࡥࡵࡺࡵࡳࡧࡢࡱࡴࡪࡥ࠾ࡽࢀࠦᲿ").format(self.percy_capture_mode)
    uri = bstack1l11ll111l_opy_(bstack11ll111l1ll_opy_)
    try:
      response = bstack11l1lll1ll_opy_(bstack1ll1l1_opy_ (u"ࠪࡋࡊ࡚ࠧ᳀"), uri, {}, {bstack1ll1l1_opy_ (u"ࠫࡦࡻࡴࡩࠩ᳁"): (self.config[bstack1ll1l1_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧ᳂")], self.config[bstack1ll1l1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ᳃")])})
      if response.status_code == 200:
        data = response.json()
        self.bstack1llll11l11_opy_ = data.get(bstack1ll1l1_opy_ (u"ࠧࡴࡷࡦࡧࡪࡹࡳࠨ᳄"))
        self.percy_capture_mode = data.get(bstack1ll1l1_opy_ (u"ࠨࡲࡨࡶࡨࡿ࡟ࡤࡣࡳࡸࡺࡸࡥࡠ࡯ࡲࡨࡪ࠭᳅"))
        os.environ[bstack1ll1l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡈࡖࡈ࡟ࠧ᳆")] = str(self.bstack1llll11l11_opy_)
        os.environ[bstack1ll1l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡉࡗࡉ࡙ࡠࡅࡄࡔ࡙࡛ࡒࡆࡡࡐࡓࡉࡋࠧ᳇")] = str(self.percy_capture_mode)
        if bstack111lllll1ll_opy_ == bstack1ll1l1_opy_ (u"ࠦࡺࡴࡤࡦࡨ࡬ࡲࡪࡪࠢ᳈") and str(self.bstack1llll11l11_opy_).lower() == bstack1ll1l1_opy_ (u"ࠧࡺࡲࡶࡧࠥ᳉"):
          self.bstack1111l1ll1_opy_ = True
        if bstack1ll1l1_opy_ (u"ࠨࡴࡰ࡭ࡨࡲࠧ᳊") in data:
          return data[bstack1ll1l1_opy_ (u"ࠢࡵࡱ࡮ࡩࡳࠨ᳋")]
        else:
          raise bstack1ll1l1_opy_ (u"ࠨࡖࡲ࡯ࡪࡴࠠࡏࡱࡷࠤࡋࡵࡵ࡯ࡦࠣ࠱ࠥࢁࡽࠨ᳌").format(data)
      else:
        raise bstack1ll1l1_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥ࡬ࡥࡵࡥ࡫ࠤࡵ࡫ࡲࡤࡻࠣࡸࡴࡱࡥ࡯࠮ࠣࡖࡪࡹࡰࡰࡰࡶࡩࠥࡹࡴࡢࡶࡸࡷࠥ࠳ࠠࡼࡿ࠯ࠤࡗ࡫ࡳࡱࡱࡱࡷࡪࠦࡂࡰࡦࡼࠤ࠲ࠦࡻࡾࠤ᳍").format(response.status_code, response.json())
    except Exception as e:
      self.logger.error(bstack1ll1l1_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡦࡶࡪࡧࡴࡪࡰࡪࠤࡵ࡫ࡲࡤࡻࠣࡴࡷࡵࡪࡦࡥࡷࠦ᳎").format(e))
  def bstack11l1111l111_opy_(self):
    bstack11l1111llll_opy_ = os.path.join(tempfile.gettempdir(), bstack1ll1l1_opy_ (u"ࠦࡵ࡫ࡲࡤࡻࡆࡳࡳ࡬ࡩࡨ࠰࡭ࡷࡴࡴࠢ᳏"))
    try:
      if bstack1ll1l1_opy_ (u"ࠬࡼࡥࡳࡵ࡬ࡳࡳ࠭᳐") not in self.bstack111lll11lll_opy_:
        self.bstack111lll11lll_opy_[bstack1ll1l1_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴࠧ᳑")] = 2
      with open(bstack11l1111llll_opy_, bstack1ll1l1_opy_ (u"ࠧࡸࠩ᳒")) as fp:
        json.dump(self.bstack111lll11lll_opy_, fp)
      return bstack11l1111llll_opy_
    except Exception as e:
      self.logger.error(bstack1ll1l1_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡨࡸࡥࡢࡶࡨࠤࡵ࡫ࡲࡤࡻࠣࡧࡴࡴࡦ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࢁࡽࠣ᳓").format(e))
  def bstack111ll1lllll_opy_(self, cmd, env = os.environ.copy()):
    try:
      if self.bstack111llll1l11_opy_ == bstack1ll1l1_opy_ (u"ࠩࡺ࡭ࡳ᳔࠭"):
        bstack111ll1llll1_opy_ = [bstack1ll1l1_opy_ (u"ࠪࡧࡲࡪ࠮ࡦࡺࡨ᳕ࠫ"), bstack1ll1l1_opy_ (u"ࠫ࠴ࡩ᳖ࠧ")]
        cmd = bstack111ll1llll1_opy_ + cmd
      cmd = bstack1ll1l1_opy_ (u"᳗ࠬࠦࠧ").join(cmd)
      self.logger.debug(bstack1ll1l1_opy_ (u"ࠨࡒࡶࡰࡱ࡭ࡳ࡭ࠠࡼࡿ᳘ࠥ").format(cmd))
      with open(self.bstack111ll1l1l11_opy_, bstack1ll1l1_opy_ (u"ࠢࡢࠤ᳙")) as bstack111llllll1l_opy_:
        process = subprocess.Popen(cmd, shell=True, stdout=bstack111llllll1l_opy_, text=True, stderr=bstack111llllll1l_opy_, env=env, universal_newlines=True)
      return process
    except Exception as e:
      self.bstack111ll1l11l1_opy_ = True
      self.logger.error(bstack1ll1l1_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸࡺࡡࡳࡶࠣࡴࡪࡸࡣࡺࠢࡺ࡭ࡹ࡮ࠠࡤ࡯ࡧࠤ࠲ࠦࡻࡾ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࡀࠠࡼࡿࠥ᳚").format(cmd, e))
  def shutdown(self):
    try:
      if self.bstack111ll1l1lll_opy_:
        self.logger.info(bstack1ll1l1_opy_ (u"ࠤࡖࡸࡴࡶࡰࡪࡰࡪࠤࡕ࡫ࡲࡤࡻࠥ᳛"))
        cmd = [self.binary_path, bstack1ll1l1_opy_ (u"ࠥࡩࡽ࡫ࡣ࠻ࡵࡷࡳࡵࠨ᳜")]
        self.bstack111ll1lllll_opy_(cmd)
        self.bstack111ll1l1lll_opy_ = False
    except Exception as e:
      self.logger.error(bstack1ll1l1_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡶࡲࡴࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡷࡪࡶ࡫ࠤࡨࡵ࡭࡮ࡣࡱࡨࠥ࠳ࠠࡼࡿ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴ࠺ࠡࡽࢀ᳝ࠦ").format(cmd, e))
  def bstack11l1l1l1_opy_(self):
    if not self.bstack1llll11l11_opy_:
      return
    try:
      bstack11l111111l1_opy_ = 0
      while not self.bstack111ll1l1lll_opy_ and bstack11l111111l1_opy_ < self.bstack111lll11l11_opy_:
        if self.bstack111ll1l11l1_opy_:
          self.logger.info(bstack1ll1l1_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡸ࡫ࡴࡶࡲࠣࡪࡦ࡯࡬ࡦࡦ᳞ࠥ"))
          return
        time.sleep(1)
        bstack11l111111l1_opy_ += 1
      os.environ[bstack1ll1l1_opy_ (u"࠭ࡐࡆࡔࡆ࡝ࡤࡈࡅࡔࡖࡢࡔࡑࡇࡔࡇࡑࡕࡑ᳟ࠬ")] = str(self.bstack11l1111l11l_opy_())
      self.logger.info(bstack1ll1l1_opy_ (u"ࠢࡑࡧࡵࡧࡾࠦࡳࡦࡶࡸࡴࠥࡩ࡯࡮ࡲ࡯ࡩࡹ࡫ࡤࠣ᳠"))
    except Exception as e:
      self.logger.error(bstack1ll1l1_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸ࡫ࡴࡶࡲࠣࡴࡪࡸࡣࡺ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡻࡾࠤ᳡").format(e))
  def bstack11l1111l11l_opy_(self):
    if self.bstack11l11111l_opy_:
      return
    try:
      bstack111lll11l1l_opy_ = [platform[bstack1ll1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫᳢ࠧ")].lower() for platform in self.config.get(bstack1ll1l1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ᳣࠭"), [])]
      bstack11l111l111l_opy_ = sys.maxsize
      bstack111lll1111l_opy_ = bstack1ll1l1_opy_ (u"᳤ࠫࠬ")
      for browser in bstack111lll11l1l_opy_:
        if browser in self.bstack11l111111ll_opy_:
          bstack111llll1lll_opy_ = self.bstack11l111111ll_opy_[browser]
        if bstack111llll1lll_opy_ < bstack11l111l111l_opy_:
          bstack11l111l111l_opy_ = bstack111llll1lll_opy_
          bstack111lll1111l_opy_ = browser
      return bstack111lll1111l_opy_
    except Exception as e:
      self.logger.error(bstack1ll1l1_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡨ࡬ࡲࡩࠦࡢࡦࡵࡷࠤࡵࡲࡡࡵࡨࡲࡶࡲ࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡿࢂࠨ᳥").format(e))
  @classmethod
  def bstack1111l1l1_opy_(self):
    return os.getenv(bstack1ll1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡅࡓࡅ࡜᳦ࠫ"), bstack1ll1l1_opy_ (u"ࠧࡇࡣ࡯ࡷࡪ᳧࠭")).lower()
  @classmethod
  def bstack11l11111_opy_(self):
    return os.getenv(bstack1ll1l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡇࡕࡇ࡞ࡥࡃࡂࡒࡗ࡙ࡗࡋ࡟ࡎࡑࡇࡉ᳨ࠬ"), bstack1ll1l1_opy_ (u"ࠩࠪᳩ"))
  @classmethod
  def bstack1l1ll1lll11_opy_(cls, value):
    cls.bstack1111l1ll1_opy_ = value
  @classmethod
  def bstack11l111l1111_opy_(cls):
    return cls.bstack1111l1ll1_opy_
  @classmethod
  def bstack1l1ll1l1l11_opy_(cls, value):
    cls.percy_build_id = value
  @classmethod
  def bstack111lll1l1ll_opy_(cls):
    return cls.percy_build_id
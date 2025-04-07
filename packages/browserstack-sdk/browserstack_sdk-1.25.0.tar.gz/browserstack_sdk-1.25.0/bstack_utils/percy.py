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
from bstack_utils.helper import bstack1ll11l11l_opy_, bstack111ll11ll_opy_
from bstack_utils.measure import measure
class bstack111l11l1l_opy_:
  working_dir = os.getcwd()
  bstack1llll11111_opy_ = False
  config = {}
  bstack11l1llll111_opy_ = bstack11l1l11_opy_ (u"ࠩࠪᯘ")
  binary_path = bstack11l1l11_opy_ (u"ࠪࠫᯙ")
  bstack11l11lllll1_opy_ = bstack11l1l11_opy_ (u"ࠫࠬᯚ")
  bstack1l111llll_opy_ = False
  bstack11l11l1111l_opy_ = None
  bstack11l111lll11_opy_ = {}
  bstack11l11llll1l_opy_ = 300
  bstack11l11l111ll_opy_ = False
  logger = None
  bstack11l1l11l111_opy_ = False
  bstack1lllll11_opy_ = False
  percy_build_id = None
  bstack11l11lll111_opy_ = bstack11l1l11_opy_ (u"ࠬ࠭ᯛ")
  bstack11l111l11l1_opy_ = {
    bstack11l1l11_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ࠭ᯜ") : 1,
    bstack11l1l11_opy_ (u"ࠧࡧ࡫ࡵࡩ࡫ࡵࡸࠨᯝ") : 2,
    bstack11l1l11_opy_ (u"ࠨࡧࡧ࡫ࡪ࠭ᯞ") : 3,
    bstack11l1l11_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪࠩᯟ") : 4
  }
  def __init__(self) -> None: pass
  def bstack11l11l1l111_opy_(self):
    bstack11l11l1l1ll_opy_ = bstack11l1l11_opy_ (u"ࠪࠫᯠ")
    bstack11l1l1111l1_opy_ = sys.platform
    bstack11l111l111l_opy_ = bstack11l1l11_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪᯡ")
    if re.match(bstack11l1l11_opy_ (u"ࠧࡪࡡࡳࡹ࡬ࡲࢁࡳࡡࡤࠢࡲࡷࠧᯢ"), bstack11l1l1111l1_opy_) != None:
      bstack11l11l1l1ll_opy_ = bstack1l111111111_opy_ + bstack11l1l11_opy_ (u"ࠨ࠯ࡱࡧࡵࡧࡾ࠳࡯ࡴࡺ࠱ࡾ࡮ࡶࠢᯣ")
      self.bstack11l11lll111_opy_ = bstack11l1l11_opy_ (u"ࠧ࡮ࡣࡦࠫᯤ")
    elif re.match(bstack11l1l11_opy_ (u"ࠣ࡯ࡶࡻ࡮ࡴࡼ࡮ࡵࡼࡷࢁࡳࡩ࡯ࡩࡺࢀࡨࡿࡧࡸ࡫ࡱࢀࡧࡩࡣࡸ࡫ࡱࢀࡼ࡯࡮ࡤࡧࡿࡩࡲࡩࡼࡸ࡫ࡱ࠷࠷ࠨᯥ"), bstack11l1l1111l1_opy_) != None:
      bstack11l11l1l1ll_opy_ = bstack1l111111111_opy_ + bstack11l1l11_opy_ (u"ࠤ࠲ࡴࡪࡸࡣࡺ࠯ࡺ࡭ࡳ࠴ࡺࡪࡲ᯦ࠥ")
      bstack11l111l111l_opy_ = bstack11l1l11_opy_ (u"ࠥࡴࡪࡸࡣࡺ࠰ࡨࡼࡪࠨᯧ")
      self.bstack11l11lll111_opy_ = bstack11l1l11_opy_ (u"ࠫࡼ࡯࡮ࠨᯨ")
    else:
      bstack11l11l1l1ll_opy_ = bstack1l111111111_opy_ + bstack11l1l11_opy_ (u"ࠧ࠵ࡰࡦࡴࡦࡽ࠲ࡲࡩ࡯ࡷࡻ࠲ࡿ࡯ࡰࠣᯩ")
      self.bstack11l11lll111_opy_ = bstack11l1l11_opy_ (u"࠭࡬ࡪࡰࡸࡼࠬᯪ")
    return bstack11l11l1l1ll_opy_, bstack11l111l111l_opy_
  def bstack11l11l1llll_opy_(self):
    try:
      bstack11l11llllll_opy_ = [os.path.join(expanduser(bstack11l1l11_opy_ (u"ࠢࡿࠤᯫ")), bstack11l1l11_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨᯬ")), self.working_dir, tempfile.gettempdir()]
      for path in bstack11l11llllll_opy_:
        if(self.bstack11l11l1lll1_opy_(path)):
          return path
      raise bstack11l1l11_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠠࡱࡧࡵࡧࡾࠦࡢࡪࡰࡤࡶࡾࠨᯭ")
    except Exception as e:
      self.logger.error(bstack11l1l11_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡦࡪࡰࡧࠤࡦࡼࡡࡪ࡮ࡤࡦࡱ࡫ࠠࡱࡣࡷ࡬ࠥ࡬࡯ࡳࠢࡳࡩࡷࡩࡹࠡࡦࡲࡻࡳࡲ࡯ࡢࡦ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠ࠮ࠢࡾࢁࠧᯮ").format(e))
  def bstack11l11l1lll1_opy_(self, path):
    try:
      if not os.path.exists(path):
        os.makedirs(path)
      return True
    except:
      return False
  def bstack11l111ll1ll_opy_(self, bstack11l11ll1ll1_opy_):
    return os.path.join(bstack11l11ll1ll1_opy_, self.bstack11l1llll111_opy_ + bstack11l1l11_opy_ (u"ࠦ࠳࡫ࡴࡢࡩࠥᯯ"))
  def bstack11l11l11111_opy_(self, bstack11l11ll1ll1_opy_, bstack11l11lll1l1_opy_):
    if not bstack11l11lll1l1_opy_: return
    try:
      bstack11l111l1l1l_opy_ = self.bstack11l111ll1ll_opy_(bstack11l11ll1ll1_opy_)
      with open(bstack11l111l1l1l_opy_, bstack11l1l11_opy_ (u"ࠧࡽࠢᯰ")) as f:
        f.write(bstack11l11lll1l1_opy_)
        self.logger.debug(bstack11l1l11_opy_ (u"ࠨࡓࡢࡸࡨࡨࠥࡴࡥࡸࠢࡈࡘࡦ࡭ࠠࡧࡱࡵࠤࡵ࡫ࡲࡤࡻࠥᯱ"))
    except Exception as e:
      self.logger.error(bstack11l1l11_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡦࡼࡥࠡࡶ࡫ࡩࠥ࡫ࡴࡢࡩ࠯ࠤࡪࡸࡲࡰࡴ࠽ࠤࢀࢃ᯲ࠢ").format(e))
  def bstack11l1l11l1l1_opy_(self, bstack11l11ll1ll1_opy_):
    try:
      bstack11l111l1l1l_opy_ = self.bstack11l111ll1ll_opy_(bstack11l11ll1ll1_opy_)
      if os.path.exists(bstack11l111l1l1l_opy_):
        with open(bstack11l111l1l1l_opy_, bstack11l1l11_opy_ (u"ࠣࡴ᯳ࠥ")) as f:
          bstack11l11lll1l1_opy_ = f.read().strip()
          return bstack11l11lll1l1_opy_ if bstack11l11lll1l1_opy_ else None
    except Exception as e:
      self.logger.error(bstack11l1l11_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢ࡯ࡳࡦࡪࡩ࡯ࡩࠣࡉ࡙ࡧࡧ࠭ࠢࡨࡶࡷࡵࡲ࠻ࠢࡾࢁࠧ᯴").format(e))
  def bstack11l1111l1ll_opy_(self, bstack11l11ll1ll1_opy_, bstack11l11l1l1ll_opy_):
    bstack11l1l111ll1_opy_ = self.bstack11l1l11l1l1_opy_(bstack11l11ll1ll1_opy_)
    if bstack11l1l111ll1_opy_:
      try:
        bstack11l111ll11l_opy_ = self.bstack11l11ll111l_opy_(bstack11l1l111ll1_opy_, bstack11l11l1l1ll_opy_)
        if not bstack11l111ll11l_opy_:
          self.logger.debug(bstack11l1l11_opy_ (u"ࠥࡔࡪࡸࡣࡺࠢࡥ࡭ࡳࡧࡲࡺࠢ࡬ࡷࠥࡻࡰࠡࡶࡲࠤࡩࡧࡴࡦࠢࠫࡉ࡙ࡧࡧࠡࡷࡱࡧ࡭ࡧ࡮ࡨࡧࡧ࠭ࠧ᯵"))
          return True
        self.logger.debug(bstack11l1l11_opy_ (u"ࠦࡓ࡫ࡷࠡࡒࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠠࡷࡧࡵࡷ࡮ࡵ࡮ࠡࡣࡹࡥ࡮ࡲࡡࡣ࡮ࡨ࠰ࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࡩ࡯ࡩࠣࡹࡵࡪࡡࡵࡧࠥ᯶"))
        return False
      except Exception as e:
        self.logger.warn(bstack11l1l11_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡥ࡫ࡩࡨࡱࠠࡧࡱࡵࠤࡧ࡯࡮ࡢࡴࡼࠤࡺࡶࡤࡢࡶࡨࡷ࠱ࠦࡵࡴ࡫ࡱ࡫ࠥ࡫ࡸࡪࡵࡷ࡭ࡳ࡭ࠠࡣ࡫ࡱࡥࡷࡿ࠺ࠡࡽࢀࠦ᯷").format(e))
    return False
  def bstack11l11ll111l_opy_(self, bstack11l1l111ll1_opy_, bstack11l11l1l1ll_opy_):
    try:
      headers = {
        bstack11l1l11_opy_ (u"ࠨࡉࡧ࠯ࡑࡳࡳ࡫࠭ࡎࡣࡷࡧ࡭ࠨ᯸"): bstack11l1l111ll1_opy_
      }
      response = bstack111ll11ll_opy_(bstack11l1l11_opy_ (u"ࠧࡈࡇࡗࠫ᯹"), bstack11l11l1l1ll_opy_, {}, {bstack11l1l11_opy_ (u"ࠣࡪࡨࡥࡩ࡫ࡲࡴࠤ᯺"): headers})
      if response.status_code == 304:
        return False
      return True
    except Exception as e:
      raise(bstack11l1l11_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡥ࡫ࡩࡨࡱࡩ࡯ࡩࠣࡪࡴࡸࠠࡑࡧࡵࡧࡾࠦࡢࡪࡰࡤࡶࡾࠦࡵࡱࡦࡤࡸࡪࡹ࠺ࠡࡽࢀࠦ᯻").format(e))
  @measure(event_name=EVENTS.bstack11lllll11ll_opy_, stage=STAGE.bstack1l1ll1lll_opy_)
  def bstack11l1l1111ll_opy_(self, bstack11l11l1l1ll_opy_, bstack11l111l111l_opy_):
    try:
      bstack11l11lll1ll_opy_ = self.bstack11l11l1llll_opy_()
      bstack11l11ll11l1_opy_ = os.path.join(bstack11l11lll1ll_opy_, bstack11l1l11_opy_ (u"ࠪࡴࡪࡸࡣࡺ࠰ࡽ࡭ࡵ࠭᯼"))
      bstack11l111lllll_opy_ = os.path.join(bstack11l11lll1ll_opy_, bstack11l111l111l_opy_)
      if self.bstack11l1111l1ll_opy_(bstack11l11lll1ll_opy_, bstack11l11l1l1ll_opy_):
        if os.path.exists(bstack11l111lllll_opy_):
          self.logger.info(bstack11l1l11_opy_ (u"ࠦࡕ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠣࡪࡴࡻ࡮ࡥࠢ࡬ࡲࠥࢁࡽ࠭ࠢࡶ࡯࡮ࡶࡰࡪࡰࡪࠤࡩࡵࡷ࡯࡮ࡲࡥࡩࠨ᯽").format(bstack11l111lllll_opy_))
          return bstack11l111lllll_opy_
        if os.path.exists(bstack11l11ll11l1_opy_):
          self.logger.info(bstack11l1l11_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡿ࡯ࡰࠡࡨࡲࡹࡳࡪࠠࡪࡰࠣࡿࢂ࠲ࠠࡶࡰࡽ࡭ࡵࡶࡩ࡯ࡩࠥ᯾").format(bstack11l11ll11l1_opy_))
          return self.bstack11l11l11l11_opy_(bstack11l11ll11l1_opy_, bstack11l111l111l_opy_)
      self.logger.info(bstack11l1l11_opy_ (u"ࠨࡄࡰࡹࡱࡰࡴࡧࡤࡪࡰࡪࠤࡵ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠣࡪࡷࡵ࡭ࠡࡽࢀࠦ᯿").format(bstack11l11l1l1ll_opy_))
      response = bstack111ll11ll_opy_(bstack11l1l11_opy_ (u"ࠧࡈࡇࡗࠫᰀ"), bstack11l11l1l1ll_opy_, {}, {})
      if response.status_code == 200:
        bstack11l1111ll11_opy_ = response.headers.get(bstack11l1l11_opy_ (u"ࠣࡇࡗࡥ࡬ࠨᰁ"), bstack11l1l11_opy_ (u"ࠤࠥᰂ"))
        if bstack11l1111ll11_opy_:
          self.bstack11l11l11111_opy_(bstack11l11lll1ll_opy_, bstack11l1111ll11_opy_)
        with open(bstack11l11ll11l1_opy_, bstack11l1l11_opy_ (u"ࠪࡻࡧ࠭ᰃ")) as file:
          file.write(response.content)
        self.logger.info(bstack11l1l11_opy_ (u"ࠦࡉࡵࡷ࡯࡮ࡲࡥࡩ࡫ࡤࠡࡲࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠠࡢࡰࡧࠤࡸࡧࡶࡦࡦࠣࡥࡹࠦࡻࡾࠤᰄ").format(bstack11l11ll11l1_opy_))
        return self.bstack11l11l11l11_opy_(bstack11l11ll11l1_opy_, bstack11l111l111l_opy_)
      else:
        raise(bstack11l1l11_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡦࡲࡻࡳࡲ࡯ࡢࡦࠣࡸ࡭࡫ࠠࡧ࡫࡯ࡩ࠳ࠦࡓࡵࡣࡷࡹࡸࠦࡣࡰࡦࡨ࠾ࠥࢁࡽࠣᰅ").format(response.status_code))
    except Exception as e:
      self.logger.error(bstack11l1l11_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡧࡳࡼࡴ࡬ࡰࡣࡧࠤࡵ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻ࠽ࠤࢀࢃࠢᰆ").format(e))
  def bstack11l11l1ll1l_opy_(self, bstack11l11l1l1ll_opy_, bstack11l111l111l_opy_):
    try:
      retry = 2
      bstack11l111lllll_opy_ = None
      bstack11l1l111111_opy_ = False
      while retry > 0:
        bstack11l111lllll_opy_ = self.bstack11l1l1111ll_opy_(bstack11l11l1l1ll_opy_, bstack11l111l111l_opy_)
        bstack11l1l111111_opy_ = self.bstack11l11l11l1l_opy_(bstack11l11l1l1ll_opy_, bstack11l111l111l_opy_, bstack11l111lllll_opy_)
        if bstack11l1l111111_opy_:
          break
        retry -= 1
      return bstack11l111lllll_opy_, bstack11l1l111111_opy_
    except Exception as e:
      self.logger.error(bstack11l1l11_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣ࡫ࡪࡺࠠࡱࡧࡵࡧࡾࠦࡢࡪࡰࡤࡶࡾࠦࡰࡢࡶ࡫ࠦᰇ").format(e))
    return bstack11l111lllll_opy_, False
  def bstack11l11l11l1l_opy_(self, bstack11l11l1l1ll_opy_, bstack11l111l111l_opy_, bstack11l111lllll_opy_, bstack11l1l111lll_opy_ = 0):
    if bstack11l1l111lll_opy_ > 1:
      return False
    if bstack11l111lllll_opy_ == None or os.path.exists(bstack11l111lllll_opy_) == False:
      self.logger.warn(bstack11l1l11_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡱࡣࡷ࡬ࠥࡴ࡯ࡵࠢࡩࡳࡺࡴࡤ࠭ࠢࡵࡩࡹࡸࡹࡪࡰࡪࠤࡩࡵࡷ࡯࡮ࡲࡥࡩࠨᰈ"))
      return False
    bstack11l11l1l1l1_opy_ = bstack11l1l11_opy_ (u"ࠤࡡ࠲࠯ࡆࡰࡦࡴࡦࡽࡡ࠵ࡣ࡭࡫ࠣࡠࡩ࠴࡜ࡥ࠭࠱ࡠࡩ࠱ࠢᰉ")
    command = bstack11l1l11_opy_ (u"ࠪࡿࢂࠦ࠭࠮ࡸࡨࡶࡸ࡯࡯࡯ࠩᰊ").format(bstack11l111lllll_opy_)
    bstack11l11ll1lll_opy_ = subprocess.check_output(command, shell=True, text=True)
    if re.match(bstack11l11l1l1l1_opy_, bstack11l11ll1lll_opy_) != None:
      return True
    else:
      self.logger.error(bstack11l1l11_opy_ (u"ࠦࡕ࡫ࡲࡤࡻࠣࡺࡪࡸࡳࡪࡱࡱࠤࡨ࡮ࡥࡤ࡭ࠣࡪࡦ࡯࡬ࡦࡦࠥᰋ"))
      return False
  def bstack11l11l11l11_opy_(self, bstack11l11ll11l1_opy_, bstack11l111l111l_opy_):
    try:
      working_dir = os.path.dirname(bstack11l11ll11l1_opy_)
      shutil.unpack_archive(bstack11l11ll11l1_opy_, working_dir)
      bstack11l111lllll_opy_ = os.path.join(working_dir, bstack11l111l111l_opy_)
      os.chmod(bstack11l111lllll_opy_, 0o755)
      return bstack11l111lllll_opy_
    except Exception as e:
      self.logger.error(bstack11l1l11_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡷࡱࡾ࡮ࡶࠠࡱࡧࡵࡧࡾࠦࡢࡪࡰࡤࡶࡾࠨᰌ"))
  def bstack11l11lll11l_opy_(self):
    try:
      bstack11l11ll1l1l_opy_ = self.config.get(bstack11l1l11_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬᰍ"))
      bstack11l11lll11l_opy_ = bstack11l11ll1l1l_opy_ or (bstack11l11ll1l1l_opy_ is None and self.bstack1llll11111_opy_)
      if not bstack11l11lll11l_opy_ or self.config.get(bstack11l1l11_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪᰎ"), None) not in bstack11lllll1ll1_opy_:
        return False
      self.bstack1l111llll_opy_ = True
      return True
    except Exception as e:
      self.logger.error(bstack11l1l11_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡩ࡫ࡴࡦࡥࡷࠤࡵ࡫ࡲࡤࡻ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡼࡿࠥᰏ").format(e))
  def bstack11l11llll11_opy_(self):
    try:
      bstack11l11llll11_opy_ = self.percy_capture_mode
      return bstack11l11llll11_opy_
    except Exception as e:
      self.logger.error(bstack11l1l11_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡪࡥࡵࡧࡦࡸࠥࡶࡥࡳࡥࡼࠤࡨࡧࡰࡵࡷࡵࡩࠥࡳ࡯ࡥࡧ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡼࡿࠥᰐ").format(e))
  def init(self, bstack1llll11111_opy_, config, logger):
    self.bstack1llll11111_opy_ = bstack1llll11111_opy_
    self.config = config
    self.logger = logger
    if not self.bstack11l11lll11l_opy_():
      return
    self.bstack11l111lll11_opy_ = config.get(bstack11l1l11_opy_ (u"ࠪࡴࡪࡸࡣࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩᰑ"), {})
    self.percy_capture_mode = config.get(bstack11l1l11_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡆࡥࡵࡺࡵࡳࡧࡐࡳࡩ࡫ࠧᰒ"))
    try:
      bstack11l11l1l1ll_opy_, bstack11l111l111l_opy_ = self.bstack11l11l1l111_opy_()
      self.bstack11l1llll111_opy_ = bstack11l111l111l_opy_
      bstack11l111lllll_opy_, bstack11l1l111111_opy_ = self.bstack11l11l1ll1l_opy_(bstack11l11l1l1ll_opy_, bstack11l111l111l_opy_)
      if bstack11l1l111111_opy_:
        self.binary_path = bstack11l111lllll_opy_
        thread = Thread(target=self.bstack11l1111ll1l_opy_)
        thread.start()
      else:
        self.bstack11l1l11l111_opy_ = True
        self.logger.error(bstack11l1l11_opy_ (u"ࠧࡏ࡮ࡷࡣ࡯࡭ࡩࠦࡰࡦࡴࡦࡽࠥࡶࡡࡵࡪࠣࡪࡴࡻ࡮ࡥࠢ࠰ࠤࢀࢃࠬࠡࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡺࡡࡳࡶࠣࡔࡪࡸࡣࡺࠤᰓ").format(bstack11l111lllll_opy_))
    except Exception as e:
      self.logger.error(bstack11l1l11_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡸࡦࡸࡴࠡࡲࡨࡶࡨࡿࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࢀࢃࠢᰔ").format(e))
  def bstack11l11l1ll11_opy_(self):
    try:
      logfile = os.path.join(self.working_dir, bstack11l1l11_opy_ (u"ࠧ࡭ࡱࡪࠫᰕ"), bstack11l1l11_opy_ (u"ࠨࡲࡨࡶࡨࡿ࠮࡭ࡱࡪࠫᰖ"))
      os.makedirs(os.path.dirname(logfile)) if not os.path.exists(os.path.dirname(logfile)) else None
      self.logger.debug(bstack11l1l11_opy_ (u"ࠤࡓࡹࡸ࡮ࡩ࡯ࡩࠣࡴࡪࡸࡣࡺࠢ࡯ࡳ࡬ࡹࠠࡢࡶࠣࡿࢂࠨᰗ").format(logfile))
      self.bstack11l11lllll1_opy_ = logfile
    except Exception as e:
      self.logger.error(bstack11l1l11_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡦࡶࠣࡴࡪࡸࡣࡺࠢ࡯ࡳ࡬ࠦࡰࡢࡶ࡫࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡽࢀࠦᰘ").format(e))
  @measure(event_name=EVENTS.bstack11llll11l1l_opy_, stage=STAGE.bstack1l1ll1lll_opy_)
  def bstack11l1111ll1l_opy_(self):
    bstack11l111ll1l1_opy_ = self.bstack11l1l111l11_opy_()
    if bstack11l111ll1l1_opy_ == None:
      self.bstack11l1l11l111_opy_ = True
      self.logger.error(bstack11l1l11_opy_ (u"ࠦࡕ࡫ࡲࡤࡻࠣࡸࡴࡱࡥ࡯ࠢࡱࡳࡹࠦࡦࡰࡷࡱࡨ࠱ࠦࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡸࡦࡸࡴࠡࡲࡨࡶࡨࡿࠢᰙ"))
      return False
    command_args = [bstack11l1l11_opy_ (u"ࠧࡧࡰࡱ࠼ࡨࡼࡪࡩ࠺ࡴࡶࡤࡶࡹࠨᰚ") if self.bstack1llll11111_opy_ else bstack11l1l11_opy_ (u"࠭ࡥࡹࡧࡦ࠾ࡸࡺࡡࡳࡶࠪᰛ")]
    bstack11l1ll11ll1_opy_ = self.bstack11l11l11lll_opy_()
    if bstack11l1ll11ll1_opy_ != None:
      command_args.append(bstack11l1l11_opy_ (u"ࠢ࠮ࡥࠣࡿࢂࠨᰜ").format(bstack11l1ll11ll1_opy_))
    env = os.environ.copy()
    env[bstack11l1l11_opy_ (u"ࠣࡒࡈࡖࡈ࡟࡟ࡕࡑࡎࡉࡓࠨᰝ")] = bstack11l111ll1l1_opy_
    env[bstack11l1l11_opy_ (u"ࠤࡗࡌࡤࡈࡕࡊࡎࡇࡣ࡚࡛ࡉࡅࠤᰞ")] = os.environ.get(bstack11l1l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨᰟ"), bstack11l1l11_opy_ (u"ࠫࠬᰠ"))
    bstack11l111llll1_opy_ = [self.binary_path]
    self.bstack11l11l1ll11_opy_()
    self.bstack11l11l1111l_opy_ = self.bstack11l111lll1l_opy_(bstack11l111llll1_opy_ + command_args, env)
    self.logger.debug(bstack11l1l11_opy_ (u"࡙ࠧࡴࡢࡴࡷ࡭ࡳ࡭ࠠࡉࡧࡤࡰࡹ࡮ࠠࡄࡪࡨࡧࡰࠨᰡ"))
    bstack11l1l111lll_opy_ = 0
    while self.bstack11l11l1111l_opy_.poll() == None:
      bstack11l11l111l1_opy_ = self.bstack11l11l1l11l_opy_()
      if bstack11l11l111l1_opy_:
        self.logger.debug(bstack11l1l11_opy_ (u"ࠨࡈࡦࡣ࡯ࡸ࡭ࠦࡃࡩࡧࡦ࡯ࠥࡹࡵࡤࡥࡨࡷࡸ࡬ࡵ࡭ࠤᰢ"))
        self.bstack11l11l111ll_opy_ = True
        return True
      bstack11l1l111lll_opy_ += 1
      self.logger.debug(bstack11l1l11_opy_ (u"ࠢࡉࡧࡤࡰࡹ࡮ࠠࡄࡪࡨࡧࡰࠦࡒࡦࡶࡵࡽࠥ࠳ࠠࡼࡿࠥᰣ").format(bstack11l1l111lll_opy_))
      time.sleep(2)
    self.logger.error(bstack11l1l11_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸࡺࡡࡳࡶࠣࡴࡪࡸࡣࡺ࠮ࠣࡌࡪࡧ࡬ࡵࡪࠣࡇ࡭࡫ࡣ࡬ࠢࡉࡥ࡮ࡲࡥࡥࠢࡤࡪࡹ࡫ࡲࠡࡽࢀࠤࡦࡺࡴࡦ࡯ࡳࡸࡸࠨᰤ").format(bstack11l1l111lll_opy_))
    self.bstack11l1l11l111_opy_ = True
    return False
  def bstack11l11l1l11l_opy_(self, bstack11l1l111lll_opy_ = 0):
    if bstack11l1l111lll_opy_ > 10:
      return False
    try:
      bstack11l111l1lll_opy_ = os.environ.get(bstack11l1l11_opy_ (u"ࠩࡓࡉࡗࡉ࡙ࡠࡕࡈࡖ࡛ࡋࡒࡠࡃࡇࡈࡗࡋࡓࡔࠩᰥ"), bstack11l1l11_opy_ (u"ࠪ࡬ࡹࡺࡰ࠻࠱࠲ࡰࡴࡩࡡ࡭ࡪࡲࡷࡹࡀ࠵࠴࠵࠻ࠫᰦ"))
      bstack11l1l11l11l_opy_ = bstack11l111l1lll_opy_ + bstack11llll1111l_opy_
      response = requests.get(bstack11l1l11l11l_opy_)
      data = response.json()
      self.percy_build_id = data.get(bstack11l1l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࠪᰧ"), {}).get(bstack11l1l11_opy_ (u"ࠬ࡯ࡤࠨᰨ"), None)
      return True
    except:
      self.logger.debug(bstack11l1l11_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡵࡣࡤࡷࡵࡶࡪࡪࠠࡸࡪ࡬ࡰࡪࠦࡰࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣ࡬ࡪࡧ࡬ࡵࡪࠣࡧ࡭࡫ࡣ࡬ࠢࡵࡩࡸࡶ࡯࡯ࡵࡨࠦᰩ"))
      return False
  def bstack11l1l111l11_opy_(self):
    bstack11l111l1ll1_opy_ = bstack11l1l11_opy_ (u"ࠧࡢࡲࡳࠫᰪ") if self.bstack1llll11111_opy_ else bstack11l1l11_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵࡧࠪᰫ")
    bstack11l1l11111l_opy_ = bstack11l1l11_opy_ (u"ࠤࡸࡲࡩ࡫ࡦࡪࡰࡨࡨࠧᰬ") if self.config.get(bstack11l1l11_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩᰭ")) is None else True
    bstack11ll11l111l_opy_ = bstack11l1l11_opy_ (u"ࠦࡦࡶࡩ࠰ࡣࡳࡴࡤࡶࡥࡳࡥࡼ࠳࡬࡫ࡴࡠࡲࡵࡳ࡯࡫ࡣࡵࡡࡷࡳࡰ࡫࡮ࡀࡰࡤࡱࡪࡃࡻࡾࠨࡷࡽࡵ࡫࠽ࡼࡿࠩࡴࡪࡸࡣࡺ࠿ࡾࢁࠧᰮ").format(self.config[bstack11l1l11_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪᰯ")], bstack11l111l1ll1_opy_, bstack11l1l11111l_opy_)
    if self.percy_capture_mode:
      bstack11ll11l111l_opy_ += bstack11l1l11_opy_ (u"ࠨࠦࡱࡧࡵࡧࡾࡥࡣࡢࡲࡷࡹࡷ࡫࡟࡮ࡱࡧࡩࡂࢁࡽࠣᰰ").format(self.percy_capture_mode)
    uri = bstack1ll11l11l_opy_(bstack11ll11l111l_opy_)
    try:
      response = bstack111ll11ll_opy_(bstack11l1l11_opy_ (u"ࠧࡈࡇࡗࠫᰱ"), uri, {}, {bstack11l1l11_opy_ (u"ࠨࡣࡸࡸ࡭࠭ᰲ"): (self.config[bstack11l1l11_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫᰳ")], self.config[bstack11l1l11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ᰴ")])})
      if response.status_code == 200:
        data = response.json()
        self.bstack1l111llll_opy_ = data.get(bstack11l1l11_opy_ (u"ࠫࡸࡻࡣࡤࡧࡶࡷࠬᰵ"))
        self.percy_capture_mode = data.get(bstack11l1l11_opy_ (u"ࠬࡶࡥࡳࡥࡼࡣࡨࡧࡰࡵࡷࡵࡩࡤࡳ࡯ࡥࡧࠪᰶ"))
        os.environ[bstack11l1l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡅࡓࡅ࡜᰷ࠫ")] = str(self.bstack1l111llll_opy_)
        os.environ[bstack11l1l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡆࡔࡆ࡝ࡤࡉࡁࡑࡖࡘࡖࡊࡥࡍࡐࡆࡈࠫ᰸")] = str(self.percy_capture_mode)
        if bstack11l1l11111l_opy_ == bstack11l1l11_opy_ (u"ࠣࡷࡱࡨࡪ࡬ࡩ࡯ࡧࡧࠦ᰹") and str(self.bstack1l111llll_opy_).lower() == bstack11l1l11_opy_ (u"ࠤࡷࡶࡺ࡫ࠢ᰺"):
          self.bstack1lllll11_opy_ = True
        if bstack11l1l11_opy_ (u"ࠥࡸࡴࡱࡥ࡯ࠤ᰻") in data:
          return data[bstack11l1l11_opy_ (u"ࠦࡹࡵ࡫ࡦࡰࠥ᰼")]
        else:
          raise bstack11l1l11_opy_ (u"࡚ࠬ࡯࡬ࡧࡱࠤࡓࡵࡴࠡࡈࡲࡹࡳࡪࠠ࠮ࠢࡾࢁࠬ᰽").format(data)
      else:
        raise bstack11l1l11_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡩࡩࡹࡩࡨࠡࡲࡨࡶࡨࡿࠠࡵࡱ࡮ࡩࡳ࠲ࠠࡓࡧࡶࡴࡴࡴࡳࡦࠢࡶࡸࡦࡺࡵࡴࠢ࠰ࠤࢀࢃࠬࠡࡔࡨࡷࡵࡵ࡮ࡴࡧࠣࡆࡴࡪࡹࠡ࠯ࠣࡿࢂࠨ᰾").format(response.status_code, response.json())
    except Exception as e:
      self.logger.error(bstack11l1l11_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡣࡳࡧࡤࡸ࡮ࡴࡧࠡࡲࡨࡶࡨࡿࠠࡱࡴࡲ࡮ࡪࡩࡴࠣ᰿").format(e))
  def bstack11l11l11lll_opy_(self):
    bstack11l1111llll_opy_ = os.path.join(tempfile.gettempdir(), bstack11l1l11_opy_ (u"ࠣࡲࡨࡶࡨࡿࡃࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠦ᱀"))
    try:
      if bstack11l1l11_opy_ (u"ࠩࡹࡩࡷࡹࡩࡰࡰࠪ᱁") not in self.bstack11l111lll11_opy_:
        self.bstack11l111lll11_opy_[bstack11l1l11_opy_ (u"ࠪࡺࡪࡸࡳࡪࡱࡱࠫ᱂")] = 2
      with open(bstack11l1111llll_opy_, bstack11l1l11_opy_ (u"ࠫࡼ࠭᱃")) as fp:
        json.dump(self.bstack11l111lll11_opy_, fp)
      return bstack11l1111llll_opy_
    except Exception as e:
      self.logger.error(bstack11l1l11_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡥࡵࡩࡦࡺࡥࠡࡲࡨࡶࡨࡿࠠࡤࡱࡱࡪ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡾࢁࠧ᱄").format(e))
  def bstack11l111lll1l_opy_(self, cmd, env = os.environ.copy()):
    try:
      if self.bstack11l11lll111_opy_ == bstack11l1l11_opy_ (u"࠭ࡷࡪࡰࠪ᱅"):
        bstack11l11ll11ll_opy_ = [bstack11l1l11_opy_ (u"ࠧࡤ࡯ࡧ࠲ࡪࡾࡥࠨ᱆"), bstack11l1l11_opy_ (u"ࠨ࠱ࡦࠫ᱇")]
        cmd = bstack11l11ll11ll_opy_ + cmd
      cmd = bstack11l1l11_opy_ (u"ࠩࠣࠫ᱈").join(cmd)
      self.logger.debug(bstack11l1l11_opy_ (u"ࠥࡖࡺࡴ࡮ࡪࡰࡪࠤࢀࢃࠢ᱉").format(cmd))
      with open(self.bstack11l11lllll1_opy_, bstack11l1l11_opy_ (u"ࠦࡦࠨ᱊")) as bstack11l111l1l11_opy_:
        process = subprocess.Popen(cmd, shell=True, stdout=bstack11l111l1l11_opy_, text=True, stderr=bstack11l111l1l11_opy_, env=env, universal_newlines=True)
      return process
    except Exception as e:
      self.bstack11l1l11l111_opy_ = True
      self.logger.error(bstack11l1l11_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡷࡥࡷࡺࠠࡱࡧࡵࡧࡾࠦࡷࡪࡶ࡫ࠤࡨࡳࡤࠡ࠯ࠣࡿࢂ࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰ࠽ࠤࢀࢃࠢ᱋").format(cmd, e))
  def shutdown(self):
    try:
      if self.bstack11l11l111ll_opy_:
        self.logger.info(bstack11l1l11_opy_ (u"ࠨࡓࡵࡱࡳࡴ࡮ࡴࡧࠡࡒࡨࡶࡨࡿࠢ᱌"))
        cmd = [self.binary_path, bstack11l1l11_opy_ (u"ࠢࡦࡺࡨࡧ࠿ࡹࡴࡰࡲࠥᱍ")]
        self.bstack11l111lll1l_opy_(cmd)
        self.bstack11l11l111ll_opy_ = False
    except Exception as e:
      self.logger.error(bstack11l1l11_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸࡺ࡯ࡱࠢࡶࡩࡸࡹࡩࡰࡰࠣࡻ࡮ࡺࡨࠡࡥࡲࡱࡲࡧ࡮ࡥࠢ࠰ࠤࢀࢃࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱ࠾ࠥࢁࡽࠣᱎ").format(cmd, e))
  def bstack1l1l1111l1_opy_(self):
    if not self.bstack1l111llll_opy_:
      return
    try:
      bstack11l11ll1l11_opy_ = 0
      while not self.bstack11l11l111ll_opy_ and bstack11l11ll1l11_opy_ < self.bstack11l11llll1l_opy_:
        if self.bstack11l1l11l111_opy_:
          self.logger.info(bstack11l1l11_opy_ (u"ࠤࡓࡩࡷࡩࡹࠡࡵࡨࡸࡺࡶࠠࡧࡣ࡬ࡰࡪࡪࠢᱏ"))
          return
        time.sleep(1)
        bstack11l11ll1l11_opy_ += 1
      os.environ[bstack11l1l11_opy_ (u"ࠪࡔࡊࡘࡃ࡚ࡡࡅࡉࡘ࡚࡟ࡑࡎࡄࡘࡋࡕࡒࡎࠩ᱐")] = str(self.bstack11l111l1111_opy_())
      self.logger.info(bstack11l1l11_opy_ (u"ࠦࡕ࡫ࡲࡤࡻࠣࡷࡪࡺࡵࡱࠢࡦࡳࡲࡶ࡬ࡦࡶࡨࡨࠧ᱑"))
    except Exception as e:
      self.logger.error(bstack11l1l11_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡨࡸࡺࡶࠠࡱࡧࡵࡧࡾ࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡿࢂࠨ᱒").format(e))
  def bstack11l111l1111_opy_(self):
    if self.bstack1llll11111_opy_:
      return
    try:
      bstack11l1l111l1l_opy_ = [platform[bstack11l1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫ᱓")].lower() for platform in self.config.get(bstack11l1l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ᱔"), [])]
      bstack11l11l11ll1_opy_ = sys.maxsize
      bstack11l11ll1111_opy_ = bstack11l1l11_opy_ (u"ࠨࠩ᱕")
      for browser in bstack11l1l111l1l_opy_:
        if browser in self.bstack11l111l11l1_opy_:
          bstack11l111l11ll_opy_ = self.bstack11l111l11l1_opy_[browser]
        if bstack11l111l11ll_opy_ < bstack11l11l11ll1_opy_:
          bstack11l11l11ll1_opy_ = bstack11l111l11ll_opy_
          bstack11l11ll1111_opy_ = browser
      return bstack11l11ll1111_opy_
    except Exception as e:
      self.logger.error(bstack11l1l11_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥ࡬ࡩ࡯ࡦࠣࡦࡪࡹࡴࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡼࡿࠥ᱖").format(e))
  @classmethod
  def bstack1ll1111111_opy_(self):
    return os.getenv(bstack11l1l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡉࡗࡉ࡙ࠨ᱗"), bstack11l1l11_opy_ (u"ࠫࡋࡧ࡬ࡴࡧࠪ᱘")).lower()
  @classmethod
  def bstack11lllll1_opy_(self):
    return os.getenv(bstack11l1l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡋࡒࡄ࡛ࡢࡇࡆࡖࡔࡖࡔࡈࡣࡒࡕࡄࡆࠩ᱙"), bstack11l1l11_opy_ (u"࠭ࠧᱚ"))
  @classmethod
  def bstack1l1lll1lll1_opy_(cls, value):
    cls.bstack1lllll11_opy_ = value
  @classmethod
  def bstack11l1111lll1_opy_(cls):
    return cls.bstack1lllll11_opy_
  @classmethod
  def bstack1l1lll1ll11_opy_(cls, value):
    cls.percy_build_id = value
  @classmethod
  def bstack11l111ll111_opy_(cls):
    return cls.percy_build_id
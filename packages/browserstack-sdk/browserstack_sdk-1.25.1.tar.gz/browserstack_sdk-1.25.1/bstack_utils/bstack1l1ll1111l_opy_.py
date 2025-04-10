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
import sys
import logging
import tarfile
import io
import os
import time
import requests
import re
from requests_toolbelt.multipart.encoder import MultipartEncoder
from bstack_utils.constants import bstack11lll111ll1_opy_, bstack11ll1ll1ll1_opy_
import tempfile
import json
bstack11l11l1l1l1_opy_ = os.getenv(bstack1ll1l1_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡍ࡟ࡇࡋࡏࡉࠧᯚ"), None) or os.path.join(tempfile.gettempdir(), bstack1ll1l1_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡩ࡫ࡢࡶࡩ࠱ࡰࡴ࡭ࠢᯛ"))
bstack11l111ll111_opy_ = os.path.join(bstack1ll1l1_opy_ (u"ࠨ࡬ࡰࡩࠥᯜ"), bstack1ll1l1_opy_ (u"ࠧࡴࡦ࡮࠱ࡨࡲࡩ࠮ࡦࡨࡦࡺ࡭࠮࡭ࡱࡪࠫᯝ"))
logging.Formatter.converter = time.gmtime
def get_logger(name=__name__, level=None):
  logger = logging.getLogger(name)
  if level:
    logging.basicConfig(
      level=level,
      format=bstack1ll1l1_opy_ (u"ࠨࠧࠫࡥࡸࡩࡴࡪ࡯ࡨ࠭ࡸ࡛ࠦࠦࠪࡱࡥࡲ࡫ࠩࡴ࡟࡞ࠩ࠭ࡲࡥࡷࡧ࡯ࡲࡦࡳࡥࠪࡵࡠࠤ࠲ࠦࠥࠩ࡯ࡨࡷࡸࡧࡧࡦࠫࡶࠫᯞ"),
      datefmt=bstack1ll1l1_opy_ (u"ࠩࠨ࡝࠲ࠫ࡭࠮ࠧࡧࡘࠪࡎ࠺ࠦࡏ࠽ࠩࡘࡠࠧᯟ"),
      stream=sys.stdout
    )
  return logger
def bstack1lll1l11lll_opy_():
  bstack11l11l11111_opy_ = os.environ.get(bstack1ll1l1_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅࡍࡓࡇࡒ࡚ࡡࡇࡉࡇ࡛ࡇࠣᯠ"), bstack1ll1l1_opy_ (u"ࠦ࡫ࡧ࡬ࡴࡧࠥᯡ"))
  return logging.DEBUG if bstack11l11l11111_opy_.lower() == bstack1ll1l1_opy_ (u"ࠧࡺࡲࡶࡧࠥᯢ") else logging.INFO
def bstack1ll111lll1l_opy_():
  global bstack11l11l1l1l1_opy_
  if os.path.exists(bstack11l11l1l1l1_opy_):
    os.remove(bstack11l11l1l1l1_opy_)
  if os.path.exists(bstack11l111ll111_opy_):
    os.remove(bstack11l111ll111_opy_)
def bstack1lll111lll_opy_():
  for handler in logging.getLogger().handlers:
    logging.getLogger().removeHandler(handler)
def bstack1l1l1l111_opy_(config, log_level):
  bstack11l11l11ll1_opy_ = log_level
  if bstack1ll1l1_opy_ (u"࠭࡬ࡰࡩࡏࡩࡻ࡫࡬ࠨᯣ") in config and config[bstack1ll1l1_opy_ (u"ࠧ࡭ࡱࡪࡐࡪࡼࡥ࡭ࠩᯤ")] in bstack11lll111ll1_opy_:
    bstack11l11l11ll1_opy_ = bstack11lll111ll1_opy_[config[bstack1ll1l1_opy_ (u"ࠨ࡮ࡲ࡫ࡑ࡫ࡶࡦ࡮ࠪᯥ")]]
  if config.get(bstack1ll1l1_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡄࡹࡹࡵࡃࡢࡲࡷࡹࡷ࡫ࡌࡰࡩࡶ᯦ࠫ"), False):
    logging.getLogger().setLevel(bstack11l11l11ll1_opy_)
    return bstack11l11l11ll1_opy_
  global bstack11l11l1l1l1_opy_
  bstack1lll111lll_opy_()
  bstack11l11l1111l_opy_ = logging.Formatter(
    fmt=bstack1ll1l1_opy_ (u"ࠪࠩ࠭ࡧࡳࡤࡶ࡬ࡱࡪ࠯ࡳࠡ࡝ࠨࠬࡳࡧ࡭ࡦࠫࡶࡡࡠࠫࠨ࡭ࡧࡹࡩࡱࡴࡡ࡮ࡧࠬࡷࡢࠦ࠭ࠡࠧࠫࡱࡪࡹࡳࡢࡩࡨ࠭ࡸ࠭ᯧ"),
    datefmt=bstack1ll1l1_opy_ (u"ࠫࠪ࡟࠭ࠦ࡯࠰ࠩࡩ࡚ࠥࡉ࠼ࠨࡑ࠿ࠫࡓ࡛ࠩᯨ"),
  )
  bstack11l11l11lll_opy_ = logging.StreamHandler(sys.stdout)
  file_handler = logging.FileHandler(bstack11l11l1l1l1_opy_)
  file_handler.setFormatter(bstack11l11l1111l_opy_)
  bstack11l11l11lll_opy_.setFormatter(bstack11l11l1111l_opy_)
  file_handler.setLevel(logging.DEBUG)
  bstack11l11l11lll_opy_.setLevel(log_level)
  file_handler.addFilter(lambda r: r.name != bstack1ll1l1_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࠮ࡸࡧࡥࡨࡷ࡯ࡶࡦࡴ࠱ࡶࡪࡳ࡯ࡵࡧ࠱ࡶࡪࡳ࡯ࡵࡧࡢࡧࡴࡴ࡮ࡦࡥࡷ࡭ࡴࡴࠧᯩ"))
  logging.getLogger().setLevel(logging.DEBUG)
  bstack11l11l11lll_opy_.setLevel(bstack11l11l11ll1_opy_)
  logging.getLogger().addHandler(bstack11l11l11lll_opy_)
  logging.getLogger().addHandler(file_handler)
  return bstack11l11l11ll1_opy_
def bstack11l111ll1l1_opy_(config):
  try:
    bstack11l11l1ll1l_opy_ = set(bstack11ll1ll1ll1_opy_)
    bstack11l11l1l1ll_opy_ = bstack1ll1l1_opy_ (u"࠭ࠧᯪ")
    with open(bstack1ll1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹ࡮࡮ࠪᯫ")) as bstack11l11l1ll11_opy_:
      bstack11l111llll1_opy_ = bstack11l11l1ll11_opy_.read()
      bstack11l11l1l1ll_opy_ = re.sub(bstack1ll1l1_opy_ (u"ࡳࠩࡡࠬࡡࡹࠫࠪࡁࠦ࠲࠯ࠪ࡜࡯ࠩᯬ"), bstack1ll1l1_opy_ (u"ࠩࠪᯭ"), bstack11l111llll1_opy_, flags=re.M)
      bstack11l11l1l1ll_opy_ = re.sub(
        bstack1ll1l1_opy_ (u"ࡵࠫࡣ࠮࡜ࡴ࠭ࠬࡃ࠭࠭ᯮ") + bstack1ll1l1_opy_ (u"ࠫࢁ࠭ᯯ").join(bstack11l11l1ll1l_opy_) + bstack1ll1l1_opy_ (u"ࠬ࠯࠮ࠫࠦࠪᯰ"),
        bstack1ll1l1_opy_ (u"ࡸࠧ࡝࠴࠽ࠤࡠࡘࡅࡅࡃࡆࡘࡊࡊ࡝ࠨᯱ"),
        bstack11l11l1l1ll_opy_, flags=re.M | re.I
      )
    def bstack11l111ll1ll_opy_(dic):
      bstack11l111ll11l_opy_ = {}
      for key, value in dic.items():
        if key in bstack11l11l1ll1l_opy_:
          bstack11l111ll11l_opy_[key] = bstack1ll1l1_opy_ (u"ࠧ࡜ࡔࡈࡈࡆࡉࡔࡆࡆࡠ᯲ࠫ")
        else:
          if isinstance(value, dict):
            bstack11l111ll11l_opy_[key] = bstack11l111ll1ll_opy_(value)
          else:
            bstack11l111ll11l_opy_[key] = value
      return bstack11l111ll11l_opy_
    bstack11l111ll11l_opy_ = bstack11l111ll1ll_opy_(config)
    return {
      bstack1ll1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡺ࡯࡯᯳ࠫ"): bstack11l11l1l1ll_opy_,
      bstack1ll1l1_opy_ (u"ࠩࡩ࡭ࡳࡧ࡬ࡤࡱࡱࡪ࡮࡭࠮࡫ࡵࡲࡲࠬ᯴"): json.dumps(bstack11l111ll11l_opy_)
    }
  except Exception as e:
    return {}
def bstack11l11l11l1l_opy_(inipath, rootpath):
  log_dir = os.path.join(os.getcwd(), bstack1ll1l1_opy_ (u"ࠪࡰࡴ࡭ࠧ᯵"))
  if not os.path.exists(log_dir):
    os.makedirs(log_dir)
  bstack11l11l111l1_opy_ = os.path.join(log_dir, bstack1ll1l1_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡨࡵ࡮ࡧ࡫ࡪࡷࠬ᯶"))
  if not os.path.exists(bstack11l11l111l1_opy_):
    bstack11l11l11l11_opy_ = {
      bstack1ll1l1_opy_ (u"ࠧ࡯࡮ࡪࡲࡤࡸ࡭ࠨ᯷"): str(inipath),
      bstack1ll1l1_opy_ (u"ࠨࡲࡰࡱࡷࡴࡦࡺࡨࠣ᯸"): str(rootpath)
    }
    with open(os.path.join(log_dir, bstack1ll1l1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࡟ࡤࡱࡱࡪ࡮࡭ࡳ࠯࡬ࡶࡳࡳ࠭᯹")), bstack1ll1l1_opy_ (u"ࠨࡹࠪ᯺")) as bstack11l111lll11_opy_:
      bstack11l111lll11_opy_.write(json.dumps(bstack11l11l11l11_opy_))
def bstack11l11l1l11l_opy_():
  try:
    bstack11l11l111l1_opy_ = os.path.join(os.getcwd(), bstack1ll1l1_opy_ (u"ࠩ࡯ࡳ࡬࠭᯻"), bstack1ll1l1_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡧࡴࡴࡦࡪࡩࡶ࠲࡯ࡹ࡯࡯ࠩ᯼"))
    if os.path.exists(bstack11l11l111l1_opy_):
      with open(bstack11l11l111l1_opy_, bstack1ll1l1_opy_ (u"ࠫࡷ࠭᯽")) as bstack11l111lll11_opy_:
        bstack11l111lll1l_opy_ = json.load(bstack11l111lll11_opy_)
      return bstack11l111lll1l_opy_.get(bstack1ll1l1_opy_ (u"ࠬ࡯࡮ࡪࡲࡤࡸ࡭࠭᯾"), bstack1ll1l1_opy_ (u"࠭ࠧ᯿")), bstack11l111lll1l_opy_.get(bstack1ll1l1_opy_ (u"ࠧࡳࡱࡲࡸࡵࡧࡴࡩࠩᰀ"), bstack1ll1l1_opy_ (u"ࠨࠩᰁ"))
  except:
    pass
  return None, None
def bstack11l111lllll_opy_():
  try:
    bstack11l11l111l1_opy_ = os.path.join(os.getcwd(), bstack1ll1l1_opy_ (u"ࠩ࡯ࡳ࡬࠭ᰂ"), bstack1ll1l1_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡧࡴࡴࡦࡪࡩࡶ࠲࡯ࡹ࡯࡯ࠩᰃ"))
    if os.path.exists(bstack11l11l111l1_opy_):
      os.remove(bstack11l11l111l1_opy_)
  except:
    pass
def bstack1l111lll1_opy_(config):
  from bstack_utils.helper import bstack11ll11ll_opy_
  global bstack11l11l1l1l1_opy_
  try:
    if config.get(bstack1ll1l1_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩࡆࡻࡴࡰࡅࡤࡴࡹࡻࡲࡦࡎࡲ࡫ࡸ࠭ᰄ"), False):
      return
    uuid = os.getenv(bstack1ll1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪᰅ")) if os.getenv(bstack1ll1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫᰆ")) else bstack11ll11ll_opy_.get_property(bstack1ll1l1_opy_ (u"ࠢࡴࡦ࡮ࡖࡺࡴࡉࡥࠤᰇ"))
    if not uuid or uuid == bstack1ll1l1_opy_ (u"ࠨࡰࡸࡰࡱ࠭ᰈ"):
      return
    bstack11l11l111ll_opy_ = [bstack1ll1l1_opy_ (u"ࠩࡵࡩࡶࡻࡩࡳࡧࡰࡩࡳࡺࡳ࠯ࡶࡻࡸࠬᰉ"), bstack1ll1l1_opy_ (u"ࠪࡔ࡮ࡶࡦࡪ࡮ࡨࠫᰊ"), bstack1ll1l1_opy_ (u"ࠫࡵࡿࡰࡳࡱ࡭ࡩࡨࡺ࠮ࡵࡱࡰࡰࠬᰋ"), bstack11l11l1l1l1_opy_, bstack11l111ll111_opy_]
    bstack11l11l1l111_opy_, root_path = bstack11l11l1l11l_opy_()
    if bstack11l11l1l111_opy_ != None:
      bstack11l11l111ll_opy_.append(bstack11l11l1l111_opy_)
    if root_path != None:
      bstack11l11l111ll_opy_.append(os.path.join(root_path, bstack1ll1l1_opy_ (u"ࠬࡩ࡯࡯ࡨࡷࡩࡸࡺ࠮ࡱࡻࠪᰌ")))
    bstack1lll111lll_opy_()
    logging.shutdown()
    output_file = os.path.join(tempfile.gettempdir(), bstack1ll1l1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࠳࡬ࡰࡩࡶ࠱ࠬᰍ") + uuid + bstack1ll1l1_opy_ (u"ࠧ࠯ࡶࡤࡶ࠳࡭ࡺࠨᰎ"))
    with tarfile.open(output_file, bstack1ll1l1_opy_ (u"ࠣࡹ࠽࡫ࡿࠨᰏ")) as archive:
      for file in filter(lambda f: os.path.exists(f), bstack11l11l111ll_opy_):
        try:
          archive.add(file,  arcname=os.path.basename(file))
        except:
          pass
      for name, data in bstack11l111ll1l1_opy_(config).items():
        tarinfo = tarfile.TarInfo(name)
        bstack11l111l1lll_opy_ = data.encode()
        tarinfo.size = len(bstack11l111l1lll_opy_)
        archive.addfile(tarinfo, io.BytesIO(bstack11l111l1lll_opy_))
    bstack1l1lll1l1l_opy_ = MultipartEncoder(
      fields= {
        bstack1ll1l1_opy_ (u"ࠩࡧࡥࡹࡧࠧᰐ"): (os.path.basename(output_file), open(os.path.abspath(output_file), bstack1ll1l1_opy_ (u"ࠪࡶࡧ࠭ᰑ")), bstack1ll1l1_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱ࡻ࠱࡬ࢀࡩࡱࠩᰒ")),
        bstack1ll1l1_opy_ (u"ࠬࡩ࡬ࡪࡧࡱࡸࡇࡻࡩ࡭ࡦࡘࡹ࡮ࡪࠧᰓ"): uuid
      }
    )
    response = requests.post(
      bstack1ll1l1_opy_ (u"ࠨࡨࡵࡶࡳࡷ࠿࠵࠯ࡶࡲ࡯ࡳࡦࡪ࠭ࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡧࡱ࡯ࡥ࡯ࡶ࠰ࡰࡴ࡭ࡳ࠰ࡷࡳࡰࡴࡧࡤࠣᰔ"),
      data=bstack1l1lll1l1l_opy_,
      headers={bstack1ll1l1_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪ࠭ᰕ"): bstack1l1lll1l1l_opy_.content_type},
      auth=(config[bstack1ll1l1_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪᰖ")], config[bstack1ll1l1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬᰗ")])
    )
    os.remove(output_file)
    if response.status_code != 200:
      get_logger().debug(bstack1ll1l1_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢࡸࡴࡱࡵࡡࡥࠢ࡯ࡳ࡬ࡹ࠺ࠡࠩᰘ") + response.status_code)
  except Exception as e:
    get_logger().debug(bstack1ll1l1_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡷࡪࡴࡤࡪࡰࡪࠤࡱࡵࡧࡴ࠼ࠪᰙ") + str(e))
  finally:
    try:
      bstack1ll111lll1l_opy_()
      bstack11l111lllll_opy_()
    except:
      pass
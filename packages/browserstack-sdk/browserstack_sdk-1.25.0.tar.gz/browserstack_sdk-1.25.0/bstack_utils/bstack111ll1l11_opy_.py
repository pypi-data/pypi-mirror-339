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
import sys
import logging
import tarfile
import io
import os
import time
import requests
import re
from requests_toolbelt.multipart.encoder import MultipartEncoder
from bstack_utils.constants import bstack11lllll1l11_opy_, bstack11llll1ll11_opy_
import tempfile
import json
bstack11l1ll111ll_opy_ = os.getenv(bstack11l1l11_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡑࡊࡣࡋࡏࡌࡆࠤᭋ"), None) or os.path.join(tempfile.gettempdir(), bstack11l1l11_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡦࡨࡦࡺ࡭࠮࡭ࡱࡪࠦᭌ"))
bstack11l1ll11l1l_opy_ = os.path.join(bstack11l1l11_opy_ (u"ࠥࡰࡴ࡭ࠢ᭍"), bstack11l1l11_opy_ (u"ࠫࡸࡪ࡫࠮ࡥ࡯࡭࠲ࡪࡥࡣࡷࡪ࠲ࡱࡵࡧࠨ᭎"))
logging.Formatter.converter = time.gmtime
def get_logger(name=__name__, level=None):
  logger = logging.getLogger(name)
  if level:
    logging.basicConfig(
      level=level,
      format=bstack11l1l11_opy_ (u"ࠬࠫࠨࡢࡵࡦࡸ࡮ࡳࡥࠪࡵࠣ࡟ࠪ࠮࡮ࡢ࡯ࡨ࠭ࡸࡣ࡛ࠦࠪ࡯ࡩࡻ࡫࡬࡯ࡣࡰࡩ࠮ࡹ࡝ࠡ࠯ࠣࠩ࠭ࡳࡥࡴࡵࡤ࡫ࡪ࠯ࡳࠨ᭏"),
      datefmt=bstack11l1l11_opy_ (u"࡚࠭ࠥ࠯ࠨࡱ࠲ࠫࡤࡕࠧࡋ࠾ࠪࡓ࠺ࠦࡕ࡝ࠫ᭐"),
      stream=sys.stdout
    )
  return logger
def bstack1lll111ll11_opy_():
  bstack11l1l1lll1l_opy_ = os.environ.get(bstack11l1l11_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡂࡊࡐࡄࡖ࡞ࡥࡄࡆࡄࡘࡋࠧ᭑"), bstack11l1l11_opy_ (u"ࠣࡨࡤࡰࡸ࡫ࠢ᭒"))
  return logging.DEBUG if bstack11l1l1lll1l_opy_.lower() == bstack11l1l11_opy_ (u"ࠤࡷࡶࡺ࡫ࠢ᭓") else logging.INFO
def bstack1ll11111111_opy_():
  global bstack11l1ll111ll_opy_
  if os.path.exists(bstack11l1ll111ll_opy_):
    os.remove(bstack11l1ll111ll_opy_)
  if os.path.exists(bstack11l1ll11l1l_opy_):
    os.remove(bstack11l1ll11l1l_opy_)
def bstack1l1l1111_opy_():
  for handler in logging.getLogger().handlers:
    logging.getLogger().removeHandler(handler)
def bstack11ll1l111l_opy_(config, log_level):
  bstack11l1l1ll111_opy_ = log_level
  if bstack11l1l11_opy_ (u"ࠪࡰࡴ࡭ࡌࡦࡸࡨࡰࠬ᭔") in config and config[bstack11l1l11_opy_ (u"ࠫࡱࡵࡧࡍࡧࡹࡩࡱ࠭᭕")] in bstack11lllll1l11_opy_:
    bstack11l1l1ll111_opy_ = bstack11lllll1l11_opy_[config[bstack11l1l11_opy_ (u"ࠬࡲ࡯ࡨࡎࡨࡺࡪࡲࠧ᭖")]]
  if config.get(bstack11l1l11_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡁࡶࡶࡲࡇࡦࡶࡴࡶࡴࡨࡐࡴ࡭ࡳࠨ᭗"), False):
    logging.getLogger().setLevel(bstack11l1l1ll111_opy_)
    return bstack11l1l1ll111_opy_
  global bstack11l1ll111ll_opy_
  bstack1l1l1111_opy_()
  bstack11l1l1llll1_opy_ = logging.Formatter(
    fmt=bstack11l1l11_opy_ (u"ࠧࠦࠪࡤࡷࡨࡺࡩ࡮ࡧࠬࡷࠥࡡࠥࠩࡰࡤࡱࡪ࠯ࡳ࡞࡝ࠨࠬࡱ࡫ࡶࡦ࡮ࡱࡥࡲ࡫ࠩࡴ࡟ࠣ࠱ࠥࠫࠨ࡮ࡧࡶࡷࡦ࡭ࡥࠪࡵࠪ᭘"),
    datefmt=bstack11l1l11_opy_ (u"ࠨࠧ࡜࠱ࠪࡳ࠭ࠦࡦࡗࠩࡍࡀࠥࡎ࠼ࠨࡗ࡟࠭᭙"),
  )
  bstack11l1l1ll1ll_opy_ = logging.StreamHandler(sys.stdout)
  file_handler = logging.FileHandler(bstack11l1ll111ll_opy_)
  file_handler.setFormatter(bstack11l1l1llll1_opy_)
  bstack11l1l1ll1ll_opy_.setFormatter(bstack11l1l1llll1_opy_)
  file_handler.setLevel(logging.DEBUG)
  bstack11l1l1ll1ll_opy_.setLevel(log_level)
  file_handler.addFilter(lambda r: r.name != bstack11l1l11_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ࠲ࡼ࡫ࡢࡥࡴ࡬ࡺࡪࡸ࠮ࡳࡧࡰࡳࡹ࡫࠮ࡳࡧࡰࡳࡹ࡫࡟ࡤࡱࡱࡲࡪࡩࡴࡪࡱࡱࠫ᭚"))
  logging.getLogger().setLevel(logging.DEBUG)
  bstack11l1l1ll1ll_opy_.setLevel(bstack11l1l1ll111_opy_)
  logging.getLogger().addHandler(bstack11l1l1ll1ll_opy_)
  logging.getLogger().addHandler(file_handler)
  return bstack11l1l1ll111_opy_
def bstack11l1l1l1l1l_opy_(config):
  try:
    bstack11l1l1l11ll_opy_ = set(bstack11llll1ll11_opy_)
    bstack11l1ll11111_opy_ = bstack11l1l11_opy_ (u"ࠪࠫ᭛")
    with open(bstack11l1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡽࡲࡲࠧ᭜")) as bstack11l1l1l1111_opy_:
      bstack11l1ll1111l_opy_ = bstack11l1l1l1111_opy_.read()
      bstack11l1ll11111_opy_ = re.sub(bstack11l1l11_opy_ (u"ࡷ࠭࡞ࠩ࡞ࡶ࠯࠮ࡅࠣ࠯ࠬࠧࡠࡳ࠭᭝"), bstack11l1l11_opy_ (u"࠭ࠧ᭞"), bstack11l1ll1111l_opy_, flags=re.M)
      bstack11l1ll11111_opy_ = re.sub(
        bstack11l1l11_opy_ (u"ࡲࠨࡠࠫࡠࡸ࠱ࠩࡀࠪࠪ᭟") + bstack11l1l11_opy_ (u"ࠨࡾࠪ᭠").join(bstack11l1l1l11ll_opy_) + bstack11l1l11_opy_ (u"ࠩࠬ࠲࠯ࠪࠧ᭡"),
        bstack11l1l11_opy_ (u"ࡵࠫࡡ࠸࠺ࠡ࡝ࡕࡉࡉࡇࡃࡕࡇࡇࡡࠬ᭢"),
        bstack11l1ll11111_opy_, flags=re.M | re.I
      )
    def bstack11l1ll111l1_opy_(dic):
      bstack11l1l1l1ll1_opy_ = {}
      for key, value in dic.items():
        if key in bstack11l1l1l11ll_opy_:
          bstack11l1l1l1ll1_opy_[key] = bstack11l1l11_opy_ (u"ࠫࡠࡘࡅࡅࡃࡆࡘࡊࡊ࡝ࠨ᭣")
        else:
          if isinstance(value, dict):
            bstack11l1l1l1ll1_opy_[key] = bstack11l1ll111l1_opy_(value)
          else:
            bstack11l1l1l1ll1_opy_[key] = value
      return bstack11l1l1l1ll1_opy_
    bstack11l1l1l1ll1_opy_ = bstack11l1ll111l1_opy_(config)
    return {
      bstack11l1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡾࡳ࡬ࠨ᭤"): bstack11l1ll11111_opy_,
      bstack11l1l11_opy_ (u"࠭ࡦࡪࡰࡤࡰࡨࡵ࡮ࡧ࡫ࡪ࠲࡯ࡹ࡯࡯ࠩ᭥"): json.dumps(bstack11l1l1l1ll1_opy_)
    }
  except Exception as e:
    return {}
def bstack11l1l1lll11_opy_(inipath, rootpath):
  log_dir = os.path.join(os.getcwd(), bstack11l1l11_opy_ (u"ࠧ࡭ࡱࡪࠫ᭦"))
  if not os.path.exists(log_dir):
    os.makedirs(log_dir)
  bstack11l1ll11ll1_opy_ = os.path.join(log_dir, bstack11l1l11_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡥࡲࡲ࡫࡯ࡧࡴࠩ᭧"))
  if not os.path.exists(bstack11l1ll11ll1_opy_):
    bstack11l1l1lllll_opy_ = {
      bstack11l1l11_opy_ (u"ࠤ࡬ࡲ࡮ࡶࡡࡵࡪࠥ᭨"): str(inipath),
      bstack11l1l11_opy_ (u"ࠥࡶࡴࡵࡴࡱࡣࡷ࡬ࠧ᭩"): str(rootpath)
    }
    with open(os.path.join(log_dir, bstack11l1l11_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡨࡵ࡮ࡧ࡫ࡪࡷ࠳ࡰࡳࡰࡰࠪ᭪")), bstack11l1l11_opy_ (u"ࠬࡽࠧ᭫")) as bstack11l1l1l1l11_opy_:
      bstack11l1l1l1l11_opy_.write(json.dumps(bstack11l1l1lllll_opy_))
def bstack11l1l1l11l1_opy_():
  try:
    bstack11l1ll11ll1_opy_ = os.path.join(os.getcwd(), bstack11l1l11_opy_ (u"࠭࡬ࡰࡩ᭬ࠪ"), bstack11l1l11_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࡟ࡤࡱࡱࡪ࡮࡭ࡳ࠯࡬ࡶࡳࡳ࠭᭭"))
    if os.path.exists(bstack11l1ll11ll1_opy_):
      with open(bstack11l1ll11ll1_opy_, bstack11l1l11_opy_ (u"ࠨࡴࠪ᭮")) as bstack11l1l1l1l11_opy_:
        bstack11l1l1l111l_opy_ = json.load(bstack11l1l1l1l11_opy_)
      return bstack11l1l1l111l_opy_.get(bstack11l1l11_opy_ (u"ࠩ࡬ࡲ࡮ࡶࡡࡵࡪࠪ᭯"), bstack11l1l11_opy_ (u"ࠪࠫ᭰")), bstack11l1l1l111l_opy_.get(bstack11l1l11_opy_ (u"ࠫࡷࡵ࡯ࡵࡲࡤࡸ࡭࠭᭱"), bstack11l1l11_opy_ (u"ࠬ࠭᭲"))
  except:
    pass
  return None, None
def bstack11l1l1l1lll_opy_():
  try:
    bstack11l1ll11ll1_opy_ = os.path.join(os.getcwd(), bstack11l1l11_opy_ (u"࠭࡬ࡰࡩࠪ᭳"), bstack11l1l11_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࡟ࡤࡱࡱࡪ࡮࡭ࡳ࠯࡬ࡶࡳࡳ࠭᭴"))
    if os.path.exists(bstack11l1ll11ll1_opy_):
      os.remove(bstack11l1ll11ll1_opy_)
  except:
    pass
def bstack1lll1l1111_opy_(config):
  from bstack_utils.helper import bstack111ll1lll_opy_
  global bstack11l1ll111ll_opy_
  try:
    if config.get(bstack11l1l11_opy_ (u"ࠨࡦ࡬ࡷࡦࡨ࡬ࡦࡃࡸࡸࡴࡉࡡࡱࡶࡸࡶࡪࡒ࡯ࡨࡵࠪ᭵"), False):
      return
    uuid = os.getenv(bstack11l1l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧ᭶")) if os.getenv(bstack11l1l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨ᭷")) else bstack111ll1lll_opy_.get_property(bstack11l1l11_opy_ (u"ࠦࡸࡪ࡫ࡓࡷࡱࡍࡩࠨ᭸"))
    if not uuid or uuid == bstack11l1l11_opy_ (u"ࠬࡴࡵ࡭࡮ࠪ᭹"):
      return
    bstack11l1l1ll11l_opy_ = [bstack11l1l11_opy_ (u"࠭ࡲࡦࡳࡸ࡭ࡷ࡫࡭ࡦࡰࡷࡷ࠳ࡺࡸࡵࠩ᭺"), bstack11l1l11_opy_ (u"ࠧࡑ࡫ࡳࡪ࡮ࡲࡥࠨ᭻"), bstack11l1l11_opy_ (u"ࠨࡲࡼࡴࡷࡵࡪࡦࡥࡷ࠲ࡹࡵ࡭࡭ࠩ᭼"), bstack11l1ll111ll_opy_, bstack11l1ll11l1l_opy_]
    bstack11l1ll11l11_opy_, root_path = bstack11l1l1l11l1_opy_()
    if bstack11l1ll11l11_opy_ != None:
      bstack11l1l1ll11l_opy_.append(bstack11l1ll11l11_opy_)
    if root_path != None:
      bstack11l1l1ll11l_opy_.append(os.path.join(root_path, bstack11l1l11_opy_ (u"ࠩࡦࡳࡳ࡬ࡴࡦࡵࡷ࠲ࡵࡿࠧ᭽")))
    bstack1l1l1111_opy_()
    logging.shutdown()
    output_file = os.path.join(tempfile.gettempdir(), bstack11l1l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠰ࡰࡴ࡭ࡳ࠮ࠩ᭾") + uuid + bstack11l1l11_opy_ (u"ࠫ࠳ࡺࡡࡳ࠰ࡪࡾࠬ᭿"))
    with tarfile.open(output_file, bstack11l1l11_opy_ (u"ࠧࡽ࠺ࡨࡼࠥᮀ")) as archive:
      for file in filter(lambda f: os.path.exists(f), bstack11l1l1ll11l_opy_):
        try:
          archive.add(file,  arcname=os.path.basename(file))
        except:
          pass
      for name, data in bstack11l1l1l1l1l_opy_(config).items():
        tarinfo = tarfile.TarInfo(name)
        bstack11l1l1ll1l1_opy_ = data.encode()
        tarinfo.size = len(bstack11l1l1ll1l1_opy_)
        archive.addfile(tarinfo, io.BytesIO(bstack11l1l1ll1l1_opy_))
    bstack1l111l111_opy_ = MultipartEncoder(
      fields= {
        bstack11l1l11_opy_ (u"࠭ࡤࡢࡶࡤࠫᮁ"): (os.path.basename(output_file), open(os.path.abspath(output_file), bstack11l1l11_opy_ (u"ࠧࡳࡤࠪᮂ")), bstack11l1l11_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡸ࠮ࡩࡽ࡭ࡵ࠭ᮃ")),
        bstack11l1l11_opy_ (u"ࠩࡦࡰ࡮࡫࡮ࡵࡄࡸ࡭ࡱࡪࡕࡶ࡫ࡧࠫᮄ"): uuid
      }
    )
    response = requests.post(
      bstack11l1l11_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡺࡶ࡬ࡰࡣࡧ࠱ࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡤ࡮࡬ࡩࡳࡺ࠭࡭ࡱࡪࡷ࠴ࡻࡰ࡭ࡱࡤࡨࠧᮅ"),
      data=bstack1l111l111_opy_,
      headers={bstack11l1l11_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠪᮆ"): bstack1l111l111_opy_.content_type},
      auth=(config[bstack11l1l11_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧᮇ")], config[bstack11l1l11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩᮈ")])
    )
    os.remove(output_file)
    if response.status_code != 200:
      get_logger().debug(bstack11l1l11_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡵࡱ࡮ࡲࡥࡩࠦ࡬ࡰࡩࡶ࠾ࠥ࠭ᮉ") + response.status_code)
  except Exception as e:
    get_logger().debug(bstack11l1l11_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡴࡧࡱࡨ࡮ࡴࡧࠡ࡮ࡲ࡫ࡸࡀࠧᮊ") + str(e))
  finally:
    try:
      bstack1ll11111111_opy_()
      bstack11l1l1l1lll_opy_()
    except:
      pass
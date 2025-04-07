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
from bstack_utils.bstack111ll1l11_opy_ import get_logger
logger = get_logger(__name__)
class bstack1l111ll11ll_opy_(object):
  bstack1l11l11ll_opy_ = os.path.join(os.path.expanduser(bstack11l1l11_opy_ (u"ࠧࡿࠩᓁ")), bstack11l1l11_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨᓂ"))
  bstack1l111ll1lll_opy_ = os.path.join(bstack1l11l11ll_opy_, bstack11l1l11_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࡶ࠲࡯ࡹ࡯࡯ࠩᓃ"))
  commands_to_wrap = None
  perform_scan = None
  bstack11l1lll11l_opy_ = None
  bstack1l111ll11_opy_ = None
  bstack1l111ll11l1_opy_ = None
  def __new__(cls):
    if not hasattr(cls, bstack11l1l11_opy_ (u"ࠪ࡭ࡳࡹࡴࡢࡰࡦࡩࠬᓄ")):
      cls.instance = super(bstack1l111ll11ll_opy_, cls).__new__(cls)
      cls.instance.bstack1l111ll1l11_opy_()
    return cls.instance
  def bstack1l111ll1l11_opy_(self):
    try:
      with open(self.bstack1l111ll1lll_opy_, bstack11l1l11_opy_ (u"ࠫࡷ࠭ᓅ")) as bstack1lll11lll_opy_:
        bstack1l111ll1l1l_opy_ = bstack1lll11lll_opy_.read()
        data = json.loads(bstack1l111ll1l1l_opy_)
        if bstack11l1l11_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩࡹࠧᓆ") in data:
          self.bstack1l111ll1ll1_opy_(data[bstack11l1l11_opy_ (u"࠭ࡣࡰ࡯ࡰࡥࡳࡪࡳࠨᓇ")])
        if bstack11l1l11_opy_ (u"ࠧࡴࡥࡵ࡭ࡵࡺࡳࠨᓈ") in data:
          self.bstack1l1l1l1111_opy_(data[bstack11l1l11_opy_ (u"ࠨࡵࡦࡶ࡮ࡶࡴࡴࠩᓉ")])
    except:
      pass
  def bstack1l1l1l1111_opy_(self, scripts):
    if scripts != None:
      self.perform_scan = scripts.get(bstack11l1l11_opy_ (u"ࠩࡶࡧࡦࡴࠧᓊ"),bstack11l1l11_opy_ (u"ࠪࠫᓋ"))
      self.bstack11l1lll11l_opy_ = scripts.get(bstack11l1l11_opy_ (u"ࠫ࡬࡫ࡴࡓࡧࡶࡹࡱࡺࡳࠨᓌ"),bstack11l1l11_opy_ (u"ࠬ࠭ᓍ"))
      self.bstack1l111ll11_opy_ = scripts.get(bstack11l1l11_opy_ (u"࠭ࡧࡦࡶࡕࡩࡸࡻ࡬ࡵࡵࡖࡹࡲࡳࡡࡳࡻࠪᓎ"),bstack11l1l11_opy_ (u"ࠧࠨᓏ"))
      self.bstack1l111ll11l1_opy_ = scripts.get(bstack11l1l11_opy_ (u"ࠨࡵࡤࡺࡪࡘࡥࡴࡷ࡯ࡸࡸ࠭ᓐ"),bstack11l1l11_opy_ (u"ࠩࠪᓑ"))
  def bstack1l111ll1ll1_opy_(self, commands_to_wrap):
    if commands_to_wrap != None and len(commands_to_wrap) != 0:
      self.commands_to_wrap = commands_to_wrap
  def store(self):
    try:
      with open(self.bstack1l111ll1lll_opy_, bstack11l1l11_opy_ (u"ࠪࡻࠬᓒ")) as file:
        json.dump({
          bstack11l1l11_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࡸࠨᓓ"): self.commands_to_wrap,
          bstack11l1l11_opy_ (u"ࠧࡹࡣࡳ࡫ࡳࡸࡸࠨᓔ"): {
            bstack11l1l11_opy_ (u"ࠨࡳࡤࡣࡱࠦᓕ"): self.perform_scan,
            bstack11l1l11_opy_ (u"ࠢࡨࡧࡷࡖࡪࡹࡵ࡭ࡶࡶࠦᓖ"): self.bstack11l1lll11l_opy_,
            bstack11l1l11_opy_ (u"ࠣࡩࡨࡸࡗ࡫ࡳࡶ࡮ࡷࡷࡘࡻ࡭࡮ࡣࡵࡽࠧᓗ"): self.bstack1l111ll11_opy_,
            bstack11l1l11_opy_ (u"ࠤࡶࡥࡻ࡫ࡒࡦࡵࡸࡰࡹࡹࠢᓘ"): self.bstack1l111ll11l1_opy_
          }
        }, file)
    except Exception as e:
      logger.error(bstack11l1l11_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡࡵࡷࡳࡷ࡯࡮ࡨࠢࡦࡳࡲࡳࡡ࡯ࡦࡶ࠾ࠥࢁࡽࠣᓙ").format(e))
      pass
  def bstack11ll111111_opy_(self, bstack1ll1l1ll111_opy_):
    try:
      return any(command.get(bstack11l1l11_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᓚ")) == bstack1ll1l1ll111_opy_ for command in self.commands_to_wrap)
    except:
      return False
bstack11ll1lll1l_opy_ = bstack1l111ll11ll_opy_()
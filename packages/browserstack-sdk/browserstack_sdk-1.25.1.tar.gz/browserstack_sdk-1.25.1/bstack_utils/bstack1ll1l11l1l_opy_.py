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
from bstack_utils.bstack1l1ll1111l_opy_ import get_logger
logger = get_logger(__name__)
class bstack11lll1lll11_opy_(object):
  bstack1l1llll1_opy_ = os.path.join(os.path.expanduser(bstack1ll1l1_opy_ (u"ࠧࡿࠩᘭ")), bstack1ll1l1_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨᘮ"))
  bstack11lll1ll1ll_opy_ = os.path.join(bstack1l1llll1_opy_, bstack1ll1l1_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࡶ࠲࡯ࡹ࡯࡯ࠩᘯ"))
  commands_to_wrap = None
  perform_scan = None
  bstack1ll11l1ll1_opy_ = None
  bstack1l111l1lll_opy_ = None
  bstack11llll1lll1_opy_ = None
  def __new__(cls):
    if not hasattr(cls, bstack1ll1l1_opy_ (u"ࠪ࡭ࡳࡹࡴࡢࡰࡦࡩࠬᘰ")):
      cls.instance = super(bstack11lll1lll11_opy_, cls).__new__(cls)
      cls.instance.bstack11lll1ll1l1_opy_()
    return cls.instance
  def bstack11lll1ll1l1_opy_(self):
    try:
      with open(self.bstack11lll1ll1ll_opy_, bstack1ll1l1_opy_ (u"ࠫࡷ࠭ᘱ")) as bstack11ll11llll_opy_:
        bstack11lll1ll11l_opy_ = bstack11ll11llll_opy_.read()
        data = json.loads(bstack11lll1ll11l_opy_)
        if bstack1ll1l1_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩࡹࠧᘲ") in data:
          self.bstack11llll1llll_opy_(data[bstack1ll1l1_opy_ (u"࠭ࡣࡰ࡯ࡰࡥࡳࡪࡳࠨᘳ")])
        if bstack1ll1l1_opy_ (u"ࠧࡴࡥࡵ࡭ࡵࡺࡳࠨᘴ") in data:
          self.bstack11llllll1_opy_(data[bstack1ll1l1_opy_ (u"ࠨࡵࡦࡶ࡮ࡶࡴࡴࠩᘵ")])
    except:
      pass
  def bstack11llllll1_opy_(self, scripts):
    if scripts != None:
      self.perform_scan = scripts.get(bstack1ll1l1_opy_ (u"ࠩࡶࡧࡦࡴࠧᘶ"),bstack1ll1l1_opy_ (u"ࠪࠫᘷ"))
      self.bstack1ll11l1ll1_opy_ = scripts.get(bstack1ll1l1_opy_ (u"ࠫ࡬࡫ࡴࡓࡧࡶࡹࡱࡺࡳࠨᘸ"),bstack1ll1l1_opy_ (u"ࠬ࠭ᘹ"))
      self.bstack1l111l1lll_opy_ = scripts.get(bstack1ll1l1_opy_ (u"࠭ࡧࡦࡶࡕࡩࡸࡻ࡬ࡵࡵࡖࡹࡲࡳࡡࡳࡻࠪᘺ"),bstack1ll1l1_opy_ (u"ࠧࠨᘻ"))
      self.bstack11llll1lll1_opy_ = scripts.get(bstack1ll1l1_opy_ (u"ࠨࡵࡤࡺࡪࡘࡥࡴࡷ࡯ࡸࡸ࠭ᘼ"),bstack1ll1l1_opy_ (u"ࠩࠪᘽ"))
  def bstack11llll1llll_opy_(self, commands_to_wrap):
    if commands_to_wrap != None and len(commands_to_wrap) != 0:
      self.commands_to_wrap = commands_to_wrap
  def store(self):
    try:
      with open(self.bstack11lll1ll1ll_opy_, bstack1ll1l1_opy_ (u"ࠪࡻࠬᘾ")) as file:
        json.dump({
          bstack1ll1l1_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࡸࠨᘿ"): self.commands_to_wrap,
          bstack1ll1l1_opy_ (u"ࠧࡹࡣࡳ࡫ࡳࡸࡸࠨᙀ"): {
            bstack1ll1l1_opy_ (u"ࠨࡳࡤࡣࡱࠦᙁ"): self.perform_scan,
            bstack1ll1l1_opy_ (u"ࠢࡨࡧࡷࡖࡪࡹࡵ࡭ࡶࡶࠦᙂ"): self.bstack1ll11l1ll1_opy_,
            bstack1ll1l1_opy_ (u"ࠣࡩࡨࡸࡗ࡫ࡳࡶ࡮ࡷࡷࡘࡻ࡭࡮ࡣࡵࡽࠧᙃ"): self.bstack1l111l1lll_opy_,
            bstack1ll1l1_opy_ (u"ࠤࡶࡥࡻ࡫ࡒࡦࡵࡸࡰࡹࡹࠢᙄ"): self.bstack11llll1lll1_opy_
          }
        }, file)
    except Exception as e:
      logger.error(bstack1ll1l1_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡࡵࡷࡳࡷ࡯࡮ࡨࠢࡦࡳࡲࡳࡡ࡯ࡦࡶ࠾ࠥࢁࡽࠣᙅ").format(e))
      pass
  def bstack1ll1lll11l_opy_(self, bstack1ll1l1l11ll_opy_):
    try:
      return any(command.get(bstack1ll1l1_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᙆ")) == bstack1ll1l1l11ll_opy_ for command in self.commands_to_wrap)
    except:
      return False
bstack1ll1l11l1l_opy_ = bstack11lll1lll11_opy_()
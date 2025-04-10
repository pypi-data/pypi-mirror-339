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
import json
import multiprocessing
import os
from bstack_utils.config import Config
class bstack1l1111llll_opy_():
  def __init__(self, args, logger, bstack1111llll1l_opy_, bstack111l1111l1_opy_, bstack1111ll1ll1_opy_):
    self.args = args
    self.logger = logger
    self.bstack1111llll1l_opy_ = bstack1111llll1l_opy_
    self.bstack111l1111l1_opy_ = bstack111l1111l1_opy_
    self.bstack1111ll1ll1_opy_ = bstack1111ll1ll1_opy_
  def bstack11ll11ll1_opy_(self, bstack111l1111ll_opy_, bstack1l1lll111_opy_, bstack1111ll1l1l_opy_=False):
    bstack1ll11ll111_opy_ = []
    manager = multiprocessing.Manager()
    bstack1111llllll_opy_ = manager.list()
    bstack11ll11ll_opy_ = Config.bstack1l11l1l1ll_opy_()
    if bstack1111ll1l1l_opy_:
      for index, platform in enumerate(self.bstack1111llll1l_opy_[bstack1ll1l1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩစ")]):
        if index == 0:
          bstack1l1lll111_opy_[bstack1ll1l1_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪဆ")] = self.args
        bstack1ll11ll111_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack111l1111ll_opy_,
                                                    args=(bstack1l1lll111_opy_, bstack1111llllll_opy_)))
    else:
      for index, platform in enumerate(self.bstack1111llll1l_opy_[bstack1ll1l1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫဇ")]):
        bstack1ll11ll111_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack111l1111ll_opy_,
                                                    args=(bstack1l1lll111_opy_, bstack1111llllll_opy_)))
    i = 0
    for t in bstack1ll11ll111_opy_:
      try:
        if bstack11ll11ll_opy_.get_property(bstack1ll1l1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡶࡩࡸࡹࡩࡰࡰࠪဈ")):
          os.environ[bstack1ll1l1_opy_ (u"ࠪࡇ࡚ࡘࡒࡆࡐࡗࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡄࡂࡖࡄࠫဉ")] = json.dumps(self.bstack1111llll1l_opy_[bstack1ll1l1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧည")][i % self.bstack1111ll1ll1_opy_])
      except Exception as e:
        self.logger.debug(bstack1ll1l1_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡷࡹࡵࡲࡪࡰࡪࠤࡨࡻࡲࡳࡧࡱࡸࠥࡶ࡬ࡢࡶࡩࡳࡷࡳࠠࡥࡧࡷࡥ࡮ࡲࡳ࠻ࠢࡾࢁࠧဋ").format(str(e)))
      i += 1
      t.start()
    for t in bstack1ll11ll111_opy_:
      t.join()
    return list(bstack1111llllll_opy_)
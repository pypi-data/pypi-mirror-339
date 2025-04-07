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
import json
import multiprocessing
import os
from bstack_utils.config import Config
class bstack111l1l111_opy_():
  def __init__(self, args, logger, bstack111l1111l1_opy_, bstack111l11l111_opy_, bstack1111lll111_opy_):
    self.args = args
    self.logger = logger
    self.bstack111l1111l1_opy_ = bstack111l1111l1_opy_
    self.bstack111l11l111_opy_ = bstack111l11l111_opy_
    self.bstack1111lll111_opy_ = bstack1111lll111_opy_
  def bstack1l1ll1l1_opy_(self, bstack111l111111_opy_, bstack11llll111l_opy_, bstack1111lll11l_opy_=False):
    bstack1ll1ll1lll_opy_ = []
    manager = multiprocessing.Manager()
    bstack111l11l1ll_opy_ = manager.list()
    bstack111ll1lll_opy_ = Config.bstack111l1l1l_opy_()
    if bstack1111lll11l_opy_:
      for index, platform in enumerate(self.bstack111l1111l1_opy_[bstack11l1l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧဃ")]):
        if index == 0:
          bstack11llll111l_opy_[bstack11l1l11_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨင")] = self.args
        bstack1ll1ll1lll_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack111l111111_opy_,
                                                    args=(bstack11llll111l_opy_, bstack111l11l1ll_opy_)))
    else:
      for index, platform in enumerate(self.bstack111l1111l1_opy_[bstack11l1l11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩစ")]):
        bstack1ll1ll1lll_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack111l111111_opy_,
                                                    args=(bstack11llll111l_opy_, bstack111l11l1ll_opy_)))
    i = 0
    for t in bstack1ll1ll1lll_opy_:
      try:
        if bstack111ll1lll_opy_.get_property(bstack11l1l11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠨဆ")):
          os.environ[bstack11l1l11_opy_ (u"ࠨࡅࡘࡖࡗࡋࡎࡕࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡉࡇࡔࡂࠩဇ")] = json.dumps(self.bstack111l1111l1_opy_[bstack11l1l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬဈ")][i % self.bstack1111lll111_opy_])
      except Exception as e:
        self.logger.debug(bstack11l1l11_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡࡵࡷࡳࡷ࡯࡮ࡨࠢࡦࡹࡷࡸࡥ࡯ࡶࠣࡴࡱࡧࡴࡧࡱࡵࡱࠥࡪࡥࡵࡣ࡬ࡰࡸࡀࠠࡼࡿࠥဉ").format(str(e)))
      i += 1
      t.start()
    for t in bstack1ll1ll1lll_opy_:
      t.join()
    return list(bstack111l11l1ll_opy_)
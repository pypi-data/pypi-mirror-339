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
class RobotHandler():
    def __init__(self, args, logger, bstack111l1111l1_opy_, bstack111l11l111_opy_):
        self.args = args
        self.logger = logger
        self.bstack111l1111l1_opy_ = bstack111l1111l1_opy_
        self.bstack111l11l111_opy_ = bstack111l11l111_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack111l1l111l_opy_(bstack1111ll1l1l_opy_):
        bstack1111ll1ll1_opy_ = []
        if bstack1111ll1l1l_opy_:
            tokens = str(os.path.basename(bstack1111ll1l1l_opy_)).split(bstack11l1l11_opy_ (u"ࠦࡤࠨည"))
            camelcase_name = bstack11l1l11_opy_ (u"ࠧࠦࠢဋ").join(t.title() for t in tokens)
            suite_name, bstack1111ll1l11_opy_ = os.path.splitext(camelcase_name)
            bstack1111ll1ll1_opy_.append(suite_name)
        return bstack1111ll1ll1_opy_
    @staticmethod
    def bstack1111ll1lll_opy_(typename):
        if bstack11l1l11_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࠤဌ") in typename:
            return bstack11l1l11_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࡈࡶࡷࡵࡲࠣဍ")
        return bstack11l1l11_opy_ (u"ࠣࡗࡱ࡬ࡦࡴࡤ࡭ࡧࡧࡉࡷࡸ࡯ࡳࠤဎ")
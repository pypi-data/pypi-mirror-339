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
class RobotHandler():
    def __init__(self, args, logger, bstack1111llll1l_opy_, bstack111l1111l1_opy_):
        self.args = args
        self.logger = logger
        self.bstack1111llll1l_opy_ = bstack1111llll1l_opy_
        self.bstack111l1111l1_opy_ = bstack111l1111l1_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack111l1l1l1l_opy_(bstack1111ll111l_opy_):
        bstack1111ll11l1_opy_ = []
        if bstack1111ll111l_opy_:
            tokens = str(os.path.basename(bstack1111ll111l_opy_)).split(bstack1ll1l1_opy_ (u"ࠨ࡟ࠣဌ"))
            camelcase_name = bstack1ll1l1_opy_ (u"ࠢࠡࠤဍ").join(t.title() for t in tokens)
            suite_name, bstack1111ll11ll_opy_ = os.path.splitext(camelcase_name)
            bstack1111ll11l1_opy_.append(suite_name)
        return bstack1111ll11l1_opy_
    @staticmethod
    def bstack1111ll1l11_opy_(typename):
        if bstack1ll1l1_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࠦဎ") in typename:
            return bstack1ll1l1_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࡊࡸࡲࡰࡴࠥဏ")
        return bstack1ll1l1_opy_ (u"࡙ࠥࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡋࡲࡳࡱࡵࠦတ")
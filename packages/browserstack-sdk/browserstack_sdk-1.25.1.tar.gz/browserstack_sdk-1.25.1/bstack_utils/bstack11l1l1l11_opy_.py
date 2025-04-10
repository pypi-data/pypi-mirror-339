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
from time import sleep
from datetime import datetime
from urllib.parse import urlencode
from bstack_utils.bstack11lll1ll111_opy_ import bstack11lll1l11ll_opy_
from bstack_utils.constants import *
import json
class bstack1l1l1ll11l_opy_:
    def __init__(self, bstack1llll1ll11_opy_, bstack11lll1l1111_opy_):
        self.bstack1llll1ll11_opy_ = bstack1llll1ll11_opy_
        self.bstack11lll1l1111_opy_ = bstack11lll1l1111_opy_
        self.bstack11lll1l1l11_opy_ = None
    def __call__(self):
        bstack11lll1l1l1l_opy_ = {}
        while True:
            self.bstack11lll1l1l11_opy_ = bstack11lll1l1l1l_opy_.get(
                bstack1ll1l1_opy_ (u"ࠬࡴࡥࡹࡶࡢࡴࡴࡲ࡬ࡠࡶ࡬ࡱࡪ࠭ᙇ"),
                int(datetime.now().timestamp() * 1000)
            )
            bstack11lll1l1ll1_opy_ = self.bstack11lll1l1l11_opy_ - int(datetime.now().timestamp() * 1000)
            if bstack11lll1l1ll1_opy_ > 0:
                sleep(bstack11lll1l1ll1_opy_ / 1000)
            params = {
                bstack1ll1l1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᙈ"): self.bstack1llll1ll11_opy_,
                bstack1ll1l1_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪᙉ"): int(datetime.now().timestamp() * 1000)
            }
            bstack11lll1l111l_opy_ = bstack1ll1l1_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࠥᙊ") + bstack11lll1l1lll_opy_ + bstack1ll1l1_opy_ (u"ࠤ࠲ࡥࡺࡺ࡯࡮ࡣࡷࡩ࠴ࡧࡰࡪ࠱ࡹ࠵࠴ࠨᙋ")
            if self.bstack11lll1l1111_opy_.lower() == bstack1ll1l1_opy_ (u"ࠥࡶࡪࡹࡵ࡭ࡶࡶࠦᙌ"):
                bstack11lll1l1l1l_opy_ = bstack11lll1l11ll_opy_.results(bstack11lll1l111l_opy_, params)
            else:
                bstack11lll1l1l1l_opy_ = bstack11lll1l11ll_opy_.bstack11lll1l11l1_opy_(bstack11lll1l111l_opy_, params)
            if str(bstack11lll1l1l1l_opy_.get(bstack1ll1l1_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫᙍ"), bstack1ll1l1_opy_ (u"ࠬ࠸࠰࠱ࠩᙎ"))) != bstack1ll1l1_opy_ (u"࠭࠴࠱࠶ࠪᙏ"):
                break
        return bstack11lll1l1l1l_opy_.get(bstack1ll1l1_opy_ (u"ࠧࡥࡣࡷࡥࠬᙐ"), bstack11lll1l1l1l_opy_)
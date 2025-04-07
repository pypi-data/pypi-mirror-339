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
from time import sleep
from datetime import datetime
from urllib.parse import urlencode
from bstack_utils.bstack1l11111ll11_opy_ import bstack1l11111ll1l_opy_
from bstack_utils.constants import *
import json
class bstack1l1l111l11_opy_:
    def __init__(self, bstack1111l1ll_opy_, bstack1l1111l1111_opy_):
        self.bstack1111l1ll_opy_ = bstack1111l1ll_opy_
        self.bstack1l1111l1111_opy_ = bstack1l1111l1111_opy_
        self.bstack1l11111l1l1_opy_ = None
    def __call__(self):
        bstack1l1111l11l1_opy_ = {}
        while True:
            self.bstack1l11111l1l1_opy_ = bstack1l1111l11l1_opy_.get(
                bstack11l1l11_opy_ (u"ࠩࡱࡩࡽࡺ࡟ࡱࡱ࡯ࡰࡤࡺࡩ࡮ࡧࠪᖸ"),
                int(datetime.now().timestamp() * 1000)
            )
            bstack1l11111llll_opy_ = self.bstack1l11111l1l1_opy_ - int(datetime.now().timestamp() * 1000)
            if bstack1l11111llll_opy_ > 0:
                sleep(bstack1l11111llll_opy_ / 1000)
            params = {
                bstack11l1l11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᖹ"): self.bstack1111l1ll_opy_,
                bstack11l1l11_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧᖺ"): int(datetime.now().timestamp() * 1000)
            }
            bstack1l1111l111l_opy_ = bstack11l1l11_opy_ (u"ࠧ࡮ࡴࡵࡲࡶ࠾࠴࠵ࠢᖻ") + bstack1l11111lll1_opy_ + bstack11l1l11_opy_ (u"ࠨ࠯ࡢࡷࡷࡳࡲࡧࡴࡦ࠱ࡤࡴ࡮࠵ࡶ࠲࠱ࠥᖼ")
            if self.bstack1l1111l1111_opy_.lower() == bstack11l1l11_opy_ (u"ࠢࡳࡧࡶࡹࡱࡺࡳࠣᖽ"):
                bstack1l1111l11l1_opy_ = bstack1l11111ll1l_opy_.results(bstack1l1111l111l_opy_, params)
            else:
                bstack1l1111l11l1_opy_ = bstack1l11111ll1l_opy_.bstack1l11111l1ll_opy_(bstack1l1111l111l_opy_, params)
            if str(bstack1l1111l11l1_opy_.get(bstack11l1l11_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨᖾ"), bstack11l1l11_opy_ (u"ࠩ࠵࠴࠵࠭ᖿ"))) != bstack11l1l11_opy_ (u"ࠪ࠸࠵࠺ࠧᗀ"):
                break
        return bstack1l1111l11l1_opy_.get(bstack11l1l11_opy_ (u"ࠫࡩࡧࡴࡢࠩᗁ"), bstack1l1111l11l1_opy_)
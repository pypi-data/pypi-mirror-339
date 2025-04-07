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
import logging
import abc
from browserstack_sdk.sdk_cli.bstack1111l1llll_opy_ import bstack1111l1lll1_opy_
class bstack1lllll1l111_opy_(abc.ABC):
    bin_session_id: str
    bstack1111l1llll_opy_: bstack1111l1lll1_opy_
    def __init__(self):
        self.bstack1lll11lll1l_opy_ = None
        self.config = None
        self.bin_session_id = None
        self.bstack1111l1llll_opy_ = None
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
    def bstack1llll111l11_opy_(self):
        return (self.bstack1lll11lll1l_opy_ != None and self.bin_session_id != None and self.bstack1111l1llll_opy_ != None)
    def configure(self, bstack1lll11lll1l_opy_, config, bin_session_id: str, bstack1111l1llll_opy_: bstack1111l1lll1_opy_):
        self.bstack1lll11lll1l_opy_ = bstack1lll11lll1l_opy_
        self.config = config
        self.bin_session_id = bin_session_id
        self.bstack1111l1llll_opy_ = bstack1111l1llll_opy_
        if self.bin_session_id:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠣ࡝ࡾ࡭ࡩ࠮ࡳࡦ࡮ࡩ࠭ࢂࡣࠠࡤࡱࡱࡪ࡮࡭ࡵࡳࡧࡧࠤࡲࡵࡤࡶ࡮ࡨࠤࢀࡹࡥ࡭ࡨ࠱ࡣࡤࡩ࡬ࡢࡵࡶࡣࡤ࠴࡟ࡠࡰࡤࡱࡪࡥ࡟ࡾ࠼ࠣࡦ࡮ࡴ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧࡁࠧᆝ") + str(self.bin_session_id) + bstack11l1l11_opy_ (u"ࠤࠥᆞ"))
    def bstack1ll1l1111l1_opy_(self):
        if not self.bin_session_id:
            raise ValueError(bstack11l1l11_opy_ (u"ࠥࡦ࡮ࡴ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧࠤࡨࡧ࡮࡯ࡱࡷࠤࡧ࡫ࠠࡏࡱࡱࡩࠧᆟ"))
    @abc.abstractmethod
    def is_enabled(self) -> bool:
        return False
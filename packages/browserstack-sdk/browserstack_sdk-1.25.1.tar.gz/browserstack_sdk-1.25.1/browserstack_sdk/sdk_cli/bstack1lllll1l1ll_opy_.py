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
import logging
import abc
from browserstack_sdk.sdk_cli.bstack1111l1ll11_opy_ import bstack1111l1llll_opy_
class bstack1lll1llll11_opy_(abc.ABC):
    bin_session_id: str
    bstack1111l1ll11_opy_: bstack1111l1llll_opy_
    def __init__(self):
        self.bstack1llllll1ll1_opy_ = None
        self.config = None
        self.bin_session_id = None
        self.bstack1111l1ll11_opy_ = None
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
    def bstack1llll1lll11_opy_(self):
        return (self.bstack1llllll1ll1_opy_ != None and self.bin_session_id != None and self.bstack1111l1ll11_opy_ != None)
    def configure(self, bstack1llllll1ll1_opy_, config, bin_session_id: str, bstack1111l1ll11_opy_: bstack1111l1llll_opy_):
        self.bstack1llllll1ll1_opy_ = bstack1llllll1ll1_opy_
        self.config = config
        self.bin_session_id = bin_session_id
        self.bstack1111l1ll11_opy_ = bstack1111l1ll11_opy_
        if self.bin_session_id:
            self.logger.debug(bstack1ll1l1_opy_ (u"ࠥ࡟ࢀ࡯ࡤࠩࡵࡨࡰ࡫࠯ࡽ࡞ࠢࡦࡳࡳ࡬ࡩࡨࡷࡵࡩࡩࠦ࡭ࡰࡦࡸࡰࡪࠦࡻࡴࡧ࡯ࡪ࠳ࡥ࡟ࡤ࡮ࡤࡷࡸࡥ࡟࠯ࡡࡢࡲࡦࡳࡥࡠࡡࢀ࠾ࠥࡨࡩ࡯ࡡࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩࡃࠢᆟ") + str(self.bin_session_id) + bstack1ll1l1_opy_ (u"ࠦࠧᆠ"))
    def bstack1ll1l11ll11_opy_(self):
        if not self.bin_session_id:
            raise ValueError(bstack1ll1l1_opy_ (u"ࠧࡨࡩ࡯ࡡࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩࠦࡣࡢࡰࡱࡳࡹࠦࡢࡦࠢࡑࡳࡳ࡫ࠢᆡ"))
    @abc.abstractmethod
    def is_enabled(self) -> bool:
        return False
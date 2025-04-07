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
import threading
import logging
import bstack_utils.accessibility as bstack1l1l1l1ll1_opy_
from bstack_utils.helper import bstack1llllllll1_opy_
logger = logging.getLogger(__name__)
def bstack11lll11l1l_opy_(bstack11111l11l_opy_):
  return True if bstack11111l11l_opy_ in threading.current_thread().__dict__.keys() else False
def bstack1ll1l11111_opy_(context, *args):
    tags = getattr(args[0], bstack11l1l11_opy_ (u"ࠬࡺࡡࡨࡵࠪᗂ"), [])
    bstack11l11llll1_opy_ = bstack1l1l1l1ll1_opy_.bstack11lll111_opy_(tags)
    threading.current_thread().isA11yTest = bstack11l11llll1_opy_
    try:
      bstack1l1lll1l_opy_ = threading.current_thread().bstackSessionDriver if bstack11lll11l1l_opy_(bstack11l1l11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬᗃ")) else context.browser
      if bstack1l1lll1l_opy_ and bstack1l1lll1l_opy_.session_id and bstack11l11llll1_opy_ and bstack1llllllll1_opy_(
              threading.current_thread(), bstack11l1l11_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭ᗄ"), None):
          threading.current_thread().isA11yTest = bstack1l1l1l1ll1_opy_.bstack1l111l11l1_opy_(bstack1l1lll1l_opy_, bstack11l11llll1_opy_)
    except Exception as e:
       logger.debug(bstack11l1l11_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸࡺࡡࡳࡶࠣࡥ࠶࠷ࡹࠡ࡫ࡱࠤࡧ࡫ࡨࡢࡸࡨ࠾ࠥࢁࡽࠨᗅ").format(str(e)))
def bstack11111lll_opy_(bstack1l1lll1l_opy_):
    if bstack1llllllll1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"ࠩ࡬ࡷࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭ᗆ"), None) and bstack1llllllll1_opy_(
      threading.current_thread(), bstack11l1l11_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩᗇ"), None) and not bstack1llllllll1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"ࠫࡦ࠷࠱ࡺࡡࡶࡸࡴࡶࠧᗈ"), False):
      threading.current_thread().a11y_stop = True
      bstack1l1l1l1ll1_opy_.bstack1ll11111l_opy_(bstack1l1lll1l_opy_, name=bstack11l1l11_opy_ (u"ࠧࠨᗉ"), path=bstack11l1l11_opy_ (u"ࠨࠢᗊ"))
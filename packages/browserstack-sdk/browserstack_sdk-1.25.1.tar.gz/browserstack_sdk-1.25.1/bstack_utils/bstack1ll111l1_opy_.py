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
import threading
import logging
import bstack_utils.accessibility as bstack1l11llll_opy_
from bstack_utils.helper import bstack11111l111_opy_
logger = logging.getLogger(__name__)
def bstack1l111l11l1_opy_(bstack1ll111l11l_opy_):
  return True if bstack1ll111l11l_opy_ in threading.current_thread().__dict__.keys() else False
def bstack11l1llllll_opy_(context, *args):
    tags = getattr(args[0], bstack1ll1l1_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭ᙑ"), [])
    bstack1ll11ll1l1_opy_ = bstack1l11llll_opy_.bstack1ll11l1ll_opy_(tags)
    threading.current_thread().isA11yTest = bstack1ll11ll1l1_opy_
    try:
      bstack11llll1l1l_opy_ = threading.current_thread().bstackSessionDriver if bstack1l111l11l1_opy_(bstack1ll1l1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨᙒ")) else context.browser
      if bstack11llll1l1l_opy_ and bstack11llll1l1l_opy_.session_id and bstack1ll11ll1l1_opy_ and bstack11111l111_opy_(
              threading.current_thread(), bstack1ll1l1_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩᙓ"), None):
          threading.current_thread().isA11yTest = bstack1l11llll_opy_.bstack11llll11_opy_(bstack11llll1l1l_opy_, bstack1ll11ll1l1_opy_)
    except Exception as e:
       logger.debug(bstack1ll1l1_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡶࡤࡶࡹࠦࡡ࠲࠳ࡼࠤ࡮ࡴࠠࡣࡧ࡫ࡥࡻ࡫࠺ࠡࡽࢀࠫᙔ").format(str(e)))
def bstack1111111l1_opy_(bstack11llll1l1l_opy_):
    if bstack11111l111_opy_(threading.current_thread(), bstack1ll1l1_opy_ (u"ࠬ࡯ࡳࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩᙕ"), None) and bstack11111l111_opy_(
      threading.current_thread(), bstack1ll1l1_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬᙖ"), None) and not bstack11111l111_opy_(threading.current_thread(), bstack1ll1l1_opy_ (u"ࠧࡢ࠳࠴ࡽࡤࡹࡴࡰࡲࠪᙗ"), False):
      threading.current_thread().a11y_stop = True
      bstack1l11llll_opy_.bstack1111l1l11_opy_(bstack11llll1l1l_opy_, name=bstack1ll1l1_opy_ (u"ࠣࠤᙘ"), path=bstack1ll1l1_opy_ (u"ࠤࠥᙙ"))
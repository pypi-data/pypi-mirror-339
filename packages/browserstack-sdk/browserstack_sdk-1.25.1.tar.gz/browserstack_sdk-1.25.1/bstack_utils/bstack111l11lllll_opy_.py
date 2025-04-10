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
logger = logging.getLogger(__name__)
bstack111l1l11l11_opy_ = 1000
bstack111l11lll1l_opy_ = 2
class bstack111l1l1111l_opy_:
    def __init__(self, handler, bstack111l11lll11_opy_=bstack111l1l11l11_opy_, bstack111l1l111ll_opy_=bstack111l11lll1l_opy_):
        self.queue = []
        self.handler = handler
        self.bstack111l11lll11_opy_ = bstack111l11lll11_opy_
        self.bstack111l1l111ll_opy_ = bstack111l1l111ll_opy_
        self.lock = threading.Lock()
        self.timer = None
        self.bstack1111l1l1ll_opy_ = None
    def start(self):
        if not (self.timer and self.timer.is_alive()):
            self.bstack111l1l111l1_opy_()
    def bstack111l1l111l1_opy_(self):
        self.bstack1111l1l1ll_opy_ = threading.Event()
        def bstack111l1l11l1l_opy_():
            self.bstack1111l1l1ll_opy_.wait(self.bstack111l1l111ll_opy_)
            if not self.bstack1111l1l1ll_opy_.is_set():
                self.bstack111l11llll1_opy_()
        self.timer = threading.Thread(target=bstack111l1l11l1l_opy_, daemon=True)
        self.timer.start()
    def bstack111l1l11111_opy_(self):
        try:
            if self.bstack1111l1l1ll_opy_ and not self.bstack1111l1l1ll_opy_.is_set():
                self.bstack1111l1l1ll_opy_.set()
            if self.timer and self.timer.is_alive() and self.timer != threading.current_thread():
                self.timer.join()
        except Exception as e:
            logger.debug(bstack1ll1l1_opy_ (u"࡛࠭ࡴࡶࡲࡴࡤࡺࡩ࡮ࡧࡵࡡࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮࠻ࠢࠪᵝ") + (str(e) or bstack1ll1l1_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡧࡴࡻ࡬ࡥࠢࡱࡳࡹࠦࡢࡦࠢࡦࡳࡳࡼࡥࡳࡶࡨࡨࠥࡺ࡯ࠡࡵࡷࡶ࡮ࡴࡧࠣᵞ")))
        finally:
            self.timer = None
    def bstack111l11ll1ll_opy_(self):
        if self.timer:
            self.bstack111l1l11111_opy_()
        self.bstack111l1l111l1_opy_()
    def add(self, event):
        with self.lock:
            self.queue.append(event)
            if len(self.queue) >= self.bstack111l11lll11_opy_:
                threading.Thread(target=self.bstack111l11llll1_opy_).start()
    def bstack111l11llll1_opy_(self, source = bstack1ll1l1_opy_ (u"ࠨࠩᵟ")):
        with self.lock:
            if not self.queue:
                self.bstack111l11ll1ll_opy_()
                return
            data = self.queue[:self.bstack111l11lll11_opy_]
            del self.queue[:self.bstack111l11lll11_opy_]
        self.handler(data)
        if source != bstack1ll1l1_opy_ (u"ࠩࡶ࡬ࡺࡺࡤࡰࡹࡱࠫᵠ"):
            self.bstack111l11ll1ll_opy_()
    def shutdown(self):
        self.bstack111l1l11111_opy_()
        while self.queue:
            self.bstack111l11llll1_opy_(source=bstack1ll1l1_opy_ (u"ࠪࡷ࡭ࡻࡴࡥࡱࡺࡲࠬᵡ"))
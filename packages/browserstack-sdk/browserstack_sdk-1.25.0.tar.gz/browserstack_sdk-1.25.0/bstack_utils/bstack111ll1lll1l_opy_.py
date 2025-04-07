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
logger = logging.getLogger(__name__)
bstack111ll1llll1_opy_ = 1000
bstack111ll1l1ll1_opy_ = 2
class bstack111ll1ll111_opy_:
    def __init__(self, handler, bstack111ll1ll1l1_opy_=bstack111ll1llll1_opy_, bstack111ll1lll11_opy_=bstack111ll1l1ll1_opy_):
        self.queue = []
        self.handler = handler
        self.bstack111ll1ll1l1_opy_ = bstack111ll1ll1l1_opy_
        self.bstack111ll1lll11_opy_ = bstack111ll1lll11_opy_
        self.lock = threading.Lock()
        self.timer = None
        self.bstack1111ll111l_opy_ = None
    def start(self):
        if not (self.timer and self.timer.is_alive()):
            self.bstack111ll1ll11l_opy_()
    def bstack111ll1ll11l_opy_(self):
        self.bstack1111ll111l_opy_ = threading.Event()
        def bstack111ll1l1lll_opy_():
            self.bstack1111ll111l_opy_.wait(self.bstack111ll1lll11_opy_)
            if not self.bstack1111ll111l_opy_.is_set():
                self.bstack111ll1l1l11_opy_()
        self.timer = threading.Thread(target=bstack111ll1l1lll_opy_, daemon=True)
        self.timer.start()
    def bstack111ll1l1l1l_opy_(self):
        try:
            if self.bstack1111ll111l_opy_ and not self.bstack1111ll111l_opy_.is_set():
                self.bstack1111ll111l_opy_.set()
            if self.timer and self.timer.is_alive() and self.timer != threading.current_thread():
                self.timer.join()
        except Exception as e:
            logger.debug(bstack11l1l11_opy_ (u"ࠪ࡟ࡸࡺ࡯ࡱࡡࡷ࡭ࡲ࡫ࡲ࡞ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲ࠿ࠦࠧ᳎") + (str(e) or bstack11l1l11_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡤࡱࡸࡰࡩࠦ࡮ࡰࡶࠣࡦࡪࠦࡣࡰࡰࡹࡩࡷࡺࡥࡥࠢࡷࡳࠥࡹࡴࡳ࡫ࡱ࡫ࠧ᳏")))
        finally:
            self.timer = None
    def bstack111ll1ll1ll_opy_(self):
        if self.timer:
            self.bstack111ll1l1l1l_opy_()
        self.bstack111ll1ll11l_opy_()
    def add(self, event):
        with self.lock:
            self.queue.append(event)
            if len(self.queue) >= self.bstack111ll1ll1l1_opy_:
                threading.Thread(target=self.bstack111ll1l1l11_opy_).start()
    def bstack111ll1l1l11_opy_(self, source = bstack11l1l11_opy_ (u"ࠬ࠭᳐")):
        with self.lock:
            if not self.queue:
                self.bstack111ll1ll1ll_opy_()
                return
            data = self.queue[:self.bstack111ll1ll1l1_opy_]
            del self.queue[:self.bstack111ll1ll1l1_opy_]
        self.handler(data)
        if source != bstack11l1l11_opy_ (u"࠭ࡳࡩࡷࡷࡨࡴࡽ࡮ࠨ᳑"):
            self.bstack111ll1ll1ll_opy_()
    def shutdown(self):
        self.bstack111ll1l1l1l_opy_()
        while self.queue:
            self.bstack111ll1l1l11_opy_(source=bstack11l1l11_opy_ (u"ࠧࡴࡪࡸࡸࡩࡵࡷ࡯ࠩ᳒"))
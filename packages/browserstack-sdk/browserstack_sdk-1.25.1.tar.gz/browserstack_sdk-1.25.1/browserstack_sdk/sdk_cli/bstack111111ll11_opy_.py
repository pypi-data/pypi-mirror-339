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
import threading
import os
from typing import Dict, Any
from dataclasses import dataclass
from collections import defaultdict
from datetime import timedelta
@dataclass
class bstack111111l1l1_opy_:
    id: str
    hash: str
    thread_id: int
    process_id: int
    type: str
class bstack11111111l1_opy_:
    bstack1l1111ll1l1_opy_ = bstack1ll1l1_opy_ (u"ࠦࡧ࡫࡮ࡤࡪࡰࡥࡷࡱࠢᔙ")
    context: bstack111111l1l1_opy_
    data: Dict[str, Any]
    platform_index: int
    def __init__(self, context: bstack111111l1l1_opy_):
        self.context = context
        self.data = dict({bstack11111111l1_opy_.bstack1l1111ll1l1_opy_: defaultdict(lambda: timedelta(microseconds=0))})
        self.platform_index = int(os.environ.get(bstack1ll1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬᔚ"), bstack1ll1l1_opy_ (u"࠭࠰ࠨᔛ")))
    def ref(self) -> str:
        return str(self.context.id)
    def bstack1lllllllll1_opy_(self, target: object):
        return bstack11111111l1_opy_.create_context(target) == self.context
    def bstack1ll11l1llll_opy_(self, context: bstack111111l1l1_opy_):
        return context and context.thread_id == self.context.thread_id and context.process_id == self.context.process_id
    def bstack11lll1l111_opy_(self, key: str, value: timedelta):
        self.data[bstack11111111l1_opy_.bstack1l1111ll1l1_opy_][key] += value
    def bstack1llll11l11l_opy_(self) -> dict:
        return self.data[bstack11111111l1_opy_.bstack1l1111ll1l1_opy_]
    @staticmethod
    def create_context(
        target: object,
        thread_id=threading.get_ident(),
        process_id=os.getpid(),
    ):
        return bstack111111l1l1_opy_(
            id=hash(target),
            hash=hash(target),
            thread_id=thread_id,
            process_id=process_id,
            type=target,
        )
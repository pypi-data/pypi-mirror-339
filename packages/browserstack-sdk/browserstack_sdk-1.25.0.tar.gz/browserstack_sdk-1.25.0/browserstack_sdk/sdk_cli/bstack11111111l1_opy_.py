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
import os
import threading
import os
from typing import Dict, Any
from dataclasses import dataclass
from collections import defaultdict
from datetime import timedelta
@dataclass
class bstack11111l1111_opy_:
    id: str
    hash: str
    thread_id: int
    process_id: int
    type: str
class bstack11111ll11l_opy_:
    bstack1l111lll111_opy_ = bstack11l1l11_opy_ (u"ࠦࡧ࡫࡮ࡤࡪࡰࡥࡷࡱࠢᒾ")
    context: bstack11111l1111_opy_
    data: Dict[str, Any]
    platform_index: int
    def __init__(self, context: bstack11111l1111_opy_):
        self.context = context
        self.data = dict({bstack11111ll11l_opy_.bstack1l111lll111_opy_: defaultdict(lambda: timedelta(microseconds=0))})
        self.platform_index = int(os.environ.get(bstack11l1l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬᒿ"), bstack11l1l11_opy_ (u"࠭࠰ࠨᓀ")))
    def ref(self) -> str:
        return str(self.context.id)
    def bstack111111l11l_opy_(self, target: object):
        return bstack11111ll11l_opy_.create_context(target) == self.context
    def bstack1ll11l1ll1l_opy_(self, context: bstack11111l1111_opy_):
        return context and context.thread_id == self.context.thread_id and context.process_id == self.context.process_id
    def bstack1ll11lll_opy_(self, key: str, value: timedelta):
        self.data[bstack11111ll11l_opy_.bstack1l111lll111_opy_][key] += value
    def bstack1lll1l11l1l_opy_(self) -> dict:
        return self.data[bstack11111ll11l_opy_.bstack1l111lll111_opy_]
    @staticmethod
    def create_context(
        target: object,
        thread_id=threading.get_ident(),
        process_id=os.getpid(),
    ):
        return bstack11111l1111_opy_(
            id=hash(target),
            hash=hash(target),
            thread_id=thread_id,
            process_id=process_id,
            type=target,
        )
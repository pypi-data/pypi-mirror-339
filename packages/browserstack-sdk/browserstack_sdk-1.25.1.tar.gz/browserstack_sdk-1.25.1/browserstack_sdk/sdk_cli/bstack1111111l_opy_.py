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
from collections import defaultdict
from threading import Lock
from dataclasses import dataclass
import logging
import traceback
from typing import List, Dict, Any
import os
@dataclass
class bstack11l1lll11_opy_:
    sdk_version: str
    path_config: str
    path_project: str
    test_framework: str
    frameworks: List[str]
    framework_versions: Dict[str, str]
    bs_config: Dict[str, Any]
@dataclass
class bstack11111111l_opy_:
    pass
class bstack1l1111ll1l_opy_:
    bstack111l1111_opy_ = bstack1ll1l1_opy_ (u"ࠤࡥࡳࡴࡺࡳࡵࡴࡤࡴࠧს")
    CONNECT = bstack1ll1l1_opy_ (u"ࠥࡧࡴࡴ࡮ࡦࡥࡷࠦტ")
    bstack1lll11l1l_opy_ = bstack1ll1l1_opy_ (u"ࠦࡸ࡮ࡵࡵࡦࡲࡻࡳࠨუ")
    CONFIG = bstack1ll1l1_opy_ (u"ࠧࡩ࡯࡯ࡨ࡬࡫ࠧფ")
    bstack1ll1lll11ll_opy_ = bstack1ll1l1_opy_ (u"ࠨࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡵࠥქ")
    bstack11l111111_opy_ = bstack1ll1l1_opy_ (u"ࠢࡦࡺ࡬ࡸࠧღ")
class bstack1ll1lll1ll1_opy_:
    bstack1ll1lll1lll_opy_ = bstack1ll1l1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡴࡶࡤࡶࡹ࡫ࡤࠣყ")
    FINISHED = bstack1ll1l1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡨ࡬ࡲ࡮ࡹࡨࡦࡦࠥშ")
class bstack1ll1lll11l1_opy_:
    bstack1ll1lll1lll_opy_ = bstack1ll1l1_opy_ (u"ࠥࡸࡪࡹࡴࡠࡴࡸࡲࡤࡹࡴࡢࡴࡷࡩࡩࠨჩ")
    FINISHED = bstack1ll1l1_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡦࡪࡰ࡬ࡷ࡭࡫ࡤࠣც")
class bstack1ll1llll11l_opy_:
    bstack1ll1lll1lll_opy_ = bstack1ll1l1_opy_ (u"ࠧ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡴࡶࡤࡶࡹ࡫ࡤࠣძ")
    FINISHED = bstack1ll1l1_opy_ (u"ࠨࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡨ࡬ࡲ࡮ࡹࡨࡦࡦࠥწ")
class bstack1ll1lll1l11_opy_:
    bstack1ll1lll1l1l_opy_ = bstack1ll1l1_opy_ (u"ࠢࡤࡤࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤࡩࡲࡦࡣࡷࡩࡩࠨჭ")
class bstack1ll1llll111_opy_:
    _1lll111l1l1_opy_ = None
    def __new__(cls):
        if not cls._1lll111l1l1_opy_:
            cls._1lll111l1l1_opy_ = super(bstack1ll1llll111_opy_, cls).__new__(cls)
        return cls._1lll111l1l1_opy_
    def __init__(self):
        self._hooks = defaultdict(lambda: defaultdict(list))
        self._lock = Lock()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
    def clear(self):
        with self._lock:
            self._hooks = defaultdict(list)
    def register(self, event_name, callback):
        with self._lock:
            if not callable(callback):
                raise ValueError(bstack1ll1l1_opy_ (u"ࠣࡅࡤࡰࡱࡨࡡࡤ࡭ࠣࡱࡺࡹࡴࠡࡤࡨࠤࡨࡧ࡬࡭ࡣࡥࡰࡪࠦࡦࡰࡴࠣࠦხ") + event_name)
            pid = os.getpid()
            self.logger.debug(bstack1ll1l1_opy_ (u"ࠤࡕࡩ࡬࡯ࡳࡵࡧࡵ࡭ࡳ࡭ࠠࡤࡣ࡯ࡰࡧࡧࡣ࡬ࠢࡩࡳࡷࠦࡥࡷࡧࡱࡸࠥ࠭ࡻࡦࡸࡨࡲࡹࡥ࡮ࡢ࡯ࡨࢁࠬࠦࡷࡪࡶ࡫ࠤࡵ࡯ࡤࠡࠤჯ") + str(pid) + bstack1ll1l1_opy_ (u"ࠥࠦჰ"))
            self._hooks[event_name][pid].append(callback)
    def invoke(self, event_name, *args, **kwargs):
        with self._lock:
            pid = os.getpid()
            callbacks = self._hooks.get(event_name, {}).get(pid, [])
            if not callbacks:
                self.logger.warning(bstack1ll1l1_opy_ (u"ࠦࡓࡵࠠࡤࡣ࡯ࡰࡧࡧࡣ࡬ࡵࠣࡪࡴࡸࠠࡦࡸࡨࡲࡹࠦࠧࡼࡧࡹࡩࡳࡺ࡟࡯ࡣࡰࡩࢂ࠭ࠠࡸ࡫ࡷ࡬ࠥࡶࡩࡥࠢࠥჱ") + str(pid) + bstack1ll1l1_opy_ (u"ࠧࠨჲ"))
                return
            self.logger.debug(bstack1ll1l1_opy_ (u"ࠨࡉ࡯ࡸࡲ࡯࡮ࡴࡧࠡࡽ࡯ࡩࡳ࠮ࡣࡢ࡮࡯ࡦࡦࡩ࡫ࡴࠫࢀࠤࡨࡧ࡬࡭ࡤࡤࡧࡰࡹࠠࡧࡱࡵࠤࡪࡼࡥ࡯ࡶࠣࠫࢀ࡫ࡶࡦࡰࡷࡣࡳࡧ࡭ࡦࡿࠪࠤࡼ࡯ࡴࡩࠢࡳ࡭ࡩࠦࠢჳ") + str(pid) + bstack1ll1l1_opy_ (u"ࠢࠣჴ"))
            for callback in callbacks:
                try:
                    self.logger.debug(bstack1ll1l1_opy_ (u"ࠣࡋࡱࡺࡴࡱࡥࡥࠢࡦࡥࡱࡲࡢࡢࡥ࡮ࠤ࡫ࡵࡲࠡࡧࡹࡩࡳࡺࠠࠨࡽࡨࡺࡪࡴࡴࡠࡰࡤࡱࡪࢃࠧࠡࡹ࡬ࡸ࡭ࠦࡰࡪࡦࠣࠦჵ") + str(pid) + bstack1ll1l1_opy_ (u"ࠤࠥჶ"))
                    callback(event_name, *args, **kwargs)
                except Exception as e:
                    self.logger.error(bstack1ll1l1_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢ࡬ࡲࡻࡵ࡫ࡪࡰࡪࠤࡨࡧ࡬࡭ࡤࡤࡧࡰࠦࡦࡰࡴࠣࡩࡻ࡫࡮ࡵࠢࠪࡿࡪࡼࡥ࡯ࡶࡢࡲࡦࡳࡥࡾࠩࠣࡻ࡮ࡺࡨࠡࡲ࡬ࡨࠥࢁࡰࡪࡦࢀ࠾ࠥࠨჷ") + str(e) + bstack1ll1l1_opy_ (u"ࠦࠧჸ"))
                    traceback.print_exc()
bstack1111111l_opy_ = bstack1ll1llll111_opy_()
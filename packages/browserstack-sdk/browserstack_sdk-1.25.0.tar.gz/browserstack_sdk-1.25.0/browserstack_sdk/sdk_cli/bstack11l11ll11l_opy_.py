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
from collections import defaultdict
from threading import Lock
from dataclasses import dataclass
import logging
import traceback
from typing import List, Dict, Any
import os
@dataclass
class bstack1l1ll11ll_opy_:
    sdk_version: str
    path_config: str
    path_project: str
    test_framework: str
    frameworks: List[str]
    framework_versions: Dict[str, str]
    bs_config: Dict[str, Any]
@dataclass
class bstack111111ll1_opy_:
    pass
class bstack1llll111ll_opy_:
    bstack111l1ll1l_opy_ = bstack11l1l11_opy_ (u"ࠢࡣࡱࡲࡸࡸࡺࡲࡢࡲࠥჟ")
    CONNECT = bstack11l1l11_opy_ (u"ࠣࡥࡲࡲࡳ࡫ࡣࡵࠤრ")
    bstack1ll11111ll_opy_ = bstack11l1l11_opy_ (u"ࠤࡶ࡬ࡺࡺࡤࡰࡹࡱࠦს")
    CONFIG = bstack11l1l11_opy_ (u"ࠥࡧࡴࡴࡦࡪࡩࠥტ")
    bstack1ll1llll11l_opy_ = bstack11l1l11_opy_ (u"ࠦ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࡳࠣუ")
    bstack1l1llllll_opy_ = bstack11l1l11_opy_ (u"ࠧ࡫ࡸࡪࡶࠥფ")
class bstack1ll1lllll11_opy_:
    bstack1ll1llll1ll_opy_ = bstack11l1l11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡹࡴࡢࡴࡷࡩࡩࠨქ")
    FINISHED = bstack11l1l11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡦࡪࡰ࡬ࡷ࡭࡫ࡤࠣღ")
class bstack1ll1lllll1l_opy_:
    bstack1ll1llll1ll_opy_ = bstack11l1l11_opy_ (u"ࠣࡶࡨࡷࡹࡥࡲࡶࡰࡢࡷࡹࡧࡲࡵࡧࡧࠦყ")
    FINISHED = bstack11l1l11_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡳࡷࡱࡣ࡫࡯࡮ࡪࡵ࡫ࡩࡩࠨშ")
class bstack1ll1llll111_opy_:
    bstack1ll1llll1ll_opy_ = bstack11l1l11_opy_ (u"ࠥ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡹࡴࡢࡴࡷࡩࡩࠨჩ")
    FINISHED = bstack11l1l11_opy_ (u"ࠦ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡦࡪࡰ࡬ࡷ࡭࡫ࡤࠣც")
class bstack1ll1lll1lll_opy_:
    bstack1ll1llllll1_opy_ = bstack11l1l11_opy_ (u"ࠧࡩࡢࡵࡡࡶࡩࡸࡹࡩࡰࡰࡢࡧࡷ࡫ࡡࡵࡧࡧࠦძ")
class bstack1ll1llll1l1_opy_:
    _1lll1l1l11l_opy_ = None
    def __new__(cls):
        if not cls._1lll1l1l11l_opy_:
            cls._1lll1l1l11l_opy_ = super(bstack1ll1llll1l1_opy_, cls).__new__(cls)
        return cls._1lll1l1l11l_opy_
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
                raise ValueError(bstack11l1l11_opy_ (u"ࠨࡃࡢ࡮࡯ࡦࡦࡩ࡫ࠡ࡯ࡸࡷࡹࠦࡢࡦࠢࡦࡥࡱࡲࡡࡣ࡮ࡨࠤ࡫ࡵࡲࠡࠤწ") + event_name)
            pid = os.getpid()
            self.logger.debug(bstack11l1l11_opy_ (u"ࠢࡓࡧࡪ࡭ࡸࡺࡥࡳ࡫ࡱ࡫ࠥࡩࡡ࡭࡮ࡥࡥࡨࡱࠠࡧࡱࡵࠤࡪࡼࡥ࡯ࡶࠣࠫࢀ࡫ࡶࡦࡰࡷࡣࡳࡧ࡭ࡦࡿࠪࠤࡼ࡯ࡴࡩࠢࡳ࡭ࡩࠦࠢჭ") + str(pid) + bstack11l1l11_opy_ (u"ࠣࠤხ"))
            self._hooks[event_name][pid].append(callback)
    def invoke(self, event_name, *args, **kwargs):
        with self._lock:
            pid = os.getpid()
            callbacks = self._hooks.get(event_name, {}).get(pid, [])
            if not callbacks:
                self.logger.warning(bstack11l1l11_opy_ (u"ࠤࡑࡳࠥࡩࡡ࡭࡮ࡥࡥࡨࡱࡳࠡࡨࡲࡶࠥ࡫ࡶࡦࡰࡷࠤࠬࢁࡥࡷࡧࡱࡸࡤࡴࡡ࡮ࡧࢀࠫࠥࡽࡩࡵࡪࠣࡴ࡮ࡪࠠࠣჯ") + str(pid) + bstack11l1l11_opy_ (u"ࠥࠦჰ"))
                return
            self.logger.debug(bstack11l1l11_opy_ (u"ࠦࡎࡴࡶࡰ࡭࡬ࡲ࡬ࠦࡻ࡭ࡧࡱࠬࡨࡧ࡬࡭ࡤࡤࡧࡰࡹࠩࡾࠢࡦࡥࡱࡲࡢࡢࡥ࡮ࡷࠥ࡬࡯ࡳࠢࡨࡺࡪࡴࡴࠡࠩࡾࡩࡻ࡫࡮ࡵࡡࡱࡥࡲ࡫ࡽࠨࠢࡺ࡭ࡹ࡮ࠠࡱ࡫ࡧࠤࠧჱ") + str(pid) + bstack11l1l11_opy_ (u"ࠧࠨჲ"))
            for callback in callbacks:
                try:
                    self.logger.debug(bstack11l1l11_opy_ (u"ࠨࡉ࡯ࡸࡲ࡯ࡪࡪࠠࡤࡣ࡯ࡰࡧࡧࡣ࡬ࠢࡩࡳࡷࠦࡥࡷࡧࡱࡸࠥ࠭ࡻࡦࡸࡨࡲࡹࡥ࡮ࡢ࡯ࡨࢁࠬࠦࡷࡪࡶ࡫ࠤࡵ࡯ࡤࠡࠤჳ") + str(pid) + bstack11l1l11_opy_ (u"ࠢࠣჴ"))
                    callback(event_name, *args, **kwargs)
                except Exception as e:
                    self.logger.error(bstack11l1l11_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡪࡰࡹࡳࡰ࡯࡮ࡨࠢࡦࡥࡱࡲࡢࡢࡥ࡮ࠤ࡫ࡵࡲࠡࡧࡹࡩࡳࡺࠠࠨࡽࡨࡺࡪࡴࡴࡠࡰࡤࡱࡪࢃࠧࠡࡹ࡬ࡸ࡭ࠦࡰࡪࡦࠣࡿࡵ࡯ࡤࡾ࠼ࠣࠦჵ") + str(e) + bstack11l1l11_opy_ (u"ࠤࠥჶ"))
                    traceback.print_exc()
bstack11l11ll11l_opy_ = bstack1ll1llll1l1_opy_()
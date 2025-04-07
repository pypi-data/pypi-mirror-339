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
from enum import Enum
import os
import threading
import traceback
from typing import Dict, List, Any, Callable, Tuple, Union
import abc
from datetime import datetime, timezone
from dataclasses import dataclass
from browserstack_sdk.sdk_cli.bstack11111111l1_opy_ import bstack11111ll11l_opy_, bstack11111l1111_opy_
class bstack1lll111lll1_opy_(Enum):
    PRE = 0
    POST = 1
    def __repr__(self) -> str:
        return bstack11l1l11_opy_ (u"ࠥࡘࡪࡹࡴࡉࡱࡲ࡯ࡘࡺࡡࡵࡧ࠱ࡿࢂࠨᒓ").format(self.name)
class bstack1llllll1lll_opy_(Enum):
    NONE = 0
    BEFORE_ALL = 1
    LOG = 2
    SETUP_FIXTURE = 3
    INIT_TEST = 4
    BEFORE_EACH = 5
    AFTER_EACH = 6
    TEST = 7
    STEP = 8
    LOG_REPORT = 9
    AFTER_ALL = 10
    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return self.value == other.value
        return NotImplemented
    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented
    def __repr__(self) -> str:
        return bstack11l1l11_opy_ (u"࡙ࠦ࡫ࡳࡵࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡗࡹࡧࡴࡦ࠰ࡾࢁࠧᒔ").format(self.name)
class bstack1lllllll111_opy_(bstack11111ll11l_opy_):
    bstack1ll1lll11ll_opy_: List[str]
    bstack1l11l1ll1ll_opy_: Dict[str, str]
    state: bstack1llllll1lll_opy_
    bstack11111l1l11_opy_: datetime
    bstack111111lll1_opy_: datetime
    def __init__(
        self,
        context: bstack11111l1111_opy_,
        bstack1ll1lll11ll_opy_: List[str],
        bstack1l11l1ll1ll_opy_: Dict[str, str],
        state=bstack1llllll1lll_opy_.NONE,
    ):
        super().__init__(context)
        self.bstack1ll1lll11ll_opy_ = bstack1ll1lll11ll_opy_
        self.bstack1l11l1ll1ll_opy_ = bstack1l11l1ll1ll_opy_
        self.state = state
        self.bstack11111l1l11_opy_ = datetime.now(tz=timezone.utc)
        self.bstack111111lll1_opy_ = datetime.now(tz=timezone.utc)
    def bstack1111111l1l_opy_(self, bstack1111l11ll1_opy_: bstack1llllll1lll_opy_):
        bstack11111lll11_opy_ = bstack1llllll1lll_opy_(bstack1111l11ll1_opy_).name
        if not bstack11111lll11_opy_:
            return False
        if bstack1111l11ll1_opy_ == self.state:
            return False
        self.state = bstack1111l11ll1_opy_
        self.bstack111111lll1_opy_ = datetime.now(tz=timezone.utc)
        return True
@dataclass
class bstack1l11lll1l11_opy_:
    test_framework_name: str
    test_framework_version: str
    platform_index: int
@dataclass
class bstack1lll11ll111_opy_:
    kind: str
    message: str
    level: Union[None, str] = None
    timestamp: Union[None, datetime] = datetime.now(tz=timezone.utc)
class TestFramework(abc.ABC):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    bstack1ll1lll11l1_opy_ = bstack11l1l11_opy_ (u"ࠧࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠣᒕ")
    bstack1l11ll1llll_opy_ = bstack11l1l11_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡮ࡪࠢᒖ")
    bstack1ll1l11l111_opy_ = bstack11l1l11_opy_ (u"ࠢࡵࡧࡶࡸࡤࡴࡡ࡮ࡧࠥᒗ")
    bstack1l1l111ll11_opy_ = bstack11l1l11_opy_ (u"ࠣࡶࡨࡷࡹࡥࡦࡪ࡮ࡨࡣࡵࡧࡴࡩࠤᒘ")
    bstack1l11ll1l111_opy_ = bstack11l1l11_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡵࡣࡪࡷࠧᒙ")
    bstack1l1ll1111ll_opy_ = bstack11l1l11_opy_ (u"ࠥࡸࡪࡹࡴࡠࡴࡨࡷࡺࡲࡴࠣᒚ")
    bstack1ll11l111ll_opy_ = bstack11l1l11_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡵࡩࡸࡻ࡬ࡵࡡࡤࡸࠧᒛ")
    bstack1ll111111ll_opy_ = bstack11l1l11_opy_ (u"ࠧࡺࡥࡴࡶࡢࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠢᒜ")
    bstack1ll111ll111_opy_ = bstack11l1l11_opy_ (u"ࠨࡴࡦࡵࡷࡣࡪࡴࡤࡦࡦࡢࡥࡹࠨᒝ")
    bstack1l11llll1l1_opy_ = bstack11l1l11_opy_ (u"ࠢࡵࡧࡶࡸࡤࡲ࡯ࡤࡣࡷ࡭ࡴࡴࠢᒞ")
    bstack1ll1l1llll1_opy_ = bstack11l1l11_opy_ (u"ࠣࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫ࠢᒟ")
    bstack1ll11111l11_opy_ = bstack11l1l11_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠦᒠ")
    bstack1l11ll1111l_opy_ = bstack11l1l11_opy_ (u"ࠥࡸࡪࡹࡴࡠࡥࡲࡨࡪࠨᒡ")
    bstack1l1lll11lll_opy_ = bstack11l1l11_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡵࡩࡷࡻ࡮ࡠࡰࡤࡱࡪࠨᒢ")
    bstack1ll1l11llll_opy_ = bstack11l1l11_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡪࡰࡧࡩࡽࠨᒣ")
    bstack1l1l1lllll1_opy_ = bstack11l1l11_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡫ࡧࡩ࡭ࡷࡵࡩࠧᒤ")
    bstack1l11l11l1l1_opy_ = bstack11l1l11_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡬ࡡࡪ࡮ࡸࡶࡪࡥࡴࡺࡲࡨࠦᒥ")
    bstack1l11l1ll11l_opy_ = bstack11l1l11_opy_ (u"ࠣࡶࡨࡷࡹࡥ࡬ࡰࡩࡶࠦᒦ")
    bstack1l11lll11l1_opy_ = bstack11l1l11_opy_ (u"ࠤࡷࡩࡸࡺ࡟࡮ࡧࡷࡥࠧᒧ")
    bstack1l11l111l11_opy_ = bstack11l1l11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡵࡦࡳࡵ࡫ࡳࠨᒨ")
    bstack1l1l11llll1_opy_ = bstack11l1l11_opy_ (u"ࠦࡦࡻࡴࡰ࡯ࡤࡸࡪࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟࡯ࡣࡰࡩࠧᒩ")
    bstack1l11l11l1ll_opy_ = bstack11l1l11_opy_ (u"ࠧ࡫ࡶࡦࡰࡷࡣࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠣᒪ")
    bstack1l11l1l11ll_opy_ = bstack11l1l11_opy_ (u"ࠨࡥࡷࡧࡱࡸࡤ࡫࡮ࡥࡧࡧࡣࡦࡺࠢᒫ")
    bstack1l11lll1lll_opy_ = bstack11l1l11_opy_ (u"ࠢࡩࡱࡲ࡯ࡤ࡯ࡤࠣᒬ")
    bstack1l11lll11ll_opy_ = bstack11l1l11_opy_ (u"ࠣࡪࡲࡳࡰࡥࡲࡦࡵࡸࡰࡹࠨᒭ")
    bstack1l11ll1ll11_opy_ = bstack11l1l11_opy_ (u"ࠤ࡫ࡳࡴࡱ࡟࡭ࡱࡪࡷࠧᒮ")
    bstack1l11ll11111_opy_ = bstack11l1l11_opy_ (u"ࠥ࡬ࡴࡵ࡫ࡠࡰࡤࡱࡪࠨᒯ")
    bstack1l11l11lll1_opy_ = bstack11l1l11_opy_ (u"ࠦࡵ࡫࡮ࡥ࡫ࡱ࡫ࠧᒰ")
    bstack1l11l1lll11_opy_ = bstack11l1l11_opy_ (u"ࠧࡶࡥ࡯ࡦ࡬ࡲ࡬ࠨᒱ")
    bstack1l1llll1lll_opy_ = bstack11l1l11_opy_ (u"ࠨࡔࡆࡕࡗࡣࡘࡉࡒࡆࡇࡑࡗࡍࡕࡔࠣᒲ")
    bstack1ll11l1l11l_opy_ = bstack11l1l11_opy_ (u"ࠢࡕࡇࡖࡘࡤࡒࡏࡈࠤᒳ")
    bstack1111111111_opy_: Dict[str, bstack1lllllll111_opy_] = dict()
    bstack1l11l1111l1_opy_: Dict[str, List[Callable]] = dict()
    bstack1ll1lll11ll_opy_: List[str]
    bstack1l11l1ll1ll_opy_: Dict[str, str]
    def __init__(
        self,
        bstack1ll1lll11ll_opy_: List[str],
        bstack1l11l1ll1ll_opy_: Dict[str, str],
    ):
        self.bstack1ll1lll11ll_opy_ = bstack1ll1lll11ll_opy_
        self.bstack1l11l1ll1ll_opy_ = bstack1l11l1ll1ll_opy_
    def track_event(
        self,
        context: bstack1l11lll1l11_opy_,
        test_framework_state: bstack1llllll1lll_opy_,
        test_hook_state: bstack1lll111lll1_opy_,
        *args,
        **kwargs,
    ):
        self.logger.debug(bstack11l1l11_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡦࡸࡨࡲࡹࡀࠠࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫࠽ࡼࡿࠣࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࡂࢁࡽࠡࡣࡵ࡫ࡸࡃࡻࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࡾࢁࠧᒴ").format(test_framework_state,test_hook_state,args,kwargs))
    def bstack1l11l1l1ll1_opy_(
        self,
        instance: bstack1lllllll111_opy_,
        bstack1111l1ll11_opy_: Tuple[bstack1llllll1lll_opy_, bstack1lll111lll1_opy_],
        *args,
        **kwargs,
    ):
        bstack1l1l11l1111_opy_ = TestFramework.bstack1l1l11l1l11_opy_(bstack1111l1ll11_opy_)
        if not bstack1l1l11l1111_opy_ in TestFramework.bstack1l11l1111l1_opy_:
            return
        self.logger.debug(bstack11l1l11_opy_ (u"ࠤ࡬ࡲࡻࡵ࡫ࡪࡰࡪࠤࢀࢃࠠࡤࡣ࡯ࡰࡧࡧࡣ࡬ࡵࠥᒵ").format(len(TestFramework.bstack1l11l1111l1_opy_[bstack1l1l11l1111_opy_])))
        for callback in TestFramework.bstack1l11l1111l1_opy_[bstack1l1l11l1111_opy_]:
            try:
                callback(self, instance, bstack1111l1ll11_opy_, *args, **kwargs)
            except Exception as e:
                self.logger.error(bstack11l1l11_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠢ࡬ࡲࡻࡵ࡫ࡪࡰࡪࠤࡨࡧ࡬࡭ࡤࡤࡧࡰࡀࠠࡼࡿࠥᒶ").format(e))
                traceback.print_exc()
    @abc.abstractmethod
    def bstack1l1llll1111_opy_(self):
        return
    @abc.abstractmethod
    def bstack1l1lllllll1_opy_(self, instance, bstack1111l1ll11_opy_):
        return
    @abc.abstractmethod
    def bstack1ll11111111_opy_(self, instance, bstack1111l1ll11_opy_):
        return
    @staticmethod
    def bstack11111ll111_opy_(target: object, strict=True):
        if target is None:
            return None
        ctx = bstack11111ll11l_opy_.create_context(target)
        instance = TestFramework.bstack1111111111_opy_.get(ctx.id, None)
        if instance and instance.bstack111111l11l_opy_(target):
            return instance
        return instance if instance and not strict else None
    @staticmethod
    def bstack1ll1111lll1_opy_(reverse=True) -> List[bstack1lllllll111_opy_]:
        thread_id = threading.get_ident()
        process_id = os.getpid()
        return sorted(
            filter(
                lambda t: t.context.thread_id == thread_id
                and t.context.process_id == process_id,
                TestFramework.bstack1111111111_opy_.values(),
            ),
            key=lambda t: t.bstack11111l1l11_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1111l1l1ll_opy_(ctx: bstack11111l1111_opy_, reverse=True) -> List[bstack1lllllll111_opy_]:
        return sorted(
            filter(
                lambda t: t.context.thread_id == ctx.thread_id
                and t.context.process_id == ctx.process_id,
                TestFramework.bstack1111111111_opy_.values(),
            ),
            key=lambda t: t.bstack11111l1l11_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1111111l11_opy_(instance: bstack1lllllll111_opy_, key: str):
        return instance and key in instance.data
    @staticmethod
    def bstack11111l1l1l_opy_(instance: bstack1lllllll111_opy_, key: str, default_value=None):
        return instance.data.get(key, default_value) if instance else default_value
    @staticmethod
    def bstack1111111l1l_opy_(instance: bstack1lllllll111_opy_, key: str, value: Any):
        TestFramework.logger.debug(bstack11l1l11_opy_ (u"ࠦࡸ࡫ࡴࡠࡵࡷࡥࡹ࡫࠺ࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࡿࢂࠦ࡫ࡦࡻࡀࡿࢂࠦࡶࡢ࡮ࡸࡩࡂࢁࡽࠣᒷ").format(instance.ref(),key,value))
        instance.data[key] = value
        return True
    @staticmethod
    def bstack1l11llll1ll_opy_(instance: bstack1lllllll111_opy_, entries: Dict[str, Any]):
        TestFramework.logger.debug(bstack11l1l11_opy_ (u"ࠧࡹࡥࡵࡡࡶࡸࡦࡺࡥࡠࡧࡱࡸࡷ࡯ࡥࡴ࠼ࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡽࠡࡧࡱࡸࡷ࡯ࡥࡴ࠿ࡾࢁࠧᒸ").format(instance.ref(),entries,))
        instance.data.update(entries)
        return True
    @staticmethod
    def bstack1l111lll11l_opy_(instance: bstack1llllll1lll_opy_, key: str, value: Any):
        TestFramework.logger.debug(bstack11l1l11_opy_ (u"ࠨࡵࡱࡦࡤࡸࡪࡥࡳࡵࡣࡷࡩ࠿ࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࡽࢀࠤࡰ࡫ࡹ࠾ࡽࢀࠤࡻࡧ࡬ࡶࡧࡀࡿࢂࠨᒹ").format(instance.ref(),key,value))
        instance.data.update(key, value)
        return True
    @staticmethod
    def get_data(key: str, target: object, strict=True, default_value=None):
        instance = TestFramework.bstack11111ll111_opy_(target, strict)
        return TestFramework.bstack11111l1l1l_opy_(instance, key, default_value)
    @staticmethod
    def set_data(key: str, value: Any, target: object, strict=True):
        instance = TestFramework.bstack11111ll111_opy_(target, strict)
        if not instance:
            return False
        instance.data[key] = value
        return True
    @staticmethod
    def bstack1l11ll111ll_opy_(instance: bstack1lllllll111_opy_, key: str, value: object):
        if instance == None:
            return
        instance.data[key] = value
    @staticmethod
    def bstack1l11lllll1l_opy_(instance: bstack1lllllll111_opy_, key: str):
        return instance.data[key]
    @staticmethod
    def bstack1l1l11l1l11_opy_(bstack1111l1ll11_opy_: Tuple[bstack1llllll1lll_opy_, bstack1lll111lll1_opy_]):
        return bstack11l1l11_opy_ (u"ࠢ࠻ࠤᒺ").join((bstack1llllll1lll_opy_(bstack1111l1ll11_opy_[0]).name, bstack1lll111lll1_opy_(bstack1111l1ll11_opy_[1]).name))
    @staticmethod
    def bstack1ll1l11l11l_opy_(bstack1111l1ll11_opy_: Tuple[bstack1llllll1lll_opy_, bstack1lll111lll1_opy_], callback: Callable):
        bstack1l1l11l1111_opy_ = TestFramework.bstack1l1l11l1l11_opy_(bstack1111l1ll11_opy_)
        TestFramework.logger.debug(bstack11l1l11_opy_ (u"ࠣࡵࡨࡸࡤ࡮࡯ࡰ࡭ࡢࡧࡦࡲ࡬ࡣࡣࡦ࡯࠿ࠦࡨࡰࡱ࡮ࡣࡷ࡫ࡧࡪࡵࡷࡶࡾࡥ࡫ࡦࡻࡀࡿࢂࠨᒻ").format(bstack1l1l11l1111_opy_))
        if not bstack1l1l11l1111_opy_ in TestFramework.bstack1l11l1111l1_opy_:
            TestFramework.bstack1l11l1111l1_opy_[bstack1l1l11l1111_opy_] = []
        TestFramework.bstack1l11l1111l1_opy_[bstack1l1l11l1111_opy_].append(callback)
    @staticmethod
    def bstack1l1llll1l11_opy_(o):
        klass = o.__class__
        module = klass.__module__
        if module == bstack11l1l11_opy_ (u"ࠤࡥࡹ࡮ࡲࡴࡪࡰࡶࠦᒼ"):
            return klass.__qualname__
        return module + bstack11l1l11_opy_ (u"ࠥ࠲ࠧᒽ") + klass.__qualname__
    @staticmethod
    def bstack1ll111l111l_opy_(obj, keys, default_value=None):
        return {k: getattr(obj, k, default_value) for k in keys}
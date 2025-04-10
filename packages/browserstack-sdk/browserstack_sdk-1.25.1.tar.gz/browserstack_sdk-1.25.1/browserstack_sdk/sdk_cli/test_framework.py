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
from enum import Enum
import os
import threading
import traceback
from typing import Dict, List, Any, Callable, Tuple, Union
import abc
from datetime import datetime, timezone
from dataclasses import dataclass
from browserstack_sdk.sdk_cli.bstack1111l1ll11_opy_ import bstack1111l1llll_opy_
from browserstack_sdk.sdk_cli.bstack111111ll11_opy_ import bstack11111111l1_opy_, bstack111111l1l1_opy_
class bstack1lll1l11l1l_opy_(Enum):
    PRE = 0
    POST = 1
    def __repr__(self) -> str:
        return bstack1ll1l1_opy_ (u"ࠢࡕࡧࡶࡸࡍࡵ࡯࡬ࡕࡷࡥࡹ࡫࠮ࡼࡿࠥᓫ").format(self.name)
class bstack1lllllll1ll_opy_(Enum):
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
        return bstack1ll1l1_opy_ (u"ࠣࡖࡨࡷࡹࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡔࡶࡤࡸࡪ࠴ࡻࡾࠤᓬ").format(self.name)
class bstack1lll1l1l1l1_opy_(bstack11111111l1_opy_):
    bstack1ll1l1l1111_opy_: List[str]
    bstack1l11llll1ll_opy_: Dict[str, str]
    state: bstack1lllllll1ll_opy_
    bstack1111l11111_opy_: datetime
    bstack111111lll1_opy_: datetime
    def __init__(
        self,
        context: bstack111111l1l1_opy_,
        bstack1ll1l1l1111_opy_: List[str],
        bstack1l11llll1ll_opy_: Dict[str, str],
        state=bstack1lllllll1ll_opy_.NONE,
    ):
        super().__init__(context)
        self.bstack1ll1l1l1111_opy_ = bstack1ll1l1l1111_opy_
        self.bstack1l11llll1ll_opy_ = bstack1l11llll1ll_opy_
        self.state = state
        self.bstack1111l11111_opy_ = datetime.now(tz=timezone.utc)
        self.bstack111111lll1_opy_ = datetime.now(tz=timezone.utc)
    def bstack1111111111_opy_(self, bstack11111111ll_opy_: bstack1lllllll1ll_opy_):
        bstack1111l111l1_opy_ = bstack1lllllll1ll_opy_(bstack11111111ll_opy_).name
        if not bstack1111l111l1_opy_:
            return False
        if bstack11111111ll_opy_ == self.state:
            return False
        self.state = bstack11111111ll_opy_
        self.bstack111111lll1_opy_ = datetime.now(tz=timezone.utc)
        return True
@dataclass
class bstack1l111lll1l1_opy_:
    test_framework_name: str
    test_framework_version: str
    platform_index: int
@dataclass
class bstack1llll1l1lll_opy_:
    kind: str
    message: str
    level: Union[None, str] = None
    timestamp: Union[None, datetime] = datetime.now(tz=timezone.utc)
    fileName: str = None
    bstack1ll111l1l1l_opy_: int = None
    bstack1ll11111ll1_opy_: str = None
    bstack1l11_opy_: str = None
    bstack1llll1ll11_opy_: str = None
    bstack1ll11111111_opy_: str = None
    bstack1l11l1l111l_opy_: str = None
class TestFramework(abc.ABC):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    bstack1ll1ll1ll11_opy_ = bstack1ll1l1_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠧᓭ")
    bstack1l111l1ll1l_opy_ = bstack1ll1l1_opy_ (u"ࠥࡸࡪࡹࡴࡠ࡫ࡧࠦᓮ")
    bstack1ll1ll1l1l1_opy_ = bstack1ll1l1_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡱࡥࡲ࡫ࠢᓯ")
    bstack1l11l1lll11_opy_ = bstack1ll1l1_opy_ (u"ࠧࡺࡥࡴࡶࡢࡪ࡮ࡲࡥࡠࡲࡤࡸ࡭ࠨᓰ")
    bstack1l11l1111l1_opy_ = bstack1ll1l1_opy_ (u"ࠨࡴࡦࡵࡷࡣࡹࡧࡧࡴࠤᓱ")
    bstack1l1l1lll111_opy_ = bstack1ll1l1_opy_ (u"ࠢࡵࡧࡶࡸࡤࡸࡥࡴࡷ࡯ࡸࠧᓲ")
    bstack1l1lll111l1_opy_ = bstack1ll1l1_opy_ (u"ࠣࡶࡨࡷࡹࡥࡲࡦࡵࡸࡰࡹࡥࡡࡵࠤᓳ")
    bstack1l1lllll1l1_opy_ = bstack1ll1l1_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠦᓴ")
    bstack1ll11111l1l_opy_ = bstack1ll1l1_opy_ (u"ࠥࡸࡪࡹࡴࡠࡧࡱࡨࡪࡪ࡟ࡢࡶࠥᓵ")
    bstack1l11l1111ll_opy_ = bstack1ll1l1_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡯ࡳࡨࡧࡴࡪࡱࡱࠦᓶ")
    bstack1ll1ll1l1ll_opy_ = bstack1ll1l1_opy_ (u"ࠧࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࠦᓷ")
    bstack1ll111l1lll_opy_ = bstack1ll1l1_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠣᓸ")
    bstack1l11l1ll111_opy_ = bstack1ll1l1_opy_ (u"ࠢࡵࡧࡶࡸࡤࡩ࡯ࡥࡧࠥᓹ")
    bstack1l1ll1lll1l_opy_ = bstack1ll1l1_opy_ (u"ࠣࡶࡨࡷࡹࡥࡲࡦࡴࡸࡲࡤࡴࡡ࡮ࡧࠥᓺ")
    bstack1ll11llll1l_opy_ = bstack1ll1l1_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࡣ࡮ࡴࡤࡦࡺࠥᓻ")
    bstack1l1l1ll1111_opy_ = bstack1ll1l1_opy_ (u"ࠥࡸࡪࡹࡴࡠࡨࡤ࡭ࡱࡻࡲࡦࠤᓼ")
    bstack1l111ll1lll_opy_ = bstack1ll1l1_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡩࡥ࡮ࡲࡵࡳࡧࡢࡸࡾࡶࡥࠣᓽ")
    bstack1l11l1ll11l_opy_ = bstack1ll1l1_opy_ (u"ࠧࡺࡥࡴࡶࡢࡰࡴ࡭ࡳࠣᓾ")
    bstack1l11l1ll1ll_opy_ = bstack1ll1l1_opy_ (u"ࠨࡴࡦࡵࡷࡣࡲ࡫ࡴࡢࠤᓿ")
    bstack1l111l11lll_opy_ = bstack1ll1l1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡹࡣࡰࡲࡨࡷࠬᔀ")
    bstack1l1l111l1ll_opy_ = bstack1ll1l1_opy_ (u"ࠣࡣࡸࡸࡴࡳࡡࡵࡧࡢࡷࡪࡹࡳࡪࡱࡱࡣࡳࡧ࡭ࡦࠤᔁ")
    bstack1l11lll1ll1_opy_ = bstack1ll1l1_opy_ (u"ࠤࡨࡺࡪࡴࡴࡠࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠧᔂ")
    bstack1l11ll1111l_opy_ = bstack1ll1l1_opy_ (u"ࠥࡩࡻ࡫࡮ࡵࡡࡨࡲࡩ࡫ࡤࡠࡣࡷࠦᔃ")
    bstack1l11l11l1ll_opy_ = bstack1ll1l1_opy_ (u"ࠦ࡭ࡵ࡯࡬ࡡ࡬ࡨࠧᔄ")
    bstack1l11ll1l1ll_opy_ = bstack1ll1l1_opy_ (u"ࠧ࡮࡯ࡰ࡭ࡢࡶࡪࡹࡵ࡭ࡶࠥᔅ")
    bstack1l11lll1l11_opy_ = bstack1ll1l1_opy_ (u"ࠨࡨࡰࡱ࡮ࡣࡱࡵࡧࡴࠤᔆ")
    bstack1l11llll11l_opy_ = bstack1ll1l1_opy_ (u"ࠢࡩࡱࡲ࡯ࡤࡴࡡ࡮ࡧࠥᔇ")
    bstack1l11lllll11_opy_ = bstack1ll1l1_opy_ (u"ࠣ࡮ࡲ࡫ࡸࠨᔈ")
    bstack1l11l11l11l_opy_ = bstack1ll1l1_opy_ (u"ࠤࡦࡹࡸࡺ࡯࡮ࡡࡰࡩࡹࡧࡤࡢࡶࡤࠦᔉ")
    bstack1l11lll11ll_opy_ = bstack1ll1l1_opy_ (u"ࠥࡴࡪࡴࡤࡪࡰࡪࠦᔊ")
    bstack1l11l11111l_opy_ = bstack1ll1l1_opy_ (u"ࠦࡵ࡫࡮ࡥ࡫ࡱ࡫ࠧᔋ")
    bstack1ll11l111ll_opy_ = bstack1ll1l1_opy_ (u"࡚ࠧࡅࡔࡖࡢࡗࡈࡘࡅࡆࡐࡖࡌࡔ࡚ࠢᔌ")
    bstack1l1lll1ll11_opy_ = bstack1ll1l1_opy_ (u"ࠨࡔࡆࡕࡗࡣࡑࡕࡇࠣᔍ")
    bstack1ll111l1111_opy_ = bstack1ll1l1_opy_ (u"ࠢࡕࡇࡖࡘࡤࡇࡔࡕࡃࡆࡌࡒࡋࡎࡕࠤᔎ")
    bstack1llllllll1l_opy_: Dict[str, bstack1lll1l1l1l1_opy_] = dict()
    bstack1l111l111l1_opy_: Dict[str, List[Callable]] = dict()
    bstack1ll1l1l1111_opy_: List[str]
    bstack1l11llll1ll_opy_: Dict[str, str]
    def __init__(
        self,
        bstack1ll1l1l1111_opy_: List[str],
        bstack1l11llll1ll_opy_: Dict[str, str],
        bstack1111l1ll11_opy_: bstack1111l1llll_opy_
    ):
        self.bstack1ll1l1l1111_opy_ = bstack1ll1l1l1111_opy_
        self.bstack1l11llll1ll_opy_ = bstack1l11llll1ll_opy_
        self.bstack1111l1ll11_opy_ = bstack1111l1ll11_opy_
    def track_event(
        self,
        context: bstack1l111lll1l1_opy_,
        test_framework_state: bstack1lllllll1ll_opy_,
        test_hook_state: bstack1lll1l11l1l_opy_,
        *args,
        **kwargs,
    ):
        self.logger.debug(bstack1ll1l1_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡦࡸࡨࡲࡹࡀࠠࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫࠽ࡼࡿࠣࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࡂࢁࡽࠡࡣࡵ࡫ࡸࡃࡻࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࡾࢁࠧᔏ").format(test_framework_state,test_hook_state,args,kwargs))
    def bstack1l111llllll_opy_(
        self,
        instance: bstack1lll1l1l1l1_opy_,
        bstack1111l1l11l_opy_: Tuple[bstack1lllllll1ll_opy_, bstack1lll1l11l1l_opy_],
        *args,
        **kwargs,
    ):
        bstack1l1l11111ll_opy_ = TestFramework.bstack1l1l111111l_opy_(bstack1111l1l11l_opy_)
        if not bstack1l1l11111ll_opy_ in TestFramework.bstack1l111l111l1_opy_:
            return
        self.logger.debug(bstack1ll1l1_opy_ (u"ࠤ࡬ࡲࡻࡵ࡫ࡪࡰࡪࠤࢀࢃࠠࡤࡣ࡯ࡰࡧࡧࡣ࡬ࡵࠥᔐ").format(len(TestFramework.bstack1l111l111l1_opy_[bstack1l1l11111ll_opy_])))
        for callback in TestFramework.bstack1l111l111l1_opy_[bstack1l1l11111ll_opy_]:
            try:
                callback(self, instance, bstack1111l1l11l_opy_, *args, **kwargs)
            except Exception as e:
                self.logger.error(bstack1ll1l1_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠢ࡬ࡲࡻࡵ࡫ࡪࡰࡪࠤࡨࡧ࡬࡭ࡤࡤࡧࡰࡀࠠࡼࡿࠥᔑ").format(e))
                traceback.print_exc()
    @abc.abstractmethod
    def bstack1l1lllll11l_opy_(self):
        return
    @abc.abstractmethod
    def bstack1ll111ll1l1_opy_(self, instance, bstack1111l1l11l_opy_):
        return
    @abc.abstractmethod
    def bstack1ll111lll1l_opy_(self, instance, bstack1111l1l11l_opy_):
        return
    @staticmethod
    def bstack11111l1111_opy_(target: object, strict=True):
        if target is None:
            return None
        ctx = bstack11111111l1_opy_.create_context(target)
        instance = TestFramework.bstack1llllllll1l_opy_.get(ctx.id, None)
        if instance and instance.bstack1lllllllll1_opy_(target):
            return instance
        return instance if instance and not strict else None
    @staticmethod
    def bstack1l1lll1ll1l_opy_(reverse=True) -> List[bstack1lll1l1l1l1_opy_]:
        thread_id = threading.get_ident()
        process_id = os.getpid()
        return sorted(
            filter(
                lambda t: t.context.thread_id == thread_id
                and t.context.process_id == process_id,
                TestFramework.bstack1llllllll1l_opy_.values(),
            ),
            key=lambda t: t.bstack1111l11111_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack11111l1lll_opy_(ctx: bstack111111l1l1_opy_, reverse=True) -> List[bstack1lll1l1l1l1_opy_]:
        return sorted(
            filter(
                lambda t: t.context.thread_id == ctx.thread_id
                and t.context.process_id == ctx.process_id,
                TestFramework.bstack1llllllll1l_opy_.values(),
            ),
            key=lambda t: t.bstack1111l11111_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack11111l1l1l_opy_(instance: bstack1lll1l1l1l1_opy_, key: str):
        return instance and key in instance.data
    @staticmethod
    def bstack11111lllll_opy_(instance: bstack1lll1l1l1l1_opy_, key: str, default_value=None):
        return instance.data.get(key, default_value) if instance else default_value
    @staticmethod
    def bstack1111111111_opy_(instance: bstack1lll1l1l1l1_opy_, key: str, value: Any):
        TestFramework.logger.debug(bstack1ll1l1_opy_ (u"ࠦࡸ࡫ࡴࡠࡵࡷࡥࡹ࡫࠺ࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࡿࢂࠦ࡫ࡦࡻࡀࡿࢂࠦࡶࡢ࡮ࡸࡩࡂࢁࡽࠣᔒ").format(instance.ref(),key,value))
        instance.data[key] = value
        return True
    @staticmethod
    def bstack1l11lll1111_opy_(instance: bstack1lll1l1l1l1_opy_, entries: Dict[str, Any]):
        TestFramework.logger.debug(bstack1ll1l1_opy_ (u"ࠧࡹࡥࡵࡡࡶࡸࡦࡺࡥࡠࡧࡱࡸࡷ࡯ࡥࡴ࠼ࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡽࠡࡧࡱࡸࡷ࡯ࡥࡴ࠿ࡾࢁࠧᔓ").format(instance.ref(),entries,))
        instance.data.update(entries)
        return True
    @staticmethod
    def bstack1l1111ll1ll_opy_(instance: bstack1lllllll1ll_opy_, key: str, value: Any):
        TestFramework.logger.debug(bstack1ll1l1_opy_ (u"ࠨࡵࡱࡦࡤࡸࡪࡥࡳࡵࡣࡷࡩ࠿ࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࡽࢀࠤࡰ࡫ࡹ࠾ࡽࢀࠤࡻࡧ࡬ࡶࡧࡀࡿࢂࠨᔔ").format(instance.ref(),key,value))
        instance.data.update(key, value)
        return True
    @staticmethod
    def get_data(key: str, target: object, strict=True, default_value=None):
        instance = TestFramework.bstack11111l1111_opy_(target, strict)
        return TestFramework.bstack11111lllll_opy_(instance, key, default_value)
    @staticmethod
    def set_data(key: str, value: Any, target: object, strict=True):
        instance = TestFramework.bstack11111l1111_opy_(target, strict)
        if not instance:
            return False
        instance.data[key] = value
        return True
    @staticmethod
    def bstack1l11l111lll_opy_(instance: bstack1lll1l1l1l1_opy_, key: str, value: object):
        if instance == None:
            return
        instance.data[key] = value
    @staticmethod
    def bstack1l111l1llll_opy_(instance: bstack1lll1l1l1l1_opy_, key: str):
        return instance.data[key]
    @staticmethod
    def bstack1l1l111111l_opy_(bstack1111l1l11l_opy_: Tuple[bstack1lllllll1ll_opy_, bstack1lll1l11l1l_opy_]):
        return bstack1ll1l1_opy_ (u"ࠢ࠻ࠤᔕ").join((bstack1lllllll1ll_opy_(bstack1111l1l11l_opy_[0]).name, bstack1lll1l11l1l_opy_(bstack1111l1l11l_opy_[1]).name))
    @staticmethod
    def bstack1ll1l11l1l1_opy_(bstack1111l1l11l_opy_: Tuple[bstack1lllllll1ll_opy_, bstack1lll1l11l1l_opy_], callback: Callable):
        bstack1l1l11111ll_opy_ = TestFramework.bstack1l1l111111l_opy_(bstack1111l1l11l_opy_)
        TestFramework.logger.debug(bstack1ll1l1_opy_ (u"ࠣࡵࡨࡸࡤ࡮࡯ࡰ࡭ࡢࡧࡦࡲ࡬ࡣࡣࡦ࡯࠿ࠦࡨࡰࡱ࡮ࡣࡷ࡫ࡧࡪࡵࡷࡶࡾࡥ࡫ࡦࡻࡀࡿࢂࠨᔖ").format(bstack1l1l11111ll_opy_))
        if not bstack1l1l11111ll_opy_ in TestFramework.bstack1l111l111l1_opy_:
            TestFramework.bstack1l111l111l1_opy_[bstack1l1l11111ll_opy_] = []
        TestFramework.bstack1l111l111l1_opy_[bstack1l1l11111ll_opy_].append(callback)
    @staticmethod
    def bstack1ll11l11111_opy_(o):
        klass = o.__class__
        module = klass.__module__
        if module == bstack1ll1l1_opy_ (u"ࠤࡥࡹ࡮ࡲࡴࡪࡰࡶࠦᔗ"):
            return klass.__qualname__
        return module + bstack1ll1l1_opy_ (u"ࠥ࠲ࠧᔘ") + klass.__qualname__
    @staticmethod
    def bstack1ll111lll11_opy_(obj, keys, default_value=None):
        return {k: getattr(obj, k, default_value) for k in keys}
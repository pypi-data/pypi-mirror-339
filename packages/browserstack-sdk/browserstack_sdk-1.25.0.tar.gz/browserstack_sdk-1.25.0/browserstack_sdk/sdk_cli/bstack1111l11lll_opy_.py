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
from typing import Dict, Tuple, Callable, Type, List, Any
import abc
from datetime import datetime, timezone, timedelta
from browserstack_sdk.sdk_cli.bstack11111111l1_opy_ import bstack11111ll11l_opy_, bstack11111l1111_opy_
import os
import threading
class bstack111111111l_opy_(Enum):
    PRE = 0
    POST = 1
    def __repr__(self) -> str:
        return bstack11l1l11_opy_ (u"ࠥࡌࡴࡵ࡫ࡔࡶࡤࡸࡪ࠴ࡻࡾࠤတ").format(self.name)
class bstack1111l1ll1l_opy_(Enum):
    NONE = 0
    bstack111111ll11_opy_ = 1
    bstack11111111ll_opy_ = 3
    bstack111111l111_opy_ = 4
    bstack11111lll1l_opy_ = 5
    QUIT = 6
    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return self.value == other.value
        return NotImplemented
    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented
    def __repr__(self) -> str:
        return bstack11l1l11_opy_ (u"ࠦࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡖࡸࡦࡺࡥ࠯ࡽࢀࠦထ").format(self.name)
class bstack11111l11ll_opy_(bstack11111ll11l_opy_):
    framework_name: str
    framework_version: str
    state: bstack1111l1ll1l_opy_
    previous_state: bstack1111l1ll1l_opy_
    bstack11111l1l11_opy_: datetime
    bstack111111lll1_opy_: datetime
    def __init__(
        self,
        context: bstack11111l1111_opy_,
        framework_name: str,
        framework_version: str,
        state=bstack1111l1ll1l_opy_.NONE,
    ):
        super().__init__(context)
        self.framework_name = framework_name
        self.framework_version = framework_version
        self.state = state
        self.previous_state = bstack1111l1ll1l_opy_.NONE
        self.bstack11111l1l11_opy_ = datetime.now(tz=timezone.utc)
        self.bstack111111lll1_opy_ = datetime.now(tz=timezone.utc)
    def bstack1111111l1l_opy_(self, bstack1111l11ll1_opy_: bstack1111l1ll1l_opy_):
        bstack11111lll11_opy_ = bstack1111l1ll1l_opy_(bstack1111l11ll1_opy_).name
        if not bstack11111lll11_opy_:
            return False
        if bstack1111l11ll1_opy_ == self.state:
            return False
        if self.state == bstack1111l1ll1l_opy_.bstack11111111ll_opy_: # bstack1111111lll_opy_ bstack1111l111l1_opy_ for bstack111111l1ll_opy_ in bstack111111ll1l_opy_, it bstack1111l1l11l_opy_ bstack11111llll1_opy_ bstack1111l11l1l_opy_ times bstack1111l11l11_opy_ a new state
            return True
        if (
            bstack1111l11ll1_opy_ == bstack1111l1ll1l_opy_.NONE
            or (self.state != bstack1111l1ll1l_opy_.NONE and bstack1111l11ll1_opy_ == bstack1111l1ll1l_opy_.bstack111111ll11_opy_)
            or (self.state < bstack1111l1ll1l_opy_.bstack111111ll11_opy_ and bstack1111l11ll1_opy_ == bstack1111l1ll1l_opy_.bstack111111l111_opy_)
            or (self.state < bstack1111l1ll1l_opy_.bstack111111ll11_opy_ and bstack1111l11ll1_opy_ == bstack1111l1ll1l_opy_.QUIT)
        ):
            raise ValueError(bstack11l1l11_opy_ (u"ࠧ࡯࡮ࡷࡣ࡯࡭ࡩࠦࡳࡵࡣࡷࡩࠥࡺࡲࡢࡰࡶ࡭ࡹ࡯࡯࡯࠼ࠣࠦဒ") + str(self.state) + bstack11l1l11_opy_ (u"ࠨࠠ࠾ࡀࠣࠦဓ") + str(bstack1111l11ll1_opy_))
        self.previous_state = self.state
        self.state = bstack1111l11ll1_opy_
        self.bstack111111lll1_opy_ = datetime.now(tz=timezone.utc)
        return True
class bstack11111ll1l1_opy_(abc.ABC):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    bstack1111111111_opy_: Dict[str, bstack11111l11ll_opy_] = dict()
    framework_name: str
    framework_version: str
    classes: List[Type]
    def __init__(
        self,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
    ):
        self.framework_name = framework_name
        self.framework_version = framework_version
        self.classes = classes
    @abc.abstractmethod
    def bstack111111llll_opy_(self, instance: bstack11111l11ll_opy_, method_name: str, bstack11111l1ll1_opy_: timedelta, *args, **kwargs):
        return
    @abc.abstractmethod
    def bstack1111l111ll_opy_(
        self, method_name, previous_state: bstack1111l1ll1l_opy_, *args, **kwargs
    ) -> bstack1111l1ll1l_opy_:
        return
    @abc.abstractmethod
    def bstack1111l1111l_opy_(
        self,
        target: object,
        exec: Tuple[bstack11111l11ll_opy_, str],
        bstack1111l1ll11_opy_: Tuple[bstack1111l1ll1l_opy_, bstack111111111l_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable:
        return
    def bstack11111l11l1_opy_(self, bstack11111l111l_opy_: List[str]):
        for clazz in self.classes:
            for method_name in bstack11111l111l_opy_:
                bstack1111111ll1_opy_ = getattr(clazz, method_name, None)
                if not callable(bstack1111111ll1_opy_):
                    self.logger.warning(bstack11l1l11_opy_ (u"ࠢࡶࡰࡳࡥࡹࡩࡨࡦࡦࠣࡱࡪࡺࡨࡰࡦ࠽ࠤࠧန") + str(method_name) + bstack11l1l11_opy_ (u"ࠣࠤပ"))
                    continue
                bstack1111l11111_opy_ = self.bstack1111l111ll_opy_(
                    method_name, previous_state=bstack1111l1ll1l_opy_.NONE
                )
                bstack11111lllll_opy_ = self.bstack1llllllllll_opy_(
                    method_name,
                    (bstack1111l11111_opy_ if bstack1111l11111_opy_ else bstack1111l1ll1l_opy_.NONE),
                    bstack1111111ll1_opy_,
                )
                if not callable(bstack11111lllll_opy_):
                    self.logger.warning(bstack11l1l11_opy_ (u"ࠤࡰࡩࡹ࡮࡯ࡥࠢࡱࡳࡹࠦࡰࡢࡶࡦ࡬ࡪࡪ࠺ࠡࡽࡰࡩࡹ࡮࡯ࡥࡡࡱࡥࡲ࡫ࡽࠡࠪࡾࡷࡪࡲࡦ࠯ࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦࡿ࠽ࠤࠧဖ") + str(self.framework_version) + bstack11l1l11_opy_ (u"ࠥ࠭ࠧဗ"))
                    continue
                setattr(clazz, method_name, bstack11111lllll_opy_)
    def bstack1llllllllll_opy_(
        self,
        method_name: str,
        bstack1111l11111_opy_: bstack1111l1ll1l_opy_,
        bstack1111111ll1_opy_: Callable,
    ):
        def wrapped(target, *args, **kwargs):
            bstack1l1ll1l111_opy_ = datetime.now()
            (bstack1111l11111_opy_,) = wrapped.__vars__
            bstack1111l11111_opy_ = (
                bstack1111l11111_opy_
                if bstack1111l11111_opy_ and bstack1111l11111_opy_ != bstack1111l1ll1l_opy_.NONE
                else self.bstack1111l111ll_opy_(method_name, previous_state=bstack1111l11111_opy_, *args, **kwargs)
            )
            if bstack1111l11111_opy_ == bstack1111l1ll1l_opy_.bstack111111ll11_opy_:
                ctx = bstack11111ll11l_opy_.create_context(self.bstack1111l1l1l1_opy_(target))
                if not self.bstack111111l1l1_opy_() or ctx.id not in bstack11111ll1l1_opy_.bstack1111111111_opy_:
                    bstack11111ll1l1_opy_.bstack1111111111_opy_[ctx.id] = bstack11111l11ll_opy_(
                        ctx, self.framework_name, self.framework_version, bstack1111l11111_opy_
                    )
                self.logger.debug(bstack11l1l11_opy_ (u"ࠦࡼࡸࡡࡱࡲࡨࡨࠥࡳࡥࡵࡪࡲࡨࠥࡩࡲࡦࡣࡷࡩࡩࡀࠠࡼࡶࡤࡶ࡬࡫ࡴ࠯ࡡࡢࡧࡱࡧࡳࡴࡡࡢࢁࠥࡳࡥࡵࡪࡲࡨࡤࡴࡡ࡮ࡧࡀࡿࡲ࡫ࡴࡩࡱࡧࡣࡳࡧ࡭ࡦࡿࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࡂࢁࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾࠢࡦࡸࡽࡃࡻࡤࡶࡻ࠲࡮ࡪࡽࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡶࡁࠧဘ") + str(bstack11111ll1l1_opy_.bstack1111111111_opy_.keys()) + bstack11l1l11_opy_ (u"ࠧࠨမ"))
            else:
                self.logger.debug(bstack11l1l11_opy_ (u"ࠨࡷࡳࡣࡳࡴࡪࡪࠠ࡮ࡧࡷ࡬ࡴࡪࠠࡪࡰࡹࡳࡰ࡫ࡤ࠻ࠢࡾࡸࡦࡸࡧࡦࡶ࠱ࡣࡤࡩ࡬ࡢࡵࡶࡣࡤࢃࠠ࡮ࡧࡷ࡬ࡴࡪ࡟࡯ࡣࡰࡩࡂࢁ࡭ࡦࡶ࡫ࡳࡩࡥ࡮ࡢ࡯ࡨࢁࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫࠽ࡼࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡹ࠽ࠣယ") + str(bstack11111ll1l1_opy_.bstack1111111111_opy_.keys()) + bstack11l1l11_opy_ (u"ࠢࠣရ"))
            instance = bstack11111ll1l1_opy_.bstack11111ll111_opy_(self.bstack1111l1l1l1_opy_(target))
            if bstack1111l11111_opy_ == bstack1111l1ll1l_opy_.NONE or not instance:
                ctx = bstack11111ll11l_opy_.create_context(self.bstack1111l1l1l1_opy_(target))
                self.logger.warning(bstack11l1l11_opy_ (u"ࠣࡹࡵࡥࡵࡶࡥࡥࠢࡰࡩࡹ࡮࡯ࡥࠢࡸࡲࡹࡸࡡࡤ࡭ࡨࡨ࠿ࠦࡻ࡮ࡧࡷ࡬ࡴࡪ࡟࡯ࡣࡰࡩࢂࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥ࠾ࡽࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁࠥࡩࡴࡹ࠿ࡾࡧࡹࡾࡽࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡶࡁࠧလ") + str(bstack11111ll1l1_opy_.bstack1111111111_opy_.keys()) + bstack11l1l11_opy_ (u"ࠤࠥဝ"))
                return bstack1111111ll1_opy_(target, *args, **kwargs)
            bstack1111l1l111_opy_ = self.bstack1111l1111l_opy_(
                target,
                (instance, method_name),
                (bstack1111l11111_opy_, bstack111111111l_opy_.PRE),
                None,
                *args,
                **kwargs,
            )
            if instance.bstack1111111l1l_opy_(bstack1111l11111_opy_):
                self.logger.debug(bstack11l1l11_opy_ (u"ࠥࡥࡵࡶ࡬ࡪࡧࡧࠤࡸࡺࡡࡵࡧ࠰ࡸࡷࡧ࡮ࡴ࡫ࡷ࡭ࡴࡴ࠺ࠡࡽ࡬ࡲࡸࡺࡡ࡯ࡥࡨ࠲ࡵࡸࡥࡷ࡫ࡲࡹࡸࡥࡳࡵࡣࡷࡩࢂࠦ࠽࠿ࠢࡾ࡭ࡳࡹࡴࡢࡰࡦࡩ࠳ࡹࡴࡢࡶࡨࢁࠥ࠮ࡻࡵࡻࡳࡩ࠭ࡺࡡࡳࡩࡨࡸ࠮ࢃ࠮ࡼ࡯ࡨࡸ࡭ࡵࡤࡠࡰࡤࡱࡪࢃࠠࡼࡣࡵ࡫ࡸࢃࠩࠡ࡝ࠥသ") + str(instance.ref()) + bstack11l1l11_opy_ (u"ࠦࡢࠨဟ"))
            result = (
                bstack1111l1l111_opy_(target, bstack1111111ll1_opy_, *args, **kwargs)
                if callable(bstack1111l1l111_opy_)
                else bstack1111111ll1_opy_(target, *args, **kwargs)
            )
            bstack11111ll1ll_opy_ = self.bstack1111l1111l_opy_(
                target,
                (instance, method_name),
                (bstack1111l11111_opy_, bstack111111111l_opy_.POST),
                result,
                *args,
                **kwargs,
            )
            self.bstack111111llll_opy_(instance, method_name, datetime.now() - bstack1l1ll1l111_opy_, *args, **kwargs)
            return bstack11111ll1ll_opy_ if bstack11111ll1ll_opy_ else result
        wrapped.__name__ = method_name
        wrapped.__vars__ = (bstack1111l11111_opy_,)
        return wrapped
    @staticmethod
    def bstack11111ll111_opy_(target: object, strict=True):
        ctx = bstack11111ll11l_opy_.create_context(target)
        instance = bstack11111ll1l1_opy_.bstack1111111111_opy_.get(ctx.id, None)
        if instance and instance.bstack111111l11l_opy_(target):
            return instance
        return instance if instance and not strict else None
    @staticmethod
    def bstack1111l1l1ll_opy_(
        ctx: bstack11111l1111_opy_, state: bstack1111l1ll1l_opy_, reverse=True
    ) -> List[bstack11111l11ll_opy_]:
        return sorted(
            filter(
                lambda t: t.state == state
                and t.context.thread_id == ctx.thread_id
                and t.context.process_id == ctx.process_id,
                bstack11111ll1l1_opy_.bstack1111111111_opy_.values(),
            ),
            key=lambda t: t.bstack11111l1l11_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1111111l11_opy_(instance: bstack11111l11ll_opy_, key: str):
        return instance and key in instance.data
    @staticmethod
    def bstack11111l1l1l_opy_(instance: bstack11111l11ll_opy_, key: str, default_value=None):
        return instance.data.get(key, default_value) if instance else default_value
    @staticmethod
    def bstack1111111l1l_opy_(instance: bstack11111l11ll_opy_, key: str, value: Any) -> bool:
        instance.data[key] = value
        bstack11111ll1l1_opy_.logger.debug(bstack11l1l11_opy_ (u"ࠧࡹࡥࡵࡡࡶࡸࡦࡺࡥ࠻ࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࢀ࡯࡮ࡴࡶࡤࡲࡨ࡫࠮ࡳࡧࡩࠬ࠮ࢃࠠ࡬ࡧࡼࡁࢀࡱࡥࡺࡿࠣࡺࡦࡲࡵࡦ࠿ࠥဠ") + str(value) + bstack11l1l11_opy_ (u"ࠨࠢအ"))
        return True
    @staticmethod
    def get_data(key: str, target: object, strict=True, default_value=None):
        instance = bstack11111ll1l1_opy_.bstack11111ll111_opy_(target, strict)
        return bstack11111ll1l1_opy_.bstack11111l1l1l_opy_(instance, key, default_value)
    @staticmethod
    def set_data(key: str, value: Any, target: object, strict=True):
        instance = bstack11111ll1l1_opy_.bstack11111ll111_opy_(target, strict)
        if not instance:
            return False
        instance.data[key] = value
        return True
    def bstack111111l1l1_opy_(self):
        return self.framework_name == bstack11l1l11_opy_ (u"ࠧࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠫဢ")
    def bstack1111l1l1l1_opy_(self, target):
        return target if not self.bstack111111l1l1_opy_() else self.bstack11111l1lll_opy_()
    @staticmethod
    def bstack11111l1lll_opy_():
        return str(os.getpid()) + str(threading.get_ident())
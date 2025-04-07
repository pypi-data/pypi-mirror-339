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
from datetime import datetime, timezone
from pyexpat import features
from uuid import uuid4
from typing import Dict, List, Any, Tuple
from browserstack_sdk.sdk_cli.bstack11111111l1_opy_ import bstack11111ll11l_opy_
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    bstack1llllll1lll_opy_,
    bstack1lllllll111_opy_,
    bstack1lll111lll1_opy_,
    bstack1l11lll1l11_opy_,
    bstack1lll11ll111_opy_,
)
import traceback
from bstack_utils.bstack1l1ll1l11l_opy_ import bstack1lll1llll1l_opy_
from bstack_utils.constants import EVENTS
class PytestBDDFramework(TestFramework):
    bstack1l1l111l111_opy_ = bstack11l1l11_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡩ࡭ࡽࡺࡵࡳࡧࡶࠦፋ")
    bstack1l1l1111l11_opy_ = bstack11l1l11_opy_ (u"ࠧࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡴࡡࡶࡸࡦࡸࡴࡦࡦࠥፌ")
    bstack1l11ll11l1l_opy_ = bstack11l1l11_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡵࡢࡪ࡮ࡴࡩࡴࡪࡨࡨࠧፍ")
    bstack1l11llllll1_opy_ = bstack11l1l11_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡰࡦࡹࡴࡠࡵࡷࡥࡷࡺࡥࡥࠤፎ")
    bstack1l11l111lll_opy_ = bstack11l1l11_opy_ (u"ࠣࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡱࡧࡳࡵࡡࡩ࡭ࡳ࡯ࡳࡩࡧࡧࠦፏ")
    bstack1l11lllllll_opy_: bool
    bstack1l11lll111l_opy_ = [
        bstack1llllll1lll_opy_.BEFORE_ALL,
        bstack1llllll1lll_opy_.AFTER_ALL,
        bstack1llllll1lll_opy_.BEFORE_EACH,
        bstack1llllll1lll_opy_.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack1l11l1ll1ll_opy_: Dict[str, str],
        bstack1ll1lll11ll_opy_: List[str]=[bstack11l1l11_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠨፐ")],
    ):
        super().__init__(bstack1ll1lll11ll_opy_, bstack1l11l1ll1ll_opy_)
        self.bstack1l11lllllll_opy_ = any(bstack11l1l11_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠢፑ") in item.lower() for item in bstack1ll1lll11ll_opy_)
    def track_event(
        self,
        context: bstack1l11lll1l11_opy_,
        test_framework_state: bstack1llllll1lll_opy_,
        test_hook_state: bstack1lll111lll1_opy_,
        *args,
        **kwargs,
    ):
        super().track_event(self, context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == bstack1llllll1lll_opy_.NONE:
            self.logger.warning(bstack11l1l11_opy_ (u"ࠦ࡮࡭࡮ࡰࡴࡨࡨࠥࡩࡡ࡭࡮ࡥࡥࡨࡱࠠࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾࠢࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࡁࠧፒ") + str(test_hook_state) + bstack11l1l11_opy_ (u"ࠧࠨፓ"))
            return
        if not self.bstack1l11lllllll_opy_:
            self.logger.warning(bstack11l1l11_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡻ࡮ࡴࡷࡳࡴࡴࡸࡴࡦࡦࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡃࠢፔ") + str(str(self.bstack1ll1lll11ll_opy_)) + bstack11l1l11_opy_ (u"ࠢࠣፕ"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack11l1l11_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡦࡸࡨࡲࡹࡀࠠࡶࡰࡨࡼࡵ࡫ࡣࡵࡧࡧࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥፖ") + str(kwargs) + bstack11l1l11_opy_ (u"ࠤࠥፗ"))
            return
        instance = self.__1l11l1ll1l1_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡨࡺࡪࡴࡴ࠻ࠢࡸࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࡻࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦࡿࠣࡥࡷ࡭ࡳ࠾ࠤፘ") + str(args) + bstack11l1l11_opy_ (u"ࠦࠧፙ"))
            return
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.bstack1l11lll111l_opy_ and test_hook_state == bstack1lll111lll1_opy_.PRE:
                bstack1ll1ll1l1l1_opy_ = bstack1lll1llll1l_opy_.bstack1ll1ll1lll1_opy_(EVENTS.bstack1lll1ll1ll_opy_.value)
                name = str(EVENTS.bstack1lll1ll1ll_opy_.name)+bstack11l1l11_opy_ (u"ࠧࡀࠢፚ")+str(test_framework_state.name)
                TestFramework.bstack1l11ll111ll_opy_(instance, name, bstack1ll1ll1l1l1_opy_)
        except Exception as e:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡮࡯ࡰ࡭ࠣࡩࡷࡸ࡯ࡳࠢࡳࡶࡪࡀࠠࡼࡿࠥ፛").format(e))
        try:
            if test_framework_state == bstack1llllll1lll_opy_.TEST:
                if not TestFramework.bstack1111111l11_opy_(instance, TestFramework.bstack1l11ll1llll_opy_) and test_hook_state == bstack1lll111lll1_opy_.PRE:
                    if not (len(args) >= 3):
                        return
                    test = PytestBDDFramework.__1l11lll1ll1_opy_(args)
                    if test:
                        instance.data.update(test)
                        self.logger.debug(bstack11l1l11_opy_ (u"ࠢ࡭ࡱࡤࡨࡪࡪࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾ࡭ࡳࡹࡴࡢࡰࡦࡩ࠳ࡸࡥࡧࠪࠬࢁࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࠢ፜") + str(test_hook_state) + bstack11l1l11_opy_ (u"ࠣࠤ፝"))
                if test_hook_state == bstack1lll111lll1_opy_.PRE and not TestFramework.bstack1111111l11_opy_(instance, TestFramework.bstack1ll111111ll_opy_):
                    TestFramework.bstack1111111l1l_opy_(instance, TestFramework.bstack1ll111111ll_opy_, datetime.now(tz=timezone.utc))
                    PytestBDDFramework.__1l11l11ll11_opy_(instance, args)
                    self.logger.debug(bstack11l1l11_opy_ (u"ࠤࡶࡩࡹࠦࡴࡦࡵࡷ࠱ࡸࡺࡡࡳࡶࠣࡪࡴࡸࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾ࡭ࡳࡹࡴࡢࡰࡦࡩ࠳ࡸࡥࡧࠪࠬࢁࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࠢ፞") + str(test_hook_state) + bstack11l1l11_opy_ (u"ࠥࠦ፟"))
                elif test_hook_state == bstack1lll111lll1_opy_.POST and not TestFramework.bstack1111111l11_opy_(instance, TestFramework.bstack1ll111ll111_opy_):
                    TestFramework.bstack1111111l1l_opy_(instance, TestFramework.bstack1ll111ll111_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack11l1l11_opy_ (u"ࠦࡸ࡫ࡴࠡࡶࡨࡷࡹ࠳ࡥ࡯ࡦࠣࡪࡴࡸࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾ࡭ࡳࡹࡴࡢࡰࡦࡩ࠳ࡸࡥࡧࠪࠬࢁࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࠢ፠") + str(test_hook_state) + bstack11l1l11_opy_ (u"ࠧࠨ፡"))
            elif test_framework_state == bstack1llllll1lll_opy_.STEP:
                if test_hook_state == bstack1lll111lll1_opy_.PRE:
                    PytestBDDFramework.__1l1l1111l1l_opy_(instance, args)
                elif test_hook_state == bstack1lll111lll1_opy_.POST:
                    PytestBDDFramework.__1l11l1l111l_opy_(instance, args)
            elif test_framework_state == bstack1llllll1lll_opy_.LOG and test_hook_state == bstack1lll111lll1_opy_.POST:
                PytestBDDFramework.__1l11l1l1111_opy_(instance, *args)
            elif test_framework_state == bstack1llllll1lll_opy_.LOG_REPORT and test_hook_state == bstack1lll111lll1_opy_.POST:
                self.__1l1l111l1ll_opy_(instance, *args)
            elif test_framework_state in PytestBDDFramework.bstack1l11lll111l_opy_:
                self.__1l11l1l1l1l_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack11l1l11_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥ࡮ࡡ࡯ࡦ࡯ࡩࡩࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࡼࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࢀࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࠢ።") + str(instance.ref()) + bstack11l1l11_opy_ (u"ࠢࠣ፣"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack1l11l1l1ll1_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.bstack1l11lll111l_opy_ and test_hook_state == bstack1lll111lll1_opy_.POST:
                name = str(EVENTS.bstack1lll1ll1ll_opy_.name)+bstack11l1l11_opy_ (u"ࠣ࠼ࠥ፤")+str(test_framework_state.name)
                bstack1ll1ll1l1l1_opy_ = TestFramework.bstack1l11lllll1l_opy_(instance, name)
                bstack1lll1llll1l_opy_.end(EVENTS.bstack1lll1ll1ll_opy_.value, bstack1ll1ll1l1l1_opy_+bstack11l1l11_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤ፥"), bstack1ll1ll1l1l1_opy_+bstack11l1l11_opy_ (u"ࠥ࠾ࡪࡴࡤࠣ፦"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣ࡬ࡴࡵ࡫ࠡࡧࡵࡶࡴࡸ࠺ࠡࡽࢀࠦ፧").format(e))
    def bstack1l1llll1111_opy_(self):
        return self.bstack1l11lllllll_opy_
    def __1l11ll11lll_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack11l1l11_opy_ (u"ࠧ࡭ࡥࡵࡡࡵࡩࡸࡻ࡬ࡵࠤ፨"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack1ll111l111l_opy_(rep, [bstack11l1l11_opy_ (u"ࠨࡷࡩࡧࡱࠦ፩"), bstack11l1l11_opy_ (u"ࠢࡰࡷࡷࡧࡴࡳࡥࠣ፪"), bstack11l1l11_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣ፫"), bstack11l1l11_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤ፬"), bstack11l1l11_opy_ (u"ࠥࡷࡰ࡯ࡰࡱࡧࡧࠦ፭"), bstack11l1l11_opy_ (u"ࠦࡱࡵ࡮ࡨࡴࡨࡴࡷࡺࡥࡹࡶࠥ፮")])
        return None
    def __1l1l111l1ll_opy_(self, instance: bstack1lllllll111_opy_, *args):
        result = self.__1l11ll11lll_opy_(*args)
        if not result:
            return
        failure = None
        bstack1111ll1lll_opy_ = None
        if result.get(bstack11l1l11_opy_ (u"ࠧࡵࡵࡵࡥࡲࡱࡪࠨ፯"), None) == bstack11l1l11_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨ፰") and len(args) > 1 and getattr(args[1], bstack11l1l11_opy_ (u"ࠢࡦࡺࡦ࡭ࡳ࡬࡯ࠣ፱"), None) is not None:
            failure = [{bstack11l1l11_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫ፲"): [args[1].excinfo.exconly(), result.get(bstack11l1l11_opy_ (u"ࠤ࡯ࡳࡳ࡭ࡲࡦࡲࡵࡸࡪࡾࡴࠣ፳"), None)]}]
            bstack1111ll1lll_opy_ = bstack11l1l11_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࡋࡲࡳࡱࡵࠦ፴") if bstack11l1l11_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࠢ፵") in getattr(args[1].excinfo, bstack11l1l11_opy_ (u"ࠧࡺࡹࡱࡧࡱࡥࡲ࡫ࠢ፶"), bstack11l1l11_opy_ (u"ࠨࠢ፷")) else bstack11l1l11_opy_ (u"ࠢࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠣ፸")
        bstack1l1l1111111_opy_ = result.get(bstack11l1l11_opy_ (u"ࠣࡱࡸࡸࡨࡵ࡭ࡦࠤ፹"), TestFramework.bstack1l11l11lll1_opy_)
        if bstack1l1l1111111_opy_ != TestFramework.bstack1l11l11lll1_opy_:
            TestFramework.bstack1111111l1l_opy_(instance, TestFramework.bstack1ll11l111ll_opy_, datetime.now(tz=timezone.utc))
        TestFramework.bstack1l11llll1ll_opy_(instance, {
            TestFramework.bstack1l1l1lllll1_opy_: failure,
            TestFramework.bstack1l11l11l1l1_opy_: bstack1111ll1lll_opy_,
            TestFramework.bstack1l1ll1111ll_opy_: bstack1l1l1111111_opy_,
        })
    def __1l11l1ll1l1_opy_(
        self,
        context: bstack1l11lll1l11_opy_,
        test_framework_state: bstack1llllll1lll_opy_,
        test_hook_state: bstack1lll111lll1_opy_,
        *args,
        **kwargs,
    ):
        instance = None
        if test_framework_state == bstack1llllll1lll_opy_.SETUP_FIXTURE:
            instance = self.__1l11l1lllll_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        else:
            target = None # bstack1l11l1l11l1_opy_ bstack1l1l11111l1_opy_ this to be bstack11l1l11_opy_ (u"ࠤࡱࡳࡩ࡫ࡩࡥࠤ፺")
            if test_framework_state == bstack1llllll1lll_opy_.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__1l1l1111ll1_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == bstack1llllll1lll_opy_.LOG:
                nodeid = getattr(getattr(args[0], bstack11l1l11_opy_ (u"ࠥࡲࡴࡪࡥࠣ፻"), None), bstack11l1l11_opy_ (u"ࠦࡳࡵࡤࡦ࡫ࡧࠦ፼"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack11l1l11_opy_ (u"ࠧࡴ࡯ࡥࡧࠥ፽"), None):
                target = args[0].node.nodeid
            elif getattr(args[0], bstack11l1l11_opy_ (u"ࠨ࡮ࡰࡦࡨ࡭ࡩࠨ፾"), None):
                target = args[0].nodeid
            instance = TestFramework.bstack11111ll111_opy_(target) if target else None
        return instance
    def __1l11l1l1l1l_opy_(
        self,
        instance: bstack1lllllll111_opy_,
        test_framework_state: bstack1llllll1lll_opy_,
        test_hook_state: bstack1lll111lll1_opy_,
        *args,
    ):
        key = test_framework_state.name
        bstack1l1l11111ll_opy_ = TestFramework.bstack11111l1l1l_opy_(instance, PytestBDDFramework.bstack1l1l1111l11_opy_, {})
        if not key in bstack1l1l11111ll_opy_:
            bstack1l1l11111ll_opy_[key] = []
        bstack1l11ll1l1l1_opy_ = TestFramework.bstack11111l1l1l_opy_(instance, PytestBDDFramework.bstack1l11ll11l1l_opy_, {})
        if not key in bstack1l11ll1l1l1_opy_:
            bstack1l11ll1l1l1_opy_[key] = []
        bstack1l11l11llll_opy_ = {
            PytestBDDFramework.bstack1l1l1111l11_opy_: bstack1l1l11111ll_opy_,
            PytestBDDFramework.bstack1l11ll11l1l_opy_: bstack1l11ll1l1l1_opy_,
        }
        if test_hook_state == bstack1lll111lll1_opy_.PRE:
            hook_name = args[1] if len(args) > 1 else None
            hook = {
                bstack11l1l11_opy_ (u"ࠢ࡬ࡧࡼࠦ፿"): key,
                TestFramework.bstack1l11lll1lll_opy_: uuid4().__str__(),
                TestFramework.bstack1l11lll11ll_opy_: TestFramework.bstack1l11l1lll11_opy_,
                TestFramework.bstack1l11l11l1ll_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack1l11ll1ll11_opy_: [],
                TestFramework.bstack1l11ll11111_opy_: hook_name
            }
            bstack1l1l11111ll_opy_[key].append(hook)
            bstack1l11l11llll_opy_[PytestBDDFramework.bstack1l11llllll1_opy_] = key
        elif test_hook_state == bstack1lll111lll1_opy_.POST:
            bstack1l11ll11ll1_opy_ = bstack1l1l11111ll_opy_.get(key, [])
            hook = bstack1l11ll11ll1_opy_.pop() if bstack1l11ll11ll1_opy_ else None
            if hook:
                result = self.__1l11ll11lll_opy_(*args)
                if result:
                    bstack1l11l1l1l11_opy_ = result.get(bstack11l1l11_opy_ (u"ࠣࡱࡸࡸࡨࡵ࡭ࡦࠤᎀ"), TestFramework.bstack1l11l1lll11_opy_)
                    if bstack1l11l1l1l11_opy_ != TestFramework.bstack1l11l1lll11_opy_:
                        hook[TestFramework.bstack1l11lll11ll_opy_] = bstack1l11l1l1l11_opy_
                hook[TestFramework.bstack1l11l1l11ll_opy_] = datetime.now(tz=timezone.utc)
                bstack1l11ll1l1l1_opy_[key].append(hook)
                bstack1l11l11llll_opy_[PytestBDDFramework.bstack1l11l111lll_opy_] = key
        TestFramework.bstack1l11llll1ll_opy_(instance, bstack1l11l11llll_opy_)
        self.logger.debug(bstack11l1l11_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡪࡲࡳࡰࡥࡥࡷࡧࡱࡸ࠿ࠦࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥ࠾ࡽ࡮ࡩࡾࢃ࠮ࡼࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࢀࠤ࡭ࡵ࡯࡬ࡵࡢࡷࡹࡧࡲࡵࡧࡧࡁࢀ࡮࡯ࡰ࡭ࡶࡣࡸࡺࡡࡳࡶࡨࡨࢂࠦࡨࡰࡱ࡮ࡷࡤ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࠽ࠣᎁ") + str(bstack1l11ll1l1l1_opy_) + bstack11l1l11_opy_ (u"ࠥࠦᎂ"))
    def __1l11l1lllll_opy_(
        self,
        context: bstack1l11lll1l11_opy_,
        test_framework_state: bstack1llllll1lll_opy_,
        test_hook_state: bstack1lll111lll1_opy_,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack1ll111l111l_opy_(args[0], [bstack11l1l11_opy_ (u"ࠦࡸࡩ࡯ࡱࡧࠥᎃ"), bstack11l1l11_opy_ (u"ࠧࡧࡲࡨࡰࡤࡱࡪࠨᎄ"), bstack11l1l11_opy_ (u"ࠨࡰࡢࡴࡤࡱࡸࠨᎅ"), bstack11l1l11_opy_ (u"ࠢࡪࡦࡶࠦᎆ"), bstack11l1l11_opy_ (u"ࠣࡷࡱ࡭ࡹࡺࡥࡴࡶࠥᎇ"), bstack11l1l11_opy_ (u"ࠤࡥࡥࡸ࡫ࡩࡥࠤᎈ")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scenario = args[2] if len(args) == 3 else None
        scope = request.scope if hasattr(request, bstack11l1l11_opy_ (u"ࠥࡷࡨࡵࡰࡦࠤᎉ")) else fixturedef.get(bstack11l1l11_opy_ (u"ࠦࡸࡩ࡯ࡱࡧࠥᎊ"), None)
        fixturename = request.fixturename if hasattr(request, bstack11l1l11_opy_ (u"ࠧ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࠥᎋ")) else None
        node = request.node if hasattr(request, bstack11l1l11_opy_ (u"ࠨ࡮ࡰࡦࡨࠦᎌ")) else None
        target = request.node.nodeid if hasattr(node, bstack11l1l11_opy_ (u"ࠢ࡯ࡱࡧࡩ࡮ࡪࠢᎍ")) else None
        baseid = fixturedef.get(bstack11l1l11_opy_ (u"ࠣࡤࡤࡷࡪ࡯ࡤࠣᎎ"), None) or bstack11l1l11_opy_ (u"ࠤࠥᎏ")
        if (not target or len(baseid) > 0) and hasattr(request, bstack11l1l11_opy_ (u"ࠥࡣࡵࡿࡦࡶࡰࡦ࡭ࡹ࡫࡭ࠣ᎐")):
            target = PytestBDDFramework.__1l1l111l11l_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack11l1l11_opy_ (u"ࠦࡱࡵࡣࡢࡶ࡬ࡳࡳࠨ᎑")) else None
            if target and not TestFramework.bstack11111ll111_opy_(target):
                self.__1l1l1111ll1_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack11l1l11_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࡫ࡶࡦࡰࡷ࠾ࠥ࡬ࡡ࡭࡮ࡥࡥࡨࡱࠠࡵࡣࡵ࡫ࡪࡺ࠽ࡼࡶࡤࡶ࡬࡫ࡴࡾࠢࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫࠽ࡼࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࢃࠠ࡯ࡱࡧࡩࡂࢁ࡮ࡰࡦࡨࢁࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࠢ᎒") + str(test_hook_state) + bstack11l1l11_opy_ (u"ࠨࠢ᎓"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstack11l1l11_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡦࡪࡺࡷࡹࡷ࡫࡟ࡦࡸࡨࡲࡹࡀࠠࡶࡰ࡫ࡥࡳࡪ࡬ࡦࡦࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࢀࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫ࡽࠡࡨ࡬ࡼࡹࡻࡲࡦࡦࡨࡪࡂࢁࡦࡪࡺࡷࡹࡷ࡫ࡤࡦࡨࢀࠤࡸࡩ࡯ࡱࡧࡀࡿࡸࡩ࡯ࡱࡧࢀࠤࡹࡧࡲࡨࡧࡷࡁࠧ᎔") + str(target) + bstack11l1l11_opy_ (u"ࠣࠤ᎕"))
            return None
        instance = TestFramework.bstack11111ll111_opy_(target)
        if not instance:
            self.logger.warning(bstack11l1l11_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡨ࡬ࡼࡹࡻࡲࡦࡡࡨࡺࡪࡴࡴ࠻ࠢࡸࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࡻࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦࡿࠣࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥ࠾ࡽࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫ࡽࠡࡵࡦࡳࡵ࡫࠽ࡼࡵࡦࡳࡵ࡫ࡽࠡࡤࡤࡷࡪ࡯ࡤ࠾ࡽࡥࡥࡸ࡫ࡩࡥࡿࠣࡸࡦࡸࡧࡦࡶࡀࠦ᎖") + str(target) + bstack11l1l11_opy_ (u"ࠥࠦ᎗"))
            return None
        bstack1l11l1llll1_opy_ = TestFramework.bstack11111l1l1l_opy_(instance, PytestBDDFramework.bstack1l1l111l111_opy_, {})
        if os.getenv(bstack11l1l11_opy_ (u"ࠦࡘࡊࡋࡠࡅࡏࡍࡤࡌࡌࡂࡉࡢࡊࡎ࡞ࡔࡖࡔࡈࡗࠧ᎘"), bstack11l1l11_opy_ (u"ࠧ࠷ࠢ᎙")) == bstack11l1l11_opy_ (u"ࠨ࠱ࠣ᎚"):
            bstack1l11ll11l11_opy_ = bstack11l1l11_opy_ (u"ࠢ࠻ࠤ᎛").join((scope, fixturename))
            bstack1l1l111l1l1_opy_ = datetime.now(tz=timezone.utc)
            bstack1l11lll1l1l_opy_ = {
                bstack11l1l11_opy_ (u"ࠣ࡭ࡨࡽࠧ᎜"): bstack1l11ll11l11_opy_,
                bstack11l1l11_opy_ (u"ࠤࡷࡥ࡬ࡹࠢ᎝"): PytestBDDFramework.__1l11l11ll1l_opy_(request.node, scenario),
                bstack11l1l11_opy_ (u"ࠥࡪ࡮ࡾࡴࡶࡴࡨࠦ᎞"): fixturedef,
                bstack11l1l11_opy_ (u"ࠦࡸࡩ࡯ࡱࡧࠥ᎟"): scope,
                bstack11l1l11_opy_ (u"ࠧࡺࡹࡱࡧࠥᎠ"): None,
            }
            try:
                if test_hook_state == bstack1lll111lll1_opy_.POST and callable(getattr(args[-1], bstack11l1l11_opy_ (u"ࠨࡧࡦࡶࡢࡶࡪࡹࡵ࡭ࡶࠥᎡ"), None)):
                    bstack1l11lll1l1l_opy_[bstack11l1l11_opy_ (u"ࠢࡵࡻࡳࡩࠧᎢ")] = TestFramework.bstack1l1llll1l11_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == bstack1lll111lll1_opy_.PRE:
                bstack1l11lll1l1l_opy_[bstack11l1l11_opy_ (u"ࠣࡷࡸ࡭ࡩࠨᎣ")] = uuid4().__str__()
                bstack1l11lll1l1l_opy_[PytestBDDFramework.bstack1l11l11l1ll_opy_] = bstack1l1l111l1l1_opy_
            elif test_hook_state == bstack1lll111lll1_opy_.POST:
                bstack1l11lll1l1l_opy_[PytestBDDFramework.bstack1l11l1l11ll_opy_] = bstack1l1l111l1l1_opy_
            if bstack1l11ll11l11_opy_ in bstack1l11l1llll1_opy_:
                bstack1l11l1llll1_opy_[bstack1l11ll11l11_opy_].update(bstack1l11lll1l1l_opy_)
                self.logger.debug(bstack11l1l11_opy_ (u"ࠤࡸࡴࡩࡧࡴࡦࡦࠣࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥ࠾ࡽࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫ࡽࠡࡵࡦࡳࡵ࡫࠽ࡼࡵࡦࡳࡵ࡫ࡽࠡࡨ࡬ࡼࡹࡻࡲࡦ࠿ࠥᎤ") + str(bstack1l11l1llll1_opy_[bstack1l11ll11l11_opy_]) + bstack11l1l11_opy_ (u"ࠥࠦᎥ"))
            else:
                bstack1l11l1llll1_opy_[bstack1l11ll11l11_opy_] = bstack1l11lll1l1l_opy_
                self.logger.debug(bstack11l1l11_opy_ (u"ࠦࡸࡧࡶࡦࡦࠣࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥ࠾ࡽࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫ࡽࠡࡵࡦࡳࡵ࡫࠽ࡼࡵࡦࡳࡵ࡫ࡽࠡࡨ࡬ࡼࡹࡻࡲࡦ࠿ࡾࡸࡪࡹࡴࡠࡨ࡬ࡼࡹࡻࡲࡦࡿࠣࡸࡷࡧࡣ࡬ࡧࡧࡣ࡫࡯ࡸࡵࡷࡵࡩࡸࡃࠢᎦ") + str(len(bstack1l11l1llll1_opy_)) + bstack11l1l11_opy_ (u"ࠧࠨᎧ"))
        TestFramework.bstack1111111l1l_opy_(instance, PytestBDDFramework.bstack1l1l111l111_opy_, bstack1l11l1llll1_opy_)
        self.logger.debug(bstack11l1l11_opy_ (u"ࠨࡳࡢࡸࡨࡨࠥ࡬ࡩࡹࡶࡸࡶࡪࡹ࠽ࡼ࡮ࡨࡲ࠭ࡺࡲࡢࡥ࡮ࡩࡩࡥࡦࡪࡺࡷࡹࡷ࡫ࡳࠪࡿࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࠨᎨ") + str(instance.ref()) + bstack11l1l11_opy_ (u"ࠢࠣᎩ"))
        return instance
    def __1l1l1111ll1_opy_(
        self,
        context: bstack1l11lll1l11_opy_,
        test_framework_state: bstack1llllll1lll_opy_,
        target: Any,
        *args,
    ):
        ctx = bstack11111ll11l_opy_.create_context(target)
        ob = bstack1lllllll111_opy_(ctx, self.bstack1ll1lll11ll_opy_, self.bstack1l11l1ll1ll_opy_, test_framework_state)
        TestFramework.bstack1l11llll1ll_opy_(ob, {
            TestFramework.bstack1ll1l1llll1_opy_: context.test_framework_name,
            TestFramework.bstack1ll11111l11_opy_: context.test_framework_version,
            TestFramework.bstack1l11l1ll11l_opy_: [],
            PytestBDDFramework.bstack1l1l111l111_opy_: {},
            PytestBDDFramework.bstack1l11ll11l1l_opy_: {},
            PytestBDDFramework.bstack1l1l1111l11_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack1111111l1l_opy_(ob, TestFramework.bstack1l11llll1l1_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack1111111l1l_opy_(ob, TestFramework.bstack1ll1l11llll_opy_, context.platform_index)
        TestFramework.bstack1111111111_opy_[ctx.id] = ob
        self.logger.debug(bstack11l1l11_opy_ (u"ࠣࡵࡤࡺࡪࡪࠠࡪࡰࡶࡸࡦࡴࡣࡦࠢࡦࡸࡽ࠴ࡩࡥ࠿ࡾࡧࡹࡾ࠮ࡪࡦࢀࠤࡹࡧࡲࡨࡧࡷࡁࢀࡺࡡࡳࡩࡨࡸࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡹ࠽ࠣᎪ") + str(TestFramework.bstack1111111111_opy_.keys()) + bstack11l1l11_opy_ (u"ࠤࠥᎫ"))
        return ob
    @staticmethod
    def __1l11l11ll11_opy_(instance, args):
        request, feature, scenario = args
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack11l1l11_opy_ (u"ࠪ࡭ࡩ࠭Ꭼ"): id(step),
                bstack11l1l11_opy_ (u"ࠫࡹ࡫ࡸࡵࠩᎭ"): step.name,
                bstack11l1l11_opy_ (u"ࠬࡱࡥࡺࡹࡲࡶࡩ࠭Ꭾ"): step.keyword,
            })
        meta = {
            bstack11l1l11_opy_ (u"࠭ࡦࡦࡣࡷࡹࡷ࡫ࠧᎯ"): {
                bstack11l1l11_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᎰ"): feature.name,
                bstack11l1l11_opy_ (u"ࠨࡲࡤࡸ࡭࠭Ꮁ"): feature.filename,
                bstack11l1l11_opy_ (u"ࠩࡧࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠧᎲ"): feature.description
            },
            bstack11l1l11_opy_ (u"ࠪࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬᎳ"): {
                bstack11l1l11_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᎴ"): scenario.name
            },
            bstack11l1l11_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᎵ"): steps,
            bstack11l1l11_opy_ (u"࠭ࡥࡹࡣࡰࡴࡱ࡫ࡳࠨᎶ"): PytestBDDFramework.__1l11l111ll1_opy_(request.node)
        }
        instance.data.update(
            {
                TestFramework.bstack1l11lll11l1_opy_: meta
            }
        )
    @staticmethod
    def __1l1l1111l1l_opy_(instance, args):
        request, bstack1l11ll1ll1l_opy_ = args
        bstack1l11lllll11_opy_ = id(bstack1l11ll1ll1l_opy_)
        bstack1l1l1111lll_opy_ = instance.data[TestFramework.bstack1l11lll11l1_opy_]
        step = next(filter(lambda st: st[bstack11l1l11_opy_ (u"ࠧࡪࡦࠪᎷ")] == bstack1l11lllll11_opy_, bstack1l1l1111lll_opy_[bstack11l1l11_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᎸ")]), None)
        step.update({
            bstack11l1l11_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭Ꮉ"): datetime.now(tz=timezone.utc)
        })
        index = next((i for i, st in enumerate(bstack1l1l1111lll_opy_[bstack11l1l11_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᎺ")]) if st[bstack11l1l11_opy_ (u"ࠫ࡮ࡪࠧᎻ")] == step[bstack11l1l11_opy_ (u"ࠬ࡯ࡤࠨᎼ")]), None)
        if index is not None:
            bstack1l1l1111lll_opy_[bstack11l1l11_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᎽ")][index] = step
        instance.data[TestFramework.bstack1l11lll11l1_opy_] = bstack1l1l1111lll_opy_
    @staticmethod
    def __1l11l1l111l_opy_(instance, args):
        bstack11l1l11_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡼ࡮ࡥ࡯ࠢ࡯ࡩࡳࠦࡡࡳࡩࡶࠤ࡮ࡹࠠ࠳࠮ࠣ࡭ࡹࠦࡳࡪࡩࡱ࡭࡫࡯ࡥࡴࠢࡷ࡬ࡪࡸࡥࠡ࡫ࡶࠤࡳࡵࠠࡦࡺࡦࡩࡵࡺࡩࡰࡰࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡣࡵ࡫ࡸࠦࡡࡳࡧࠣ࠱ࠥࡡࡲࡦࡳࡸࡩࡸࡺࠬࠡࡵࡷࡩࡵࡣࠊࠡࠢࠣࠤࠥࠦࠠࠡ࡫ࡩࠤࡦࡸࡧࡴࠢࡤࡶࡪࠦ࠳ࠡࡶ࡫ࡩࡳࠦࡴࡩࡧࠣࡰࡦࡹࡴࠡࡸࡤࡰࡺ࡫ࠠࡪࡵࠣࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥᎾ")
        bstack1l11ll1l11l_opy_ = datetime.now(tz=timezone.utc)
        request = args[0]
        bstack1l11ll1ll1l_opy_ = args[1]
        bstack1l11lllll11_opy_ = id(bstack1l11ll1ll1l_opy_)
        bstack1l1l1111lll_opy_ = instance.data[TestFramework.bstack1l11lll11l1_opy_]
        step = None
        if bstack1l11lllll11_opy_ is not None and bstack1l1l1111lll_opy_.get(bstack11l1l11_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᎿ")):
            step = next(filter(lambda st: st[bstack11l1l11_opy_ (u"ࠩ࡬ࡨࠬᏀ")] == bstack1l11lllll11_opy_, bstack1l1l1111lll_opy_[bstack11l1l11_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᏁ")]), None)
            step.update({
                bstack11l1l11_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᏂ"): bstack1l11ll1l11l_opy_,
            })
        if len(args) > 2:
            exception = args[2]
            step.update({
                bstack11l1l11_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬᏃ"): bstack11l1l11_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭Ꮔ"),
                bstack11l1l11_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࠨᏅ"): str(exception)
            })
        else:
            if step is not None:
                step.update({
                    bstack11l1l11_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᏆ"): bstack11l1l11_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩᏇ"),
                })
        index = next((i for i, st in enumerate(bstack1l1l1111lll_opy_[bstack11l1l11_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᏈ")]) if st[bstack11l1l11_opy_ (u"ࠫ࡮ࡪࠧᏉ")] == step[bstack11l1l11_opy_ (u"ࠬ࡯ࡤࠨᏊ")]), None)
        if index is not None:
            bstack1l1l1111lll_opy_[bstack11l1l11_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᏋ")][index] = step
        instance.data[TestFramework.bstack1l11lll11l1_opy_] = bstack1l1l1111lll_opy_
    @staticmethod
    def __1l11l111ll1_opy_(node):
        try:
            examples = []
            if hasattr(node, bstack11l1l11_opy_ (u"ࠧࡤࡣ࡯ࡰࡸࡶࡥࡤࠩᏌ")):
                examples = list(node.callspec.params[bstack11l1l11_opy_ (u"ࠨࡡࡳࡽࡹ࡫ࡳࡵࡡࡥࡨࡩࡥࡥࡹࡣࡰࡴࡱ࡫ࠧᏍ")].values())
            return examples
        except:
            return []
    def bstack1l1lllllll1_opy_(self, instance: bstack1lllllll111_opy_, bstack1111l1ll11_opy_: Tuple[bstack1llllll1lll_opy_, bstack1lll111lll1_opy_]):
        bstack1l11ll111l1_opy_ = (
            PytestBDDFramework.bstack1l11llllll1_opy_
            if bstack1111l1ll11_opy_[1] == bstack1lll111lll1_opy_.PRE
            else PytestBDDFramework.bstack1l11l111lll_opy_
        )
        hook = PytestBDDFramework.bstack1l11l1l1lll_opy_(instance, bstack1l11ll111l1_opy_)
        entries = hook.get(TestFramework.bstack1l11ll1ll11_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack11111l1l1l_opy_(instance, TestFramework.bstack1l11l1ll11l_opy_, []))
        return entries
    def bstack1ll11111111_opy_(self, instance: bstack1lllllll111_opy_, bstack1111l1ll11_opy_: Tuple[bstack1llllll1lll_opy_, bstack1lll111lll1_opy_]):
        bstack1l11ll111l1_opy_ = (
            PytestBDDFramework.bstack1l11llllll1_opy_
            if bstack1111l1ll11_opy_[1] == bstack1lll111lll1_opy_.PRE
            else PytestBDDFramework.bstack1l11l111lll_opy_
        )
        PytestBDDFramework.bstack1l11ll1lll1_opy_(instance, bstack1l11ll111l1_opy_)
        TestFramework.bstack11111l1l1l_opy_(instance, TestFramework.bstack1l11l1ll11l_opy_, []).clear()
    @staticmethod
    def bstack1l11l1l1lll_opy_(instance: bstack1lllllll111_opy_, bstack1l11ll111l1_opy_: str):
        bstack1l11l11l111_opy_ = (
            PytestBDDFramework.bstack1l11ll11l1l_opy_
            if bstack1l11ll111l1_opy_ == PytestBDDFramework.bstack1l11l111lll_opy_
            else PytestBDDFramework.bstack1l1l1111l11_opy_
        )
        bstack1l11ll1l1ll_opy_ = TestFramework.bstack11111l1l1l_opy_(instance, bstack1l11ll111l1_opy_, None)
        bstack1l11l11l11l_opy_ = TestFramework.bstack11111l1l1l_opy_(instance, bstack1l11l11l111_opy_, None) if bstack1l11ll1l1ll_opy_ else None
        return (
            bstack1l11l11l11l_opy_[bstack1l11ll1l1ll_opy_][-1]
            if isinstance(bstack1l11l11l11l_opy_, dict) and len(bstack1l11l11l11l_opy_.get(bstack1l11ll1l1ll_opy_, [])) > 0
            else None
        )
    @staticmethod
    def bstack1l11ll1lll1_opy_(instance: bstack1lllllll111_opy_, bstack1l11ll111l1_opy_: str):
        hook = PytestBDDFramework.bstack1l11l1l1lll_opy_(instance, bstack1l11ll111l1_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack1l11ll1ll11_opy_, []).clear()
    @staticmethod
    def __1l11l1l1111_opy_(instance: bstack1lllllll111_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack11l1l11_opy_ (u"ࠤࡪࡩࡹࡥࡲࡦࡥࡲࡶࡩࡹࠢᏎ"), None)):
            return
        if os.getenv(bstack11l1l11_opy_ (u"ࠥࡗࡉࡑ࡟ࡄࡎࡌࡣࡋࡒࡁࡈࡡࡏࡓࡌ࡙ࠢᏏ"), bstack11l1l11_opy_ (u"ࠦ࠶ࠨᏐ")) != bstack11l1l11_opy_ (u"ࠧ࠷ࠢᏑ"):
            PytestBDDFramework.logger.warning(bstack11l1l11_opy_ (u"ࠨࡩࡨࡰࡲࡶ࡮ࡴࡧࠡࡥࡤࡴࡱࡵࡧࠣᏒ"))
            return
        bstack1l11llll11l_opy_ = {
            bstack11l1l11_opy_ (u"ࠢࡴࡧࡷࡹࡵࠨᏓ"): (PytestBDDFramework.bstack1l11llllll1_opy_, PytestBDDFramework.bstack1l1l1111l11_opy_),
            bstack11l1l11_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࠥᏔ"): (PytestBDDFramework.bstack1l11l111lll_opy_, PytestBDDFramework.bstack1l11ll11l1l_opy_),
        }
        for when in (bstack11l1l11_opy_ (u"ࠤࡶࡩࡹࡻࡰࠣᏕ"), bstack11l1l11_opy_ (u"ࠥࡧࡦࡲ࡬ࠣᏖ"), bstack11l1l11_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࠨᏗ")):
            bstack1l11lll1111_opy_ = args[1].get_records(when)
            if not bstack1l11lll1111_opy_:
                continue
            records = [
                bstack1lll11ll111_opy_(
                    kind=TestFramework.bstack1ll11l1l11l_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack11l1l11_opy_ (u"ࠧࡲࡥࡷࡧ࡯ࡲࡦࡳࡥࠣᏘ")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack11l1l11_opy_ (u"ࠨࡣࡳࡧࡤࡸࡪࡪࠢᏙ")) and r.created
                        else None
                    ),
                )
                for r in bstack1l11lll1111_opy_
                if isinstance(getattr(r, bstack11l1l11_opy_ (u"ࠢ࡮ࡧࡶࡷࡦ࡭ࡥࠣᏚ"), None), str) and r.message.strip()
            ]
            if not records:
                continue
            bstack1l11llll111_opy_, bstack1l11l11l111_opy_ = bstack1l11llll11l_opy_.get(when, (None, None))
            bstack1l11l1lll1l_opy_ = TestFramework.bstack11111l1l1l_opy_(instance, bstack1l11llll111_opy_, None) if bstack1l11llll111_opy_ else None
            bstack1l11l11l11l_opy_ = TestFramework.bstack11111l1l1l_opy_(instance, bstack1l11l11l111_opy_, None) if bstack1l11l1lll1l_opy_ else None
            if isinstance(bstack1l11l11l11l_opy_, dict) and len(bstack1l11l11l11l_opy_.get(bstack1l11l1lll1l_opy_, [])) > 0:
                hook = bstack1l11l11l11l_opy_[bstack1l11l1lll1l_opy_][-1]
                if isinstance(hook, dict) and TestFramework.bstack1l11ll1ll11_opy_ in hook:
                    hook[TestFramework.bstack1l11ll1ll11_opy_].extend(records)
                    continue
            logs = TestFramework.bstack11111l1l1l_opy_(instance, TestFramework.bstack1l11l1ll11l_opy_, [])
            logs.extend(records)
    @staticmethod
    def __1l11lll1ll1_opy_(args) -> Dict[str, Any]:
        request, feature, scenario = args
        bstack1l1l1ll1l_opy_ = request.node.nodeid
        test_name = PytestBDDFramework.__1l11l1ll111_opy_(request.node, scenario)
        bstack1l1l111111l_opy_ = feature.filename
        if not bstack1l1l1ll1l_opy_ or not test_name or not bstack1l1l111111l_opy_:
            return None
        code = None
        return {
            TestFramework.bstack1ll1lll11l1_opy_: uuid4().__str__(),
            TestFramework.bstack1l11ll1llll_opy_: bstack1l1l1ll1l_opy_,
            TestFramework.bstack1ll1l11l111_opy_: test_name,
            TestFramework.bstack1l1lll11lll_opy_: bstack1l1l1ll1l_opy_,
            TestFramework.bstack1l1l111ll11_opy_: bstack1l1l111111l_opy_,
            TestFramework.bstack1l11ll1l111_opy_: PytestBDDFramework.__1l11l11ll1l_opy_(feature, scenario),
            TestFramework.bstack1l11ll1111l_opy_: code,
            TestFramework.bstack1l1ll1111ll_opy_: TestFramework.bstack1l11l11lll1_opy_,
            TestFramework.bstack1l1l11llll1_opy_: test_name
        }
    @staticmethod
    def __1l11l1ll111_opy_(node, scenario):
        if hasattr(node, bstack11l1l11_opy_ (u"ࠨࡥࡤࡰࡱࡹࡰࡦࡥࠪᏛ")):
            parts = node.nodeid.rsplit(bstack11l1l11_opy_ (u"ࠤ࡞ࠦᏜ"))
            params = parts[-1]
            return bstack11l1l11_opy_ (u"ࠥࡿࢂ࡛ࠦࡼࡿࠥᏝ").format(scenario.name, params)
        return scenario.name
    @staticmethod
    def __1l11l11ll1l_opy_(feature, scenario) -> List[str]:
        return (list(feature.tags) if hasattr(feature, bstack11l1l11_opy_ (u"ࠫࡹࡧࡧࡴࠩᏞ")) else []) + (list(scenario.tags) if hasattr(scenario, bstack11l1l11_opy_ (u"ࠬࡺࡡࡨࡵࠪᏟ")) else [])
    @staticmethod
    def __1l1l111l11l_opy_(location):
        return bstack11l1l11_opy_ (u"ࠨ࠺࠻ࠤᏠ").join(filter(lambda x: isinstance(x, str), location))
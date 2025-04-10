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
from datetime import datetime, timezone
from uuid import uuid4
from typing import Dict, List, Any, Tuple
from browserstack_sdk.sdk_cli.bstack111111ll11_opy_ import bstack11111111l1_opy_
from browserstack_sdk.sdk_cli.utils.bstack11ll1l111_opy_ import bstack1l111ll111l_opy_
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    bstack1lllllll1ll_opy_,
    bstack1lll1l1l1l1_opy_,
    bstack1lll1l11l1l_opy_,
    bstack1l111lll1l1_opy_,
    bstack1llll1l1lll_opy_,
)
import traceback
from bstack_utils.helper import bstack1ll1111ll11_opy_
from bstack_utils.bstack1l111l1111_opy_ import bstack1lll111l11l_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.utils.bstack1lll1llll1l_opy_ import bstack1lllll11111_opy_
from browserstack_sdk.sdk_cli.bstack1111l1ll11_opy_ import bstack1111l1llll_opy_
bstack1l1lll11l1l_opy_ = bstack1ll1111ll11_opy_()
bstack1l1lllll111_opy_ = bstack1ll1l1_opy_ (u"ࠣࡗࡳࡰࡴࡧࡤࡦࡦࡄࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹ࠭ࠣ፤")
bstack1l11l11ll1l_opy_ = bstack1ll1l1_opy_ (u"ࠤࡋࡳࡴࡱࡌࡦࡸࡨࡰࠧ፥")
bstack1l11l111l1l_opy_ = bstack1ll1l1_opy_ (u"ࠥࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࡈࡰࡱ࡮ࡉࡻ࡫࡮ࡵࠤ፦")
bstack1l11lll1lll_opy_ = 1.0
_1ll111ll11l_opy_ = set()
class PytestBDDFramework(TestFramework):
    bstack1l11ll1ll1l_opy_ = bstack1ll1l1_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡩ࡭ࡽࡺࡵࡳࡧࡶࠦ፧")
    bstack1l11l11llll_opy_ = bstack1ll1l1_opy_ (u"ࠧࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡴࡡࡶࡸࡦࡸࡴࡦࡦࠥ፨")
    bstack1l11l1l1ll1_opy_ = bstack1ll1l1_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡵࡢࡪ࡮ࡴࡩࡴࡪࡨࡨࠧ፩")
    bstack1l111ll1ll1_opy_ = bstack1ll1l1_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡰࡦࡹࡴࡠࡵࡷࡥࡷࡺࡥࡥࠤ፪")
    bstack1l111ll1l1l_opy_ = bstack1ll1l1_opy_ (u"ࠣࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡱࡧࡳࡵࡡࡩ࡭ࡳ࡯ࡳࡩࡧࡧࠦ፫")
    bstack1l11l1l1111_opy_: bool
    bstack1111l1ll11_opy_: bstack1111l1llll_opy_  = None
    bstack1l11ll111l1_opy_ = [
        bstack1lllllll1ll_opy_.BEFORE_ALL,
        bstack1lllllll1ll_opy_.AFTER_ALL,
        bstack1lllllll1ll_opy_.BEFORE_EACH,
        bstack1lllllll1ll_opy_.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack1l11llll1ll_opy_: Dict[str, str],
        bstack1ll1l1l1111_opy_: List[str]=[bstack1ll1l1_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠨ፬")],
        bstack1111l1ll11_opy_: bstack1111l1llll_opy_ = None,
        bstack1llllll1ll1_opy_=None
    ):
        super().__init__(bstack1ll1l1l1111_opy_, bstack1l11llll1ll_opy_, bstack1111l1ll11_opy_)
        self.bstack1l11l1l1111_opy_ = any(bstack1ll1l1_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠢ፭") in item.lower() for item in bstack1ll1l1l1111_opy_)
        self.bstack1llllll1ll1_opy_ = bstack1llllll1ll1_opy_
    def track_event(
        self,
        context: bstack1l111lll1l1_opy_,
        test_framework_state: bstack1lllllll1ll_opy_,
        test_hook_state: bstack1lll1l11l1l_opy_,
        *args,
        **kwargs,
    ):
        super().track_event(self, context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == bstack1lllllll1ll_opy_.TEST or test_framework_state in PytestBDDFramework.bstack1l11ll111l1_opy_:
            bstack1l111ll111l_opy_(test_framework_state, test_hook_state)
        if test_framework_state == bstack1lllllll1ll_opy_.NONE:
            self.logger.warning(bstack1ll1l1_opy_ (u"ࠦ࡮࡭࡮ࡰࡴࡨࡨࠥࡩࡡ࡭࡮ࡥࡥࡨࡱࠠࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾࠢࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࡁࠧ፮") + str(test_hook_state) + bstack1ll1l1_opy_ (u"ࠧࠨ፯"))
            return
        if not self.bstack1l11l1l1111_opy_:
            self.logger.warning(bstack1ll1l1_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡻ࡮ࡴࡷࡳࡴࡴࡸࡴࡦࡦࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡃࠢ፰") + str(str(self.bstack1ll1l1l1111_opy_)) + bstack1ll1l1_opy_ (u"ࠢࠣ፱"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack1ll1l1_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡦࡸࡨࡲࡹࡀࠠࡶࡰࡨࡼࡵ࡫ࡣࡵࡧࡧࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥ፲") + str(kwargs) + bstack1ll1l1_opy_ (u"ࠤࠥ፳"))
            return
        instance = self.__1l11llll1l1_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack1ll1l1_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡨࡺࡪࡴࡴ࠻ࠢࡸࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࡻࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦࡿࠣࡥࡷ࡭ࡳ࠾ࠤ፴") + str(args) + bstack1ll1l1_opy_ (u"ࠦࠧ፵"))
            return
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.bstack1l11ll111l1_opy_ and test_hook_state == bstack1lll1l11l1l_opy_.PRE:
                bstack1ll1l1l111l_opy_ = bstack1lll111l11l_opy_.bstack1ll1ll111ll_opy_(EVENTS.bstack1l1ll1ll_opy_.value)
                name = str(EVENTS.bstack1l1ll1ll_opy_.name)+bstack1ll1l1_opy_ (u"ࠧࡀࠢ፶")+str(test_framework_state.name)
                TestFramework.bstack1l11l111lll_opy_(instance, name, bstack1ll1l1l111l_opy_)
        except Exception as e:
            self.logger.debug(bstack1ll1l1_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡮࡯ࡰ࡭ࠣࡩࡷࡸ࡯ࡳࠢࡳࡶࡪࡀࠠࡼࡿࠥ፷").format(e))
        try:
            if test_framework_state == bstack1lllllll1ll_opy_.TEST:
                if not TestFramework.bstack11111l1l1l_opy_(instance, TestFramework.bstack1l111l1ll1l_opy_) and test_hook_state == bstack1lll1l11l1l_opy_.PRE:
                    if not (len(args) >= 3):
                        return
                    test = PytestBDDFramework.__1l11l1l1l11_opy_(args)
                    if test:
                        instance.data.update(test)
                        self.logger.debug(bstack1ll1l1_opy_ (u"ࠢ࡭ࡱࡤࡨࡪࡪࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾ࡭ࡳࡹࡴࡢࡰࡦࡩ࠳ࡸࡥࡧࠪࠬࢁࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࠢ፸") + str(test_hook_state) + bstack1ll1l1_opy_ (u"ࠣࠤ፹"))
                if test_hook_state == bstack1lll1l11l1l_opy_.PRE and not TestFramework.bstack11111l1l1l_opy_(instance, TestFramework.bstack1l1lllll1l1_opy_):
                    TestFramework.bstack1111111111_opy_(instance, TestFramework.bstack1l1lllll1l1_opy_, datetime.now(tz=timezone.utc))
                    PytestBDDFramework.__1l11ll11lll_opy_(instance, args)
                    self.logger.debug(bstack1ll1l1_opy_ (u"ࠤࡶࡩࡹࠦࡴࡦࡵࡷ࠱ࡸࡺࡡࡳࡶࠣࡪࡴࡸࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾ࡭ࡳࡹࡴࡢࡰࡦࡩ࠳ࡸࡥࡧࠪࠬࢁࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࠢ፺") + str(test_hook_state) + bstack1ll1l1_opy_ (u"ࠥࠦ፻"))
                elif test_hook_state == bstack1lll1l11l1l_opy_.POST and not TestFramework.bstack11111l1l1l_opy_(instance, TestFramework.bstack1ll11111l1l_opy_):
                    TestFramework.bstack1111111111_opy_(instance, TestFramework.bstack1ll11111l1l_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1ll1l1_opy_ (u"ࠦࡸ࡫ࡴࠡࡶࡨࡷࡹ࠳ࡥ࡯ࡦࠣࡪࡴࡸࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾ࡭ࡳࡹࡴࡢࡰࡦࡩ࠳ࡸࡥࡧࠪࠬࢁࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࠢ፼") + str(test_hook_state) + bstack1ll1l1_opy_ (u"ࠧࠨ፽"))
            elif test_framework_state == bstack1lllllll1ll_opy_.STEP:
                if test_hook_state == bstack1lll1l11l1l_opy_.PRE:
                    PytestBDDFramework.__1l11l1l1l1l_opy_(instance, args)
                elif test_hook_state == bstack1lll1l11l1l_opy_.POST:
                    PytestBDDFramework.__1l11l11lll1_opy_(instance, args)
            elif test_framework_state == bstack1lllllll1ll_opy_.LOG and test_hook_state == bstack1lll1l11l1l_opy_.POST:
                PytestBDDFramework.__1l11l1lll1l_opy_(instance, *args)
            elif test_framework_state == bstack1lllllll1ll_opy_.LOG_REPORT and test_hook_state == bstack1lll1l11l1l_opy_.POST:
                self.__1l111lll11l_opy_(instance, *args)
                self.__1l111ll11ll_opy_(instance)
            elif test_framework_state in PytestBDDFramework.bstack1l11ll111l1_opy_:
                self.__1l11lll11l1_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack1ll1l1_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥ࡮ࡡ࡯ࡦ࡯ࡩࡩࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࡼࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࢀࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࠢ፾") + str(instance.ref()) + bstack1ll1l1_opy_ (u"ࠢࠣ፿"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack1l111llllll_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.bstack1l11ll111l1_opy_ and test_hook_state == bstack1lll1l11l1l_opy_.POST:
                name = str(EVENTS.bstack1l1ll1ll_opy_.name)+bstack1ll1l1_opy_ (u"ࠣ࠼ࠥᎀ")+str(test_framework_state.name)
                bstack1ll1l1l111l_opy_ = TestFramework.bstack1l111l1llll_opy_(instance, name)
                bstack1lll111l11l_opy_.end(EVENTS.bstack1l1ll1ll_opy_.value, bstack1ll1l1l111l_opy_+bstack1ll1l1_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᎁ"), bstack1ll1l1l111l_opy_+bstack1ll1l1_opy_ (u"ࠥ࠾ࡪࡴࡤࠣᎂ"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack1ll1l1_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣ࡬ࡴࡵ࡫ࠡࡧࡵࡶࡴࡸ࠺ࠡࡽࢀࠦᎃ").format(e))
    def bstack1l1lllll11l_opy_(self):
        return self.bstack1l11l1l1111_opy_
    def __1l11ll1ll11_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack1ll1l1_opy_ (u"ࠧ࡭ࡥࡵࡡࡵࡩࡸࡻ࡬ࡵࠤᎄ"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack1ll111lll11_opy_(rep, [bstack1ll1l1_opy_ (u"ࠨࡷࡩࡧࡱࠦᎅ"), bstack1ll1l1_opy_ (u"ࠢࡰࡷࡷࡧࡴࡳࡥࠣᎆ"), bstack1ll1l1_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣᎇ"), bstack1ll1l1_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤᎈ"), bstack1ll1l1_opy_ (u"ࠥࡷࡰ࡯ࡰࡱࡧࡧࠦᎉ"), bstack1ll1l1_opy_ (u"ࠦࡱࡵ࡮ࡨࡴࡨࡴࡷࡺࡥࡹࡶࠥᎊ")])
        return None
    def __1l111lll11l_opy_(self, instance: bstack1lll1l1l1l1_opy_, *args):
        result = self.__1l11ll1ll11_opy_(*args)
        if not result:
            return
        failure = None
        bstack1111ll1l11_opy_ = None
        if result.get(bstack1ll1l1_opy_ (u"ࠧࡵࡵࡵࡥࡲࡱࡪࠨᎋ"), None) == bstack1ll1l1_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨᎌ") and len(args) > 1 and getattr(args[1], bstack1ll1l1_opy_ (u"ࠢࡦࡺࡦ࡭ࡳ࡬࡯ࠣᎍ"), None) is not None:
            failure = [{bstack1ll1l1_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫᎎ"): [args[1].excinfo.exconly(), result.get(bstack1ll1l1_opy_ (u"ࠤ࡯ࡳࡳ࡭ࡲࡦࡲࡵࡸࡪࡾࡴࠣᎏ"), None)]}]
            bstack1111ll1l11_opy_ = bstack1ll1l1_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࡋࡲࡳࡱࡵࠦ᎐") if bstack1ll1l1_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࠢ᎑") in getattr(args[1].excinfo, bstack1ll1l1_opy_ (u"ࠧࡺࡹࡱࡧࡱࡥࡲ࡫ࠢ᎒"), bstack1ll1l1_opy_ (u"ࠨࠢ᎓")) else bstack1ll1l1_opy_ (u"ࠢࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠣ᎔")
        bstack1l11ll111ll_opy_ = result.get(bstack1ll1l1_opy_ (u"ࠣࡱࡸࡸࡨࡵ࡭ࡦࠤ᎕"), TestFramework.bstack1l11lll11ll_opy_)
        if bstack1l11ll111ll_opy_ != TestFramework.bstack1l11lll11ll_opy_:
            TestFramework.bstack1111111111_opy_(instance, TestFramework.bstack1l1lll111l1_opy_, datetime.now(tz=timezone.utc))
        TestFramework.bstack1l11lll1111_opy_(instance, {
            TestFramework.bstack1l1l1ll1111_opy_: failure,
            TestFramework.bstack1l111ll1lll_opy_: bstack1111ll1l11_opy_,
            TestFramework.bstack1l1l1lll111_opy_: bstack1l11ll111ll_opy_,
        })
    def __1l11llll1l1_opy_(
        self,
        context: bstack1l111lll1l1_opy_,
        test_framework_state: bstack1lllllll1ll_opy_,
        test_hook_state: bstack1lll1l11l1l_opy_,
        *args,
        **kwargs,
    ):
        instance = None
        if test_framework_state == bstack1lllllll1ll_opy_.SETUP_FIXTURE:
            instance = self.__1l111ll11l1_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        else:
            target = None # bstack1l11l111l11_opy_ bstack1l11l1l1lll_opy_ this to be bstack1ll1l1_opy_ (u"ࠤࡱࡳࡩ࡫ࡩࡥࠤ᎖")
            if test_framework_state == bstack1lllllll1ll_opy_.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__1l111lll1ll_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == bstack1lllllll1ll_opy_.LOG:
                nodeid = getattr(getattr(args[0], bstack1ll1l1_opy_ (u"ࠥࡲࡴࡪࡥࠣ᎗"), None), bstack1ll1l1_opy_ (u"ࠦࡳࡵࡤࡦ࡫ࡧࠦ᎘"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack1ll1l1_opy_ (u"ࠧࡴ࡯ࡥࡧࠥ᎙"), None):
                target = args[0].node.nodeid
            elif getattr(args[0], bstack1ll1l1_opy_ (u"ࠨ࡮ࡰࡦࡨ࡭ࡩࠨ᎚"), None):
                target = args[0].nodeid
            instance = TestFramework.bstack11111l1111_opy_(target) if target else None
        return instance
    def __1l11lll11l1_opy_(
        self,
        instance: bstack1lll1l1l1l1_opy_,
        test_framework_state: bstack1lllllll1ll_opy_,
        test_hook_state: bstack1lll1l11l1l_opy_,
        *args,
    ):
        key = test_framework_state.name
        bstack1l11lll111l_opy_ = TestFramework.bstack11111lllll_opy_(instance, PytestBDDFramework.bstack1l11l11llll_opy_, {})
        if not key in bstack1l11lll111l_opy_:
            bstack1l11lll111l_opy_[key] = []
        bstack1l11l1llll1_opy_ = TestFramework.bstack11111lllll_opy_(instance, PytestBDDFramework.bstack1l11l1l1ll1_opy_, {})
        if not key in bstack1l11l1llll1_opy_:
            bstack1l11l1llll1_opy_[key] = []
        bstack1l11ll1l11l_opy_ = {
            PytestBDDFramework.bstack1l11l11llll_opy_: bstack1l11lll111l_opy_,
            PytestBDDFramework.bstack1l11l1l1ll1_opy_: bstack1l11l1llll1_opy_,
        }
        if test_hook_state == bstack1lll1l11l1l_opy_.PRE:
            hook_name = args[1] if len(args) > 1 else None
            hook = {
                bstack1ll1l1_opy_ (u"ࠢ࡬ࡧࡼࠦ᎛"): key,
                TestFramework.bstack1l11l11l1ll_opy_: uuid4().__str__(),
                TestFramework.bstack1l11ll1l1ll_opy_: TestFramework.bstack1l11l11111l_opy_,
                TestFramework.bstack1l11lll1ll1_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack1l11lll1l11_opy_: [],
                TestFramework.bstack1l11llll11l_opy_: hook_name,
                TestFramework.bstack1l11l11l11l_opy_: bstack1lllll11111_opy_.bstack1l11llll111_opy_()
            }
            bstack1l11lll111l_opy_[key].append(hook)
            bstack1l11ll1l11l_opy_[PytestBDDFramework.bstack1l111ll1ll1_opy_] = key
        elif test_hook_state == bstack1lll1l11l1l_opy_.POST:
            bstack1l111ll1111_opy_ = bstack1l11lll111l_opy_.get(key, [])
            hook = bstack1l111ll1111_opy_.pop() if bstack1l111ll1111_opy_ else None
            if hook:
                result = self.__1l11ll1ll11_opy_(*args)
                if result:
                    bstack1l11lllll1l_opy_ = result.get(bstack1ll1l1_opy_ (u"ࠣࡱࡸࡸࡨࡵ࡭ࡦࠤ᎜"), TestFramework.bstack1l11l11111l_opy_)
                    if bstack1l11lllll1l_opy_ != TestFramework.bstack1l11l11111l_opy_:
                        hook[TestFramework.bstack1l11ll1l1ll_opy_] = bstack1l11lllll1l_opy_
                hook[TestFramework.bstack1l11ll1111l_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack1l11l11l11l_opy_] = bstack1lllll11111_opy_.bstack1l11llll111_opy_()
                self.bstack1l11lll1l1l_opy_(hook)
                logs = hook.get(TestFramework.bstack1l11lllll11_opy_, [])
                self.bstack1l1llll1lll_opy_(instance, logs)
                bstack1l11l1llll1_opy_[key].append(hook)
                bstack1l11ll1l11l_opy_[PytestBDDFramework.bstack1l111ll1l1l_opy_] = key
        TestFramework.bstack1l11lll1111_opy_(instance, bstack1l11ll1l11l_opy_)
        self.logger.debug(bstack1ll1l1_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡪࡲࡳࡰࡥࡥࡷࡧࡱࡸ࠿ࠦࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥ࠾ࡽ࡮ࡩࡾࢃ࠮ࡼࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࢀࠤ࡭ࡵ࡯࡬ࡵࡢࡷࡹࡧࡲࡵࡧࡧࡁࢀ࡮࡯ࡰ࡭ࡶࡣࡸࡺࡡࡳࡶࡨࡨࢂࠦࡨࡰࡱ࡮ࡷࡤ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࠽ࠣ᎝") + str(bstack1l11l1llll1_opy_) + bstack1ll1l1_opy_ (u"ࠥࠦ᎞"))
    def __1l111ll11l1_opy_(
        self,
        context: bstack1l111lll1l1_opy_,
        test_framework_state: bstack1lllllll1ll_opy_,
        test_hook_state: bstack1lll1l11l1l_opy_,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack1ll111lll11_opy_(args[0], [bstack1ll1l1_opy_ (u"ࠦࡸࡩ࡯ࡱࡧࠥ᎟"), bstack1ll1l1_opy_ (u"ࠧࡧࡲࡨࡰࡤࡱࡪࠨᎠ"), bstack1ll1l1_opy_ (u"ࠨࡰࡢࡴࡤࡱࡸࠨᎡ"), bstack1ll1l1_opy_ (u"ࠢࡪࡦࡶࠦᎢ"), bstack1ll1l1_opy_ (u"ࠣࡷࡱ࡭ࡹࡺࡥࡴࡶࠥᎣ"), bstack1ll1l1_opy_ (u"ࠤࡥࡥࡸ࡫ࡩࡥࠤᎤ")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scenario = args[2] if len(args) == 3 else None
        scope = request.scope if hasattr(request, bstack1ll1l1_opy_ (u"ࠥࡷࡨࡵࡰࡦࠤᎥ")) else fixturedef.get(bstack1ll1l1_opy_ (u"ࠦࡸࡩ࡯ࡱࡧࠥᎦ"), None)
        fixturename = request.fixturename if hasattr(request, bstack1ll1l1_opy_ (u"ࠧ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࠥᎧ")) else None
        node = request.node if hasattr(request, bstack1ll1l1_opy_ (u"ࠨ࡮ࡰࡦࡨࠦᎨ")) else None
        target = request.node.nodeid if hasattr(node, bstack1ll1l1_opy_ (u"ࠢ࡯ࡱࡧࡩ࡮ࡪࠢᎩ")) else None
        baseid = fixturedef.get(bstack1ll1l1_opy_ (u"ࠣࡤࡤࡷࡪ࡯ࡤࠣᎪ"), None) or bstack1ll1l1_opy_ (u"ࠤࠥᎫ")
        if (not target or len(baseid) > 0) and hasattr(request, bstack1ll1l1_opy_ (u"ࠥࡣࡵࡿࡦࡶࡰࡦ࡭ࡹ࡫࡭ࠣᎬ")):
            target = PytestBDDFramework.__1l11ll1l1l1_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack1ll1l1_opy_ (u"ࠦࡱࡵࡣࡢࡶ࡬ࡳࡳࠨᎭ")) else None
            if target and not TestFramework.bstack11111l1111_opy_(target):
                self.__1l111lll1ll_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack1ll1l1_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࡫ࡶࡦࡰࡷ࠾ࠥ࡬ࡡ࡭࡮ࡥࡥࡨࡱࠠࡵࡣࡵ࡫ࡪࡺ࠽ࡼࡶࡤࡶ࡬࡫ࡴࡾࠢࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫࠽ࡼࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࢃࠠ࡯ࡱࡧࡩࡂࢁ࡮ࡰࡦࡨࢁࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࠢᎮ") + str(test_hook_state) + bstack1ll1l1_opy_ (u"ࠨࠢᎯ"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstack1ll1l1_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡦࡪࡺࡷࡹࡷ࡫࡟ࡦࡸࡨࡲࡹࡀࠠࡶࡰ࡫ࡥࡳࡪ࡬ࡦࡦࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࢀࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫ࡽࠡࡨ࡬ࡼࡹࡻࡲࡦࡦࡨࡪࡂࢁࡦࡪࡺࡷࡹࡷ࡫ࡤࡦࡨࢀࠤࡸࡩ࡯ࡱࡧࡀࡿࡸࡩ࡯ࡱࡧࢀࠤࡹࡧࡲࡨࡧࡷࡁࠧᎰ") + str(target) + bstack1ll1l1_opy_ (u"ࠣࠤᎱ"))
            return None
        instance = TestFramework.bstack11111l1111_opy_(target)
        if not instance:
            self.logger.warning(bstack1ll1l1_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡨ࡬ࡼࡹࡻࡲࡦࡡࡨࡺࡪࡴࡴ࠻ࠢࡸࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࡻࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦࡿࠣࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥ࠾ࡽࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫ࡽࠡࡵࡦࡳࡵ࡫࠽ࡼࡵࡦࡳࡵ࡫ࡽࠡࡤࡤࡷࡪ࡯ࡤ࠾ࡽࡥࡥࡸ࡫ࡩࡥࡿࠣࡸࡦࡸࡧࡦࡶࡀࠦᎲ") + str(target) + bstack1ll1l1_opy_ (u"ࠥࠦᎳ"))
            return None
        bstack1l111ll1l11_opy_ = TestFramework.bstack11111lllll_opy_(instance, PytestBDDFramework.bstack1l11ll1ll1l_opy_, {})
        if os.getenv(bstack1ll1l1_opy_ (u"ࠦࡘࡊࡋࡠࡅࡏࡍࡤࡌࡌࡂࡉࡢࡊࡎ࡞ࡔࡖࡔࡈࡗࠧᎴ"), bstack1ll1l1_opy_ (u"ࠧ࠷ࠢᎵ")) == bstack1ll1l1_opy_ (u"ࠨ࠱ࠣᎶ"):
            bstack1l11l1l11ll_opy_ = bstack1ll1l1_opy_ (u"ࠢ࠻ࠤᎷ").join((scope, fixturename))
            bstack1l11l1lllll_opy_ = datetime.now(tz=timezone.utc)
            bstack1l11l111111_opy_ = {
                bstack1ll1l1_opy_ (u"ࠣ࡭ࡨࡽࠧᎸ"): bstack1l11l1l11ll_opy_,
                bstack1ll1l1_opy_ (u"ࠤࡷࡥ࡬ࡹࠢᎹ"): PytestBDDFramework.__1l11l1l11l1_opy_(request.node, scenario),
                bstack1ll1l1_opy_ (u"ࠥࡪ࡮ࡾࡴࡶࡴࡨࠦᎺ"): fixturedef,
                bstack1ll1l1_opy_ (u"ࠦࡸࡩ࡯ࡱࡧࠥᎻ"): scope,
                bstack1ll1l1_opy_ (u"ࠧࡺࡹࡱࡧࠥᎼ"): None,
            }
            try:
                if test_hook_state == bstack1lll1l11l1l_opy_.POST and callable(getattr(args[-1], bstack1ll1l1_opy_ (u"ࠨࡧࡦࡶࡢࡶࡪࡹࡵ࡭ࡶࠥᎽ"), None)):
                    bstack1l11l111111_opy_[bstack1ll1l1_opy_ (u"ࠢࡵࡻࡳࡩࠧᎾ")] = TestFramework.bstack1ll11l11111_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == bstack1lll1l11l1l_opy_.PRE:
                bstack1l11l111111_opy_[bstack1ll1l1_opy_ (u"ࠣࡷࡸ࡭ࡩࠨᎿ")] = uuid4().__str__()
                bstack1l11l111111_opy_[PytestBDDFramework.bstack1l11lll1ll1_opy_] = bstack1l11l1lllll_opy_
            elif test_hook_state == bstack1lll1l11l1l_opy_.POST:
                bstack1l11l111111_opy_[PytestBDDFramework.bstack1l11ll1111l_opy_] = bstack1l11l1lllll_opy_
            if bstack1l11l1l11ll_opy_ in bstack1l111ll1l11_opy_:
                bstack1l111ll1l11_opy_[bstack1l11l1l11ll_opy_].update(bstack1l11l111111_opy_)
                self.logger.debug(bstack1ll1l1_opy_ (u"ࠤࡸࡴࡩࡧࡴࡦࡦࠣࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥ࠾ࡽࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫ࡽࠡࡵࡦࡳࡵ࡫࠽ࡼࡵࡦࡳࡵ࡫ࡽࠡࡨ࡬ࡼࡹࡻࡲࡦ࠿ࠥᏀ") + str(bstack1l111ll1l11_opy_[bstack1l11l1l11ll_opy_]) + bstack1ll1l1_opy_ (u"ࠥࠦᏁ"))
            else:
                bstack1l111ll1l11_opy_[bstack1l11l1l11ll_opy_] = bstack1l11l111111_opy_
                self.logger.debug(bstack1ll1l1_opy_ (u"ࠦࡸࡧࡶࡦࡦࠣࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥ࠾ࡽࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫ࡽࠡࡵࡦࡳࡵ࡫࠽ࡼࡵࡦࡳࡵ࡫ࡽࠡࡨ࡬ࡼࡹࡻࡲࡦ࠿ࡾࡸࡪࡹࡴࡠࡨ࡬ࡼࡹࡻࡲࡦࡿࠣࡸࡷࡧࡣ࡬ࡧࡧࡣ࡫࡯ࡸࡵࡷࡵࡩࡸࡃࠢᏂ") + str(len(bstack1l111ll1l11_opy_)) + bstack1ll1l1_opy_ (u"ࠧࠨᏃ"))
        TestFramework.bstack1111111111_opy_(instance, PytestBDDFramework.bstack1l11ll1ll1l_opy_, bstack1l111ll1l11_opy_)
        self.logger.debug(bstack1ll1l1_opy_ (u"ࠨࡳࡢࡸࡨࡨࠥ࡬ࡩࡹࡶࡸࡶࡪࡹ࠽ࡼ࡮ࡨࡲ࠭ࡺࡲࡢࡥ࡮ࡩࡩࡥࡦࡪࡺࡷࡹࡷ࡫ࡳࠪࡿࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࠨᏄ") + str(instance.ref()) + bstack1ll1l1_opy_ (u"ࠢࠣᏅ"))
        return instance
    def __1l111lll1ll_opy_(
        self,
        context: bstack1l111lll1l1_opy_,
        test_framework_state: bstack1lllllll1ll_opy_,
        target: Any,
        *args,
    ):
        ctx = bstack11111111l1_opy_.create_context(target)
        ob = bstack1lll1l1l1l1_opy_(ctx, self.bstack1ll1l1l1111_opy_, self.bstack1l11llll1ll_opy_, test_framework_state)
        TestFramework.bstack1l11lll1111_opy_(ob, {
            TestFramework.bstack1ll1ll1l1ll_opy_: context.test_framework_name,
            TestFramework.bstack1ll111l1lll_opy_: context.test_framework_version,
            TestFramework.bstack1l11l1ll11l_opy_: [],
            PytestBDDFramework.bstack1l11ll1ll1l_opy_: {},
            PytestBDDFramework.bstack1l11l1l1ll1_opy_: {},
            PytestBDDFramework.bstack1l11l11llll_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack1111111111_opy_(ob, TestFramework.bstack1l11l1111ll_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack1111111111_opy_(ob, TestFramework.bstack1ll11llll1l_opy_, context.platform_index)
        TestFramework.bstack1llllllll1l_opy_[ctx.id] = ob
        self.logger.debug(bstack1ll1l1_opy_ (u"ࠣࡵࡤࡺࡪࡪࠠࡪࡰࡶࡸࡦࡴࡣࡦࠢࡦࡸࡽ࠴ࡩࡥ࠿ࡾࡧࡹࡾ࠮ࡪࡦࢀࠤࡹࡧࡲࡨࡧࡷࡁࢀࡺࡡࡳࡩࡨࡸࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡹ࠽ࠣᏆ") + str(TestFramework.bstack1llllllll1l_opy_.keys()) + bstack1ll1l1_opy_ (u"ࠤࠥᏇ"))
        return ob
    @staticmethod
    def __1l11ll11lll_opy_(instance, args):
        request, feature, scenario = args
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack1ll1l1_opy_ (u"ࠪ࡭ࡩ࠭Ꮘ"): id(step),
                bstack1ll1l1_opy_ (u"ࠫࡹ࡫ࡸࡵࠩᏉ"): step.name,
                bstack1ll1l1_opy_ (u"ࠬࡱࡥࡺࡹࡲࡶࡩ࠭Ꮚ"): step.keyword,
            })
        meta = {
            bstack1ll1l1_opy_ (u"࠭ࡦࡦࡣࡷࡹࡷ࡫ࠧᏋ"): {
                bstack1ll1l1_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᏌ"): feature.name,
                bstack1ll1l1_opy_ (u"ࠨࡲࡤࡸ࡭࠭Ꮝ"): feature.filename,
                bstack1ll1l1_opy_ (u"ࠩࡧࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠧᏎ"): feature.description
            },
            bstack1ll1l1_opy_ (u"ࠪࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬᏏ"): {
                bstack1ll1l1_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᏐ"): scenario.name
            },
            bstack1ll1l1_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᏑ"): steps,
            bstack1ll1l1_opy_ (u"࠭ࡥࡹࡣࡰࡴࡱ࡫ࡳࠨᏒ"): PytestBDDFramework.__1l11ll11l11_opy_(request.node)
        }
        instance.data.update(
            {
                TestFramework.bstack1l11l1ll1ll_opy_: meta
            }
        )
    def bstack1l11lll1l1l_opy_(self, hook: Dict[str, Any]) -> None:
        bstack1ll1l1_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡕࡸ࡯ࡤࡧࡶࡷࡪࡹࠠࡵࡪࡨࠤࡍࡵ࡯࡬ࡎࡨࡺࡪࡲࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷࠥࡹࡩ࡮࡫࡯ࡥࡷࠦࡴࡰࠢࡷ࡬ࡪࠦࡊࡢࡸࡤࠤ࡮ࡳࡰ࡭ࡧࡰࡩࡳࡺࡡࡵ࡫ࡲࡲ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡕࡪ࡬ࡷࠥࡳࡥࡵࡪࡲࡨ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡈ࡮ࡥࡤ࡭ࡶࠤࡹ࡮ࡥࠡࡊࡲࡳࡰࡒࡥࡷࡧ࡯ࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿࠠࡪࡰࡶ࡭ࡩ࡫ࠠࡿ࠱࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠱ࡘࡴࡱࡵࡡࡥࡧࡧࡅࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡇࡱࡵࠤࡪࡧࡣࡩࠢࡩ࡭ࡱ࡫ࠠࡪࡰࠣ࡬ࡴࡵ࡫ࡠ࡮ࡨࡺࡪࡲ࡟ࡧ࡫࡯ࡩࡸ࠲ࠠࡳࡧࡳࡰࡦࡩࡥࡴࠢࠥࡘࡪࡹࡴࡍࡧࡹࡩࡱࠨࠠࡸ࡫ࡷ࡬ࠥࠨࡈࡰࡱ࡮ࡐࡪࡼࡥ࡭ࠤࠣ࡭ࡳࠦࡩࡵࡵࠣࡴࡦࡺࡨ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡊࡨࠣࡥࠥ࡬ࡩ࡭ࡧࠣ࡭ࡳࠦࡴࡩࡧࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾࠦ࡭ࡢࡶࡦ࡬ࡪࡹࠠࡢࠢࡰࡳࡩ࡯ࡦࡪࡧࡧࠤ࡭ࡵ࡯࡬࠯࡯ࡩࡻ࡫࡬ࠡࡨ࡬ࡰࡪ࠲ࠠࡪࡶࠣࡧࡷ࡫ࡡࡵࡧࡶࠤࡦࠦࡌࡰࡩࡈࡲࡹࡸࡹࠡࡱࡥ࡮ࡪࡩࡴࠡࡹ࡬ࡸ࡭ࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࠣࡨࡪࡺࡡࡪ࡮ࡶ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡗ࡮ࡳࡩ࡭ࡣࡵࡰࡾ࠲ࠠࡪࡶࠣࡴࡷࡵࡣࡦࡵࡶࡩࡸࠦࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠡ࡮ࡲࡧࡦࡺࡥࡥࠢ࡬ࡲࠥࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬࠰ࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࡍࡵ࡯࡬ࡇࡹࡩࡳࡺࠠࡣࡻࠣࡶࡪࡶ࡬ࡢࡥ࡬ࡲ࡬ࠦࠢࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࠦࠥࡽࡩࡵࡪࠣࠦࡍࡵ࡯࡬ࡎࡨࡺࡪࡲ࠯ࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࡌࡴࡵ࡫ࡆࡸࡨࡲࡹࠨ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡔࡩࡧࠣࡧࡷ࡫ࡡࡵࡧࡧࠤࡑࡵࡧࡆࡰࡷࡶࡾࠦ࡯ࡣ࡬ࡨࡧࡹࡹࠠࡢࡴࡨࠤࡦࡪࡤࡦࡦࠣࡸࡴࠦࡴࡩࡧࠣ࡬ࡴࡵ࡫ࠨࡵࠣࠦࡱࡵࡧࡴࠤࠣࡰ࡮ࡹࡴ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡅࡷ࡭ࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡩࡱࡲ࡯࠿ࠦࡔࡩࡧࠣࡩࡻ࡫࡮ࡵࠢࡧ࡭ࡨࡺࡩࡰࡰࡤࡶࡾࠦࡣࡰࡰࡷࡥ࡮ࡴࡩ࡯ࡩࠣࡩࡽ࡯ࡳࡵ࡫ࡱ࡫ࠥࡲ࡯ࡨࡵࠣࡥࡳࡪࠠࡩࡱࡲ࡯ࠥ࡯࡮ࡧࡱࡵࡱࡦࡺࡩࡰࡰ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࡫ࡳࡴࡱ࡟࡭ࡧࡹࡩࡱࡥࡦࡪ࡮ࡨࡷ࠿ࠦࡌࡪࡵࡷࠤࡴ࡬ࠠࡑࡣࡷ࡬ࠥࡵࡢ࡫ࡧࡦࡸࡸࠦࡦࡳࡱࡰࠤࡹ࡮ࡥࠡࡖࡨࡷࡹࡒࡥࡷࡧ࡯ࠤࡲࡵ࡮ࡪࡶࡲࡶ࡮ࡴࡧ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡣࡷ࡬ࡰࡩࡥ࡬ࡦࡸࡨࡰࡤ࡬ࡩ࡭ࡧࡶ࠾ࠥࡒࡩࡴࡶࠣࡳ࡫ࠦࡐࡢࡶ࡫ࠤࡴࡨࡪࡦࡥࡷࡷࠥ࡬ࡲࡰ࡯ࠣࡸ࡭࡫ࠠࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࠤࡲࡵ࡮ࡪࡶࡲࡶ࡮ࡴࡧ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨᏓ")
        global _1ll111ll11l_opy_
        platform_index = os.environ[bstack1ll1l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨᏔ")]
        bstack1ll11l1111l_opy_ = os.path.join(bstack1l1lll11l1l_opy_, (bstack1l1lllll111_opy_ + str(platform_index)), bstack1l11l11ll1l_opy_)
        if not os.path.exists(bstack1ll11l1111l_opy_) or not os.path.isdir(bstack1ll11l1111l_opy_):
            return
        logs = hook.get(bstack1ll1l1_opy_ (u"ࠤ࡯ࡳ࡬ࡹࠢᏕ"), [])
        with os.scandir(bstack1ll11l1111l_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _1ll111ll11l_opy_:
                    self.logger.info(bstack1ll1l1_opy_ (u"ࠥࡔࡦࡺࡨࠡࡣ࡯ࡶࡪࡧࡤࡺࠢࡳࡶࡴࡩࡥࡴࡵࡨࡨࠥࢁࡽࠣᏖ").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack1ll1l1_opy_ (u"ࠦࠧᏗ")
                    log_entry = bstack1llll1l1lll_opy_(
                        kind=bstack1ll1l1_opy_ (u"࡚ࠧࡅࡔࡖࡢࡅ࡙࡚ࡁࡄࡊࡐࡉࡓ࡚ࠢᏘ"),
                        message=bstack1ll1l1_opy_ (u"ࠨࠢᏙ"),
                        level=bstack1ll1l1_opy_ (u"ࠢࠣᏚ"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack1ll111l1l1l_opy_=entry.stat().st_size,
                        bstack1ll11111ll1_opy_=bstack1ll1l1_opy_ (u"ࠣࡏࡄࡒ࡚ࡇࡌࡠࡗࡓࡐࡔࡇࡄࠣᏛ"),
                        bstack1l11_opy_=os.path.abspath(entry.path),
                        bstack1l11l1l111l_opy_=hook.get(TestFramework.bstack1l11l11l1ll_opy_)
                    )
                    logs.append(log_entry)
                    _1ll111ll11l_opy_.add(abs_path)
        platform_index = os.environ[bstack1ll1l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩᏜ")]
        bstack1l111llll11_opy_ = os.path.join(bstack1l1lll11l1l_opy_, (bstack1l1lllll111_opy_ + str(platform_index)), bstack1l11l11ll1l_opy_, bstack1l11l111l1l_opy_)
        if not os.path.exists(bstack1l111llll11_opy_) or not os.path.isdir(bstack1l111llll11_opy_):
            self.logger.info(bstack1ll1l1_opy_ (u"ࠥࡒࡴࠦࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࡋࡳࡴࡱࡅࡷࡧࡱࡸࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾࠦࡦࡰࡷࡱࡨࠥࡧࡴ࠻ࠢࡾࢁࠧᏝ").format(bstack1l111llll11_opy_))
        else:
            self.logger.info(bstack1ll1l1_opy_ (u"ࠦࡕࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࡍࡵ࡯࡬ࡇࡹࡩࡳࡺࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷࠥ࡬ࡲࡰ࡯ࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾࡀࠠࡼࡿࠥᏞ").format(bstack1l111llll11_opy_))
            with os.scandir(bstack1l111llll11_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _1ll111ll11l_opy_:
                        self.logger.info(bstack1ll1l1_opy_ (u"ࠧࡖࡡࡵࡪࠣࡥࡱࡸࡥࡢࡦࡼࠤࡵࡸ࡯ࡤࡧࡶࡷࡪࡪࠠࡼࡿࠥᏟ").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack1ll1l1_opy_ (u"ࠨࠢᏠ")
                        log_entry = bstack1llll1l1lll_opy_(
                            kind=bstack1ll1l1_opy_ (u"ࠢࡕࡇࡖࡘࡤࡇࡔࡕࡃࡆࡌࡒࡋࡎࡕࠤᏡ"),
                            message=bstack1ll1l1_opy_ (u"ࠣࠤᏢ"),
                            level=bstack1ll1l1_opy_ (u"ࠤࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࠨᏣ"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack1ll111l1l1l_opy_=entry.stat().st_size,
                            bstack1ll11111ll1_opy_=bstack1ll1l1_opy_ (u"ࠥࡑࡆࡔࡕࡂࡎࡢ࡙ࡕࡒࡏࡂࡆࠥᏤ"),
                            bstack1l11_opy_=os.path.abspath(entry.path),
                            bstack1ll11111111_opy_=hook.get(TestFramework.bstack1l11l11l1ll_opy_)
                        )
                        logs.append(log_entry)
                        _1ll111ll11l_opy_.add(abs_path)
        hook[bstack1ll1l1_opy_ (u"ࠦࡱࡵࡧࡴࠤᏥ")] = logs
    def bstack1l1llll1lll_opy_(
        self,
        bstack1l1lll1l11l_opy_: bstack1lll1l1l1l1_opy_,
        entries: List[bstack1llll1l1lll_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack1ll1l1_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡒࡉࡠࡄࡌࡒࡤ࡙ࡅࡔࡕࡌࡓࡓࡥࡉࡅࠤᏦ"))
        req.platform_index = TestFramework.bstack11111lllll_opy_(bstack1l1lll1l11l_opy_, TestFramework.bstack1ll11llll1l_opy_)
        req.execution_context.hash = str(bstack1l1lll1l11l_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l1lll1l11l_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l1lll1l11l_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack11111lllll_opy_(bstack1l1lll1l11l_opy_, TestFramework.bstack1ll1ll1l1ll_opy_)
            log_entry.test_framework_version = TestFramework.bstack11111lllll_opy_(bstack1l1lll1l11l_opy_, TestFramework.bstack1ll111l1lll_opy_)
            log_entry.uuid = entry.bstack1l11l1l111l_opy_
            log_entry.test_framework_state = bstack1l1lll1l11l_opy_.state.name
            log_entry.message = entry.message.encode(bstack1ll1l1_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧᏧ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            log_entry.level = bstack1ll1l1_opy_ (u"ࠢࠣᏨ")
            if entry.kind == bstack1ll1l1_opy_ (u"ࠣࡖࡈࡗ࡙ࡥࡁࡕࡖࡄࡇࡍࡓࡅࡏࡖࠥᏩ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1ll111l1l1l_opy_
                log_entry.file_path = entry.bstack1l11_opy_
        def bstack1l1llll1l11_opy_():
            bstack1ll11l1l1_opy_ = datetime.now()
            try:
                self.bstack1llllll1ll1_opy_.LogCreatedEvent(req)
                bstack1l1lll1l11l_opy_.bstack11lll1l111_opy_(bstack1ll1l1_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡴࡧࡱࡨࡤࡲ࡯ࡨࡡࡦࡶࡪࡧࡴࡦࡦࡢࡩࡻ࡫࡮ࡵࡡࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࠨᏪ"), datetime.now() - bstack1ll11l1l1_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1ll1l1_opy_ (u"ࠥࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࡴࡧࡱࡨࡤࡲ࡯ࡨࡡࡦࡶࡪࡧࡴࡦࡦࡢࡩࡻ࡫࡮ࡵࡡࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࠦࡻࡾࠤᏫ").format(str(e)))
                traceback.print_exc()
        self.bstack1111l1ll11_opy_.enqueue(bstack1l1llll1l11_opy_)
    def __1l111ll11ll_opy_(self, instance) -> None:
        bstack1ll1l1_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡎࡲࡥࡩࡹࠠࡤࡷࡶࡸࡴࡳࠠࡵࡣࡪࡷࠥ࡬࡯ࡳࠢࡷ࡬ࡪࠦࡧࡪࡸࡨࡲࠥࡺࡥࡴࡶࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡇࡷ࡫ࡡࡵࡧࡶࠤࡦࠦࡤࡪࡥࡷࠤࡨࡵ࡮ࡵࡣ࡬ࡲ࡮ࡴࡧࠡࡶࡨࡷࡹࠦ࡬ࡦࡸࡨࡰࠥࡩࡵࡴࡶࡲࡱࠥࡳࡥࡵࡣࡧࡥࡹࡧࠠࡳࡧࡷࡶ࡮࡫ࡶࡦࡦࠣࡪࡷࡵ࡭ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡆࡹࡸࡺ࡯࡮ࡖࡤ࡫ࡒࡧ࡮ࡢࡩࡨࡶࠥࡧ࡮ࡥࠢࡸࡴࡩࡧࡴࡦࡵࠣࡸ࡭࡫ࠠࡪࡰࡶࡸࡦࡴࡣࡦࠢࡶࡸࡦࡺࡥࠡࡷࡶ࡭ࡳ࡭ࠠࡴࡧࡷࡣࡸࡺࡡࡵࡧࡢࡩࡳࡺࡲࡪࡧࡶ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤᏬ")
        bstack1l11ll1l11l_opy_ = {bstack1ll1l1_opy_ (u"ࠧࡩࡵࡴࡶࡲࡱࡤࡳࡥࡵࡣࡧࡥࡹࡧࠢᏭ"): bstack1lllll11111_opy_.bstack1l11llll111_opy_()}
        TestFramework.bstack1l11lll1111_opy_(instance, bstack1l11ll1l11l_opy_)
    @staticmethod
    def __1l11l1l1l1l_opy_(instance, args):
        request, bstack1l11ll1l111_opy_ = args
        bstack1l111l1ll11_opy_ = id(bstack1l11ll1l111_opy_)
        bstack1l11l111ll1_opy_ = instance.data[TestFramework.bstack1l11l1ll1ll_opy_]
        step = next(filter(lambda st: st[bstack1ll1l1_opy_ (u"࠭ࡩࡥࠩᏮ")] == bstack1l111l1ll11_opy_, bstack1l11l111ll1_opy_[bstack1ll1l1_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭Ꮿ")]), None)
        step.update({
            bstack1ll1l1_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᏰ"): datetime.now(tz=timezone.utc)
        })
        index = next((i for i, st in enumerate(bstack1l11l111ll1_opy_[bstack1ll1l1_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨᏱ")]) if st[bstack1ll1l1_opy_ (u"ࠪ࡭ࡩ࠭Ᏺ")] == step[bstack1ll1l1_opy_ (u"ࠫ࡮ࡪࠧᏳ")]), None)
        if index is not None:
            bstack1l11l111ll1_opy_[bstack1ll1l1_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᏴ")][index] = step
        instance.data[TestFramework.bstack1l11l1ll1ll_opy_] = bstack1l11l111ll1_opy_
    @staticmethod
    def __1l11l11lll1_opy_(instance, args):
        bstack1ll1l1_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡻ࡭࡫࡮ࠡ࡮ࡨࡲࠥࡧࡲࡨࡵࠣ࡭ࡸࠦ࠲࠭ࠢ࡬ࡸࠥࡹࡩࡨࡰ࡬ࡪ࡮࡫ࡳࠡࡶ࡫ࡩࡷ࡫ࠠࡪࡵࠣࡲࡴࠦࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡢࡴࡪࡷࠥࡧࡲࡦࠢ࠰ࠤࡠࡸࡥࡲࡷࡨࡷࡹ࠲ࠠࡴࡶࡨࡴࡢࠐࠠࠡࠢࠣࠤࠥࠦࠠࡪࡨࠣࡥࡷ࡭ࡳࠡࡣࡵࡩࠥ࠹ࠠࡵࡪࡨࡲࠥࡺࡨࡦࠢ࡯ࡥࡸࡺࠠࡷࡣ࡯ࡹࡪࠦࡩࡴࠢࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤᏵ")
        bstack1l11l11ll11_opy_ = datetime.now(tz=timezone.utc)
        request = args[0]
        bstack1l11ll1l111_opy_ = args[1]
        bstack1l111l1ll11_opy_ = id(bstack1l11ll1l111_opy_)
        bstack1l11l111ll1_opy_ = instance.data[TestFramework.bstack1l11l1ll1ll_opy_]
        step = None
        if bstack1l111l1ll11_opy_ is not None and bstack1l11l111ll1_opy_.get(bstack1ll1l1_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭᏶")):
            step = next(filter(lambda st: st[bstack1ll1l1_opy_ (u"ࠨ࡫ࡧࠫ᏷")] == bstack1l111l1ll11_opy_, bstack1l11l111ll1_opy_[bstack1ll1l1_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨᏸ")]), None)
            step.update({
                bstack1ll1l1_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᏹ"): bstack1l11l11ll11_opy_,
            })
        if len(args) > 2:
            exception = args[2]
            step.update({
                bstack1ll1l1_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫᏺ"): bstack1ll1l1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᏻ"),
                bstack1ll1l1_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧᏼ"): str(exception)
            })
        else:
            if step is not None:
                step.update({
                    bstack1ll1l1_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᏽ"): bstack1ll1l1_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ᏾"),
                })
        index = next((i for i, st in enumerate(bstack1l11l111ll1_opy_[bstack1ll1l1_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨ᏿")]) if st[bstack1ll1l1_opy_ (u"ࠪ࡭ࡩ࠭᐀")] == step[bstack1ll1l1_opy_ (u"ࠫ࡮ࡪࠧᐁ")]), None)
        if index is not None:
            bstack1l11l111ll1_opy_[bstack1ll1l1_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᐂ")][index] = step
        instance.data[TestFramework.bstack1l11l1ll1ll_opy_] = bstack1l11l111ll1_opy_
    @staticmethod
    def __1l11ll11l11_opy_(node):
        try:
            examples = []
            if hasattr(node, bstack1ll1l1_opy_ (u"࠭ࡣࡢ࡮࡯ࡷࡵ࡫ࡣࠨᐃ")):
                examples = list(node.callspec.params[bstack1ll1l1_opy_ (u"ࠧࡠࡲࡼࡸࡪࡹࡴࡠࡤࡧࡨࡤ࡫ࡸࡢ࡯ࡳࡰࡪ࠭ᐄ")].values())
            return examples
        except:
            return []
    def bstack1ll111ll1l1_opy_(self, instance: bstack1lll1l1l1l1_opy_, bstack1111l1l11l_opy_: Tuple[bstack1lllllll1ll_opy_, bstack1lll1l11l1l_opy_]):
        bstack1l11ll11111_opy_ = (
            PytestBDDFramework.bstack1l111ll1ll1_opy_
            if bstack1111l1l11l_opy_[1] == bstack1lll1l11l1l_opy_.PRE
            else PytestBDDFramework.bstack1l111ll1l1l_opy_
        )
        hook = PytestBDDFramework.bstack1l11ll11l1l_opy_(instance, bstack1l11ll11111_opy_)
        entries = hook.get(TestFramework.bstack1l11lll1l11_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack11111lllll_opy_(instance, TestFramework.bstack1l11l1ll11l_opy_, []))
        return entries
    def bstack1ll111lll1l_opy_(self, instance: bstack1lll1l1l1l1_opy_, bstack1111l1l11l_opy_: Tuple[bstack1lllllll1ll_opy_, bstack1lll1l11l1l_opy_]):
        bstack1l11ll11111_opy_ = (
            PytestBDDFramework.bstack1l111ll1ll1_opy_
            if bstack1111l1l11l_opy_[1] == bstack1lll1l11l1l_opy_.PRE
            else PytestBDDFramework.bstack1l111ll1l1l_opy_
        )
        PytestBDDFramework.bstack1l111lll111_opy_(instance, bstack1l11ll11111_opy_)
        TestFramework.bstack11111lllll_opy_(instance, TestFramework.bstack1l11l1ll11l_opy_, []).clear()
    @staticmethod
    def bstack1l11ll11l1l_opy_(instance: bstack1lll1l1l1l1_opy_, bstack1l11ll11111_opy_: str):
        bstack1l111l1lll1_opy_ = (
            PytestBDDFramework.bstack1l11l1l1ll1_opy_
            if bstack1l11ll11111_opy_ == PytestBDDFramework.bstack1l111ll1l1l_opy_
            else PytestBDDFramework.bstack1l11l11llll_opy_
        )
        bstack1l11l1ll1l1_opy_ = TestFramework.bstack11111lllll_opy_(instance, bstack1l11ll11111_opy_, None)
        bstack1l11ll1llll_opy_ = TestFramework.bstack11111lllll_opy_(instance, bstack1l111l1lll1_opy_, None) if bstack1l11l1ll1l1_opy_ else None
        return (
            bstack1l11ll1llll_opy_[bstack1l11l1ll1l1_opy_][-1]
            if isinstance(bstack1l11ll1llll_opy_, dict) and len(bstack1l11ll1llll_opy_.get(bstack1l11l1ll1l1_opy_, [])) > 0
            else None
        )
    @staticmethod
    def bstack1l111lll111_opy_(instance: bstack1lll1l1l1l1_opy_, bstack1l11ll11111_opy_: str):
        hook = PytestBDDFramework.bstack1l11ll11l1l_opy_(instance, bstack1l11ll11111_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack1l11lll1l11_opy_, []).clear()
    @staticmethod
    def __1l11l1lll1l_opy_(instance: bstack1lll1l1l1l1_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack1ll1l1_opy_ (u"ࠣࡩࡨࡸࡤࡸࡥࡤࡱࡵࡨࡸࠨᐅ"), None)):
            return
        if os.getenv(bstack1ll1l1_opy_ (u"ࠤࡖࡈࡐࡥࡃࡍࡋࡢࡊࡑࡇࡇࡠࡎࡒࡋࡘࠨᐆ"), bstack1ll1l1_opy_ (u"ࠥ࠵ࠧᐇ")) != bstack1ll1l1_opy_ (u"ࠦ࠶ࠨᐈ"):
            PytestBDDFramework.logger.warning(bstack1ll1l1_opy_ (u"ࠧ࡯ࡧ࡯ࡱࡵ࡭ࡳ࡭ࠠࡤࡣࡳࡰࡴ࡭ࠢᐉ"))
            return
        bstack1l111llll1l_opy_ = {
            bstack1ll1l1_opy_ (u"ࠨࡳࡦࡶࡸࡴࠧᐊ"): (PytestBDDFramework.bstack1l111ll1ll1_opy_, PytestBDDFramework.bstack1l11l11llll_opy_),
            bstack1ll1l1_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࠤᐋ"): (PytestBDDFramework.bstack1l111ll1l1l_opy_, PytestBDDFramework.bstack1l11l1l1ll1_opy_),
        }
        for when in (bstack1ll1l1_opy_ (u"ࠣࡵࡨࡸࡺࡶࠢᐌ"), bstack1ll1l1_opy_ (u"ࠤࡦࡥࡱࡲࠢᐍ"), bstack1ll1l1_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࠧᐎ")):
            bstack1l11ll11ll1_opy_ = args[1].get_records(when)
            if not bstack1l11ll11ll1_opy_:
                continue
            records = [
                bstack1llll1l1lll_opy_(
                    kind=TestFramework.bstack1l1lll1ll11_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack1ll1l1_opy_ (u"ࠦࡱ࡫ࡶࡦ࡮ࡱࡥࡲ࡫ࠢᐏ")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack1ll1l1_opy_ (u"ࠧࡩࡲࡦࡣࡷࡩࡩࠨᐐ")) and r.created
                        else None
                    ),
                )
                for r in bstack1l11ll11ll1_opy_
                if isinstance(getattr(r, bstack1ll1l1_opy_ (u"ࠨ࡭ࡦࡵࡶࡥ࡬࡫ࠢᐑ"), None), str) and r.message.strip()
            ]
            if not records:
                continue
            bstack1l11l11l1l1_opy_, bstack1l111l1lll1_opy_ = bstack1l111llll1l_opy_.get(when, (None, None))
            bstack1l11ll1lll1_opy_ = TestFramework.bstack11111lllll_opy_(instance, bstack1l11l11l1l1_opy_, None) if bstack1l11l11l1l1_opy_ else None
            bstack1l11ll1llll_opy_ = TestFramework.bstack11111lllll_opy_(instance, bstack1l111l1lll1_opy_, None) if bstack1l11ll1lll1_opy_ else None
            if isinstance(bstack1l11ll1llll_opy_, dict) and len(bstack1l11ll1llll_opy_.get(bstack1l11ll1lll1_opy_, [])) > 0:
                hook = bstack1l11ll1llll_opy_[bstack1l11ll1lll1_opy_][-1]
                if isinstance(hook, dict) and TestFramework.bstack1l11lll1l11_opy_ in hook:
                    hook[TestFramework.bstack1l11lll1l11_opy_].extend(records)
                    continue
            logs = TestFramework.bstack11111lllll_opy_(instance, TestFramework.bstack1l11l1ll11l_opy_, [])
            logs.extend(records)
    @staticmethod
    def __1l11l1l1l11_opy_(args) -> Dict[str, Any]:
        request, feature, scenario = args
        bstack11l11l1l1l_opy_ = request.node.nodeid
        test_name = PytestBDDFramework.__1l11l11l111_opy_(request.node, scenario)
        bstack1l111lllll1_opy_ = feature.filename
        if not bstack11l11l1l1l_opy_ or not test_name or not bstack1l111lllll1_opy_:
            return None
        code = None
        return {
            TestFramework.bstack1ll1ll1ll11_opy_: uuid4().__str__(),
            TestFramework.bstack1l111l1ll1l_opy_: bstack11l11l1l1l_opy_,
            TestFramework.bstack1ll1ll1l1l1_opy_: test_name,
            TestFramework.bstack1l1ll1lll1l_opy_: bstack11l11l1l1l_opy_,
            TestFramework.bstack1l11l1lll11_opy_: bstack1l111lllll1_opy_,
            TestFramework.bstack1l11l1111l1_opy_: PytestBDDFramework.__1l11l1l11l1_opy_(feature, scenario),
            TestFramework.bstack1l11l1ll111_opy_: code,
            TestFramework.bstack1l1l1lll111_opy_: TestFramework.bstack1l11lll11ll_opy_,
            TestFramework.bstack1l1l111l1ll_opy_: test_name
        }
    @staticmethod
    def __1l11l11l111_opy_(node, scenario):
        if hasattr(node, bstack1ll1l1_opy_ (u"ࠧࡤࡣ࡯ࡰࡸࡶࡥࡤࠩᐒ")):
            parts = node.nodeid.rsplit(bstack1ll1l1_opy_ (u"ࠣ࡝ࠥᐓ"))
            params = parts[-1]
            return bstack1ll1l1_opy_ (u"ࠤࡾࢁࠥࡡࡻࡾࠤᐔ").format(scenario.name, params)
        return scenario.name
    @staticmethod
    def __1l11l1l11l1_opy_(feature, scenario) -> List[str]:
        return (list(feature.tags) if hasattr(feature, bstack1ll1l1_opy_ (u"ࠪࡸࡦ࡭ࡳࠨᐕ")) else []) + (list(scenario.tags) if hasattr(scenario, bstack1ll1l1_opy_ (u"ࠫࡹࡧࡧࡴࠩᐖ")) else [])
    @staticmethod
    def __1l11ll1l1l1_opy_(location):
        return bstack1ll1l1_opy_ (u"ࠧࡀ࠺ࠣᐗ").join(filter(lambda x: isinstance(x, str), location))
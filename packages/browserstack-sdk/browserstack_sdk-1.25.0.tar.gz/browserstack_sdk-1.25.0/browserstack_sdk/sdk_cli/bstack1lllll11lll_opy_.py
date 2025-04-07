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
from bstack_utils.bstack11l111ll1l_opy_ import bstack11l11l11_opy_
class bstack1llll1111ll_opy_(TestFramework):
    bstack1l1l111l111_opy_ = bstack11l1l11_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡬ࡩࡹࡶࡸࡶࡪࡹࠢᏡ")
    bstack1l1l1111l11_opy_ = bstack11l1l11_opy_ (u"ࠣࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡷࡤࡹࡴࡢࡴࡷࡩࡩࠨᏢ")
    bstack1l11ll11l1l_opy_ = bstack11l1l11_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡸࡥࡦࡪࡰ࡬ࡷ࡭࡫ࡤࠣᏣ")
    bstack1l11llllll1_opy_ = bstack11l1l11_opy_ (u"ࠥࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥ࡬ࡢࡵࡷࡣࡸࡺࡡࡳࡶࡨࡨࠧᏤ")
    bstack1l11l111lll_opy_ = bstack11l1l11_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟࡭ࡣࡶࡸࡤ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪࠢᏥ")
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
        bstack1ll1lll11ll_opy_: List[str]=[bstack11l1l11_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸࠧᏦ")],
    ):
        super().__init__(bstack1ll1lll11ll_opy_, bstack1l11l1ll1ll_opy_)
        self.bstack1l11lllllll_opy_ = any(bstack11l1l11_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹࠨᏧ") in item.lower() for item in bstack1ll1lll11ll_opy_)
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
            self.logger.warning(bstack11l1l11_opy_ (u"ࠢࡪࡩࡱࡳࡷ࡫ࡤࠡࡥࡤࡰࡱࡨࡡࡤ࡭ࠣࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁࠥࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫࠽ࠣᏨ") + str(test_hook_state) + bstack11l1l11_opy_ (u"ࠣࠤᏩ"))
            return
        if not self.bstack1l11lllllll_opy_:
            self.logger.warning(bstack11l1l11_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡧࡹࡩࡳࡺ࠺ࠡࡷࡱࡷࡺࡶࡰࡰࡴࡷࡩࡩࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬࠿ࠥᏪ") + str(str(self.bstack1ll1lll11ll_opy_)) + bstack11l1l11_opy_ (u"ࠥࠦᏫ"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack11l1l11_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡹࡳ࡫ࡸࡱࡧࡦࡸࡪࡪࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨᏬ") + str(kwargs) + bstack11l1l11_opy_ (u"ࠧࠨᏭ"))
            return
        instance = self.__1l11l1ll1l1_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡻ࡮ࡩࡣࡱࡨࡱ࡫ࡤࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࡾࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࢂࠦࡡࡳࡩࡶࡁࠧᏮ") + str(args) + bstack11l1l11_opy_ (u"ࠢࠣᏯ"))
            return
        try:
            if instance!= None and test_framework_state in bstack1llll1111ll_opy_.bstack1l11lll111l_opy_ and test_hook_state == bstack1lll111lll1_opy_.PRE:
                bstack1ll1ll1l1l1_opy_ = bstack1lll1llll1l_opy_.bstack1ll1ll1lll1_opy_(EVENTS.bstack1lll1ll1ll_opy_.value)
                name = str(EVENTS.bstack1lll1ll1ll_opy_.name)+bstack11l1l11_opy_ (u"ࠣ࠼ࠥᏰ")+str(test_framework_state.name)
                TestFramework.bstack1l11ll111ll_opy_(instance, name, bstack1ll1ll1l1l1_opy_)
        except Exception as e:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡪࡲࡳࡰࠦࡥࡳࡴࡲࡶࠥࡶࡲࡦ࠼ࠣࡿࢂࠨᏱ").format(e))
        try:
            if not TestFramework.bstack1111111l11_opy_(instance, TestFramework.bstack1l11ll1llll_opy_) and test_hook_state == bstack1lll111lll1_opy_.PRE:
                test = bstack1llll1111ll_opy_.__1l11lll1ll1_opy_(args[0])
                if test:
                    instance.data.update(test)
                    self.logger.debug(bstack11l1l11_opy_ (u"ࠥࡰࡴࡧࡤࡦࡦࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡩ࡯ࡵࡷࡥࡳࡩࡥ࠯ࡴࡨࡪ࠭࠯ࡽࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࠥᏲ") + str(test_hook_state) + bstack11l1l11_opy_ (u"ࠦࠧᏳ"))
            if test_framework_state == bstack1llllll1lll_opy_.TEST:
                if test_hook_state == bstack1lll111lll1_opy_.PRE and not TestFramework.bstack1111111l11_opy_(instance, TestFramework.bstack1ll111111ll_opy_):
                    TestFramework.bstack1111111l1l_opy_(instance, TestFramework.bstack1ll111111ll_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack11l1l11_opy_ (u"ࠧࡹࡥࡵࠢࡷࡩࡸࡺ࠭ࡴࡶࡤࡶࡹࠦࡦࡰࡴࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡩ࡯ࡵࡷࡥࡳࡩࡥ࠯ࡴࡨࡪ࠭࠯ࡽࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࠥᏴ") + str(test_hook_state) + bstack11l1l11_opy_ (u"ࠨࠢᏵ"))
                elif test_hook_state == bstack1lll111lll1_opy_.POST and not TestFramework.bstack1111111l11_opy_(instance, TestFramework.bstack1ll111ll111_opy_):
                    TestFramework.bstack1111111l1l_opy_(instance, TestFramework.bstack1ll111ll111_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack11l1l11_opy_ (u"ࠢࡴࡧࡷࠤࡹ࡫ࡳࡵ࠯ࡨࡲࡩࠦࡦࡰࡴࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡩ࡯ࡵࡷࡥࡳࡩࡥ࠯ࡴࡨࡪ࠭࠯ࡽࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࠥ᏶") + str(test_hook_state) + bstack11l1l11_opy_ (u"ࠣࠤ᏷"))
            elif test_framework_state == bstack1llllll1lll_opy_.LOG and test_hook_state == bstack1lll111lll1_opy_.POST:
                bstack1llll1111ll_opy_.__1l11l1l1111_opy_(instance, *args)
            elif test_framework_state == bstack1llllll1lll_opy_.LOG_REPORT and test_hook_state == bstack1lll111lll1_opy_.POST:
                self.__1l1l111l1ll_opy_(instance, *args)
            elif test_framework_state in bstack1llll1111ll_opy_.bstack1l11lll111l_opy_:
                self.__1l11l1l1l1l_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack11l1l11_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡧࡹࡩࡳࡺ࠺ࠡࡪࡤࡲࡩࡲࡥࡥࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࡿࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࠥᏸ") + str(instance.ref()) + bstack11l1l11_opy_ (u"ࠥࠦᏹ"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack1l11l1l1ll1_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in bstack1llll1111ll_opy_.bstack1l11lll111l_opy_ and test_hook_state == bstack1lll111lll1_opy_.POST:
                name = str(EVENTS.bstack1lll1ll1ll_opy_.name)+bstack11l1l11_opy_ (u"ࠦ࠿ࠨᏺ")+str(test_framework_state.name)
                bstack1ll1ll1l1l1_opy_ = TestFramework.bstack1l11lllll1l_opy_(instance, name)
                bstack1lll1llll1l_opy_.end(EVENTS.bstack1lll1ll1ll_opy_.value, bstack1ll1ll1l1l1_opy_+bstack11l1l11_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧᏻ"), bstack1ll1ll1l1l1_opy_+bstack11l1l11_opy_ (u"ࠨ࠺ࡦࡰࡧࠦᏼ"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡨࡰࡱ࡮ࠤࡪࡸࡲࡰࡴ࠽ࠤࢀࢃࠢᏽ").format(e))
    def bstack1l1llll1111_opy_(self):
        return self.bstack1l11lllllll_opy_
    def __1l11ll11lll_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack11l1l11_opy_ (u"ࠣࡩࡨࡸࡤࡸࡥࡴࡷ࡯ࡸࠧ᏾"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack1ll111l111l_opy_(rep, [bstack11l1l11_opy_ (u"ࠤࡺ࡬ࡪࡴࠢ᏿"), bstack11l1l11_opy_ (u"ࠥࡳࡺࡺࡣࡰ࡯ࡨࠦ᐀"), bstack11l1l11_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦᐁ"), bstack11l1l11_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧᐂ"), bstack11l1l11_opy_ (u"ࠨࡳ࡬࡫ࡳࡴࡪࡪࠢᐃ"), bstack11l1l11_opy_ (u"ࠢ࡭ࡱࡱ࡫ࡷ࡫ࡰࡳࡶࡨࡼࡹࠨᐄ")])
        return None
    def __1l1l111l1ll_opy_(self, instance: bstack1lllllll111_opy_, *args):
        result = self.__1l11ll11lll_opy_(*args)
        if not result:
            return
        failure = None
        bstack1111ll1lll_opy_ = None
        if result.get(bstack11l1l11_opy_ (u"ࠣࡱࡸࡸࡨࡵ࡭ࡦࠤᐅ"), None) == bstack11l1l11_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤᐆ") and len(args) > 1 and getattr(args[1], bstack11l1l11_opy_ (u"ࠥࡩࡽࡩࡩ࡯ࡨࡲࠦᐇ"), None) is not None:
            failure = [{bstack11l1l11_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧᐈ"): [args[1].excinfo.exconly(), result.get(bstack11l1l11_opy_ (u"ࠧࡲ࡯࡯ࡩࡵࡩࡵࡸࡴࡦࡺࡷࠦᐉ"), None)]}]
            bstack1111ll1lll_opy_ = bstack11l1l11_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࡇࡵࡶࡴࡸࠢᐊ") if bstack11l1l11_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࠥᐋ") in getattr(args[1].excinfo, bstack11l1l11_opy_ (u"ࠣࡶࡼࡴࡪࡴࡡ࡮ࡧࠥᐌ"), bstack11l1l11_opy_ (u"ࠤࠥᐍ")) else bstack11l1l11_opy_ (u"࡙ࠥࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡋࡲࡳࡱࡵࠦᐎ")
        bstack1l1l1111111_opy_ = result.get(bstack11l1l11_opy_ (u"ࠦࡴࡻࡴࡤࡱࡰࡩࠧᐏ"), TestFramework.bstack1l11l11lll1_opy_)
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
            target = None # bstack1l11l1l11l1_opy_ bstack1l1l11111l1_opy_ this to be bstack11l1l11_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࠧᐐ")
            if test_framework_state == bstack1llllll1lll_opy_.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__1l1l1111ll1_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == bstack1llllll1lll_opy_.LOG:
                nodeid = getattr(getattr(args[0], bstack11l1l11_opy_ (u"ࠨ࡮ࡰࡦࡨࠦᐑ"), None), bstack11l1l11_opy_ (u"ࠢ࡯ࡱࡧࡩ࡮ࡪࠢᐒ"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack11l1l11_opy_ (u"ࠣࡰࡲࡨࡪ࡯ࡤࠣᐓ"), None):
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
        bstack1l1l11111ll_opy_ = TestFramework.bstack11111l1l1l_opy_(instance, bstack1llll1111ll_opy_.bstack1l1l1111l11_opy_, {})
        if not key in bstack1l1l11111ll_opy_:
            bstack1l1l11111ll_opy_[key] = []
        bstack1l11ll1l1l1_opy_ = TestFramework.bstack11111l1l1l_opy_(instance, bstack1llll1111ll_opy_.bstack1l11ll11l1l_opy_, {})
        if not key in bstack1l11ll1l1l1_opy_:
            bstack1l11ll1l1l1_opy_[key] = []
        bstack1l11l11llll_opy_ = {
            bstack1llll1111ll_opy_.bstack1l1l1111l11_opy_: bstack1l1l11111ll_opy_,
            bstack1llll1111ll_opy_.bstack1l11ll11l1l_opy_: bstack1l11ll1l1l1_opy_,
        }
        if test_hook_state == bstack1lll111lll1_opy_.PRE:
            hook = {
                bstack11l1l11_opy_ (u"ࠤ࡮ࡩࡾࠨᐔ"): key,
                TestFramework.bstack1l11lll1lll_opy_: uuid4().__str__(),
                TestFramework.bstack1l11lll11ll_opy_: TestFramework.bstack1l11l1lll11_opy_,
                TestFramework.bstack1l11l11l1ll_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack1l11ll1ll11_opy_: [],
                TestFramework.bstack1l11ll11111_opy_: args[1] if len(args) > 1 else bstack11l1l11_opy_ (u"ࠪࠫᐕ")
            }
            bstack1l1l11111ll_opy_[key].append(hook)
            bstack1l11l11llll_opy_[bstack1llll1111ll_opy_.bstack1l11llllll1_opy_] = key
        elif test_hook_state == bstack1lll111lll1_opy_.POST:
            bstack1l11ll11ll1_opy_ = bstack1l1l11111ll_opy_.get(key, [])
            hook = bstack1l11ll11ll1_opy_.pop() if bstack1l11ll11ll1_opy_ else None
            if hook:
                result = self.__1l11ll11lll_opy_(*args)
                if result:
                    bstack1l11l1l1l11_opy_ = result.get(bstack11l1l11_opy_ (u"ࠦࡴࡻࡴࡤࡱࡰࡩࠧᐖ"), TestFramework.bstack1l11l1lll11_opy_)
                    if bstack1l11l1l1l11_opy_ != TestFramework.bstack1l11l1lll11_opy_:
                        hook[TestFramework.bstack1l11lll11ll_opy_] = bstack1l11l1l1l11_opy_
                hook[TestFramework.bstack1l11l1l11ll_opy_] = datetime.now(tz=timezone.utc)
                bstack1l11ll1l1l1_opy_[key].append(hook)
                bstack1l11l11llll_opy_[bstack1llll1111ll_opy_.bstack1l11l111lll_opy_] = key
        TestFramework.bstack1l11llll1ll_opy_(instance, bstack1l11l11llll_opy_)
        self.logger.debug(bstack11l1l11_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣ࡭ࡵ࡯࡬ࡡࡨࡺࡪࡴࡴ࠻ࠢࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࡁࢀࡱࡥࡺࡿ࠱ࡿࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡩࡱࡲ࡯ࡸࡥࡳࡵࡣࡵࡸࡪࡪ࠽ࡼࡪࡲࡳࡰࡹ࡟ࡴࡶࡤࡶࡹ࡫ࡤࡾࠢ࡫ࡳࡴࡱࡳࡠࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡀࠦᐗ") + str(bstack1l11ll1l1l1_opy_) + bstack11l1l11_opy_ (u"ࠨࠢᐘ"))
    def __1l11l1lllll_opy_(
        self,
        context: bstack1l11lll1l11_opy_,
        test_framework_state: bstack1llllll1lll_opy_,
        test_hook_state: bstack1lll111lll1_opy_,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack1ll111l111l_opy_(args[0], [bstack11l1l11_opy_ (u"ࠢࡴࡥࡲࡴࡪࠨᐙ"), bstack11l1l11_opy_ (u"ࠣࡣࡵ࡫ࡳࡧ࡭ࡦࠤᐚ"), bstack11l1l11_opy_ (u"ࠤࡳࡥࡷࡧ࡭ࡴࠤᐛ"), bstack11l1l11_opy_ (u"ࠥ࡭ࡩࡹࠢᐜ"), bstack11l1l11_opy_ (u"ࠦࡺࡴࡩࡵࡶࡨࡷࡹࠨᐝ"), bstack11l1l11_opy_ (u"ࠧࡨࡡࡴࡧ࡬ࡨࠧᐞ")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scope = request.scope if hasattr(request, bstack11l1l11_opy_ (u"ࠨࡳࡤࡱࡳࡩࠧᐟ")) else fixturedef.get(bstack11l1l11_opy_ (u"ࠢࡴࡥࡲࡴࡪࠨᐠ"), None)
        fixturename = request.fixturename if hasattr(request, bstack11l1l11_opy_ (u"ࠣࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࠨᐡ")) else None
        node = request.node if hasattr(request, bstack11l1l11_opy_ (u"ࠤࡱࡳࡩ࡫ࠢᐢ")) else None
        target = request.node.nodeid if hasattr(node, bstack11l1l11_opy_ (u"ࠥࡲࡴࡪࡥࡪࡦࠥᐣ")) else None
        baseid = fixturedef.get(bstack11l1l11_opy_ (u"ࠦࡧࡧࡳࡦ࡫ࡧࠦᐤ"), None) or bstack11l1l11_opy_ (u"ࠧࠨᐥ")
        if (not target or len(baseid) > 0) and hasattr(request, bstack11l1l11_opy_ (u"ࠨ࡟ࡱࡻࡩࡹࡳࡩࡩࡵࡧࡰࠦᐦ")):
            target = bstack1llll1111ll_opy_.__1l1l111l11l_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack11l1l11_opy_ (u"ࠢ࡭ࡱࡦࡥࡹ࡯࡯࡯ࠤᐧ")) else None
            if target and not TestFramework.bstack11111ll111_opy_(target):
                self.__1l1l1111ll1_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack11l1l11_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠࡧࡹࡩࡳࡺ࠺ࠡࡨࡤࡰࡱࡨࡡࡤ࡭ࠣࡸࡦࡸࡧࡦࡶࡀࡿࡹࡧࡲࡨࡧࡷࢁࠥ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࡀࡿ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦࡿࠣࡲࡴࡪࡥ࠾ࡽࡱࡳࡩ࡫ࡽࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࠥᐨ") + str(test_hook_state) + bstack11l1l11_opy_ (u"ࠤࠥᐩ"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstack11l1l11_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡩ࡭ࡽࡺࡵࡳࡧࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡹࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࡼࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࢀࠤ࡫࡯ࡸࡵࡷࡵࡩࡩ࡫ࡦ࠾ࡽࡩ࡭ࡽࡺࡵࡳࡧࡧࡩ࡫ࢃࠠࡴࡥࡲࡴࡪࡃࡻࡴࡥࡲࡴࡪࢃࠠࡵࡣࡵ࡫ࡪࡺ࠽ࠣᐪ") + str(target) + bstack11l1l11_opy_ (u"ࠦࠧᐫ"))
            return None
        instance = TestFramework.bstack11111ll111_opy_(target)
        if not instance:
            self.logger.warning(bstack11l1l11_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡻ࡮ࡩࡣࡱࡨࡱ࡫ࡤࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࡾࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࢂࠦࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࡁࢀ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࢀࠤࡸࡩ࡯ࡱࡧࡀࡿࡸࡩ࡯ࡱࡧࢀࠤࡧࡧࡳࡦ࡫ࡧࡁࢀࡨࡡࡴࡧ࡬ࡨࢂࠦࡴࡢࡴࡪࡩࡹࡃࠢᐬ") + str(target) + bstack11l1l11_opy_ (u"ࠨࠢᐭ"))
            return None
        bstack1l11l1llll1_opy_ = TestFramework.bstack11111l1l1l_opy_(instance, bstack1llll1111ll_opy_.bstack1l1l111l111_opy_, {})
        if os.getenv(bstack11l1l11_opy_ (u"ࠢࡔࡆࡎࡣࡈࡒࡉࡠࡈࡏࡅࡌࡥࡆࡊ࡚ࡗ࡙ࡗࡋࡓࠣᐮ"), bstack11l1l11_opy_ (u"ࠣ࠳ࠥᐯ")) == bstack11l1l11_opy_ (u"ࠤ࠴ࠦᐰ"):
            bstack1l11ll11l11_opy_ = bstack11l1l11_opy_ (u"ࠥ࠾ࠧᐱ").join((scope, fixturename))
            bstack1l1l111l1l1_opy_ = datetime.now(tz=timezone.utc)
            bstack1l11lll1l1l_opy_ = {
                bstack11l1l11_opy_ (u"ࠦࡰ࡫ࡹࠣᐲ"): bstack1l11ll11l11_opy_,
                bstack11l1l11_opy_ (u"ࠧࡺࡡࡨࡵࠥᐳ"): bstack1llll1111ll_opy_.__1l11l11ll1l_opy_(request.node),
                bstack11l1l11_opy_ (u"ࠨࡦࡪࡺࡷࡹࡷ࡫ࠢᐴ"): fixturedef,
                bstack11l1l11_opy_ (u"ࠢࡴࡥࡲࡴࡪࠨᐵ"): scope,
                bstack11l1l11_opy_ (u"ࠣࡶࡼࡴࡪࠨᐶ"): None,
            }
            try:
                if test_hook_state == bstack1lll111lll1_opy_.POST and callable(getattr(args[-1], bstack11l1l11_opy_ (u"ࠤࡪࡩࡹࡥࡲࡦࡵࡸࡰࡹࠨᐷ"), None)):
                    bstack1l11lll1l1l_opy_[bstack11l1l11_opy_ (u"ࠥࡸࡾࡶࡥࠣᐸ")] = TestFramework.bstack1l1llll1l11_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == bstack1lll111lll1_opy_.PRE:
                bstack1l11lll1l1l_opy_[bstack11l1l11_opy_ (u"ࠦࡺࡻࡩࡥࠤᐹ")] = uuid4().__str__()
                bstack1l11lll1l1l_opy_[bstack1llll1111ll_opy_.bstack1l11l11l1ll_opy_] = bstack1l1l111l1l1_opy_
            elif test_hook_state == bstack1lll111lll1_opy_.POST:
                bstack1l11lll1l1l_opy_[bstack1llll1111ll_opy_.bstack1l11l1l11ll_opy_] = bstack1l1l111l1l1_opy_
            if bstack1l11ll11l11_opy_ in bstack1l11l1llll1_opy_:
                bstack1l11l1llll1_opy_[bstack1l11ll11l11_opy_].update(bstack1l11lll1l1l_opy_)
                self.logger.debug(bstack11l1l11_opy_ (u"ࠧࡻࡰࡥࡣࡷࡩࡩࠦࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࡁࢀ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࢀࠤࡸࡩ࡯ࡱࡧࡀࡿࡸࡩ࡯ࡱࡧࢀࠤ࡫࡯ࡸࡵࡷࡵࡩࡂࠨᐺ") + str(bstack1l11l1llll1_opy_[bstack1l11ll11l11_opy_]) + bstack11l1l11_opy_ (u"ࠨࠢᐻ"))
            else:
                bstack1l11l1llll1_opy_[bstack1l11ll11l11_opy_] = bstack1l11lll1l1l_opy_
                self.logger.debug(bstack11l1l11_opy_ (u"ࠢࡴࡣࡹࡩࡩࠦࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࡁࢀ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࢀࠤࡸࡩ࡯ࡱࡧࡀࡿࡸࡩ࡯ࡱࡧࢀࠤ࡫࡯ࡸࡵࡷࡵࡩࡂࢁࡴࡦࡵࡷࡣ࡫࡯ࡸࡵࡷࡵࡩࢂࠦࡴࡳࡣࡦ࡯ࡪࡪ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡴ࠿ࠥᐼ") + str(len(bstack1l11l1llll1_opy_)) + bstack11l1l11_opy_ (u"ࠣࠤᐽ"))
        TestFramework.bstack1111111l1l_opy_(instance, bstack1llll1111ll_opy_.bstack1l1l111l111_opy_, bstack1l11l1llll1_opy_)
        self.logger.debug(bstack11l1l11_opy_ (u"ࠤࡶࡥࡻ࡫ࡤࠡࡨ࡬ࡼࡹࡻࡲࡦࡵࡀࡿࡱ࡫࡮ࠩࡶࡵࡥࡨࡱࡥࡥࡡࡩ࡭ࡽࡺࡵࡳࡧࡶ࠭ࢂࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࠤᐾ") + str(instance.ref()) + bstack11l1l11_opy_ (u"ࠥࠦᐿ"))
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
            bstack1llll1111ll_opy_.bstack1l1l111l111_opy_: {},
            bstack1llll1111ll_opy_.bstack1l11ll11l1l_opy_: {},
            bstack1llll1111ll_opy_.bstack1l1l1111l11_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack1111111l1l_opy_(ob, TestFramework.bstack1l11llll1l1_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack1111111l1l_opy_(ob, TestFramework.bstack1ll1l11llll_opy_, context.platform_index)
        TestFramework.bstack1111111111_opy_[ctx.id] = ob
        self.logger.debug(bstack11l1l11_opy_ (u"ࠦࡸࡧࡶࡦࡦࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࠥࡩࡴࡹ࠰࡬ࡨࡂࢁࡣࡵࡺ࠱࡭ࡩࢃࠠࡵࡣࡵ࡫ࡪࡺ࠽ࡼࡶࡤࡶ࡬࡫ࡴࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠࡪࡰࡶࡸࡦࡴࡣࡦࡵࡀࠦᑀ") + str(TestFramework.bstack1111111111_opy_.keys()) + bstack11l1l11_opy_ (u"ࠧࠨᑁ"))
        return ob
    def bstack1l1lllllll1_opy_(self, instance: bstack1lllllll111_opy_, bstack1111l1ll11_opy_: Tuple[bstack1llllll1lll_opy_, bstack1lll111lll1_opy_]):
        bstack1l11ll111l1_opy_ = (
            bstack1llll1111ll_opy_.bstack1l11llllll1_opy_
            if bstack1111l1ll11_opy_[1] == bstack1lll111lll1_opy_.PRE
            else bstack1llll1111ll_opy_.bstack1l11l111lll_opy_
        )
        hook = bstack1llll1111ll_opy_.bstack1l11l1l1lll_opy_(instance, bstack1l11ll111l1_opy_)
        entries = hook.get(TestFramework.bstack1l11ll1ll11_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack11111l1l1l_opy_(instance, TestFramework.bstack1l11l1ll11l_opy_, []))
        return entries
    def bstack1ll11111111_opy_(self, instance: bstack1lllllll111_opy_, bstack1111l1ll11_opy_: Tuple[bstack1llllll1lll_opy_, bstack1lll111lll1_opy_]):
        bstack1l11ll111l1_opy_ = (
            bstack1llll1111ll_opy_.bstack1l11llllll1_opy_
            if bstack1111l1ll11_opy_[1] == bstack1lll111lll1_opy_.PRE
            else bstack1llll1111ll_opy_.bstack1l11l111lll_opy_
        )
        bstack1llll1111ll_opy_.bstack1l11ll1lll1_opy_(instance, bstack1l11ll111l1_opy_)
        TestFramework.bstack11111l1l1l_opy_(instance, TestFramework.bstack1l11l1ll11l_opy_, []).clear()
    @staticmethod
    def bstack1l11l1l1lll_opy_(instance: bstack1lllllll111_opy_, bstack1l11ll111l1_opy_: str):
        bstack1l11l11l111_opy_ = (
            bstack1llll1111ll_opy_.bstack1l11ll11l1l_opy_
            if bstack1l11ll111l1_opy_ == bstack1llll1111ll_opy_.bstack1l11l111lll_opy_
            else bstack1llll1111ll_opy_.bstack1l1l1111l11_opy_
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
        hook = bstack1llll1111ll_opy_.bstack1l11l1l1lll_opy_(instance, bstack1l11ll111l1_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack1l11ll1ll11_opy_, []).clear()
    @staticmethod
    def __1l11l1l1111_opy_(instance: bstack1lllllll111_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack11l1l11_opy_ (u"ࠨࡧࡦࡶࡢࡶࡪࡩ࡯ࡳࡦࡶࠦᑂ"), None)):
            return
        if os.getenv(bstack11l1l11_opy_ (u"ࠢࡔࡆࡎࡣࡈࡒࡉࡠࡈࡏࡅࡌࡥࡌࡐࡉࡖࠦᑃ"), bstack11l1l11_opy_ (u"ࠣ࠳ࠥᑄ")) != bstack11l1l11_opy_ (u"ࠤ࠴ࠦᑅ"):
            bstack1llll1111ll_opy_.logger.warning(bstack11l1l11_opy_ (u"ࠥ࡭࡬ࡴ࡯ࡳ࡫ࡱ࡫ࠥࡩࡡࡱ࡮ࡲ࡫ࠧᑆ"))
            return
        bstack1l11llll11l_opy_ = {
            bstack11l1l11_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࠥᑇ"): (bstack1llll1111ll_opy_.bstack1l11llllll1_opy_, bstack1llll1111ll_opy_.bstack1l1l1111l11_opy_),
            bstack11l1l11_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴࠢᑈ"): (bstack1llll1111ll_opy_.bstack1l11l111lll_opy_, bstack1llll1111ll_opy_.bstack1l11ll11l1l_opy_),
        }
        for when in (bstack11l1l11_opy_ (u"ࠨࡳࡦࡶࡸࡴࠧᑉ"), bstack11l1l11_opy_ (u"ࠢࡤࡣ࡯ࡰࠧᑊ"), bstack11l1l11_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࠥᑋ")):
            bstack1l11lll1111_opy_ = args[1].get_records(when)
            if not bstack1l11lll1111_opy_:
                continue
            records = [
                bstack1lll11ll111_opy_(
                    kind=TestFramework.bstack1ll11l1l11l_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack11l1l11_opy_ (u"ࠤ࡯ࡩࡻ࡫࡬࡯ࡣࡰࡩࠧᑌ")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack11l1l11_opy_ (u"ࠥࡧࡷ࡫ࡡࡵࡧࡧࠦᑍ")) and r.created
                        else None
                    ),
                )
                for r in bstack1l11lll1111_opy_
                if isinstance(getattr(r, bstack11l1l11_opy_ (u"ࠦࡲ࡫ࡳࡴࡣࡪࡩࠧᑎ"), None), str) and r.message.strip()
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
    def __1l11lll1ll1_opy_(test) -> Dict[str, Any]:
        bstack1l1l1ll1l_opy_ = bstack1llll1111ll_opy_.__1l1l111l11l_opy_(test.location) if hasattr(test, bstack11l1l11_opy_ (u"ࠧࡲ࡯ࡤࡣࡷ࡭ࡴࡴࠢᑏ")) else getattr(test, bstack11l1l11_opy_ (u"ࠨ࡮ࡰࡦࡨ࡭ࡩࠨᑐ"), None)
        test_name = test.name if hasattr(test, bstack11l1l11_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᑑ")) else None
        bstack1l1l111111l_opy_ = test.fspath.strpath if hasattr(test, bstack11l1l11_opy_ (u"ࠣࡨࡶࡴࡦࡺࡨࠣᑒ")) and test.fspath else None
        if not bstack1l1l1ll1l_opy_ or not test_name or not bstack1l1l111111l_opy_:
            return None
        code = None
        if hasattr(test, bstack11l1l11_opy_ (u"ࠤࡲࡦ࡯ࠨᑓ")):
            try:
                import inspect
                code = inspect.getsource(test.obj)
            except:
                pass
        bstack1l11l111l1l_opy_ = []
        try:
            bstack1l11l111l1l_opy_ = bstack11l11l11_opy_.bstack111l1l111l_opy_(test)
        except:
            bstack1llll1111ll_opy_.logger.warning(bstack11l1l11_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡦࡪࡰࡧࠤࡹ࡫ࡳࡵࠢࡶࡧࡴࡶࡥࡴ࠮ࠣࡸࡪࡹࡴࠡࡵࡦࡳࡵ࡫ࡳࠡࡹ࡬ࡰࡱࠦࡢࡦࠢࡵࡩࡸࡵ࡬ࡷࡧࡧࠤ࡮ࡴࠠࡄࡎࡌࠦᑔ"))
        return {
            TestFramework.bstack1ll1lll11l1_opy_: uuid4().__str__(),
            TestFramework.bstack1l11ll1llll_opy_: bstack1l1l1ll1l_opy_,
            TestFramework.bstack1ll1l11l111_opy_: test_name,
            TestFramework.bstack1l1lll11lll_opy_: getattr(test, bstack11l1l11_opy_ (u"ࠦࡳࡵࡤࡦ࡫ࡧࠦᑕ"), None),
            TestFramework.bstack1l1l111ll11_opy_: bstack1l1l111111l_opy_,
            TestFramework.bstack1l11ll1l111_opy_: bstack1llll1111ll_opy_.__1l11l11ll1l_opy_(test),
            TestFramework.bstack1l11ll1111l_opy_: code,
            TestFramework.bstack1l1ll1111ll_opy_: TestFramework.bstack1l11l11lll1_opy_,
            TestFramework.bstack1l1l11llll1_opy_: bstack1l1l1ll1l_opy_,
            TestFramework.bstack1l11l111l11_opy_: bstack1l11l111l1l_opy_
        }
    @staticmethod
    def __1l11l11ll1l_opy_(test) -> List[str]:
        return (
            [getattr(f, bstack11l1l11_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᑖ"), None) for f in test.own_markers if getattr(f, bstack11l1l11_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᑗ"), None)]
            if isinstance(getattr(test, bstack11l1l11_opy_ (u"ࠢࡰࡹࡱࡣࡲࡧࡲ࡬ࡧࡵࡷࠧᑘ"), None), list)
            else []
        )
    @staticmethod
    def __1l1l111l11l_opy_(location):
        return bstack11l1l11_opy_ (u"ࠣ࠼࠽ࠦᑙ").join(filter(lambda x: isinstance(x, str), location))
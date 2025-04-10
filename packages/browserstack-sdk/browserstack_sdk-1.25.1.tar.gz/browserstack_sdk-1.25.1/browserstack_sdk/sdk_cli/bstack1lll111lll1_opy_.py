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
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    bstack1lllllll1ll_opy_,
    bstack1lll1l1l1l1_opy_,
    bstack1lll1l11l1l_opy_,
    bstack1l111lll1l1_opy_,
    bstack1llll1l1lll_opy_,
)
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from datetime import datetime, timezone
from typing import List, Dict, Any
import traceback
from bstack_utils.helper import bstack1ll1111ll11_opy_
from bstack_utils.bstack1l111l1111_opy_ import bstack1lll111l11l_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.bstack1111l1ll11_opy_ import bstack1111l1llll_opy_
from browserstack_sdk.sdk_cli.utils.bstack1lll1llll1l_opy_ import bstack1lllll11111_opy_
from bstack_utils.bstack111llll1l1_opy_ import bstack11l1ll1ll_opy_
bstack1l1lll11l1l_opy_ = bstack1ll1111ll11_opy_()
bstack1l11lll1lll_opy_ = 1.0
bstack1l1lllll111_opy_ = bstack1ll1l1_opy_ (u"ࠨࡕࡱ࡮ࡲࡥࡩ࡫ࡤࡂࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷ࠲ࠨᐘ")
bstack1l111l1l111_opy_ = bstack1ll1l1_opy_ (u"ࠢࡕࡧࡶࡸࡑ࡫ࡶࡦ࡮ࠥᐙ")
bstack1l111l1l1l1_opy_ = bstack1ll1l1_opy_ (u"ࠣࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࠧᐚ")
bstack1l111l1l11l_opy_ = bstack1ll1l1_opy_ (u"ࠤࡋࡳࡴࡱࡌࡦࡸࡨࡰࠧᐛ")
bstack1l111l11ll1_opy_ = bstack1ll1l1_opy_ (u"ࠥࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࡈࡰࡱ࡮ࡉࡻ࡫࡮ࡵࠤᐜ")
_1ll111ll11l_opy_ = set()
class bstack1llll11l111_opy_(TestFramework):
    bstack1l11ll1ll1l_opy_ = bstack1ll1l1_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡩ࡭ࡽࡺࡵࡳࡧࡶࠦᐝ")
    bstack1l11l11llll_opy_ = bstack1ll1l1_opy_ (u"ࠧࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡴࡡࡶࡸࡦࡸࡴࡦࡦࠥᐞ")
    bstack1l11l1l1ll1_opy_ = bstack1ll1l1_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡵࡢࡪ࡮ࡴࡩࡴࡪࡨࡨࠧᐟ")
    bstack1l111ll1ll1_opy_ = bstack1ll1l1_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡰࡦࡹࡴࡠࡵࡷࡥࡷࡺࡥࡥࠤᐠ")
    bstack1l111ll1l1l_opy_ = bstack1ll1l1_opy_ (u"ࠣࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡱࡧࡳࡵࡡࡩ࡭ࡳ࡯ࡳࡩࡧࡧࠦᐡ")
    bstack1l11l1l1111_opy_: bool
    bstack1111l1ll11_opy_: bstack1111l1llll_opy_  = None
    bstack1llllll1ll1_opy_ = None
    bstack1l11ll111l1_opy_ = [
        bstack1lllllll1ll_opy_.BEFORE_ALL,
        bstack1lllllll1ll_opy_.AFTER_ALL,
        bstack1lllllll1ll_opy_.BEFORE_EACH,
        bstack1lllllll1ll_opy_.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack1l11llll1ll_opy_: Dict[str, str],
        bstack1ll1l1l1111_opy_: List[str]=[bstack1ll1l1_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵࠤᐢ")],
        bstack1111l1ll11_opy_: bstack1111l1llll_opy_=None,
        bstack1llllll1ll1_opy_=None
    ):
        super().__init__(bstack1ll1l1l1111_opy_, bstack1l11llll1ll_opy_, bstack1111l1ll11_opy_)
        self.bstack1l11l1l1111_opy_ = any(bstack1ll1l1_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶࠥᐣ") in item.lower() for item in bstack1ll1l1l1111_opy_)
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
        if test_framework_state == bstack1lllllll1ll_opy_.TEST or test_framework_state in bstack1llll11l111_opy_.bstack1l11ll111l1_opy_:
            bstack1l111ll111l_opy_(test_framework_state, test_hook_state)
        if test_framework_state == bstack1lllllll1ll_opy_.NONE:
            self.logger.warning(bstack1ll1l1_opy_ (u"ࠦ࡮࡭࡮ࡰࡴࡨࡨࠥࡩࡡ࡭࡮ࡥࡥࡨࡱࠠࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾࠢࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࡁࠧᐤ") + str(test_hook_state) + bstack1ll1l1_opy_ (u"ࠧࠨᐥ"))
            return
        if not self.bstack1l11l1l1111_opy_:
            self.logger.warning(bstack1ll1l1_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡻ࡮ࡴࡷࡳࡴࡴࡸࡴࡦࡦࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡃࠢᐦ") + str(str(self.bstack1ll1l1l1111_opy_)) + bstack1ll1l1_opy_ (u"ࠢࠣᐧ"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack1ll1l1_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡦࡸࡨࡲࡹࡀࠠࡶࡰࡨࡼࡵ࡫ࡣࡵࡧࡧࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥᐨ") + str(kwargs) + bstack1ll1l1_opy_ (u"ࠤࠥᐩ"))
            return
        instance = self.__1l11llll1l1_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack1ll1l1_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡨࡺࡪࡴࡴ࠻ࠢࡸࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࡻࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦࡿࠣࡥࡷ࡭ࡳ࠾ࠤᐪ") + str(args) + bstack1ll1l1_opy_ (u"ࠦࠧᐫ"))
            return
        try:
            if instance!= None and test_framework_state in bstack1llll11l111_opy_.bstack1l11ll111l1_opy_ and test_hook_state == bstack1lll1l11l1l_opy_.PRE:
                bstack1ll1l1l111l_opy_ = bstack1lll111l11l_opy_.bstack1ll1ll111ll_opy_(EVENTS.bstack1l1ll1ll_opy_.value)
                name = str(EVENTS.bstack1l1ll1ll_opy_.name)+bstack1ll1l1_opy_ (u"ࠧࡀࠢᐬ")+str(test_framework_state.name)
                TestFramework.bstack1l11l111lll_opy_(instance, name, bstack1ll1l1l111l_opy_)
        except Exception as e:
            self.logger.debug(bstack1ll1l1_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡮࡯ࡰ࡭ࠣࡩࡷࡸ࡯ࡳࠢࡳࡶࡪࡀࠠࡼࡿࠥᐭ").format(e))
        try:
            if not TestFramework.bstack11111l1l1l_opy_(instance, TestFramework.bstack1l111l1ll1l_opy_) and test_hook_state == bstack1lll1l11l1l_opy_.PRE:
                test = bstack1llll11l111_opy_.__1l11l1l1l11_opy_(args[0])
                if test:
                    instance.data.update(test)
                    self.logger.debug(bstack1ll1l1_opy_ (u"ࠢ࡭ࡱࡤࡨࡪࡪࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾ࡭ࡳࡹࡴࡢࡰࡦࡩ࠳ࡸࡥࡧࠪࠬࢁࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࠢᐮ") + str(test_hook_state) + bstack1ll1l1_opy_ (u"ࠣࠤᐯ"))
            if test_framework_state == bstack1lllllll1ll_opy_.TEST:
                if test_hook_state == bstack1lll1l11l1l_opy_.PRE and not TestFramework.bstack11111l1l1l_opy_(instance, TestFramework.bstack1l1lllll1l1_opy_):
                    TestFramework.bstack1111111111_opy_(instance, TestFramework.bstack1l1lllll1l1_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1ll1l1_opy_ (u"ࠤࡶࡩࡹࠦࡴࡦࡵࡷ࠱ࡸࡺࡡࡳࡶࠣࡪࡴࡸࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾ࡭ࡳࡹࡴࡢࡰࡦࡩ࠳ࡸࡥࡧࠪࠬࢁࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࠢᐰ") + str(test_hook_state) + bstack1ll1l1_opy_ (u"ࠥࠦᐱ"))
                elif test_hook_state == bstack1lll1l11l1l_opy_.POST and not TestFramework.bstack11111l1l1l_opy_(instance, TestFramework.bstack1ll11111l1l_opy_):
                    TestFramework.bstack1111111111_opy_(instance, TestFramework.bstack1ll11111l1l_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1ll1l1_opy_ (u"ࠦࡸ࡫ࡴࠡࡶࡨࡷࡹ࠳ࡥ࡯ࡦࠣࡪࡴࡸࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾ࡭ࡳࡹࡴࡢࡰࡦࡩ࠳ࡸࡥࡧࠪࠬࢁࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࠢᐲ") + str(test_hook_state) + bstack1ll1l1_opy_ (u"ࠧࠨᐳ"))
            elif test_framework_state == bstack1lllllll1ll_opy_.LOG and test_hook_state == bstack1lll1l11l1l_opy_.POST:
                bstack1llll11l111_opy_.__1l11l1lll1l_opy_(instance, *args)
            elif test_framework_state == bstack1lllllll1ll_opy_.LOG_REPORT and test_hook_state == bstack1lll1l11l1l_opy_.POST:
                self.__1l111lll11l_opy_(instance, *args)
                self.__1l111ll11ll_opy_(instance)
            elif test_framework_state in bstack1llll11l111_opy_.bstack1l11ll111l1_opy_:
                self.__1l11lll11l1_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack1ll1l1_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥ࡮ࡡ࡯ࡦ࡯ࡩࡩࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࡼࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࢀࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࠢᐴ") + str(instance.ref()) + bstack1ll1l1_opy_ (u"ࠢࠣᐵ"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack1l111llllll_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in bstack1llll11l111_opy_.bstack1l11ll111l1_opy_ and test_hook_state == bstack1lll1l11l1l_opy_.POST:
                name = str(EVENTS.bstack1l1ll1ll_opy_.name)+bstack1ll1l1_opy_ (u"ࠣ࠼ࠥᐶ")+str(test_framework_state.name)
                bstack1ll1l1l111l_opy_ = TestFramework.bstack1l111l1llll_opy_(instance, name)
                bstack1lll111l11l_opy_.end(EVENTS.bstack1l1ll1ll_opy_.value, bstack1ll1l1l111l_opy_+bstack1ll1l1_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᐷ"), bstack1ll1l1l111l_opy_+bstack1ll1l1_opy_ (u"ࠥ࠾ࡪࡴࡤࠣᐸ"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack1ll1l1_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣ࡬ࡴࡵ࡫ࠡࡧࡵࡶࡴࡸ࠺ࠡࡽࢀࠦᐹ").format(e))
    def bstack1l1lllll11l_opy_(self):
        return self.bstack1l11l1l1111_opy_
    def __1l11ll1ll11_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack1ll1l1_opy_ (u"ࠧ࡭ࡥࡵࡡࡵࡩࡸࡻ࡬ࡵࠤᐺ"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack1ll111lll11_opy_(rep, [bstack1ll1l1_opy_ (u"ࠨࡷࡩࡧࡱࠦᐻ"), bstack1ll1l1_opy_ (u"ࠢࡰࡷࡷࡧࡴࡳࡥࠣᐼ"), bstack1ll1l1_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣᐽ"), bstack1ll1l1_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤᐾ"), bstack1ll1l1_opy_ (u"ࠥࡷࡰ࡯ࡰࡱࡧࡧࠦᐿ"), bstack1ll1l1_opy_ (u"ࠦࡱࡵ࡮ࡨࡴࡨࡴࡷࡺࡥࡹࡶࠥᑀ")])
        return None
    def __1l111lll11l_opy_(self, instance: bstack1lll1l1l1l1_opy_, *args):
        result = self.__1l11ll1ll11_opy_(*args)
        if not result:
            return
        failure = None
        bstack1111ll1l11_opy_ = None
        if result.get(bstack1ll1l1_opy_ (u"ࠧࡵࡵࡵࡥࡲࡱࡪࠨᑁ"), None) == bstack1ll1l1_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨᑂ") and len(args) > 1 and getattr(args[1], bstack1ll1l1_opy_ (u"ࠢࡦࡺࡦ࡭ࡳ࡬࡯ࠣᑃ"), None) is not None:
            failure = [{bstack1ll1l1_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫᑄ"): [args[1].excinfo.exconly(), result.get(bstack1ll1l1_opy_ (u"ࠤ࡯ࡳࡳ࡭ࡲࡦࡲࡵࡸࡪࡾࡴࠣᑅ"), None)]}]
            bstack1111ll1l11_opy_ = bstack1ll1l1_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࡋࡲࡳࡱࡵࠦᑆ") if bstack1ll1l1_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࠢᑇ") in getattr(args[1].excinfo, bstack1ll1l1_opy_ (u"ࠧࡺࡹࡱࡧࡱࡥࡲ࡫ࠢᑈ"), bstack1ll1l1_opy_ (u"ࠨࠢᑉ")) else bstack1ll1l1_opy_ (u"ࠢࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠣᑊ")
        bstack1l11ll111ll_opy_ = result.get(bstack1ll1l1_opy_ (u"ࠣࡱࡸࡸࡨࡵ࡭ࡦࠤᑋ"), TestFramework.bstack1l11lll11ll_opy_)
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
            target = None # bstack1l11l111l11_opy_ bstack1l11l1l1lll_opy_ this to be bstack1ll1l1_opy_ (u"ࠤࡱࡳࡩ࡫ࡩࡥࠤᑌ")
            if test_framework_state == bstack1lllllll1ll_opy_.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__1l111lll1ll_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == bstack1lllllll1ll_opy_.LOG:
                nodeid = getattr(getattr(args[0], bstack1ll1l1_opy_ (u"ࠥࡲࡴࡪࡥࠣᑍ"), None), bstack1ll1l1_opy_ (u"ࠦࡳࡵࡤࡦ࡫ࡧࠦᑎ"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack1ll1l1_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࠧᑏ"), None):
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
        bstack1l11lll111l_opy_ = TestFramework.bstack11111lllll_opy_(instance, bstack1llll11l111_opy_.bstack1l11l11llll_opy_, {})
        if not key in bstack1l11lll111l_opy_:
            bstack1l11lll111l_opy_[key] = []
        bstack1l11l1llll1_opy_ = TestFramework.bstack11111lllll_opy_(instance, bstack1llll11l111_opy_.bstack1l11l1l1ll1_opy_, {})
        if not key in bstack1l11l1llll1_opy_:
            bstack1l11l1llll1_opy_[key] = []
        bstack1l11ll1l11l_opy_ = {
            bstack1llll11l111_opy_.bstack1l11l11llll_opy_: bstack1l11lll111l_opy_,
            bstack1llll11l111_opy_.bstack1l11l1l1ll1_opy_: bstack1l11l1llll1_opy_,
        }
        if test_hook_state == bstack1lll1l11l1l_opy_.PRE:
            hook = {
                bstack1ll1l1_opy_ (u"ࠨ࡫ࡦࡻࠥᑐ"): key,
                TestFramework.bstack1l11l11l1ll_opy_: uuid4().__str__(),
                TestFramework.bstack1l11ll1l1ll_opy_: TestFramework.bstack1l11l11111l_opy_,
                TestFramework.bstack1l11lll1ll1_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack1l11lll1l11_opy_: [],
                TestFramework.bstack1l11llll11l_opy_: args[1] if len(args) > 1 else bstack1ll1l1_opy_ (u"ࠧࠨᑑ"),
                TestFramework.bstack1l11l11l11l_opy_: bstack1lllll11111_opy_.bstack1l11llll111_opy_()
            }
            bstack1l11lll111l_opy_[key].append(hook)
            bstack1l11ll1l11l_opy_[bstack1llll11l111_opy_.bstack1l111ll1ll1_opy_] = key
        elif test_hook_state == bstack1lll1l11l1l_opy_.POST:
            bstack1l111ll1111_opy_ = bstack1l11lll111l_opy_.get(key, [])
            hook = bstack1l111ll1111_opy_.pop() if bstack1l111ll1111_opy_ else None
            if hook:
                result = self.__1l11ll1ll11_opy_(*args)
                if result:
                    bstack1l11lllll1l_opy_ = result.get(bstack1ll1l1_opy_ (u"ࠣࡱࡸࡸࡨࡵ࡭ࡦࠤᑒ"), TestFramework.bstack1l11l11111l_opy_)
                    if bstack1l11lllll1l_opy_ != TestFramework.bstack1l11l11111l_opy_:
                        hook[TestFramework.bstack1l11ll1l1ll_opy_] = bstack1l11lllll1l_opy_
                hook[TestFramework.bstack1l11ll1111l_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack1l11l11l11l_opy_]= bstack1lllll11111_opy_.bstack1l11llll111_opy_()
                self.bstack1l11lll1l1l_opy_(hook)
                logs = hook.get(TestFramework.bstack1l11lllll11_opy_, [])
                if logs: self.bstack1l1llll1lll_opy_(instance, logs)
                bstack1l11l1llll1_opy_[key].append(hook)
                bstack1l11ll1l11l_opy_[bstack1llll11l111_opy_.bstack1l111ll1l1l_opy_] = key
        TestFramework.bstack1l11lll1111_opy_(instance, bstack1l11ll1l11l_opy_)
        self.logger.debug(bstack1ll1l1_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡪࡲࡳࡰࡥࡥࡷࡧࡱࡸ࠿ࠦࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥ࠾ࡽ࡮ࡩࡾࢃ࠮ࡼࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࢀࠤ࡭ࡵ࡯࡬ࡵࡢࡷࡹࡧࡲࡵࡧࡧࡁࢀ࡮࡯ࡰ࡭ࡶࡣࡸࡺࡡࡳࡶࡨࡨࢂࠦࡨࡰࡱ࡮ࡷࡤ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࠽ࠣᑓ") + str(bstack1l11l1llll1_opy_) + bstack1ll1l1_opy_ (u"ࠥࠦᑔ"))
    def __1l111ll11l1_opy_(
        self,
        context: bstack1l111lll1l1_opy_,
        test_framework_state: bstack1lllllll1ll_opy_,
        test_hook_state: bstack1lll1l11l1l_opy_,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack1ll111lll11_opy_(args[0], [bstack1ll1l1_opy_ (u"ࠦࡸࡩ࡯ࡱࡧࠥᑕ"), bstack1ll1l1_opy_ (u"ࠧࡧࡲࡨࡰࡤࡱࡪࠨᑖ"), bstack1ll1l1_opy_ (u"ࠨࡰࡢࡴࡤࡱࡸࠨᑗ"), bstack1ll1l1_opy_ (u"ࠢࡪࡦࡶࠦᑘ"), bstack1ll1l1_opy_ (u"ࠣࡷࡱ࡭ࡹࡺࡥࡴࡶࠥᑙ"), bstack1ll1l1_opy_ (u"ࠤࡥࡥࡸ࡫ࡩࡥࠤᑚ")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scope = request.scope if hasattr(request, bstack1ll1l1_opy_ (u"ࠥࡷࡨࡵࡰࡦࠤᑛ")) else fixturedef.get(bstack1ll1l1_opy_ (u"ࠦࡸࡩ࡯ࡱࡧࠥᑜ"), None)
        fixturename = request.fixturename if hasattr(request, bstack1ll1l1_opy_ (u"ࠧ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࠥᑝ")) else None
        node = request.node if hasattr(request, bstack1ll1l1_opy_ (u"ࠨ࡮ࡰࡦࡨࠦᑞ")) else None
        target = request.node.nodeid if hasattr(node, bstack1ll1l1_opy_ (u"ࠢ࡯ࡱࡧࡩ࡮ࡪࠢᑟ")) else None
        baseid = fixturedef.get(bstack1ll1l1_opy_ (u"ࠣࡤࡤࡷࡪ࡯ࡤࠣᑠ"), None) or bstack1ll1l1_opy_ (u"ࠤࠥᑡ")
        if (not target or len(baseid) > 0) and hasattr(request, bstack1ll1l1_opy_ (u"ࠥࡣࡵࡿࡦࡶࡰࡦ࡭ࡹ࡫࡭ࠣᑢ")):
            target = bstack1llll11l111_opy_.__1l11ll1l1l1_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack1ll1l1_opy_ (u"ࠦࡱࡵࡣࡢࡶ࡬ࡳࡳࠨᑣ")) else None
            if target and not TestFramework.bstack11111l1111_opy_(target):
                self.__1l111lll1ll_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack1ll1l1_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࡫ࡶࡦࡰࡷ࠾ࠥ࡬ࡡ࡭࡮ࡥࡥࡨࡱࠠࡵࡣࡵ࡫ࡪࡺ࠽ࡼࡶࡤࡶ࡬࡫ࡴࡾࠢࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫࠽ࡼࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࢃࠠ࡯ࡱࡧࡩࡂࢁ࡮ࡰࡦࡨࢁࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࠢᑤ") + str(test_hook_state) + bstack1ll1l1_opy_ (u"ࠨࠢᑥ"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstack1ll1l1_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡦࡪࡺࡷࡹࡷ࡫࡟ࡦࡸࡨࡲࡹࡀࠠࡶࡰ࡫ࡥࡳࡪ࡬ࡦࡦࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࢀࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫ࡽࠡࡨ࡬ࡼࡹࡻࡲࡦࡦࡨࡪࡂࢁࡦࡪࡺࡷࡹࡷ࡫ࡤࡦࡨࢀࠤࡸࡩ࡯ࡱࡧࡀࡿࡸࡩ࡯ࡱࡧࢀࠤࡹࡧࡲࡨࡧࡷࡁࠧᑦ") + str(target) + bstack1ll1l1_opy_ (u"ࠣࠤᑧ"))
            return None
        instance = TestFramework.bstack11111l1111_opy_(target)
        if not instance:
            self.logger.warning(bstack1ll1l1_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡨ࡬ࡼࡹࡻࡲࡦࡡࡨࡺࡪࡴࡴ࠻ࠢࡸࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࡻࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦࡿࠣࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥ࠾ࡽࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫ࡽࠡࡵࡦࡳࡵ࡫࠽ࡼࡵࡦࡳࡵ࡫ࡽࠡࡤࡤࡷࡪ࡯ࡤ࠾ࡽࡥࡥࡸ࡫ࡩࡥࡿࠣࡸࡦࡸࡧࡦࡶࡀࠦᑨ") + str(target) + bstack1ll1l1_opy_ (u"ࠥࠦᑩ"))
            return None
        bstack1l111ll1l11_opy_ = TestFramework.bstack11111lllll_opy_(instance, bstack1llll11l111_opy_.bstack1l11ll1ll1l_opy_, {})
        if os.getenv(bstack1ll1l1_opy_ (u"ࠦࡘࡊࡋࡠࡅࡏࡍࡤࡌࡌࡂࡉࡢࡊࡎ࡞ࡔࡖࡔࡈࡗࠧᑪ"), bstack1ll1l1_opy_ (u"ࠧ࠷ࠢᑫ")) == bstack1ll1l1_opy_ (u"ࠨ࠱ࠣᑬ"):
            bstack1l11l1l11ll_opy_ = bstack1ll1l1_opy_ (u"ࠢ࠻ࠤᑭ").join((scope, fixturename))
            bstack1l11l1lllll_opy_ = datetime.now(tz=timezone.utc)
            bstack1l11l111111_opy_ = {
                bstack1ll1l1_opy_ (u"ࠣ࡭ࡨࡽࠧᑮ"): bstack1l11l1l11ll_opy_,
                bstack1ll1l1_opy_ (u"ࠤࡷࡥ࡬ࡹࠢᑯ"): bstack1llll11l111_opy_.__1l11l1l11l1_opy_(request.node),
                bstack1ll1l1_opy_ (u"ࠥࡪ࡮ࡾࡴࡶࡴࡨࠦᑰ"): fixturedef,
                bstack1ll1l1_opy_ (u"ࠦࡸࡩ࡯ࡱࡧࠥᑱ"): scope,
                bstack1ll1l1_opy_ (u"ࠧࡺࡹࡱࡧࠥᑲ"): None,
            }
            try:
                if test_hook_state == bstack1lll1l11l1l_opy_.POST and callable(getattr(args[-1], bstack1ll1l1_opy_ (u"ࠨࡧࡦࡶࡢࡶࡪࡹࡵ࡭ࡶࠥᑳ"), None)):
                    bstack1l11l111111_opy_[bstack1ll1l1_opy_ (u"ࠢࡵࡻࡳࡩࠧᑴ")] = TestFramework.bstack1ll11l11111_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == bstack1lll1l11l1l_opy_.PRE:
                bstack1l11l111111_opy_[bstack1ll1l1_opy_ (u"ࠣࡷࡸ࡭ࡩࠨᑵ")] = uuid4().__str__()
                bstack1l11l111111_opy_[bstack1llll11l111_opy_.bstack1l11lll1ll1_opy_] = bstack1l11l1lllll_opy_
            elif test_hook_state == bstack1lll1l11l1l_opy_.POST:
                bstack1l11l111111_opy_[bstack1llll11l111_opy_.bstack1l11ll1111l_opy_] = bstack1l11l1lllll_opy_
            if bstack1l11l1l11ll_opy_ in bstack1l111ll1l11_opy_:
                bstack1l111ll1l11_opy_[bstack1l11l1l11ll_opy_].update(bstack1l11l111111_opy_)
                self.logger.debug(bstack1ll1l1_opy_ (u"ࠤࡸࡴࡩࡧࡴࡦࡦࠣࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥ࠾ࡽࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫ࡽࠡࡵࡦࡳࡵ࡫࠽ࡼࡵࡦࡳࡵ࡫ࡽࠡࡨ࡬ࡼࡹࡻࡲࡦ࠿ࠥᑶ") + str(bstack1l111ll1l11_opy_[bstack1l11l1l11ll_opy_]) + bstack1ll1l1_opy_ (u"ࠥࠦᑷ"))
            else:
                bstack1l111ll1l11_opy_[bstack1l11l1l11ll_opy_] = bstack1l11l111111_opy_
                self.logger.debug(bstack1ll1l1_opy_ (u"ࠦࡸࡧࡶࡦࡦࠣࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥ࠾ࡽࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫ࡽࠡࡵࡦࡳࡵ࡫࠽ࡼࡵࡦࡳࡵ࡫ࡽࠡࡨ࡬ࡼࡹࡻࡲࡦ࠿ࡾࡸࡪࡹࡴࡠࡨ࡬ࡼࡹࡻࡲࡦࡿࠣࡸࡷࡧࡣ࡬ࡧࡧࡣ࡫࡯ࡸࡵࡷࡵࡩࡸࡃࠢᑸ") + str(len(bstack1l111ll1l11_opy_)) + bstack1ll1l1_opy_ (u"ࠧࠨᑹ"))
        TestFramework.bstack1111111111_opy_(instance, bstack1llll11l111_opy_.bstack1l11ll1ll1l_opy_, bstack1l111ll1l11_opy_)
        self.logger.debug(bstack1ll1l1_opy_ (u"ࠨࡳࡢࡸࡨࡨࠥ࡬ࡩࡹࡶࡸࡶࡪࡹ࠽ࡼ࡮ࡨࡲ࠭ࡺࡲࡢࡥ࡮ࡩࡩࡥࡦࡪࡺࡷࡹࡷ࡫ࡳࠪࡿࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࠨᑺ") + str(instance.ref()) + bstack1ll1l1_opy_ (u"ࠢࠣᑻ"))
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
            bstack1llll11l111_opy_.bstack1l11ll1ll1l_opy_: {},
            bstack1llll11l111_opy_.bstack1l11l1l1ll1_opy_: {},
            bstack1llll11l111_opy_.bstack1l11l11llll_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack1111111111_opy_(ob, TestFramework.bstack1l11l1111ll_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack1111111111_opy_(ob, TestFramework.bstack1ll11llll1l_opy_, context.platform_index)
        TestFramework.bstack1llllllll1l_opy_[ctx.id] = ob
        self.logger.debug(bstack1ll1l1_opy_ (u"ࠣࡵࡤࡺࡪࡪࠠࡪࡰࡶࡸࡦࡴࡣࡦࠢࡦࡸࡽ࠴ࡩࡥ࠿ࡾࡧࡹࡾ࠮ࡪࡦࢀࠤࡹࡧࡲࡨࡧࡷࡁࢀࡺࡡࡳࡩࡨࡸࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡹ࠽ࠣᑼ") + str(TestFramework.bstack1llllllll1l_opy_.keys()) + bstack1ll1l1_opy_ (u"ࠤࠥᑽ"))
        return ob
    def bstack1ll111ll1l1_opy_(self, instance: bstack1lll1l1l1l1_opy_, bstack1111l1l11l_opy_: Tuple[bstack1lllllll1ll_opy_, bstack1lll1l11l1l_opy_]):
        bstack1l11ll11111_opy_ = (
            bstack1llll11l111_opy_.bstack1l111ll1ll1_opy_
            if bstack1111l1l11l_opy_[1] == bstack1lll1l11l1l_opy_.PRE
            else bstack1llll11l111_opy_.bstack1l111ll1l1l_opy_
        )
        hook = bstack1llll11l111_opy_.bstack1l11ll11l1l_opy_(instance, bstack1l11ll11111_opy_)
        entries = hook.get(TestFramework.bstack1l11lll1l11_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack11111lllll_opy_(instance, TestFramework.bstack1l11l1ll11l_opy_, []))
        return entries
    def bstack1ll111lll1l_opy_(self, instance: bstack1lll1l1l1l1_opy_, bstack1111l1l11l_opy_: Tuple[bstack1lllllll1ll_opy_, bstack1lll1l11l1l_opy_]):
        bstack1l11ll11111_opy_ = (
            bstack1llll11l111_opy_.bstack1l111ll1ll1_opy_
            if bstack1111l1l11l_opy_[1] == bstack1lll1l11l1l_opy_.PRE
            else bstack1llll11l111_opy_.bstack1l111ll1l1l_opy_
        )
        bstack1llll11l111_opy_.bstack1l111lll111_opy_(instance, bstack1l11ll11111_opy_)
        TestFramework.bstack11111lllll_opy_(instance, TestFramework.bstack1l11l1ll11l_opy_, []).clear()
    def bstack1l11lll1l1l_opy_(self, hook: Dict[str, Any]) -> None:
        bstack1ll1l1_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡑࡴࡲࡧࡪࡹࡳࡦࡵࠣࡸ࡭࡫ࠠࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮ࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠡࡵ࡬ࡱ࡮ࡲࡡࡳࠢࡷࡳࠥࡺࡨࡦࠢࡍࡥࡻࡧࠠࡪ࡯ࡳࡰࡪࡳࡥ࡯ࡶࡤࡸ࡮ࡵ࡮࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡘ࡭࡯ࡳࠡ࡯ࡨࡸ࡭ࡵࡤ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡄࡪࡨࡧࡰࡹࠠࡵࡪࡨࠤࡍࡵ࡯࡬ࡎࡨࡺࡪࡲࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻࠣ࡭ࡳࡹࡩࡥࡧࠣࢂ࠴࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠴࡛ࡰ࡭ࡱࡤࡨࡪࡪࡁࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡊࡴࡸࠠࡦࡣࡦ࡬ࠥ࡬ࡩ࡭ࡧࠣ࡭ࡳࠦࡨࡰࡱ࡮ࡣࡱ࡫ࡶࡦ࡮ࡢࡪ࡮ࡲࡥࡴ࠮ࠣࡶࡪࡶ࡬ࡢࡥࡨࡷࠥࠨࡔࡦࡵࡷࡐࡪࡼࡥ࡭ࠤࠣࡻ࡮ࡺࡨࠡࠤࡋࡳࡴࡱࡌࡦࡸࡨࡰࠧࠦࡩ࡯ࠢ࡬ࡸࡸࠦࡰࡢࡶ࡫࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡍ࡫ࠦࡡࠡࡨ࡬ࡰࡪࠦࡩ࡯ࠢࡷ࡬ࡪࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺࠢࡰࡥࡹࡩࡨࡦࡵࠣࡥࠥࡳ࡯ࡥ࡫ࡩ࡭ࡪࡪࠠࡩࡱࡲ࡯࠲ࡲࡥࡷࡧ࡯ࠤ࡫࡯࡬ࡦ࠮ࠣ࡭ࡹࠦࡣࡳࡧࡤࡸࡪࡹࠠࡢࠢࡏࡳ࡬ࡋ࡮ࡵࡴࡼࠤࡴࡨࡪࡦࡥࡷࠤࡼ࡯ࡴࡩࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࠦࡤࡦࡶࡤ࡭ࡱࡹ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡓࡪ࡯࡬ࡰࡦࡸ࡬ࡺ࠮ࠣ࡭ࡹࠦࡰࡳࡱࡦࡩࡸࡹࡥࡴࠢࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶࠤࡱࡵࡣࡢࡶࡨࡨࠥ࡯࡮ࠡࡊࡲࡳࡰࡒࡥࡷࡧ࡯࠳ࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࡉࡱࡲ࡯ࡊࡼࡥ࡯ࡶࠣࡦࡾࠦࡲࡦࡲ࡯ࡥࡨ࡯࡮ࡨࠢࠥࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࠢࠡࡹ࡬ࡸ࡭ࠦࠢࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮࠲ࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࡈࡰࡱ࡮ࡉࡻ࡫࡮ࡵࠤ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡗ࡬ࡪࠦࡣࡳࡧࡤࡸࡪࡪࠠࡍࡱࡪࡉࡳࡺࡲࡺࠢࡲࡦ࡯࡫ࡣࡵࡵࠣࡥࡷ࡫ࠠࡢࡦࡧࡩࡩࠦࡴࡰࠢࡷ࡬ࡪࠦࡨࡰࡱ࡮ࠫࡸࠦࠢ࡭ࡱࡪࡷࠧࠦ࡬ࡪࡵࡷ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡁࡳࡩࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࡬ࡴࡵ࡫࠻ࠢࡗ࡬ࡪࠦࡥࡷࡧࡱࡸࠥࡪࡩࡤࡶ࡬ࡳࡳࡧࡲࡺࠢࡦࡳࡳࡺࡡࡪࡰ࡬ࡲ࡬ࠦࡥࡹ࡫ࡶࡸ࡮ࡴࡧࠡ࡮ࡲ࡫ࡸࠦࡡ࡯ࡦࠣ࡬ࡴࡵ࡫ࠡ࡫ࡱࡪࡴࡸ࡭ࡢࡶ࡬ࡳࡳ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࡮࡯ࡰ࡭ࡢࡰࡪࡼࡥ࡭ࡡࡩ࡭ࡱ࡫ࡳ࠻ࠢࡏ࡭ࡸࡺࠠࡰࡨࠣࡔࡦࡺࡨࠡࡱࡥ࡮ࡪࡩࡴࡴࠢࡩࡶࡴࡳࠠࡵࡪࡨࠤ࡙࡫ࡳࡵࡎࡨࡺࡪࡲࠠ࡮ࡱࡱ࡭ࡹࡵࡲࡪࡰࡪ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡦࡺ࡯࡬ࡥࡡ࡯ࡩࡻ࡫࡬ࡠࡨ࡬ࡰࡪࡹ࠺ࠡࡎ࡬ࡷࡹࠦ࡯ࡧࠢࡓࡥࡹ࡮ࠠࡰࡤ࡭ࡩࡨࡺࡳࠡࡨࡵࡳࡲࠦࡴࡩࡧࠣࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࠠ࡮ࡱࡱ࡭ࡹࡵࡲࡪࡰࡪ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤᑾ")
        global _1ll111ll11l_opy_
        platform_index = os.environ[bstack1ll1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫᑿ")]
        bstack1ll11l1111l_opy_ = os.path.join(bstack1l1lll11l1l_opy_, (bstack1l1lllll111_opy_ + str(platform_index)), bstack1l111l1l11l_opy_)
        if not os.path.exists(bstack1ll11l1111l_opy_) or not os.path.isdir(bstack1ll11l1111l_opy_):
            self.logger.info(bstack1ll1l1_opy_ (u"ࠧࡊࡩࡳࡧࡦࡸࡴࡸࡹࠡࡦࡲࡩࡸࠦ࡮ࡰࡶࠣࡩࡽ࡯ࡳࡵࡵࠣࡸࡴࠦࡰࡳࡱࡦࡩࡸࡹࠠࡼࡿࠥᒀ").format(bstack1ll11l1111l_opy_))
            return
        logs = hook.get(bstack1ll1l1_opy_ (u"ࠨ࡬ࡰࡩࡶࠦᒁ"), [])
        with os.scandir(bstack1ll11l1111l_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _1ll111ll11l_opy_:
                    self.logger.info(bstack1ll1l1_opy_ (u"ࠢࡑࡣࡷ࡬ࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡰࡳࡱࡦࡩࡸࡹࡥࡥࠢࡾࢁࠧᒂ").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack1ll1l1_opy_ (u"ࠣࠤᒃ")
                    log_entry = bstack1llll1l1lll_opy_(
                        kind=bstack1ll1l1_opy_ (u"ࠤࡗࡉࡘ࡚࡟ࡂࡖࡗࡅࡈࡎࡍࡆࡐࡗࠦᒄ"),
                        message=bstack1ll1l1_opy_ (u"ࠥࠦᒅ"),
                        level=bstack1ll1l1_opy_ (u"ࠦࠧᒆ"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack1ll111l1l1l_opy_=entry.stat().st_size,
                        bstack1ll11111ll1_opy_=bstack1ll1l1_opy_ (u"ࠧࡓࡁࡏࡗࡄࡐࡤ࡛ࡐࡍࡑࡄࡈࠧᒇ"),
                        bstack1l11_opy_=os.path.abspath(entry.path),
                        bstack1l11l1l111l_opy_=hook.get(TestFramework.bstack1l11l11l1ll_opy_)
                    )
                    logs.append(log_entry)
                    _1ll111ll11l_opy_.add(abs_path)
        platform_index = os.environ[bstack1ll1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ᒈ")]
        bstack1l111llll11_opy_ = os.path.join(bstack1l1lll11l1l_opy_, (bstack1l1lllll111_opy_ + str(platform_index)), bstack1l111l1l11l_opy_, bstack1l111l11ll1_opy_)
        if not os.path.exists(bstack1l111llll11_opy_) or not os.path.isdir(bstack1l111llll11_opy_):
            self.logger.info(bstack1ll1l1_opy_ (u"ࠢࡏࡱࠣࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࡈࡰࡱ࡮ࡉࡻ࡫࡮ࡵࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻࠣࡪࡴࡻ࡮ࡥࠢࡤࡸ࠿ࠦࡻࡾࠤᒉ").format(bstack1l111llll11_opy_))
        else:
            self.logger.info(bstack1ll1l1_opy_ (u"ࠣࡒࡵࡳࡨ࡫ࡳࡴ࡫ࡱ࡫ࠥࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࡊࡲࡳࡰࡋࡶࡦࡰࡷࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴࠢࡩࡶࡴࡳࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻ࠽ࠤࢀࢃࠢᒊ").format(bstack1l111llll11_opy_))
            with os.scandir(bstack1l111llll11_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _1ll111ll11l_opy_:
                        self.logger.info(bstack1ll1l1_opy_ (u"ࠤࡓࡥࡹ࡮ࠠࡢ࡮ࡵࡩࡦࡪࡹࠡࡲࡵࡳࡨ࡫ࡳࡴࡧࡧࠤࢀࢃࠢᒋ").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack1ll1l1_opy_ (u"ࠥࠦᒌ")
                        log_entry = bstack1llll1l1lll_opy_(
                            kind=bstack1ll1l1_opy_ (u"࡙ࠦࡋࡓࡕࡡࡄࡘ࡙ࡇࡃࡉࡏࡈࡒ࡙ࠨᒍ"),
                            message=bstack1ll1l1_opy_ (u"ࠧࠨᒎ"),
                            level=bstack1ll1l1_opy_ (u"ࠨࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࠥᒏ"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack1ll111l1l1l_opy_=entry.stat().st_size,
                            bstack1ll11111ll1_opy_=bstack1ll1l1_opy_ (u"ࠢࡎࡃࡑ࡙ࡆࡒ࡟ࡖࡒࡏࡓࡆࡊࠢᒐ"),
                            bstack1l11_opy_=os.path.abspath(entry.path),
                            bstack1ll11111111_opy_=hook.get(TestFramework.bstack1l11l11l1ll_opy_)
                        )
                        logs.append(log_entry)
                        _1ll111ll11l_opy_.add(abs_path)
        hook[bstack1ll1l1_opy_ (u"ࠣ࡮ࡲ࡫ࡸࠨᒑ")] = logs
    def bstack1l1llll1lll_opy_(
        self,
        bstack1l1lll1l11l_opy_: bstack1lll1l1l1l1_opy_,
        entries: List[bstack1llll1l1lll_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack1ll1l1_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡏࡍࡤࡈࡉࡏࡡࡖࡉࡘ࡙ࡉࡐࡐࡢࡍࡉࠨᒒ"))
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
            log_entry.message = entry.message.encode(bstack1ll1l1_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤᒓ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            log_entry.level = bstack1ll1l1_opy_ (u"ࠦࠧᒔ")
            if entry.kind == bstack1ll1l1_opy_ (u"࡚ࠧࡅࡔࡖࡢࡅ࡙࡚ࡁࡄࡊࡐࡉࡓ࡚ࠢᒕ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1ll111l1l1l_opy_
                log_entry.file_path = entry.bstack1l11_opy_
        def bstack1l1llll1l11_opy_():
            bstack1ll11l1l1_opy_ = datetime.now()
            try:
                self.bstack1llllll1ll1_opy_.LogCreatedEvent(req)
                bstack1l1lll1l11l_opy_.bstack11lll1l111_opy_(bstack1ll1l1_opy_ (u"ࠨࡧࡳࡲࡦ࠾ࡸ࡫࡮ࡥࡡ࡯ࡳ࡬ࡥࡣࡳࡧࡤࡸࡪࡪ࡟ࡦࡸࡨࡲࡹࡥࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࠥᒖ"), datetime.now() - bstack1ll11l1l1_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1ll1l1_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࡸ࡫࡮ࡥࡡ࡯ࡳ࡬ࡥࡣࡳࡧࡤࡸࡪࡪ࡟ࡦࡸࡨࡲࡹࡥࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࠣࡿࢂࠨᒗ").format(str(e)))
                traceback.print_exc()
        self.bstack1111l1ll11_opy_.enqueue(bstack1l1llll1l11_opy_)
    def __1l111ll11ll_opy_(self, instance) -> None:
        bstack1ll1l1_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡒ࡯ࡢࡦࡶࠤࡨࡻࡳࡵࡱࡰࠤࡹࡧࡧࡴࠢࡩࡳࡷࠦࡴࡩࡧࠣ࡫࡮ࡼࡥ࡯ࠢࡷࡩࡸࡺࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠣ࡭ࡳࡹࡴࡢࡰࡦࡩ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡄࡴࡨࡥࡹ࡫ࡳࠡࡣࠣࡨ࡮ࡩࡴࠡࡥࡲࡲࡹࡧࡩ࡯࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡰࡪࡼࡥ࡭ࠢࡦࡹࡸࡺ࡯࡮ࠢࡰࡩࡹࡧࡤࡢࡶࡤࠤࡷ࡫ࡴࡳ࡫ࡨࡺࡪࡪࠠࡧࡴࡲࡱࠏࠦࠠࠡࠢࠣࠤࠥࠦࡃࡶࡵࡷࡳࡲ࡚ࡡࡨࡏࡤࡲࡦ࡭ࡥࡳࠢࡤࡲࡩࠦࡵࡱࡦࡤࡸࡪࡹࠠࡵࡪࡨࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࠦࡳࡵࡣࡷࡩࠥࡻࡳࡪࡰࡪࠤࡸ࡫ࡴࡠࡵࡷࡥࡹ࡫࡟ࡦࡰࡷࡶ࡮࡫ࡳ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨᒘ")
        bstack1l11ll1l11l_opy_ = {bstack1ll1l1_opy_ (u"ࠤࡦࡹࡸࡺ࡯࡮ࡡࡰࡩࡹࡧࡤࡢࡶࡤࠦᒙ"): bstack1lllll11111_opy_.bstack1l11llll111_opy_()}
        from browserstack_sdk.sdk_cli.test_framework import TestFramework
        TestFramework.bstack1l11lll1111_opy_(instance, bstack1l11ll1l11l_opy_)
    @staticmethod
    def bstack1l11ll11l1l_opy_(instance: bstack1lll1l1l1l1_opy_, bstack1l11ll11111_opy_: str):
        bstack1l111l1lll1_opy_ = (
            bstack1llll11l111_opy_.bstack1l11l1l1ll1_opy_
            if bstack1l11ll11111_opy_ == bstack1llll11l111_opy_.bstack1l111ll1l1l_opy_
            else bstack1llll11l111_opy_.bstack1l11l11llll_opy_
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
        hook = bstack1llll11l111_opy_.bstack1l11ll11l1l_opy_(instance, bstack1l11ll11111_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack1l11lll1l11_opy_, []).clear()
    @staticmethod
    def __1l11l1lll1l_opy_(instance: bstack1lll1l1l1l1_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack1ll1l1_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡳࡧࡦࡳࡷࡪࡳࠣᒚ"), None)):
            return
        if os.getenv(bstack1ll1l1_opy_ (u"ࠦࡘࡊࡋࡠࡅࡏࡍࡤࡌࡌࡂࡉࡢࡐࡔࡍࡓࠣᒛ"), bstack1ll1l1_opy_ (u"ࠧ࠷ࠢᒜ")) != bstack1ll1l1_opy_ (u"ࠨ࠱ࠣᒝ"):
            bstack1llll11l111_opy_.logger.warning(bstack1ll1l1_opy_ (u"ࠢࡪࡩࡱࡳࡷ࡯࡮ࡨࠢࡦࡥࡵࡲ࡯ࡨࠤᒞ"))
            return
        bstack1l111llll1l_opy_ = {
            bstack1ll1l1_opy_ (u"ࠣࡵࡨࡸࡺࡶࠢᒟ"): (bstack1llll11l111_opy_.bstack1l111ll1ll1_opy_, bstack1llll11l111_opy_.bstack1l11l11llll_opy_),
            bstack1ll1l1_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࠦᒠ"): (bstack1llll11l111_opy_.bstack1l111ll1l1l_opy_, bstack1llll11l111_opy_.bstack1l11l1l1ll1_opy_),
        }
        for when in (bstack1ll1l1_opy_ (u"ࠥࡷࡪࡺࡵࡱࠤᒡ"), bstack1ll1l1_opy_ (u"ࠦࡨࡧ࡬࡭ࠤᒢ"), bstack1ll1l1_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴࠢᒣ")):
            bstack1l11ll11ll1_opy_ = args[1].get_records(when)
            if not bstack1l11ll11ll1_opy_:
                continue
            records = [
                bstack1llll1l1lll_opy_(
                    kind=TestFramework.bstack1l1lll1ll11_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack1ll1l1_opy_ (u"ࠨ࡬ࡦࡸࡨࡰࡳࡧ࡭ࡦࠤᒤ")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack1ll1l1_opy_ (u"ࠢࡤࡴࡨࡥࡹ࡫ࡤࠣᒥ")) and r.created
                        else None
                    ),
                )
                for r in bstack1l11ll11ll1_opy_
                if isinstance(getattr(r, bstack1ll1l1_opy_ (u"ࠣ࡯ࡨࡷࡸࡧࡧࡦࠤᒦ"), None), str) and r.message.strip()
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
    def __1l11l1l1l11_opy_(test) -> Dict[str, Any]:
        bstack11l11l1l1l_opy_ = bstack1llll11l111_opy_.__1l11ll1l1l1_opy_(test.location) if hasattr(test, bstack1ll1l1_opy_ (u"ࠤ࡯ࡳࡨࡧࡴࡪࡱࡱࠦᒧ")) else getattr(test, bstack1ll1l1_opy_ (u"ࠥࡲࡴࡪࡥࡪࡦࠥᒨ"), None)
        test_name = test.name if hasattr(test, bstack1ll1l1_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᒩ")) else None
        bstack1l111lllll1_opy_ = test.fspath.strpath if hasattr(test, bstack1ll1l1_opy_ (u"ࠧ࡬ࡳࡱࡣࡷ࡬ࠧᒪ")) and test.fspath else None
        if not bstack11l11l1l1l_opy_ or not test_name or not bstack1l111lllll1_opy_:
            return None
        code = None
        if hasattr(test, bstack1ll1l1_opy_ (u"ࠨ࡯ࡣ࡬ࠥᒫ")):
            try:
                import inspect
                code = inspect.getsource(test.obj)
            except:
                pass
        bstack1l111l1l1ll_opy_ = []
        try:
            bstack1l111l1l1ll_opy_ = bstack11l1ll1ll_opy_.bstack111l1l1l1l_opy_(test)
        except:
            bstack1llll11l111_opy_.logger.warning(bstack1ll1l1_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡪ࡮ࡴࡤࠡࡶࡨࡷࡹࠦࡳࡤࡱࡳࡩࡸ࠲ࠠࡵࡧࡶࡸࠥࡹࡣࡰࡲࡨࡷࠥࡽࡩ࡭࡮ࠣࡦࡪࠦࡲࡦࡵࡲࡰࡻ࡫ࡤࠡ࡫ࡱࠤࡈࡒࡉࠣᒬ"))
        return {
            TestFramework.bstack1ll1ll1ll11_opy_: uuid4().__str__(),
            TestFramework.bstack1l111l1ll1l_opy_: bstack11l11l1l1l_opy_,
            TestFramework.bstack1ll1ll1l1l1_opy_: test_name,
            TestFramework.bstack1l1ll1lll1l_opy_: getattr(test, bstack1ll1l1_opy_ (u"ࠣࡰࡲࡨࡪ࡯ࡤࠣᒭ"), None),
            TestFramework.bstack1l11l1lll11_opy_: bstack1l111lllll1_opy_,
            TestFramework.bstack1l11l1111l1_opy_: bstack1llll11l111_opy_.__1l11l1l11l1_opy_(test),
            TestFramework.bstack1l11l1ll111_opy_: code,
            TestFramework.bstack1l1l1lll111_opy_: TestFramework.bstack1l11lll11ll_opy_,
            TestFramework.bstack1l1l111l1ll_opy_: bstack11l11l1l1l_opy_,
            TestFramework.bstack1l111l11lll_opy_: bstack1l111l1l1ll_opy_
        }
    @staticmethod
    def __1l11l1l11l1_opy_(test) -> List[str]:
        return (
            [getattr(f, bstack1ll1l1_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᒮ"), None) for f in test.own_markers if getattr(f, bstack1ll1l1_opy_ (u"ࠥࡲࡦࡳࡥࠣᒯ"), None)]
            if isinstance(getattr(test, bstack1ll1l1_opy_ (u"ࠦࡴࡽ࡮ࡠ࡯ࡤࡶࡰ࡫ࡲࡴࠤᒰ"), None), list)
            else []
        )
    @staticmethod
    def __1l11ll1l1l1_opy_(location):
        return bstack1ll1l1_opy_ (u"ࠧࡀ࠺ࠣᒱ").join(filter(lambda x: isinstance(x, str), location))
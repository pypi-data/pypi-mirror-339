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
from datetime import datetime, timezone
import os
from typing import Any, Tuple, Callable, List
from browserstack_sdk.sdk_cli.bstack1111l11lll_opy_ import bstack11111l11ll_opy_, bstack1111l1ll1l_opy_, bstack111111111l_opy_
from browserstack_sdk.sdk_cli.bstack1lll11llll1_opy_ import bstack1lllll1l111_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l1llll_opy_ import bstack1lll1lll11l_opy_
from browserstack_sdk.sdk_cli.bstack1lllll1ll11_opy_ import bstack1lll1l11ll1_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1llllll1lll_opy_, bstack1lllllll111_opy_, bstack1lll111lll1_opy_, bstack1lll11ll111_opy_
from json import dumps, JSONEncoder
import grpc
from browserstack_sdk import sdk_pb2 as structs
import sys
import traceback
import time
import json
from bstack_utils.helper import bstack1ll1111l1ll_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
bstack1ll111l11ll_opy_ = [bstack11l1l11_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᆮ"), bstack11l1l11_opy_ (u"ࠧࡶࡡࡳࡧࡱࡸࠧᆯ"), bstack11l1l11_opy_ (u"ࠨࡣࡰࡰࡩ࡭࡬ࠨᆰ"), bstack11l1l11_opy_ (u"ࠢࡴࡧࡶࡷ࡮ࡵ࡮ࠣᆱ"), bstack11l1l11_opy_ (u"ࠣࡲࡤࡸ࡭ࠨᆲ")]
bstack1ll111111l1_opy_ = {
    bstack11l1l11_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠰ࡳࡽࡹ࡮࡯࡯࠰ࡌࡸࡪࡳࠢᆳ"): bstack1ll111l11ll_opy_,
    bstack11l1l11_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠱ࡴࡾࡺࡨࡰࡰ࠱ࡔࡦࡩ࡫ࡢࡩࡨࠦᆴ"): bstack1ll111l11ll_opy_,
    bstack11l1l11_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠲ࡵࡿࡴࡩࡱࡱ࠲ࡒࡵࡤࡶ࡮ࡨࠦᆵ"): bstack1ll111l11ll_opy_,
    bstack11l1l11_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠳ࡶࡹࡵࡪࡲࡲ࠳ࡉ࡬ࡢࡵࡶࠦᆶ"): bstack1ll111l11ll_opy_,
    bstack11l1l11_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠴ࡰࡺࡶ࡫ࡳࡳ࠴ࡆࡶࡰࡦࡸ࡮ࡵ࡮ࠣᆷ"): bstack1ll111l11ll_opy_
    + [
        bstack11l1l11_opy_ (u"ࠢࡰࡴ࡬࡫࡮ࡴࡡ࡭ࡰࡤࡱࡪࠨᆸ"),
        bstack11l1l11_opy_ (u"ࠣ࡭ࡨࡽࡼࡵࡲࡥࡵࠥᆹ"),
        bstack11l1l11_opy_ (u"ࠤࡩ࡭ࡽࡺࡵࡳࡧ࡬ࡲ࡫ࡵࠢᆺ"),
        bstack11l1l11_opy_ (u"ࠥ࡯ࡪࡿࡷࡰࡴࡧࡷࠧᆻ"),
        bstack11l1l11_opy_ (u"ࠦࡨࡧ࡬࡭ࡵࡳࡩࡨࠨᆼ"),
        bstack11l1l11_opy_ (u"ࠧࡩࡡ࡭࡮ࡲࡦ࡯ࠨᆽ"),
        bstack11l1l11_opy_ (u"ࠨࡳࡵࡣࡵࡸࠧᆾ"),
        bstack11l1l11_opy_ (u"ࠢࡴࡶࡲࡴࠧᆿ"),
        bstack11l1l11_opy_ (u"ࠣࡦࡸࡶࡦࡺࡩࡰࡰࠥᇀ"),
        bstack11l1l11_opy_ (u"ࠤࡺ࡬ࡪࡴࠢᇁ"),
    ],
    bstack11l1l11_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠱ࡱࡦ࡯࡮࠯ࡕࡨࡷࡸ࡯࡯࡯ࠤᇂ"): [bstack11l1l11_opy_ (u"ࠦࡸࡺࡡࡳࡶࡳࡥࡹ࡮ࠢᇃ"), bstack11l1l11_opy_ (u"ࠧࡺࡥࡴࡶࡶࡪࡦ࡯࡬ࡦࡦࠥᇄ"), bstack11l1l11_opy_ (u"ࠨࡴࡦࡵࡷࡷࡨࡵ࡬࡭ࡧࡦࡸࡪࡪࠢᇅ"), bstack11l1l11_opy_ (u"ࠢࡪࡶࡨࡱࡸࠨᇆ")],
    bstack11l1l11_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠯ࡥࡲࡲ࡫࡯ࡧ࠯ࡅࡲࡲ࡫࡯ࡧࠣᇇ"): [bstack11l1l11_opy_ (u"ࠤ࡬ࡲࡻࡵࡣࡢࡶ࡬ࡳࡳࡥࡰࡢࡴࡤࡱࡸࠨᇈ"), bstack11l1l11_opy_ (u"ࠥࡥࡷ࡭ࡳࠣᇉ")],
    bstack11l1l11_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠲࡫࡯ࡸࡵࡷࡵࡩࡸ࠴ࡆࡪࡺࡷࡹࡷ࡫ࡄࡦࡨࠥᇊ"): [bstack11l1l11_opy_ (u"ࠧࡹࡣࡰࡲࡨࠦᇋ"), bstack11l1l11_opy_ (u"ࠨࡡࡳࡩࡱࡥࡲ࡫ࠢᇌ"), bstack11l1l11_opy_ (u"ࠢࡧࡷࡱࡧࠧᇍ"), bstack11l1l11_opy_ (u"ࠣࡲࡤࡶࡦࡳࡳࠣᇎ"), bstack11l1l11_opy_ (u"ࠤࡸࡲ࡮ࡺࡴࡦࡵࡷࠦᇏ"), bstack11l1l11_opy_ (u"ࠥ࡭ࡩࡹࠢᇐ")],
    bstack11l1l11_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠲࡫࡯ࡸࡵࡷࡵࡩࡸ࠴ࡓࡶࡤࡕࡩࡶࡻࡥࡴࡶࠥᇑ"): [bstack11l1l11_opy_ (u"ࠧ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࠥᇒ"), bstack11l1l11_opy_ (u"ࠨࡰࡢࡴࡤࡱࠧᇓ"), bstack11l1l11_opy_ (u"ࠢࡱࡣࡵࡥࡲࡥࡩ࡯ࡦࡨࡼࠧᇔ")],
    bstack11l1l11_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠯ࡴࡸࡲࡳ࡫ࡲ࠯ࡅࡤࡰࡱࡏ࡮ࡧࡱࠥᇕ"): [bstack11l1l11_opy_ (u"ࠤࡺ࡬ࡪࡴࠢᇖ"), bstack11l1l11_opy_ (u"ࠥࡶࡪࡹࡵ࡭ࡶࠥᇗ")],
    bstack11l1l11_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠲ࡲࡧࡲ࡬࠰ࡶࡸࡷࡻࡣࡵࡷࡵࡩࡸ࠴ࡎࡰࡦࡨࡏࡪࡿࡷࡰࡴࡧࡷࠧᇘ"): [bstack11l1l11_opy_ (u"ࠧࡴ࡯ࡥࡧࠥᇙ"), bstack11l1l11_opy_ (u"ࠨࡰࡢࡴࡨࡲࡹࠨᇚ")],
    bstack11l1l11_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠮࡮ࡣࡵ࡯࠳ࡹࡴࡳࡷࡦࡸࡺࡸࡥࡴ࠰ࡐࡥࡷࡱࠢᇛ"): [bstack11l1l11_opy_ (u"ࠣࡰࡤࡱࡪࠨᇜ"), bstack11l1l11_opy_ (u"ࠤࡤࡶ࡬ࡹࠢᇝ"), bstack11l1l11_opy_ (u"ࠥ࡯ࡼࡧࡲࡨࡵࠥᇞ")],
}
class bstack1lll1ll1111_opy_(bstack1lllll1l111_opy_):
    bstack1l1llll1ll1_opy_ = bstack11l1l11_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡧࡩ࡫࡫ࡲࡳࡧࡧࠦᇟ")
    bstack1ll11l11ll1_opy_ = bstack11l1l11_opy_ (u"ࠧࡏࡎࡇࡑࠥᇠ")
    bstack1ll1111llll_opy_ = bstack11l1l11_opy_ (u"ࠨࡅࡓࡔࡒࡖࠧᇡ")
    bstack1ll11l11111_opy_: Callable
    bstack1l1llllll11_opy_: Callable
    def __init__(self, bstack1llll11ll1l_opy_, bstack1llll1l1l1l_opy_):
        super().__init__()
        self.bstack1ll1l1l11l1_opy_ = bstack1llll1l1l1l_opy_
        if os.getenv(bstack11l1l11_opy_ (u"ࠢࡔࡆࡎࡣࡈࡒࡉࡠࡈࡏࡅࡌࡥࡏ࠲࠳࡜ࠦᇢ"), bstack11l1l11_opy_ (u"ࠣ࠳ࠥᇣ")) != bstack11l1l11_opy_ (u"ࠤ࠴ࠦᇤ") or not self.is_enabled():
            self.logger.warning(bstack11l1l11_opy_ (u"ࠥࠦᇥ") + str(self.__class__.__name__) + bstack11l1l11_opy_ (u"ࠦࠥࡪࡩࡴࡣࡥࡰࡪࡪࠢᇦ"))
            return
        TestFramework.bstack1ll1l11l11l_opy_((bstack1llllll1lll_opy_.TEST, bstack1lll111lll1_opy_.PRE), self.bstack1ll1l1ll11l_opy_)
        TestFramework.bstack1ll1l11l11l_opy_((bstack1llllll1lll_opy_.TEST, bstack1lll111lll1_opy_.POST), self.bstack1ll1lll1l1l_opy_)
        for event in bstack1llllll1lll_opy_:
            for state in bstack1lll111lll1_opy_:
                TestFramework.bstack1ll1l11l11l_opy_((event, state), self.bstack1l1llll11l1_opy_)
        bstack1llll11ll1l_opy_.bstack1ll1l11l11l_opy_((bstack1111l1ll1l_opy_.bstack111111l111_opy_, bstack111111111l_opy_.POST), self.bstack1ll11l11lll_opy_)
        self.bstack1ll11l11111_opy_ = sys.stdout.write
        sys.stdout.write = self.bstack1ll11111lll_opy_(bstack1lll1ll1111_opy_.bstack1ll11l11ll1_opy_, self.bstack1ll11l11111_opy_)
        self.bstack1l1llllll11_opy_ = sys.stderr.write
        sys.stderr.write = self.bstack1ll11111lll_opy_(bstack1lll1ll1111_opy_.bstack1ll1111llll_opy_, self.bstack1l1llllll11_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1llll11l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lllllll111_opy_,
        bstack1111l1ll11_opy_: Tuple[bstack1llllll1lll_opy_, bstack1lll111lll1_opy_],
        *args,
        **kwargs,
    ):
        if f.bstack1l1llll1111_opy_() and instance:
            bstack1ll11111ll1_opy_ = datetime.now()
            test_framework_state, test_hook_state = bstack1111l1ll11_opy_
            if test_framework_state == bstack1llllll1lll_opy_.SETUP_FIXTURE:
                return
            elif test_framework_state == bstack1llllll1lll_opy_.LOG:
                bstack1l1ll1l111_opy_ = datetime.now()
                entries = f.bstack1l1lllllll1_opy_(instance, bstack1111l1ll11_opy_)
                if entries:
                    self.bstack1ll111lllll_opy_(instance, entries)
                    instance.bstack1ll11lll_opy_(bstack11l1l11_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡷࡪࡴࡤࡠ࡮ࡲ࡫ࡤࡩࡲࡦࡣࡷࡩࡩࡥࡥࡷࡧࡱࡸࠧᇧ"), datetime.now() - bstack1l1ll1l111_opy_)
                    f.bstack1ll11111111_opy_(instance, bstack1111l1ll11_opy_)
                instance.bstack1ll11lll_opy_(bstack11l1l11_opy_ (u"ࠨ࡯࠲࠳ࡼ࠾ࡴࡴ࡟ࡢ࡮࡯ࡣࡹ࡫ࡳࡵࡡࡨࡺࡪࡴࡴࡴࠤᇨ"), datetime.now() - bstack1ll11111ll1_opy_)
                return # bstack1l1lllll111_opy_ not send this event with the bstack1ll111l1l11_opy_ bstack1ll111l1111_opy_
            elif (
                test_framework_state == bstack1llllll1lll_opy_.TEST
                and test_hook_state == bstack1lll111lll1_opy_.POST
                and not f.bstack1111111l11_opy_(instance, TestFramework.bstack1ll11l111ll_opy_)
            ):
                self.logger.warning(bstack11l1l11_opy_ (u"ࠢࡥࡴࡲࡴࡵ࡯࡮ࡨࠢࡧࡹࡪࠦࡴࡰࠢ࡯ࡥࡨࡱࠠࡰࡨࠣࡶࡪࡹࡵ࡭ࡶࡶࠤࠧᇩ") + str(TestFramework.bstack1111111l11_opy_(instance, TestFramework.bstack1ll11l111ll_opy_)) + bstack11l1l11_opy_ (u"ࠣࠤᇪ"))
                f.bstack1111111l1l_opy_(instance, bstack1lll1ll1111_opy_.bstack1l1llll1ll1_opy_, True)
                return # bstack1l1lllll111_opy_ not send this event bstack1l1lllll1ll_opy_ bstack1ll11l11l11_opy_
            elif (
                f.bstack11111l1l1l_opy_(instance, bstack1lll1ll1111_opy_.bstack1l1llll1ll1_opy_, False)
                and test_framework_state == bstack1llllll1lll_opy_.LOG_REPORT
                and test_hook_state == bstack1lll111lll1_opy_.POST
                and f.bstack1111111l11_opy_(instance, TestFramework.bstack1ll11l111ll_opy_)
            ):
                self.logger.warning(bstack11l1l11_opy_ (u"ࠤ࡬ࡲ࡯࡫ࡣࡵ࡫ࡱ࡫࡚ࠥࡥࡴࡶࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࡘࡺࡡࡵࡧ࠱ࡘࡊ࡙ࡔ࠭ࠢࡗࡩࡸࡺࡈࡰࡱ࡮ࡗࡹࡧࡴࡦ࠰ࡓࡓࡘ࡚ࠠࠣᇫ") + str(TestFramework.bstack1111111l11_opy_(instance, TestFramework.bstack1ll11l111ll_opy_)) + bstack11l1l11_opy_ (u"ࠥࠦᇬ"))
                self.bstack1l1llll11l1_opy_(f, instance, (bstack1llllll1lll_opy_.TEST, bstack1lll111lll1_opy_.POST), *args, **kwargs)
            bstack1l1ll1l111_opy_ = datetime.now()
            data = instance.data.copy()
            bstack1ll111lll1l_opy_ = sorted(
                filter(lambda x: x.get(bstack11l1l11_opy_ (u"ࠦࡪࡼࡥ࡯ࡶࡢࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠢᇭ"), None), data.pop(bstack11l1l11_opy_ (u"ࠧࡺࡥࡴࡶࡢࡪ࡮ࡾࡴࡶࡴࡨࡷࠧᇮ"), {}).values()),
                key=lambda x: x[bstack11l1l11_opy_ (u"ࠨࡥࡷࡧࡱࡸࡤࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠤᇯ")],
            )
            if bstack1lll1lll11l_opy_.bstack1ll111lll11_opy_ in data:
                data.pop(bstack1lll1lll11l_opy_.bstack1ll111lll11_opy_)
            data.update({bstack11l1l11_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡬ࡩࡹࡶࡸࡶࡪࡹࠢᇰ"): bstack1ll111lll1l_opy_})
            instance.bstack1ll11lll_opy_(bstack11l1l11_opy_ (u"ࠣ࡬ࡶࡳࡳࡀࡴࡦࡵࡷࡣ࡫࡯ࡸࡵࡷࡵࡩࡸࠨᇱ"), datetime.now() - bstack1l1ll1l111_opy_)
            bstack1l1ll1l111_opy_ = datetime.now()
            event_json = dumps(data, cls=bstack1ll111llll1_opy_)
            instance.bstack1ll11lll_opy_(bstack11l1l11_opy_ (u"ࠤ࡭ࡷࡴࡴ࠺ࡰࡰࡢࡥࡱࡲ࡟ࡵࡧࡶࡸࡤ࡫ࡶࡦࡰࡷࡷࠧᇲ"), datetime.now() - bstack1l1ll1l111_opy_)
            self.bstack1ll111l1111_opy_(instance, bstack1111l1ll11_opy_, event_json=event_json)
            instance.bstack1ll11lll_opy_(bstack11l1l11_opy_ (u"ࠥࡳ࠶࠷ࡹ࠻ࡱࡱࡣࡦࡲ࡬ࡠࡶࡨࡷࡹࡥࡥࡷࡧࡱࡸࡸࠨᇳ"), datetime.now() - bstack1ll11111ll1_opy_)
    def bstack1ll1l1ll11l_opy_(
        self,
        f: TestFramework,
        instance: bstack1lllllll111_opy_,
        bstack1111l1ll11_opy_: Tuple[bstack1llllll1lll_opy_, bstack1lll111lll1_opy_],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack1l1ll1l11l_opy_ import bstack1lll1llll1l_opy_
        bstack1ll1ll1l1l1_opy_ = bstack1lll1llll1l_opy_.bstack1ll1ll1lll1_opy_(EVENTS.bstack1l1111111_opy_.value)
        self.bstack1ll1l1l11l1_opy_.bstack1ll111ll11l_opy_(instance, f, bstack1111l1ll11_opy_, *args, **kwargs)
        bstack1lll1llll1l_opy_.end(EVENTS.bstack1l1111111_opy_.value, bstack1ll1ll1l1l1_opy_ + bstack11l1l11_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦᇴ"), bstack1ll1ll1l1l1_opy_ + bstack11l1l11_opy_ (u"ࠧࡀࡥ࡯ࡦࠥᇵ"), status=True, failure=None, test_name=None)
    def bstack1ll1lll1l1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1lllllll111_opy_,
        bstack1111l1ll11_opy_: Tuple[bstack1llllll1lll_opy_, bstack1lll111lll1_opy_],
        *args,
        **kwargs,
    ):
        req = self.bstack1ll1l1l11l1_opy_.bstack1l1lllll11l_opy_(instance, f, bstack1111l1ll11_opy_, *args, **kwargs)
        self.bstack1ll111l1l1l_opy_(f, instance, req)
    @measure(event_name=EVENTS.bstack1l1llll11ll_opy_, stage=STAGE.bstack1l1ll1lll_opy_)
    def bstack1ll111l1l1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1lllllll111_opy_,
        req: structs.TestSessionEventRequest
    ):
        if not req:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠨࡓ࡬࡫ࡳࡴ࡮ࡴࡧࠡࡖࡨࡷࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡋࡶࡦࡰࡷࠤ࡬ࡘࡐࡄࠢࡦࡥࡱࡲ࠺ࠡࡐࡲࠤࡻࡧ࡬ࡪࡦࠣࡶࡪࡷࡵࡦࡵࡷࠤࡩࡧࡴࡢࠤᇶ"))
            return
        bstack1l1ll1l111_opy_ = datetime.now()
        try:
            r = self.bstack1lll11lll1l_opy_.TestSessionEvent(req)
            instance.bstack1ll11lll_opy_(bstack11l1l11_opy_ (u"ࠢࡨࡴࡳࡧ࠿ࡹࡥ࡯ࡦࡢࡸࡪࡹࡴࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡨࡺࡪࡴࡴࠣᇷ"), datetime.now() - bstack1l1ll1l111_opy_)
            f.bstack1111111l1l_opy_(instance, self.bstack1ll1l1l11l1_opy_.bstack1ll11111l1l_opy_, r.success)
            if not r.success:
                self.logger.info(bstack11l1l11_opy_ (u"ࠣࡴࡨࡧࡪ࡯ࡶࡦࡦࠣࡪࡷࡵ࡭ࠡࡵࡨࡶࡻ࡫ࡲ࠻ࠢࠥᇸ") + str(r) + bstack11l1l11_opy_ (u"ࠤࠥᇹ"))
        except grpc.RpcError as e:
            self.logger.error(bstack11l1l11_opy_ (u"ࠥࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࠣᇺ") + str(e) + bstack11l1l11_opy_ (u"ࠦࠧᇻ"))
            traceback.print_exc()
            raise e
    def bstack1ll11l11lll_opy_(
        self,
        f: bstack1lll1l11ll1_opy_,
        _driver: object,
        exec: Tuple[bstack11111l11ll_opy_, str],
        _1l1lllll1l1_opy_: Tuple[bstack1111l1ll1l_opy_, bstack111111111l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if not bstack1lll1l11ll1_opy_.bstack1ll1ll11l1l_opy_(method_name):
            return
        if f.bstack1ll1ll1l111_opy_(*args) != bstack1lll1l11ll1_opy_.bstack1ll1111l111_opy_:
            return
        bstack1ll11111ll1_opy_ = datetime.now()
        screenshot = result.get(bstack11l1l11_opy_ (u"ࠧࡼࡡ࡭ࡷࡨࠦᇼ"), None) if isinstance(result, dict) else None
        if not isinstance(screenshot, str) or len(screenshot) <= 0:
            self.logger.warning(bstack11l1l11_opy_ (u"ࠨࡩ࡯ࡸࡤࡰ࡮ࡪࠠࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠤ࡮ࡳࡡࡨࡧࠣࡦࡦࡹࡥ࠷࠶ࠣࡷࡹࡸࠢᇽ"))
            return
        bstack1ll11l11l1l_opy_ = self.bstack1ll11l111l1_opy_(instance)
        if bstack1ll11l11l1l_opy_:
            entry = bstack1lll11ll111_opy_(TestFramework.bstack1l1llll1lll_opy_, screenshot)
            self.bstack1ll111lllll_opy_(bstack1ll11l11l1l_opy_, [entry])
            instance.bstack1ll11lll_opy_(bstack11l1l11_opy_ (u"ࠢࡰ࠳࠴ࡽ࠿ࡵ࡮ࡠࡣࡩࡸࡪࡸ࡟ࡦࡺࡨࡧࡺࡺࡥࠣᇾ"), datetime.now() - bstack1ll11111ll1_opy_)
        else:
            self.logger.warning(bstack11l1l11_opy_ (u"ࠣࡷࡱࡥࡧࡲࡥࠡࡶࡲࠤࡩ࡫ࡴࡦࡴࡰ࡭ࡳ࡫ࠠࡵࡧࡶࡸࠥ࡬࡯ࡳࠢࡺ࡬࡮ࡩࡨࠡࡶ࡫࡭ࡸࠦࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠣࡻࡦࡹࠠࡵࡣ࡮ࡩࡳࠦࡢࡺࠢࡧࡶ࡮ࡼࡥࡳ࠿ࠥᇿ") + str(instance.ref()) + bstack11l1l11_opy_ (u"ࠤࠥሀ"))
    @measure(event_name=EVENTS.bstack1ll111l1lll_opy_, stage=STAGE.bstack1l1ll1lll_opy_)
    def bstack1ll111lllll_opy_(
        self,
        bstack1ll11l11l1l_opy_: bstack1lllllll111_opy_,
        entries: List[bstack1lll11ll111_opy_],
    ):
        self.bstack1ll1l1111l1_opy_()
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack11111l1l1l_opy_(bstack1ll11l11l1l_opy_, TestFramework.bstack1ll1l11llll_opy_)
        req.execution_context.hash = str(bstack1ll11l11l1l_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1ll11l11l1l_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1ll11l11l1l_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack11111l1l1l_opy_(bstack1ll11l11l1l_opy_, TestFramework.bstack1ll1l1llll1_opy_)
            log_entry.test_framework_version = TestFramework.bstack11111l1l1l_opy_(bstack1ll11l11l1l_opy_, TestFramework.bstack1ll11111l11_opy_)
            log_entry.uuid = TestFramework.bstack11111l1l1l_opy_(bstack1ll11l11l1l_opy_, TestFramework.bstack1ll1lll11l1_opy_)
            log_entry.test_framework_state = bstack1ll11l11l1l_opy_.state.name
            log_entry.message = entry.message.encode(bstack11l1l11_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤሁ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            if isinstance(entry.level, str) and len(entry.level.strip()) > 0:
                log_entry.level = entry.level.strip()
        def bstack1ll1111l1l1_opy_():
            bstack1l1ll1l111_opy_ = datetime.now()
            try:
                self.bstack1lll11lll1l_opy_.LogCreatedEvent(req)
                if entry.kind == TestFramework.bstack1l1llll1lll_opy_:
                    bstack1ll11l11l1l_opy_.bstack1ll11lll_opy_(bstack11l1l11_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡶࡩࡳࡪ࡟࡭ࡱࡪࡣࡨࡸࡥࡢࡶࡨࡨࡤ࡫ࡶࡦࡰࡷࡣࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠣሂ"), datetime.now() - bstack1l1ll1l111_opy_)
                else:
                    bstack1ll11l11l1l_opy_.bstack1ll11lll_opy_(bstack11l1l11_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡷࡪࡴࡤࡠ࡮ࡲ࡫ࡤࡩࡲࡦࡣࡷࡩࡩࡥࡥࡷࡧࡱࡸࡤࡲ࡯ࡨࠤሃ"), datetime.now() - bstack1l1ll1l111_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack11l1l11_opy_ (u"ࠨࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࠦሄ") + str(e))
                traceback.print_exc()
                raise e
        self.bstack1111l1llll_opy_.enqueue(bstack1ll1111l1l1_opy_)
    @measure(event_name=EVENTS.bstack1ll11l1111l_opy_, stage=STAGE.bstack1l1ll1lll_opy_)
    def bstack1ll111l1111_opy_(
        self,
        instance: bstack1lllllll111_opy_,
        bstack1111l1ll11_opy_: Tuple[bstack1llllll1lll_opy_, bstack1lll111lll1_opy_],
        event_json=None,
    ):
        self.bstack1ll1l1111l1_opy_()
        req = structs.TestFrameworkEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack11111l1l1l_opy_(instance, TestFramework.bstack1ll1l11llll_opy_)
        req.test_framework_name = TestFramework.bstack11111l1l1l_opy_(instance, TestFramework.bstack1ll1l1llll1_opy_)
        req.test_framework_version = TestFramework.bstack11111l1l1l_opy_(instance, TestFramework.bstack1ll11111l11_opy_)
        req.test_framework_state = bstack1111l1ll11_opy_[0].name
        req.test_hook_state = bstack1111l1ll11_opy_[1].name
        started_at = TestFramework.bstack11111l1l1l_opy_(instance, TestFramework.bstack1ll111111ll_opy_, None)
        if started_at:
            req.started_at = started_at.isoformat()
        ended_at = TestFramework.bstack11111l1l1l_opy_(instance, TestFramework.bstack1ll111ll111_opy_, None)
        if ended_at:
            req.ended_at = ended_at.isoformat()
        req.uuid = instance.ref()
        req.event_json = (event_json if event_json else dumps(instance.data, cls=bstack1ll111llll1_opy_)).encode(bstack11l1l11_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨህ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        def bstack1ll1111l1l1_opy_():
            bstack1l1ll1l111_opy_ = datetime.now()
            try:
                self.bstack1lll11lll1l_opy_.TestFrameworkEvent(req)
                instance.bstack1ll11lll_opy_(bstack11l1l11_opy_ (u"ࠣࡩࡵࡴࡨࡀࡳࡦࡰࡧࡣࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤ࡫ࡶࡦࡰࡷࠦሆ"), datetime.now() - bstack1l1ll1l111_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack11l1l11_opy_ (u"ࠤࡵࡴࡨ࠳ࡥࡳࡴࡲࡶ࠿ࠦࠢሇ") + str(e))
                traceback.print_exc()
                raise e
        self.bstack1111l1llll_opy_.enqueue(bstack1ll1111l1l1_opy_)
    def bstack1ll1111111l_opy_(self, event_url: str, bstack111ll1ll1l_opy_: dict) -> bool:
        return True # always return True so that old bstack1ll111ll1l1_opy_ bstack1ll111l11l1_opy_'t bstack1ll111ll1ll_opy_
    def bstack1ll11l111l1_opy_(self, instance: bstack11111l11ll_opy_):
        bstack1ll1111ll11_opy_ = TestFramework.bstack1111l1l1ll_opy_(instance.context)
        for t in bstack1ll1111ll11_opy_:
            bstack1ll1111l11l_opy_ = TestFramework.bstack11111l1l1l_opy_(t, bstack1lll1lll11l_opy_.bstack1ll111lll11_opy_, [])
            if any(instance is d[1] for d in bstack1ll1111l11l_opy_):
                return t
    def bstack1l1llll111l_opy_(self, message):
        self.bstack1ll11l11111_opy_(message + bstack11l1l11_opy_ (u"ࠥࡠࡳࠨለ"))
    def log_error(self, message):
        self.bstack1l1llllll11_opy_(message + bstack11l1l11_opy_ (u"ࠦࡡࡴࠢሉ"))
    def bstack1ll11111lll_opy_(self, level, original_func):
        def bstack1l1llllllll_opy_(*args):
            return_value = original_func(*args)
            if not args or not isinstance(args[0], str) or not args[0].strip():
                return return_value
            message = args[0].strip()
            bstack1ll1111ll11_opy_ = TestFramework.bstack1ll1111lll1_opy_()
            if not bstack1ll1111ll11_opy_:
                return return_value
            bstack1ll11l11l1l_opy_ = next(
                (
                    instance
                    for instance in bstack1ll1111ll11_opy_
                    if TestFramework.bstack1111111l11_opy_(instance, TestFramework.bstack1ll1lll11l1_opy_)
                ),
                None,
            )
            if not bstack1ll11l11l1l_opy_:
                return
            entry = bstack1lll11ll111_opy_(TestFramework.bstack1ll11l1l11l_opy_, message, level)
            self.bstack1ll111lllll_opy_(bstack1ll11l11l1l_opy_, [entry])
            return return_value
        return bstack1l1llllllll_opy_
class bstack1ll111llll1_opy_(JSONEncoder):
    def __init__(self, **kwargs):
        self.bstack1l1llll1l1l_opy_ = set()
        kwargs[bstack11l1l11_opy_ (u"ࠧࡹ࡫ࡪࡲ࡮ࡩࡾࡹࠢሊ")] = True
        super().__init__(**kwargs)
    def default(self, obj):
        return bstack1ll11l1l111_opy_(obj, self.bstack1l1llll1l1l_opy_)
def bstack1ll1111ll1l_opy_(obj):
    return isinstance(obj, (str, int, float, bool, type(None)))
def bstack1ll11l1l111_opy_(obj, bstack1l1llll1l1l_opy_=None, max_depth=3):
    if bstack1l1llll1l1l_opy_ is None:
        bstack1l1llll1l1l_opy_ = set()
    if id(obj) in bstack1l1llll1l1l_opy_ or max_depth <= 0:
        return None
    max_depth -= 1
    bstack1l1llll1l1l_opy_.add(id(obj))
    if isinstance(obj, datetime):
        return obj.isoformat()
    bstack1l1llllll1l_opy_ = TestFramework.bstack1l1llll1l11_opy_(obj)
    bstack1ll111l1ll1_opy_ = next((k.lower() in bstack1l1llllll1l_opy_.lower() for k in bstack1ll111111l1_opy_.keys()), None)
    if bstack1ll111l1ll1_opy_:
        obj = TestFramework.bstack1ll111l111l_opy_(obj, bstack1ll111111l1_opy_[bstack1ll111l1ll1_opy_])
    if not isinstance(obj, dict):
        keys = []
        if hasattr(obj, bstack11l1l11_opy_ (u"ࠨ࡟ࡠࡵ࡯ࡳࡹࡹ࡟ࡠࠤላ")):
            keys = getattr(obj, bstack11l1l11_opy_ (u"ࠢࡠࡡࡶࡰࡴࡺࡳࡠࡡࠥሌ"), [])
        elif hasattr(obj, bstack11l1l11_opy_ (u"ࠣࡡࡢࡨ࡮ࡩࡴࡠࡡࠥል")):
            keys = getattr(obj, bstack11l1l11_opy_ (u"ࠤࡢࡣࡩ࡯ࡣࡵࡡࡢࠦሎ"), {}).keys()
        else:
            keys = dir(obj)
        obj = {k: getattr(obj, k, None) for k in keys if not str(k).startswith(bstack11l1l11_opy_ (u"ࠥࡣࠧሏ"))}
        if not obj and bstack1l1llllll1l_opy_ == bstack11l1l11_opy_ (u"ࠦࡵࡧࡴࡩ࡮࡬ࡦ࠳ࡖ࡯ࡴ࡫ࡻࡔࡦࡺࡨࠣሐ"):
            obj = {bstack11l1l11_opy_ (u"ࠧࡶࡡࡵࡪࠥሑ"): str(obj)}
    result = {}
    for key, value in obj.items():
        if not bstack1ll1111ll1l_opy_(key) or str(key).startswith(bstack11l1l11_opy_ (u"ࠨ࡟ࠣሒ")):
            continue
        if value is not None and bstack1ll1111ll1l_opy_(value):
            result[key] = value
        elif isinstance(value, dict):
            r = bstack1ll11l1l111_opy_(value, bstack1l1llll1l1l_opy_, max_depth)
            if r is not None:
                result[key] = r
        elif isinstance(value, (list, tuple, set, frozenset)):
            result[key] = list(filter(None, [bstack1ll11l1l111_opy_(o, bstack1l1llll1l1l_opy_, max_depth) for o in value]))
    return result or None
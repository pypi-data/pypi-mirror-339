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
from datetime import datetime, timezone
import os
from pathlib import Path
from typing import Any, Tuple, Callable, List
from browserstack_sdk.sdk_cli.bstack111111l1ll_opy_ import bstack1llllllllll_opy_, bstack11111ll1l1_opy_, bstack1111l1l1l1_opy_
from browserstack_sdk.sdk_cli.bstack1lllll1l1ll_opy_ import bstack1lll1llll11_opy_
from browserstack_sdk.sdk_cli.bstack1lll11111ll_opy_ import bstack1lll1l1l11l_opy_
from browserstack_sdk.sdk_cli.bstack1lll1ll11ll_opy_ import bstack1lll1ll1lll_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1lllllll1ll_opy_, bstack1lll1l1l1l1_opy_, bstack1lll1l11l1l_opy_, bstack1llll1l1lll_opy_
from json import dumps, JSONEncoder
import grpc
from browserstack_sdk import sdk_pb2 as structs
import sys
import traceback
import time
import json
from bstack_utils.helper import bstack1l1llll11ll_opy_, bstack1ll1111ll11_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
bstack1l1llll1l1l_opy_ = [bstack1ll1l1_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᆰ"), bstack1ll1l1_opy_ (u"ࠢࡱࡣࡵࡩࡳࡺࠢᆱ"), bstack1ll1l1_opy_ (u"ࠣࡥࡲࡲ࡫࡯ࡧࠣᆲ"), bstack1ll1l1_opy_ (u"ࠤࡶࡩࡸࡹࡩࡰࡰࠥᆳ"), bstack1ll1l1_opy_ (u"ࠥࡴࡦࡺࡨࠣᆴ")]
bstack1l1lll11l1l_opy_ = bstack1ll1111ll11_opy_()
bstack1l1lllll111_opy_ = bstack1ll1l1_opy_ (u"࡚ࠦࡶ࡬ࡰࡣࡧࡩࡩࡇࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵ࠰ࠦᆵ")
bstack1ll111lllll_opy_ = {
    bstack1ll1l1_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠳ࡶࡹࡵࡪࡲࡲ࠳ࡏࡴࡦ࡯ࠥᆶ"): bstack1l1llll1l1l_opy_,
    bstack1ll1l1_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠴ࡰࡺࡶ࡫ࡳࡳ࠴ࡐࡢࡥ࡮ࡥ࡬࡫ࠢᆷ"): bstack1l1llll1l1l_opy_,
    bstack1ll1l1_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠮ࡱࡻࡷ࡬ࡴࡴ࠮ࡎࡱࡧࡹࡱ࡫ࠢᆸ"): bstack1l1llll1l1l_opy_,
    bstack1ll1l1_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠯ࡲࡼࡸ࡭ࡵ࡮࠯ࡅ࡯ࡥࡸࡹࠢᆹ"): bstack1l1llll1l1l_opy_,
    bstack1ll1l1_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠰ࡳࡽࡹ࡮࡯࡯࠰ࡉࡹࡳࡩࡴࡪࡱࡱࠦᆺ"): bstack1l1llll1l1l_opy_
    + [
        bstack1ll1l1_opy_ (u"ࠥࡳࡷ࡯ࡧࡪࡰࡤࡰࡳࡧ࡭ࡦࠤᆻ"),
        bstack1ll1l1_opy_ (u"ࠦࡰ࡫ࡹࡸࡱࡵࡨࡸࠨᆼ"),
        bstack1ll1l1_opy_ (u"ࠧ࡬ࡩࡹࡶࡸࡶࡪ࡯࡮ࡧࡱࠥᆽ"),
        bstack1ll1l1_opy_ (u"ࠨ࡫ࡦࡻࡺࡳࡷࡪࡳࠣᆾ"),
        bstack1ll1l1_opy_ (u"ࠢࡤࡣ࡯ࡰࡸࡶࡥࡤࠤᆿ"),
        bstack1ll1l1_opy_ (u"ࠣࡥࡤࡰࡱࡵࡢ࡫ࠤᇀ"),
        bstack1ll1l1_opy_ (u"ࠤࡶࡸࡦࡸࡴࠣᇁ"),
        bstack1ll1l1_opy_ (u"ࠥࡷࡹࡵࡰࠣᇂ"),
        bstack1ll1l1_opy_ (u"ࠦࡩࡻࡲࡢࡶ࡬ࡳࡳࠨᇃ"),
        bstack1ll1l1_opy_ (u"ࠧࡽࡨࡦࡰࠥᇄ"),
    ],
    bstack1ll1l1_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠴࡭ࡢ࡫ࡱ࠲ࡘ࡫ࡳࡴ࡫ࡲࡲࠧᇅ"): [bstack1ll1l1_opy_ (u"ࠢࡴࡶࡤࡶࡹࡶࡡࡵࡪࠥᇆ"), bstack1ll1l1_opy_ (u"ࠣࡶࡨࡷࡹࡹࡦࡢ࡫࡯ࡩࡩࠨᇇ"), bstack1ll1l1_opy_ (u"ࠤࡷࡩࡸࡺࡳࡤࡱ࡯ࡰࡪࡩࡴࡦࡦࠥᇈ"), bstack1ll1l1_opy_ (u"ࠥ࡭ࡹ࡫࡭ࡴࠤᇉ")],
    bstack1ll1l1_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠲ࡨࡵ࡮ࡧ࡫ࡪ࠲ࡈࡵ࡮ࡧ࡫ࡪࠦᇊ"): [bstack1ll1l1_opy_ (u"ࠧ࡯࡮ࡷࡱࡦࡥࡹ࡯࡯࡯ࡡࡳࡥࡷࡧ࡭ࡴࠤᇋ"), bstack1ll1l1_opy_ (u"ࠨࡡࡳࡩࡶࠦᇌ")],
    bstack1ll1l1_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠮ࡧ࡫ࡻࡸࡺࡸࡥࡴ࠰ࡉ࡭ࡽࡺࡵࡳࡧࡇࡩ࡫ࠨᇍ"): [bstack1ll1l1_opy_ (u"ࠣࡵࡦࡳࡵ࡫ࠢᇎ"), bstack1ll1l1_opy_ (u"ࠤࡤࡶ࡬ࡴࡡ࡮ࡧࠥᇏ"), bstack1ll1l1_opy_ (u"ࠥࡪࡺࡴࡣࠣᇐ"), bstack1ll1l1_opy_ (u"ࠦࡵࡧࡲࡢ࡯ࡶࠦᇑ"), bstack1ll1l1_opy_ (u"ࠧࡻ࡮ࡪࡶࡷࡩࡸࡺࠢᇒ"), bstack1ll1l1_opy_ (u"ࠨࡩࡥࡵࠥᇓ")],
    bstack1ll1l1_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠮ࡧ࡫ࡻࡸࡺࡸࡥࡴ࠰ࡖࡹࡧࡘࡥࡲࡷࡨࡷࡹࠨᇔ"): [bstack1ll1l1_opy_ (u"ࠣࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࠨᇕ"), bstack1ll1l1_opy_ (u"ࠤࡳࡥࡷࡧ࡭ࠣᇖ"), bstack1ll1l1_opy_ (u"ࠥࡴࡦࡸࡡ࡮ࡡ࡬ࡲࡩ࡫ࡸࠣᇗ")],
    bstack1ll1l1_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠲ࡷࡻ࡮࡯ࡧࡵ࠲ࡈࡧ࡬࡭ࡋࡱࡪࡴࠨᇘ"): [bstack1ll1l1_opy_ (u"ࠧࡽࡨࡦࡰࠥᇙ"), bstack1ll1l1_opy_ (u"ࠨࡲࡦࡵࡸࡰࡹࠨᇚ")],
    bstack1ll1l1_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠮࡮ࡣࡵ࡯࠳ࡹࡴࡳࡷࡦࡸࡺࡸࡥࡴ࠰ࡑࡳࡩ࡫ࡋࡦࡻࡺࡳࡷࡪࡳࠣᇛ"): [bstack1ll1l1_opy_ (u"ࠣࡰࡲࡨࡪࠨᇜ"), bstack1ll1l1_opy_ (u"ࠤࡳࡥࡷ࡫࡮ࡵࠤᇝ")],
    bstack1ll1l1_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠱ࡱࡦࡸ࡫࠯ࡵࡷࡶࡺࡩࡴࡶࡴࡨࡷ࠳ࡓࡡࡳ࡭ࠥᇞ"): [bstack1ll1l1_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᇟ"), bstack1ll1l1_opy_ (u"ࠧࡧࡲࡨࡵࠥᇠ"), bstack1ll1l1_opy_ (u"ࠨ࡫ࡸࡣࡵ࡫ࡸࠨᇡ")],
}
_1ll111ll11l_opy_ = set()
class bstack1lll1111l11_opy_(bstack1lll1llll11_opy_):
    bstack1ll111l11l1_opy_ = bstack1ll1l1_opy_ (u"ࠢࡵࡧࡶࡸࡤࡪࡥࡧࡧࡵࡶࡪࡪࠢᇢ")
    bstack1l1lll1llll_opy_ = bstack1ll1l1_opy_ (u"ࠣࡋࡑࡊࡔࠨᇣ")
    bstack1l1lll11ll1_opy_ = bstack1ll1l1_opy_ (u"ࠤࡈࡖࡗࡕࡒࠣᇤ")
    bstack1ll1111l11l_opy_: Callable
    bstack1l1llll1ll1_opy_: Callable
    def __init__(self, bstack1lllll1l11l_opy_, bstack1lll1llllll_opy_):
        super().__init__()
        self.bstack1ll1l11lll1_opy_ = bstack1lll1llllll_opy_
        if os.getenv(bstack1ll1l1_opy_ (u"ࠥࡗࡉࡑ࡟ࡄࡎࡌࡣࡋࡒࡁࡈࡡࡒ࠵࠶࡟ࠢᇥ"), bstack1ll1l1_opy_ (u"ࠦ࠶ࠨᇦ")) != bstack1ll1l1_opy_ (u"ࠧ࠷ࠢᇧ") or not self.is_enabled():
            self.logger.warning(bstack1ll1l1_opy_ (u"ࠨࠢᇨ") + str(self.__class__.__name__) + bstack1ll1l1_opy_ (u"ࠢࠡࡦ࡬ࡷࡦࡨ࡬ࡦࡦࠥᇩ"))
            return
        TestFramework.bstack1ll1l11l1l1_opy_((bstack1lllllll1ll_opy_.TEST, bstack1lll1l11l1l_opy_.PRE), self.bstack1ll1l1111ll_opy_)
        TestFramework.bstack1ll1l11l1l1_opy_((bstack1lllllll1ll_opy_.TEST, bstack1lll1l11l1l_opy_.POST), self.bstack1ll1ll1llll_opy_)
        for event in bstack1lllllll1ll_opy_:
            for state in bstack1lll1l11l1l_opy_:
                TestFramework.bstack1ll1l11l1l1_opy_((event, state), self.bstack1ll1111lll1_opy_)
        bstack1lllll1l11l_opy_.bstack1ll1l11l1l1_opy_((bstack11111ll1l1_opy_.bstack111111l11l_opy_, bstack1111l1l1l1_opy_.POST), self.bstack1l1lll11lll_opy_)
        self.bstack1ll1111l11l_opy_ = sys.stdout.write
        sys.stdout.write = self.bstack1l1llll1111_opy_(bstack1lll1111l11_opy_.bstack1l1lll1llll_opy_, self.bstack1ll1111l11l_opy_)
        self.bstack1l1llll1ll1_opy_ = sys.stderr.write
        sys.stderr.write = self.bstack1l1llll1111_opy_(bstack1lll1111l11_opy_.bstack1l1lll11ll1_opy_, self.bstack1l1llll1ll1_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1ll1111lll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1l1l1l1_opy_,
        bstack1111l1l11l_opy_: Tuple[bstack1lllllll1ll_opy_, bstack1lll1l11l1l_opy_],
        *args,
        **kwargs,
    ):
        if f.bstack1l1lllll11l_opy_() and instance:
            bstack1ll111111l1_opy_ = datetime.now()
            test_framework_state, test_hook_state = bstack1111l1l11l_opy_
            if test_framework_state == bstack1lllllll1ll_opy_.SETUP_FIXTURE:
                return
            elif test_framework_state == bstack1lllllll1ll_opy_.LOG:
                bstack1ll11l1l1_opy_ = datetime.now()
                entries = f.bstack1ll111ll1l1_opy_(instance, bstack1111l1l11l_opy_)
                if entries:
                    self.bstack1l1llll1lll_opy_(instance, entries)
                    instance.bstack11lll1l111_opy_(bstack1ll1l1_opy_ (u"ࠣࡩࡵࡴࡨࡀࡳࡦࡰࡧࡣࡱࡵࡧࡠࡥࡵࡩࡦࡺࡥࡥࡡࡨࡺࡪࡴࡴࠣᇪ"), datetime.now() - bstack1ll11l1l1_opy_)
                    f.bstack1ll111lll1l_opy_(instance, bstack1111l1l11l_opy_)
                instance.bstack11lll1l111_opy_(bstack1ll1l1_opy_ (u"ࠤࡲ࠵࠶ࡿ࠺ࡰࡰࡢࡥࡱࡲ࡟ࡵࡧࡶࡸࡤ࡫ࡶࡦࡰࡷࡷࠧᇫ"), datetime.now() - bstack1ll111111l1_opy_)
                return # bstack1l1llllllll_opy_ not send this event with the bstack1l1llll111l_opy_ bstack1ll111ll111_opy_
            elif (
                test_framework_state == bstack1lllllll1ll_opy_.TEST
                and test_hook_state == bstack1lll1l11l1l_opy_.POST
                and not f.bstack11111l1l1l_opy_(instance, TestFramework.bstack1l1lll111l1_opy_)
            ):
                self.logger.warning(bstack1ll1l1_opy_ (u"ࠥࡨࡷࡵࡰࡱ࡫ࡱ࡫ࠥࡪࡵࡦࠢࡷࡳࠥࡲࡡࡤ࡭ࠣࡳ࡫ࠦࡲࡦࡵࡸࡰࡹࡹࠠࠣᇬ") + str(TestFramework.bstack11111l1l1l_opy_(instance, TestFramework.bstack1l1lll111l1_opy_)) + bstack1ll1l1_opy_ (u"ࠦࠧᇭ"))
                f.bstack1111111111_opy_(instance, bstack1lll1111l11_opy_.bstack1ll111l11l1_opy_, True)
                return # bstack1l1llllllll_opy_ not send this event bstack1ll1111llll_opy_ bstack1l1llll11l1_opy_
            elif (
                f.bstack11111lllll_opy_(instance, bstack1lll1111l11_opy_.bstack1ll111l11l1_opy_, False)
                and test_framework_state == bstack1lllllll1ll_opy_.LOG_REPORT
                and test_hook_state == bstack1lll1l11l1l_opy_.POST
                and f.bstack11111l1l1l_opy_(instance, TestFramework.bstack1l1lll111l1_opy_)
            ):
                self.logger.warning(bstack1ll1l1_opy_ (u"ࠧ࡯࡮࡫ࡧࡦࡸ࡮ࡴࡧࠡࡖࡨࡷࡹࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡔࡶࡤࡸࡪ࠴ࡔࡆࡕࡗ࠰࡚ࠥࡥࡴࡶࡋࡳࡴࡱࡓࡵࡣࡷࡩ࠳ࡖࡏࡔࡖࠣࠦᇮ") + str(TestFramework.bstack11111l1l1l_opy_(instance, TestFramework.bstack1l1lll111l1_opy_)) + bstack1ll1l1_opy_ (u"ࠨࠢᇯ"))
                self.bstack1ll1111lll1_opy_(f, instance, (bstack1lllllll1ll_opy_.TEST, bstack1lll1l11l1l_opy_.POST), *args, **kwargs)
            bstack1ll11l1l1_opy_ = datetime.now()
            data = instance.data.copy()
            bstack1l1lll1lll1_opy_ = sorted(
                filter(lambda x: x.get(bstack1ll1l1_opy_ (u"ࠢࡦࡸࡨࡲࡹࡥࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠥᇰ"), None), data.pop(bstack1ll1l1_opy_ (u"ࠣࡶࡨࡷࡹࡥࡦࡪࡺࡷࡹࡷ࡫ࡳࠣᇱ"), {}).values()),
                key=lambda x: x[bstack1ll1l1_opy_ (u"ࠤࡨࡺࡪࡴࡴࡠࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠧᇲ")],
            )
            if bstack1lll1l1l11l_opy_.bstack1l1lll1l1l1_opy_ in data:
                data.pop(bstack1lll1l1l11l_opy_.bstack1l1lll1l1l1_opy_)
            data.update({bstack1ll1l1_opy_ (u"ࠥࡸࡪࡹࡴࡠࡨ࡬ࡼࡹࡻࡲࡦࡵࠥᇳ"): bstack1l1lll1lll1_opy_})
            instance.bstack11lll1l111_opy_(bstack1ll1l1_opy_ (u"ࠦ࡯ࡹ࡯࡯࠼ࡷࡩࡸࡺ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡴࠤᇴ"), datetime.now() - bstack1ll11l1l1_opy_)
            bstack1ll11l1l1_opy_ = datetime.now()
            event_json = dumps(data, cls=bstack1l1llllll1l_opy_)
            instance.bstack11lll1l111_opy_(bstack1ll1l1_opy_ (u"ࠧࡰࡳࡰࡰ࠽ࡳࡳࡥࡡ࡭࡮ࡢࡸࡪࡹࡴࡠࡧࡹࡩࡳࡺࡳࠣᇵ"), datetime.now() - bstack1ll11l1l1_opy_)
            self.bstack1ll111ll111_opy_(instance, bstack1111l1l11l_opy_, event_json=event_json)
            instance.bstack11lll1l111_opy_(bstack1ll1l1_opy_ (u"ࠨ࡯࠲࠳ࡼ࠾ࡴࡴ࡟ࡢ࡮࡯ࡣࡹ࡫ࡳࡵࡡࡨࡺࡪࡴࡴࡴࠤᇶ"), datetime.now() - bstack1ll111111l1_opy_)
    def bstack1ll1l1111ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1l1l1l1_opy_,
        bstack1111l1l11l_opy_: Tuple[bstack1lllllll1ll_opy_, bstack1lll1l11l1l_opy_],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack1l111l1111_opy_ import bstack1lll111l11l_opy_
        bstack1ll1l1l111l_opy_ = bstack1lll111l11l_opy_.bstack1ll1ll111ll_opy_(EVENTS.bstack11lllllll1_opy_.value)
        self.bstack1ll1l11lll1_opy_.bstack1l1lll1l111_opy_(instance, f, bstack1111l1l11l_opy_, *args, **kwargs)
        bstack1lll111l11l_opy_.end(EVENTS.bstack11lllllll1_opy_.value, bstack1ll1l1l111l_opy_ + bstack1ll1l1_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢᇷ"), bstack1ll1l1l111l_opy_ + bstack1ll1l1_opy_ (u"ࠣ࠼ࡨࡲࡩࠨᇸ"), status=True, failure=None, test_name=None)
    def bstack1ll1ll1llll_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1l1l1l1_opy_,
        bstack1111l1l11l_opy_: Tuple[bstack1lllllll1ll_opy_, bstack1lll1l11l1l_opy_],
        *args,
        **kwargs,
    ):
        req = self.bstack1ll1l11lll1_opy_.bstack1ll11l11l11_opy_(instance, f, bstack1111l1l11l_opy_, *args, **kwargs)
        self.bstack1l1lll11l11_opy_(f, instance, req)
    @measure(event_name=EVENTS.bstack1l1lllllll1_opy_, stage=STAGE.bstack1llll1l1_opy_)
    def bstack1l1lll11l11_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1l1l1l1_opy_,
        req: structs.TestSessionEventRequest
    ):
        if not req:
            self.logger.debug(bstack1ll1l1_opy_ (u"ࠤࡖ࡯࡮ࡶࡰࡪࡰࡪࠤ࡙࡫ࡳࡵࡕࡨࡷࡸ࡯࡯࡯ࡇࡹࡩࡳࡺࠠࡨࡔࡓࡇࠥࡩࡡ࡭࡮࠽ࠤࡓࡵࠠࡷࡣ࡯࡭ࡩࠦࡲࡦࡳࡸࡩࡸࡺࠠࡥࡣࡷࡥࠧᇹ"))
            return
        bstack1ll11l1l1_opy_ = datetime.now()
        try:
            r = self.bstack1llllll1ll1_opy_.TestSessionEvent(req)
            instance.bstack11lll1l111_opy_(bstack1ll1l1_opy_ (u"ࠥ࡫ࡷࡶࡣ࠻ࡵࡨࡲࡩࡥࡴࡦࡵࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡫ࡶࡦࡰࡷࠦᇺ"), datetime.now() - bstack1ll11l1l1_opy_)
            f.bstack1111111111_opy_(instance, self.bstack1ll1l11lll1_opy_.bstack1ll111llll1_opy_, r.success)
            if not r.success:
                self.logger.info(bstack1ll1l1_opy_ (u"ࠦࡷ࡫ࡣࡦ࡫ࡹࡩࡩࠦࡦࡳࡱࡰࠤࡸ࡫ࡲࡷࡧࡵ࠾ࠥࠨᇻ") + str(r) + bstack1ll1l1_opy_ (u"ࠧࠨᇼ"))
        except grpc.RpcError as e:
            self.logger.error(bstack1ll1l1_opy_ (u"ࠨࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࠦᇽ") + str(e) + bstack1ll1l1_opy_ (u"ࠢࠣᇾ"))
            traceback.print_exc()
            raise e
    def bstack1l1lll11lll_opy_(
        self,
        f: bstack1lll1ll1lll_opy_,
        _driver: object,
        exec: Tuple[bstack1llllllllll_opy_, str],
        _1ll111l111l_opy_: Tuple[bstack11111ll1l1_opy_, bstack1111l1l1l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if not bstack1lll1ll1lll_opy_.bstack1ll1l1llll1_opy_(method_name):
            return
        if f.bstack1ll1l1ll111_opy_(*args) == bstack1lll1ll1lll_opy_.bstack1ll1111ll1l_opy_:
            bstack1ll111111l1_opy_ = datetime.now()
            screenshot = result.get(bstack1ll1l1_opy_ (u"ࠣࡸࡤࡰࡺ࡫ࠢᇿ"), None) if isinstance(result, dict) else None
            if not isinstance(screenshot, str) or len(screenshot) <= 0:
                self.logger.warning(bstack1ll1l1_opy_ (u"ࠤ࡬ࡲࡻࡧ࡬ࡪࡦࠣࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠠࡪ࡯ࡤ࡫ࡪࠦࡢࡢࡵࡨ࠺࠹ࠦࡳࡵࡴࠥሀ"))
                return
            bstack1l1lll1l11l_opy_ = self.bstack1l1lll1111l_opy_(instance)
            if bstack1l1lll1l11l_opy_:
                entry = bstack1llll1l1lll_opy_(TestFramework.bstack1ll11l111ll_opy_, screenshot)
                self.bstack1l1llll1lll_opy_(bstack1l1lll1l11l_opy_, [entry])
                instance.bstack11lll1l111_opy_(bstack1ll1l1_opy_ (u"ࠥࡳ࠶࠷ࡹ࠻ࡱࡱࡣࡦ࡬ࡴࡦࡴࡢࡩࡽ࡫ࡣࡶࡶࡨࠦሁ"), datetime.now() - bstack1ll111111l1_opy_)
            else:
                self.logger.warning(bstack1ll1l1_opy_ (u"ࠦࡺࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡥࡧࡷࡩࡷࡳࡩ࡯ࡧࠣࡸࡪࡹࡴࠡࡨࡲࡶࠥࡽࡨࡪࡥ࡫ࠤࡹ࡮ࡩࡴࠢࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࠦࡷࡢࡵࠣࡸࡦࡱࡥ࡯ࠢࡥࡽࠥࡪࡲࡪࡸࡨࡶࡂࠦࡻࡾࠤሂ").format(instance.ref()))
        event = {}
        bstack1l1lll1l11l_opy_ = self.bstack1l1lll1111l_opy_(instance)
        if bstack1l1lll1l11l_opy_:
            self.bstack1ll1111111l_opy_(event, bstack1l1lll1l11l_opy_)
            if event.get(bstack1ll1l1_opy_ (u"ࠧࡲ࡯ࡨࡵࠥሃ")):
                self.bstack1l1llll1lll_opy_(bstack1l1lll1l11l_opy_, event[bstack1ll1l1_opy_ (u"ࠨ࡬ࡰࡩࡶࠦሄ")])
            else:
                self.logger.info(bstack1ll1l1_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡨࡪࡺࡥࡳ࡯࡬ࡲࡪࠦ࡬ࡰࡩࡶࠤ࡫ࡵࡲࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࠥ࡫ࡶࡦࡰࡷࠦህ"))
    @measure(event_name=EVENTS.bstack1ll11111l11_opy_, stage=STAGE.bstack1llll1l1_opy_)
    def bstack1l1llll1lll_opy_(
        self,
        bstack1l1lll1l11l_opy_: bstack1lll1l1l1l1_opy_,
        entries: List[bstack1llll1l1lll_opy_],
    ):
        self.bstack1ll1l11ll11_opy_()
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack11111lllll_opy_(bstack1l1lll1l11l_opy_, TestFramework.bstack1ll11llll1l_opy_)
        req.execution_context.hash = str(bstack1l1lll1l11l_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l1lll1l11l_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l1lll1l11l_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack11111lllll_opy_(bstack1l1lll1l11l_opy_, TestFramework.bstack1ll1ll1l1ll_opy_)
            log_entry.test_framework_version = TestFramework.bstack11111lllll_opy_(bstack1l1lll1l11l_opy_, TestFramework.bstack1ll111l1lll_opy_)
            log_entry.uuid = TestFramework.bstack11111lllll_opy_(bstack1l1lll1l11l_opy_, TestFramework.bstack1ll1ll1ll11_opy_)
            log_entry.test_framework_state = bstack1l1lll1l11l_opy_.state.name
            log_entry.message = entry.message.encode(bstack1ll1l1_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢሆ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            if isinstance(entry.level, str) and len(entry.level.strip()) > 0:
                log_entry.level = entry.level.strip()
            if entry.kind == bstack1ll1l1_opy_ (u"ࠤࡗࡉࡘ࡚࡟ࡂࡖࡗࡅࡈࡎࡍࡆࡐࡗࠦሇ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1ll111l1l1l_opy_
                log_entry.file_path = entry.bstack1l11_opy_
        def bstack1l1llll1l11_opy_():
            bstack1ll11l1l1_opy_ = datetime.now()
            try:
                self.bstack1llllll1ll1_opy_.LogCreatedEvent(req)
                if entry.kind == TestFramework.bstack1ll11l111ll_opy_:
                    bstack1l1lll1l11l_opy_.bstack11lll1l111_opy_(bstack1ll1l1_opy_ (u"ࠥ࡫ࡷࡶࡣ࠻ࡵࡨࡲࡩࡥ࡬ࡰࡩࡢࡧࡷ࡫ࡡࡵࡧࡧࡣࡪࡼࡥ࡯ࡶࡢࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠢለ"), datetime.now() - bstack1ll11l1l1_opy_)
                elif entry.kind == TestFramework.bstack1ll111l1111_opy_:
                    bstack1l1lll1l11l_opy_.bstack11lll1l111_opy_(bstack1ll1l1_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡶࡩࡳࡪ࡟࡭ࡱࡪࡣࡨࡸࡥࡢࡶࡨࡨࡤ࡫ࡶࡦࡰࡷࡣࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠣሉ"), datetime.now() - bstack1ll11l1l1_opy_)
                else:
                    bstack1l1lll1l11l_opy_.bstack11lll1l111_opy_(bstack1ll1l1_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡷࡪࡴࡤࡠ࡮ࡲ࡫ࡤࡩࡲࡦࡣࡷࡩࡩࡥࡥࡷࡧࡱࡸࡤࡲ࡯ࡨࠤሊ"), datetime.now() - bstack1ll11l1l1_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1ll1l1_opy_ (u"ࠨࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࠦላ") + str(e))
                traceback.print_exc()
                raise e
        self.bstack1111l1ll11_opy_.enqueue(bstack1l1llll1l11_opy_)
    @measure(event_name=EVENTS.bstack1l1lll1l1ll_opy_, stage=STAGE.bstack1llll1l1_opy_)
    def bstack1ll111ll111_opy_(
        self,
        instance: bstack1lll1l1l1l1_opy_,
        bstack1111l1l11l_opy_: Tuple[bstack1lllllll1ll_opy_, bstack1lll1l11l1l_opy_],
        event_json=None,
    ):
        self.bstack1ll1l11ll11_opy_()
        req = structs.TestFrameworkEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack11111lllll_opy_(instance, TestFramework.bstack1ll11llll1l_opy_)
        req.test_framework_name = TestFramework.bstack11111lllll_opy_(instance, TestFramework.bstack1ll1ll1l1ll_opy_)
        req.test_framework_version = TestFramework.bstack11111lllll_opy_(instance, TestFramework.bstack1ll111l1lll_opy_)
        req.test_framework_state = bstack1111l1l11l_opy_[0].name
        req.test_hook_state = bstack1111l1l11l_opy_[1].name
        started_at = TestFramework.bstack11111lllll_opy_(instance, TestFramework.bstack1l1lllll1l1_opy_, None)
        if started_at:
            req.started_at = started_at.isoformat()
        ended_at = TestFramework.bstack11111lllll_opy_(instance, TestFramework.bstack1ll11111l1l_opy_, None)
        if ended_at:
            req.ended_at = ended_at.isoformat()
        req.uuid = instance.ref()
        req.event_json = (event_json if event_json else dumps(instance.data, cls=bstack1l1llllll1l_opy_)).encode(bstack1ll1l1_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨሌ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        def bstack1l1llll1l11_opy_():
            bstack1ll11l1l1_opy_ = datetime.now()
            try:
                self.bstack1llllll1ll1_opy_.TestFrameworkEvent(req)
                instance.bstack11lll1l111_opy_(bstack1ll1l1_opy_ (u"ࠣࡩࡵࡴࡨࡀࡳࡦࡰࡧࡣࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤ࡫ࡶࡦࡰࡷࠦል"), datetime.now() - bstack1ll11l1l1_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1ll1l1_opy_ (u"ࠤࡵࡴࡨ࠳ࡥࡳࡴࡲࡶ࠿ࠦࠢሎ") + str(e))
                traceback.print_exc()
                raise e
        self.bstack1111l1ll11_opy_.enqueue(bstack1l1llll1l11_opy_)
    def bstack1l1lll1111l_opy_(self, instance: bstack1llllllllll_opy_):
        bstack1ll111l1ll1_opy_ = TestFramework.bstack11111l1lll_opy_(instance.context)
        for t in bstack1ll111l1ll1_opy_:
            bstack1ll111l1l11_opy_ = TestFramework.bstack11111lllll_opy_(t, bstack1lll1l1l11l_opy_.bstack1l1lll1l1l1_opy_, [])
            if any(instance is d[1] for d in bstack1ll111l1l11_opy_):
                return t
    def bstack1ll1111l111_opy_(self, message):
        self.bstack1ll1111l11l_opy_(message + bstack1ll1l1_opy_ (u"ࠥࡠࡳࠨሏ"))
    def log_error(self, message):
        self.bstack1l1llll1ll1_opy_(message + bstack1ll1l1_opy_ (u"ࠦࡡࡴࠢሐ"))
    def bstack1l1llll1111_opy_(self, level, original_func):
        def bstack1ll1111l1ll_opy_(*args):
            return_value = original_func(*args)
            if not args or not isinstance(args[0], str) or not args[0].strip():
                return return_value
            message = args[0].strip()
            bstack1ll111l1ll1_opy_ = TestFramework.bstack1l1lll1ll1l_opy_()
            if not bstack1ll111l1ll1_opy_:
                return return_value
            bstack1l1lll1l11l_opy_ = next(
                (
                    instance
                    for instance in bstack1ll111l1ll1_opy_
                    if TestFramework.bstack11111l1l1l_opy_(instance, TestFramework.bstack1ll1ll1ll11_opy_)
                ),
                None,
            )
            if not bstack1l1lll1l11l_opy_:
                return
            entry = bstack1llll1l1lll_opy_(TestFramework.bstack1l1lll1ll11_opy_, message, level)
            self.bstack1l1llll1lll_opy_(bstack1l1lll1l11l_opy_, [entry])
            return return_value
        return bstack1ll1111l1ll_opy_
    def bstack1ll1111111l_opy_(self, event: dict, instance=None) -> None:
        global _1ll111ll11l_opy_
        levels = [bstack1ll1l1_opy_ (u"࡚ࠧࡥࡴࡶࡏࡩࡻ࡫࡬ࠣሑ"), bstack1ll1l1_opy_ (u"ࠨࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࠥሒ")]
        bstack1ll1111l1l1_opy_ = bstack1ll1l1_opy_ (u"ࠢࠣሓ")
        if instance is not None:
            try:
                bstack1ll1111l1l1_opy_ = TestFramework.bstack11111lllll_opy_(instance, TestFramework.bstack1ll1ll1ll11_opy_)
            except Exception as e:
                self.logger.warning(bstack1ll1l1_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡷࡸ࡭ࡩࠦࡦࡳࡱࡰࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࠨሔ").format(e))
        bstack1ll111l11ll_opy_ = []
        try:
            for level in levels:
                platform_index = os.environ[bstack1ll1l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩሕ")]
                bstack1ll11l1111l_opy_ = os.path.join(bstack1l1lll11l1l_opy_, (bstack1l1lllll111_opy_ + str(platform_index)), level)
                if not os.path.isdir(bstack1ll11l1111l_opy_):
                    self.logger.info(bstack1ll1l1_opy_ (u"ࠥࡈ࡮ࡸࡥࡤࡶࡲࡶࡾࠦ࡮ࡰࡶࠣࡴࡷ࡫ࡳࡦࡰࡷࠤ࡫ࡵࡲࠡࡲࡵࡳࡨ࡫ࡳࡴ࡫ࡱ࡫࡚ࠥࡥࡴࡶࠣࡥࡳࡪࠠࡃࡷ࡬ࡰࡩࠦ࡬ࡦࡸࡨࡰࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵࠥሖ").format(bstack1ll11l1111l_opy_))
                file_names = os.listdir(bstack1ll11l1111l_opy_)
                for file_name in file_names:
                    file_path = os.path.join(bstack1ll11l1111l_opy_, file_name)
                    abs_path = os.path.abspath(file_path)
                    if abs_path in _1ll111ll11l_opy_:
                        self.logger.info(bstack1ll1l1_opy_ (u"ࠦࡕࡧࡴࡩࠢࡤࡰࡷ࡫ࡡࡥࡻࠣࡴࡷࡵࡣࡦࡵࡶࡩࡩࠦࡻࡾࠤሗ").format(abs_path))
                        continue
                    if os.path.isfile(file_path):
                        try:
                            bstack1l1llllll11_opy_ = os.path.getmtime(file_path)
                            timestamp = datetime.fromtimestamp(bstack1l1llllll11_opy_, tz=timezone.utc).isoformat()
                            file_size = os.path.getsize(file_path)
                            if level == bstack1ll1l1_opy_ (u"࡚ࠧࡥࡴࡶࡏࡩࡻ࡫࡬ࠣመ"):
                                entry = bstack1llll1l1lll_opy_(
                                    kind=bstack1ll1l1_opy_ (u"ࠨࡔࡆࡕࡗࡣࡆ࡚ࡔࡂࡅࡋࡑࡊࡔࡔࠣሙ"),
                                    message=bstack1ll1l1_opy_ (u"ࠢࠣሚ"),
                                    level=level,
                                    timestamp=timestamp,
                                    fileName=file_name,
                                    bstack1ll111l1l1l_opy_=file_size,
                                    bstack1ll11111ll1_opy_=bstack1ll1l1_opy_ (u"ࠣࡏࡄࡒ࡚ࡇࡌࡠࡗࡓࡐࡔࡇࡄࠣማ"),
                                    bstack1l11_opy_=os.path.abspath(file_path),
                                    bstack1llll1ll11_opy_=bstack1ll1111l1l1_opy_
                                )
                            elif level == bstack1ll1l1_opy_ (u"ࠤࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࠨሜ"):
                                entry = bstack1llll1l1lll_opy_(
                                    kind=bstack1ll1l1_opy_ (u"ࠥࡘࡊ࡙ࡔࡠࡃࡗࡘࡆࡉࡈࡎࡇࡑࡘࠧም"),
                                    message=bstack1ll1l1_opy_ (u"ࠦࠧሞ"),
                                    level=level,
                                    timestamp=timestamp,
                                    fileName=file_name,
                                    bstack1ll111l1l1l_opy_=file_size,
                                    bstack1ll11111ll1_opy_=bstack1ll1l1_opy_ (u"ࠧࡓࡁࡏࡗࡄࡐࡤ࡛ࡐࡍࡑࡄࡈࠧሟ"),
                                    bstack1l11_opy_=os.path.abspath(file_path),
                                    bstack1ll11111111_opy_=bstack1ll1111l1l1_opy_
                                )
                            bstack1ll111l11ll_opy_.append(entry)
                            _1ll111ll11l_opy_.add(abs_path)
                        except Exception as bstack1ll11l111l1_opy_:
                            self.logger.error(bstack1ll1l1_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡵࡥ࡮ࡹࡥࡥࠢࡺ࡬ࡪࡴࠠࡱࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴࠤሠ").format(bstack1ll11l111l1_opy_))
        except Exception as e:
            self.logger.error(bstack1ll1l1_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡶࡦ࡯ࡳࡦࡦࠣࡻ࡭࡫࡮ࠡࡲࡵࡳࡨ࡫ࡳࡴ࡫ࡱ࡫ࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵࠥሡ").format(e))
        event[bstack1ll1l1_opy_ (u"ࠣ࡮ࡲ࡫ࡸࠨሢ")] = bstack1ll111l11ll_opy_
class bstack1l1llllll1l_opy_(JSONEncoder):
    def __init__(self, **kwargs):
        self.bstack1ll111111ll_opy_ = set()
        kwargs[bstack1ll1l1_opy_ (u"ࠤࡶ࡯࡮ࡶ࡫ࡦࡻࡶࠦሣ")] = True
        super().__init__(**kwargs)
    def default(self, obj):
        return bstack1l1lll111ll_opy_(obj, self.bstack1ll111111ll_opy_)
def bstack1ll111ll1ll_opy_(obj):
    return isinstance(obj, (str, int, float, bool, type(None)))
def bstack1l1lll111ll_opy_(obj, bstack1ll111111ll_opy_=None, max_depth=3):
    if bstack1ll111111ll_opy_ is None:
        bstack1ll111111ll_opy_ = set()
    if id(obj) in bstack1ll111111ll_opy_ or max_depth <= 0:
        return None
    max_depth -= 1
    bstack1ll111111ll_opy_.add(id(obj))
    if isinstance(obj, datetime):
        return obj.isoformat()
    bstack1l1lllll1ll_opy_ = TestFramework.bstack1ll11l11111_opy_(obj)
    bstack1ll11111lll_opy_ = next((k.lower() in bstack1l1lllll1ll_opy_.lower() for k in bstack1ll111lllll_opy_.keys()), None)
    if bstack1ll11111lll_opy_:
        obj = TestFramework.bstack1ll111lll11_opy_(obj, bstack1ll111lllll_opy_[bstack1ll11111lll_opy_])
    if not isinstance(obj, dict):
        keys = []
        if hasattr(obj, bstack1ll1l1_opy_ (u"ࠥࡣࡤࡹ࡬ࡰࡶࡶࡣࡤࠨሤ")):
            keys = getattr(obj, bstack1ll1l1_opy_ (u"ࠦࡤࡥࡳ࡭ࡱࡷࡷࡤࡥࠢሥ"), [])
        elif hasattr(obj, bstack1ll1l1_opy_ (u"ࠧࡥ࡟ࡥ࡫ࡦࡸࡤࡥࠢሦ")):
            keys = getattr(obj, bstack1ll1l1_opy_ (u"ࠨ࡟ࡠࡦ࡬ࡧࡹࡥ࡟ࠣሧ"), {}).keys()
        else:
            keys = dir(obj)
        obj = {k: getattr(obj, k, None) for k in keys if not str(k).startswith(bstack1ll1l1_opy_ (u"ࠢࡠࠤረ"))}
        if not obj and bstack1l1lllll1ll_opy_ == bstack1ll1l1_opy_ (u"ࠣࡲࡤࡸ࡭ࡲࡩࡣ࠰ࡓࡳࡸ࡯ࡸࡑࡣࡷ࡬ࠧሩ"):
            obj = {bstack1ll1l1_opy_ (u"ࠤࡳࡥࡹ࡮ࠢሪ"): str(obj)}
    result = {}
    for key, value in obj.items():
        if not bstack1ll111ll1ll_opy_(key) or str(key).startswith(bstack1ll1l1_opy_ (u"ࠥࡣࠧራ")):
            continue
        if value is not None and bstack1ll111ll1ll_opy_(value):
            result[key] = value
        elif isinstance(value, dict):
            r = bstack1l1lll111ll_opy_(value, bstack1ll111111ll_opy_, max_depth)
            if r is not None:
                result[key] = r
        elif isinstance(value, (list, tuple, set, frozenset)):
            result[key] = list(filter(None, [bstack1l1lll111ll_opy_(o, bstack1ll111111ll_opy_, max_depth) for o in value]))
    return result or None